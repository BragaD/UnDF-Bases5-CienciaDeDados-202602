# Conjuntos de Dados

## `estados.csv` — 27 unidades federativas

População e taxa de homicídios de **2024**.

| Coluna | Fonte |
|---|---|
| `Estado`, `Sigla` | IBGE — [API de localidades](https://servicodados.ibge.gov.br/api/v1/localidades/estados) |
| `Populacao` | IBGE — SIDRA, tabela 6579, variável 9324, ano 2024 |
| `Taxa.Homicidios` | Atlas da Violência (Ipea/FBSP), edição de 2024 — por 100 mil habitantes |

## `alugueis.csv` — 10.692 imóveis para alugar em 5 cidades

São Paulo, Rio de Janeiro, Belo Horizonte, Porto Alegre e Campinas.

Fonte: *Brazilian houses to rent* (v2), publicado no Kaggle por rubenssjr sob
**CC0** (domínio público). Só os nomes das colunas e os dois campos binários
foram traduzidos para o português.

**Nada foi limpo, de propósito.** A coluna `andar` traz `"-"` em 2.461 das
10.692 linhas (23%), o que faz o `pandas` lê-la como `object` em vez de
número — é a armadilha que a seção 6.3 usa para mostrar que a inferência de
tipo é heurística, não garantia. Os outliers também ficaram: há um imóvel de
46.335 m² e um condomínio de R$ 1.117.000.

## `cidades.csv` — as 5 cidades, com UF e região

Escrito à mão. Existe para a seção 6.5 ter um `merge` de verdade: liga
`alugueis.csv` a `estados.csv` pela sigla. São Paulo e Campinas dividem a
mesma UF, então a junção é um muitos-para-um real.

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
| `imagem-cores.jpg` | 17 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Piet_Mondriaan,_1930_-_Mondrian_Composition_II_in_Red,_Blue,_and_Yellow.jpg) — Piet Mondriaan, *Composition II in Red, Blue, and Yellow* (1930); domínio público (autor falecido em 1944 — PD-old, PD-Art, PD-US por publicação pré-1931); redimensionada para no máximo 600 px no lado maior |

## `Advertising.csv`, `Income1.csv`, `Income2.csv` — os três do capítulo 7 (ISLP)

Do [site oficial de @james2023](https://www.statlearning.com/s/), *An
Introduction to Statistical Learning*. O capítulo 7 atual (*O que é
aprendizado estatístico*, ISLP) usa os três; o resto do capítulo roda sobre
dado simulado.

| Coluna | `Advertising.csv` | `Income1.csv` | `Income2.csv` |
|---|---|---|---|
| — | 200 mercados, investimento em publicidade (`TV`, `radio`, `newspaper`, em milhares de dólares) e `sales` (milhares de unidades) | 30 pessoas, `Education` (anos) e `Income` (milhares de dólares) | 30 pessoas, `Education`, `Seniority` e `Income` |

Os três vêm do R e trazem, como primeira coluna, um **índice sem nome** — o
`pandas` o lê como `Unnamed: 0`. O arquivo fica como veio: não removemos essa
coluna do CSV, é assunto de como cada seção lê o arquivo.

`Income1` e `Income2` são **simulados pelos autores** de @james2023, não são
dado observado. É por isso que o capítulo pode desenhar o *f* verdadeiro nas
figuras: quando o dado é gerado por uma função conhecida mais ruído, dá para
mostrar, ao lado do ajuste, o erro que nenhum modelo consegue eliminar —
coisa que não é possível fazer com dado real, onde o *f* verdadeiro é
justamente o que se está tentando estimar.

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
