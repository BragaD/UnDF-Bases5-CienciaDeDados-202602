# Reescrita dos capítulos 6–17 com numpy

**Data:** 2026-09-06
**Status:** decidido pelo autor; este documento fixa as consequências
**Branch:** `reescrita-numpy`

## A decisão

O autor pediu, textualmente: *"reescreva em uma nova branch os capítulos de 06 a 17 sem essa estratégia de fazer tudo em Python puro. Não use scikit-learn, mas pode utilizar numpy. Os modelos e algoritmos devem ser construídos com numpy."*

Isto inverte, para os capítulos 6 a 17, a decisão pedagógica central da spec original (`2026-08-15-estrutura-livro-bases5-design.md`, seção "Pedagogia"): lá, *"o pacote `scratch/` não importa numpy em lugar nenhum"* era a tese do livro. A tese nova é dividida em duas metades:

- **Capítulos 1–5 continuam em Python puro.** O capítulo 4 (Álgebra Linear) segue ensinando `Vector = List[float]` e `dot` como `sum` sobre `zip`, e o capítulo 5 (Gradiente Descendente) segue iterando sobre listas. Esses capítulos são a **motivação** do numpy: quem escreveu `dot` à mão entende o que `@` faz. O pacote `scratch/` continua vendorizado, intocado, com o hash travado em `tests/test_scratch.py`.
- **Capítulos 6–17 constroem os modelos com numpy.** Vetores e matrizes são `np.ndarray`; produto escalar é `@`; somas sobre pontos viram reduções com `axis`; laços sobre os dados viram operações vetorizadas. O algoritmo continua sendo escrito por nós — o que muda é a calculadora, não o autor.

O que **não** muda: a identidade do livro ("abre as caixas-pretas"), a estrutura (17 capítulos, 87 seções, 104 `.qmd`, mesmos nomes de arquivo, mesma numeração), os dados, as citações ao Grus, o callout de fechamento em `scikit-learn`, os notebooks derivados, a suíte de invariantes.

## A regra que decide cada dúvida: numpy é a calculadora, não o modelo

Numpy entra para fazer **álgebra linear, broadcasting, reduções, indexação booleana e sorteio**. O que o capítulo existe para ensinar — a regra de atualização do gradiente, o critério de partição da árvore, a votação do k-NN, a verossimilhança do Naive Bayes, os passos do k-means, a retropropagação — continua escrito por nós, linha a linha, no `.qmd`.

Concretamente:

| Pode e deve | Não pode |
|---|---|
| `X @ w`, `X.T @ X`, `np.linalg.solve`, `np.linalg.inv`, `np.linalg.norm` | `np.linalg.lstsq` **como** implementação da regressão (só como conferência, num callout) |
| `np.mean`, `np.std(ddof=1)`, `np.var`, `np.corrcoef`, `np.cov` | `np.polyfit` |
| `np.argmax`, `np.argsort`, `np.unique(return_counts=True)`, `np.bincount` | qualquer `sklearn.*` num chunk executável |
| `rng.permutation`, `rng.random`, `rng.normal`, `rng.choice` | `np.random.seed` global, `random` da stdlib |
| máscaras booleanas para partições e minibatches | `scipy.*` (não é dependência declarada) |
| `np.exp`, `np.log`, `np.tanh`, `np.maximum`, `np.where` | reimplementar em Python o que a linha à esquerda já faz |

A pergunta de desempate é: **o aluno ainda vê a fórmula?** `beta = np.linalg.solve(X.T @ X, X.T @ y)` mostra as equações normais; `np.linalg.lstsq(X, y)` esconde. `np.corrcoef(x, y)[0, 1]` é aceitável porque correlação é assunto de Bases 3, assumido — não é o que o capítulo ensina.

**Laços continuam existindo** onde o laço *é* o algoritmo: a iteração do gradiente descendente, as épocas de treino, a recursão da árvore de decisão, a repetição do k-means até convergir, a fusão par a par do clustering hierárquico. O que sai é o laço **sobre os pontos de dados** — esse vira uma operação de array.

## O pacote `scratch_np/`

Novo pacote na raiz, **nosso** (não vendorizado; editável; testado em `tests/test_scratch_np.py`). Espelha o `scratch/` do Grus módulo a módulo, com os **mesmos nomes de função** sempre que a função existe nos dois — assim a correspondência com o livro-texto continua evidente e o aluno acha no Grus a versão em listas do que está lendo em arrays.

| Módulo | Dono | Conteúdo |
|---|---|---|
| `scratch_np/gradient_descent.py` | andaime (orquestrador) | `gradient_step`, `minibatches` |
| `scratch_np/machine_learning.py` | andaime; **cap. 8 ensina** | `split_data`, `train_test_split`, `accuracy`, `precision`, `recall`, `f1_score` |
| `scratch_np/probability.py` | andaime | `normal_cdf`, `inverse_normal_cdf` (vetorizadas) |
| `scratch_np/statistics.py` | andaime | os dados da DataSciencester como arrays (`num_friends`, `daily_minutes` e as versões `_good`) |
| `scratch_np/working_with_data.py` | cap. 7 | `rescale`, `pca`, `de_mean`, `direction`, `first_principal_component`, ... |
| `scratch_np/k_nearest_neighbors.py` | cap. 9 | `majority_vote`, `knn_classify`, `random_distances` |
| `scratch_np/naive_bayes.py` | cap. 10 | `tokenize`, `Message`, `NaiveBayesClassifier` |
| `scratch_np/simple_linear_regression.py` | cap. 11 | `predict`, `error`, `sum_of_sqerrors`, `least_squares_fit`, `total_sum_of_squares`, `r_squared` |
| `scratch_np/multiple_regression.py` | cap. 12 | `inputs` (dados), `predict`, `least_squares_fit`, `multiple_r_squared`, bootstrap, `p_value`, ridge |
| `scratch_np/logistic_regression.py` | cap. 13 | `xs`, `ys` (dados), `logistic`, `negative_log_likelihood`, gradientes |
| `scratch_np/decision_trees.py` | cap. 14 | `entropy`, `partition_entropy`, `build_tree_id3`, `classify`, `inputs` (dados) |
| `scratch_np/neural_networks.py` | cap. 15 | `sigmoid`, `feed_forward`, `sqerror_gradients`, `binary_encode`, `fizz_buzz_encode` |
| `scratch_np/deep_learning.py` | cap. 16 | `Tensor = np.ndarray`, `Layer`, `Linear`, `Sequential`, perdas, otimizadores, `Dropout`, `softmax` |
| `scratch_np/clustering.py` | cap. 17 | `KMeans`, `squared_clustering_errors`, `bottom_up_cluster`, ... |

**Módulos que não existem em `scratch_np/`, de propósito:** `linear_algebra` (é o numpy inteiro — `dot` é `@`, `distance` é `np.linalg.norm(a - b)`, `vector_mean` é `X.mean(axis=0)`), `getting_data` (o capítulo 6 escreve os chunks direto, como já faz), `visualization`.

**Dados que moram em `scratch/`** (as listas hard-coded do Grus: `statistics.num_friends`, `multiple_regression.inputs`, `logistic_regression.data`, `decision_trees.inputs`, `naive_bayes` não tem) são **reexportados como arrays** pelo módulo correspondente de `scratch_np/`. Essa é a **única** situação em que um arquivo de `scratch_np/` pode importar `scratch.*`: para pegar dado, nunca função. Importar `scratch.statistics` desenha figuras no nível do módulo — o reexportador faz `plt.close('all')` depois.

### O padrão "a seção implementa, a próxima importa"

Igual ao capítulo 9 hoje: cada `.qmd` roda num kernel próprio, então a seção que ensina o algoritmo o escreve inline num chunk, e as seções seguintes (e os capítulos seguintes) importam **o mesmo código** de `scratch_np/`. O código do módulo e o código do chunk são idênticos — o módulo é o chunk salvo em arquivo. Quando o texto diz *"`knn_classify` não é redefinida aqui: vem de `scratch_np.k_nearest_neighbors`, o mesmo código que você escreveu na seção anterior"*, isso precisa ser verdade.

### Convenções de array

- `import numpy as np` no topo de cada chunk que o usa (cada `.qmd` é um kernel).
- Matriz de dados `X` tem forma `(n, d)`: uma linha por observação, uma coluna por atributo. Alvo `y` tem forma `(n,)`. Parâmetros `w`, `beta`, `theta` têm forma `(d,)`. Um único ponto é `(d,)`.
- `dtype=float` explícito ao construir arrays a partir de dados lidos (`np.array(..., dtype=float)`), para não herdar `int` por acidente.
- Anotações de tipo usam `np.ndarray`. Não criar aliases como `Vector = np.ndarray` — o alias do Grus existia porque `List[float]` não dizia "vetor"; `np.ndarray` já diz.
- Onde o Grus usa a fórmula amostral (variância e desvio padrão com $n-1$: `statistics.variance`, `standard_deviation`), usar `ddof=1`. Onde o texto afirma um número (`assert 22.9 < alpha < 23.0`), o número tem que continuar valendo — e se não valer, é o texto que se recalcula a partir da saída real, nunca o `assert` que se afrouxa sem explicação.

### Aleatoriedade

Todo chunk estocástico cria um gerador **explícito e semeado**:

```python
rng = np.random.default_rng(42)
```

Funções estocásticas de `scratch_np/` recebem `rng: np.random.Generator` como parâmetro **obrigatório** (sem valor padrão): a semente é decisão de quem chama, visível no chunk, como o capítulo 9 exige hoje. Nunca `np.random.seed(...)` (estado global) nem `random` da stdlib. Uma linha de prosa justifica a semente onde ela aparece pela primeira vez na seção, no formato do callout "A semente não é opcional" do capítulo 9.

**Os sorteios mudam.** `random.seed(12)` + `split_data` do Grus e `default_rng(12)` + `rng.permutation` produzem divisões diferentes. Toda afirmação do texto que dependia de um sorteio específico (a matriz de confusão do Iris, a acurácia do filtro de spam, o `beta` do bootstrap) é **recalculada a partir da saída nova**. É a principal fonte de trabalho de revisão desta reescrita.

## Onde o numpy é apresentado ao leitor

O leitor chega ao capítulo 6 tendo visto numpy uma única vez: no callout de fechamento do capítulo 4, que mostra `np.array`, `np.dot`, `np.linalg.norm` como "o que a biblioteca faria melhor". Falta a apresentação de verdade.

- **Capítulo 7, seção 7.1 (`01-explorando-seus-dados.qmd`) abre com um bloco `## De listas a arrays`.** É a única casa possível sem mexer na estrutura: é a primeira seção em que os dados são numéricos e multidimensionais, e é onde `bucketize`/histograma (1D), colunas (2D) e matriz de correlação (n-D) pedem arrays. O bloco cobre, nesta ordem: o que é um `ndarray` e por que ele existe (o `dot` do capítulo 4 lado a lado com `@`); `shape` e `dtype`; indexação e fatias, inclusive `X[:, j]`; máscaras booleanas; broadcasting com escalar e com vetor; `axis` nas reduções; e o custo — o laço em Python que some. Tamanho-alvo: 80 a 120 linhas de `.qmd`, com chunks curtos que mostram a saída. Fecha remetendo ao callout do capítulo 4.
- **Capítulo 6 faz o primeiro contato, e só.** A seção "Lendo Arquivos" mostra `np.loadtxt`/`np.genfromtxt` para colunas numéricas, com `shape` e uma operação vetorizada, e remete explicitamente à seção 7.1 para a apresentação completa. Raspagem, JSON e APIs continuam sendo o que são — não há modelo no capítulo 6, e forçar numpy onde não há número seria decoração.

## O que muda em cada seção

O planejador de cada capítulo decide os detalhes; estas são as exigências comuns.

**Código.** Chunks reescritos em numpy segundo a regra da calculadora. Chunks de figura recebem arrays direto (`plt.scatter(X[:, 0], X[:, 1])`). Chunks `eval: false` (código de download, raspagem viva) ficam como estão. Nenhum chunk executável importa `scratch.` (o pacote em Python puro) — só `scratch_np.` e `numpy`. Nenhum chunk executável importa `sklearn` (isso já é verdade hoje; vira teste).

**Prosa.** Toda frase que descrevia o código antigo e não descreve o novo sai ou muda: *"São um milhão de distâncias euclidianas calculadas em Python puro"*, *"trinta linhas contra sete"*, *"a lentidão é o preço da transparência"*, *"`dot` é um `sum` sobre um `zip`"*. Os números do texto (acurácias, coeficientes, contagens, tempos) são reconferidos contra a saída real. O que **não** muda: aberturas de seção, callouts de correspondência (`Esta seção corresponde a *The Model*, do capítulo 12 de @grus2019.`), posição e forma dos callouts `.conceito`/`.exemplo`, o tom, os nomes de função em inglês do Grus, os objetivos do `index.qmd` (ajustados só onde dizem "Python puro").

**O callout de fechamento em `scikit-learn` fica.** É o fecho do arco "abrir a caixa-preta" e é o único lugar onde a biblioteca aparece — sempre num bloco ```` ```python ```` que não executa. A instrução do autor ("não use scikit-learn") vale para a **implementação**; o callout compara, não implementa. O texto do callout é atualizado: a comparação agora é entre a nossa versão em numpy e a da biblioteca, e frases como "força bruta em Python puro já é instantânea" trocam de sentido. *Esta leitura é uma decisão do orquestrador e está sinalizada no relatório final; se o autor quiser os callouts fora, é uma remoção mecânica.*

**Invariantes que continuam:** citação em toda seção; nenhum número de seção do Grus inventado; caminhos de dados a partir da raiz; todo chunk começa em coluna zero (bloco não se parte entre células); a única **subida** de gradiente do livro é a da PCA no capítulo 7 (`tests/test_gradiente.py` — se um capítulo passar a subir, ele registra o motivo); notebooks regenerados após qualquer edição de `.qmd`.

## Contratos entre capítulos

Estas assinaturas são fixadas aqui porque um capítulo importa do outro, e os capítulos são escritos em paralelo. Quem implementa o módulo pode acrescentar funções; **não pode** mudar estas.

```python
# scratch_np/gradient_descent.py  (andaime)
def gradient_step(v: np.ndarray, gradient: np.ndarray, step_size: float) -> np.ndarray:
    """v + step_size * gradient. Passo negativo = descida — a mesma convenção do cap. 5."""
def minibatches(n: int, batch_size: int, rng: np.random.Generator, shuffle: bool = True) -> Iterator[np.ndarray]:
    """Gera arrays de índices; quem chama faz X[idx], y[idx]."""

# scratch_np/machine_learning.py  (andaime; cap. 8 ensina o mesmo código)
def split_data(data, prob: float, rng: np.random.Generator):
    """Embaralha e corta em int(len(data) * prob). Array -> dois arrays; sequência -> duas listas."""
def train_test_split(xs: np.ndarray, ys: np.ndarray, test_pct: float, rng: np.random.Generator):
    """-> (x_train, x_test, y_train, y_test), fatiados pelos mesmos índices."""
def accuracy(tp: int, fp: int, fn: int, tn: int) -> float
def precision(tp: int, fp: int, fn: int, tn: int) -> float
def recall(tp: int, fp: int, fn: int, tn: int) -> float
def f1_score(tp: int, fp: int, fn: int, tn: int) -> float

# scratch_np/probability.py  (andaime)
def normal_cdf(x, mu: float = 0, sigma: float = 1) -> np.ndarray | float
def inverse_normal_cdf(p, mu: float = 0, sigma: float = 1, tolerance: float = 1e-5) -> np.ndarray | float

# scratch_np/statistics.py  (andaime)
num_friends, daily_minutes, num_friends_good, daily_minutes_good: np.ndarray  # float, forma (n,)

# scratch_np/simple_linear_regression.py  (cap. 11; o cap. 12 importa)
def total_sum_of_squares(y: np.ndarray) -> float
def least_squares_fit(x: np.ndarray, y: np.ndarray) -> tuple[float, float]   # (alpha, beta)
def predict(alpha: float, beta: float, x) -> np.ndarray | float

# scratch_np/multiple_regression.py  (cap. 12; o cap. 13 importa)
inputs: np.ndarray            # (200, 3): coluna constante 1, amigos, horas de trabalho
def predict(x: np.ndarray, beta: np.ndarray)          # x (d,) ou X (n, d) -> escalar ou (n,)
def least_squares_fit(xs: np.ndarray, ys: np.ndarray, rng: np.random.Generator,
                      learning_rate: float = 0.001, num_steps: int = 1000,
                      batch_size: int = 1) -> np.ndarray   # beta (d,)

# scratch_np/neural_networks.py  (cap. 15; o cap. 16 importa)
def sigmoid(t) -> np.ndarray | float
def binary_encode(x: int) -> np.ndarray       # (10,) bits, do menos significativo
def fizz_buzz_encode(x: int) -> np.ndarray    # (4,) one-hot: [x, fizz, buzz, fizzbuzz]
```

Ordem de implementação: **sequencial, na ordem do livro (6, 7, 8, …, 17)**, um capítulo por vez — planejador, implementador e revisor de cada capítulo terminam antes de o próximo começar, para que cada capítulo aproveite as convenções e o código já entregues pelos anteriores (decisão do autor, 2026-09-07; a ordem do livro satisfaz todas as dependências acima). Os módulos do andaime existem antes do capítulo 6.

## Verificação sem render

O `make render` é serializado e leva minutos; doze agentes disputando o lock não funciona, e edição concorrente durante um render envenena o `_freeze/` (CLAUDE.md). Por isso **implementadores e revisores não renderizam**. Eles verificam com três comandos, todos no venv do host (`.venv/`, que já tem numpy, matplotlib, jupyter, scikit-learn e pytest; Docker é opcional):

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0          # os mesmos do Dockerfile
.venv/bin/python scripts/gerar-notebooks.py      # regenera os 17 notebooks (idempotente)
.venv/bin/python scripts/executar-secoes.py 11   # cada .qmd do cap. 11 num kernel PRÓPRIO (como o site)
.venv/bin/python scripts/executar-notebooks.py cap11   # o capítulo inteiro num kernel só (como a aula)
.venv/bin/pytest tests/ -q                       # invariantes
```

`executar-secoes.py` é novo: reaproveita o parser de `gerar-notebooks.py`, monta um notebook só de código para **cada** `.qmd` do capítulo e o executa num kernel novo com o cwd na raiz. É o análogo fiel do `quarto render` daquele arquivo — pega o `import` que falta numa seção porque foi feito na anterior, que o notebook de aula (um kernel só) deixa passar. Não toca em `_freeze/` nem em `.quarto/`, então pode rodar em paralelo.

O render completo (`make render`, depois `make offline`) é feito **uma vez, pelo orquestrador**, no fim de cada onda e no fim de tudo.

## Testes novos (`tests/test_scratch_np.py`)

- Todo módulo de `scratch_np/` importa numpy e nenhum importa `sklearn`; todos importam sem rede e sem erro (subprocesso, mesmo padrão de `test_modulos_importaveis_sem_rede`).
- Nos capítulos listados em `CAPITULOS_NUMPY` (o conjunto cresce a cada capítulo entregue; no fim é `range(6, 18)`): nenhum chunk executável importa `scratch.` (só `scratch_np.`); nenhum usa `np.random.seed` nem `random.` da stdlib (exceções com motivo, no padrão de `NAO_IMPORTAVEIS`); a expressão "Python puro" só aparece em frases registradas com motivo (o teste é o detector de sobra de prosa antiga, o revisor é quem julga).
- Em **todo** o livro: nenhum chunk executável contém `sklearn` (já é verdade hoje; passa a ser garantido).

## Processo

Um agente **planejador** (Fable 5.1) por capítulo lê esta spec, o `CLAUDE.md`, o capítulo 9 (estilo) e o seu capítulo inteiro, e escreve `docs/superpowers/plans/2026-09-06-numpy-capNN.md` com: inventário do que existe (chunks, imports, números afirmados, figuras, frases que descrevem Python puro); o desenho numpy do módulo do capítulo (código **completo** do módulo, já dentro dos contratos acima); o plano seção a seção (chunk a chunk: código novo por inteiro; lista das frases a mudar e por quê; números a recalcular; semente); riscos. Um agente **implementador** por capítulo executa o plano e verifica com os três comandos. Um agente **revisor** por capítulo lê o resultado com a pergunta única do autor — *o texto condiz com o que foi reescrito?* — e devolve uma lista de discrepâncias, que o implementador corrige. Depois das três ondas, um passe de **coerência global** ajusta o que fala do livro inteiro: `index.qmd` da raiz, `content/cap01`, `content/cap04/index.qmd` ("este livro não usa numpy em lugar nenhum"), `README.md`, `CLAUDE.md`, e a spec original ganha uma nota de correção apontando para esta.

## Decisões registradas

| Decisão | Escolha | Por quê |
|---|---|---|
| Escopo da reescrita | Caps. 6–17; 1–5 intactos | Pedido do autor; os caps. 1–5 são a motivação do numpy |
| Onde vive o código numpy | Pacote novo `scratch_np/`, espelhando o `scratch/` | Cada `.qmd` é um kernel; "a seção implementa, a próxima importa" precisa de um módulo |
| Nomes de função | Os do Grus, em inglês | Correspondência com o livro-texto continua evidente |
| `linear_algebra` em numpy | Não existe | É o próprio numpy |
| Dados hard-coded do Grus | Reexportados como arrays por `scratch_np/` | Única importação permitida de `scratch.` fora dos caps. 1–5 |
| RNG | `np.random.default_rng(semente)` explícito, passado como parâmetro | Semente visível no chunk, sem estado global |
| Callout `scikit-learn` | Fica, com texto atualizado | "Não use scikit-learn" lê-se como "não implemente com"; o callout compara |
| Apresentação do numpy | `## De listas a arrays` abrindo a 7.1; primeiro contato na 6.1 | Sem mudar a estrutura de 87 seções; é a primeira seção com dado numérico n-dimensional |
| Verificação dos agentes | Execução por seção e por capítulo no host; render só pelo orquestrador | Render é serializado e envenena o cache sob edição concorrente |
| Testes de invariante | Conjunto `CAPITULOS_NUMPY` que cresce por capítulo | `make teste` verde em todo commit da branch |
