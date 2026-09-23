---
paths:
  - "content/**/*.qmd"
  - "notebooks/**/*.ipynb"
  - "atividades/**/*.qmd"
---

# Base de conhecimento do curso: Bases 5 — Ciência de Dados (UnDF)

Lida por `/create-lecture`, `/scaffold-exercises`, `/devils-advocate` e pelos agentes
`pedagogy-reviewer` e `domain-reviewer` **antes** de criar ou revisar conteúdo. O `CLAUDE.md`
e a spec vigente (`docs/superpowers/specs/2026-09-10-estrutura-nova-islp-design.md`) são a
fonte de verdade para escopo, ementa e ambiente; este arquivo guarda o que eles não guardam:
**notação, progressão e armadilhas de conteúdo**. Cresce a cada capítulo — quem escreve um
capítulo acrescenta aqui a notação nova e as armadilhas que mediu.

## Registro de notação

A notação é a do ISLP (@james2023) — a spec proíbe renomear por gosto.

| Regra | Convenção | Exemplo | Anti-padrão |
|---|---|---|---|
| Tamanhos | $n$ observações, $p$ preditores | $X$ é $n \times p$ | $m$, $d$ |
| Preditores e resposta | $X = (X_1, \dots, X_p)$; resposta $Y$; no código, `X` (DataFrame) e `y` (Series) | `X = propaganda[["tv"]]` | `features`, `target` no texto |
| Função e estimativa | $f$ e $\hat f$; previsão $\hat y$ | $\hat y = \hat f(x_0)$ | $h(x)$, $g(x)$ |
| Erro irredutível | $\varepsilon$, $\mathrm{E}(\varepsilon) = 0$ | $Y = f(X) + \varepsilon$ | $e$ |
| Coeficientes | $\beta_0, \beta_1, \dots$; estimados $\hat\beta_j$ | `intercept_`, `coef_` | $w$, $b$ na prosa |
| Soma dos resíduos | RSS $= \sum (y_i - \hat y_i)^2$ | — | SSE |
| Qualidade de ajuste | MSE, $R^2$, RSE; MSE **de treino** × **de teste** sempre qualificado | `mean_squared_error`, `r2_score` | "o erro" sem dizer de qual conjunto |
| Classificação | taxa de erro $\frac{1}{n}\sum I(y_i \ne \hat y_i)$; $\Pr(Y = k \mid X = x)$ | `predict_proba` | "acurácia" sem dizer o conjunto |
| Regularização | $\lambda$ na prosa | o `alpha` do `scikit-learn` (ver armadilhas) | $\alpha$ como símbolo da prosa |
| Nomes de dado | colunas em português, `snake_case`, sem acento; categorias com acento (`"São Paulo"`) | `tv`, `vendas`, `inadimplente` | `sales`, `default` |
| Números | vírgula decimal e ponto de milhar na prosa ("10.692", "0,25"); em LaTeX, `0{,}25` | — | `0.25` na prosa |

## Progressão do livro

| Capítulo | Pergunta central | Fonte | Dados |
|---|---|---|---|
| 6 — Dados e `pandas` | Que tipo de dado eu tenho, e como ele chega a um `X` e um `y`? | — (modelo de estilo da casa) | `estados.csv`, `alugueis.csv`, `cidades.csv` |
| 7 — Aprendizado estatístico | O que é estimar $f$, e como saber se estimei bem? | ISLP 2 (7.1 = lab 2.3) | `Advertising`, `Income1`, `Income2`, `alugueis` |
| 8 — Regressão linear | Uma reta, várias, e quando ela falha | ISLP 3 (sem inferência) | `Advertising`, `Auto`, `Credit` |
| 9 — Classificação | Por que não uma reta, e como julgar um classificador | ISLP 4 | `Default`, `Auto` |
| 10 a 16 | ver a spec | ISLP 5, 6, 8.1, 8.2, 10, 12, 9 | ver a spec |
| 17 — Do começo ao fim | Um problema real inteiro, sem vazamento | — | a definir no plano |

`train_test_split` e a distinção treino/teste nascem no cap. 7 e são usados por todos os
seguintes. Validação cruzada nasce no cap. 10 — antes dele, não se usa `cross_val_score`
sem apresentá-lo.

## Armadilhas de código ↔ teoria (verificadas)

| Armadilha | Impacto | Correção |
|---|---|---|
| `LogisticRegression` do `scikit-learn` é **regularizada por padrão** (L2, `C=1.0`); a logística do ISLP 4.3 não é | coeficientes encolhidos, diferentes dos do livro, sem aviso | `C=np.inf` (o cap. 9 usa) ou `penalty=None`, e o texto diz por quê |
| `Lasso` minimiza $\frac{1}{2n}\mathrm{RSS} + \alpha\lVert\beta\rVert_1$; o ISLP (6.7) escreve $\mathrm{RSS} + \lambda\lVert\beta\rVert_1$. `Ridge` usa $\mathrm{RSS} + \alpha\lVert\beta\rVert_2^2$ | o mesmo número em `alpha` não é o mesmo $\lambda$ entre os dois | no lasso, $\alpha = \lambda / (2n)$; a prosa fala de $\lambda$ e o código diz a conversão |
| `cross_val_score(..., scoring="neg_mean_squared_error")` devolve MSE **negativo** | "o maior score" é o menor erro; média negativa impressa na prosa | trocar o sinal no chunk, antes de imprimir |
| `predict_proba` ordena as colunas por `classes_`, não pela ordem em que a prosa pensa | a coluna 1 nem sempre é "sim" | indexar pela posição de `classes_` |
| `pd.get_dummies(..., drop_first=True)` descarta a primeira categoria **em ordem alfabética** | a base muda se a categoria mudar de nome | dizer qual é a base; para trocar, ordenar as categorias antes (a 8.4 faz) |
| Ridge, lasso, *k*-NN, SVM e PCA dependem da escala dos preditores | um preditor em reais domina um em anos | `StandardScaler` dentro de um `Pipeline` (depois do cap. 10, ajustado só no treino) |
| `train_test_split` sem `random_state` | a divisão muda a cada render; todo número da prosa fica velho | `random_state=<n>` sempre (INV-5) |
| `pd.read_html` sem `flavor="bs4"` | `ImportError` (o `lxml` não está no `uv.lock`) | `flavor="bs4"`; **não** instalar `lxml` |
| Marcador `N/D` não é nulo padrão do `pandas` (`n/a` é) | a coluna vira `object` e `sum()` concatena texto, sem erro | `na_values=["N/D"]` |
| `memory_usage(deep=True)` em coluna de texto não-ASCII depois de `nunique()` | 730.981 × 795.738 bytes na coluna `cidade` de `alugueis.csv` | medir a memória **antes** de explorar a coluna |
| Mensagem de `TypeError` do `pandas` concatena a coluna inteira | 12.722 caracteres na 6.3 | `try/except` e truncar (INV-10) |
| Saída de numpy 2 com `np.float64(...)` numa tupla | ruído na saída do chunk | `float(...)` antes de exibir |
| `set` de strings sai em ordem diferente a cada processo | saída muda a cada render | `sorted(...)` |

## Anti-padrões já vividos

| Anti-padrão | O que aconteceu | Correção |
|---|---|---|
| Superlativo "conferido" no olho | a 6.5 disse que São Paulo tinha a maior distância média–mediana; era Belo Horizonte, e a tabela estava logo acima | chunk que ordena/compara (INV-8) |
| Decisão de seção anterior perdida | a 6.4 preencheu `andar` com zero; a 6.5 releu o CSV e mostrou os 2.461 nulos de volta | reconstruir no setup (INV-9) |
| Epígrafe sem fonte primária | "In God we trust; all others must bring data" não tem evidência de ser de Deming | sem verificação em fonte primária, a citação não entra |
| "Você provavelmente já ajustou uma reta com `.fit()`" | a turma não confirmou essa premissa | não assumir modelo treinado antes |
| Remissão a Bases 3 | a turma não cursou com este professor | assumir o **tema**, nunca o **tratamento** |
| Meta-texto sobre o ISLP | "É essa pergunta que abre o ISLP, com o exemplo que também abre esta seção"; "A função exata que os autores usaram […] não está disponível fora do pacote `ISLP` do R, que este material não instala" | falar só do assunto; o ISLP fica no callout (INV-13) |
| Ponte forçada | "O capítulo anterior fechou com `X` e `y` prontos…"; "A seção anterior fechou perguntando o que significa estimar uma função…" | abrir pela pergunta, pelo dado ou pelo fenômeno (INV-13) |
