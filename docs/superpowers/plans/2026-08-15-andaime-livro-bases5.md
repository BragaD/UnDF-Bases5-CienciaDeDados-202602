# Andaime do livro Bases 5 — Ciência de Dados: Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir o andaime completo do livro Quarto da disciplina Bases 5 — 17 capítulos registrados, 105 arquivos `.qmd`, ambiente containerizado, CI publicando no GitHub Pages — com o Capítulo 9 (k-Vizinhos) escrito por inteiro como modelo de estilo.

**Architecture:** Livro Quarto (`type: book`) renderizado dentro de um container Docker que trava Python 3.12 + Quarto + dependências via `uv.lock`. O código do livro-texto entra vendorizado em `scratch/`, importado pelos chunks a partir da raiz do projeto (`execute-dir: project`). Os dados entram commitados em `dados/`; nenhum byte vem da rede em tempo de render, e isso é verificado por um render com `--network none`. Uma suíte `pytest` guarda as invariantes estruturais que o Quarto não checa sozinho.

**Tech Stack:** Quarto 1.9.38, Python 3.12, `uv`, Docker + Docker Compose, pytest, GitHub Actions, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-08-15-estrutura-livro-bases5-design.md`

## Global Constraints

- **Livro-texto:** Joel Grus, *Data Science from Scratch*, 2ª ed. (2019). Chave BibTeX: `grus2019`. PDF na raiz do projeto.
- **Escopo:** 17 capítulos — Grus 1, 2, 3, 4 e 8 a 20. Numeração nossa sequencial 1–17.
- **Citação:** o número num callout `de @grus2019` é sempre **do Grus**. **O Grus não numera as seções** — cite capítulo + título da seção: `Esta seção corresponde a *The Model*, do capítulo 12 de @grus2019.` Nunca escreva "seção 12.1".
- **Idioma:** português brasileiro em todo texto, título e nome de arquivo. Código e identificadores em inglês, como no livro.
- **Nunca editar `scratch/`.** Toda adaptação vive no `.qmd`.
- **Nunca reescrever o código do livro com numpy, broadcasting ou `sklearn`.** `Vector = List[float]` é a tese pedagógica.
- **`scikit-learn` só nos callouts de fechamento**, nunca na implementação de uma seção.
- **Teto de versão em toda dependência.** Pacotes `0.x` levam teto no **minor** (`>=0.14,<0.15`), não na major.
- **Caminhos de dados a partir da raiz:** `dados/arquivo.csv`, nunca `../../dados/arquivo.csv`.
- **Semente explícita em todo chunk com RNG.** O Grus usa `random` da stdlib, não `numpy.random`.
- **Porta 4201** no preview (a 4200 é do `bases_3_estatistica`).
- **Imagem GHCR minúscula e literal:** `ghcr.io/bragad/undf-bases5-ciencia-de-dados-202602:latest`.
- **Repositório de referência para copiar infra:** `../bases_3_estatistica/`.

---

## Estrutura de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `.gitignore` | Artefatos de render, venv, lixo do macOS, o PDF do livro |
| `.python-version` | `3.12` |
| `pyproject.toml` | Dependências com teto de versão |
| `uv.lock` | Versões exatas, gerado por `uv lock` |
| `Dockerfile` | Quarto + Python via `uv sync --frozen`, venv em `/opt/venv` |
| `compose.yaml` | Preview local na porta 4201 |
| `Makefile` | `build`, `preview`, `render`, `shell`, `check`, `lock`, `clean`, `teste`, `offline` |
| `_quarto.yml` | Config mestre: 17 capítulos, 105 hrefs, tema, `execute-dir: project` |
| `index.qmd` | Página inicial do livro |
| `references.bib` | `@grus2019` e referências de apoio |
| `styles.css` | `.conceito`, `.exemplo`, dark mode |
| `spoiler.html` | JS do spoiler (ofuscação, nunca gabarito) |
| `scratch/` | Pacote do Grus, vendorizado literalmente, **nunca editado** |
| `im/` | Diretório vazio; existe porque `working_with_data.py:41` grava PNG no import |
| `dados/` | Os seis conjuntos + `README.md` de proveniência |
| `scripts/baixar-dados.py` | Coleta única dos dados externos; não roda no render |
| `scripts/gerar-stubs.py` | Gera os 88 stubs e o bloco `chapters` do `_quarto.yml` |
| `content/capNN/` | Um diretório por capítulo, um `.qmd` por seção |
| `tests/test_estrutura.py` | Invariantes que o Quarto não checa: registro, caminhos, citações |
| `.github/workflows/quarto-render.yml` | CI: build da imagem → render → publish em `gh-pages` |
| `.devcontainer/devcontainer.json` | Codespaces / VS Code Dev Containers |
| `README.md` | Como rodar, estrutura, publicação |

### Mapa completo de capítulos e seções

Esta é a fonte de verdade para `scripts/gerar-stubs.py` e para `_quarto.yml`.

| Nosso | Grus | Diretório | Título |
|---|---|---|---|
| 1 | 1 | `cap01` | Introdução |
| 2 | 2 | `cap02` | Um Curso Rápido de Python |
| 3 | 3 | `cap03` | Visualizando Dados |
| 4 | 4 | `cap04` | Álgebra Linear |
| 5 | 8 | `cap05` | Gradiente Descendente |
| 6 | 9 | `cap06` | Obtendo Dados |
| 7 | 10 | `cap07` | Trabalhando com Dados |
| 8 | 11 | `cap08` | Machine Learning |
| 9 | 12 | `cap09` | k-Vizinhos Mais Próximos |
| 10 | 13 | `cap10` | Naive Bayes |
| 11 | 14 | `cap11` | Regressão Linear Simples |
| 12 | 15 | `cap12` | Regressão Múltipla |
| 13 | 16 | `cap13` | Regressão Logística |
| 14 | 17 | `cap14` | Árvores de Decisão |
| 15 | 18 | `cap15` | Redes Neurais |
| 16 | 19 | `cap16` | Deep Learning |
| 17 | 20 | `cap17` | Clustering |

**Seções** (arquivo → título nosso → título original no Grus, que vai no callout):

**cap01** (Grus 1) — 3 seções
1. `01-a-ascensao-dos-dados` — A Ascensão dos Dados — *The Ascendance of Data*
2. `02-o-que-e-ciencia-de-dados` — O que é Ciência de Dados? — *What Is Data Science?*
3. `03-hipotese-motivadora-datasciencester` — Hipótese Motivadora: DataSciencester — *Motivating Hypothetical: DataSciencester*

**cap02** (Grus 2) — 6 seções agrupadas de 27
1. `01-ambiente-e-sintaxe` — Ambiente e Sintaxe — *The Zen of Python; Getting Python; Virtual Environments; Whitespace Formatting; Modules*
2. `02-funcoes-strings-excecoes` — Funções, Strings e Exceções — *Functions; Strings; Exceptions*
3. `03-estruturas-de-dados` — Estruturas de Dados — *Lists; Tuples; Dictionaries; defaultdict; Counters; Sets*
4. `04-controle-de-fluxo` — Controle de Fluxo — *Control Flow; Truthiness; Sorting; List Comprehensions*
5. `05-testes-classes-e-geradores` — Testes, Classes e Geradores — *Automated Testing and assert; Object-Oriented Programming; Iterables and Generators*
6. `06-ferramentas-e-tipos` — Ferramentas e Anotações de Tipo — *Randomness; Regular Expressions; Functional Programming; zip and Argument Unpacking; args and kwargs; Type Annotations; Welcome to DataSciencester!*

**cap03** (Grus 3) — 4 seções
1. `01-matplotlib` — matplotlib — *matplotlib*
2. `02-graficos-de-barras` — Gráficos de Barras — *Bar Charts*
3. `03-graficos-de-linhas` — Gráficos de Linhas — *Line Charts*
4. `04-graficos-de-dispersao` — Gráficos de Dispersão — *Scatterplots*

**cap04** (Grus 4) — 2 seções
1. `01-vetores` — Vetores — *Vectors*
2. `02-matrizes` — Matrizes — *Matrices*

**cap05** (Grus 8) — 6 seções
1. `01-a-ideia-por-tras-do-gradiente` — A Ideia por Trás do Gradiente Descendente — *The Idea Behind Gradient Descent*
2. `02-estimando-o-gradiente` — Estimando o Gradiente — *Estimating the Gradient*
3. `03-usando-o-gradiente` — Usando o Gradiente — *Using the Gradient*
4. `04-escolhendo-o-tamanho-do-passo` — Escolhendo o Tamanho do Passo — *Choosing the Right Step Size*
5. `05-ajustando-modelos` — Ajustando Modelos com Gradiente Descendente — *Using Gradient Descent to Fit Models*
6. `06-minibatch-e-estocastico` — Minibatch e Gradiente Estocástico — *Minibatch and Stochastic Gradient Descent*

**cap06** (Grus 9) — 5 seções
1. `01-stdin-e-stdout` — stdin e stdout — *stdin and stdout*
2. `02-lendo-arquivos` — Lendo Arquivos — *Reading Files*
3. `03-raspando-a-web` — Raspando a Web — *Scraping the Web*
4. `04-usando-apis` — Usando APIs — *Using APIs*
5. `05-exemplo-apis-do-twitter` — Exemplo: As APIs do Twitter — *Example: Using the Twitter APIs*

**cap07** (Grus 10) — 8 seções
1. `01-explorando-seus-dados` — Explorando Seus Dados — *Exploring Your Data*
2. `02-namedtuples` — Usando NamedTuples — *Using NamedTuples*
3. `03-dataclasses` — Dataclasses — *Dataclasses*
4. `04-limpeza-e-transformacao` — Limpeza e Transformação — *Cleaning and Munging*
5. `05-manipulando-dados` — Manipulando Dados — *Manipulating Data*
6. `06-reescalonamento` — Reescalonamento — *Rescaling*
7. `07-um-parenteses-tqdm` — Um Parêntese: tqdm — *An Aside: tqdm*
8. `08-reducao-de-dimensionalidade` — Redução de Dimensionalidade — *Dimensionality Reduction*

**cap08** (Grus 11) — 6 seções
1. `01-modelagem` — Modelagem — *Modeling*
2. `02-o-que-e-machine-learning` — O que é Machine Learning? — *What Is Machine Learning?*
3. `03-overfitting-e-underfitting` — Overfitting e Underfitting — *Overfitting and Underfitting*
4. `04-correcao` — Correção — *Correctness*
5. `05-vies-e-variancia` — O Compromisso Viés-Variância — *The Bias-Variance Tradeoff*
6. `06-extracao-e-selecao-de-atributos` — Extração e Seleção de Atributos — *Feature Extraction and Selection*

**cap09** (Grus 12) — 3 seções — **escrito por inteiro na Tarefa 7**
1. `01-o-modelo` — O Modelo — *The Model*
2. `02-exemplo-o-dataset-iris` — Exemplo: O Dataset Iris — *Example: The Iris Dataset*
3. `03-a-maldicao-da-dimensionalidade` — A Maldição da Dimensionalidade — *The Curse of Dimensionality*

**cap10** (Grus 13) — 5 seções
1. `01-um-filtro-de-spam-bem-burro` — Um Filtro de Spam Bem Burro — *A Really Dumb Spam Filter*
2. `02-um-filtro-mais-sofisticado` — Um Filtro de Spam Mais Sofisticado — *A More Sophisticated Spam Filter*
3. `03-implementacao` — Implementação — *Implementation*
4. `04-testando-o-modelo` — Testando o Modelo — *Testing Our Model*
5. `05-usando-o-modelo` — Usando o Modelo — *Using Our Model*

**cap11** (Grus 14) — 3 seções
1. `01-o-modelo` — O Modelo — *The Model*
2. `02-usando-gradiente-descendente` — Usando Gradiente Descendente — *Using Gradient Descent*
3. `03-maxima-verossimilhanca` — Estimação por Máxima Verossimilhança — *Maximum Likelihood Estimation*

**cap12** (Grus 15) — 8 seções
1. `01-o-modelo` — O Modelo — *The Model*
2. `02-hipoteses-do-minimos-quadrados` — Outras Hipóteses do Modelo de Mínimos Quadrados — *Further Assumptions of the Least Squares Model*
3. `03-ajustando-o-modelo` — Ajustando o Modelo — *Fitting the Model*
4. `04-interpretando-o-modelo` — Interpretando o Modelo — *Interpreting the Model*
5. `05-qualidade-do-ajuste` — Qualidade do Ajuste — *Goodness of Fit*
6. `06-digressao-o-bootstrap` — Digressão: O Bootstrap — *Digression: The Bootstrap*
7. `07-erros-padrao-dos-coeficientes` — Erros Padrão dos Coeficientes — *Standard Errors of Regression Coefficients*
8. `08-regularizacao` — Regularização — *Regularization*

**cap13** (Grus 16) — 5 seções
1. `01-o-problema` — O Problema — *The Problem*
2. `02-a-funcao-logistica` — A Função Logística — *The Logistic Function*
3. `03-aplicando-o-modelo` — Aplicando o Modelo — *Applying the Model*
4. `04-qualidade-do-ajuste` — Qualidade do Ajuste — *Goodness of Fit*
5. `05-maquinas-de-vetores-de-suporte` — Máquinas de Vetores de Suporte — *Support Vector Machines*

**cap14** (Grus 17) — 6 seções
1. `01-o-que-e-uma-arvore-de-decisao` — O que é uma Árvore de Decisão? — *What Is a Decision Tree?*
2. `02-entropia` — Entropia — *Entropy*
3. `03-a-entropia-de-uma-particao` — A Entropia de uma Partição — *The Entropy of a Partition*
4. `04-criando-uma-arvore` — Criando uma Árvore de Decisão — *Creating a Decision Tree*
5. `05-juntando-tudo` — Juntando Tudo — *Putting It All Together*
6. `06-florestas-aleatorias` — Florestas Aleatórias — *Random Forests*

**cap15** (Grus 18) — 4 seções
1. `01-perceptrons` — Perceptrons — *Perceptrons*
2. `02-redes-feed-forward` — Redes Neurais Feed-Forward — *Feed-Forward Neural Networks*
3. `03-retropropagacao` — Retropropagação — *Backpropagation*
4. `04-exemplo-fizz-buzz` — Exemplo: Fizz Buzz — *Example: Fizz Buzz*

**cap16** (Grus 19) — 8 seções agrupadas de 12
1. `01-o-tensor` — O Tensor — *The Tensor*
2. `02-a-abstracao-de-camada` — A Abstração de Camada — *The Layer Abstraction*
3. `03-a-camada-linear` — A Camada Linear — *The Linear Layer*
4. `04-redes-como-sequencia-de-camadas` — Redes como Sequência de Camadas — *Neural Networks as a Sequence of Layers*
5. `05-perda-e-otimizacao` — Perda e Otimização — *Loss and Optimization; Example: XOR Revisited*
6. `06-outras-funcoes-de-ativacao` — Outras Funções de Ativação — *Other Activation Functions; Example: FizzBuzz Revisited*
7. `07-softmax-e-dropout` — Softmax, Entropia Cruzada e Dropout — *Softmaxes and Cross-Entropy; Dropout*
8. `08-exemplo-mnist` — Exemplo: MNIST — *Example: MNIST; Saving and Loading Models*

**cap17** (Grus 20) — 6 seções
1. `01-a-ideia` — A Ideia — *The Idea*
2. `02-o-modelo` — O Modelo — *The Model*
3. `03-exemplo-encontros` — Exemplo: Encontros — *Example: Meetups*
4. `04-escolhendo-k` — Escolhendo k — *Choosing k*
5. `05-exemplo-clustering-de-cores` — Exemplo: Clustering de Cores — *Example: Clustering Colors*
6. `06-clustering-hierarquico` — Clustering Hierárquico Bottom-Up — *Bottom-Up Hierarchical Clustering*

**Total: 88 seções + 17 `index.qmd` = 105 `.qmd`.**

---

## Task 1: Ambiente containerizado

**Files:**
- Create: `.gitignore`, `.python-version`, `pyproject.toml`, `Dockerfile`, `compose.yaml`, `Makefile`
- Generated: `uv.lock`
- Reference: `../bases_3_estatistica/{Dockerfile,compose.yaml,Makefile,.gitignore}`

**Interfaces:**
- Consumes: nada (primeira tarefa)
- Produces: imagem `bases5-ciencia-de-dados:local`; alvos `make build|preview|render|shell|check|lock|clean|teste|offline`; venv em `/opt/venv`; serviço compose chamado `livro` montando o projeto em `/livro`

- [ ] **Step 1: Criar `.python-version` e `.gitignore`**

`.python-version`:
```
3.12
```

`.gitignore`:
```gitignore
# Quarto
/.quarto/
/_book/
/_freeze/

# Lixo que um render abortado deixa dentro de content/. O Quarto cria estes
# arquivos durante o render e os apaga no fim; se ele aborta (o bind mount do
# Docker no macOS às vezes falha com "Directory not empty"), eles ficam — e
# travam o render seguinte. O `make clean` os remove.
content/**/*.html
content/**/*_files/

# O PDF do livro-texto. 10 MB de material da O'Reilly num repositório que
# vira site público — fica fora do controle de versão de propósito.
*.pdf

# Python
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ipynb_checkpoints/
**/*.quarto_ipynb

# Ambiente
.env

# macOS
.DS_Store

# Editores
.vscode/

# Claude Code — preferências locais da máquina
.claude/settings.local.json
```

- [ ] **Step 2: Criar `pyproject.toml`**

```toml
[project]
name = "bases5-ciencia-de-dados"
version = "0.1.0"
description = "Livro Quarto — Bases 5: Ciência de Dados (UnDF)"
requires-python = ">=3.12"
# Limites de versão: o uv.lock trava as versões exatas, mas um `make lock`
# futuro resolveria livremente e poderia puxar uma versão incompatível. No
# livro irmão (bases_3_estatistica) isso não é teórico: o pandas 3 mudou o
# dtype padrão de texto e quebrou dois exemplos SEM levantar exceção — apenas
# devolvendo a resposta errada.
#
# Pacotes 0.x levam limite no MINOR, não na major: em SemVer pré-1.0 é o minor
# que carrega mudança incompatível, então "<1" não protegeria nada.
#
# numpy NÃO está listado de propósito. Ele vem como dependência transitiva do
# matplotlib e do scikit-learn, mas não é ferramenta desta disciplina: o livro
# implementa Vector = List[float] em Python puro, e essa ausência é o sinal.
dependencies = [
    "jupyter>=1,<2",              # Quarto executa chunks Python via jupyter
    "matplotlib>=3,<4",           # cap. 3 e os gráficos do livro
    "tqdm>=4,<5",                 # caps. 7, 12, 17
    "requests>=2,<3",             # cap. 6
    "beautifulsoup4>=4,<5",       # cap. 6
    "html5lib>=1,<2",             # cap. 6
    "python-dateutil>=2,<3",      # cap. 7
    "pillow>=11,<12",             # cap. 17
    "scikit-learn>=1,<2",         # NOSSO, não do livro — callouts de caixa-preta
    "pytest>=8,<9",               # suíte de invariantes estruturais
]

[tool.uv]
package = false
```

- [ ] **Step 3: Gerar o lock**

Run: `uv lock`
Expected: cria `uv.lock` sem erro de resolução.

- [ ] **Step 4: Criar o `Dockerfile`**

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ARG QUARTO_VERSION=1.9.38
ARG TARGETARCH

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=pt_BR.UTF-8 \
    LC_ALL=pt_BR.UTF-8 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    QUARTO_PYTHON=/opt/venv/bin/python \
    MPLBACKEND=Agg

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl git locales \
    && sed -i '/^# *pt_BR.UTF-8/s/^# *//' /etc/locale.gen \
    && locale-gen \
    && curl -fsSL -o /tmp/quarto.deb \
        "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${TARGETARCH}.deb" \
    && apt-get install -y --no-install-recommends /tmp/quarto.deb \
    && rm -f /tmp/quarto.deb \
    && rm -rf /var/lib/apt/lists/*

# Um shell de login recarrega /etc/profile, que reescreve o PATH e descarta o
# ENV PATH acima — deixando `python` apontar para o interpretador do sistema em
# vez do venv. Isto garante o venv também em `bash -l` e `docker exec -it`.
RUN echo 'export PATH="/opt/venv/bin:$PATH"' > /etc/profile.d/venv.sh

WORKDIR /livro

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-cache

EXPOSE 4201

CMD ["quarto", "preview", "--host", "0.0.0.0", "--port", "4201", "--no-browser"]
```

- [ ] **Step 5: Criar o `compose.yaml`**

```yaml
services:
  livro:
    build:
      context: .
    image: bases5-ciencia-de-dados:local
    user: "${UID:-1000}:${GID:-1000}"
    environment:
      - HOME=/tmp
    ports:
      - "4201:4201"
    volumes:
      - .:/livro
```

- [ ] **Step 6: Criar o `Makefile`**

```makefile
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
	$(COMPOSE) run --rm --no-deps --network none livro quarto render

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
```

- [ ] **Step 7: Construir a imagem e verificar**

Run: `make build && make check`
Expected: build sem erro; `quarto check` reporta Quarto 1.9.38 e Python em `/opt/venv/bin/python`.

- [ ] **Step 8: Verificar que o venv sobrevive a um shell de login**

Run: `docker compose run --rm --no-deps livro bash -lc 'which python && python -V'`
Expected: `/opt/venv/bin/python` e `Python 3.12.x`. Se sair `/usr/bin/python`, o `/etc/profile.d/venv.sh` não foi criado.

- [ ] **Step 9: Commit**

```bash
git add .gitignore .python-version pyproject.toml uv.lock Dockerfile compose.yaml Makefile
git commit -m "feat: ambiente containerizado com Quarto 1.9.38 e Python 3.12"
```

---

## Task 2: Esqueleto Quarto mínimo que renderiza

**Files:**
- Create: `_quarto.yml`, `index.qmd`, `references.bib`, `styles.css`, `spoiler.html`, `images/logo-undf.png`
- Reference: `../bases_3_estatistica/{_quarto.yml,styles.css,spoiler.html,images/logo-undf.png}`

**Interfaces:**
- Consumes: imagem Docker da Tarefa 1
- Produces: `_book/index.html` renderizável; chave BibTeX `grus2019`; classes CSS `.conceito` e `.exemplo`; `execute-dir: project` (todo chunk roda a partir da raiz)

- [ ] **Step 1: Copiar os assets visuais do livro irmão**

```bash
mkdir -p images
cp ../bases_3_estatistica/styles.css .
cp ../bases_3_estatistica/spoiler.html .
cp ../bases_3_estatistica/images/logo-undf.png images/
```

- [ ] **Step 2: Criar `references.bib`**

```bibtex
@book{grus2019,
  author    = {Grus, Joel},
  title     = {Data Science from Scratch: First Principles with Python},
  edition   = {2nd},
  publisher = {O'Reilly Media},
  year      = {2019},
  isbn      = {978-1-492-04113-9}
}

@book{bruce2020,
  author    = {Bruce, Peter and Bruce, Andrew and Gedeck, Peter},
  title     = {Practical Statistics for Data Scientists},
  edition   = {2nd},
  publisher = {O'Reilly Media},
  year      = {2020},
  isbn      = {978-1-492-07294-2}
}

@book{geron2022,
  author    = {G{\'e}ron, Aur{\'e}lien},
  title     = {Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow},
  edition   = {3rd},
  publisher = {O'Reilly Media},
  year      = {2022},
  isbn      = {978-1-098-12597-4}
}

@book{james2021,
  author    = {James, Gareth and Witten, Daniela and Hastie, Trevor and Tibshirani, Robert},
  title     = {An Introduction to Statistical Learning},
  edition   = {2nd},
  publisher = {Springer},
  year      = {2021},
  isbn      = {978-1-0716-1417-4}
}

@book{hastie2009,
  author    = {Hastie, Trevor and Tibshirani, Robert and Friedman, Jerome},
  title     = {The Elements of Statistical Learning},
  edition   = {2nd},
  publisher = {Springer},
  year      = {2009},
  isbn      = {978-0-387-84857-0}
}
```

- [ ] **Step 3: Criar `_quarto.yml` com um único capítulo provisório**

O bloco `chapters` completo entra na Tarefa 6, gerado por script. Aqui só o mínimo que renderiza:

```yaml
project:
  type: book
  output-dir: _book
  execute-dir: project

execute:
  freeze: auto

jupyter: python3

lang: pt

book:
  title: "Bases 5"
  subtitle: "Ciência de Dados"
  site-url: "https://BragaD.github.io/UnDF-Bases5-CienciaDeDados-202602"
  repo-url: "https://github.com/BragaD/UnDF-Bases5-CienciaDeDados-202602"
  repo-actions: [issue]
  navbar:
    logo: images/logo-undf.png
    logo-alt: "Logo UnDF"
    title: "Bases 5 — Ciência de Dados"
  date: today
  date-format: "DD/MM/YYYY"
  chapters:
    - text: "Início"
      href: index.qmd
  page-navigation: true
  page-footer:
    border: true
    left: "UnDF — Ciência da Computação — Ciência de Dados — 2026.2"
    right:
      - icon: github
        href: "https://github.com/BragaD/UnDF-Bases5-CienciaDeDados-202602"

format:
  html:
    theme:
      light: cosmo
      dark: darkly
    css: styles.css
    number-sections: false
    include-after-body: spoiler.html
    toc: true
    toc-depth: 4
    toc-title: "Nesta página"
    link-external-icon: true
    link-external-newwindow: true
    code-copy: true
    code-overflow: wrap

bibliography: references.bib

editor: source
code-annotations: hover

author:
  - name: "Douglas Braga"
    email: "douglas.braga@undf.edu.br"
```

- [ ] **Step 4: Criar `index.qmd`**

```markdown
# Bem-vindo {.unnumbered}

Este é o material de apoio da disciplina **Bases 5 — Ciência de Dados**, do curso de **Ciência da Computação** da UnDF.

## Sobre a Disciplina

Você provavelmente já treinou um modelo chamando uma função pronta: um `.fit()`, um `.predict()`, e uma resposta que apareceu sem explicação. Esta disciplina abre essas caixas-pretas.

Todo algoritmo aqui é construído do zero, em Python puro — sem `numpy`, sem `scikit-learn`, sem nada que esconda a mecânica. O código é mais lento e mais verboso do que o de produção, e isso é proposital: o que se ganha é enxergar o que acontece por dentro. No fim de cada seção, depois de você ter construído a coisa, mostramos a chamada de biblioteca equivalente — que a partir dali deixa de ser mágica.

Os temas são:

- Fundamentos: Python para dados, visualização, álgebra linear e gradiente descendente
- Obtenção e preparação de dados
- Aprendizado supervisionado: k-vizinhos, Naive Bayes, regressão linear, logística e árvores de decisão
- Redes neurais e deep learning, construídos camada por camada
- Aprendizado não-supervisionado: clustering

## Material Bibliográfico

O livro-texto da disciplina é:

> @grus2019

O código e os exemplos originais estão em [github.com/joelgrus/data-science-from-scratch](https://github.com/joelgrus/data-science-from-scratch), sob licença MIT, e vêm reproduzidos neste repositório no diretório `scratch/`.

Esta disciplina cobre os **capítulos 1 a 4 e 8 a 20 de @grus2019**, aqui reorganizados em 17 capítulos sequenciais. Os capítulos 5 a 7 do Grus (Estatística, Probabilidade, Hipótese e Inferência) pertencem à disciplina de Estatística; os capítulos 21 a 27 ficam fora do escopo deste semestre.

## Como Usar Este Material

Cada capítulo traz:

- Conceitos com implementações executáveis em Python puro
- O código do livro-texto, rodando sobre os conjuntos de dados originais
- Um fechamento mostrando a ferramenta de produção equivalente

O ambiente completo (Python, bibliotecas e Quarto) está empacotado em um container Docker — veja o `README.md` para rodar o livro na sua máquina.

## Licença {.unnumbered}

Material disponibilizado para fins educacionais. O código e os exemplos originais são de autoria de Joel Grus [@grus2019], sob licença MIT.
```

- [ ] **Step 5: Renderizar e verificar**

Run: `make render`
Expected: `_book/index.html` existe e contém "Bases 5".

Run: `test -f _book/index.html && grep -q "Ciência de Dados" _book/index.html && echo OK`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add _quarto.yml index.qmd references.bib styles.css spoiler.html images/
git commit -m "feat: esqueleto Quarto renderizável com tema e bibliografia"
```

---

## Task 3: Vendorizar o pacote `scratch/`

**Files:**
- Create: `scratch/` (cópia do upstream), `LICENSE-scratch`, `im/.gitkeep`
- Create: `tests/test_scratch.py`

**Interfaces:**
- Consumes: ambiente da Tarefa 1
- Produces: `scratch.linear_algebra.{Vector,dot,distance,add,scalar_multiply,vector_mean,squared_distance,Matrix,make_matrix,shape,magnitude,subtract,sum_of_squares}`, `scratch.machine_learning.{split_data,train_test_split,accuracy,precision,recall,f1_score}`, `scratch.statistics.{mean,median,standard_deviation,correlation,de_mean,num_friends_good,daily_minutes_good}`, `scratch.probability.{normal_cdf,inverse_normal_cdf}` — todos importáveis a partir da raiz do projeto

- [ ] **Step 1: Escrever o teste que falha**

`tests/test_scratch.py`:
```python
"""O pacote scratch/ é vendorizado literalmente do repositório do Grus.

Estes testes travam duas coisas que já quebraram na análise do código:
importar working_with_data grava um PNG em im/, e importar getting_data
dispara uma requisição HTTP.
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

MODULOS_EM_ESCOPO = [
    "linear_algebra",
    "statistics",
    "probability",
    "gradient_descent",
    "getting_data",
    "working_with_data",
    "machine_learning",
    "k_nearest_neighbors",
    "naive_bayes",
    "simple_linear_regression",
    "multiple_regression",
    "logistic_regression",
    "decision_trees",
    "neural_networks",
    "deep_learning",
    "clustering",
]


def test_todos_os_modulos_em_escopo_existem():
    for nome in MODULOS_EM_ESCOPO:
        assert (RAIZ / "scratch" / f"{nome}.py").is_file(), f"falta scratch/{nome}.py"


def test_diretorio_im_existe():
    """working_with_data.py:41 faz plt.savefig('im/...') no nível do módulo.

    Sem im/, qualquer `from scratch.working_with_data import rescale`
    estoura com FileNotFoundError — e isso atinge os capítulos 7 e 13.
    """
    assert (RAIZ / "im").is_dir()


def test_vector_e_lista_de_float_nao_numpy():
    """A tese pedagógica do livro. Se alguém 'otimizar' isto, o teste cai."""
    fonte = (RAIZ / "scratch" / "linear_algebra.py").read_text()
    assert "Vector = List[float]" in fonte
    assert "import numpy" not in fonte


def test_scratch_nao_importa_numpy_em_lugar_nenhum():
    for py in (RAIZ / "scratch").glob("*.py"):
        assert "import numpy" not in py.read_text(), f"{py.name} importa numpy"


def test_modulos_importaveis_sem_rede():
    """Importa cada módulo em escopo, menos getting_data.

    getting_data.py:90 tem um requests.get no corpo do módulo — importá-lo
    dispara rede. Por isso o capítulo 6 nunca o importa, e este teste
    documenta a exclusão em vez de escondê-la.
    """
    alvos = [m for m in MODULOS_EM_ESCOPO if m != "getting_data"]
    codigo = "\n".join(f"import scratch.{m}" for m in alvos)
    r = subprocess.run(
        [sys.executable, "-c", codigo],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        env={"MPLBACKEND": "Agg", "PATH": "/opt/venv/bin:/usr/bin:/bin", "HOME": "/tmp"},
    )
    assert r.returncode == 0, r.stderr
```

- [ ] **Step 2: Rodar o teste para confirmar que falha**

Run: `make teste`
Expected: FAIL — `falta scratch/linear_algebra.py` (o diretório ainda não existe).

- [ ] **Step 3: Vendorizar o pacote**

```bash
git clone --depth 1 https://github.com/joelgrus/data-science-from-scratch.git /tmp/dsfs
cp -r /tmp/dsfs/scratch .
cp /tmp/dsfs/LICENSE LICENSE-scratch
mkdir -p im && touch im/.gitkeep
rm -rf /tmp/dsfs
```

- [ ] **Step 4: Rodar o teste para confirmar que passa**

Run: `make teste`
Expected: PASS, 5 testes.

Se `test_modulos_importaveis_sem_rede` falhar com `FileNotFoundError: im/working_scatter.png`, o `im/` não foi criado — volte ao Step 3.

- [ ] **Step 5: Confirmar que `scratch/` está intocado**

Run: `git diff --no-index --stat /tmp/dsfs-check/scratch scratch 2>/dev/null || echo "sem baseline, ok"`

Verificação manual: nenhum arquivo em `scratch/` deve ter sido editado. Toda adaptação vive no `.qmd`.

- [ ] **Step 6: Commit**

```bash
git add scratch/ LICENSE-scratch im/.gitkeep tests/test_scratch.py
git commit -m "feat: vendoriza o pacote scratch/ do Grus (MIT) com im/ e testes de invariante"
```

---

## Task 4: Conjuntos de dados

**Files:**
- Create: `scripts/baixar-dados.py`, `dados/README.md`
- Generated (commitados): `dados/stocks.csv`, `dados/comma_delimited_stock_prices.csv`, `dados/getting-data.html`, `dados/iris.data`, `dados/spam-assuntos.csv`, `dados/mnist/*.idx*-ubyte.gz`, `dados/imagem-cores.jpg`
- Create: `tests/test_dados.py`

**Interfaces:**
- Consumes: ambiente da Tarefa 1
- Produces: os seis conjuntos em `dados/`, lidos pelos capítulos 6, 7, 9, 10, 16 e 17 com caminho relativo à raiz

- [ ] **Step 1: Escrever o teste que falha**

`tests/test_dados.py`:
```python
"""Nenhum byte vem da rede em tempo de render — os dados são commitados."""
import csv
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"

ESPERADOS = [
    "stocks.csv",
    "comma_delimited_stock_prices.csv",
    "getting-data.html",
    "iris.data",
    "spam-assuntos.csv",
    "imagem-cores.jpg",
]


def test_conjuntos_presentes():
    for nome in ESPERADOS:
        assert (DADOS / nome).is_file(), f"falta dados/{nome}"


def test_mnist_presente():
    arquivos = list((DADOS / "mnist").glob("*.gz"))
    assert len(arquivos) == 4, f"esperava 4 arquivos MNIST, achei {len(arquivos)}"


def test_iris_tem_150_linhas_e_4_medidas():
    linhas = [l for l in (DADOS / "iris.data").read_text().splitlines() if l.strip()]
    assert len(linhas) == 150
    primeira = linhas[0].split(",")
    assert len(primeira) == 5           # 4 medidas + a classe
    assert primeira[-1].startswith("Iris-")


def test_spam_tem_assunto_e_rotulo():
    with (DADOS / "spam-assuntos.csv").open(encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        assert leitor.fieldnames == ["assunto", "is_spam"]
        linhas = list(leitor)
    assert len(linhas) > 1000
    assert {l["is_spam"] for l in linhas} == {"True", "False"}


def test_dados_README_documenta_cada_conjunto():
    texto = (DADOS / "README.md").read_text()
    for nome in ESPERADOS + ["mnist"]:
        assert nome in texto, f"dados/README.md não menciona {nome}"
```

- [ ] **Step 2: Rodar o teste para confirmar que falha**

Run: `make teste`
Expected: FAIL — `falta dados/stocks.csv`.

- [ ] **Step 3: Escrever `scripts/baixar-dados.py`**

Este script roda **uma única vez**; os arquivos que ele produz são commitados. Ele não é um chunk do livro.

```python
#!/usr/bin/env python3
"""Coleta única dos dados externos do livro. Os resultados são COMMITADOS.

Rodar com:
    docker compose run --rm --no-deps livro python scripts/baixar-dados.py

Isto não é um chunk do livro. Um livro que faz chamadas de rede a cada render
é frágil: a página raspada muda de layout, a API sai do ar, e o material
quebra sem ninguém ter tocado no repositório.
"""
import csv
import gzip
import io
import shutil
import tarfile
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"
DADOS.mkdir(exist_ok=True)


def baixar(url: str, destino: Path) -> None:
    if destino.exists():
        print(f"skip  {destino.relative_to(RAIZ)} (já existe)")
        return
    destino.parent.mkdir(parents=True, exist_ok=True)
    print(f"baixa {destino.relative_to(RAIZ)} <- {url}")
    with urllib.request.urlopen(url) as r, destino.open("wb") as f:
        shutil.copyfileobj(r, f)


# 1-2. CSVs de ações, do próprio repositório do Grus
BASE_GRUS = "https://raw.githubusercontent.com/joelgrus/data-science-from-scratch/master/"
baixar(BASE_GRUS + "stocks.csv", DADOS / "stocks.csv")
baixar(BASE_GRUS + "comma_delimited_stock_prices.csv",
       DADOS / "comma_delimited_stock_prices.csv")

# 3. HTML de exemplo do capítulo 6 (Grus 9)
baixar("https://raw.githubusercontent.com/joelgrus/data/master/getting-data.html",
       DADOS / "getting-data.html")

# 4. Iris, do capítulo 9 (Grus 12)
baixar("https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data",
       DADOS / "iris.data")

# 5. MNIST, do capítulo 16 (Grus 19)
MNIST = "https://ossci-datasets.s3.amazonaws.com/mnist/"
for nome in ["train-images-idx3-ubyte.gz", "train-labels-idx1-ubyte.gz",
             "t10k-images-idx3-ubyte.gz", "t10k-labels-idx1-ubyte.gz"]:
    baixar(MNIST + nome, DADOS / "mnist" / nome)

# 6. SpamAssassin — extraímos SÓ os assuntos.
#
# O naive_bayes.py do Grus lê cada arquivo de e-mail e descarta tudo menos a
# linha "Subject:". Baixar centenas de MB de corpus para usar uma linha por
# arquivo não se justifica num repositório de livro. O código de varredura dos
# diretórios continua no capítulo 10, com eval: false — ele É parte da lição,
# só não precisa rodar a cada render.
SPAM_BASE = "https://spamassassin.apache.org/old/publiccorpus/"
TARBALLS = [
    ("20021010_easy_ham.tar.bz2", False),
    ("20021010_hard_ham.tar.bz2", False),
    ("20021010_spam.tar.bz2", True),
]

saida = DADOS / "spam-assuntos.csv"
if saida.exists():
    print(f"skip  {saida.relative_to(RAIZ)} (já existe)")
else:
    linhas = []
    for nome, is_spam in TARBALLS:
        print(f"lê    {nome}")
        with urllib.request.urlopen(SPAM_BASE + nome) as r:
            bruto = io.BytesIO(r.read())
        with tarfile.open(fileobj=bruto, mode="r:bz2") as tar:
            for membro in tar.getmembers():
                if not membro.isfile():
                    continue
                f = tar.extractfile(membro)
                if f is None:
                    continue
                for linha in io.TextIOWrapper(f, errors="ignore"):
                    if linha.startswith("Subject:"):
                        linhas.append({
                            "assunto": linha[len("Subject:"):].strip(),
                            "is_spam": is_spam,
                        })
                        break
    with saida.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["assunto", "is_spam"])
        escritor.writeheader()
        escritor.writerows(linhas)
    print(f"ok    {saida.relative_to(RAIZ)} ({len(linhas)} assuntos)")

print("---")
print("Revise os arquivos e commite-os. Este script não roda no render.")
```

- [ ] **Step 4: Rodar a coleta**

Run: `docker compose run --rm --no-deps livro python scripts/baixar-dados.py`
Expected: todos os arquivos criados; a linha final do SpamAssassin reporta alguns milhares de assuntos.

- [ ] **Step 5: Escolher e adicionar a imagem do capítulo 17**

O Grus usa `girl_with_book.jpg` e **não a distribui** — o texto manda o leitor apontar para uma imagem qualquer. Critérios: licença que permita redistribuição (CC0 ou equivalente) e poucas regiões de cor bem definidas, para o k-means dar resultado legível com k pequeno.

Baixe uma imagem CC0 (por exemplo de <https://www.pexels.com> ou <https://commons.wikimedia.org>, filtrando por domínio público), redimensione para no máximo 600 px no lado maior, e salve em `dados/imagem-cores.jpg`. Registre a URL de origem e a licença no `dados/README.md` do próximo passo.

Run: `python3 -c "from PIL import Image; im = Image.open('dados/imagem-cores.jpg'); print(im.size)"`
Expected: nenhuma dimensão maior que 600.

- [ ] **Step 6: Escrever `dados/README.md`**

```markdown
# Conjuntos de Dados

Todos os arquivos deste diretório são **commitados**. Nenhum é baixado em tempo
de render: um livro que faz chamadas de rede a cada render é frágil — a página
raspada muda de layout, a API sai do ar, e o material quebra sem ninguém ter
tocado no repositório.

A coleta é feita uma única vez por `scripts/baixar-dados.py`:

```bash
docker compose run --rm --no-deps livro python scripts/baixar-dados.py
```

| Arquivo | Capítulo | Origem |
|---|---|---|
| `stocks.csv` | 7 | [repo do Grus](https://github.com/joelgrus/data-science-from-scratch) |
| `comma_delimited_stock_prices.csv` | 7 | repo do Grus |
| `getting-data.html` | 6 | [joelgrus/data](https://github.com/joelgrus/data) |
| `iris.data` | 9 | [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/iris) |
| `spam-assuntos.csv` | 10 | [SpamAssassin public corpus](https://spamassassin.apache.org/old/publiccorpus/) — **só os assuntos**, ver abaixo |
| `mnist/` | 16 | [MNIST](https://ossci-datasets.s3.amazonaws.com/mnist/) |
| `imagem-cores.jpg` | 17 | *(preencher com a URL de origem e a licença)* |

## `spam-assuntos.csv` — por que só os assuntos

O `scratch/naive_bayes.py` lê cada arquivo de e-mail do corpus e **descarta tudo
menos a linha `Subject:`**. Baixar centenas de MB para usar uma linha por arquivo
não se justifica num repositório de livro.

O CSV tem duas colunas, `assunto` e `is_spam`. O código de varredura dos
diretórios continua aparecendo no capítulo 10 com `eval: false` — ele *é* parte
da lição, só não precisa rodar a cada render.

## `imagem-cores.jpg` — por que não é a do livro

O Grus usa `girl_with_book.jpg` e não a distribui; o texto manda o leitor apontar
para uma imagem qualquer. A nossa precisa de licença que permita redistribuição e
de poucas regiões de cor bem definidas, para o k-means produzir um resultado
legível com k pequeno.
```

- [ ] **Step 7: Rodar o teste para confirmar que passa**

Run: `make teste`
Expected: PASS — os testes de `test_scratch.py` e `test_dados.py`.

- [ ] **Step 8: Commit**

```bash
git add scripts/baixar-dados.py dados/ tests/test_dados.py
git commit -m "feat: vendoriza os seis conjuntos de dados; nada vem da rede no render"
```

---

## Task 5: Suíte de invariantes estruturais

**Files:**
- Create: `tests/test_estrutura.py`

**Interfaces:**
- Consumes: `_quarto.yml` da Tarefa 2
- Produces: `make teste` guardando três invariantes: todo `.qmd` registrado, nenhum caminho relativo de dados, todo stub citando o Grus

- [ ] **Step 1: Escrever os testes**

Esta tarefa vem **antes** da geração dos stubs de propósito: os testes definem o contrato que o gerador precisa cumprir.

`tests/test_estrutura.py`:
```python
"""Invariantes que o Quarto não checa sozinho.

A pior falha deste tipo de projeto é silenciosa: um .qmd que existe no disco,
não está no _quarto.yml, e simplesmente não aparece no livro. Ninguém percebe
até alguém procurar a seção.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
QUARTO_YML = RAIZ / "_quarto.yml"
CONTENT = RAIZ / "content"


def hrefs_registrados() -> set[str]:
    """Extrai os href: do _quarto.yml sem depender de um parser YAML."""
    texto = QUARTO_YML.read_text(encoding="utf-8")
    return set(re.findall(r"href:\s*(\S+\.qmd)", texto))


def qmds_no_disco() -> set[str]:
    return {
        str(p.relative_to(RAIZ))
        for p in CONTENT.rglob("*.qmd")
        if not p.name.startswith("_")
    }


def test_todo_qmd_esta_registrado_no_quarto_yml():
    faltando = qmds_no_disco() - hrefs_registrados()
    assert not faltando, (
        "arquivos no disco que não aparecem no livro: " + ", ".join(sorted(faltando))
    )


def test_todo_href_do_quarto_yml_existe_no_disco():
    quebrados = {h for h in hrefs_registrados() if not (RAIZ / h).is_file()}
    assert not quebrados, "hrefs apontando para nada: " + ", ".join(sorted(quebrados))


def test_nenhum_qmd_usa_caminho_relativo_de_dados():
    """execute-dir: project => o cwd é a raiz. '../../dados/' nunca resolve."""
    ofensores = [
        str(p.relative_to(RAIZ))
        for p in CONTENT.rglob("*.qmd")
        if "../dados/" in p.read_text(encoding="utf-8")
    ]
    assert not ofensores, "caminho relativo de dados em: " + ", ".join(sorted(ofensores))


def test_toda_secao_cita_o_grus():
    """Todo .qmd de seção traz um callout `de @grus2019`.

    É o que ancora a seção no livro-texto e o que permite conferir o
    conteúdo depois.
    """
    sem_citacao = [
        str(p.relative_to(RAIZ))
        for p in CONTENT.rglob("*.qmd")
        if p.name != "index.qmd" and "@grus2019" not in p.read_text(encoding="utf-8")
    ]
    assert not sem_citacao, "seções sem citação: " + ", ".join(sorted(sem_citacao))


def test_nenhuma_secao_inventa_numero_de_secao_do_grus():
    """O Grus NÃO numera as seções — o sumário só traz títulos.

    Escrever "seção 12.1 de @grus2019" seria inventar uma referência que o
    livro não tem. O callout cita capítulo + título da seção.
    """
    padrao = re.compile(r"se[çc][ãa]o\s+\d+\.\d+\s+de\s+@grus2019", re.IGNORECASE)
    ofensores = [
        str(p.relative_to(RAIZ))
        for p in CONTENT.rglob("*.qmd")
        if padrao.search(p.read_text(encoding="utf-8"))
    ]
    assert not ofensores, "número de seção inventado em: " + ", ".join(sorted(ofensores))


def test_dezessete_capitulos():
    dirs = sorted(d.name for d in CONTENT.iterdir() if d.is_dir())
    assert dirs == [f"cap{n:02d}" for n in range(1, 18)]


def test_cada_capitulo_tem_index():
    for n in range(1, 18):
        assert (CONTENT / f"cap{n:02d}" / "index.qmd").is_file(), f"falta cap{n:02d}/index.qmd"
```

- [ ] **Step 2: Rodar para confirmar que falha**

Run: `make teste`
Expected: FAIL em `test_dezessete_capitulos` — `content/` ainda não existe.

- [ ] **Step 3: Commit dos testes**

```bash
git add tests/test_estrutura.py
git commit -m "test: invariantes estruturais do livro (registro, caminhos, citações)"
```

---

## Task 6: Gerar os 105 `.qmd` e o `_quarto.yml` completo

**Files:**
- Create: `scripts/gerar-stubs.py`
- Generated: `content/cap01/` … `content/cap17/` (105 `.qmd`)
- Modify: `_quarto.yml` (bloco `book.chapters`)

**Interfaces:**
- Consumes: testes da Tarefa 5, `_quarto.yml` da Tarefa 2
- Produces: 105 `.qmd` no disco e registrados; `make teste` verde

- [ ] **Step 1: Escrever `scripts/gerar-stubs.py`**

O mapa completo de capítulos e seções está na seção **Mapa completo** deste plano — copie-o para a constante `LIVRO` abaixo. O script é idempotente: nunca sobrescreve arquivo existente.

```python
#!/usr/bin/env python3
"""Gera os stubs de seção e o bloco `chapters` do _quarto.yml.

Idempotente: nunca sobrescreve um arquivo que já existe. Rodar de novo depois
de escrever um capítulo é seguro.

Uso:
    python3 scripts/gerar-stubs.py            # cria os .qmd faltantes
    python3 scripts/gerar-stubs.py --yaml     # imprime o bloco chapters
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONTENT = RAIZ / "content"

# (nosso_num, grus_num, titulo_capitulo, [(arquivo, titulo_nosso, titulo_grus), ...])
# ATENÇÃO: preencher com o mapa completo da seção "Mapa completo de capítulos e
# seções" do plano. Reproduzido aqui na íntegra — 17 capítulos, 88 seções.
LIVRO = [
    (1, 1, "Introdução", [
        ("01-a-ascensao-dos-dados", "A Ascensão dos Dados", "The Ascendance of Data"),
        ("02-o-que-e-ciencia-de-dados", "O que é Ciência de Dados?", "What Is Data Science?"),
        ("03-hipotese-motivadora-datasciencester", "Hipótese Motivadora: DataSciencester", "Motivating Hypothetical: DataSciencester"),
    ]),
    (2, 2, "Um Curso Rápido de Python", [
        ("01-ambiente-e-sintaxe", "Ambiente e Sintaxe", "The Zen of Python; Getting Python; Virtual Environments; Whitespace Formatting; Modules"),
        ("02-funcoes-strings-excecoes", "Funções, Strings e Exceções", "Functions; Strings; Exceptions"),
        ("03-estruturas-de-dados", "Estruturas de Dados", "Lists; Tuples; Dictionaries; defaultdict; Counters; Sets"),
        ("04-controle-de-fluxo", "Controle de Fluxo", "Control Flow; Truthiness; Sorting; List Comprehensions"),
        ("05-testes-classes-e-geradores", "Testes, Classes e Geradores", "Automated Testing and assert; Object-Oriented Programming; Iterables and Generators"),
        ("06-ferramentas-e-tipos", "Ferramentas e Anotações de Tipo", "Randomness; Regular Expressions; Functional Programming; zip and Argument Unpacking; args and kwargs; Type Annotations; Welcome to DataSciencester!"),
    ]),
    (3, 3, "Visualizando Dados", [
        ("01-matplotlib", "matplotlib", "matplotlib"),
        ("02-graficos-de-barras", "Gráficos de Barras", "Bar Charts"),
        ("03-graficos-de-linhas", "Gráficos de Linhas", "Line Charts"),
        ("04-graficos-de-dispersao", "Gráficos de Dispersão", "Scatterplots"),
    ]),
    (4, 4, "Álgebra Linear", [
        ("01-vetores", "Vetores", "Vectors"),
        ("02-matrizes", "Matrizes", "Matrices"),
    ]),
    (5, 8, "Gradiente Descendente", [
        ("01-a-ideia-por-tras-do-gradiente", "A Ideia por Trás do Gradiente Descendente", "The Idea Behind Gradient Descent"),
        ("02-estimando-o-gradiente", "Estimando o Gradiente", "Estimating the Gradient"),
        ("03-usando-o-gradiente", "Usando o Gradiente", "Using the Gradient"),
        ("04-escolhendo-o-tamanho-do-passo", "Escolhendo o Tamanho do Passo", "Choosing the Right Step Size"),
        ("05-ajustando-modelos", "Ajustando Modelos com Gradiente Descendente", "Using Gradient Descent to Fit Models"),
        ("06-minibatch-e-estocastico", "Minibatch e Gradiente Estocástico", "Minibatch and Stochastic Gradient Descent"),
    ]),
    (6, 9, "Obtendo Dados", [
        ("01-stdin-e-stdout", "stdin e stdout", "stdin and stdout"),
        ("02-lendo-arquivos", "Lendo Arquivos", "Reading Files"),
        ("03-raspando-a-web", "Raspando a Web", "Scraping the Web"),
        ("04-usando-apis", "Usando APIs", "Using APIs"),
        ("05-exemplo-apis-do-twitter", "Exemplo: As APIs do Twitter", "Example: Using the Twitter APIs"),
    ]),
    (7, 10, "Trabalhando com Dados", [
        ("01-explorando-seus-dados", "Explorando Seus Dados", "Exploring Your Data"),
        ("02-namedtuples", "Usando NamedTuples", "Using NamedTuples"),
        ("03-dataclasses", "Dataclasses", "Dataclasses"),
        ("04-limpeza-e-transformacao", "Limpeza e Transformação", "Cleaning and Munging"),
        ("05-manipulando-dados", "Manipulando Dados", "Manipulating Data"),
        ("06-reescalonamento", "Reescalonamento", "Rescaling"),
        ("07-um-parenteses-tqdm", "Um Parêntese: tqdm", "An Aside: tqdm"),
        ("08-reducao-de-dimensionalidade", "Redução de Dimensionalidade", "Dimensionality Reduction"),
    ]),
    (8, 11, "Machine Learning", [
        ("01-modelagem", "Modelagem", "Modeling"),
        ("02-o-que-e-machine-learning", "O que é Machine Learning?", "What Is Machine Learning?"),
        ("03-overfitting-e-underfitting", "Overfitting e Underfitting", "Overfitting and Underfitting"),
        ("04-correcao", "Correção", "Correctness"),
        ("05-vies-e-variancia", "O Compromisso Viés-Variância", "The Bias-Variance Tradeoff"),
        ("06-extracao-e-selecao-de-atributos", "Extração e Seleção de Atributos", "Feature Extraction and Selection"),
    ]),
    (9, 12, "k-Vizinhos Mais Próximos", [
        ("01-o-modelo", "O Modelo", "The Model"),
        ("02-exemplo-o-dataset-iris", "Exemplo: O Dataset Iris", "Example: The Iris Dataset"),
        ("03-a-maldicao-da-dimensionalidade", "A Maldição da Dimensionalidade", "The Curse of Dimensionality"),
    ]),
    (10, 13, "Naive Bayes", [
        ("01-um-filtro-de-spam-bem-burro", "Um Filtro de Spam Bem Burro", "A Really Dumb Spam Filter"),
        ("02-um-filtro-mais-sofisticado", "Um Filtro de Spam Mais Sofisticado", "A More Sophisticated Spam Filter"),
        ("03-implementacao", "Implementação", "Implementation"),
        ("04-testando-o-modelo", "Testando o Modelo", "Testing Our Model"),
        ("05-usando-o-modelo", "Usando o Modelo", "Using Our Model"),
    ]),
    (11, 14, "Regressão Linear Simples", [
        ("01-o-modelo", "O Modelo", "The Model"),
        ("02-usando-gradiente-descendente", "Usando Gradiente Descendente", "Using Gradient Descent"),
        ("03-maxima-verossimilhanca", "Estimação por Máxima Verossimilhança", "Maximum Likelihood Estimation"),
    ]),
    (12, 15, "Regressão Múltipla", [
        ("01-o-modelo", "O Modelo", "The Model"),
        ("02-hipoteses-do-minimos-quadrados", "Outras Hipóteses do Modelo de Mínimos Quadrados", "Further Assumptions of the Least Squares Model"),
        ("03-ajustando-o-modelo", "Ajustando o Modelo", "Fitting the Model"),
        ("04-interpretando-o-modelo", "Interpretando o Modelo", "Interpreting the Model"),
        ("05-qualidade-do-ajuste", "Qualidade do Ajuste", "Goodness of Fit"),
        ("06-digressao-o-bootstrap", "Digressão: O Bootstrap", "Digression: The Bootstrap"),
        ("07-erros-padrao-dos-coeficientes", "Erros Padrão dos Coeficientes", "Standard Errors of Regression Coefficients"),
        ("08-regularizacao", "Regularização", "Regularization"),
    ]),
    (13, 16, "Regressão Logística", [
        ("01-o-problema", "O Problema", "The Problem"),
        ("02-a-funcao-logistica", "A Função Logística", "The Logistic Function"),
        ("03-aplicando-o-modelo", "Aplicando o Modelo", "Applying the Model"),
        ("04-qualidade-do-ajuste", "Qualidade do Ajuste", "Goodness of Fit"),
        ("05-maquinas-de-vetores-de-suporte", "Máquinas de Vetores de Suporte", "Support Vector Machines"),
    ]),
    (14, 17, "Árvores de Decisão", [
        ("01-o-que-e-uma-arvore-de-decisao", "O que é uma Árvore de Decisão?", "What Is a Decision Tree?"),
        ("02-entropia", "Entropia", "Entropy"),
        ("03-a-entropia-de-uma-particao", "A Entropia de uma Partição", "The Entropy of a Partition"),
        ("04-criando-uma-arvore", "Criando uma Árvore de Decisão", "Creating a Decision Tree"),
        ("05-juntando-tudo", "Juntando Tudo", "Putting It All Together"),
        ("06-florestas-aleatorias", "Florestas Aleatórias", "Random Forests"),
    ]),
    (15, 18, "Redes Neurais", [
        ("01-perceptrons", "Perceptrons", "Perceptrons"),
        ("02-redes-feed-forward", "Redes Neurais Feed-Forward", "Feed-Forward Neural Networks"),
        ("03-retropropagacao", "Retropropagação", "Backpropagation"),
        ("04-exemplo-fizz-buzz", "Exemplo: Fizz Buzz", "Example: Fizz Buzz"),
    ]),
    (16, 19, "Deep Learning", [
        ("01-o-tensor", "O Tensor", "The Tensor"),
        ("02-a-abstracao-de-camada", "A Abstração de Camada", "The Layer Abstraction"),
        ("03-a-camada-linear", "A Camada Linear", "The Linear Layer"),
        ("04-redes-como-sequencia-de-camadas", "Redes como Sequência de Camadas", "Neural Networks as a Sequence of Layers"),
        ("05-perda-e-otimizacao", "Perda e Otimização", "Loss and Optimization; Example: XOR Revisited"),
        ("06-outras-funcoes-de-ativacao", "Outras Funções de Ativação", "Other Activation Functions; Example: FizzBuzz Revisited"),
        ("07-softmax-e-dropout", "Softmax, Entropia Cruzada e Dropout", "Softmaxes and Cross-Entropy; Dropout"),
        ("08-exemplo-mnist", "Exemplo: MNIST", "Example: MNIST; Saving and Loading Models"),
    ]),
    (17, 20, "Clustering", [
        ("01-a-ideia", "A Ideia", "The Idea"),
        ("02-o-modelo", "O Modelo", "The Model"),
        ("03-exemplo-encontros", "Exemplo: Encontros", "Example: Meetups"),
        ("04-escolhendo-k", "Escolhendo k", "Choosing k"),
        ("05-exemplo-clustering-de-cores", "Exemplo: Clustering de Cores", "Example: Clustering Colors"),
        ("06-clustering-hierarquico", "Clustering Hierárquico Bottom-Up", "Bottom-Up Hierarchical Clustering"),
    ]),
]


def stub_secao(titulo: str, grus_cap: int, titulo_grus: str) -> str:
    return f"""# {titulo}

::: {{.callout-note}}
Esta seção corresponde a *{titulo_grus}*, do capítulo {grus_cap} de @grus2019.
:::

::: {{.callout-warning}}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
"""


def stub_index(nosso: int, grus_cap: int, titulo: str, secoes) -> str:
    linhas = [
        f"# {titulo}",
        "",
        "::: {.callout-note}",
        f"Este capítulo corresponde ao capítulo {grus_cap} de @grus2019.",
        ":::",
        "",
        "::: {.callout-warning}",
        "## Em construção",
        "A visão geral deste capítulo ainda será escrita.",
        ":::",
        "",
        "## Seções",
        "",
        "| Seção | Tópico |",
        "|---|---|",
    ]
    for i, (arquivo, titulo_secao, _) in enumerate(secoes, start=1):
        linhas.append(f"| [{nosso}.{i}]({arquivo}.qmd) | {titulo_secao} |")
    linhas += ["", "## Leituras adicionais", "",
               f"*A seção “For Further Exploration” do capítulo {grus_cap} de @grus2019 entra aqui.*", ""]
    return "\n".join(linhas)


def gerar() -> None:
    criados = pulados = 0
    for nosso, grus_cap, titulo, secoes in LIVRO:
        d = CONTENT / f"cap{nosso:02d}"
        d.mkdir(parents=True, exist_ok=True)

        alvo = d / "index.qmd"
        if alvo.exists():
            pulados += 1
        else:
            alvo.write_text(stub_index(nosso, grus_cap, titulo, secoes), encoding="utf-8")
            criados += 1

        for arquivo, titulo_secao, titulo_grus in secoes:
            alvo = d / f"{arquivo}.qmd"
            if alvo.exists():
                pulados += 1
                continue
            alvo.write_text(stub_secao(titulo_secao, grus_cap, titulo_grus), encoding="utf-8")
            criados += 1
    print(f"criados: {criados}   pulados (já existiam): {pulados}")


def imprimir_yaml() -> None:
    print("  chapters:")
    print('    - text: "Início"')
    print("      href: index.qmd")
    for nosso, grus_cap, titulo, secoes in LIVRO:
        print(f'    - part: "Capítulo {nosso}: {titulo}"')
        print("      chapters:")
        print(f"        - href: content/cap{nosso:02d}/index.qmd")
        print('          text: "Visão Geral"')
        for arquivo, titulo_secao, _ in secoes:
            print(f"        - href: content/cap{nosso:02d}/{arquivo}.qmd")
            print(f'          text: "{titulo_secao}"')


if __name__ == "__main__":
    if "--yaml" in sys.argv:
        imprimir_yaml()
    else:
        gerar()
```

- [ ] **Step 2: Gerar os arquivos**

Run: `python3 scripts/gerar-stubs.py`
Expected: `criados: 105   pulados (já existiam): 0`

Run: `find content -name '*.qmd' | wc -l`
Expected: `105`

- [ ] **Step 3: Injetar o bloco `chapters` no `_quarto.yml`**

Run: `python3 scripts/gerar-stubs.py --yaml`

Substitua no `_quarto.yml` o bloco `chapters:` provisório (as duas linhas de "Início" criadas na Tarefa 2) pela saída completa do comando, mantendo a indentação de dois espaços sob `book:`.

- [ ] **Step 4: Rodar os testes**

Run: `make teste`
Expected: PASS em todos, inclusive `test_todo_qmd_esta_registrado_no_quarto_yml`, `test_dezessete_capitulos` e `test_nenhuma_secao_inventa_numero_de_secao_do_grus`.

- [ ] **Step 5: Renderizar o livro inteiro**

Run: `make render`
Expected: sem erro; `_book/` com 105 páginas mais o índice.

Run: `find _book/content -name '*.html' | wc -l`
Expected: `105`

- [ ] **Step 6: Commit**

```bash
git add scripts/gerar-stubs.py content/ _quarto.yml
git commit -m "feat: 17 capítulos e 88 seções como stubs, registrados no _quarto.yml"
```

---

## Task 7: Capítulo 9 (k-Vizinhos) escrito por inteiro

**Files:**
- Modify: `content/cap09/index.qmd`, `content/cap09/01-o-modelo.qmd`, `content/cap09/02-exemplo-o-dataset-iris.qmd`, `content/cap09/03-a-maldicao-da-dimensionalidade.qmd`

**Interfaces:**
- Consumes: `scratch.linear_algebra.{Vector,distance}`, `scratch.machine_learning.split_data`, `dados/iris.data`
- Produces: o modelo de estilo que os outros 16 capítulos seguem — estrutura de seção, formato do callout de fechamento em `scikit-learn`, uso de semente, e o padrão de citação

Este é o capítulo-modelo. **Ele define o estilo do livro inteiro** — quem escrever o capítulo 5 depois vai copiar a forma daqui.

- [ ] **Step 1: Escrever `content/cap09/index.qmd`**

````markdown
# k-Vizinhos Mais Próximos

::: {.callout-note}
Este capítulo corresponde ao capítulo 12 de @grus2019.
:::

Quase todo modelo deste livro olha o conjunto de dados inteiro para aprender um padrão: ajusta coeficientes, mede erros, itera. O k-vizinhos mais próximos não faz nada disso. Ele não aprende — ele guarda. Na hora de classificar um ponto novo, procura os pontos rotulados mais parecidos e deixa que eles votem.

É o modelo mais simples deste livro, e o primeiro que vale a pena implementar por inteiro. Ele precisa de exatamente duas coisas: uma noção de distância, e a hipótese de que pontos próximos se parecem.

Ao final deste capítulo, você será capaz de:

- Explicar o que o k-vizinhos faz e o que ele deliberadamente ignora
- Implementar uma votação majoritária que resolve empates de forma determinística
- Classificar dados reais com o algoritmo que você escreveu
- Explicar por que aumentar o número de dimensões degrada o método, e demonstrar isso numericamente
- Reconhecer o mesmo algoritmo na interface do `scikit-learn`

## Seções

| Seção | Tópico |
|---|---|
| [9.1](01-o-modelo.qmd) | O Modelo |
| [9.2](02-exemplo-o-dataset-iris.qmd) | Exemplo: O Dataset Iris |
| [9.3](03-a-maldicao-da-dimensionalidade.qmd) | A Maldição da Dimensionalidade |

## Leituras adicionais

O `scikit-learn` traz muitos [modelos de vizinhos mais próximos](https://scikit-learn.org/stable/modules/neighbors.html), incluindo variantes com pesos por distância e estruturas de indexação (`KDTree`, `BallTree`) que evitam comparar o ponto novo com todos os outros.

Para o tratamento estatístico do compromisso entre viés e variância na escolha de *k*, veja @hastie2009.
````

- [ ] **Step 2: Escrever `content/cap09/01-o-modelo.qmd`**

````markdown
# O Modelo

::: {.callout-note}
Esta seção corresponde a *The Model*, do capítulo 12 de @grus2019.
:::

Imagine que você quer prever em quem uma pessoa vai votar. Sem saber mais nada sobre ela, uma aposta razoável é olhar como os vizinhos dela votam. Se você souber mais — idade, renda, quantos filhos tem —, dá para olhar os vizinhos *naquelas dimensões* também, e não só na geográfica.

Essa é a ideia inteira.

::: {.conceito}
O k-vizinhos mais próximos precisa de apenas duas coisas:

1. Uma noção de **distância**
2. A hipótese de que pontos **próximos são parecidos**

Ele não faz nenhuma suposição matemática sobre a forma dos dados e não tem etapa de treino. Em compensação, **ignora quase toda a informação disponível**: a previsão para um ponto novo depende só do punhado de pontos mais próximos dele.
:::

Essa é uma troca real, não um detalhe. O k-vizinhos raramente ajuda a *entender* o fenômeno. Prever o voto de alguém a partir do voto dos vizinhos não diz nada sobre a causa daquele voto — enquanto um modelo baseado em renda e estado civil poderia dizer.

## Contando votos

Escolhido um *k* — 3 ou 5, digamos —, classificar um ponto novo é achar os *k* pontos rotulados mais próximos e deixá-los votar. Precisamos, então, de uma função que conte votos.

A primeira tentativa é direta:

```{python}
from typing import List
from collections import Counter

def raw_majority_vote(labels: List[str]) -> str:
    votes = Counter(labels)
    winner, _ = votes.most_common(1)[0]
    return winner

assert raw_majority_vote(['a', 'b', 'c', 'b']) == 'b'
```

Só que ela não faz nada de inteligente com empates. Se estivéssemos classificando filmes e os cinco mais próximos fossem G, G, PG, PG e R, teríamos dois votos para G e dois para PG. Há três saídas possíveis:

- Escolher um dos vencedores ao acaso
- Ponderar os votos pela distância e pegar o vencedor ponderado
- Reduzir *k* até haver um vencedor único

Vamos implementar a terceira:

```{python}
def majority_vote(labels: List[str]) -> str:
    """Assume que os rótulos estão ordenados do mais próximo ao mais distante."""
    vote_counts = Counter(labels)
    winner, winner_count = vote_counts.most_common(1)[0]
    num_winners = len([count
                       for count in vote_counts.values()
                       if count == winner_count])

    if num_winners == 1:
        return winner                     # vencedor único
    else:
        return majority_vote(labels[:-1])  # tenta de novo sem o mais distante

# Empate: olha os 4 primeiros, então 'b'
assert majority_vote(['a', 'b', 'c', 'b', 'a']) == 'b'
```

::: {.exemplo}
A recursão sempre termina. No pior caso, descartamos um rótulo por vez até sobrar um só — e aí ele vence sozinho.

Repare que o argumento precisa estar **ordenado do mais próximo ao mais distante**. Descartar "o último" só faz sentido se o último for o vizinho menos relevante. Uma lista fora de ordem produz uma resposta errada sem erro nenhum.
:::

## O classificador

Com a votação pronta, o classificador cabe em poucas linhas. A função `distance` vem do capítulo 4:

```{python}
from typing import NamedTuple
from scratch.linear_algebra import Vector, distance

class LabeledPoint(NamedTuple):
    point: Vector
    label: str

def knn_classify(k: int,
                 labeled_points: List[LabeledPoint],
                 new_point: Vector) -> str:

    # Ordena os pontos rotulados do mais próximo ao mais distante.
    by_distance = sorted(labeled_points,
                         key=lambda lp: distance(lp.point, new_point))

    # Pega os rótulos dos k mais próximos...
    k_nearest_labels = [lp.label for lp in by_distance[:k]]

    # ...e deixa que votem.
    return majority_vote(k_nearest_labels)
```

É isso: ordenar por distância, cortar em *k*, contar. Não há treino, não há parâmetros ajustados, não há otimização. O modelo *é* o conjunto de dados.

::: {.callout-tip collapse="true"}
## Na prática: `scikit-learn`

Você acabou de escrever o algoritmo. Na vida real usaria isto:

```python
from sklearn.neighbors import KNeighborsClassifier

modelo = KNeighborsClassifier(n_neighbors=5)
modelo.fit(X_treino, y_treino)
modelo.predict(X_novo)
```

As diferenças que importam: o `scikit-learn` resolve empates escolhendo o rótulo de menor índice (não reduzindo *k*), aceita pesos por distância (`weights='distance'`), e usa estruturas de indexação como `KDTree` para não comparar o ponto novo com todos os outros — o que muda o custo de $O(n)$ por consulta para algo bem menor em dimensões baixas.

Nada disso muda o que o modelo *é*. É a mesma ordenação por distância seguida de votação que você implementou acima.
:::
````

- [ ] **Step 3: Escrever `content/cap09/02-exemplo-o-dataset-iris.qmd`**

Note o `#| label:` em cada chunk, o `eval: false` no trecho de download, e `random.seed(12)` — os três padrões que os outros capítulos vão copiar.

````markdown
# Exemplo: O Dataset Iris

::: {.callout-note}
Esta seção corresponde a *Example: The Iris Dataset*, do capítulo 12 de @grus2019.
:::

O *Iris* é um clássico do aprendizado de máquina. São 150 flores de três espécies, e para cada uma temos quatro medidas: comprimento e largura da pétala, comprimento e largura da sépala. A tarefa é prever a espécie a partir das quatro medidas.

O livro-texto baixa o arquivo do repositório da UCI:

```{python}
#| eval: false
import requests

data = requests.get(
  "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
)

with open('iris.dat', 'w') as f:
    f.write(data.text)
```

::: {.callout-important}
O chunk acima **não é executado** neste livro — repare no `eval: false`.

O arquivo já está em `dados/iris.data`, commitado no repositório. Um livro que faz chamadas de rede a cada renderização é frágil: basta a UCI sair do ar, mudar de URL ou ficar lenta para o material inteiro parar de compilar. O código fica aqui porque saber de onde o dado veio *é* parte da lição; o que não precisa acontecer toda vez é o download.
:::

Os dados são separados por vírgula, com os campos:

```
sepal_length, sepal_width, petal_length, petal_width, class
```

A primeira linha, por exemplo:

```
5.1,3.5,1.4,0.2,Iris-setosa
```

## Carregando os dados

Nossa função de vizinhos espera `LabeledPoint`, então é assim que vamos representar cada flor:

```{python}
#| label: carrega-iris
from typing import Dict, List, NamedTuple
import csv
from collections import defaultdict
from scratch.linear_algebra import Vector

class LabeledPoint(NamedTuple):
    point: Vector
    label: str

def parse_iris_row(row: List[str]) -> LabeledPoint:
    """
    sepal_length, sepal_width, petal_length, petal_width, class
    """
    measurements = [float(value) for value in row[:-1]]
    # a classe vem como "Iris-virginica"; queremos só "virginica"
    label = row[-1].split("-")[-1]

    return LabeledPoint(measurements, label)

with open('dados/iris.data') as f:
    reader = csv.reader(f)
    iris_data = [parse_iris_row(row) for row in reader if row]

# Agrupamos também por espécie, para poder desenhar
points_by_species: Dict[str, List[Vector]] = defaultdict(list)
for iris in iris_data:
    points_by_species[iris.label].append(iris.point)

len(iris_data), sorted(points_by_species)
```

::: {.callout-note}
Duas diferenças em relação ao código do livro, ambas por causa do ambiente deste material:

- O caminho é `dados/iris.data`, não `iris.data`. O `_quarto.yml` define `execute-dir: project`, então o diretório de trabalho de todo chunk é a raiz do projeto, esteja o `.qmd` onde estiver.
- O `if row` no final da compreensão descarta a linha em branco no fim do arquivo da UCI, que faria o `parse_iris_row` estourar.
:::

## Olhando os dados

Gostaríamos de visualizar as medidas para ver como variam por espécie. O problema é que são quatro dimensões, o que dificulta o desenho. Uma saída é olhar os gráficos de dispersão para cada um dos seis pares de medidas:

```{python}
#| label: fig-iris-dispersao
#| fig-cap: "Dispersões do Iris, para os seis pares de medidas"
from matplotlib import pyplot as plt

metrics = ['comprimento sépala', 'largura sépala',
           'comprimento pétala', 'largura pétala']
pairs = [(i, j) for i in range(4) for j in range(4) if i < j]
marks = ['+', '.', 'x']  # três classes, três marcadores

fig, ax = plt.subplots(2, 3, figsize=(10, 6))

for row in range(2):
    for col in range(3):
        i, j = pairs[3 * row + col]
        ax[row][col].set_title(f"{metrics[i]} vs {metrics[j]}", fontsize=8)
        ax[row][col].set_xticks([])
        ax[row][col].set_yticks([])

        for mark, (species, points) in zip(marks, points_by_species.items()):
            xs = [point[i] for point in points]
            ys = [point[j] for point in points]
            ax[row][col].scatter(xs, ys, marker=mark, label=species)

ax[-1][-1].legend(loc='lower right', prop={'size': 6})
plt.tight_layout()
plt.show()
```

As medidas realmente se agrupam por espécie. Olhando só para as sépalas, seria difícil separar *versicolor* de *virginica* — mas quando entram comprimento e largura da pétala, a separação fica clara. É exatamente a situação em que vizinhos mais próximos funciona bem.

## Classificando

Primeiro dividimos os dados em treino e teste:

```{python}
#| label: divide-iris
import random
from scratch.machine_learning import split_data

random.seed(12)
iris_train, iris_test = split_data(iris_data, 0.70)

assert len(iris_train) == 0.7 * 150
assert len(iris_test) == 0.3 * 150

len(iris_train), len(iris_test)
```

::: {.callout-warning}
## A semente não é opcional

`random.seed(12)` está ali para que este material seja reprodutível: sem ela, cada renderização do livro produziria uma divisão diferente, uma acurácia diferente e uma matriz de confusão diferente — e o número que você lê aqui não bateria com o que aparece na sua tela.

Todo chunk deste livro que usa aleatoriedade fixa a semente. Repare que é o `random` da biblioteca padrão, não o `numpy.random` — o livro inteiro é Python puro.
:::

O conjunto de treino são os "vizinhos" que usaremos para classificar os pontos de teste. Falta escolher *k*. Pequeno demais (pense em *k* = 1) e os outliers têm influência exagerada; grande demais (pense em *k* = 105) e simplesmente prevemos a classe mais comum do conjunto. Numa aplicação real criaríamos um conjunto de validação para escolher; aqui vamos usar *k* = 5:

```{python}
#| label: classifica-iris
from typing import Tuple

# quantas vezes vimos cada par (previsto, real)
confusion_matrix: Dict[Tuple[str, str], int] = defaultdict(int)
num_correct = 0

for iris in iris_test:
    predicted = knn_classify(5, iris_train, iris.point)
    actual = iris.label

    if predicted == actual:
        num_correct += 1

    confusion_matrix[(predicted, actual)] += 1

pct_correct = num_correct / len(iris_test)
pct_correct
```

```{python}
#| label: matriz-confusao-iris
for (previsto, real), n in sorted(confusion_matrix.items()):
    marca = "" if previsto == real else "   <-- erro"
    print(f"previsto {previsto:12s} real {real:12s} {n:3d}{marca}")
```

Neste conjunto simples, o modelo acerta quase tudo. Há uma *versicolor* classificada como *virginica* — justamente o par que os gráficos de dispersão mostraram ser o mais difícil de separar — e o resto sai certo.

::: {.callout-tip collapse="true"}
## Na prática: `scikit-learn`

O mesmo experimento, com a biblioteca:

```python
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

X = [p.point for p in iris_data]
y = [p.label for p in iris_data]

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.3, random_state=12
)

modelo = KNeighborsClassifier(n_neighbors=5).fit(X_treino, y_treino)
previsto = modelo.predict(X_teste)

accuracy_score(y_teste, previsto)
confusion_matrix(y_teste, previsto)
```

Sete linhas contra as trinta que escrevemos — e a acurácia não sai idêntica, porque o `train_test_split` embaralha de outro jeito e o desempate é diferente. O que a biblioteca economiza é digitação; o que ela esconde é exatamente o que você acabou de ver.
:::
````

- [ ] **Step 4: Escrever `content/cap09/03-a-maldicao-da-dimensionalidade.qmd`**

````markdown
# A Maldição da Dimensionalidade

::: {.callout-note}
Esta seção corresponde a *The Curse of Dimensionality*, do capítulo 12 de @grus2019.
:::

O k-vizinhos tem um problema sério em dimensões altas, e o nome dele é **maldição da dimensionalidade**. A raiz é simples de enunciar: espaços de dimensão alta são *vastos*. Pontos neles tendem a não estar perto de ninguém.

Dá para ver isso experimentalmente. Vamos gerar pares de pontos aleatórios num "cubo unitário" de dimensão *d*, para vários valores de *d*, e medir as distâncias.

Gerar pontos aleatórios já deve ser natural a esta altura:

```{python}
#| label: pontos-aleatorios
import random
from typing import List
from scratch.linear_algebra import Vector, distance

def random_point(dim: int) -> Vector:
    return [random.random() for _ in range(dim)]

def random_distances(dim: int, num_pairs: int) -> List[float]:
    return [distance(random_point(dim), random_point(dim))
            for _ in range(num_pairs)]
```

Para cada dimensão de 1 a 100, calculamos 10.000 distâncias e guardamos a média e a mínima:

```{python}
#| label: fig-maldicao-distancias
#| fig-cap: "Distância média e mínima entre pontos aleatórios, por dimensão"
#| cache: true
import tqdm
from matplotlib import pyplot as plt

dimensions = range(1, 101)

avg_distances = []
min_distances = []

random.seed(0)
for dim in tqdm.tqdm(dimensions, desc="Maldição da dimensionalidade"):
    distances = random_distances(dim, 10000)
    avg_distances.append(sum(distances) / 10000)
    min_distances.append(min(distances))

plt.plot(dimensions, avg_distances, label='distância média')
plt.plot(dimensions, min_distances, label='distância mínima')
plt.xlabel("# de dimensões")
plt.title("10.000 Distâncias Aleatórias")
plt.legend()
plt.show()
```

::: {.callout-note}
Este chunk leva alguns minutos: são um milhão de pares de pontos, cada um com uma distância euclidiana calculada em Python puro.

Duas coisas o tornam suportável. O `random.seed(0)` garante que o resultado é sempre o mesmo. E `cache: true` faz o Quarto guardar a saída — o chunk só reexecuta se o código dele mudar, então as renderizações seguintes são instantâneas.
:::

A distância média entre dois pontos cresce com a dimensão, o que já era de esperar. O que incomoda é outra coisa: a **razão** entre a menor distância e a distância média.

```{python}
#| label: fig-maldicao-razao
#| fig-cap: "Razão entre a menor distância e a distância média"
min_avg_ratio = [min_dist / avg_dist
                 for min_dist, avg_dist in zip(min_distances, avg_distances)]

plt.plot(dimensions, min_avg_ratio)
plt.xlabel("# de dimensões")
plt.title("Distância Mínima / Distância Média")
plt.show()
```

::: {.conceito}
Em dimensão baixa, o ponto mais próximo está **muito** mais perto que a média — a razão fica perto de zero, e "vizinho mais próximo" significa alguma coisa.

Conforme a dimensão cresce, a razão sobe em direção a 1: o ponto mais próximo está quase tão longe quanto um ponto qualquer. E aí "vizinho mais próximo" deixa de significar coisa alguma.
:::

A intuição por trás disso: dois pontos só estão próximos se estiverem próximos em **todas** as dimensões. Cada dimensão extra — mesmo que seja puro ruído — é mais uma oportunidade para dois pontos ficarem distantes um do outro. Com dimensão suficiente, todo mundo fica longe de todo mundo.

A ressalva importa: isso vale a menos que haja muita estrutura nos dados que os faça se comportar como se tivessem dimensão bem menor. Um conjunto de 100 colunas em que 97 são combinações lineares das outras 3 não é, de fato, um conjunto de 100 dimensões.

::: {.callout-tip collapse="true"}
## Na prática: o que se faz com isso

Quando os dados têm dimensão alta demais para vizinhos mais próximos, as saídas usuais são reduzir a dimensão antes de classificar — PCA, que aparece no capítulo 7, é a mais comum — ou trocar por um modelo que não dependa de distância, como as árvores de decisão do capítulo 14.

O `scikit-learn` não protege você disso. `KNeighborsClassifier` aceita 500 colunas sem reclamar, roda, devolve previsões, e elas serão ruins por um motivo que nenhuma mensagem de erro vai explicar. Saber *por que* é o que esta seção comprou.
:::
````

- [ ] **Step 5: Renderizar só o capítulo 9 e conferir os números**

Run: `docker compose run --rm --no-deps livro quarto render content/cap09/`
Expected: sem erro.

Confira na saída:
- `carrega-iris` devolve `(150, ['setosa', 'versicolor', 'virginica'])`
- `divide-iris` devolve `(105, 45)`
- `classifica-iris` devolve uma acurácia acima de 0,9
- a matriz de confusão mostra pouquíssimos erros, com pelo menos um envolvendo *versicolor*/*virginica*

- [ ] **Step 6: Rodar os testes e renderizar o livro inteiro**

Run: `make teste && make render`
Expected: PASS em tudo; render sem erro.

- [ ] **Step 7: Commit**

```bash
git add content/cap09/
git commit -m "feat: capítulo 9 (k-Vizinhos) escrito por inteiro como modelo de estilo"
```

---

## Task 8: CI, verificação offline e README

**Files:**
- Create: `.github/workflows/quarto-render.yml`, `.devcontainer/devcontainer.json`, `README.md`
- Reference: `../bases_3_estatistica/.github/workflows/quarto-render.yml`

**Interfaces:**
- Consumes: tudo das tarefas anteriores
- Produces: publicação automática em `gh-pages`; `make offline` provando que nenhum chunk depende da rede

- [ ] **Step 1: Provar que o livro renderiza sem rede**

Este é o teste que justifica todas as decisões de vendorização das Tarefas 3 e 4.

Run: `make clean && make offline`
Expected: render completo, sem erro.

Se falhar com erro de DNS ou timeout, algum chunk ainda depende da rede — ache-o pela mensagem e corrija antes de seguir. As suspeitas, em ordem: um `import scratch.getting_data` que não deveria existir, um `requests.get` sem `eval: false`, ou o MNIST sendo baixado em vez de lido de `dados/mnist/`.

- [ ] **Step 2: Criar o workflow**

```yaml
name: Render and Publish

on:
  push:
    branches: [main]
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build-image:
    name: Build da imagem
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login no GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build e push
        uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64
          push: true
          tags: ghcr.io/bragad/undf-bases5-ciencia-de-dados-202602:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  testes:
    name: Invariantes estruturais
    needs: build-image
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: read
    container:
      image: ghcr.io/bragad/undf-bases5-ciencia-de-dados-202602:latest
      credentials:
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Marcar workspace como seguro para o git
        run: git config --global --add safe.directory "$GITHUB_WORKSPACE"

      - name: pytest
        run: pytest tests/ -v

  render:
    name: Renderizar o livro
    needs: testes
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: read
    container:
      image: ghcr.io/bragad/undf-bases5-ciencia-de-dados-202602:latest
      credentials:
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Marcar workspace como seguro para o git
        run: git config --global --add safe.directory "$GITHUB_WORKSPACE"

      - name: Render
        run: quarto render

      - name: Upload do livro renderizado
        uses: actions/upload-artifact@v4
        with:
          name: livro
          path: _book/
          retention-days: 7

  publish:
    name: Publicar no GitHub Pages
    needs: render
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Download do livro renderizado
        uses: actions/download-artifact@v4
        with:
          name: livro
          path: _book

      - name: Publicar na branch gh-pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_book
          publish_branch: gh-pages
```

- [ ] **Step 3: Criar `.devcontainer/devcontainer.json`**

```json
{
  "name": "Bases 5 — Ciência de Dados",
  "dockerComposeFile": "../compose.yaml",
  "service": "livro",
  "workspaceFolder": "/livro",
  "overrideCommand": true,
  "forwardPorts": [4201],
  "customizations": {
    "vscode": {
      "extensions": [
        "quarto.quarto",
        "ms-python.python",
        "ms-toolsai.jupyter"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/opt/venv/bin/python"
      }
    }
  }
}
```

- [ ] **Step 4: Criar o `README.md`**

````markdown
# Bases 5 — Ciência de Dados

Material de apoio da disciplina **Bases 5 — Ciência de Dados**, do curso de Ciência da Computação da UnDF.

O site é publicado automaticamente em
**<https://BragaD.github.io/UnDF-Bases5-CienciaDeDados-202602>**

O livro-texto é Joel Grus, *Data Science from Scratch* (2ª ed., O'Reilly, 2019), e a disciplina cobre seus **capítulos 1 a 4 e 8 a 20**. Todo algoritmo é implementado em Python puro, sem `numpy` e sem `scikit-learn` — a biblioteca aparece só no fecho de cada seção, depois de o leitor ter construído a coisa.

## Rodando localmente

O único pré-requisito é **Docker**. Python, Quarto e todas as bibliotecas vêm dentro do container.

```bash
git clone https://github.com/BragaD/UnDF-Bases5-CienciaDeDados-202602
cd UnDF-Bases5-CienciaDeDados-202602
make preview
```

Abra <http://localhost:4201>. O preview recarrega sozinho quando você salva um `.qmd`.

Outros comandos:

```bash
make render   # gera o livro em _book/
make teste    # invariantes estruturais (registro, caminhos, citações)
make offline  # renderiza SEM REDE — prova que nada depende da internet
make shell    # shell dentro do container
make check    # diagnóstico do Quarto
make build    # reconstrói a imagem (após mudar Dockerfile ou uv.lock)
make clean    # limpa artefatos de render
```

Alternativa sem instalar nada: abra o repositório no **GitHub Codespaces** ou no VS Code com a extensão Dev Containers — o `.devcontainer/` já está configurado.

## Estrutura

```
.
├── _quarto.yml           # Config mestre: 17 capítulos, tema, engine
├── index.qmd             # Página inicial
├── content/capNN/        # Um diretório por capítulo, um .qmd por seção
├── scratch/              # Código do livro-texto, vendorizado (MIT) — NÃO EDITAR
├── im/                   # Vazio de propósito; working_with_data.py grava aqui no import
├── dados/                # Conjuntos de dados, todos commitados
├── scripts/              # Coleta única de dados; gerador de stubs
├── tests/                # Invariantes estruturais (pytest)
├── styles.css            # Classes .conceito e .exemplo, dark mode
├── references.bib        # Bibliografia
├── Dockerfile            # Quarto + Python (via uv.lock)
└── .github/workflows/    # CI: build → testes → render → gh-pages
```

Todo arquivo novo em `content/` precisa ser registrado em `_quarto.yml` — e `make teste` falha se você esquecer.

## O pacote `scratch/`

É a cópia literal do [repositório do Joel Grus](https://github.com/joelgrus/data-science-from-scratch), sob licença MIT (veja `LICENSE-scratch`). **Nunca é editado**: toda adaptação vive no `.qmd`, para que um `diff` contra o upstream continue limpo.

Um detalhe que surpreende: `im/` precisa existir, mesmo vazio, porque `scratch/working_with_data.py` grava um PNG ali no momento do import.

## Dados

Todos os conjuntos em `dados/` são commitados; nada é baixado durante a renderização. `make offline` prova isso. Veja `dados/README.md` para a proveniência de cada arquivo.

## Publicação

O CI constrói a imagem, roda os testes, renderiza e publica em `gh-pages` a cada push na `main`. Há passos manuais, feitos **uma única vez** no GitHub:

1. Criar o repositório e dar push na `main`.
2. Em **Settings → Actions → General → Workflow permissions**, selecionar "Read and write permissions".
3. Depois do primeiro workflow verde, em **Settings → Pages → Source**, escolher "Deploy from a branch" → `gh-pages`, pasta `/ (root)`.

Até o passo 3, a URL acima retorna 404 mesmo com o workflow passando.

## Licença

Material didático disponibilizado para fins educacionais. O código e os exemplos originais são de Joel Grus, sob licença MIT.
````

- [ ] **Step 5: Verificação final completa**

Run: `make clean && make teste && make offline`
Expected: testes PASS, render offline completo sem erro.

- [ ] **Step 6: Commit**

```bash
git add .github/ .devcontainer/ README.md
git commit -m "feat: CI com testes, render e publicação em gh-pages; verificação offline"
```

---

## Auto-revisão do plano

**Cobertura da spec.** Cada requisito da spec tem tarefa: identidade e pedagogia → Tarefa 7 (o modelo de estilo, com o callout de `sklearn` e o texto do `index.qmd` da Tarefa 2); escopo e mapa → Tarefa 6; dados → Tarefa 4; `scratch/` vendorizado e `im/` → Tarefa 3; infra e dependências → Tarefa 1; verificação em três camadas → Tarefas 1 (`make offline`, `make teste`), 5 (invariantes) e 8 (CI); agrupamentos dos caps. 2 e 16 → constante `LIVRO` da Tarefa 6; passos manuais do GitHub → Tarefa 8, `README.md`.

**Lacuna encontrada e coberta:** a spec pede que o `CLAUDE.md` seja atualizado. Ele já foi atualizado antes deste plano (commit `e4ec4ee`) e descreve o design aprovado — nenhuma tarefa nova é necessária, mas quem executar deve reler o `CLAUDE.md` se mudar alguma decisão pelo caminho.

**Consistência de nomes.** `knn_classify`, `majority_vote`, `LabeledPoint`, `parse_iris_row`, `points_by_species`, `iris_train`/`iris_test`, `confusion_matrix` são usados com o mesmo nome e a mesma assinatura entre os Steps 2, 3 e 4 da Tarefa 7. `split_data` e `distance` batem com as assinaturas reais do `scratch/`, verificadas no código. `LabeledPoint` é definido duas vezes de propósito (Tarefa 7 Steps 2 e 3), porque cada `.qmd` é uma página independente e o leitor pode chegar direto na segunda.

**Risco conhecido, não resolvido no plano:** o Step 5 da Tarefa 4 depende de escolher uma imagem CC0 concreta, que não dá para fixar aqui sem navegar. Os critérios estão explícitos e o teste (`dimensão ≤ 600 px`) é verificável; é a única decisão deixada para o executor.
