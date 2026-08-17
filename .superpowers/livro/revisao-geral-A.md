# Revisão geral do livro — lote A: capítulos 16 e 17

Quatro frentes varreram o livro completo. Este lote traz o que cai nos capítulos **16 e 17**,
e **dois dos itens são afirmações sobre biblioteca que eu executei e confirmei erradas**.

Lembre por que isso importa: os callouts "Na prática" são a **única parte do livro que nenhuma
renderização verifica**, porque os chunks deles são ```` ```python ```` que não executam. Das
afirmações erradas encontradas na sessão inteira, a maioria estava exatamente aí.

---

## Importantes

### A1 — O `KMeans` **não** roda dez vezes por padrão. Medido.

`content/cap17/02-o-modelo.qmd:180` e `content/cap17/03-exemplo-encontros.qmd:172` afirmam que
"por padrão, o `scikit-learn` roda o algoritmo inteiro dez vezes".

**Executado no container (scikit-learn 1.9.0):**

| `init` | `n_init` efetivo |
|---|---|
| `'k-means++'` (o **padrão**) | **1** |
| `'random'` | 10 |

O parâmetro vale `'auto'` desde a 1.4, e `'auto'` significa **1** com `k-means++`. O erro é
grave porque `n_init` é justamente **o primeiro dos dois mecanismos que o callout diz que a
biblioteca esconde** — e o argumento "ela devolve o melhor de dez" desaparece.

Conserte nos dois lugares. O de `03` repete a afirmação por conta própria, apesar de remeter ao
`02`; ou corrige os dois, ou o `03` passa a só apontar.

**Note que `content/cap17/05-exemplo-clustering-de-cores.qmd` passa `n_init=10` explícito e está
correto** — não mexa nele.

### A2 — `max_features='sqrt'` sobre 8 atributos dá **2**, não 3. Medido.

`content/cap14/06-florestas-aleatorias.qmd:403`. Executado:
`RandomForestClassifier(max_features='sqrt').fit(X_8col).estimators_[0].max_features_` → **2**,
porque a fórmula é `max(1, int(sqrt(p)))` e `int(2,828) = 2`.

Isso derruba também a frase seguinte: o padrão da biblioteca **não** coincide com a proporção que
saiu melhor na medição do capítulo. Ele bate com a linha `floresta (2 de 8)` — 91,7% —, não com
a melhor, `3 de 8` a 92,8%.

**Este item é do capítulo 14**, mas vai neste lote porque é medição de biblioteca, da mesma
família. É a única coisa do capítulo 14 que você deve tocar.

### A3 — O capítulo 16 corrige o erro do PyTorch na §5 e o comete na §8

`content/cap16/08-exemplo-mnist.qmd:474` oferece
`torch.optim.SGD(..., lr=0.01, momentum=0.99)` como tradução de
`Momentum(learning_rate=0.01, momentum=0.99)`.

Mas pela álgebra que o **próprio livro** estabelece em `content/cap16/05-perda-e-otimizacao.qmd:352`
— com `dampening=0`, o buffer do PyTorch converge para $g/(1-\mu)$ —, com $\mu = 0{,}99$ o passo
efetivo lá é **cem vezes** o nosso. A tradução fiel é `lr=0.0001`.

O PyTorch não está instalado aqui, então isto **não é executável**: decorre da análise que a §5
já faz e que a revisão confirmou correta. Corrija a §8 para ser consistente com a §5.

### A4 — "Dez mil imagens de teste" contradiz o próprio capítulo. **O erro é meu.**

`content/cap16/08-exemplo-mnist.qmd:463` — o parágrafo de handoff, que **eu** reescrevi — diz
"para cada uma das **dez mil** imagens de teste".

O capítulo fixa `N_TESTE = 2000` em `:154`, a tabela de corte em `:140` traz
"imagens de teste | 10.000 | **2.000**", o laço de confusões em `:367` é `range(N_TESTE)`, e
`:333` diz "são 2.000 imagens de teste". **Troque por "duas mil".**

### A5 — Superlativo falso sobre o preço de render

`content/cap16/08-exemplo-mnist.qmd:145` afirma ser "o **único** em que esse preço aparece com
unidade e valor medido". Quatro outros trazem: `cap09/03:57` (~6 s), `cap12/07:57` (~90 s),
`cap15/04:161` (~1 min), `cap17/05:78` (~16 s).

A tese real do parágrafo é outra e continua verdadeira: é o único em que **esse preço decide o
que o capítulo consegue afirmar**. Use essa.

### A6 — Outro superlativo, com contraexemplo no capítulo 13

`content/cap16/07-softmax-e-dropout.qmd:267` afirma que "este capítulo é o **único do livro** que
introduz uma técnica sem demonstrar que ela serve".

`content/cap13/05-maquinas-de-vetores-de-suporte.qmd` apresenta a margem máxima e diz, com todas
as letras, que a seção não implementa a SVM — sem nenhuma medição de que ela serve. Restrinja o
escopo ("o único **modelo** que este livro constrói sem conseguir demonstrar que serve") ou cite
a SVM como o outro caso.

### A7 — Rótulo de figura duplicado entre capítulos

`fig-perda-fizz-buzz` existe em `content/cap15/04-exemplo-fizz-buzz.qmd:168` **e** em
`content/cap16/06-outras-funcoes-de-ativacao.qmd:245`. O ID de crossref do Quarto é **global**:
um futuro `@fig-perda-fizz-buzz` resolveria para uma só. Hoje ninguém referencia, e por isso
passou.

Pior: as duas `fig-cap` são **idênticas palavra por palavra**, embora sejam corridas diferentes
— a do 16 é Tanh/SSE/Momentum, 300 epochs, começa num patamar de 2.760 e desce em degraus.

**Renomeie a do capítulo 16** para algo como `fig-perda-fizz-buzz-tanh` e reescreva a legenda
dizendo o que mudou. **Não toque na do capítulo 15.**

---

## Menores

- **M1** — `content/cap16/08-exemplo-mnist.qmd` mistura `optimizer` (declarado em `:195`) com
  `otimizador` (`:244`, `:247`, `:305`, `:312`, `:482`), e `modelo`/`model`, `X_treino`/`images`,
  `perda_treino`/`total_loss`. As seções 16.5 a 16.7 usam `optimizer` sem exceção. Padronize a
  16.8 com o resto do capítulo.
- **M2** — `content/cap16/02-a-abstracao-de-camada.qmd:180` usa `torch.exp` e importa só
  `import torch.nn as nn`. Falta `import torch`.
- **M3** — `content/cap17/03-exemplo-encontros.qmd:101` e `:136`: os títulos usam `--`, e o
  matplotlib **não** converte para travessão — sai hífen duplo literal. É o único lugar do livro
  com isso. Use `—`.
- **M4** — `content/cap17/05-exemplo-clustering-de-cores.qmd:117`: o painel diz "5 cores"
  enquanto o contraponto em `:177` diz "5 cores, semente 1". A seção existe para mostrar o efeito
  da semente, e esta usa `random.seed(0)`. → "5 cores, semente 0".
- **M5** — `content/cap17/03-exemplo-encontros.qmd:95` e
  `content/cap17/06-clustering-hierarquico.qmd:215`: `plt.axis([-60, 40, -30, 40])` **sem**
  `set_aspect('equal')`. Hoje a proporção sai certa por acidente (a caixa padrão casa com os
  limites), mas **são figuras de distância**: qualquer mudança de `figsize` distorce a geometria
  em silêncio. Fixe `set_aspect('equal')` e **confira a figura depois do render**.
- **M6** — `content/cap17/06-clustering-hierarquico.qmd:210` e
  `content/cap17/03-exemplo-encontros.qmd:90`: o número do centro é desenhado na média exata, e
  em `fig-hierarquico-min` o "2" cai sobre os dois círculos verdes e o "1" sobre um losango. Um
  deslocamento pequeno ou halo branco resolve. **Abra a figura depois.**
- **M7** — `content/cap14/03-a-entropia-de-uma-particao.qmd:213`: os rótulos de valor saem
  atravessados pela `axvline` vermelha quando `h` está perto de `antes`. Desloque para dentro da
  barra nesse caso. **Abra a figura depois.**
- **M8** — `content/cap16/05-perda-e-otimizacao.qmd:296`: a legenda "Momentum(0,1, momento 0,9)"
  fica ambígua (vírgula decimal ao lado da separadora) e metade do eixo x é linha reta em zero.
  → "Momentum (taxa 0,1; momento 0,9)", e corte o eixo em ~1.600 epochs ou use escala log.
- **M9** — `content/cap12/06-digressao-o-bootstrap.qmd:151` usa `random_state=0` em
  `scipy.stats.bootstrap`. Funciona na 1.18 e não emite aviso, mas o parâmetro documentado hoje é
  `rng`. Só registro; **não mexa** sem confirmar.
- **M10** — `content/cap12/07-erros-padrao-dos-coeficientes.qmd:207` e
  `content/cap12/05-qualidade-do-ajuste.qmd:117` mandam para o `statsmodels`, que **não está
  instalado no container** (confirmado: `ImportError`). Os callouts não executam, então o render
  não quebra — mas é o único par do livro cujo código o aluno não consegue rodar aqui. Uma
  cláusula ("não vem no container deste livro") fecha.

---

## Não pôde ser verificado — trate com cuidado

O PyTorch e o Keras **não estão instalados**. Estas duas ficam registradas, e **só mexa se você
confirmar na documentação**:

- `content/cap16/03-a-camada-linear.qmd:280` — o `nn.Linear` chama
  `kaiming_uniform_(weight, a=sqrt(5))`, e o ganho $a=\sqrt5$ **cancela** o ajuste para ReLU: o
  limite efetivo é $1/\sqrt{\text{fan\_in}}$, não o $\sqrt{6/\text{fan\_in}}$ de Kaiming-para-ReLU.
  Dizer "pensada para redes com ativação ReLU" pode estar invertido.
- `content/cap16/04-redes-como-sequencia-de-camadas.qmd:184` — `keras.layers.Dense(..., input_shape=(784,))`
  é idioma do Keras 2; no Keras 3 o padrão é `keras.Input(shape=(784,))` como primeiro elemento.
- `content/cap16/07-softmax-e-dropout.qmd:330` — "a documentação avisa isso **em negrito**". A doc
  diz *unnormalized logits*, mas o negrito não foi confirmado. "avisa explicitamente" é seguro.
