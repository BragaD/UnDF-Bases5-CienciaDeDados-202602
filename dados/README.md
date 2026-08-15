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
| `imagem-cores.jpg` | 17 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Piet_Mondriaan,_1930_-_Mondrian_Composition_II_in_Red,_Blue,_and_Yellow.jpg) — Piet Mondriaan, *Composition II in Red, Blue, and Yellow* (1930); domínio público (autor falecido em 1944 — PD-old, PD-Art, PD-1923); redimensionada para no máximo 600 px no lado maior |

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

Escolhemos *Composition II in Red, Blue, and Yellow* (1930), de Piet Mondriaan:
poucos blocos de cor sólida (vermelho, azul, amarelo, branco, preto), o que
torna o resultado do k-means fácil de interpretar mesmo com k pequeno.
Domínio público nos Estados Unidos (obra publicada antes de 1931) e no
Brasil (autor falecido em 1944, mais de 70 anos). Fonte:
<https://commons.wikimedia.org/wiki/File:Piet_Mondriaan,_1930_-_Mondrian_Composition_II_in_Red,_Blue,_and_Yellow.jpg>.
