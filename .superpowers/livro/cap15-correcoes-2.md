# Capítulo 15 — Redes Neurais: correções, segunda rodada

A revisão didática não achou **nenhum Crítico** e chamou o capítulo de forte, com os quatro
"Na prática" entre os melhores do livro. **Você não vai reescrever nada.** São sete Importantes
e cinco Menores, quase todos de uma frase.

**Comece pelo I1: ele conserta um erro que veio do meu contrato anterior.**

---

## Importantes

### I1 — "Distância" é a palavra errada, e fui eu que a escrevi

`04-exemplo-fizz-buzz.qmd:240`. A rodada anterior trocou a implicação falsa ("acertar 100% do
treino condena o modelo") por um critério novo: a **distância** entre treino e teste. O critério
não discrimina os casos que o próprio parágrafo apresenta.

| modelo | treino | teste | |
|---|---|---|---|
| árvore sem poda | 99,7% | 82,4% | **cai** 17,3 |
| árvore prof. 2 | 85,0% | 100% | **sobe** 15,0 |

As duas distâncias são parecidas; o que as separa é o **sinal**. Troque a palavra: o que se lê é
a **queda** do treino para o teste. A árvore sem poda cai 17 pontos; a de profundidade 2 não
cai, **sobe**; a rede deste capítulo cai menos de dois. Aí o exemplo discrimina, e a frase final
("o modelo com o melhor número de treino era o pior dos dois") continua valendo.

**Confira os quatro números contra `content/cap14/06-florestas-aleatorias.qmd`** antes de
escrever — eles são de lá.

### I2 — A §2 contradiz o "Na prática" da §1

`01:169` diz que o `Perceptron` da biblioteca tem "regra de treino própria"; `02:22` diz que
"sobre a função degrau, nada do Capítulo 5 se aplica". O aluno atento pergunta: então **como** a
biblioteca treina um perceptron?

Meia linha em `02`, depois do `.conceito`, fecha e ainda valoriza a §1: o perceptron histórico é
treinado por uma regra própria — corrigir os pesos no exemplo errado —, que **não** é gradiente
descendente, e que existe justamente porque o gradiente não estava disponível.

### I3 — A nota de índice da §3 é meio-verdadeira sobre o código

`03:93` diz "o `i` que percorre `hidden_outputs` é este $h$". Mas o código usa `i` nos **dois**
papéis: `output_deltas[i]` em `:70` enumera **saída**; `:77` e `:81` enumeram **escondido**. Quem
conferir `output_grads` com a nota na mão erra.

Reescreva dizendo qual `i` é qual, e nomeando o problema: o código reaproveita a letra, a
matemática não.

### I4 — Falta ver um número atravessar a rede, e esta é a maior alavanca da seção mais difícil do livro

Entre `03:171` e `03:187` toda a máquina já está carregada — rede aleatória e
`sqerror_gradients`. **Cinco linhas** imprimindo `output_deltas` e os dois `hidden_deltas` para
`x = [1, 0]` deixariam o aluno **ver** a culpa chegar menor atrás e proporcional ao peso da
conexão.

Hoje a seção vai do verbal e do algébrico direto para 20.000 epochs. E o gancho já existe:
`:173` manda "guardar a ordem de grandeza".

### I5 — O que a rede **ganha** é afirmado duas vezes e nunca sustentado

O índice (`:22`) e `04:281` dizem que ela "resolve um problema que nenhum dos dois resolveria" —
e o texto nunca mostra por quê. Duas meias-linhas resolvem, **por motivos diferentes**:

- **Regressão:** uma regressão sobre dez bits é uma soma ponderada de bits, e nenhuma soma
  ponderada de bits separa os múltiplos de 3. É literalmente o argumento das quatro desigualdades
  da §1, aplicado a $\{0,3\}$ contra $\{1,2\}$ — o capítulo já construiu a ferramenta.
- **Árvore:** profundidade 10 é memorização, e os padrões de 1 a 100 nunca aparecem no treino.

### I6 — Mostre os pesos ilegíveis, em vez de afirmar que são

`04:277` diz "não há resposta" sem exibir nada. A §3 **imprimiu** os pesos, e eles liam OU e E.
A §4 deveria imprimir dois dos 25 vetores de 11 números logo antes do `.conceito`. O contraste
com a §3 faz o trabalho sozinho, sem retórica — e é o arco de interpretabilidade do livro
inteiro aterrissando numa tela de números sem sentido.

### I7 — `04:270` desmente `04:279`

`:270` diz que a rede "montou, na camada escondida, alguma combinação desses bits que **aproxima
a soma alternada e o ciclo módulo 4**". Nove linhas depois, `:279` diz que não há como saber o
que ela calcula. É a mesma afirmação central nos dois sentidos.

Corte o mecanismo: alguma combinação que **funciona** — não necessariamente a soma alternada nem
o ciclo módulo 4 de que o capítulo falou no início; apenas algo que acerta 96 dos 100.

### I8 — O treino da §3 é gradiente descendente **estocástico**, e o capítulo não o nomeia

`03:185` diz "O treino é gradiente descendente comum. A única diferença é que agora há vários
vetores de parâmetros". Não é a única: o laço dá **um passo por exemplo**, que é o gradiente
descendente estocástico batizado em
`content/cap05/06-minibatch-e-estocastico.qmd:111` — que inclusive já observa que "um epoch
estocástico dá um passo por ponto".

Nomeá-lo custa meia linha e paga três dívidas: liga ao capítulo 5, explica por que 20.000 epochs
sobre 4 exemplos são 80.000 passos, e explica o serrilhado no fim da curva de
`fig-perda-fizz-buzz`.

---

## Menores

- **M1** — Na §4, `epoch_loss` é somado com pesos que **mudam durante o epoch**: não é a perda de
  uma rede fixa. Meia linha evita a leitura errada do gráfico.
- **M2** — O índice (`:13`) promete que "**cada** seção existe por causa de um limite da
  anterior", mas a §4 não é limite da §3 — é aplicação. Ajuste a promessa.
- **M3** — O capítulo termina numa boa frase (`:283`), e deve continuar terminando nela. Mas o
  único aceno ao capítulo 16 no texto corrido está dentro do callout do softmax. Uma frase de
  passagem depois do `.conceito`, **sem** roubar a última linha.
- **M4 — prosa**, com a redação proposta:
  - `04:11` "demonstra habilidade extrema em programação" é tradução dura de *extreme programming
    skill* → "Ele está convencido de que quem resolve isso é um programador excepcional."
  - `02:15` "vamos aplicar em vez dela uma aproximação suave" (ordem torta) → "no lugar dela vamos
    aplicar uma **aproximação suave** do degrau."
  - `01:24` "O `bias` é um deslocamento" e `01:39` "o viés" nunca são ligados — e **é a primeira
    vez no livro que "viés" não significa o viés estatístico** (o capítulo 12 chama o intercepto
    de "termo constante"). Ligue os dois e desarme a colisão, como `cap02:45` já faz com outro
    par: nada a ver com o viés do compromisso viés-variância do capítulo 8.
  - `01:7` usa `*n*` (itálico markdown) onde o resto do capítulo usa `$...$`.
  - O título `## Os quatro erros` precede um chunk que examina 4, 70 e **15** — e 15 não é erro. →
    "## Olhando os erros de perto".
- **M5** — A §3 tem **nove** caixas, e é a seção mais difícil do livro: a fragmentação cobra. A
  candidata a virar prosa é "A semente não é opcional" (`:175`) — duas frases dela são regra geral
  da casa, já dita em `cap02:49`. Só o parágrafo sobre inicializações levarem a **soluções**
  diferentes é específico daqui.

---

## Não mexa nisto

Os quatro "Na prática" (o da §4, que mostra a biblioteca devolvendo 0,53 por parar no platô, é
conteúdo puro), a metáfora da **culpa** na §3 — que a revisão chamou de melhor coisa da seção —,
e a última frase do capítulo.
