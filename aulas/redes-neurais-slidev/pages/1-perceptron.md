---
layout: secao
---

<span class="parte">Parte 1 · 50 min</span>

# O perceptron

Um neurônio sozinho: como decide, como erra e como se corrige.

---

# A ideia tem mais de oitenta anos

<v-clicks>

- **1943** · McCulloch e Pitts: um neurônio como conta lógica, com pesos fixados à mão.
- **1958** · Rosenblatt: o **perceptron**, um neurônio que **ajusta os próprios pesos** a partir de exemplos.
- **1969** · Minsky e Papert mostram o que um perceptron sozinho **não** consegue.
- **1986** · Rumelhart, Hinton e Williams: o **backpropagation** treina redes de várias camadas.

</v-clicks>

<div v-click class="fraco pequeno">

A aula segue essa ordem, porque cada passo resolve o defeito do anterior.

</div>

---
clicks: 6
---

# Um neurônio tem seis peças

<Olho q="1" />

<Neuronio :passo="$clicks" />

<div class="centro" style="min-height: 2em">
<span v-if="$clicks === 1"><b>Entradas</b>: os números que chegam. Um pixel, uma medida, uma resposta sim/não.</span>
<span v-if="$clicks === 2"><b>Pesos</b>: um por entrada. Dizem quanto cada entrada importa.</span>
<span v-if="$clicks === 3"><b>Viés</b>: um número que entra sempre, sem depender de entrada nenhuma.</span>
<span v-if="$clicks === 4"><b>Soma ponderada</b>: cada entrada vezes o seu peso, mais o viés.</span>
<span v-if="$clicks === 5"><b>Função de ativação</b>: transforma a soma na resposta do neurônio.</span>
<span v-if="$clicks === 6"><b>Saída</b>: a previsão, que se escreve ŷ.</span>
</div>

<!--
Seis cliques, uma peça por clique. Diga o nome de cada peça em voz alta; os nomes voltam a aula inteira.
-->

---

# A conta do neurônio são duas linhas

<Olho q="1" />

<div v-click>

**Soma ponderada**: cada entrada vezes o seu peso, mais o viés.

$$
z = w_1 x_1 + w_2 x_2 + \dots + w_n x_n + b = \mathbf{w} \cdot \mathbf{x} + b
$$

</div>

<div v-click>

**Ativação**: no perceptron, a função **degrau**.

$$
\hat{y} = \begin{cases} 1 & \text{se } z \ge 0 \\ 0 & \text{se } z < 0 \end{cases}
$$

</div>

<div v-click class="conceito">

$\hat{y}$ (lê-se "y chapéu") é a **previsão**. $y$, sem chapéu, é a **resposta certa**.

</div>

---

# Exemplo: vou ao show?

<Olho q="1" />

<div class="cols c46">
<div>

| | pergunta | peso |
|---|---|---|
| $x_1$ | tenho dinheiro? | $w_1 = 4$ |
| $x_2$ | um amigo vai? | $w_2 = 2$ |
| $x_3$ | é perto de casa? | $w_3 = 1$ |

Viés: $b = -5$. Cada $x$ vale 1 (sim) ou 0 (não).

</div>
<div>

<div v-click>

Tenho dinheiro e o amigo vai, mas é longe:

$$
z = 4 \cdot 1 + 2 \cdot 1 + 1 \cdot 0 - 5 = 1 \;\Rightarrow\; \hat{y} = 1
$$

</div>

<div v-click class="preveja">

O amigo vai e é perto, mas estou sem dinheiro. Vou?

</div>

<div v-click>

$$
z = 4 \cdot 0 + 2 \cdot 1 + 1 \cdot 1 - 5 = -2 \;\Rightarrow\; \hat{y} = 0
$$

</div>

</div>
</div>

<div v-click class="conceito">

O **peso** diz quanto cada entrada importa. O **viés** diz quão difícil é a saída dar 1.

</div>

---

# O perceptron traça uma reta

<Olho q="1" />

<div class="cols">
<div>

A fronteira entre $\hat{y} = 0$ e $\hat{y} = 1$ é onde $z = 0$:

$$
w_1 x_1 + w_2 x_2 + b = 0
$$

<div v-click>

Com duas entradas, isso é uma **reta**.

</div>

<v-clicks>

- Mudar os **pesos** gira a reta.
- Mudar o **viés** a desloca.

</v-clicks>

</div>
<div>

<Plano :reta="[2, 1, -3]" porta="E" :tam="300" />

<div class="fraco pequeno centro">

$w = (2, 1)$ e $b = -3$. Ponto cheio: resposta 1. Região azul: $\hat{y} = 1$.

</div>

</div>
</div>

---
class: mexa
---

# Gire os botões: ache uma reta para cada porta

<Olho q="1" />

<NeuronioInterativo />

<div class="fraco pequeno" style="margin-top: 8px">

Comece pela porta **E** (já resolvida). Depois ache pesos para a **OU**. Por último, tente a **XOR**.

</div>

<!--
Deixe a turma ditar os valores. Na OU, w = (2, 2) e b = -1 resolve. No XOR ninguém consegue:
não diga ainda por quê, a resposta vem no fim da parte.
-->

---

# Quem escolhe os pesos? Os exemplos

<Olho q="2" />

No show, os pesos foram escolhidos à mão. A proposta de Rosenblatt: **aprendê-los**.

<v-clicks>

1. Comece com pesos quaisquer (zero serve).
2. Mostre **um exemplo** e compare a previsão com a resposta.
3. Se errou, **mexa nos pesos** na direção que conserta.
4. Repita, exemplo após exemplo.

</v-clicks>

<div v-click>

O erro de um exemplo só pode ter três valores:

$$
\text{erro} = y - \hat{y} \in \{-1,\; 0,\; +1\}
$$

</div>

---

# A regra de correção do perceptron

<Olho q="3 4" />

$$
w_j \leftarrow w_j + \eta \,(y - \hat{y})\, x_j \qquad\qquad b \leftarrow b + \eta \,(y - \hat{y})
$$

<table>
<thead><tr><th>caso</th><th>erro</th><th>o que acontece com o peso</th></tr></thead>
<tbody>
<tr v-click><td>acertou</td><td>0</td><td>nada</td></tr>
<tr v-click><td>disse 0, era 1</td><td class="volta">+1</td><td><b>soma</b> η·x: empurra z para cima</td></tr>
<tr v-click><td>disse 1, era 0</td><td class="volta">−1</td><td><b>subtrai</b> η·x: empurra z para baixo</td></tr>
</tbody>
</table>

<div v-click class="conceito">

$\eta$ (eta) é a **taxa de aprendizado**: o tamanho do passo.

</div>

<div v-click class="conceito">

Só muda o peso de entrada **ativa**: se $x_j = 0$, aquele peso não teve culpa.

</div>

---

# Por que a regra conserta

<Olho q="4" />

Era 1 e o neurônio disse 0: $z$ ficou baixo demais. Depois da correção, com o mesmo exemplo:

<div v-click>

$$
z_{\text{novo}} = (\mathbf{w} + \eta\,\mathbf{x}) \cdot \mathbf{x} + (b + \eta)
$$

</div>

<div v-click>

$$
z_{\text{novo}} = \underbrace{\mathbf{w} \cdot \mathbf{x} + b}_{z \text{ de antes}} \;+\; \textcolor{#D9480F}{\eta\,(\mathbf{x} \cdot \mathbf{x} + 1)}
$$

</div>

<div v-click>

A parcela em laranja nunca é negativa: $z$ **sobe**. No caso contrário, pela mesma conta, $z$ desce.

</div>

<div v-click class="cuidado">

Um passo pode não bastar, e consertar um exemplo pode estragar outro. Por isso se repete.

</div>

---

# Na mão: aprendendo a porta E

Começo: $w = (0, 0)$, $b = 0$, $\eta = 1$. Uma **época** é uma passada pelos quatro exemplos.

<table>
<thead><tr><th>x₁</th><th>x₂</th><th>y</th><th>z = w·x + b</th><th>ŷ</th><th>erro</th><th>w depois</th><th>b depois</th></tr></thead>
<tbody>
<tr v-click><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td class="volta">−1</td><td>(0, 0)</td><td class="volta">−1</td></tr>
<tr v-click><td>0</td><td>1</td><td>0</td><td>−1</td><td>0</td><td>0</td><td>(0, 0)</td><td>−1</td></tr>
<tr v-click><td>1</td><td>0</td><td>0</td><td>−1</td><td>0</td><td>0</td><td>(0, 0)</td><td>−1</td></tr>
<tr v-click><td>1</td><td>1</td><td>1</td><td>−1</td><td>0</td><td class="volta">+1</td><td class="volta">(1, 1)</td><td class="volta">0</td></tr>
</tbody>
</table>

<v-clicks>

- 1º exemplo: $x = (0, 0)$, então **só o viés** mudou.
- 4º exemplo: as duas entradas estavam ativas, então **os dois pesos** subiram.
- Dois erros na primeira época. Falta repetir.

</v-clicks>

---
class: mexa
---

# Continue o treino, um exemplo por clique

<Olho q="1 2 3 4" />

<PerceptronPasso />

<div class="fraco pequeno" style="margin-top: 8px">

As quatro primeiras linhas são as do slide anterior. Antes de cada clique: o próximo exemplo vai ser acertado? Quem muda?

</div>

<!--
Na porta E o perceptron para na 6ª época, com erros 2, 3, 3, 2, 1, 0.
Troque para a XOR no fim: os erros por época nunca zeram.
-->

---

# Em código: um exemplo, passo a passo

<<< @/snippets/p1_passo.py {1-2|4-6|8|10|11|12|13-14|16-17}

<Saida v-click nome="p1_passo" />

---

# Em código: a mesma conta, para todo exemplo e toda época

<<< @/snippets/p1_treinar.py {2-4|5|7|8-10|11-12|13}

<div class="fraco pequeno">

As linhas 8 a 10 são as do slide anterior. O que mudou: dois laços por fora e um histórico.

</div>

---

# Seis épocas bastam para a porta E

<div class="cols c40">
<div>

<<< @/snippets/p1_hist.py

<v-clicks>

- A coluna `erros` cai até zero.
- Época sem erro: nenhum peso muda mais. O perceptron **parou sozinho**.

</v-clicks>

</div>
<div>

<Saida nome="p1_hist" />

</div>
</div>

---
class: sua-vez
---

# Um passo do perceptron

Um perceptron tem $w = (2, 1)$, $b = -3$ e $\eta = 1$. Chega o exemplo $x = (1, 0)$, com resposta $y = 1$.

1. Quanto vale $z$? Qual é a previsão?
2. Qual é o erro?
3. Como ficam $w$ e $b$ depois da correção?

<div v-click class="conta">

$z = 2 \cdot 1 + 1 \cdot 0 - 3 = -1$, então $\hat{y} = 0$. Erro: $1 - 0 = +1$.

</div>

<div v-click class="conta">

$w \leftarrow (2, 1) + 1 \cdot (1, 0) = (3, 1)$ e $b \leftarrow -3 + 1 = -2$. O peso $w_2$ não muda, porque $x_2 = 0$.

</div>

---

# Três portas lógicas, e uma não aprende

<img class="fig" src="/fig/portas-erros.svg" style="width: 860px" />

<div v-click>

No **XOR** (a saída é 1 quando **exatamente uma** entrada é 1), o número de erros nunca chega a zero.

</div>

<div v-click class="preveja">

Com mais épocas ele aprenderia? Olhe os quatro pontos do XOR no próximo slide.

</div>

---

# Nenhuma reta separa o XOR

<div style="display: flex; justify-content: space-around">
<Plano :reta="[2, 1, -3]" porta="E" :tam="240" titulo="E: uma reta resolve" />
<Plano v-click :reta="[1, 1, -0.5]" porta="OU" :tam="240" titulo="OU: uma reta resolve" />
<Plano v-click porta="XOR" :tam="240" titulo="XOR: nenhuma reta resolve" />
</div>

<div v-click class="cuidado">

O perceptron só resolve problemas **linearmente separáveis**: aqueles em que uma reta (um plano, com mais entradas) deixa cada classe de um lado.

</div>

---

# O perceptron nas quatro perguntas

<div class="quatro">
<div>

<span class="num">1</span> **Prever**

$\hat{y} = \text{degrau}(\mathbf{w} \cdot \mathbf{x} + b)$

</div>
<div>

<span class="num">2</span> **Medir**

$\text{erro} = y - \hat{y}$: certo ou errado

</div>
<div>

<span class="num">3</span> **Atribuir**

A culpa é dos pesos das entradas ativas

</div>
<div>

<span class="num">4</span> **Corrigir**

$w_j \leftarrow w_j + \eta\,(y - \hat{y})\,x_j$

</div>
</div>

<div v-click style="margin-top: 12px">

**Dois defeitos**, que as próximas partes consertam:

</div>

<v-clicks>

- O erro é "tudo ou nada": não diz se a previsão passou **perto** ou **longe**. → Parte 2
- Uma reta só não resolve o XOR. → Parte 3

</v-clicks>
