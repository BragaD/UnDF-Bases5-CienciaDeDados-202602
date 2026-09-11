# Conjuntos de Dados

Todos os arquivos deste diretório são **commitados**. Nenhum é baixado em tempo
de render: um livro que faz chamadas de rede a cada render é frágil — a página
raspada muda de layout, a API sai do ar, e o material quebra sem ninguém ter
tocado no repositório.

Do capítulo 6 em diante, coluna e variável estão em **português**: minúsculas,
`snake_case`, sem acento no nome; o valor de categoria preserva a grafia
correta (com acento, quando é o caso).

## `estados.csv` — 27 unidades federativas

População e taxa de homicídios de **2024**.

| Coluna | Fonte |
|---|---|
| `estado`, `sigla` | IBGE — [API de localidades](https://servicodados.ibge.gov.br/api/v1/localidades/estados) |
| `populacao` | IBGE — SIDRA, tabela 6579, variável 9324, ano 2024 |
| `taxa_homicidios` | Atlas da Violência (Ipea/FBSP), edição de 2024 — por 100 mil habitantes |

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

## `Advertising.csv`, `Income1.csv`, `Income2.csv` — os três do capítulo 7 (ISLP)

Do [site oficial de @james2023](https://www.statlearning.com/s/), *An
Introduction to Statistical Learning*. O capítulo 7 atual (*O que é
aprendizado estatístico*, ISLP) usa os três; o resto do capítulo roda sobre
dado simulado.

A coleta é feita uma única vez por `scripts/baixar-dados.py`, que baixa a
versão original — em inglês, com o índice do R:

```bash
docker compose run --rm --no-deps livro python scripts/baixar-dados.py
```

Depois do download, os cabeçalhos são traduzidos à mão e a coluna de índice
do R é removida. É essa tabela de-para que mantém a ponte com o livro-texto
— o **nome do arquivo** não muda, só o cabeçalho:

**`Advertising.csv`** — 200 mercados, investimento em publicidade e vendas.

| Original (R) | Traduzida |
|---|---|
| `Unnamed: 0` (índice do R) | *(removida)* |
| `TV` | `tv` |
| `radio` | `radio` |
| `newspaper` | `jornal` |
| `sales` | `vendas` |

**`Income1.csv`** — 30 pessoas, escolaridade e renda.

| Original (R) | Traduzida |
|---|---|
| `Unnamed: 0` (índice do R) | *(removida)* |
| `Education` | `escolaridade` |
| `Income` | `renda` |

**`Income2.csv`** — 30 pessoas, escolaridade, senioridade e renda.

| Original (R) | Traduzida |
|---|---|
| `Unnamed: 0` (índice do R) | *(removida)* |
| `Education` | `escolaridade` |
| `Seniority` | `senioridade` |
| `Income` | `renda` |

`Income1` e `Income2` são **simulados pelos autores** de @james2023, não são
dado observado. É por isso que o capítulo pode desenhar o *f* verdadeiro nas
figuras: quando o dado é gerado por uma função conhecida mais ruído, dá para
mostrar, ao lado do ajuste, o erro que nenhum modelo consegue eliminar —
coisa que não é possível fazer com dado real, onde o *f* verdadeiro é
justamente o que se está tentando estimar.

## O que saiu

Os conjuntos da abordagem de obtenção de dados abandonada — `stocks.csv`,
`comma_delimited_stock_prices.csv`, `getting-data.html`, `iris.data`,
`spam-assuntos.csv`, `imagem-cores.jpg` e `mnist/` — saíram deste diretório.
Nenhum capítulo publicado os lia; continuam recuperáveis no histórico do git,
se algum dia forem necessários de novo.
