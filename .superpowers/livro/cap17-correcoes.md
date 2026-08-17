# Capítulo 17 — Clustering: correções

A revisão de conteúdo **reproduziu as oito afirmações medidas, todas exatas**, leu as 9 figuras
e não achou **nenhum Crítico**. Ela confirmou coisas que valem registro: o `assert` do §6 prova
a igualdade com o k-means **dentro do render**, o que é mais forte que afirmar no texto; a
dívida do capítulo 4 (`vector_mean`) está paga com a frase exata; e as 12 ocorrências de
vocabulário supervisionado no capítulo são todas **contrastivas** ("o que **não** se aplica").

**Você não vai reescrever o capítulo.** Três Importantes e sete Menores.

---

## Importantes

### I1 — Um superlativo que o capítulo 16 vai derrubar amanhã

`05-exemplo-clustering-de-cores.qmd:64` — "Este é o **único** treino deste livro que demora o
suficiente para a barra do `tqdm` fazer diferença".

O capítulo 16 está sendo escrito agora, e o MNIST em Python puro passa **muito** longe dos 16 s
deste — o orçamento medido para ele é de ~2,5 minutos, e um epoch sobre o conjunto inteiro custa
seis. Troque por "um dos poucos", ou remova o superlativo. **Afirmação sobre o livro inteiro
feita de dentro de um capítulo é aposta**, e esta perde.

### I2 — O degrau do k=7 fica na página sem uma linha que o nomeie

`04-escolhendo-k.qmd:71`. A tabela impressa logo acima mostra `k = 7  erro = 430.8  (-47%)`, e a
frase seguinte diz que a partir de k=4 "a curva vira quase uma reta rente ao eixo". O callout de
`:106` explica só as **subidas** da curva.

O mecanismo é o mesmo — cada ponto da curva é uma execução independente, e ali o k-means caiu num
ótimo local afortunado —, mas o leitor vê um −47% no meio de uma reta e não recebe explicação.
Uma frase no callout resolve, e reforça o ponto da seção.

### I3 — A prosa contradiz a figura sobre as duas cores

`05-exemplo-clustering-de-cores.qmd:185` diz "dois vermelhos quase idênticos… que o olho não
distingue". Os valores são `[217, 37, 25]` e `[224, 48, 43]`, e no `fig-outra-semente` eles
deixam o campo vermelho **visivelmente manchado, em duas regiões**.

O ponto pedagógico sobrevive melhor sendo verdadeiro: "duas variantes do mesmo vermelho, que a
olho nu só aparecem como manchas no campo". **Abra a figura antes de reescrever.**

---

## Menores

- **M1** — `05:78`: `print(f"treino concluído em {time.time() - inicio:.0f} s")` publica um
  número **dependente da máquina**. O CI vai imprimir outro a cada render — é exatamente o ruído
  de diff que a regra da semente existe para evitar neste livro. Tire o número da página (ou
  mande para `#| include: false`); se o tempo importa ao texto, cite-o em prosa como medição
  desta máquina.
- **M2** — `06-clustering-hierarquico.qmd:295`: "Duas folhas com as mesmas coordenadas são, para
  o Python, o mesmo objeto." Não são: são **iguais** (`==`), não **idênticas** (`is`) — e a
  distinção é justamente o defeito que o callout está explicando.
- **M3** — `index.qmd:14` e `01-a-ideia.qmd:9`: "o único modelo não supervisionado do livro" /
  "o único capítulo em que ninguém respondeu nada" colide com o **PCA** do
  `content/cap07/08-reducao-de-dimensionalidade.qmd`, e o próprio `index.qmd:48` chama o PCA de
  método não supervisionado. O enquadramento vem de `cap08/02:28`, então não é erro novo — mas é
  aqui que a contradição aparece na mesma página. Qualifique ("o único **modelo** não
  supervisionado", ou "o primeiro capítulo cujo objetivo é agrupar, não prever").
- **M4** — As cores e os marcadores **trocam entre figuras que o texto manda comparar**: em
  `fig-tres-grupos` o grupo oeste é vermelho e o nordeste é verde; em `fig-dois-grupos` e em
  `fig-hierarquico-max` o nordeste é vermelho. `desenha_grupos` colore por índice de grupo, que
  muda entre execuções. Fixe a cor por posição (ou por rótulo), para que a comparação que o texto
  pede seja possível de fazer com os olhos.
- **M5** — `01-a-ideia.qmd:44`: a prosa diz que o segundo amontoado está "logo **abaixo** das 20
  horas" porque o empregador "evita cruzar o limite legal", mas `random.gauss(19.5, 1.2)` põe
  cerca de **um terço** desse grupo acima de 20 h, e a figura mostra barras até 22,5. Um
  `min(20, ...)` ou uma média menor faz a figura contar a história do texto. **Abra a figura
  depois de mudar.**
- **M6** — `02-o-modelo.qmd:46`: a receita numerada começa "Comece com *k* médias", enquanto o
  código 80 linhas abaixo começa com **atribuições** aleatórias. A reconciliação só chega em
  `:161`. O Grus tem a mesma emenda; aqui dá para costurar com meia frase.
- **M7** — `05:187`: "desperdiçou metade do orçamento de cores" — dois de cinco são 40%.

---

## Não mexa nisto

Os números todos (as médias dos três e dos dois grupos, os 20 valores da curva do cotovelo, os
355.200 pixels, os 16 s de treino, os 177.522 pixels vermelhos, o `min` → `[2, 4, 14]` e o `max`
→ `[5, 6, 9]`), o `assert` que prova a igualdade com o k-means dentro do render, a ponte com a
§12.5, e a dívida do capítulo 4 paga em `02-o-modelo.qmd:99-105`.
