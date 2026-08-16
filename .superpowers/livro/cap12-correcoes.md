# Capítulo 12 — Regressão Múltipla: correções

Duas revisões independentes. A de conteúdo **mediu tudo** — rodou o bootstrap com B=400, 40
sementes, 5.000 contra 20.000 passos — e falsificou três afirmações do capítulo. A didática
achou que o arco funciona ("é um capítulo, não oito tópicos") mas que ele não tem fechamento
visível.

**A boa notícia primeiro, porque ela muda o tom da rodada:** o núcleo do capítulo está certo.
Todos os números centrais batem, o bootstrap roda mesmo as 100 reamostras, a §5 demonstra
rodando, a §8 está matematicamente correta, as duas figuras descrevem o que a prosa diz, e o
arco de oito seções se sustenta. **Você não vai reescrever o capítulo. Vai consertar as
explicações erradas que ele dá para uma discrepância real.**

---

## A raiz comum — leia isto antes de qualquer item

Três achados diferentes (I2, I3, I4) têm a mesma origem: **o capítulo ajusta o modelo de uma
variável por gradiente descendente, obtém 0,84, e depois inventa três mecanismos diferentes
para explicar por que isso não bate com o 0,9039 do capítulo 11. Nenhum dos três existe.**

O que foi medido, e é o que o texto deve dizer:

- **Não é a semente.** Desvio padrão de β sobre 40 sementes: `[0.0003, 0.0000, 0.0000, 0.0002]`.
- **Não são poucos passos.** 5.000 e 20.000 passos dão **0,8415 bit a bit**, nas três sementes
  testadas.
- **É um ciclo-limite determinístico.** Com ordem de lote fixa e taxa de aprendizado fixa, o
  gradiente descendente estocástico não pousa no mínimo: ele entra numa órbita estável
  *deslocada* dele. Mais passos não corrigem, porque não há ruído a promediar — o viés é
  estrutural do otimizador com esses hiperparâmetros.

E os valores **exatos**, que eu resolvi pela equação normal e confirmei:

| modelo | β de `amigos` (exato) |
|---|---|
| só `amigos` | **0,903866** — idêntico ao do capítulo 11 |
| `amigos` + `horas` | **0,927439** |
| `amigos` + `horas` + `doutorado` | **0,972505** |

**A subida real é de +7,6%, não "mais de 15%".** O 15% vem de comparar o 0,84 contaminado com
o 0,97 do modelo completo.

E o achado que amarra tudo: a solução exata do modelo completo é
`[30.579, 0.9725, -1.865, 0.9232]` — **exatamente o que o Grus imprime, dígito a dígito.** Isto
resolve de graça o enigma "nossos números diferem dos do livro": **o Grus imprimiu a solução
exata; o nosso gradiente descendente é aproximado.** Diga isso, é uma frase e mata três
explicações erradas.

**A correção estrutural que eu quero:** use os **valores exatos** para o argumento pedagógico
sobre modelos aninhados (§2 e §4). O ponto ali é estatístico — o coeficiente muda quando outras
variáveis entram —, não sobre otimização. Com os valores exatos, o problema some da §2 e da §4,
e o callout do 0,84 encolhe para o que ele deveria ser: uma nota honesta explicando por que o
número que o *nosso* código imprime difere, e por quê isso não é conserto de mais passos.

---

## Críticos

### C1 — §7: "mais reamostras aproximariam os dois" é falso

`07-erros-padrao-dos-coeficientes.qmd:200` afirma que o bootstrap com 100 reamostras
"superestima um pouco, e mais reamostras aproximariam os dois".

**Medido com B=400:** `[1.3024, 0.1024, 0.1535, 1.2360]`, contra `[1.2715, 0.1032, 0.1551,
1.2491]` com B=100. Quadruplicar não move em direção a `1,19 / 0,080 / 0,127 / 0,998` — o termo
constante até **sobe**. E o mecanismo alegado não existe: o desvio padrão amostral de B
réplicas **não tem viés para cima**.

A explicação verdadeira é melhor, e é conteúdo de primeira: **as duas coisas medem alvos
diferentes.** A fórmula fechada dá o erro padrão *sob a hipótese de erros normais independentes
com variância constante*. O bootstrap de pares não assume nada disso — ele reamostra
`(x, y)` juntos, então é robusto a heterocedasticidade e a erro de especificação. Que os dois
discordem é **informação sobre os dados**, não imprecisão de um deles.

Note que `07:59` já cita o Grus corretamente ("mais amostras **e mais iterações**"), e a linha
200 descarta a metade das iterações para afirmar uma convergência que não acontece.

### C2 — O capítulo não tem fechamento visível

`08-regularizacao.qmd:177` — a ponte para o capítulo 13 está **dentro** de um
`::: {.callout-tip collapse="true"}`, fechado por padrão. Quem não expandir termina o **maior
capítulo do livro** na frase "No segundo, insistir nunca funciona", sobre o *lasso*.

Compare: o capítulo 8 fecha com "Onde este capítulo deságua" e o 11 com "O que isso amarra",
**antes** do callout colapsado. Falta o bloco equivalente: três parágrafos visíveis amarrando
ajuste → interpretação → R² cego → bootstrap → erros padrão → encolhimento, e entregando ao
capítulo 13. **O parágrafo final do callout já é quase esse texto — basta promovê-lo para
fora** e completá-lo.

---

## Importantes

### I1 — §5: a caixa "detalhe honesto" está factualmente errada

`05-qualidade-do-ajuste.qmd:92` afirma que "a imprecisão do próprio otimizador é da mesma ordem
de grandeza" que o ganho de uma coluna, e que "com uma coluna só o R² tanto pode subir quanto
descer um fio". As duas coisas são falsas:

- **Uma** coluna de ruído dá R² = **0,682490**, contra 0,679985 sem ela — sobe, e o valor é
  idêntico até a sexta casa nas sementes 0 e 7.
- A imprecisão do otimizador em R² é ~**2,6 × 10⁻⁵** (GD 0,679985 contra exata 0,680011) —
  **duas ordens de grandeza abaixo** do ganho de uma coluna.

A lição do parágrafo é boa; o problema é a medição inventada que a sustenta. Uma coluna já
demonstra o ponto sem ambiguidade — e o texto pode dizer isso, mostrando que vinte colunas
apenas tornam o efeito impossível de ignorar.

### I2 — §3: o callout se contradiz, e põe a explicação falsa primeiro

`03-ajustando-o-modelo.qmd:150` diz "rodar com outra semente move a resposta um pouco, e é isso
que separa os dois conjuntos de números". **Falso** (ver a raiz comum: desvio de 0,0003). O
parágrafo seguinte, `:152`, dá a explicação **certa** — o Grus imprimiu a solução exata. Então
o callout oferece duas causas incompatíveis e coloca a errada na frente. Corte a primeira.

Ainda em `:150`: "as diferenças aparecem na terceira casa" é falso para dois dos quatro
coeficientes — constante 30,5148 contra 30,58 (0,065) e horas −1,8507 contra −1,865 (0,019),
ambas na **segunda** casa.

### I3 — §2: "A segunda se combate com mais passos" é falso

`02-hipoteses-do-minimos-quadrados.qmd:122`. Ver a raiz comum: 5.000 e 20.000 passos dão o
mesmo valor bit a bit. Substitua pela explicação do ciclo-limite.

**A tese principal do callout — "a diferença é do otimizador, não do modelo" — está CERTA**, e o
"0,904 → 0,972" também. Não jogue o callout fora; conserte o mecanismo.

### I4 — §2 e §4: o "mais de 15%" está inflado ~2×, e o 0,84 contamina o argumento

`02:113` diz "uma diferença de mais de 15%". A subida exata é **+7,6%** (0,9039 → 0,9725).
`04-interpretando-o-modelo.qmd:45` reaproveita o mesmo 0,84 para sustentar o ponto pedagógico
mais importante do capítulo — "os dois coeficientes respondem a perguntas diferentes" — apoiado
num número que a §2 declarou artefato duas seções antes.

**Use os valores exatos nos dois lugares** (0,904 / 0,927 / 0,973 e +7,6%).

### I5 — A sobreposição amigos×doutorado aparece três vezes

Chunk `sobreposicao` em `02:64-76`, chunk quase idêntico em `04:50-67`, e a mesma frase em prosa
em `07:164` ("abaixo de 6 amigos… 22 usuários dos 203"). Duas execuções do mesmo cálculo e três
narrações. Corte o chunk da §4 e deixe só a frase que ele sustenta; a §7 pode reduzir a "os 22
usuários da [seção 12.2](...)".

### I6 — §4 é a única seção que abre com célula de código

Título, callout, dois chunks ocultos, e o `mostra-beta` cospe a tabela antes de qualquer frase.
As outras sete abrem com prosa, e o capítulo 9 também. Isso é também a **dobradiça 3→4 que não
existe**. Sugestão da revisão, que serve: *"A [seção anterior](03-ajustando-o-modelo.qmd)
produziu quatro números. Ajustar é a parte fácil; dizer o que eles significam é onde a
estatística aplicada costuma errar."*

### I7 — A figura da §7 esconde o que o texto afirma

`fig-bootstrap-coeficientes`: os três painéis têm eixos *x* independentes, então `amigos`
(0,75–1,5) e `doutorado` (−2 a 4) **parecem igualmente espalhados**. A lição da seção é que a
incerteza do doutorado é uma ordem de grandeza maior — e a figura normaliza isso para fora.

A §6 acertou o mesmo problema (`range=(-10,210)` nos dois painéis, e a legenda diz "Mesma escala
nos dois painéis"). Use `sharex=True` ou um `set_xlim` comum. **Depois de renderizar, abra o PNG
e confirme** que a diferença de espalhamento agora se vê.

### I8 — §7: dois tropeços em quinze linhas

- `07:126` — "distribuição *t* de Student com $n-k$ graus de liberdade". Este leitor pode nunca
  ter visto a *t*, e "graus de liberdade" entra sem definição. Uma frase resolve.
- `07:143-146` — os `assert` usam 30.58 / 0.972 / −1.865 / 0.923 (os números do Grus) logo
  depois de a tabela imprimir 30,5148 / 0,9748 / −1,8507 / 0,9141. Nada explica a troca.
  Acrescente um comentário no chunk: `# os valores do livro impresso — que são a solução
  exata; os nossos, logo acima, vêm do gradiente descendente`.

### I9 — §7 não entrega à §8, e o arco "se fecha" duas vezes

`07:169` diz "Repare no arco que se fechou aqui" e `08:113` diz de novo "O arco se fecha aqui".
O primeiro deveria ser *"o arco que se fechou até aqui — falta o passo que age sobre esse
diagnóstico"*, apontando para a §8.

### I10 — `.exemplo` usado três vezes para o que não é exemplo

`04:93` (transição para a §5), `05:87` (ressalva metodológica), `08:148` (reflexão sobre limites
de escopo). O guia reserva `.exemplo` para "um caso concreto que ilumina o conceito" — e a §2 o
usa exatamente assim em `02:84`. Os três primeiros são `.callout-note` ou prosa corrida.

---

## Menores

- **M1** — `06:61`: "O código todo tem quatro linhas de corpo". As duas funções têm um `return`
  cada; com as docstrings dá quatro, sem elas dá duas. Ambíguo. Troque por algo que não dependa
  da contagem: "duas funções, um `return` cada".
- **M2** — `06:12` chama `get_sample(num_points=n)`, que **não existe em lugar nenhum** do
  projeto (conferido). Diga explicitamente que é imaginária.
- **M3** — `06`, primeira frase: "Esta seção é uma digressão — ela sai da regressão por
  completo" cria a moldura errada antes de desmontá-la. Inverta: *"O título do Grus chama isto
  de digressão. É a ideia mais reaproveitável do capítulo."*
- **M4** — `08:42` "a **dureza** da penalidade" destoa; `08:175` já usa "força da penalidade".
  Padronize em "força". E `08:125` "Reescale antes de regularizar" — o livro usa
  "reescalonamento" (capítulo 7). Prefira "Ponha as variáveis na mesma escala antes de
  regularizar".
- **M5** — O título `02:116` "O número de 0,84 e o número de 0,904" é opaco no índice lateral.
  "Por que este 0,84 não bate com o 0,904 do Capítulo 11" diz o que o callout faz.
- **M6** — `01:70-76`: chunk executável cujo único produto é ecoar um literal com comentários.
  Um bloco ```` ```python ```` não executado serve melhor.
- **M7** — `04:87-91` discute interações e não linearidades sem apontar para os modelos que as
  capturam sem engenharia manual (árvores no capítulo 14, redes no 15). Ponteiro de graça.
- **M8** — `05:92` larga a fórmula $(1-R^2)/(n-k)$ sem origem. Troque por "uns poucos milésimos
  com 203 pontos" e cite a regra de bolso sem escrevê-la.
- **M9** — `08:87`: "basta trocar `sqerror_gradient` por `sqerror_ridge_gradient`… o resto do
  otimizador não muda uma linha". No pacote, `least_squares_fit_ridge` também troca
  `tqdm.trange` por `range`. Fiel na ideia, impreciso quanto ao código que o aluno vai abrir.
- **M10** — `03:59` diz "minilotes"; o capítulo 5 usa **minibatch** exclusivamente (29
  ocorrências, zero "minilote") e o próprio capítulo 12 usa "minibatch" nas linhas 92 e 118.
  Uniformize.
- **M11** — **Dívida de fora:** `content/cap11/03-maxima-verossimilhanca.qmd:35` promete que
  "o Capítulo 12 volta" à **homocedasticidade**. A palavra não aparece em nenhum arquivo do
  capítulo 12; `07:200` a menciona de passagem ("variância constante") dentro do callout do
  `statsmodels`. **Cumpra a promessa** — um parágrafo na §2 ou na §7 dizendo o que quebra sem
  ela. Isso encaixa com C1, que é justamente sobre o bootstrap não precisar dessa hipótese.
