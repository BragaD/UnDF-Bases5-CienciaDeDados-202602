---
layout: secao
---

<span class="parte">Parte 5 · 75 min</span>

# Backpropagation

O erro aparece na saída. A culpa está espalhada pela rede inteira.

---

# Quanta culpa tem um peso lá do começo?

<Olho q="3" />

<Rede
  :camadas="[2, 2, 1]" :largura="680" :altura="240" :quentes="['0-0-0']" :so-arestas="['0-0-0', '1-0-0', '1-1-0', '0-1-0', '0-0-1', '0-1-1']"
  :textos="{ '0-0': 'x₁', '0-1': 'x₂', '1-0': 'h₁', '1-1': 'h₂', '2-0': 'ŷ' }"
  :pesos="{ '0-0-0': '0,1 → ?' }" :fora="{ '2-0': 'ŷ = 0,584' }" :fora-q="{ '2-0': 'y = 1' }"
/>

<v-clicks>

- A perda compara $\hat{y}$ com $y$ **na saída**.
- O peso em laranja não toca a saída: ele muda $h_1$, que muda $\hat{y}$, que muda $L$.
- Queremos $\dfrac{\partial L}{\partial w}$ para **todos** os pesos, inclusive esse.

</v-clicks>

---

# A saída ingênua: mexer em cada peso e medir

<Olho q="3" />

Some um $\varepsilon$ pequeno a **um** peso, refaça a ida e veja quanto a perda mudou:

$$
\frac{\partial L}{\partial w} \approx \frac{L(w + \varepsilon) - L(w)}{\varepsilon}
$$

<v-clicks>

- Funciona, e não exige cálculo nenhum.
- Custa **uma ida completa por peso**.
- Na rede de 13.002 parâmetros: 13.002 idas para dar **um** passo.

</v-clicks>

<div v-click class="conceito">

O **backpropagation** entrega as mesmas derivadas, de todos os pesos, com **uma ida e uma volta**.

</div>

---
clicks: 2
---

# Toda conta é um grafo de contas pequenas

<Olho q="1" />

Exemplo sem rede nenhuma: $f = (x + y) \cdot z$, com $x = -2$, $y = 5$, $z = -4$.

<GrafoConta :passo="$clicks" />

<div class="centro" style="min-height: 2em">
<span v-if="$clicks === 0">A <b>ida</b> calcula da esquerda para a direita. Quanto vale q = x + y?</span>
<span v-if="$clicks === 1">q = −2 + 5 = 3. E f = q · z?</span>
<span v-if="$clicks === 2">f = 3 · (−4) = −12. A ida acabou, e cada seta guardou o seu valor.</span>
</div>

---
clicks: 5
clicksStart: 2
---

# A volta percorre o mesmo grafo ao contrário

<Olho q="3" />

<GrafoConta :passo="$clicks" />

<div class="centro" style="min-height: 3.2em">
<span v-if="$clicks === 2">Pergunta: se cada entrada subir um pouco, quanto <b>f</b> muda?</span>
<span v-if="$clicks === 3">Começa no fim: ∂f/∂f = 1.</span>
<span v-if="$clicks === 4">Produto f = q · z: a derivada em relação a um fator é <b>o outro fator</b>.</span>
<span v-if="$clicks === 5">Soma q = x + y: a derivada local é 1, então o −4 que chegou <b>passa igual</b> para x e y.</span>
</div>

---

# A regra de toda a volta

<Olho q="3" />

<div class="grande centro">

<span class="volta">derivada que **chega** da frente</span> &nbsp;×&nbsp; **derivada local** da conta

</div>

<v-clicks>

- Cada nó só precisa saber a **sua** derivada local, a de uma conta simples.
- O que chega da frente já resume tudo o que acontece dali até a perda.
- Por isso a ordem é **de trás para a frente**: quando um nó é visitado, o que ele precisa já foi calculado.

</v-clicks>

<div v-click class="conceito">

É a regra da cadeia da Parte 2, organizada para **nunca calcular a mesma coisa duas vezes**.

</div>

---

# Na rede, a volta calcula o erro de cada neurônio

<Olho q="3" />

O **erro de um neurônio** é quanto a perda muda quando a soma $z$ dele muda:

$$
\delta^{[l]}_j = \frac{\partial L}{\partial z^{[l]}_j}
$$

<v-clicks>

- Na **saída**, já conhecemos: $\delta = \hat{y} - y$ (Partes 2 e 4).
- Nas **camadas ocultas**, é o que falta descobrir.
- Com o $\delta$ de um neurônio na mão, os gradientes dos pesos dele saem numa multiplicação.

</v-clicks>

<div v-click class="fraco pequeno">

$\delta$ é a letra grega delta. É a quantidade que "anda para trás" e dá nome ao algoritmo.

</div>

---

# O ponto de partida: a ida já feita

<Olho q="1 2" />

<Rede
  :camadas="[2, 2, 1]" fortes :largura="700" :altura="280"
  :textos="{ '0-0': 'x₁', '0-1': 'x₂', '1-0': 'h₁', '1-1': 'h₂', '2-0': 'ŷ' }"
  :pesos="{ '0-0-0': '0,1', '0-1-0': '0,3', '0-0-1': '−0,2', '0-1-1': '0,4', '1-0-0': '0,5', '1-1-0': '−0,3' }"
  :fora="{ '0-0': '0,5', '0-1': '1', '1-0': 'a = 0,611', '1-1': 'a = 0,550', '2-0': 'ŷ = 0,584' }"
  :titulos="['x', 'camada 1', 'camada 2']"
/>

<div class="centro">

Resposta $y = 1$, perda $L = 0{,}537$. A volta **reusa** os valores em azul: por isso a ida os guarda.

</div>

---

# Volta, passo 1: o erro do neurônio de saída

<Olho q="3" />

<Rede
  :camadas="[2, 2, 1]" :largura="640" :altura="220" :so-arestas="[]" :nos-q="['2-0']"
  :textos="{ '0-0': 'x₁', '0-1': 'x₂', '1-0': 'h₁', '1-1': 'h₂', '2-0': 'ŷ' }"
  :fora="{ '1-0': 'a = 0,611', '1-1': 'a = 0,550', '2-0': 'ŷ = 0,584' }" :fora-q="{ '2-0': $clicks >= 1 ? 'δ = −0,416' : 'δ = ?' }"
/>

<div v-click>

$$
\delta^{[2]} = \hat{y} - y = 0{,}584 - 1 = -0{,}416
$$

</div>

<div v-click>

Negativo: a soma $z^{[2]}$ ficou **baixa demais**. A previsão precisa subir.

</div>

---

# Volta, passo 2: os gradientes da camada de saída

<Olho q="3" />

<Rede
  :camadas="[2, 2, 1]" :largura="640" :altura="220" :so-arestas="['1-0-0', '1-1-0']" :quentes="['1-0-0', '1-1-0']" :nos-q="['2-0']" :t-peso="0.5"
  :textos="{ '0-0': 'x₁', '0-1': 'x₂', '1-0': 'h₁', '1-1': 'h₂', '2-0': 'ŷ' }"
  :pesos="$clicks >= 2 ? { '1-0-0': '−0,254', '1-1-0': '−0,229' } : $clicks >= 1 ? { '1-0-0': '−0,254', '1-1-0': '?' } : { '1-0-0': '?', '1-1-0': '?' }"
  :fora="{ '1-0': 'a = 0,611', '1-1': 'a = 0,550' }" :fora-q="{ '2-0': 'δ = −0,416' }"
/>

Erro do neurônio de **chegada** vezes ativação do neurônio de **partida**:

<div v-click>

$$
\frac{\partial L}{\partial w^{[2]}_1} = \delta^{[2]} \cdot a^{[1]}_1 = -0{,}416 \cdot 0{,}611 = -0{,}254
$$

</div>

<div v-click>

$$
\frac{\partial L}{\partial w^{[2]}_2} = -0{,}416 \cdot 0{,}550 = -0{,}229 \qquad\qquad \frac{\partial L}{\partial b^{[2]}} = \delta^{[2]} = -0{,}416
$$

</div>

<div v-click class="fraco pequeno">

É a conta da Parte 2, com $a^{[1]}$ no lugar de $x$.

</div>

---

# Volta, passo 3: o erro atravessa para a camada oculta

<Olho q="3" />

<Rede
  :camadas="[2, 2, 1]" :largura="640" :altura="230" :so-arestas="['1-0-0', '1-1-0']" :quentes="['1-0-0', '1-1-0']" :nos-q="['1-0', '1-1']" volta :t-peso="0.5"
  :textos="{ '0-0': 'x₁', '0-1': 'x₂', '1-0': 'h₁', '1-1': 'h₂', '2-0': 'ŷ' }"
  :pesos="{ '1-0-0': '× 0,5', '1-1-0': '× (−0,3)' }"
  :fora-q="{ '2-0': 'δ = −0,416', '1-0': 'δ = ?', '1-1': 'δ = ?' }"
/>

<div v-click>

O erro volta **pelo mesmo peso** por onde a ativação foi, e passa pela derivada da ativação:

$$
\delta^{[1]}_j = \underbrace{w^{[2]}_j\, \delta^{[2]}}_{\text{o que chega da frente}} \cdot \underbrace{\sigma'\big(z^{[1]}_j\big)}_{\text{derivada local}}
$$

</div>

<div v-click class="fraco pequeno">

É a regra do grafo: derivada que chega da frente × derivada local.

</div>

---

# Volta, passo 3: os números

<Olho q="3" />

A derivada local da sigmoide é $a\,(1 - a)$, com a ativação que a ida guardou.

<div v-click>

**Neurônio $h_1$:**

$$
\delta^{[1]}_1 = \underbrace{0{,}5 \cdot (-0{,}416)}_{-0{,}208} \cdot \underbrace{0{,}611 \cdot (1 - 0{,}611)}_{0{,}238} = -0{,}049
$$

</div>

<div v-click class="preveja">

O peso de $h_2$ para a saída é negativo ($-0{,}3$). Que sinal vai ter o erro de $h_2$?

</div>

<div v-click>

**Neurônio $h_2$:**

$$
\delta^{[1]}_2 = \underbrace{-0{,}3 \cdot (-0{,}416)}_{0{,}125} \cdot \underbrace{0{,}550 \cdot (1 - 0{,}550)}_{0{,}248} = 0{,}031
$$

</div>

<div v-click class="conceito">

Para $\hat{y}$ subir, $h_2$ precisa **descer**. O sinal do erro inverteu sozinho.

</div>

---

# Volta, passo 4: os gradientes da camada oculta

<Olho q="3" />

<Rede
  :camadas="[2, 2, 1]" :largura="640" :altura="230" :so-arestas="['0-0-0', '0-1-0', '0-0-1', '0-1-1']" :quentes="['0-0-0', '0-1-0', '0-0-1', '0-1-1']" :nos-q="['1-0', '1-1']" :t-peso="0.3"
  :textos="{ '0-0': 'x₁', '0-1': 'x₂', '1-0': 'h₁', '1-1': 'h₂', '2-0': 'ŷ' }"
  :pesos="$clicks >= 1 ? { '0-0-0': '−0,025', '0-1-0': '−0,049', '0-0-1': '0,015', '0-1-1': '0,031' } : { '0-0-0': '?', '0-1-0': '?', '0-0-1': '?', '0-1-1': '?' }"
  :fora="{ '0-0': '0,5', '0-1': '1' }" :fora-q="{ '1-0': 'δ = −0,049', '1-1': 'δ = 0,031' }"
/>

A mesma receita do passo 2: erro de chegada vezes ativação de partida. Aqui a partida é $x$.

<div v-click>

$$
\frac{\partial L}{\partial W^{[1]}} = \begin{bmatrix} \delta^{[1]}_1 x_1 & \delta^{[1]}_1 x_2 \\ \delta^{[1]}_2 x_1 & \delta^{[1]}_2 x_2 \end{bmatrix} = \begin{bmatrix} -0{,}025 & -0{,}049 \\ 0{,}015 & 0{,}031 \end{bmatrix} \qquad \frac{\partial L}{\partial b^{[1]}} = \begin{bmatrix} -0{,}049 \\ 0{,}031 \end{bmatrix}
$$

</div>

---

# Passo 5: corrigir os nove parâmetros de uma vez

<Olho q="4" />

Com $\eta = 0{,}5$, cada parâmetro anda contra o seu gradiente: $\;\theta \leftarrow \theta - \eta\, \dfrac{\partial L}{\partial \theta}$

<table>
<thead><tr><th>parâmetro</th><th>antes</th><th>gradiente</th><th>depois</th></tr></thead>
<tbody>
<tr v-click><td>w<sup>[2]</sup><sub>1</sub></td><td>0,5</td><td class="volta">−0,254</td><td>0,627</td></tr>
<tr v-click><td>w<sup>[2]</sup><sub>2</sub></td><td>−0,3</td><td class="volta">−0,229</td><td>−0,186</td></tr>
<tr v-click><td>b<sup>[2]</sup></td><td>0,2</td><td class="volta">−0,416</td><td>0,408</td></tr>
<tr v-click><td>w<sup>[1]</sup><sub>11</sub></td><td>0,1</td><td class="volta">−0,025</td><td>0,112</td></tr>
<tr v-click><td>w<sup>[1]</sup><sub>21</sub></td><td>−0,2</td><td class="volta">0,015</td><td>−0,208</td></tr>
</tbody>
</table>

<div v-click class="conta">

**Conferindo com uma ida nova:** a previsão sobe de $0{,}584$ para $0{,}668$ e a perda cai de $0{,}537$ para $0{,}404$.

</div>

<div class="fraco menor">

Os outros quatro parâmetros seguem a mesma conta; estão na saída do código, adiante.

</div>

---
class: mexa
---

# A ida e a volta inteiras, etapa por etapa

<Olho q="1 2 3 4" />

<IdaVolta :inicio="5" />

<div class="fraco pequeno" style="margin-top: 6px">

Avance até a etapa 10, aplique a correção e repita. Quantas voltas até a perda cair abaixo de 0,1? E com $\eta = 2$? E se a resposta for $y = 0$?

</div>

<!--
Os números das etapas 1 a 10 são os dos slides anteriores (ŷ 0,584; δ −0,416; δ da oculta −0,049 e 0,031;
depois da correção, ŷ 0,668 e L 0,404). Da segunda volta em diante são números novos, calculados na página.
-->

---

# Todo gradiente de peso tem a mesma forma

<Olho q="3" />

$$
\frac{\partial L}{\partial w^{[l]}_{jk}} = \underbrace{\delta^{[l]}_j}_{\text{erro de quem recebe}} \cdot \underbrace{a^{[l-1]}_k}_{\text{ativação de quem envia}}
$$

<v-clicks>

- Entrada **zerada** ($a = 0$): o peso não participou, gradiente zero.
- Neurônio de chegada **sem erro** ($\delta = 0$): nada a corrigir, gradiente zero.
- É a regra do perceptron, generalizada para qualquer camada.

</v-clicks>

<div v-click class="conceito">

Todo o trabalho do backpropagation é calcular os $\delta$. Os gradientes vêm de graça.

</div>

---

# Com vários neurônios à frente, as culpas se somam

<Olho q="3" />

<Rede
  :camadas="[3, 3, 3]" :largura="660" :altura="250" :so-arestas="['1-1-0', '1-1-1', '1-1-2']" :quentes="['1-1-0', '1-1-1', '1-1-2']" :nos-q="['1-1']" volta :r="21"
  :textos="{ '1-1': 'j', '2-0': 'δ₁', '2-1': 'δ₂', '2-2': 'δ₃' }"
  :titulos="['camada l − 1', 'camada l', 'camada l + 1']"
/>

<div v-click>

O neurônio $j$ influencia a perda por **todos** os neurônios que ele alimenta:

$$
\delta^{[l]}_j = \Big( \sum_k w^{[l+1]}_{kj}\, \delta^{[l+1]}_k \Big) \cdot g'\big(z^{[l]}_j\big)
$$

</div>

<div v-click class="fraco pequeno">

Cada parcela é "peso da ligação vezes erro de quem recebeu". Na rede 2-2-1 a soma tinha um termo só.

</div>

---

# As quatro equações do backpropagation

<Olho q="3" />

<div v-click>

**1. Erro da saída** &nbsp; (camada $L$, a última)

$$
\delta^{[L]} = \hat{y} - y
$$

</div>

<div v-click>

**2. Erro de volta uma camada**

$$
\delta^{[l]} = \Big( \big(W^{[l+1]}\big)^{\!\top} \delta^{[l+1]} \Big) \odot g'\big(z^{[l]}\big)
$$

</div>

<div v-click>

**3 e 4. Gradientes dos pesos e dos vieses**

$$
\frac{\partial L}{\partial W^{[l]}} = \delta^{[l]} \big(a^{[l-1]}\big)^{\!\top} \qquad\qquad \frac{\partial L}{\partial b^{[l]}} = \delta^{[l]}
$$

</div>

<div v-click class="fraco pequeno">

$\odot$ multiplica elemento a elemento. Na ida, $W$ leva da camada $l$ para a $l + 1$; na volta, $W^\top$ traz de $l + 1$ para $l$.

</div>

---
clicks: 5
---

# Muitas camadas: a equação 2, repetida

<Olho q="3" />

<Cadeia
  :caixas="['x', 'camada 1', 'camada 2', 'camada 3', 'camada 4', 'perda L']"
  :ida="['a⁽⁰⁾', 'a⁽¹⁾', 'a⁽²⁾', 'a⁽³⁾', 'ŷ']" :volta="['', 'δ⁽¹⁾', 'δ⁽²⁾', 'δ⁽³⁾', 'δ⁽⁴⁾']" revela="volta" :passo="$clicks"
/>

<div style="min-height: 4.6em">
<div v-if="$clicks === 0">A ida já passou, de $x$ até a perda, guardando cada $a$.</div>
<div v-if="$clicks === 1">Começa em <b>δ⁽⁴⁾ = ŷ − y</b>, pela equação 1.</div>
<div v-if="$clicks >= 2 && $clicks <= 4">Cada δ seguinte sai do anterior pela <b>equação 2</b>. A camada recebe o δ da frente, calcula os <b>seus</b> gradientes e passa o δ para trás.</div>
<div v-if="$clicks === 5" class="conceito">A rede ter 2 camadas ou 200 não muda a receita: muda <b>quantas vezes</b> o laço roda.</div>
</div>

---

# O algoritmo completo, para um exemplo

<v-clicks>

1. <span class="ida">**Ida.**</span> Calcule $z^{[l]}$ e $a^{[l]}$ de todas as camadas, **guardando** os valores.
2. <span class="ida">**Perda.**</span> Compare $\hat{y}$ com $y$.
3. <span class="volta">**Erro da saída.**</span> $\delta^{[L]} = \hat{y} - y$.
4. <span class="volta">**Volta.**</span> Para $l = L, L - 1, \dots, 1$: gradientes da camada, $\delta^{[l]} \big(a^{[l-1]}\big)^{\!\top}$ e $\delta^{[l]}$; depois o erro da camada anterior, $\delta^{[l-1]} = \big( (W^{[l]})^{\!\top} \delta^{[l]} \big) \odot g'\big(z^{[l-1]}\big)$.
5. <span class="volta">**Correção.**</span> Todos os parâmetros andam $-\eta$ vezes o seu gradiente.

</v-clicks>

<div v-click class="conceito">

A volta custa o mesmo tipo de conta que a ida: uma multiplicação de matriz por camada. **Duas passadas**, não treze mil.

</div>

---

# Em código: a volta, linha por linha

<<< @/snippets/b_volta.py {1-4|6|7-8|9|10-11|all}

<Saida v-click nome="b_volta" />

<div class="fraco pequeno">

`np.outer(delta, a)` monta a matriz "erro de quem recebe × ativação de quem envia", um peso por célula.

</div>

---

# Em código: a correção e a ida de conferência

<<< @/snippets/b_correcao.py {1|2-5|all}

<Saida v-click nome="b_correcao" />

<div v-click>

<<< @/snippets/b_conferencia.py

</div>

---

# Um passo, e a rede já erra menos neste exemplo

<Saida nome="b_conferencia" />

<v-clicks>

- Os nove parâmetros mudaram **ao mesmo tempo**, todos calculados com os pesos antigos.
- A previsão andou na direção da resposta, sem chegar lá.

</v-clicks>

<div v-click class="conceito">

Treinar é repetir isso milhares de vezes, com todos os exemplos.

</div>

---
class: codigo-menor
---

# Como saber se a volta está certa: o método ingênuo confere

<<< @/snippets/b_numerico.py {1-3|5-6|8-11|12|13-14|all}

---

# As duas contas dão o mesmo gradiente

<Saida nome="b_numerico" />

<v-clicks>

- **backpropagation**: uma ida e uma volta, para todos os pesos.
- **mexendo no peso**: uma ida a mais **por peso**.
- As duas colunas saem de contas independentes.

</v-clicks>

<div v-click class="conceito">

É o teste que se faz ao programar uma volta nova.

</div>

<!--
As duas colunas saem de contas independentes. É o teste que se faz ao programar uma volta nova.
-->

---

# Em código: qualquer número de camadas

<<< @/snippets/b_geral.py {1-5|7-9|10|11-13|14-15|all}

<div class="fraco pequeno">

`W` e `b` são listas, com uma matriz e um vetor por camada. `W[l]` leva de `a[l]` para `a[l + 1]`.

</div>

---

# Em código: a rede aprende o XOR sozinha

<<< @/snippets/b_xor.py {1-5|10|11|12-14|all}

<div class="fraco pequeno">

Os pesos começam **aleatórios** (com semente, para o resultado se repetir). Ninguém disse à rede o que é OU nem NÃO-E.

</div>

---

# O que nenhum neurônio sozinho fazia

<img class="fig" src="/fig/xor-aprendido.svg" style="width: 800px" />

<div class="cols c55">
<div>

<Saida v-click nome="_b_xor_tabela" />

</div>
<div>

<div v-click class="conceito">

A rede **descobriu** uma representação oculta em que o XOR é separável por uma reta, como a que montamos à mão na Parte 3.

</div>

</div>
</div>

---
class: mexa
---

# Assista a rede aprender o XOR

<TreinoXor />

<v-clicks>

- A fronteira nas entradas começa como uma reta e **dobra**.
- Na camada oculta, os quatro pontos se arrumam até uma reta separá-los.
- Clique em "outro sorteio" e dê 5.000 épocas a cada um: os sorteios 1 a 5 aprendem, os de 6 a 9 **emperram**.

</v-clicks>

<div class="fraco menor">

O sorteio dos pesos é o desta página, não o do `numpy` do slide anterior: o comportamento é o mesmo, os números não.

</div>

---
class: sua-vez
---

# A volta com outra resposta

Mesma rede e mesma ida: $a^{[1]} = (0{,}611;\ 0{,}550)$, $\hat{y} = 0{,}584$, $W^{[2]} = (0{,}5;\ {-}0{,}3)$. Agora a resposta é $y = 0$.

1. Quanto vale $\delta^{[2]}$?
2. Quais são os gradientes de $w^{[2]}_1$ e $w^{[2]}_2$?
3. Calcule $\delta^{[1]}_1$, usando $\sigma'\big(z^{[1]}_1\big) = 0{,}238$. Para que lado $h_1$ deveria ir?

<div v-click class="conta">

$\delta^{[2]} = 0{,}584 - 0 = 0{,}584$. Gradientes: $0{,}584 \cdot 0{,}611 = 0{,}357$ e $0{,}584 \cdot 0{,}550 = 0{,}321$.

</div>

<div v-click class="conta">

$\delta^{[1]}_1 = 0{,}5 \cdot 0{,}584 \cdot 0{,}238 = 0{,}069$. Positivo: $h_1$ deveria **descer**, porque ele empurra $\hat{y}$ para cima e a resposta é 0.

</div>

---
class: mexa
---

# O erro encolhe a cada camada que atravessa

A equação 2 multiplica por $g'(z)$ **em toda camada**. Com a sigmoide, $g'(z) \le 0{,}25$.

<GradienteSome />

<v-clicks>

- Dez camadas de sigmoide: o erro chega ao começo multiplicado por menos de um milionésimo.
- As primeiras camadas quase não aprendem: é o **gradiente que desaparece**.
- Com a **ReLU**, o fator é 1 onde o neurônio está ativo. É um dos motivos de ela ter virado o padrão.

</v-clicks>

---

# O backpropagation nas quatro perguntas

<div class="quatro">
<div>

<span class="num">1</span> **Prever**

A ida, guardando $z$ e $a$ de cada camada

</div>
<div>

<span class="num">2</span> **Medir**

A perda na saída

</div>
<div>

<span class="num">3</span> **Atribuir**

A volta: $\delta$ da saída, depois $\delta$ de cada camada, de trás para a frente

</div>
<div>

<span class="num">4</span> **Corrigir**

$W^{[l]} \leftarrow W^{[l]} - \eta\, \delta^{[l]} \big(a^{[l-1]}\big)^{\!\top}$

</div>
</div>

<div v-click class="conceito">

O backpropagation **não é** o aprendizado: é só a pergunta 3, o cálculo do gradiente. Quem aprende é o gradiente descendente, que usa esse gradiente na pergunta 4.

</div>
