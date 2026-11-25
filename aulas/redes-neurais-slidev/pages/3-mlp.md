---
layout: secao
---

<span class="parte">Parte 3 · 50 min</span>

# A rede multicamada

Neurônios que alimentam neurônios: a camada oculta e a conta da ida.

---

# O XOR sai de duas perguntas mais fáceis

"Exatamente uma entrada é 1" é o mesmo que:

<div class="grande centro">

<span class="ida">**pelo menos uma** é 1</span> &nbsp; **E** &nbsp; <span class="ida">**não são as duas**</span>

</div>

<v-clicks>

- "Pelo menos uma é 1" é a porta **OU**: uma reta resolve.
- "Não são as duas" é a porta **NÃO-E**: uma reta resolve.
- Juntar as duas respostas é a porta **E**: uma reta resolve.

</v-clicks>

<div v-click class="conceito">

Três neurônios, cada um com a sua reta: dois respondem às perguntas fáceis, o terceiro combina as respostas.

</div>

---
clicks: 2
---

# Três perceptrons resolvem o XOR

<Rede
  :camadas="[2, 2, 1]" fortes :largura="760" :altura="300" :passo="$clicks" :visivel="{ 1: 1, 2: 2 }"
  :textos="{ '0-0': 'x₁', '0-1': 'x₂', '1-0': 'h₁', '1-1': 'h₂', '2-0': 'ŷ' }"
  :pesos="{ '0-0-0': '1', '0-1-0': '1', '0-0-1': '−1', '0-1-1': '−1', '1-0-0': '1', '1-1-0': '1' }"
  :fora="{ '1-0': 'OU · b = −1', '1-1': 'NÃO-E · b = 1', '2-0': 'E · b = −2' }"
  :titulos="['entrada', 'camada oculta', 'saída']"
/>

<div class="centro">
<span v-if="$clicks === 0">Duas entradas, como antes.</span>
<span v-if="$clicks === 1">Dois neurônios no meio: <b>h₁</b> faz a porta OU, <b>h₂</b> faz a NÃO-E.</span>
<span v-if="$clicks === 2">O neurônio de saída não vê x₁ e x₂: recebe <b>h₁ e h₂</b> e faz a porta E.</span>
</div>

<div class="fraco pequeno centro">

Os pesos foram escolhidos à mão, com a ativação degrau. Aprender esses pesos é o assunto da Parte 5.

</div>

---
class: mexa
---

# Teste os quatro casos na rede feita à mão

<XorMao />

<div v-click class="conceito">

Nas coordenadas novas, $(h_1, h_2)$, **uma reta separa as classes**. A camada oculta não classifica: ela cria uma representação em que classificar fica fácil.

</div>

<!--
Passe pelos quatro casos. Note que (0,1) e (1,0) caem no mesmo ponto do plano da direita: (h1, h2) = (1, 1).
-->

---

# Em código: a rede feita à mão acerta os quatro casos

<<< @/snippets/m_xor_mao.py {3|4|5|all}

<Saida v-click nome="m_xor_mao" />

---
clicks: 3
---

# A camada oculta calcula atributos que não estão nos dados

<Rede
  :camadas="[4, 3, 1]" :largura="900" :altura="330" :margem="170" :r="20" :passo="$clicks" :visivel="{ 1: 1, 2: 2 }"
  :so-arestas="$clicks >= 3 ? null : ['0-0-0', '0-1-0', '0-2-1', '0-0-2', '0-3-2', '1-0-0', '1-1-0', '1-2-0']"
  :fortes="['0-0-0', '0-1-0', '0-2-1', '0-0-2', '0-3-2', '1-0-0', '1-1-0', '1-2-0']"
  :fora="{ '0-0': 'preço', '0-1': 'frete', '0-2': 'marketing', '0-3': 'material', '1-0': 'acessível?', '1-1': 'conhecida?', '1-2': 'boa qualidade?', '2-0': 'campeã?' }"
  :titulos="['atributos brutos', 'camada oculta', 'saída']"
/>

<div class="centro" style="min-height: 3.4em">
<div v-if="$clicks === 0">Uma camiseta vai ser <b>campeã de vendas</b>? A tabela só tem quatro colunas.</div>
<div v-if="$clicks === 1">Quem compra pensa em outras três coisas. Cada uma sai de <b>algumas</b> colunas: preço e frete dizem se ela é acessível.</div>
<div v-if="$clicks === 2">A saída não olha o preço: decide com os <b>três atributos intermediários</b>.</div>
<div v-if="$clicks === 3">Na rede de verdade, cada neurônio recebe <b>todas</b> as entradas, e ninguém dá nome a eles: o treino escolhe os atributos que ajudam a acertar.</div>
</div>

<div class="fraco pequeno centro">

Exemplo de previsão de demanda de Andrew Ng (*Machine Learning Specialization*).

</div>

<!--
Mesma ideia do XOR: lá, h1 e h2 eram "pelo menos uma" e "não são as duas". Aqui são "acessível", "conhecida" e "boa qualidade".
Preço entra em dois neurônios, com sinais opostos: preço alto derruba "acessível" e sobe "boa qualidade" (preço como sinal de qualidade).
Os atributos de uma rede treinada raramente têm nome tão limpo. Na rede dos dígitos (Parte 6) dá para olhar os pesos da primeira camada como imagens.
-->

---

# Em código: três camisetas, três atributos ocultos

<<< @/snippets/m_camiseta.py {1-2|4-7|9-10|all}

<Saida v-click nome="m_camiseta" />

<div v-click class="conceito pequeno">

**A** é acessível, mas pouca gente a conhece. **B** é conhecida e boa, mas cara. **C** vai bem nos três, e é a de maior probabilidade. Os pesos aqui foram escolhidos à mão.

</div>

---
clicks: 3
---

# Um perceptron multicamada (MLP)

<Rede :camadas="[3, 4, 4, 2]" :titulos="['entrada', 'oculta 1', 'oculta 2', 'saída']" :visivel="{ 1: 1, 2: 2, 3: 3 }" :passo="$clicks" :altura="280" :largura="780" :r="20" />

<div style="min-height: 3.2em">
<div v-if="$clicks === 0"><b>Camada de entrada</b>: os dados, sem conta nenhuma.</div>
<div v-if="$clicks === 1 || $clicks === 2"><b>Camadas ocultas</b>: cada neurônio é o da Parte 2, recebendo as saídas da camada anterior.</div>
<div v-if="$clicks === 3"><b>Camada de saída</b>: a previsão. Cada neurônio se liga a <b>todos</b> os da camada anterior.</div>
</div>

---

# Cada camada tem uma matriz de pesos

<Olho q="1" />

<div class="cols">
<div>

| símbolo | o que é |
|---|---|
| $a^{[0]} = x$ | a entrada |
| $W^{[l]}$ | pesos que **chegam** à camada $l$ |
| $b^{[l]}$ | vieses da camada $l$ |
| $z^{[l]}$ | somas ponderadas da camada $l$ |
| $a^{[l]}$ | **ativações** (saídas) da camada $l$ |
| $g$ | a função de ativação |

</div>
<div>

<div v-click>

$W^{[l]}$ tem **uma linha por neurônio** da camada $l$ e **uma coluna por neurônio** da camada anterior.

</div>

<div v-click>

$w^{[l]}_{jk}$ liga o neurônio $k$ da camada $l-1$ ao neurônio $j$ da camada $l$.

</div>

<div v-click class="cuidado">

O número entre colchetes é a camada. Não é potência.

</div>

</div>
</div>

---
clicks: 6
---

# A ida é a mesma conta, repetida em cada camada

<Olho q="1" />

<div v-click="1">

Um neurônio $j$ da camada $l$:

$$
z^{[l]}_j = \sum_k w^{[l]}_{jk}\, a^{[l-1]}_k + b^{[l]}_j \qquad a^{[l]}_j = g\big(z^{[l]}_j\big)
$$

</div>

<div v-click="2">

A camada inteira de uma vez, com matriz:

$$
\boxed{\; z^{[l]} = W^{[l]}\, a^{[l-1]} + b^{[l]} \qquad a^{[l]} = g\big(z^{[l]}\big) \;}
$$

</div>

<Cadeia :class="{ some: $clicks < 3 }" :caixas="['x', 'z⁽¹⁾', 'a⁽¹⁾', 'z⁽²⁾', 'a⁽²⁾ = ŷ']" :ida="['W⁽¹⁾, b⁽¹⁾', 'g', 'W⁽²⁾, b⁽²⁾', 'g']" revela="ida" :passo="$clicks - 2" :largura="820" />

<!--
Em inglês, forward propagation: a entrada se propaga para a frente, camada por camada.
-->

---

# A rede que vai nos acompanhar até o fim da aula

<Rede
  :camadas="[2, 2, 1]" fortes :largura="700" :altura="270"
  :textos="{ '0-0': 'x₁', '0-1': 'x₂', '1-0': 'h₁', '1-1': 'h₂', '2-0': 'ŷ' }"
  :pesos="{ '0-0-0': '0,1', '0-1-0': '0,3', '0-0-1': '−0,2', '0-1-1': '0,4', '1-0-0': '0,5', '1-1-0': '−0,3' }"
  :fora="{ '0-0': '0,5', '0-1': '1', '1-0': 'b = 0,1', '1-1': 'b = −0,1', '2-0': 'b = 0,2' }"
  :titulos="['entrada', 'camada 1 (oculta)', 'camada 2 (saída)']"
/>

$$
W^{[1]} = \begin{bmatrix} 0{,}1 & 0{,}3 \\ -0{,}2 & 0{,}4 \end{bmatrix} \quad b^{[1]} = \begin{bmatrix} 0{,}1 \\ -0{,}1 \end{bmatrix} \qquad W^{[2]} = \begin{bmatrix} 0{,}5 & -0{,}3 \end{bmatrix} \quad b^{[2]} = 0{,}2
$$

<div class="fraco pequeno centro">

Entrada $x = (0{,}5;\ 1)$, resposta $y = 1$. Sigmoide em todos os neurônios. A linha 1 de $W^{[1]}$ são os pesos que chegam a $h_1$.

</div>

---

# Na mão: a ida, camada 1

<Olho q="1" />

**Somas ponderadas** dos dois neurônios ocultos:

<div v-click>

$$
z^{[1]}_1 = 0{,}1 \cdot 0{,}5 + 0{,}3 \cdot 1 + 0{,}1 = 0{,}45
$$

</div>

<div v-click>

$$
z^{[1]}_2 = -0{,}2 \cdot 0{,}5 + 0{,}4 \cdot 1 - 0{,}1 = 0{,}20
$$

</div>

<div v-click>

**Ativações**:

$$
a^{[1]}_1 = \sigma(0{,}45) = 0{,}611 \qquad a^{[1]}_2 = \sigma(0{,}20) = 0{,}550
$$

</div>

<div v-click class="conceito">

Essas duas ativações são a **entrada da camada seguinte**. A camada 2 nunca vê $x$.

</div>

---

# Na mão: a ida, camada 2

<Olho q="1" />

<Rede
  :camadas="[2, 2, 1]" :largura="640" :altura="230" :so-arestas="['1-0-0', '1-1-0']" :fortes="['1-0-0', '1-1-0']"
  :textos="{ '0-0': 'x₁', '0-1': 'x₂', '1-0': 'h₁', '1-1': 'h₂', '2-0': 'ŷ' }"
  :pesos="{ '1-0-0': '0,5', '1-1-0': '−0,3' }"
  :fora="{ '0-0': '0,5', '0-1': '1', '1-0': '0,611', '1-1': '0,550', '2-0': $clicks >= 2 ? '0,584' : '?' }"
/>

<div v-click>

$$
z^{[2]} = 0{,}5 \cdot 0{,}611 + (-0{,}3) \cdot 0{,}550 + 0{,}2 = 0{,}340
$$

</div>

<div v-click>

$$
\hat{y} = a^{[2]} = \sigma(0{,}340) = 0{,}584
$$

</div>

<div v-click>

$$
L = -\ln 0{,}584 = 0{,}537
$$

</div>

---
class: mexa
---

# A ida inteira, etapa por etapa

<Olho q="1 2" />

<IdaVolta :max="5" />

<div class="fraco pequeno" style="margin-top: 6px">

Refaça as cinco etapas. Depois troque a resposta para $y = 0$: o que muda na ida, e o que não muda?

</div>

<!--
Trocar y só muda a perda (etapa 5): a previsão não depende da resposta.
-->

---

# Em código: a ida, linha por linha

<<< @/snippets/m_ida.py {1-4|6-7|9|10|11|12|13|all}

<Saida v-click nome="m_ida" />

---

# Quantos botões tem uma rede?

Cada camada tem **(neurônios) × (entradas que chegam)** pesos, mais **um viés por neurônio**.

<div v-click>

A rede 2-2-1 destes slides:

$$
\underbrace{2 \cdot 2 + 2}_{\text{camada 1}} + \underbrace{1 \cdot 2 + 1}_{\text{camada 2}} = 9 \text{ parâmetros}
$$

</div>

<div v-click>

Uma rede para dígitos de $28 \times 28$ pixels, com camadas 784-16-16-10:

$$
\underbrace{16 \cdot 784 + 16}_{12.560} + \underbrace{16 \cdot 16 + 16}_{272} + \underbrace{10 \cdot 16 + 10}_{170} = 13.002 \text{ parâmetros}
$$

</div>

<div v-click class="cuidado">

Treinar é descobrir para que lado girar **cada um** desses botões. É o problema da Parte 5.

</div>

---
class: sua-vez
---

# A ida com outra entrada

Na mesma rede 2-2-1, troque a entrada para $x = (1;\ 0)$.

1. Calcule $z^{[1]}_1$ e $z^{[1]}_2$.
2. Use $\sigma(0{,}2) = 0{,}550$ e $\sigma(-0{,}3) = 0{,}426$ para as ativações.
3. Calcule $z^{[2]}$. A previsão fica acima ou abaixo de 0,5?

<div v-click class="conta">

$z^{[1]}_1 = 0{,}1 \cdot 1 + 0{,}3 \cdot 0 + 0{,}1 = 0{,}2 \qquad z^{[1]}_2 = -0{,}2 \cdot 1 + 0{,}4 \cdot 0 - 0{,}1 = -0{,}3$

</div>

<div v-click class="conta">

$z^{[2]} = 0{,}5 \cdot 0{,}550 - 0{,}3 \cdot 0{,}426 + 0{,}2 = 0{,}347$. É positivo, então $\hat{y} > 0{,}5$ (vale $0{,}586$).

</div>

---

# Sem ativação, empilhar camadas não adianta

Tire o $g$ de uma rede de duas camadas:

<div v-click>

$$
\hat{y} = W^{[2]} \big( W^{[1]} x + b^{[1]} \big) + b^{[2]}
$$

</div>

<div v-click>

$$
\hat{y} = \underbrace{W^{[2]} W^{[1]}}_{\text{uma matriz só}}\, x + \underbrace{W^{[2]} b^{[1]} + b^{[2]}}_{\text{um viés só}}
$$

</div>

<div v-click class="cuidado">

Dez camadas lineares empilhadas calculam o mesmo que **uma** camada linear. A fronteira continua sendo uma reta.

</div>

<div v-click class="conceito">

É a função de ativação, **não linear**, que dá à rede o poder de dobrar a fronteira.

</div>

---

# Três funções de ativação que você vai encontrar

<img class="fig" src="/fig/ativacoes.svg" style="width: 860px" />

<table class="pequeno">
<thead><tr><th></th><th>fórmula</th><th>derivada</th><th>saída</th></tr></thead>
<tbody>
<tr v-click><td><b>sigmoide</b></td><td>1 / (1 + e<sup>−z</sup>)</td><td>σ(z)·(1 − σ(z)), no máximo 0,25</td><td>entre 0 e 1</td></tr>
<tr v-click><td><b>tanh</b></td><td>tanh(z)</td><td>1 − tanh²(z), no máximo 1</td><td>entre −1 e 1</td></tr>
<tr v-click><td><b>ReLU</b></td><td>max(0, z)</td><td>1 se z &gt; 0, senão 0</td><td>de 0 em diante</td></tr>
</tbody>
</table>

---

# Qual ativação usar

<v-clicks>

- **Camadas ocultas: ReLU**, na dúvida. É barata, e a derivada vale 1 em todo o lado positivo.
- **Sigmoide e tanh** achatam nas pontas: lá a derivada é quase zero, e o aprendizado emperra. Esse efeito volta na Parte 5.
- **Camada de saída**: quem decide é o tipo de resposta, não o gosto. É a Parte 4.

</v-clicks>

<div v-click class="fraco pequeno">

A ReLU tem variações (*Leaky ReLU*, GELU e outras) que mudam o lado negativo. A ideia é a mesma.

</div>

---

# Mais neurônios ocultos, curvas mais flexíveis

<img class="fig" src="/fig/curvas.svg" style="width: 860px" />

<div v-click class="conceito">

**Aproximação universal**: com neurônios suficientes, uma única camada oculta aproxima qualquer função contínua. O teorema diz que os pesos existem. Não diz como achá-los.

</div>

---

# A rede multicamada nas quatro perguntas

<div class="quatro">
<div>

<span class="num">1</span> **Prever**

A ida: $a^{[l]} = g\big(W^{[l]} a^{[l-1]} + b^{[l]}\big)$, camada por camada

</div>
<div>

<span class="num">2</span> **Medir**

Uma perda na saída. Qual? Parte 4

</div>
<div>

<span class="num">3</span> **Atribuir**

**?** Quanta culpa tem um peso da camada 1, se o erro só aparece na saída?

</div>
<div>

<span class="num">4</span> **Corrigir**

Gradiente descendente, igual. Só falta o gradiente

</div>
</div>

<div v-click class="cuidado">

A regra do perceptron precisava da **resposta certa de cada neurônio**. Para os neurônios ocultos, ninguém sabe qual é. Foi esse o impasse de 1969 a 1986.

</div>
