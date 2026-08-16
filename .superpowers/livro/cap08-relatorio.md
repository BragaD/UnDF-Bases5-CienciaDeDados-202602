# Capítulo 8 — callouts "Na prática"

## O que foi escrito

Quatro callouts `.callout-tip collapse="true"`, todos no fim da seção (no caso da 8.6,
antes do callout de fechamento do capítulo, que continua sendo o último bloco).

| Seção | Título do callout | Fecha o quê |
|---|---|---|
| 8.3 Overfitting e Underfitting | `Na prática: scikit-learn` | `train_test_split`, `KFold`, `cross_val_score`, `GridSearchCV` |
| 8.4 Correção | `Na prática: scikit-learn` | `precision_score`, `recall_score`, `f1_score`, `confusion_matrix`, `classification_report` |
| 8.5 O Compromisso Viés-Variância | `Na prática: learning_curve e validation_curve` | as duas figuras da seção, e o que a biblioteca **não** oferece |
| 8.6 Extração e Seleção de Atributos | `Na prática: sklearn.feature_selection` | `SelectKBest`, `SelectFromModel`, `RFE`, `Pipeline` |

A lacuna que motivou o trabalho está fechada: `train_test_split` agora é nomeado em 8.3,
o capítulo que existe para explicá-lo, e não mais só em `cap09/02` — que passou a ser a
segunda aparição, não a primeira.

## Afirmações conferidas rodando (sklearn 1.9.0, dentro do container)

Nenhuma afirmação sobre biblioteca neste capítulo foi escrita sem execução. Cada número
que aparece em comentário de código foi copiado da saída, não da memória.

**8.3**

- Assinatura `train_test_split(*arrays, test_size=None, train_size=None, random_state=None, shuffle=True, stratify=None)`; sem `test_size`, o padrão é 25% (`75/25` sobre 100 pontos).
- `random.seed(42)` da stdlib **não** controla `train_test_split`: duas chamadas seguidas com a mesma semente devolveram `[14, 0, 11, 6, 12]` e `[2, 7, 8, 4, 6]`. Com `random_state=42`, iguais.
- `KFold(n_splits=5)` tem `shuffle=False`. Sobre o `dados/iris.data` real (lido do disco, ordenado por classe): `cv=KFold(3)` → `[0. 0. 0.]`; `cv=3` → `[0.98 0.96 0.98]`.
- `check_cv(None, y, classifier=True)` → `StratifiedKFold(n_splits=5)`; `classifier=False` → `KFold(n_splits=5)`. Confirma a inconsistência: `cross_val_score` estratifica, `train_test_split` não.
- Classe rara (8 positivos em 200, `test_size=0.25`), varredura de 200 sementes: distribuição dos positivos no teste `{0: 18, 1: 50, 2: 65, 3: 44, 4: 19, 5: 3, 6: 1}`. Com `stratify=y`, sempre exatamente 2.
- `stratify` com `shuffle=False` → `ValueError: Stratified train/test split is not implemented for shuffle=False`.
- `GridSearchCV`: `refit=True` é o padrão; `best_score_` (0.98) é o **máximo** de `cv_results_['mean_test_score']` (`[0.96 0.9667 0.9733 0.98 0.9733]`); e `best_estimator_.n_samples_fit_` = 150 = `len(X)`, ou seja o refit **reajusta o vencedor sobre todos os dados**, inclusive os que serviram de validação.
  - *Correção durante a escrita:* a primeira versão do parágrafo dizia que "o modelo vencedor nunca viu os dados que o elegeram". Está errado por causa do `refit=True`, e a checagem acima é o que pegou. O texto foi reescrito para separar as duas coisas — a nota de cada candidato é honesta; `best_score_` (máximo) e `best_estimator_` (refit) não são.

**8.4**

- Reconstruí o milhão de pessoas do teste do Luke e comparei com as funções do livro: `accuracy_score` 0.98114, `precision_score` 0.014, `recall_score` 0.005, `f1_score` 0.007368421052631579 — idênticos.
- `confusion_matrix` → `[[981070 4930] [13930 70]]`, ou seja **real nas linhas, previsto nas colunas** — a transposta da tabela da seção. `.ravel()` → `[981070 4930 13930 70]` = `tn, fp, fn, tp`, o inverso da ordem de `precision(tp, fp, fn, tn)`.
- `pos_label=1`, `average='binary'` por padrão. Com rótulos de texto: `ValueError: pos_label=1 is not a valid label. It should be one of ['ham' 'spam']` (mensagem transcrita literal). Com rótulos 0/1, mede a classe 1 em silêncio.
- `zero_division='warn'` (padrão) devolve `0.0` e emite `UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 due to no predicted samples. Use 'zero_division' parameter to control this behavior.` Testados também `0`, `1` e `np.nan` (este desde a 1.3, conforme docstring). Nenhum `DeprecationWarning` com `-W error::DeprecationWarning`.
- `recall_score` sem positivos reais: mensagem análoga, `due to no true samples`.
- Saída de `classification_report` inspecionada (colunas precision/recall/f1-score/support, linhas macro avg e weighted avg).

**8.5**

- `learning_curve(DecisionTreeClassifier(random_state=0), X, y, shuffle=True, random_state=0)` sobre o Iris → `tamanhos [12 39 66 93 120]`, treino `[1. 1. 1. 1. 1.]`, teste `[0.787 0.933 0.953 0.94 0.96]`.
- Mesma chamada com o padrão `shuffle=False` → teste `[0.333 0.333 0.667 0.947 0.96]`. Os dois primeiros pontos são artefato da ordenação por classe do arquivo.
- `validation_curve(..., param_name='max_depth', param_range=[1,2,3,5,10])` → treino `[0.667 0.962 0.973 0.998 1.]`, teste `[0.667 0.933 0.96 0.96 0.96]`.
- Formato do retorno `(n_pontos, n_dobras)` = `(5, 5)` confirmado.
- **Não existe decomposição viés-variância no `scikit-learn`.** Varri o pacote inteiro com `pkgutil.walk_packages` procurando `bias` (zero módulos) e listei `sklearn.metrics` (só `explained_variance_score`, que é métrica de regressão, não decomposição). A afirmação do callout é essa, e ela é verificada, não presumida.
- **Cuidado registrado:** sem `random_state=0` no estimador, os números mudam (`teste [0.833 0.953 ...]`). O snippet do callout mostra `DecisionTreeClassifier(random_state=0)` justamente porque é o código que produziu os números impressos.

**8.6**

- XOR de três colunas (`a`, `b` binárias, `ruido` uniforme, `y = a ^ b`), com o código exato que o callout exibe, em `random` da stdlib: `f_classif` → `scores_ [0.170, 0.259, 0.258]`; `SelectKBest(k=2).get_support()` → `[False, True, True]` — **descarta uma coluna informativa e mantém o ruído**. `SelectFromModel(RandomForestClassifier(random_state=0), max_features=2)` → importâncias `[0.524, 0.415, 0.061]`, `get_support()` `[True, True, False]`.
- `SelectKBest` padrão `k=10`; com 3 colunas emite `UserWarning: k=10 is greater than n_features=3. All the features will be returned.` (transcrito literal) e devolve tudo.
- `SelectFromModel` sem `threshold` corta pela média das importâncias: `threshold_ = 0.3333...`, que é a média de `[0.524, 0.415, 0.061]`.
- `chi2` com entrada negativa → `ValueError: Input X must be non-negative.`
- Vazamento por seleção fora da validação, com o código exato do callout (100 linhas × 2.000 colunas de ruído gaussiano, `y = [0,1]*50`, sem sinal nenhum): seleção antes da divisão → `cross_val_score(...).mean() = 0.81`; a mesma seleção dentro de um `Pipeline` → `0.45`.

## O que ficou de fora, e por quê

- **8.1 (Modelagem)** e **8.2 (O que é Machine Learning?)** não ganharam callout. Não têm análogo de biblioteca: a 8.1 define o que é um modelo (planilha, receita, pôquer) e a 8.2 distingue supervisionado de não supervisionado e apresenta a ideia de família parametrizada. Um "Na prática" ali seria propaganda de ferramenta pendurada em prosa conceitual — exatamente o que o guia proíbe. O callout `.callout-important` que a 8.2 já tem ("A escolha da família é sua, e ela não é neutra") faz o trabalho que importa naquela seção.
- **8.5 não virou "Na prática: o que se faz com isso".** O briefing deixava essa saída aberta caso o `learning_curve` ficasse forçado. Ele não fica: as duas figuras da seção são literalmente `learning_curve` (varia N com o modelo fixo) e `validation_curve` (varia a complexidade com N fixo), e a ausência de decomposição viés-variância no pacote dá ao callout o "o que a biblioteca esconde" mais honesto dos quatro — ela não esconde a conta, ela não tem a conta.
- **Limiar de decisão, `predict_proba`, `precision_recall_curve` e `roc_curve`** ficaram fora do 8.4 de propósito: `content/cap13/04-qualidade-do-ajuste.qmd` já os cobre bem, e com dados reais. O 8.4 fica com o que é dele — orientação da matriz, escolha da classe positiva e divisão por zero —, e o `classification_report` aparece só como ponteiro.
- **`sklearn.feature_extraction`** foi mencionado apenas por negação no 8.6 ("nada disso faz extração"). O `CountVectorizer` é o análogo real da extração de atributos de texto, e `content/cap10/05-usando-o-modelo.qmd` já o apresenta com o corpus de spam. Repetir aqui, sem dados, seria pior.

## Verificação

- `make refresh CAP=08` → **`render OK (tentativa 1)`**. Foi preciso o `refresh` em vez do `render` simples porque a suíte acusou `_freeze` envenenado em `content/cap08/04-correcao.qmd` (hash batendo com um fonte de outra versão — provavelmente um render concorrente de outro agente pegou o arquivo no meio da edição). O alvo `refresh` apaga só `_freeze/content/cap08` e renderiza; `make clean` **não** foi usado.
- `make render` → **`render OK (tentativa 1)`**, uma segunda vez, para incorporar as revisões de prosa feitas enquanto o primeiro render rodava.
- `make teste` → **24 passed**, incluindo `test_freeze_corresponde_ao_fonte`, `test_nenhuma_secao_inventa_numero_de_secao_do_grus` e `test_nenhum_qmd_usa_caminho_relativo_de_dados`.
- Callouts confirmados no cache de `_freeze` (que é o que a publicação consome), com hash batendo com o fonte, em 8.3, 8.4 e 8.5. A 8.6 não tem entrada de `_freeze` porque não tem nenhum chunk executável — correto.
- Nenhum chunk dos quatro callouts é executável: todos usam ```` ```python ````, verificado por varredura automática dos blocos dentro de `.callout-tip`.
- Nenhuma figura nova foi gerada (os callouts são prosa e código não executado), então não há figura a conferir contra o texto.

> Nota sobre `_book/`: no fim desta sessão o diretório aparecia vazio porque o render de **outro** agente havia acabado de começar e o Quarto limpa o destino ao iniciar. Não é sintoma de falha — os dois renders desta tarefa imprimiram `Output created: _book/index.html`.
