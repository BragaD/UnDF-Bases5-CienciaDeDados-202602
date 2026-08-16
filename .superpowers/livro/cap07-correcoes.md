# Capítulo 7 — apontamentos consolidados das duas revisões

**Revisão de conteúdo: 0 Crítico, 0 Importante, 1 Menor.** Confirmatória, não corretiva —
a verificação anterior já tinha pego as cinco divergências. O revisor confirmou a correlação
por **derivação** (Var=1,25, Cov=1, logo 1/√1,25 = 0,894), abriu as oito figuras uma a uma,
e validou que o Grus tem um erro aritmético no livro impresso.

**Revisão didática: 3 Críticos, 8 Importantes, ~10 Menores.**

Corrija tudo. Se discordar de algum item, não o ignore em silêncio: implemente o resto e
diga no relatório qual recusou e por quê.

**Rode `make render` em primeiro plano quando terminar** — ele se autocura, imprime
`render OK (tentativa N)`. Não use `make clean`, não rode em segundo plano.

---

## O veredito que organiza tudo

> **É um capítulo — mas hoje ele lê como sete mais um.**

A abertura do `index.qmd` (o dado que chegou pelos canos do capítulo 6 quase nunca está
pronto para a máquina do capítulo 5) foi chamada de a melhor do livro depois da do capítulo 5.
O problema é que ela é enunciada **uma vez e nunca reinvocada**. Das oito seções, só duas
juntas passam bastão: 7.2→7.3 e 7.7→7.8.

**Duas pontes já existem no material e não são usadas:**

1. **`de_mean` (7.8) é literalmente metade do `rescale` (7.6)** — mesma translação, sem
   dividir pelo desvio padrão. E a "Na prática" da 7.8 já diz que é preciso rodar
   `StandardScaler` antes do `PCA`. Uma frase na abertura da 7.8 converte o estranho em
   desfecho:
   > *"Centralizar é a metade da 7.6 que sobrou: mesma translação, sem dividir pelo desvio
   > padrão. Por que só a metade — e quando a outra também precisa vir junto — é o que a
   > 'Na prática' desta seção fecha."*
2. O `.conceito` da 7.1 diz que a matriz de dispersão "não escala além de um punhado de
   dimensões". **A 7.8 nunca recolhe essa deixa** — sendo que ela é exatamente o problema
   que o PCA resolve.

---

## CRÍTICOS

### C1 — a 7.8 **sobe** o gradiente e não avisa

`first_principal_component` chama `gradient_step(guess, gradient, step_size)` com
`step_size = 0.1` **positivo**. Isso é **ascensão** de gradiente: estamos maximizando a
variância direcional, não minimizando um erro.

Todo o resto do livro passa passo **negativo**, e o `content/cap05/03-usando-o-gradiente.qmd`
diz explicitamente: positivo para andar *com* o gradiente, negativo para andar *contra*.

**Este é o único uso ascendente do livro inteiro, e passa em silêncio** — num livro cuja
identidade é abrir caixas-pretas. Nota obrigatória:

> *"Repare no sinal: `step_size` aqui é positivo. Queremos **maximizar** a variância
> direcional, não minimizar um erro — então andamos **com** o gradiente. É o mesmo
> `gradient_step` de cinco linhas do [Capítulo 5](../cap05/03-usando-o-gradiente.qmd),
> usado ao contrário."*

### C2 — falta "Na prática" em 7.4 e 7.5

São as duas seções mais em formato-`pandas` do capítulo — a assinatura do livro ausente
justamente onde ela ensinaria mais. E as duas têm o que dizer; não é propaganda:

**7.4 (limpeza):** `pd.read_csv(..., parse_dates=[...], na_values=[...])` e
`to_numeric(errors='coerce')`. **O que a biblioteca esconde:** a coerção é **silenciosa** —
a linha ruim não é rejeitada, ela *sobrevive* como `NaN`/`NaT` e vai contaminar a média lá
na frente. É o irmão exato do "erro que passa pelo filtro" que a própria seção acabou de
contar (a linha da FB com ano 3014).

**7.5 (manipulação):** `df.groupby('Symbol')['Close'].max()`, `.pct_change()`,
`.resample('M')`. **O que esconde:** `pct_change()` assume que as linhas já estão ordenadas
e contíguas — a etapa `sorted(symbol_prices)` que a seção gastou um parágrafo justificando.
Esqueça o `sort_values('Date')` e o `pandas` não reclama: devolve variações entre dias que
não são consecutivos.

### C3 — a 7.8 nunca argumenta **por que variância**

Para este leitor — que provavelmente nunca viu PCA — faltam três coisas, e são as três que
fazem a técnica clicar:

1. **Por que a direção de maior variância é a que vale a pena guardar.**
2. **Que "componente" é duas coisas**: primeiro uma direção, depois uma coordenada nova.
3. **Que `directional_variance` é uma soma de quadrados, não a variância dividida por *n*.**
   O aluno que for conferir contra a definição que já conhece vai travar.

Além disso, `directional_variance_gradient` **cai do céu** — sem derivação e sem um "aceite
este como dado, e eis por que é legítimo".

---

## IMPORTANTES

### I1 — fome de `.conceito`

**Uma única ocorrência em 1.374 linhas.** Comparação: 2 no capítulo 9 (muito menor), 4 no
10, 5 no 2. A seção mais difícil do livro (7.8) **não tem nenhum** — nada diz ao aluno o que
levar dali.

Dois candidatos naturais, ambos já meio escritos no texto:
- A equivalência "direção de maior variância = o que sobra quando você projeta e não perde
  muito".
- Em 7.6: *"reescalonar não é neutro: é uma decisão sobre o que conta como sinal"* — a frase
  já está lá, dentro de um `callout-important`. É `.conceito`.

### I2 — `fig-pca-primeiro-componente` ilustra, não ensina

Sem `set_aspect("equal")`, a direção (0,924; 0,383) — uma reta de ~22,5° — **desenha em
~45°**, e a intuição de "espalhamento perpendicular mínimo", que é o que faz o PCA fazer
sentido visualmente, fica falsa.

Uma linha resolve. Vale também para `fig-pca-demeaned` e `fig-pca-residual`.

As demais figuras ensinam bem — a matriz de dispersão e o "X" das distribuições conjuntas
foram elogiadas.

### I3 — o gênero de "componente" oscila dentro da 7.8, inclusive dentro do PNG

A prosa diz "a primeira componente principal"; o `plt.title` diz "Primeiro componente
principal" e "remover o primeiro componente". Padronize no **feminino** (uso corrente em
português), corrigindo os dois `plt.title` e os dois `fig-cap`.

### I4 — o `callout-important` do `index.qmd` está no lugar errado e duplica a 7.1

É a **segunda coisa** que o aluno lê no capítulo: sete linhas de encanamento de repositório
antes de qualquer objetivo de aprendizagem. E o parágrafo sobre o erro da correlação é quase
verbatim o da 7.1 — mesma frase "perto o bastante da borda inferior", mesmo "24,6% em 20 mil
repetições".

O `index` deve provocar em **uma frase**: o módulo que este capítulo descreve nunca é
importado aqui, por duas razões que a seção 7.1 e o próprio código expõem. A 7.1 conta.

E o resto do callout — a explicação de por que `StockPrice` é redefinido — pertence à **7.4**,
onde a primeira redefinição de fato acontece, e onde já existe um `callout-note` fazendo
metade do serviço.

### I5 — o erro do Grus: bem enquadrado na 7.1, dedo em riste na 7.3

A 7.1 é **exemplar** e não deve ser tocada: termina na lição ("uma afirmação sobre dado
aleatório só é reprodutível se a semente estiver fixada"), não no autor.

A 7.3 **especula sobre o processo de escrita alheio**: *"A explicação mais provável é
reaproveitamento de exemplo: o autor trocou o preço de 102.06 para 106.03 num rascunho e não
atualizou o assert."*

Corte a especulação. Guarde a aritmética (51,03 é metade de 102,06, o preço do `dict` da 7.2)
e a lição, que é ótima: *"é um erro de manutenção de texto, do tipo que só aparece quando
alguém tenta rodar o livro em vez de só lê-lo."*

No mesmo arquivo, dois `callout-warning` seguidos num arquivo de 83 linhas soam como
acúmulo. O segundo ("Este pacote não usa `dataclass`") é contexto útil, não armadilha —
vira `callout-note`.

### I6 — a frase que se corrige sozinha (7.1, l. 46)

*"...que veio do Capítulo 6... não — ela na verdade nunca apareceu em nenhum capítulo deste
livro até aqui"*. O leitor recebe uma referência errada e depois a retratação.

Proposta:
> *"Para o segundo, precisamos da inversa da normal acumulada. Ela não apareceu em nenhum
> capítulo até aqui: vive em `scratch/probability.py`, módulo que ficou fora da ementa desta
> disciplina, mas do qual o pacote do livro-texto depende. Importamos só a função:"*

### I7 — tradução dura na 7.8 (l. 177), justo onde precisa ser límpida

*"cada linha $x$ da matriz se estende `dot(x, d)` na direção $d$"* — decalque de *"extends
dot(x,d) in the direction d"*. É exatamente a frase de que o aluno sem PCA precisa que seja
clara.

Proposta: *"a projeção de cada linha $x$ sobre $d$ tem comprimento `dot(x, d)` — é o quanto
daquele ponto 'cabe' naquela direção."*

### I8 — sobra explicação na 7.2

O parágrafo sobre `dict` carregar tabela hash própria e gastar memória é dirigido a alguém
que não sabe o que custa um `dict`. **Este leitor sabe.** Uma frase basta; a razão que
importa (o erro de digitação silencioso) já vem logo depois e é bem contada.

---

## MENORES — corrija todos

- **7.3:** *"volta a **compilar** sem aviso nenhum"* — não há compilação no modelo mental em
  jogo, e para um aluno de CC é imprecisão gratuita. → "volta a passar sem aviso nenhum".
- **7.7:** usa **"embrulhar"** e **"envolver"** para *wrap* com seis linhas de distância.
  Padronize em "envolver".
- **7.7:** *"vai **eventualmente** deixar seu código instável"* — o Grus diz *occasionally*.
  Em português "eventualmente" está certo, mas o leitor de CC vai ler como falso cognato.
  → "vai, de vez em quando, deixar".
- **7.5:** *"Faremos esse tipo de manipulação o livro inteiro"* — falta preposição ("pelo
  livro inteiro").
- **7.5:** *"quase quatro décadas de dado misturados"* — singular com particípio plural.
  → "de dados misturados".
- **7.1:** a prosa diz que a série 3 explica "as **colunas** de pontos verticais"; na linha
  de baixo da matriz (série 3 no eixo *y*) elas são **horizontais**. → "as duas faixas de
  pontos — verticais quando a série 3 está no eixo *x*, horizontais quando está no *y*".
- **7.8:** a prosa hesita ("essencialmente alinhados", "quase toda a variação") onde a figura
  mostra uma reta exata — e a matemática **garante** que é exata. Afirmar o forte ensina
  mais: *"em duas dimensões, remover a projeção sobre uma direção deixa exatamente a direção
  ortogonal — daí a reta perfeita."*
- **7.2 e 7.3** encerram ambos em `pydantic`, e a 7.3 até admite ("A seção anterior encerra
  com esse ponto"). Deixe a 7.2 parar em "mutabilidade é a próxima seção"; a 7.3 fica dona
  do `pydantic`.
- **7.1:** "Ambos têm média perto de 0" antes das figuras e "Os dois têm média próxima de
  zero" depois — a mesma frase duas vezes em torno dos gráficos.
- **7.5:** usa `zip(prices, prices[1:])` sem apontar para o `zip`/desempacotamento do
  capítulo 2. Retrolink barato e ausente, num capítulo que acerta todos os outros.
- **Deriva entre capítulos, apontada na revisão do capítulo 10:** aquele capítulo diz que o
  `shuffle` do capítulo 5 "embaralha os lotes errados", mas o capítulo 5 é preciso ao dizer
  que embaralha os **índices de início**, não os pontos. Se o capítulo 7 fizer paráfrase
  parecida de algum outro capítulo, aperte.

---

## O FECHAMENTO — a intervenção de melhor custo-benefício do capítulo

O último parágrafo da 7.8 encerra o **PCA** bem, mas não encerra o **capítulo**.

Duas ou três linhas devolvendo a moldura da abertura — *o dado que chegou torto agora está
explorado, tipado, limpo, agregado, em escala comum e com dimensões a menos, pronto para a
máquina do capítulo 5* — transformariam as oito utilidades numa trajetória, retroativamente.

---

## DESTACADO COMO BOM — mas não isento da sua atenção

Os revisores elogiaram o que segue. **Isso não significa que esteja acima de verificação**:
no capítulo 5 deste livro, uma referência factualmente falsa sobreviveu a três passadas por
estar dentro de um box marcado "não mexer".

- A abertura do `index.qmd` (os canos do 6, a máquina do 5, a distância entre os dois).
- A "Na prática" da 7.1 — nomeia o que se esconde (Pearson como padrão, `describe`
  despachando por dtype, a heurística de buckets) e fecha no laço da própria seção. É o
  modelo para as duas que você vai escrever.
- A "Na prática" da 7.6 (vazamento por `fit` no teste) e a da 7.8 (SVD × gradiente; escala e
  sinal arbitrário).
- A 7.5 fechando na desconfiança do próprio resultado ("outubro é o melhor mês… número que
  vale hesitar antes de levar a sério") — chamada de a melhor frase do capítulo.
- A rede de referências (cap05→7.6, cap06→cap07, cap08→7.8, cap09→7.8, cap10→7.1), que é
  recíproca e real.
