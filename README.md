# Bases 5 — Ciência de Dados

Material de apoio da disciplina **Bases 5 — Ciência de Dados**, do curso de Ciência da Computação da UnDF.

O site é publicado automaticamente em
**<https://BragaD.github.io/UnDF-Bases5-CienciaDeDados-202602>**

Um Quarto book: um diretório por capítulo, um `.qmd` por seção, tudo executável e renderizado dentro de um container.

O material está em transição de abordagem — os capítulos 6 a 17 saíram do livro em 2026-09-10 e estão em `arquivo/grus/`. Antes de escrever qualquer coisa, leia `CLAUDE.md` e `docs/superpowers/specs/2026-09-10-ruptura-com-o-grus-design.md`.

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
├── _quarto.yml           # Config mestre: capítulos, tema, engine
├── index.qmd             # Página inicial
├── content/capNN/        # Um diretório por capítulo, um .qmd por seção
├── notebooks/            # Um .ipynb por capítulo, gerado a partir dos .qmd
├── apoio/                # Páginas HTML interativas para projetar em aula
├── atividades/           # Listas e provas, fora do projeto-livro
├── arquivo/grus/         # Material morto — não é fonte para nada
├── scratch/              # Código vendorizado (MIT) — NÃO EDITAR
├── im/                   # Vazio de propósito; visualization.py grava 9 PNGs aqui no import
├── dados/                # Conjuntos de dados, todos commitados
├── scripts/              # Coleta única de dados; geradores de stubs e notebooks
├── tests/                # Invariantes estruturais (pytest)
├── styles.css            # Classes .conceito e .exemplo, dark mode
├── references.bib        # Bibliografia
├── Dockerfile            # Quarto + Python (via uv.lock)
└── .github/workflows/    # CI: build → testes → render → gh-pages
```

Todo arquivo novo em `content/` precisa ser registrado em `_quarto.yml` — e `make teste` falha se você esquecer.

## O pacote `scratch/`

É a cópia literal do [repositório do Joel Grus](https://github.com/joelgrus/data-science-from-scratch), sob licença MIT (veja `LICENSE-scratch`), e é o código dos capítulos 1 a 5. **Nunca é editado**: toda adaptação vive no `.qmd`, para que um `diff` contra o upstream continue limpo.

Um detalhe que surpreende: `im/` precisa existir, mesmo vazio, porque `scratch/visualization.py` (capítulo 3) tem nove `plt.savefig('im/viz_*.png')` no corpo do módulo — importá-lo grava os nove PNGs ali, a cada render. `working_with_data.py` também escreveria em `im/` no import, mas esse módulo nunca é importado (ver `CLAUDE.md`) — a razão viva para `im/` existir é `visualization.py`.

## `arquivo/grus/`

Os capítulos 6 a 17 como estavam antes da mudança de abordagem, em 2026-09-10, junto com os notebooks derivados deles, o pacote `scratch_np/` e os planos das duas reescritas. Está no `.quartoignore` e fora da suíte de testes. **Não é fonte para nada** — a razão está no `README.md` de lá.

## Dados

Todos os conjuntos em `dados/` são commitados; nada é baixado durante a renderização. `make offline` prova isso. Veja `dados/README.md` para a proveniência de cada arquivo.

## Publicação

O CI constrói a imagem, roda os testes, renderiza offline (prova que nada depende da rede) e com rede, e publica em `gh-pages` a cada push na `main`. Há passos manuais, feitos **uma única vez** no GitHub:

1. Criar o repositório e dar push na `main`.
2. Em **Settings → Actions → General → Workflow permissions**, selecionar "Read and write permissions".
3. Depois do primeiro workflow verde, em **Settings → Pages → Source**, escolher "Deploy from a branch" → `gh-pages`, pasta `/ (root)`.

Até o passo 3, a URL acima retorna 404 mesmo com o workflow passando.

## Licença

Material didático disponibilizado para fins educacionais. O código reproduzido em `scratch/` é de Joel Grus, sob licença MIT.
