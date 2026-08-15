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
