# Capítulo 16 — Deep Learning: correções

Duas revisões independentes. A de conteúdo **reproduziu todos os números** e não achou nenhum
Crítico — verificou até o transplante do XOR comparando `float.hex()`, e os valores são
**idênticos bit a bit** nos dois caminhos. A didática chamou os "Na prática" de "o melhor
conjunto que vi neste livro" e disse que sete das oito seções acertam o alvo de "cada abstração
aparece resolvendo uma dor concreta do capítulo 15".

**Você não vai reescrever o capítulo.** 1 Crítico, 6 Importantes, 12 Menores.

---

## Crítico

### C1 — "É a última coisa que este livro constrói" é falso, e é sintoma

`08-exemplo-mnist.qmd:9`. O **capítulo 17** constrói k-means e clustering hierárquico do zero,
depois deste.

E o erro denuncia algo maior: **o capítulo 16 não menciona o 17 em lugar nenhum** — nem no
`index.qmd`, nem no fecho "O fim do arco". É o **único capítulo do livro que não passa o
bastão**, enquanto `content/cap17/index.qmd:12` reaproveita explicitamente esta página ("o dígito
era um 7") e o `content/cap15/index.qmd` entrega o leitor a este capítulo pelo nome.

Duas correções:

1. Em `08:9`: "É a última coisa que **este capítulo** constrói, e a mais completa: ela usa tudo."
2. No fim de "O fim do arco", uma frase entregando o capítulo 17 — e o pivô que ele representa
   merece ser nomeado: todos os dezesseis capítulos até aqui tiveram um gabarito (a flor era
   setosa, o dígito era um 7); o capítulo 17 tira o gabarito.

---

## Importantes

### I1 — O dropout é a única abstração que entra porque o Grus a introduz

A §7 o apresenta como regularização contra sobreajuste, e liga ao capítulo 8 e à §12.8 —
corretamente. Mas **o capítulo nunca mostra sobreajuste nem mede que o dropout ajude**. Com
10.000 imagens e 3 passadas o modelo não chega perto de sobreajustar (treino corrente 0,9020
contra teste 0,8815), e não há comparação com e sem. A §8 mede o **bug** de deixá-lo ligado na
avaliação, o que prova que ele faz algo — não que ele serve.

**A postura da casa é a franqueza**, e ela cabe em três linhas: com três passadas em 10.000
imagens este modelo ainda não sobreajusta nada, então o dropout aqui não tem o que consertar;
ele está na rede porque o livro-texto o põe ali, e porque é o **comportamento** dele — não o
benefício — que esta seção quer medir.

### I2 — O capítulo 5 nunca é linkado, e o `gradient_step` aparece nu

`05-perda-e-otimizacao.qmd:74` traz `gradient_step(theta, grad, -learning_rate)` como se fosse
folclore. É o lugar exato da ligação — o `gradient_step` do
[Capítulo 5](../cap05/index.qmd), que dava um passo num **vetor** de parâmetros —, e o parágrafo
seguinte, que diz que agora há muitos tensores, vira a continuação natural. O mesmo em `:163`.

### I3 — A afirmação sobre o `optim.SGD` do PyTorch está imprecisa, e eu medi

`05-perda-e-otimizacao.qmd:348` diz "O `optim.SGD` com `momentum=0.9` **é o nosso** `Momentum`".

O nosso faz `u = μu + (1−μ)g` (`scratch/deep_learning.py:314`), que converge para **1×** o
gradiente. O PyTorch, com `dampening=0`, faz `buf = μ·buf + g`, que converge para **10×**.
**Para a mesma taxa de aprendizado, o passo efetivo do PyTorch é dez vezes maior.**

Mesma ideia, convenção diferente. Acrescente a ressalva — e note que este é um callout "Na
prática", que é justamente a parte do livro que **nenhuma renderização verifica**, porque os
chunks não executam.

### I4 — A §7 imprime uma tabela e não a lê

A saída real vai 0,530 → 0,460 → **0,340** (epoch 25) → 0,730 → 0,970 no teste: a acurácia
**piora por 25 epochs** antes de disparar. A §6 dedica três parágrafos ao platô; a §7 não
comenta nada, e o aluno fica com um número que contradiz "muito mais rápido".

Dois períodos depois do chunk fecham: a rede passa os primeiros epochs reorganizando as
fronteiras entre quatro classes antes de qualquer uma delas acertar, e a escada da §6 reaparece
aqui invertida.

### I5 — A §1 pede emprestada a motivação do Grus, e a verdadeira está na §5

O tensor é justificado por "um lote de imagens coloridas é um arranjo de quatro dimensões" — e
**este livro nunca passa de duas** (o MNIST já chega achatado em 784).

O payoff verdadeiro existe, e é do próprio livro: em `05-perda-e-otimizacao.qmd`,
`GradientDescent.step` percorre `zip(params, grads)` onde `params` traz a matriz `[30,784]` **e**
o vetor `[30]` juntos, e um único `tensor_combine` recursivo atende os dois **sem um `if`**.
Diga isso na seção "Cinco funções, e o capítulo inteiro" — é a dor concreta que a recursão paga.

### I6 — "Exatamente o mesmo resultado" é literalmente falso

`08-exemplo-mnist.qmd:373` — "Embaralhar as 784 colunas de todas as imagens da mesma forma
produziria **exatamente** o mesmo resultado de treino."

Com semente fixa, `random_tensor(30, 784)` sorteia os pesos numa ordem fixa; permutar as
entradas **sem** permutar as colunas dos pesos dá outra inicialização. O resultado é
estatisticamente equivalente, não idêntico. **O argumento pedagógico está certo**; a palavra em
negrito é que não. Troque por "o mesmo resultado esperado" ou "nada mudaria no que o modelo pode
aprender".

---

## Menores

- **M1** — `01-o-tensor.qmd:181`: o título "## **Cinco** funções, e o capítulo inteiro"
  contradiz as **seis** listadas duas linhas abaixo, o "essas seis funções" de `:185` e o "seis
  funções de três linhas" de `:213`. **O título vai para o índice lateral.**
- **M2** — A decisão dos **3 epochs** nunca é explicada. A tabela deixa 0,8595 visível e a seção
  anterior deixa 0,8620, mas o leitor precisa cruzar duas páginas sozinho. Diga a frase — "com
  duas passadas a rede profunda ainda perdia para a linear" —, que é exatamente a lição de
  orçamento que o capítulo vende.
- **M3** — Custo de render: o texto diz ~4,5 min, que é a soma dos cronômetros impressos. A
  revisão mediu o que **não** é cronometrado (imports, preparação, avaliações, sorteios,
  figuras, 9 kernels) e chegou a **~5 min**. Mesma ordem, mas é o CI que paga a cada push.
  Ajuste o número.
- **M4** — `08:325`: "O custo por imagem **triplicou**" — medido 6,15/2,30 = **2,67×**. Os
  números que a própria frase cita estão certos; só o verbo arredonda para cima.
- **M5** — `04-redes-como-sequencia-de-camadas.qmd:158`: "aplicaria o passo àquele tensor duas
  vezes por exemplo, **com dois gradientes diferentes**, e o segundo sobrescreveria o `w_grad` do
  primeiro antes de ser usado" — as duas metades se contradizem na superfície. Na execução real,
  quando `step` roda, as duas entradas de `grads()` já devolvem o **mesmo** tensor. Reordene.
- **M6** — `02:122` e `03:28` repetem a explicação das dezoito chamadas `plt.*`. Uma vez é
  honestidade sobre o encanamento; duas é contabilidade. Encolha a da §3 para um ponteiro.
- **M7** — `07:253`: "**Três** erros em cem, e eles não são do mesmo tipo" e o texto lê dois. O
  n = 4 (0,892 em "buzz", errado) é um terceiro tipo útil: erro confiante **e** com segunda
  hipótese viva.
- **M8** — `index.qmd:13` promete PyTorch **e** TensorFlow, e nenhum "Na prática" mostra
  Keras/TF. O lugar barato é a §4, onde `keras.Sequential([...])` já é citado em prosa — duas
  linhas de código fecham a promessa, e o Keras é a biblioteca que o desenho do Grus copia.
- **M9** — `08:271-282`: o `Dropout` entra **entre** `Linear` e `Tanh`, posição incomum (o usual
  é depois da ativação). Quem leu a §7 vai reparar. Uma frase: é o que o livro-texto faz, e para
  a `Tanh` a diferença é pequena porque `tanh(0) = 0`.
- **M10** — `08:82`: "Setenta mil imagens em cerca de um segundo" — a saída diz **0,65 s**. "Em
  menos de um segundo" é mais forte **e** é o número.
- **M11** — `index.qmd:62`: "o Keras — a biblioteca em que **a biblioteca** deste capítulo é
  vagamente inspirada" repete o substantivo em dez palavras. → "…em que o **desenho** deste
  capítulo se inspira".
- **M12** — `06-outras-funcoes-de-ativacao.qmd:9`: "e o deslocamento se acumula camada após
  camada" é extensão nossa; o Grus só diz que `sigmoid(0) = 1/2` produz saída positiva. O
  argumento está correto (ativação não centrada em zero), mas não está no livro-texto — ou
  marque como observação nossa, ou corte.

---

## Não mexa nisto

- **O transplante dos pesos do XOR** (§4) — verificado bit a bit por `float.hex()`. É a melhor
  prova possível de que a refatoração preserva o modelo.
- **Os dois laços de treino lado a lado** (§5) e a §2 inteira, que a revisão chamou de modelo do
  capítulo ("só faz sentido depois de doer, então vale recuperar a dor").
- **O tratamento do erro do `random_normal`** — mede, recusa consertar pelo motivo certo, e
  amarra à confissão do próprio Grus. A especulação de `03:114` está hedgeada com "provavelmente"
  e no lugar certo.
- **O orçamento de render como conteúdo**, incluindo "Isso é o assunto, não um contratempo" e o
  callout "Por que 300 epochs, e não 1.000".
- **A leitura do bug do dropout na §8**: "O modelo está certo; a medição é que está errada."
