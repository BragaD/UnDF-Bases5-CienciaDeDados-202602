# Capítulo 17 — Clustering: correções, segunda rodada

A revisão didática não achou **nenhum Crítico** e confirmou o que mais importava: a mudança de
categoria chega ao aluno (quatro reencontros com a mesma ideia, cada um mais concreto), a ponte
com a §12.5 tem peso, e **o livro termina em vez de apenas parar**. Ela também verificou que a
correção das cores funcionou — `fig-hierarquico-max` ficou **pixel a pixel idêntica** a
`fig-tres-grupos`, o que torna a frase "as duas figuras podem ser sobrepostas" literalmente
verdadeira.

**Eu já apliquei o achado B** (a segunda promessa do capítulo 1, sobre usos que ajudam e usos
que manipulam, que o fecho deixava na mesa). **Não mexa nesse parágrafo.**

Sobra um Importante e dez Menores.

---

## Importante

### I1 — As duas aberturas do capítulo são quase o mesmo texto

`index.qmd:12` e `01-a-ideia.qmd:7` trazem a mesma tese, a mesma lista de exemplos (íris, spam,
minutos, dígito) e a mesma cadência. Lidos em sequência — e são —, o aluno relê.

O modelo de estilo não faz isso: `content/cap09/index.qmd` enquadra ("ele não aprende, ele
guarda") e `content/cap09/01-o-modelo.qmd` abre com um cenário novo.

**Deixe a lista de exemplos e a tese no `index`**, e faça a §1 começar pelo que o `index` não
disse. A revisão sugeriu um caminho que funciona: em cada um daqueles casos **alguém já tinha
respondido à pergunta antes** — um botânico, um usuário que apertou "marcar como spam", um
relógio — e o modelo aprendeu a imitar essa resposta; aqui ninguém respondeu.

---

## Menores

- **M1** — `02-o-modelo.qmd:106`: "É uma **remenda**" → "É um **remendo**".
- **M2** — `index.qmd:18`: "O **k-means** é o mais conhecido do mundo" fica pendurado (o mais
  conhecido *o quê*?) e é superlativo sem fonte. → "o algoritmo de agrupamento mais usado que
  existe".
- **M3** — `04-escolhendo-k.qmd:97`: "ele contradiz aparentemente o que o parágrafo anterior
  afirmou" é ordem dura. → "e ele parece contradizer o que o parágrafo anterior afirmou".
- **M4** — `04-escolhendo-k.qmd:93`: "**Uma métrica de forma decide**" é coinagem opaca, e o
  resto do item fala de **separação**, não de forma. → "Uma métrica de separação decide."
- **M5** — `06-clustering-hierarquico.qmd:294`: "chocantemente ineficiente" é tradução dura de
  *shockingly inefficient*. → "de uma ineficiência chocante" ou "assombrosamente ineficiente".
- **M6** — `index.qmd:7`: a epígrafe de Herrick só funciona porque *clusters*, em inglês, são
  **cachos** de uva — e o trocadilho some em português, onde o capítulo nunca diz "cachos". Meia
  frase depois da atribuição recupera a piada, registrando que no original é a mesma palavra que
  dá nome ao capítulo.
- **M7** — `fig-hierarquico-min`: a cor sai do **posto** leste→oeste, não da posição absoluta,
  então o verde marca ali o par do nordeste enquanto marca o centro-sul nas outras três figuras.
  A legenda salva, mas `06:220` ganharia clareza nomeando a cor ("partidos em quatro, vermelhos,
  mais dois, verdes"). **Se mexer, abra a figura depois do render.**
- **M8** — `n_init` e `k-means++` são explicados **três** vezes (`02:186-187`, `03:174`,
  `05:192`). O de `02` é o didático; o de `03` é quase só repetição. Como cada página tem kernel
  próprio, alguma redundância é de projeto — mas `03:174` pode encolher para uma frase e um link.
- **M9** — `02-o-modelo.qmd:44`: "repetir **dois** passos exatos" seguido de uma lista de
  **quatro** itens. Os negritos em *Atribua*/*recalcule* quase resolvem; "repetir dois passos
  exatos (2 e 4) até nada mudar" fecha.
- **M10 — decisão minha, para você não gastar tempo:** a revisão levantou a hipótese de um
  "Na prática" na §17.4 sobre `adjusted_rand_score`, para o caso em que rótulos existem por acaso
  (agrupar as íris do capítulo 9 e comparar com a espécie). **Não escreva.** O capítulo passou
  seis seções fechando essa porta com cuidado; reabri-la no penúltimo callout enfraquece a lição
  mais importante do capítulo por um ganho pequeno.

---

## Não mexa nisto

- **O parágrafo novo do fecho**, sobre a segunda promessa do capítulo 1. Já está aplicado.
- O resto do fecho — a conferência da primeira promessa, as três dívidas nomeadas, e o parágrafo
  do "desconfiar de um resultado que parece bom" com as seis instâncias do próprio livro.
- `04:87-89`, que a revisão chamou de melhor parágrafo do capítulo: ele não para no paralelo com
  a §12.5, avança para a **assimetria** — na regressão o critério de fora existia e tinha nome;
  aqui não há.
- `01:65` ("Nos dezesseis capítulos anteriores, a métrica de sucesso vinha de fora, junto com os
  rótulos. Aqui ela vem de você").
- Os seis "Na prática", todos com conteúdo real.
