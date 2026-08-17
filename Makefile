.DEFAULT_GOAL := help
export UID := $(shell id -u)
export GID := $(shell id -g)
COMPOSE := docker compose
RUN := $(COMPOSE) run --rm --no-deps livro

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

build: ## Constrói a imagem Docker
	$(COMPOSE) build

preview: ## Preview com hot-reload em http://localhost:4201
	$(COMPOSE) up

render: ## Renderiza o livro para _book/ (retentativa automática, um render por vez)
# ATENÇÃO: este alvo é SERIALIZADO. Dois `quarto render` simultâneos sobre o mesmo
# `_freeze/` corrompem o cache — um grava o resultado de um chunk enquanto o outro
# lê o índice, e o livro sai com saída trocada entre páginas, sem erro nenhum na
# tela. O livro é escrito por vários agentes em paralelo, cada um responsável por um
# capítulo, então isso deixou de ser hipótese e virou questão de tempo.
#
# O lock é um `mkdir`, que é atômico em qualquer POSIX (`flock` não existe no macOS
# de fábrica). O `trap` devolve o lock mesmo se o render abortar ou levar Ctrl-C.
# Depois de 30 min esperando, o lock é considerado preso — um agente morto não pode
# bloquear o livro para sempre — e é removido com aviso na tela.
#
# No macOS, o bind mount do Docker às vezes falha ao remover os diretórios
# `*_files` temporários que o Quarto cria e apaga no fim do render — eles ficam
# com `figure-html/` e `mediabag/` vazios dentro, e o `rmdir` estoura com
# "Directory not empty". NÃO é erro de conteúdo: as células todas executaram.
#
# A falha é aleatória (aborta num arquivo diferente a cada vez) e fica mais
# provável quanto mais figuras o livro tem. O remédio, medido: apagar o lixo da
# tentativa anterior e renderizar de novo COM o `_freeze` quente — aí poucos
# chunks reexecutam, a janela da corrida encolhe, e converge em duas ou três
# tentativas. Por isso este alvo NUNCA apaga o `_freeze`.
#
# Isto vive aqui, e não na cabeça de quem roda, porque a alternativa já custou
# horas: um agente ficou preso em laço tentando entender um render que abortava.
	@bash scripts/render-seguro.sh

refresh: ## Reexecuta UM capítulo do zero: make refresh CAP=10
# Use quando desconfiar que a página publicada não corresponde ao fonte. Apaga
# só o `_freeze/` daquele capítulo (não o do livro inteiro, que custa caro) e
# renderiza. É o remédio para o cache envenenado descrito em scripts/render-seguro.sh
# quando ele já aconteceu — o script previne dali em diante, este alvo limpa o
# que ficou para trás.
	@test -n "$(CAP)" || { echo "uso: make refresh CAP=10"; exit 1; }
	@test -d "content/cap$(CAP)" || { echo "content/cap$(CAP) não existe"; exit 1; }
	rm -rf "_freeze/content/cap$(CAP)"
	@bash scripts/render-seguro.sh

offline: ## Renderiza SEM REDE (limpa _freeze antes — veja o motivo abaixo)
# `docker compose run` não tem flag --network (Compose v2), então esta é a
# única forma de provar o isolamento. Exige `make build` antes.
#
# Apaga _freeze/ primeiro DE PROPÓSITO. Com freeze: auto, o Quarto reaproveita
# a saída congelada e não executa o chunk de novo se o .qmd não mudou — então
# um `make offline` de cache quente pode reportar sucesso sem rodar um único
# chunk, e não prova nada sobre depender ou não de rede. Isto não é um `rm -rf`
# por zelo: é o que torna este alvo honesto por construção, em vez de depender
# de quem roda lembrar de limpar o cache manualmente antes. O custo é que o
# próximo render fica mais lento (sem cache) — aceitável, porque este é um
# alvo rodado deliberadamente antes de publicar, não a cada save. O CI não é
# afetado: _freeze/ está no .gitignore, então um checkout limpo já começa frio.
	rm -rf _freeze
	docker run --rm --network none -u "$(UID):$(GID)" -e HOME=/tmp \
	  -v "$(PWD)":/livro -w /livro bases5-ciencia-de-dados:local quarto render

jupyter: ## Abre o JupyterLab em http://localhost:8901 (para dar aula)
# A raiz é /livro, não /livro/notebooks, para o aluno enxergar `dados/` e
# `scratch/` — e porque com o cwd na raiz a célula de preparo não precisa subir.
# Sem token: o compose prende a porta em 127.0.0.1, então só a máquina local
# alcança. Se você mudar aquele mapeamento, ponha o token de volta.
	$(COMPOSE) run --rm --service-ports livro \
	  jupyter lab --ip=0.0.0.0 --port=8901 --no-browser \
	  --ServerApp.token='' --ServerApp.password='' --ServerApp.root_dir=/livro

notebooks: ## Regenera os notebooks de aula a partir dos .qmd
# Os notebooks são DERIVADOS do livro, não uma segunda fonte. Editou um .qmd,
# rode isto. Editar o .ipynb à mão é trabalho perdido: o gerador sobrescreve.
	$(RUN) python scripts/gerar-notebooks.py

notebooks-teste: ## Executa todos os notebooks de ponta a ponta (demora; não grava saída)
# Esta é a verificação dos notebooks, análoga ao `quarto render` para o livro.
# Roda com o cwd em notebooks/, que é o caso mais apertado — o do aluno que
# abriu o Jupyter dentro da pasta e depende da célula de preparo achar a raiz.
	$(RUN) python scripts/executar-notebooks.py

teste: ## Roda a suíte de invariantes estruturais
	$(RUN) pytest tests/ -v

shell: ## Abre um shell dentro do container
	$(RUN) bash

check: ## Diagnóstico do Quarto dentro do container
	$(RUN) quarto check

lock: ## Regenera o uv.lock a partir do pyproject.toml
	uv lock

clean: ## Remove artefatos de render (inclusive o lixo que um render abortado deixa)
	rm -rf _book _freeze .quarto
# O Quarto cria .html e *_files durante o render e os apaga no final. Se o render
# aborta (o bind mount do Docker no macOS às vezes falha com "Directory not
# empty"), esse lixo fica — e TRAVA o render seguinte, que não consegue remover
# um diretório não vazio. Os *_files aparecem tanto em content/ quanto na raiz;
# os .html só em content/ (na raiz vive o spoiler.html, versionado, que NÃO pode
# ser apagado).
	find . -name '*_files' -type d -not -path './.git/*' -exec rm -rf {} + 2>/dev/null || true
	find content -name '*.html' -type f -delete 2>/dev/null || true
	find . -name '*.quarto_ipynb' -type f -not -path './.git/*' -delete 2>/dev/null || true
# Na raiz, apaga só o .html que tem um .qmd de mesmo nome: `index.html` é lixo de
# render (a capa vem de `index.qmd`), enquanto `spoiler.html` é versionado.
	@for html in ./*.html; do \
	  [ -e "$$html" ] || continue; \
	  [ -f "$${html%.html}.qmd" ] && rm -f "$$html"; \
	done; true

.PHONY: help build preview render refresh offline jupyter notebooks notebooks-teste teste shell check lock clean
