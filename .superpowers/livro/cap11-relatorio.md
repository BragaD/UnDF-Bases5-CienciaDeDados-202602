# Relatório — Capítulo 11 (Regressão Linear Simples)

## O que foi feito

Escritos os 4 arquivos de `content/cap11/`, substituindo os stubs "Em construção":

- `index.qmd` — abertura, epígrafe (Chesterton, "traçar a linha em algum lugar"), objetivos, tabela de seções, leituras adicionais apontando para o Capítulo 12.
- `01-o-modelo.qmd` — carrega `num_friends_good`/`daily_minutes_good` de `scratch.statistics` (com `#| include: false` + `plt.close('all')`, documentado em callout); apresenta o modelo $y_i = \beta x_i + \alpha + \varepsilon_i$ com callout de causalidade; implementa `predict`, `error`, `sum_of_sqerrors`, `least_squares_fit` (fórmula fechada); testa em dado sintético; ajusta aos dados reais; gráfico de dispersão + reta (citando cap. 3); calcula R² e interpreta; fecha com "Na prática: scikit-learn".
- `02-usando-gradiente-descendente.qmd` — importa `alpha`/`beta` já ajustados de `scratch.simple_linear_regression` (fórmula fechada, renomeados `alpha_fechada`/`beta_fechada`); repete o ajuste via `gradient_step` do Capítulo 5 (10.000 epochs, `random.seed(0)`); compara lado a lado os dois resultados; fecha com "Na prática: diferenciação automática" (autodiff/backprop, apontando para caps. 15–16).
- `03-maxima-verossimilhanca.qmd` — constrói a intuição de verossimilhança antes da álgebra (callout `.conceito` sobre "dados menos surpreendentes"), deriva por que a suposição de erros normais faz maximizar verossimilhança coincidir com minimizar `sum_of_sqerrors`, ilustra numericamente comparando mínimos quadrados vs. "sempre prever a média", e aponta para a Regressão Logística (Cap. 13, Bernoulli em vez de Normal) como o motivo de ela não ter fórmula fechada.

A dívida do Capítulo 5 (`05-ajustando-modelos.qmd`) foi cumprida: seção 11.1 mostra a fórmula fechada, seção 11.2 mostra gradiente descendente convergindo ao mesmo `theta`, com referências cruzadas explícitas nos dois sentidos.

## Verificação

- `make render`: **render OK (tentativa 2)** — a 1ª tentativa abortou com o `Directory not empty` conhecido (corrida de bind mount, não erro de conteúdo); a 2ª convergiu normalmente, como o `Makefile` já prevê.
- `make teste`: **21/21 passaram**, incluindo o teste novo de chunk com linha indentada e o de número de seção do Grus inventado.
- Figura `fig-regressao-amigos-minutos` (`_book/content/cap11/01-o-modelo_files/figure-html/fig-regressao-amigos-minutos-output-1.png`) foi aberta e conferida: reta cruzando a nuvem de pontos concentrada em x baixo, com dispersão vertical grande — bate com o texto.

## Números conferidos contra a saída renderizada

- `n = 203`, média de amigos ≈ 6,88, média de minutos ≈ 29,16, correlação ≈ 0,574.
- Fórmula fechada: α ≈ 22,9476, β ≈ 0,9039.
- R² ≈ 0,3291.
- Gradiente descendente (10.000 epochs): α ≈ 22,9476, β ≈ 0,9039 — diferença para a fórmula fechada da ordem de 10⁻⁷ (α) e 10⁻⁸ (β).
- Soma dos erros ao quadrado: mínimos quadrados ≈ 13.196,6; "sempre prever a média" ≈ 19.670,3 (igual ao `total_sum_of_squares` da seção 1).

Todos os valores acima foram extraídos diretamente do HTML renderizado, não da memória.

## Preocupações

Nenhuma pendência conhecida. Os testes de estrutura (citação do Grus, número de seção não inventado, indentação de chunk) foram checados manualmente com o mesmo regex dos testes antes do render, além de passarem em `make teste`.
