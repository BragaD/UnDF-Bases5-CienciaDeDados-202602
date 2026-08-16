# Cap 10 — Naive Bayes — relatório de escrita

## Arquivos escritos (6, todos já registrados no `_quarto.yml`, nenhum renomeado)

- `content/cap10/index.qmd`
- `content/cap10/01-um-filtro-de-spam-bem-burro.qmd`
- `content/cap10/02-um-filtro-mais-sofisticado.qmd`
- `content/cap10/03-implementacao.qmd`
- `content/cap10/04-testando-o-modelo.qmd`
- `content/cap10/05-usando-o-modelo.qmd`

## Fontes lidas

- `docs/guia-para-escrever-um-capitulo.md`, `CLAUDE.md`
- `content/cap09/*` (modelo de estilo), `content/cap08/04-correcao.qmd` (métricas)
- `content/cap08/06-extracao-e-selecao-de-atributos.qmd` (promessa "sim-ou-não" a cumprir)
- PDF do Grus, capítulo 13, páginas 169–178 do livro (189–198 do PDF) — texto integral
- `scratch/naive_bayes.py` inteiro
- `dados/spam-assuntos.csv` (3.300 linhas: 2.800 ham, 500 spam) — confirmado por script

## Estrutura por seção

1. **01** — teorema de Bayes com uma palavra só (`bitcoin`), exemplo numérico 98%.
2. **02** — suposição de independência, exemplo bitcoin/rolex, *underflow* e o truque log-sum-exp com demonstração numérica real (produto direto de 300 termos de 0,01/0,012 colapsa para `(0.0, 0.0)`, indistinguível; soma de logs preserva `-1381.55` vs `-1326.85`), suavização por pseudocontador, ligação ao "sim-ou-não" do Cap. 8.
3. **03** — `tokenize`, `Message`, `NaiveBayesClassifier` (init+train+_probabilities+predict) **numa única célula de código** (ver correção abaixo). Callout "Na prática" com `BernoulliNB`.
4. **04** — importa `scratch.naive_bayes`, reproduz o teste de brinquedo do livro (3 mensagens), reproduz a predição manual (`≈0,835`) e o `assert` de igualdade exata de float — com callout-warning explicando a armadilha (ordem de iteração de `set` + `PYTHONHASHSEED`), amarrado ao `shuffle` do Cap. 5 e ao `assert` sem semente do Cap. 7.
5. **05** — código de download/varredura do SpamAssassin com `eval: false` + callout (padrão do Iris no Cap. 9); carga do CSV vendorizado; callout sobre desequilíbrio 2.800/500 amarrado à piada da leucemia do Cap. 8; `random.seed(0)` + `split_data`; treino; matriz de confusão real; precisão/revocação importadas de `scratch.machine_learning` (não redefinidas); palavras mais spammy/hammy; contraste k-vizinhos (preguiçoso) vs Naive Bayes (treina de verdade); callout "Na prática".

## Bug encontrado e corrigido durante a escrita (fora do escopo original, mas crítico)

Na primeira versão de `03-implementacao.qmd`, o corpo da classe `NaiveBayesClassifier` estava dividido em **quatro células** (`__init__`, depois `train`, `_probabilities`, `predict` cada uma começando com `def` indentado, sem reabrir `class ...:`). O `quarto render` **não acusa erro nisso** — testei diretamente com `IPython.testing.globalipapp.get_ipython()` e confirmei que o IPython aceita a célula indentada sem lançar exceção, mas **silenciosamente não anexa o método à classe** (`AttributeError` só apareceria se alguém chamasse `model.train(...)` depois). Como a seção 03 nunca instanciava a classe, o render passava "limpo" com uma classe quebrada. Corrigido consolidando toda a classe numa única célula (`#| label: naive-bayes-classifier`), no padrão já usado em `content/cap07/03-dataclasses.qmd`. Confirmei por dois caminhos: (1) `grep`/`awk` em `content/cap01` a `cap09` mostrando que nenhum capítulo escrito quebra uma classe/função entre células; (2) execução célula-a-célula via IPython real dentro do container, treinando e prevendo com sucesso após a correção.

## Verificação

- `make render`: **1ª rodada** abortou por `Directory not empty` (corrida do bind mount, não relacionada ao conteúdo) — autocorrigiu na tentativa 2, `render OK (tentativa 2)`. Após o fix do bug acima, rerodei: `render OK (tentativa 1)`.
- `make teste`: 20/20 PASSED, nas duas rodadas.
- Nenhuma figura gerada neste capítulo (confirmado: `_book/content/cap10/` só tem os 6 `.html`, sem diretórios `*_files`).
- Números conferidos na íntegra contra `_book/content/cap10/*.html` (extração de texto do HTML renderizado, não da minha memória):
  - §01: `p_spam_dado_bitcoin = 0.9803921568627451` (≈98%).
  - §02: `produto_direto = (0.0, 0.0)`; `soma_de_logs = (-1381.5510557964274, -1326.854588758241)`.
  - §04: `model.predict(text) = 0.8350515463917525` (≈0,835), `assert` de igualdade exata passa (ambiente com `PYTHONHASHSEED=0`).
  - §05: divisão `random.seed(0)` → 2.475 treino / 825 teste; baseline "sempre ham" = 699/825 = 0,8472727... (84,7%); matriz de confusão `{(False, False): 675, (True, True): 80, (True, False): 46, (False, True): 24}`; `accuracy=0.9151515151515152`, `precision=0.7692307692307693`, `recall=0.6349206349206349`; spammiest = `['assistance', 'mortgage', 'clearance', 'per', 'sale', 'systemworks', 'only', 'money', 'rates', 'adv']`; hammiest = `['spambayes', 'users', 'razor', 'zzzzteana', 'sadev', 'ouch', 'apt', 'bliss', 'selling', 'perl']` — todos batem exatamente com o texto.
- Comparação com os números do próprio Grus (84 TP/25 FP/703 TN/44 FN, precisão 77%, revocação 65%) citada no texto como "muito perto" — é verdade e não coincidência (mesmo corpus, só vendorizado antes em vez de durante o render).

## Preocupações / decisões que valem revisão humana

- O bug de classe partida entre células (corrigido) é um risco genérico deste projeto: `quarto render` não detecta indentação órfã porque IPython a tolera silenciosamente. Vale considerar um teste estrutural (`grep` por chunk começando com `def`/`return`/etc. indentado) em `tests/test_estrutura.py`, mas não adicionei teste novo porque não foi pedido e não quis expandir escopo.
- A seção 02 usa um exemplo sintético (300 termos de 0,01/0,012) para demonstrar o *underflow*, deixado explícito no texto como "não são números do classificador real" — o classificador de verdade (seção 05, ~3.762 tokens) não chega a sofrer *underflow* de fato (verificado: produto direto ainda representável, ~1e-16); isso está declarado no texto para não sugerir algo que a saída real não mostra.

## Rodada 2 — correções de `.superpowers/livro/cap10-correcoes.md`

Duas revisões independentes voltaram: conteúdo (0 Crítico, 1 Importante — a omissão da lista de melhorias do Grus e do `drop_final_s` órfão) e didática (2 Críticos, 12 Importantes, ~12 Menores). **Implementei os 2 Críticos, os 13 Importantes e todos os Menores — nenhum item recusado.**

O teste que eu mesmo tinha sugerido como "preocupação" na rodada 1 (guarda contra chunk começando indentado) já existia quando comecei esta rodada — outro agente o adicionou (`test_nenhum_chunk_comeca_com_linha_indentada`, em `tests/test_estrutura.py`). Confirmei que a suíte agora tem 21 testes, não mais 20.

**Críticos:**
- **C1** (Bayes despejado, não construído) — reescrevi a §1 inteira: agora abre com a conta de contagem (1.000 mensagens, 500 spam/250 com *bitcoin*, 500 ham/5 com *bitcoin* → 250/255 ≈ 98%) **antes** da fórmula, e a fórmula geral de Bayes chega depois, explicitamente como "a mesma conta em símbolos". $\lnot S$ ganha glosa.
- **C2** (a métrica errada defende o argumento do Cap. 8) — reescrevi o `.conceito` da §5: agora computa e mostra ao vivo que o piso "sempre ham" tem revocação **0,0** (verificado: `recall(0,0,126,699)==0.0`) e precisão **indefinida** (`ZeroDivisionError` real, capturado e impresso — não simulado em prosa), e só então usa os "sete pontos de acurácia" como isca antes de virar a mesa.

**Importantes (13/13):**
- I1 (prior 50/50 embutido, corpus 15% spam) — parágrafo novo na §5, logo após a matriz de confusão, ligando aos 24 falsos positivos e ao `fit_prior=True` do `BernoulliNB`.
- I2 (`predict` devolve probabilidade; 0,5 é escolha) — parágrafo novo na §5, ligando ao `.exemplo` do Cap. 8 sobre custo de falso positivo em spam e ao contraste com `majority_vote` do Cap. 9.
- I3 (contraste Cap. 9 incompleto e impreciso) — reescrito por inteiro: corrigi "k-vizinhos não tem parâmetro nenhum" (cita a escolha de *k*=5 e a frase do Cap. 9 sobre conjunto de validação), desarmei a colisão de nome entre os dois "*k*", e acrescentei o parágrafo que faltava — Naive Bayes não sofre a maldição da dimensionalidade da seção 9.3 porque a suposição de independência troca geometria por contagem.
- I4 (F1 ausente) — `f1_score` importado e computado: 0,696 para o modelo, indefinido para o piso (mesma razão da precisão).
- I5 (lista de melhorias do Grus omitida; `drop_final_s` órfão) — nova subseção "Como este modelo poderia melhorar" na §5: mais dados, `min_count`, stemmer (com `drop_final_s` mostrado e explicado), atributos fantasmas.
- I6 (só `BernoulliNB` nos dois "Na prática") — acrescentei `MultinomialNB`, `fit_prior` e `binarize` nos dois callouts (§3 e §5), amarrados ao papel do `set` em `tokenize`.
- I7 (ausência como susto, não promessa) — nova frase na §2 logo após a equação de independência, explicando o fator quando $x_i=0$; o `.conceito` da §3 agora diz "cumprindo a promessa da seção anterior" em vez de só "repare".
- I8 (underflow vago) — §2 agora cita $10^{-308}$ (menor `float` normal) e $10^{-600}$ (o que 300 fatores de 0,01 pediriam), deixando claro que é alcance de expoente, não precisão.
- I9 (callout do `float` sem prescrição) — acrescentei a linha `math.isclose(...)` no fim do callout-warning da §4, com a nota de que está na stdlib desde o Python 3.5.
- I10 ("ham" usado antes de definido) — definido na abertura da §1, com a etimologia Monty-Python em meia frase.
- I11 ("vendorizar" não glosado) — heading "Carregando o CSV vendorizado" → "Carregando os dados"; texto trocado por fraseado no estilo do Cap. 9 ("já traz commitado", "o CSV que carregamos").
- I12 (abertura só fecha dívida, fechamento não abre nada) — parágrafo novo no `index.qmd` (primeiro modelo probabilístico; treinar = comprimir em parâmetros) e parágrafo de fechamento na §5 ligando "contagens resumidas" a "coeficientes ajustados" da regressão.
- I13 (classe inteira numa parede de código) — `predict` separado em chunk próprio via **monkey-patch** (`def predict(self, ...)` de nível zero + `NaiveBayesClassifier.predict = predict`), com callout explicando a técnica e por que não é assim que `scratch/naive_bayes.py` faz. Testado via IPython real (train+predict funcionam) e via `pytest -k indentada` (passa).

**Menores:** todos os de prosa (bastidores, laço, "não te diz", "mais uma evidência", motores→termos) e de conteúdo (link+glosa de *prior*, nome "suavização de Laplace", nota sobre os três valores de *k*, `Counter` só usado na §5, frase duplicada removida do `index.qmd`, precisão do `shuffle` do Cap. 5, narrativa do VP restaurada no `index.qmd`) foram aplicados. O tique "de verdade" (11 ocorrências após os parágrafos novos de C2/I1/I2) foi variado para zero na §5 — pode ter ficado mais enxuto do que o pedido original de "variar", mas nenhuma leitura ficou estranha.

**Verificação desta rodada (sem `make render`, por instrução — outro agente renderiza depois):**
- `make teste`: 21/21 PASSED.
- Toda célula de código nova ou alterada foi executada num kernel IPython real dentro do container (`IPython.testing.globalipapp.get_ipython()`), na ordem do arquivo, simulando exatamente o que o Quarto faz — sem tocar `_book/` nem `_freeze/`. Confirmei ao vivo: `baseline_recall=0.0`; `precision(0,0,126,699)` realmente lança `ZeroDivisionError` (capturado); `f1_score(80,24,46,675)=0.6956521739130435`; `model.spam_messages=374`, `model.ham_messages=2101` (números citados em prosa no I1); a classe com `predict` monkey-patchado treina e prevê corretamente.
- `grep` de confirmação: nenhuma ocorrência residual das frases que deveriam ter sido trocadas (verificado explicitamente).

Nenhum item da revisão foi recusado.
