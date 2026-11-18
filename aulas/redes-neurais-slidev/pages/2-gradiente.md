---
layout: secao
---

<span class="parte">Parte 2 · 45 min</span>

# O neurônio que desce o gradiente

Trocar "certo ou errado" por "quão errado", e corrigir na medida do erro.

---
class: mexa
---

# O degrau não diz para que lado ir

<SigmoideExplora />

<v-clicks>

- Arraste $z$. Com o **degrau**, a saída quase sempre não muda nada, e de repente pula.
- Com a **sigmoide**, mudança pequena em $z$ dá mudança pequena na saída.

</v-clicks>

<div v-click class="conceito">

Sem "errou um pouco menos", não há como saber se um ajuste foi na direção certa. Precisamos de uma ativação **suave**.

</div>

---

# A sigmoide transforma z numa probabilidade

<Olho q="1" />

<div class="cols">
<div>

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

<table>
<thead><tr><th>z</th><th>σ(z)</th><th>leitura</th></tr></thead>
<tbody>
<tr v-click><td>−4</td><td>0,02</td><td>quase certo que é 0</td></tr>
<tr v-click><td>0</td><td>0,50</td><td>em cima do muro</td></tr>
<tr v-click><td>4</td><td>0,98</td><td>quase certo que é 1</td></tr>
</tbody>
</table>

</div>
<div>

<div v-click>

O neurônio continua o mesmo, só troca a ativação:

$$
z = \mathbf{w} \cdot \mathbf{x} + b \qquad \hat{y} = \sigma(z)
$$

</div>

<div v-click class="conceito">

Agora $\hat{y}$ é um número **entre 0 e 1**: a probabilidade que o neurônio dá à classe 1.

</div>

<div v-click class="fraco pequeno">

Um neurônio com sigmoide é a **regressão logística**.

</div>

</div>
</div>

---

# Na mão: a previsão de um neurônio sigmoide

<Olho q="1" />

<Neuronio :xs="['2', '1']" :ws="['0,4', '−0,6']" b="0,1" :z="$clicks >= 1 ? 'z = 0,3' : 'z = ?'" ativ="σ" :saida="$clicks >= 2 ? '0,574' : '?'" :legendas="false" :largura="640" />

<div v-click>

$$
z = 0{,}4 \cdot 2 + (-0{,}6) \cdot 1 + 0{,}1 = 0{,}3
$$

</div>

<div v-click>

$$
\hat{y} = \sigma(0{,}3) = \frac{1}{1 + e^{-0{,}3}} = 0{,}574
$$

</div>

<div v-click>

A resposta certa era $y = 1$. O neurônio deu 57% de chance. **Quão ruim é isso?**

</div>

---

# A perda mede quão ruim foi a previsão

<Olho q="2" />

**Entropia cruzada binária**, para um exemplo:

$$
L = -\big[\, y \ln \hat{y} + (1 - y) \ln (1 - \hat{y}) \,\big]
$$

<v-clicks>

- Se $y = 1$, o segundo termo some: sobra $L = -\ln \hat{y}$.
- Se $y = 0$, o primeiro termo some: sobra $L = -\ln (1 - \hat{y})$.
- No exemplo ($y = 1$, $\hat{y} = 0{,}574$): $L = -\ln 0{,}574 = 0{,}554$.

</v-clicks>

<div v-click class="conceito">

$L$ é $-\ln$ da probabilidade que o neurônio deu à **resposta certa**.

</div>

---
class: mexa
---

# Errar com confiança custa muito

<Olho q="2" />

<PerdaExplora />

<div v-click class="preveja">

A resposta é 1. Quanto custa prever 0,9? E prever 0,1? E 0,01?

</div>

<div v-click class="conceito">

Acertar com confiança custa quase zero. **Errar com confiança custa muito**, e o custo cresce sem limite.

</div>

---

# O custo é a perda média, e é ele que queremos baixar

<Olho q="2" />

Para $m$ exemplos:

$$
J(\mathbf{w}, b) = \frac{1}{m} \sum_{i=1}^{m} L^{(i)}
$$

<v-clicks>

- $J$ depende **só dos pesos e do viés**: os dados estão fixos.
- Cada posição dos botões dá um valor de $J$.
- **Treinar** é procurar a posição em que $J$ é menor.

</v-clicks>

<div v-click class="conceito">

"Para que lado girar cada botão?" virou uma pergunta de cálculo: **como $J$ muda quando $w_j$ muda?** Essa é a derivada $\dfrac{\partial J}{\partial w_j}$.

</div>

---

# Gradiente descendente: um passo contra a derivada

<Olho q="4" />

$$
w_j \leftarrow w_j - \eta\, \frac{\partial J}{\partial w_j}
$$

<v-clicks>

- Derivada **positiva**: subir $w_j$ aumenta o custo. Então **desça** $w_j$.
- Derivada **negativa**: subir $w_j$ diminui o custo. Então **suba** $w_j$.
- Derivada **perto de zero**: quase no fundo. O passo encolhe sozinho.

</v-clicks>

<div v-click class="fraco pequeno">

O conjunto das derivadas de todos os pesos é o **gradiente**.

</div>

---
class: mexa
---

# Desça o vale, um passo por clique

<Olho q="4" />

<DescidaGradiente />

<div v-click class="preveja">

Com $\eta = 0{,}4$ a descida é suave. O que acontece com $\eta = 1{,}7$? E com $1{,}9$?

</div>

<!--
η = 0,1: desce, devagar. η = 0,4: desce bem. η = 1,7: salta de um lado para o outro do vale, mas ainda fecha.
η = 1,9: cada salto vai mais longe que o anterior, e o custo sobe. A curva tem segunda derivada 1,1,
então o limite é η = 2/1,1 = 1,82.
-->

---
clicks: 4
---

# A perda depende do peso por uma cadeia de três elos

<Olho q="3" />

<Cadeia :caixas="['peso w', 'soma z', 'saída ŷ', 'perda L']" :ida="['z = w·x + b', 'ŷ = σ(z)', 'L = −ln ŷ …']" revela="ida" :passo="$clicks" />

<div v-click="4">

Mexer em $w_j$ mexe em $z$, que mexe em $\hat{y}$, que mexe em $L$. A **regra da cadeia** multiplica os três efeitos:

$$
\frac{\partial L}{\partial w_j} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z} \cdot \frac{\partial z}{\partial w_j}
$$

</div>

<!--
Como engrenagens: se a primeira gira a segunda 2 vezes mais rápido e a segunda gira a terceira 3 vezes,
a primeira gira a terceira 2 · 3 = 6 vezes.
-->

---

# Os três elos: cada função ao lado da sua derivada

<Olho q="3" />

<div class="elos">
<div class="cab"></div>
<div class="cab"><span class="ida">a função</span></div>
<div class="cab"><span class="volta">a derivada dela</span></div>
</div>

<div class="elos">
<div class="nome" v-click="1">

**Perda**, em relação à **saída** $\hat{y}$

</div>
<div class="f" v-click="1">

$$
L = -\big[\, y \ln \hat{y} + (1 - y) \ln (1 - \hat{y}) \,\big]
$$

</div>
<div class="d" v-click="2">

$$
\frac{\partial L}{\partial \hat{y}} = -\frac{y}{\hat{y}} + \frac{1 - y}{1 - \hat{y}} = \frac{\hat{y} - y}{\hat{y}\,(1 - \hat{y})}
$$

</div>
</div>

<div class="elos">
<div class="nome" v-click="3">

**Saída**, em relação à **soma** $z$

</div>
<div class="f" v-click="3">

$$
\hat{y} = \sigma(z) = \frac{1}{1 + e^{-z}}
$$

</div>
<div class="d" v-click="4">

$$
\frac{\partial \hat{y}}{\partial z} = \sigma(z)\,\big(1 - \sigma(z)\big) = \hat{y}\,(1 - \hat{y})
$$

</div>
</div>

<div class="elos">
<div class="nome" v-click="5">

**Soma**, em relação ao **peso** $w_j$

</div>
<div class="f" v-click="5">

$$
z = w_1 x_1 + \dots + w_j x_j + \dots + b
$$

</div>
<div class="d" v-click="6">

$$
\frac{\partial z}{\partial w_j} = x_j
$$

</div>
</div>

<div v-click="7" class="fraco pequeno">

Em cada linha, só a letra do denominador varia; o resto é tratado como constante.

</div>

<!--
Cada linha em dois cliques: primeiro a função (azul), depois a derivada (laranja).
Pergunte a derivada à turma antes de mostrar. Na soma, o único termo que contém w_j é w_j x_j.
-->

---

# Multiplicados, os elos se simplificam

<Olho q="3" />

$$
\frac{\partial L}{\partial w_j} = \frac{\hat{y} - y}{\textcolor{#8A99A5}{\hat{y}\,(1 - \hat{y})}} \cdot \textcolor{#8A99A5}{\hat{y}\,(1 - \hat{y})} \cdot x_j
$$

<div v-click>

Os dois fatores em cinza se cancelam:

$$
\boxed{\;\frac{\partial L}{\partial w_j} = (\hat{y} - y)\, x_j \qquad\qquad \frac{\partial L}{\partial b} = \hat{y} - y\;}
$$

</div>

<div v-click class="conceito">

A culpa de um peso é **o erro da saída vezes a entrada que passou por ele**.

</div>

<div v-click class="fraco pequeno">

Para o viés a conta é a mesma, com $\partial z / \partial b = 1$ no lugar de $x_j$.

</div>

---

# É a regra do perceptron, agora com um erro que tem tamanho

<Olho q="4" />

| | correção do peso | o erro |
|---|---|---|
| **Perceptron** | $w_j \leftarrow w_j + \eta\,(y - \hat{y})\,x_j$ | $-1$, $0$ ou $+1$ |
| **Neurônio sigmoide** | $w_j \leftarrow w_j - \eta\,(\hat{y} - y)\,x_j$ | qualquer valor entre $-1$ e $1$ |

<div v-click>

As duas linhas são a **mesma fórmula**: $-(\hat{y} - y) = (y - \hat{y})$.

</div>

<div v-click class="conceito">

A diferença está no erro: errou por pouco, corrige pouco. Errou feio, corrige muito.

</div>

---

# Na mão: um passo de gradiente

<Olho q="3 4" />

Mesmo neurônio: $w = (0{,}4;\ {-}0{,}6)$, $b = 0{,}1$, $x = (2;\ 1)$, $y = 1$, $\hat{y} = 0{,}574$. Taxa $\eta = 0{,}5$.

<div v-click>

**Erro da saída:** $\hat{y} - y = 0{,}574 - 1 = -0{,}426$

</div>

<div v-click>

**Gradientes** (erro vezes entrada):

$$
\frac{\partial L}{\partial w_1} = -0{,}426 \cdot 2 = -0{,}851 \qquad \frac{\partial L}{\partial w_2} = -0{,}426 \cdot 1 = -0{,}426 \qquad \frac{\partial L}{\partial b} = -0{,}426
$$

</div>

<div v-click>

**Correção:** $\;w_1 \leftarrow 0{,}4 - 0{,}5 \cdot (-0{,}851) = 0{,}826 \qquad w_2 \leftarrow -0{,}387 \qquad b \leftarrow 0{,}313$

</div>

<div v-click class="preveja">

Os três parâmetros subiram. A previsão nova vai ficar acima ou abaixo de 0,574?

</div>

<div v-click class="conta">

**Conferindo:** com os pesos novos, $z = 1{,}577$ e $\hat{y} = 0{,}829$. A perda caiu de $0{,}554$ para $0{,}188$.

</div>

---

# Em código: o mesmo passo

<<< @/snippets/g_passo.py {1-2|4-8|10|11|12-14|15-16|18-21}

<Saida v-click nome="g_passo" />

---

# Em código: treinar na porta E, com todos os exemplos

<<< @/snippets/g_treino_and.py {1-4|7|8|9|10-11|12-13|all}

<Saida v-click nome="g_treino_and" />

<div class="fraco pequeno">

`X @ w` faz a soma ponderada dos quatro exemplos de uma vez. O gradiente do custo é a **média** dos gradientes dos exemplos.

</div>

---

# O custo cai, e as previsões viram probabilidades

<div class="cols">
<div>

<img class="fig" src="/fig/custo-and.svg" style="width: 400px" />

</div>
<div>

<<< @/snippets/g_prev_and.py

<Saida v-click nome="g_prev_and" />

</div>
</div>

<div v-click>

Diferente do perceptron, o custo **nunca chega a zero**: sempre dá para ficar um pouco mais confiante.

</div>

---
class: sua-vez
---

# E se a resposta fosse 0?

Mesmo neurônio e mesmo exemplo: $w = (0{,}4;\ {-}0{,}6)$, $b = 0{,}1$, $x = (2;\ 1)$, $\hat{y} = 0{,}574$. Mas agora $y = 0$.

1. Quanto vale o erro da saída, $\hat{y} - y$?
2. Quais são os gradientes de $w_1$, $w_2$ e $b$?
3. Os pesos vão subir ou descer? Isso faz sentido?

<div v-click class="conta">

Erro: $0{,}574 - 0 = 0{,}574$. Gradientes: $0{,}574 \cdot 2 = 1{,}149$; $\;0{,}574 \cdot 1 = 0{,}574$; $\;0{,}574$.

</div>

<div v-click class="conta">

Gradientes positivos: os três **descem**. Faz sentido: $z$ precisa cair para $\hat{y}$ se aproximar de 0.

</div>

---

# E o XOR? O mesmo treino, agora numa função

<<< @/snippets/g_funcao.py {1|2-4|5-11|12}

<div class="fraco pequeno">

É o laço do slide anterior, sem mudar uma linha da conta: só ganhou nome e passou a receber os dados.

</div>

<div v-click class="preveja">

O neurônio sigmoide tem um erro com tamanho e desce o gradiente. Isso basta para aprender o XOR?

</div>

---
class: mexa
---

# Treine o neurônio sigmoide nas três portas

<NeuronioTreino />

<v-clicks>

- **E** e **OU**: o custo cai, e a região azul se ajusta aos pontos cheios.
- **XOR**: clique em +1000 quantas vezes quiser.

</v-clicks>

<!--
No XOR o custo fica em 0,693 = -ln 0,5, a linha tracejada, e os pesos não saem do zero.
-->

---

# O neurônio sigmoide também não aprende o XOR

<<< @/snippets/g_portas.py

<Saida v-click nome="g_portas" />

<div v-click class="cuidado">

No XOR o custo **não sai do lugar**. O neurônio responde 0,5 para as quatro entradas, o mesmo que não saber nada, e os pesos nem se mexem.

</div>

---

# Por que o gradiente não ajuda no XOR

Um passo só, a partir dos pesos em zero, olhando exemplo por exemplo:

<<< @/snippets/g_grad_xor_a.py {1-3|4|6-8}

<Saida v-click nome="g_grad_xor_a" />

---

# No XOR, os exemplos puxam em sentidos opostos

<Saida nome="g_grad_xor_a" />

<div v-click>

<<< @/snippets/g_grad_xor_b.py

<Saida nome="g_grad_xor_b" />

</div>

<v-clicks>

- Os exemplos **puxam em sentidos opostos**: $(1,1)$ quer baixar os pesos, $(0,1)$ e $(1,0)$ querem subir. Na média, dá zero.
- Não é azar do ponto de partida: a fronteira é $z = 0$, **uma reta**, com degrau ou com sigmoide.

</v-clicks>

---

# O neurônio sigmoide nas quatro perguntas

<div class="quatro">
<div>

<span class="num">1</span> **Prever**

$\hat{y} = \sigma(\mathbf{w} \cdot \mathbf{x} + b)$

</div>
<div>

<span class="num">2</span> **Medir**

Entropia cruzada: $L = -\ln$ da probabilidade dada à resposta certa

</div>
<div>

<span class="num">3</span> **Atribuir**

Regra da cadeia: $\dfrac{\partial L}{\partial w_j} = (\hat{y} - y)\,x_j$

</div>
<div>

<span class="num">4</span> **Corrigir**

$w_j \leftarrow w_j - \eta\,\dfrac{\partial L}{\partial w_j}$

</div>
</div>

<div v-click class="cuidado">

Um defeito ficou: a fronteira ainda é $z = 0$, **uma reta**. O XOR continua fora de alcance.

</div>
