# Notebooks de aula

Um notebook por capítulo, para executar ao vivo na aula. O conteúdo é o mesmo
do livro — mesma prosa, mesmas células de código, mesma ordem.

## Como abrir

```bash
make jupyter          # JupyterLab em http://localhost:8901
```

O Lab abre na raiz do projeto, e não dentro desta pasta, para você enxergar
`dados/` e `scratch/` junto. Não é preciso instalar nada na máquina: tudo roda
dentro do container, com as versões travadas no `uv.lock`.

Se preferir abrir os `.ipynb` em outro editor (VS Code, PyCharm), aponte o
kernel para o Python do container. O que **não** funciona é rodar com o Python
do sistema: o livro depende do `scratch/` e das versões fixadas.

## Como executar

De cima para baixo, sem pular. A primeira célula de código é de preparo —
ela põe o diretório de trabalho na raiz do projeto, que é o que faz
`from scratch.linear_algebra import dot` e `pd.read_csv("dados/stocks.csv")`
funcionarem. Rode-a primeiro, mesmo que você queira ir direto ao meio do
capítulo.

Depois dela, a ordem importa: quase toda seção usa nomes definidos na
anterior. Um `NameError` no meio do capítulo quase sempre significa que uma
célula acima ficou por executar.

## Uma diferença de execução em relação ao livro

No site, **cada seção roda no seu próprio kernel** — nomes não atravessam
páginas, e é por isso que os `import` se repetem de uma seção para outra. No
notebook, o capítulo inteiro roda num kernel só.

Na prática isso só ajuda: a ordem de leitura é a mesma, então tudo que uma
seção precisa já foi definido acima. Vale saber, porém, que uma célula que
funciona aqui pode depender de algo definido numa seção anterior — no site,
aquela mesma célula traz o `import` junto.

## Estes arquivos são gerados

Os notebooks saem de `scripts/gerar-notebooks.py`, que lê os `.qmd` de
`content/`. **O livro é a fonte da verdade.** Editar um `.ipynb` à mão é
trabalho perdido: o próximo `make notebooks` sobrescreve.

Para mudar o conteúdo de uma aula, edite o `.qmd` correspondente em
`content/capNN/` e rode:

```bash
make notebooks        # regenera os 17
make teste            # confere que nenhum ficou defasado
make notebooks-teste  # executa os 17 de ponta a ponta (demora)
```

Três coisas o gerador traduz, porque o Jupyter não entende o que o Quarto
entende:

- **Callouts** (`::: {.callout-note}`) viram blockquotes com rótulo. Os que
  embrulham código que executa são abertos, para o código continuar sendo
  célula de código — senão o notebook quebraria adiante.
- **Links entre capítulos** viram URLs do site publicado. Um caminho relativo
  a `../cap05/index.qmd` não resolve de dentro desta pasta.
- **Citações** (`@grus2019`) viram o texto da citação, com a bibliografia
  numa célula ao fim do notebook.

## Sem saídas gravadas

Os arquivos entram no git limpos, sem saída de execução. É de propósito: quem
executa é o aluno, na aula. Saída congelada no arquivo transformaria o diff do
git em ruído e tiraria o sentido de rodar o código.
