---
layout: secao
---

<span class="parte">Parte 4 · 30 min</span>

# A saída e a perda

Um número, duas classes ou muitas classes: cada pergunta pede uma última camada.

---

# A última camada depende do que se quer prever

<Olho q="1 2" />

<table>
<thead><tr><th>a pergunta</th><th>neurônios de saída</th><th>ativação da saída</th><th>perda</th></tr></thead>
<tbody>
<tr v-click><td><b>Quanto?</b> (regressão)</td><td>1</td><td>nenhuma: ŷ = z</td><td>erro quadrático</td></tr>
<tr v-click><td><b>Sim ou não?</b> (duas classes)</td><td>1</td><td>sigmoide</td><td>entropia cruzada binária</td></tr>
<tr v-click><td><b>Qual delas?</b> (K classes)</td><td>K, um por classe</td><td><b>softmax</b></td><td>entropia cruzada categórica</td></tr>
</tbody>
</table>

<div v-click class="conceito">

As camadas ocultas não mudam. Trocar de problema é trocar a **saída** e a **perda**.

</div>

<div v-click class="fraco pequeno">

As duas primeiras linhas já apareceram: a regressão linear e o neurônio da Parte 2. Falta a terceira.

</div>

---

# Muitas classes: um neurônio de saída por classe

<Rede
  :camadas="[3, 4, 3]" :largura="700" :altura="270" :r="21"
  :textos="{ '2-0': 'z₁', '2-1': 'z₂', '2-2': 'z₃' }" :fora="{ '2-0': 'gato', '2-1': 'cachorro', '2-2': 'pássaro' }"
  :titulos="['entrada', 'oculta', 'saída']"
/>

<v-clicks>

- Cada neurônio de saída calcula um **placar** $z_k$ para a sua classe.
- Placar é qualquer número: negativo, maior que 1, não soma nada em especial.
- Queremos **probabilidades**: positivas e somando 1.

</v-clicks>

---

# A softmax transforma placares em probabilidades

<Olho q="1" />

$$
\hat{y}_k = \frac{e^{z_k}}{\displaystyle\sum_{j=1}^{K} e^{z_j}}
$$

<v-clicks>

1. **Exponencial** de cada placar: tudo fica positivo.
2. **Divide pela soma**: tudo passa a somar 1.

</v-clicks>

<div v-click class="conceito">

A ordem se mantém: o maior placar fica com a maior probabilidade. E a exponencial **estica** as diferenças.

</div>

---

# Na mão: a softmax de três placares

<Olho q="1" />

<table>
<thead><tr><th></th><th>gato</th><th>cachorro</th><th>pássaro</th><th>soma</th></tr></thead>
<tbody>
<tr><td>placar <i>z</i></td><td>2,0</td><td>1,0</td><td>0,1</td><td></td></tr>
<tr v-click><td>exponencial <i>e<sup>z</sup></i></td><td>7,389</td><td>2,718</td><td>1,105</td><td>11,212</td></tr>
<tr v-click><td>dividido pela soma: <b>ŷ</b></td><td class="ida">0,659</td><td class="ida">0,242</td><td class="ida">0,099</td><td>1</td></tr>
</tbody>
</table>

<div v-click>

O placar do gato era o **dobro** do placar do cachorro. A probabilidade ficou quase o **triplo**: $0{,}659 / 0{,}242 = 2{,}72$.

</div>

<div v-click class="fraco pequeno">

Esse fator é $e^{2 - 1} = e$: a softmax só enxerga a **diferença** entre os placares.

</div>

---
class: mexa
---

# Mexa nos placares

<Olho q="1 2" />

<SoftmaxExplora />

<div v-click class="preveja">

Se eu somar 1 aos três placares, o que acontece com as probabilidades?

</div>

<!--
Nada muda: a softmax só enxerga diferenças entre placares. Depois suba um placar só e mostre como ele
"rouba" probabilidade dos outros. Troque a classe certa clicando na coluna "resposta y".
-->

---

# A resposta certa vira um vetor com um único 1

<Olho q="2" />

Se a classe certa é "cachorro", a resposta é escrita assim (codificação *one-hot*):

$$
y = \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix} \begin{matrix} \leftarrow \text{gato} \\ \leftarrow \text{cachorro} \\ \leftarrow \text{pássaro} \end{matrix} \qquad\qquad \hat{y} = \begin{bmatrix} 0{,}659 \\ 0{,}242 \\ 0{,}099 \end{bmatrix}
$$

<div v-click>

**Entropia cruzada categórica:**

$$
L = -\sum_{k=1}^{K} y_k \ln \hat{y}_k
$$

</div>

<div v-click class="conceito">

Como só um $y_k$ vale 1, a soma inteira se reduz a **um termo**: $L = -\ln$ da probabilidade dada à classe certa.

</div>

---

# Na mão: a mesma previsão, duas respostas possíveis

<Olho q="2" />

A rede previu $\hat{y} = (0{,}659;\ 0{,}242;\ 0{,}099)$.

<div class="cols">
<div v-click>

**Se a resposta era "gato":**

$$
L = -\ln 0{,}659 = 0{,}417
$$

A rede apostou na classe certa. Perda baixa.

</div>
<div v-click>

**Se a resposta era "cachorro":**

$$
L = -\ln 0{,}242 = 1{,}417
$$

A rede apostou em outra. Perda alta.

</div>
</div>

<div v-click class="fraco">

É a mesma perda da Parte 2. Com duas classes, softmax e entropia categórica voltam a ser sigmoide e entropia binária.

</div>

---

# O erro da saída é sempre "previsto menos certo"

<Olho q="3" />

A derivada da perda em relação ao **placar** $z_k$ de cada neurônio de saída:

<table>
<thead><tr><th>saída + perda</th><th>∂L/∂z<sub>k</sub></th></tr></thead>
<tbody>
<tr v-click><td>sem ativação + erro quadrático ½(ŷ − y)²</td><td class="volta">ŷ − y</td></tr>
<tr v-click><td>sigmoide + entropia cruzada binária</td><td class="volta">ŷ − y</td></tr>
<tr v-click><td>softmax + entropia cruzada categórica</td><td class="volta">ŷ<sub>k</sub> − y<sub>k</sub></td></tr>
</tbody>
</table>

<div v-click class="conceito">

Não é coincidência: cada perda é o par natural da sua ativação, e a conta sempre se simplifica do jeito que vimos na Parte 2.

</div>

<div v-click>

No exemplo, com resposta "cachorro": $\hat{y} - y = (0{,}659;\ 0{,}242 - 1;\ 0{,}099) = (0{,}659;\ {-}0{,}758;\ 0{,}099)$.

</div>

---
class: codigo-menor
---

# Em código: softmax e entropia cruzada

<<< @/snippets/s_softmax.py {1-3|5-6|8|9|10|all}

<Saida v-click nome="s_softmax" />

---
class: sua-vez
---

# Softmax no papel

Uma rede deu os placares $z = (3;\ 1;\ 0)$. Use $e^3 = 20{,}09$, $e^1 = 2{,}72$ e $e^0 = 1$.

1. Calcule as três probabilidades.
2. A classe certa era a **primeira**. Qual é a perda? (Use $\ln 0{,}844 = -0{,}170$.)
3. Qual é o vetor de erro $\hat{y} - y$?

<div v-click class="conta">

Soma: $20{,}09 + 2{,}72 + 1 = 23{,}81$. Probabilidades: $(0{,}844;\ 0{,}114;\ 0{,}042)$.

</div>

<div v-click class="conta">

Perda: $-\ln 0{,}844 = 0{,}170$. Erro: $(0{,}844 - 1;\ 0{,}114;\ 0{,}042) = (-0{,}156;\ 0{,}114;\ 0{,}042)$.

</div>
