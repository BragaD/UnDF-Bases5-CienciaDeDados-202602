# Aula: redes neurais, do perceptron ao backpropagation

Slides (Quarto + reveal.js) e código de uma aula de 5 horas. É um projeto Quarto
próprio, separado do livro: nada aqui entra no site nem na suíte de testes.

## Arquivos

| arquivo | o que é |
|---|---|
| `index.qmd` | o deck; só o cabeçalho, o chunk de preparo e os `include` |
| `_0-abertura.qmd` … `_6-treino.qmd` | uma parte da aula por arquivo |
| `tema.scss` | o tema: paleta das páginas de `apoio/` (azul é a ida, laranja é a volta) |
| `desenhos.py` | os diagramas em SVG (neurônio, rede, cadeia de contas, grafo) |
| `gerar_notebook.py` | deriva `redes-neurais.ipynb` dos slides |
| `redes-neurais.ipynb` | o código da aula, para a turma executar |
| `index.html` | o deck renderizado (um arquivo só) |

## Renderizar

Da raiz do repositório:

```bash
export MPLBACKEND=Agg QUARTO_PYTHON=$PWD/.venv/bin/python
quarto render aulas/redes-neurais/index.qmd
.venv/bin/python aulas/redes-neurais/gerar_notebook.py
```

Todo número de saída de código nos slides é executado no render. Os números das
contas "na mão" (em fórmula) são fixos no texto e batem com a saída do código do
slide seguinte; mudou um peso do exemplo, refaça as duas.

## Apresentar

Abra `index.html` no navegador. `→` avança um passo, `F` tela cheia, `S` abre as
notas do apresentador, `O` mostra todos os slides, `M` abre o menu.

As fórmulas (KaTeX) são carregadas da internet; o resto do deck está embutido no
arquivo.
