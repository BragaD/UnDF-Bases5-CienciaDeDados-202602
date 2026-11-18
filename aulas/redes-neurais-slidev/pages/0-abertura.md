---
clicks: 4
---

# Como uma máquina aprende a ler um dígito escrito à mão?

<img class="fig" src="/fig/digitos.svg" style="width: 860px" />

<div class="cols" style="margin-top: 8px">
<div>

<v-clicks>

- Ninguém escreveu a regra "um 7 é um traço em cima e outro inclinado".
- A máquina viu **exemplos com resposta** e ajustou números.

</v-clicks>

</div>
<div>

<div v-click class="conceito">

No fim da aula, a rede que faz isso estará escrita por você, em poucas dezenas de linhas.

</div>

<div v-click class="fraco pequeno">

Ela acerta 435 de 450 dígitos que nunca viu.

</div>

</div>
</div>

<!--
Abertura. Não explique nada ainda: a pergunta fica no ar e a resposta é a Parte 6.
O número 435 de 450 sai da execução da Parte 6 (450 imagens de teste, 15 erradas).
-->

---
clicks: 4
---

# Uma rede neural é uma função com botões

<Cadeia :caixas="['entrada x', 'rede f(x; w, b)', 'saída ŷ']" :ida="['pixels, medidas, palavras', 'um número, uma classe']" :largura="800" :passo="$clicks + 2" />

<v-clicks>

- Os **botões** são números: os **pesos** $w$ e os **vieses** $b$.
- Com os botões numa posição, a rede **prevê**. Com outra, prevê outra coisa.
- **Aprender** é girar os botões, um pouco de cada vez, até a previsão errar menos.

</v-clicks>

<div v-click class="conceito">

A aula inteira responde a uma pergunta: **para que lado, e quanto, girar cada botão?**

</div>

<!--
A imagem dos botões volta nas seis partes.
-->

---

# Ao final da aula, você consegue

<v-clicks>

1. **Calcular à mão** a previsão de um neurônio e de uma rede pequena.
2. **Medir o erro** com a função de perda certa para cada tipo de saída.
3. **Derivar** a correção de um peso pela regra da cadeia.
4. **Fazer a volta** (*backpropagation*) numa rede de várias camadas, no papel.
5. **Programar** tudo isso em `numpy` e treinar uma rede que reconhece dígitos.

</v-clicks>

<div v-click class="fraco pequeno">

Cada parte tem a ideia, a fórmula, a conta com números, o código e um exercício no papel.

</div>

---

# As quatro perguntas

Todo modelo desta aula, do neurônio sozinho à rede de muitas camadas, responde às mesmas quatro.

<div class="quatro">
<div v-click>

<span class="num">1</span> **Prever**

Dada a entrada, que conta produz a saída?

</div>
<div v-click>

<span class="num">2</span> **Medir**

Quão longe a saída ficou da resposta certa?

</div>
<div v-click>

<span class="num">3</span> **Atribuir**

Quanto do erro é culpa de cada peso?

</div>
<div v-click>

<span class="num">4</span> **Corrigir**

Como mudar cada peso para errar menos?

</div>
</div>

<div v-click style="margin-top: 14px">

<span class="ida">Azul</span> é a **ida**: o que a rede calcula. <span class="volta">Laranja</span> é a **volta**: o erro e a correção.

</div>

---

# O caminho da aula

<div class="mapa">
<div v-click>

<span class="t">1 · O perceptron</span>

Um neurônio, a regra de correção e o problema que ele não resolve.

<span class="min">50 min</span>

</div>
<div v-click>

<span class="t">2 · O neurônio que desce o gradiente</span>

Sigmoide, função de perda e a regra da cadeia num neurônio só.

<span class="min">45 min</span>

</div>
<div v-click>

<span class="t">3 · A rede multicamada</span>

Camadas ocultas, a ida passo a passo e as funções de ativação.

<span class="min">50 min</span>

</div>
<div v-click>

<span class="t">4 · A saída e a perda</span>

Regressão, duas classes, muitas classes: softmax e entropia cruzada.

<span class="min">30 min</span>

</div>
<div v-click>

<span class="t">5 · Backpropagation</span>

O erro de volta, camada por camada, na mão e em código.

<span class="min">75 min</span>

</div>
<div v-click>

<span class="t">6 · Treinar de verdade</span>

Lotes, taxa de aprendizado, dígitos escritos à mão e as bibliotecas.

<span class="min">40 min</span>

</div>
</div>
