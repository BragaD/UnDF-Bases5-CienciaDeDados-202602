# Capítulo 10 — apontamentos consolidados das duas revisões

**Revisão de conteúdo: 0 Crítico, 1 Importante, 2 Menores.** Toda a matemática de Bayes,
a suavização, o underflow e as três métricas foram recalculados à mão e batem com o HTML.
Fidelidade ao PDF conferida seção a seção, inclusive os números do próprio Grus citados
para comparação.

**Revisão didática: 2 Críticos, 12 Importantes, ~12 Menores.**

Corrija tudo. Se discordar de algum item, não o ignore em silêncio: implemente o resto e
diga no relatório qual recusou e por quê.

**NÃO rode `make render` nesta rodada** — outro agente está corrigindo o capítulo 7 em
paralelo. Faça as edições; eu renderizo e verifico depois, consolidado.

**Resumo do diagnóstico:** a engenharia pedagógica é sólida — a rampa uma-palavra →
vocabulário → código → teste de brinquedo → dados reais funciona, a §4 é excelente, e o
callout do `float` é modelar. Os dois Críticos são **de ordem**, não de conteúdo: os dois
se resolvem movendo e reescrevendo material que já está escrito.

---

## CRÍTICOS

### C1 — Bayes é despejado, não construído

A §1 abre com *"O teorema de Bayes diz que"* seguido da forma completa, com denominador de
probabilidade total. Para o leitor que nunca formalizou probabilidade — e o texto **não pode
supor que ele formalizou** —, isso é apelo à autoridade: ele não sabe ler $P(S \mid B)$, não
tem a regra do produto para verificar que $P(B \mid S)P(S)$ é o numerador certo, e a palavra
"simplesmente" carrega sozinha a lei da probabilidade total.

O texto **tem** a intuição certa — "essa conta é exatamente a proporção de mensagens com
*bitcoin* que são spam" — mas ela chega **depois** da fórmula, como consolo, em vez de antes,
como derivação.

**Comece com contagem.** Algo assim:

> De 1.000 mensagens, 500 são spam; dessas, 250 contêm *bitcoin*. Das 500 legítimas, 5
> contêm. Quem recebe uma mensagem com *bitcoin* está diante de 255 mensagens possíveis, e
> 250 delas são spam.

Aí a fórmula aparece como **a mesma conta escrita em símbolos**, e $\lnot S$ ganha a única
glosa de que precisa ("o evento complementar").

### C2 — o capítulo encena a lição do capítulo 8 e depois a defende com a métrica errada

Este é o achado mais importante da revisão.

O andaime está **todo montado**: o `.callout-warning` "Um conjunto desequilibrado, de
propósito" invoca a piada do Luke, promete o piso, o chunk `piso-sempre-ham` calcula 84,7%,
e o `.conceito` compara com 91,5%.

**Mas o argumento do capítulo 8 não é sobre acurácia — é que a acurácia esconde.** Comparar
84,7% contra 91,5% dá sete pontos de ganho: parece pouco, quase subvende o modelo, e usa
justamente o número que o capítulo 8 mandou não usar.

O número que fecha o argumento está a uma linha: o classificador "sempre ham" tem
**revocação 0** — não encontra nenhum dos 126 spams do conjunto de teste — e **precisão
indefinida**, porque nunca aponta ninguém. Contra 63,5% de revocação do modelo. É o mesmo
par 98,1%/1,4% do Luke, agora com dados de verdade.

Sugestão: mantenha a comparação de acurácia como isca e então vire a mesa.

> Sete pontos de acurácia parecem pouco. Mas olhe as outras duas: o classificador que
> responde "ham" para tudo tem revocação 0 — de 126 spams no conjunto de teste, encontra
> nenhum — e precisão indefinida, porque nunca aponta ninguém. É o teste do Luke com outro
> nome. Os 7 pontos de acurácia escondem a diferença entre um modelo e nada.

---

## IMPORTANTES

### I1 — o modelo assume 50/50 num corpus de 15% spam, e ninguém comenta

A suposição $P(S) = P(\lnot S) = 0{,}5$ entra de lado na §1 ("E se, além disso,
assumirmos…"), é carregada em silêncio para a fórmula da §2 e sobrevive intacta em
`predict`, que devolve `prob_if_spam / (prob_if_spam + prob_if_ham)` **sem prior nenhum**.

Ou seja: o capítulo que constrói um callout inteiro sobre o desequilíbrio 2.800/500 embute
no próprio modelo a hipótese de que as classes são equilibradas.

**Isso é achado, não defeito a esconder.** Explica boa parte dos 24 falsos positivos, e
explica por que os números do `scikit-learn` não batem (`BernoulliNB` usa `fit_prior=True`
por padrão). Um parágrafo curto na §5, logo depois da matriz de confusão, amarra este ponto,
o I6 e a honestidade do capítulo de uma vez.

### I2 — ninguém diz, em prosa, que `predict` devolve uma probabilidade — e que 0,5 é escolha

A única menção está num comentário de código. É a ideia mais transferível do capítulo, e
paga três dívidas:

- O `.exemplo` do capítulo 8 já disse, **com estas palavras**, que num filtro de spam o falso
  positivo é o e-mail importante que some no lixo, e que o limiar deve pender para a
  precisão. O capítulo tem 24 desses e não recolhe a deixa.
- É o contraste mais limpo com o capítulo 9, onde a votação devolve rótulo e não há botão
  para girar.
- É o que o aluno vai de fato mexer quando usar isso.

Duas frases depois do chunk `metricas`.

### I3 — o contraste com o capítulo 9 deixa o melhor de fora, e tem duas imprecisões

O que está lá (preguiçoso × treinado, compromisso de memória) está correto. Falta o par
óbvio: **o capítulo 9 gastou uma seção inteira mostrando que a distância morre em dimensão
alta, e este capítulo roda feliz com vocabulário de milhares de dimensões — por causa da
suposição de independência**, que troca geometria por contagens palavra a palavra. Isso
ensina os dois de uma vez e explica retroativamente a seção 9.3.

Duas imprecisões no mesmo parágrafo:
- *"O k-vizinhos não tem parâmetro nenhum para ajustar"* **contradiz o capítulo 9**, que
  discute a escolha de *k* e chega a dizer "numa aplicação real criaríamos um conjunto de
  validação para escolher".
- O capítulo nunca avisa que o *k* daqui (pseudocontador) e o *k* de lá (número de vizinhos)
  são **coisas diferentes com o mesmo nome**. Armadilha real, e este parágrafo é o lugar de
  desarmá-la.

Enquadramento limpo: nenhum dos dois *aprende* parâmetros otimizando; ambos têm um
hiperparâmetro escolhido à mão; a diferença é que um comprime os dados em contagens e o
outro guarda tudo.

### I4 — o F1 não aparece

O capítulo 8 definiu precisão, revocação **e** F1, e explicou que a média harmônica é puxada
para baixo pelo pior dos dois — feito sob medida para este caso. Aqui saem três métricas e a
quarta fica de fora.

`f1_score(80, 24, 46, 675)` dá **0,696**, e o piso "sempre ham" dá **0**. Importar de
`scratch.machine_learning` junto com as outras custa um nome no `import`.

### I5 — a omissão da lista de melhorias do Grus deixa um objeto morto no pacote

*(Este é o Importante da revisão de conteúdo.)*

O PDF traz, depois das palavras spammiest/hammiest, quatro sugestões: mais dados de treino,
um limiar `min_count`, um *stemmer* (com o exemplo `drop_final_s`) e atributos "fantasmas"
como `contains:number`. **Nada disso aparece no capítulo, nem como nota de omissão.**

Consequência concreta: `scratch/naive_bayes.py` define `drop_final_s`, que fica sendo um
objeto morto e inexplicado no módulo vendorizado — sem nada no livro dizendo por que existe.
Diferente das outras omissões do projeto (o download do SpamAssassin tem callout), esta não
tem nenhuma. Um parágrafo curto resolve.

### I6 — os dois "Na prática" não deixam o aluno reconhecer a escolha que ele fez sem perceber

Ambos mostram só `BernoulliNB`. Falta o essencial: **`MultinomialNB` existe, é a escolha mais
comum para texto, e a diferença entre os dois é exatamente o `set` do `tokenize`.**

> O `set` em `tokenize` é o que faz o nosso modelo ser Bernoulli e não multinomial:
> guardando contagens em vez de presenças, e trocando `BernoulliNB` por `MultinomialNB`,
> você teria a outra família — a que pergunta quantas vezes a palavra apareceu, não se
> apareceu.

Isso transforma uma linha de código que passou batida numa decisão de modelagem. E o que a
biblioteca esconde: `fit_prior=True` (ver I1) e `binarize`.

### I7 — a ausência de uma palavra chega como surpresa, quando devia chegar como consequência

A §2 escreve $P(X_1=x_1,\ldots,X_n=x_n \mid S)$ com $x_i$ genérico, mas **nunca diz o que o
fator vale quando $x_i = 0$**. Aí o `.conceito` da §3 apresenta o `log(1 - prob)` com um
"Repare no que `predict` faz" — retórica de revelação sobre algo que o leitor deveria já ter
na fórmula.

Uma frase na §2, logo depois da equação:

> Quando $x_i = 0$ — a palavra não está na mensagem — o fator correspondente é
> $1 - P(X_i \mid S)$. A ausência de uma palavra é informação tanto quanto a presença, e o
> modelo vai usar as duas.

O `.conceito` da §3, que é o melhor callout do capítulo, fica **mais forte** cobrando uma
promessa do que dando um susto.

### I8 — o *underflow* pede o número, e este é o público que o entende de imediato

*"O computador não lida bem com números de ponto flutuante grudados demais em zero"* é vago
justamente onde um número ensina — e é sutilmente enganoso, porque sugere problema de
**precisão** quando o problema é de **alcance de expoente**.

Para alunos de Computação:

> O menor `float` positivo representável fica em torno de $10^{-308}$; multiplicar 300
> fatores de 0,01 pede $10^{-600}$, e não há expoente para isso. O produto não fica
> impreciso — ele vira `0.0` e leva a informação junto.

O chunk `underflow-demo` já demonstra isso; falta a frase que diz por quê.

### I9 — o callout do `float` diagnostica e não prescreve

O enquadramento está certo e foi elogiado: ataca a prática e não o autor, generaliza para a
família de três erros dos capítulos 5, 7 e 10, traz evidência medida e fecha com "o erro que
**você** vai cometer algum dia".

Mas o aluno sai sabendo que `==` é a pergunta errada e **sem saber qual é a certa**. Uma
linha: `assert math.isclose(model.predict(text), p_if_spam / (p_if_spam + p_if_ham))`, com a
observação de que `math.isclose` é da biblioteca padrão e existe desde o Python 3.5. É o
único parágrafo do callout que transfere para o código do próprio aluno.

### I10 — "ham" é usada duas seções antes de ser definida

A primeira ocorrência é `p_bitcoin_dado_ham`, na §1, sem glosa; a definição só chega na §3.
E "ham" é uma piada em inglês — o presunto do quadro do Monty Python que também deu nome ao
spam — à qual o leitor brasileiro não tem acesso nenhum.

Defina na §1, com a etimologia em meia frase.

### I11 — "vendorizar" é jargão de casa não declarado

Aparece três vezes na §5 e num título de subseção, sem nunca ser explicado. O capítulo 9, na
mesma situação, escreveu *"já está em `dados/iris.data`, commitado no repositório"* — legível
sem glossário. Troque por isso, ou defina o termo uma vez.

### I12 — a abertura fecha uma dívida e não abre nada; o fechamento não olha para frente

O `index.qmd` diz muito bem **o que este capítulo encerra** (a promessa do capítulo 8, a forma
do capítulo 9) e nada sobre o que ele **entrega aos seguintes**.

Há coisa real a dizer: é o primeiro modelo probabilístico do livro (devolve probabilidade,
não rótulo) e o primeiro em que treinar significa **comprimir os dados em parâmetros e jogar
o resto fora** — a postura de todo modelo daqui até o fim, incluindo a sequência de regressão
que vem a seguir.

E o capítulo termina no contraste com o capítulo 9 seguido de um `.callout-tip` recolhido: a
última coisa que o leitor vê aberta é um resumo para dentro. Um parágrafo final ligando
"contagens resumidas" a "coeficientes ajustados" deixaria o aluno em algum lugar.

### I13 — a classe inteira num chunk só, narrada antes de ser vista

O parágrafo da §3 descreve `__init__`, `train`, `_probabilities` e `predict` em prosa
corrida, e só então vêm 60 linhas de código de uma vez — com `predict`, a parte
conceitualmente difícil, caindo numa oração subordinada.

O capítulo 9 alterna código curto e prosa (`raw_majority_vote` → problema dos empates →
`majority_vote`). **Separe `predict` num chunk próprio**, com duas frases de entrada, e deixe
`__init__`/`train`/`_probabilities` juntos.

⚠️ **Cuidado ao dividir:** existe um teste (`test_nenhum_chunk_comeca_com_linha_indentada`)
que proíbe chunk começando com linha indentada, porque isso significa bloco partido entre
células — o IPython aceita e **não anexa o método à classe**, em silêncio. Foi exatamente o
bug que você já corrigiu neste capítulo. Se separar `predict`, ele precisa ser um `def` de
nível zero ou uma classe reaberta por inteiro. Rode `make teste` para confirmar.

---

## MENORES — corrija todos

**Prosa:**
- *"por trás dos panos"* (§3) → **"nos bastidores"**. ("Por baixo dos panos" existe, mas
  significa clandestinamente.)
- *"o *loop* percorre `self.tokens`"* (§3) → **"o laço percorre"**; o livro usa "laço" em todo
  lugar.
- *"não **te** diz nada"* (§2) → "não diz nada sobre"; quebra o registro de "você" do resto.
- *"é maior evidência de que"* (§5) → **"é mais uma evidência de que"**.
- §5: *"Vale calcular esse piso depois de separar treino e teste, adiante, e usá-lo como
  régua contra a qual o classificador de verdade precisa se provar melhor que nada"* — três
  adverbiais empilhados. → *"Calculamos esse piso adiante, depois de separar treino e teste,
  e o usamos como régua: é o mínimo que o classificador precisa superar."*
- *"os dois grandes **motores** desse número"* (§4) → "os dois termos que dominam esse número".
- **"de verdade" virou tique**: seis ocorrências na §5. Varie.

**Conteúdo:**
- O `.callout-note` que fecha a §2 é o **único callout decorativo do capítulo**: liga a
  suavização a "o capítulo sobre extração de atributos" **sem link** (o resto do livro sempre
  linka), e solta ***prior*** em inglês sem glosa, para o leitor que o próprio capítulo assume
  nunca ter formalizado probabilidade. Ou dê meia frase, ou corte.
- **O nome "suavização de Laplace" (ou regra da sucessão) nunca aparece.** Uma aposição de
  três palavras é o que separa o aluno de conseguir procurar o assunto sozinho.
- O exemplo da §2 usa $k = 1$; a classe da §3 tem `k: float = 0.5`; o `.callout-tip` da §3
  mostra `alpha=1.0` e o da §5 mostra `alpha=0.5`. Nada errado, mas **três valores diferentes
  sem uma palavra sobre como se escolhe *k***.
- `Counter` é citado na §3 como um dos "quatro que trabalham juntos", mas não é usado nessa
  seção (só na §5).
- Repetição quase literal de *"funciona bem o bastante para já ter sido usado de verdade em
  filtros de spam"* entre o `index.qmd` e a §2.
- **Deriva entre capítulos:** o callout da §4 diz que o `shuffle` do capítulo 5 "embaralha os
  lotes errados". O capítulo 5 é preciso ao dizer que ele embaralha os **índices de início**,
  não os pontos. Aperte a paráfrase para não afrouxar o que a fonte acertou.
- `index.qmd`: a abertura troca "the VP of Messaging has asked you" por "cabe a você
  construir um filtro", removendo o gatilho narrativo do Grus. É reescrita legítima, mas
  confira se os outros índices preservam mais desse enredo — a moldura DataSciencester é do
  livro.

---

## DESTACADO COMO BOM — mas não isento da sua atenção

**Isso não é lista de "não mexer".** No capítulo 5 deste livro, uma referência factualmente
falsa sobreviveu a três passadas por estar dentro de um box elogiado.

- A **§4 inteira** — chamada de a melhor seção do capítulo, e o momento em que a matemática
  vira aritmética visível ao refazer a conta à mão.
- O **`.conceito` da §3** sobre `log(1 - prob)` — o melhor callout do capítulo (e o I7 o
  deixa mais forte).
- O **callout do `float`** — modelar no enquadramento (ataca a prática, não o autor;
  generaliza para a família de três; traz evidência medida). O I9 só acrescenta a prescrição
  que falta.
- A **rampa geral**: uma palavra → vocabulário → código → teste de brinquedo → dados reais.
