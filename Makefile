.DEFAULT_GOAL := help
export UID := $(shell id -u)
export GID := $(shell id -g)
COMPOSE := docker compose
RUN := $(COMPOSE) run --rm --no-deps livro

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

build: ## Constrói a imagem Docker
	$(COMPOSE) build

preview: ## Preview com hot-reload em http://localhost:4201
	$(COMPOSE) up

render: ## Renderiza o livro para _book/
	$(RUN) quarto render

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

.PHONY: help build preview render offline teste shell check lock clean
