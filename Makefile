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

offline: ## Renderiza SEM REDE — prova que nenhum chunk depende da internet
# `docker compose run` não tem flag --network (Compose v2), então esta é a
# única forma de provar o isolamento. Exige `make build` antes.
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
