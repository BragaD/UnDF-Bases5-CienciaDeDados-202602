---
layout: secao
---

<span class="parte">Parte 6 · 40 min</span>

# Treinar de verdade

Do exemplo de quatro pontos a imagens de dígitos escritos à mão.

---

# O problema: reconhecer dígitos escritos à mão

<img class="fig" src="/fig/digitos.svg" style="width: 860px" />

<v-clicks>

- 1.797 imagens de $8 \times 8$ pixels: **64 entradas**, cada uma a intensidade de um pixel.
- **10 classes**: os dígitos de 0 a 9.
- Rede 64-32-10: camada oculta com **ReLU**, saída com **softmax**.

</v-clicks>

---

# Preparar os dados

<<< @/snippets/t_dados.py {1-2|4-6|7|all}

<Saida v-click nome="t_dados" />

<div class="fraco pequeno">

A rede treina numa parte e é avaliada na outra, que ela nunca viu.

</div>

---

# Lote, minilote, um por vez

<Olho q="4" />

Quantos exemplos entram em **cada passo** de correção?

<table>
<thead><tr><th></th><th>exemplos por passo</th><th>o gradiente</th><th>passos por época</th></tr></thead>
<tbody>
<tr v-click><td><b>Lote inteiro</b></td><td>todos</td><td>exato, caro</td><td>1</td></tr>
<tr v-click><td><b>Estocástico</b></td><td>1</td><td>barato, ruidoso</td><td>um por exemplo</td></tr>
<tr v-click><td><b>Minilote</b></td><td>16 a 256</td><td>meio-termo</td><td>dezenas</td></tr>
</tbody>
</table>

<div v-click class="conceito">

Na prática se usa o **minilote**: o gradiente é a **média** dos gradientes dos exemplos do lote, e as contas viram operações de matriz.

</div>

<div v-click class="fraco pequeno">

Uma **época** continua sendo uma passada por todos os exemplos de treino.

</div>

---

# As peças da rede 64-32-10

<<< @/snippets/t_pecas.py {1-2|4-6|8-12|all}

<Saida v-click nome="t_pecas" />

---

# Com um lote, cada linha da matriz é um exemplo

<Olho q="1" />

<<< @/snippets/t_lote_ida.py {1|3-4|5-6|all}

<Saida v-click nome="t_lote_ida" />

<v-clicks>

- Com um exemplo por linha, a conta da camada vira `X @ W.T`: o mesmo $W a + b$, para as 32 linhas de uma vez.
- Antes de treinar, as dez probabilidades não dizem nada.

</v-clicks>

---

# A volta do lote: as mesmas quatro equações

<Olho q="3" />

<<< @/snippets/t_lote_volta.py {1-2|4|5-6|7|8-9|all}

<Saida v-click nome="t_lote_volta" />

<div class="fraco pequeno">

Cada gradiente tem a forma da matriz que ele corrige. Conferir as formas pega metade dos erros de quem programa uma rede.

</div>

---

# O laço de treino completo

<<< @/snippets/t_treinar.py {2-5|7-10|11-12|13-14|15-16|17-18|all}{maxHeight:'420px'}

<style>
.slidev-layout { --slidev-code-font-size: 12px; }
</style>

---

# A rede escrita à mão acerta quase todos os dígitos de teste

<div class="cols c55">
<div>

<<< @/snippets/t_resultado.py {1-2|4-7|9-12}

<Saida v-click nome="t_resultado" />

</div>
<div>

<img class="fig" src="/fig/custo-digitos.svg" style="width: 360px" />

</div>
</div>

<div class="fraco pequeno">

Algumas dezenas de linhas de `numpy`, sem biblioteca de redes neurais: ida, volta e correção.

</div>

---

# Onde ela erra

<img class="fig" src="/fig/erros-digitos.svg" style="width: 880px" />

<Saida nome="t_erros_n" />

<div v-click>

Olhar os erros é o primeiro diagnóstico: vários desses dígitos confundiriam uma pessoa.

</div>

---

# A taxa de aprendizado decide se o treino funciona

<Olho q="4" />

<img class="fig" src="/fig/taxas.svg" style="width: 800px" />

<v-clicks>

- **Pequena demais**: aprende, mas levaria milhares de épocas.
- **Grande demais**: cada passo salta para o outro lado do vale, e o custo não cai.
- É o primeiro botão a ajustar quando uma rede não treina.

</v-clicks>

---

# Por que os pesos começam aleatórios

<v-clicks>

- Se todos os pesos começam **iguais** (zero, por exemplo), todos os neurônios de uma camada calculam a mesma coisa.
- Recebem o mesmo $\delta$, o mesmo gradiente, a mesma correção.
- Continuam iguais para sempre: a camada inteira vale por **um** neurônio.

</v-clicks>

<div v-click class="conceito">

Pesos iniciais **aleatórios e pequenos** quebram a simetria. Os vieses podem começar em zero.

</div>

<div v-click class="fraco pequeno">

O tamanho do sorteio importa: no código, $\sqrt{2 / n_{\text{entradas}}}$ (inicialização de He), a escolha usual com ReLU.

</div>

---

# Aprender demais: o risco de decorar o treino

Uma rede tem botões suficientes para **decorar** os exemplos de treino, ruído incluído.

<v-clicks>

- Sinal: o custo de treino continua caindo, e o de **validação** começa a subir.
- **Parada antecipada**: interromper o treino quando a validação para de melhorar.
- **Penalidade nos pesos** (L2): somar ao custo um termo que cresce com o tamanho dos pesos.
- ***Dropout***: a cada passo, desligar ao acaso uma parte dos neurônios.

</v-clicks>

---

# A mesma rede em cinco linhas de scikit-learn

<<< @/snippets/t_sklearn.py {1|3-4|5|7-10}

<Saida v-click nome="t_sklearn" />

<div v-click>

Por dentro, `fit` roda o mesmo laço: ida, volta, correção, lote após lote.

</div>

---

# Nas bibliotecas de redes profundas, a volta é automática

```python {1-7|9|10|11|12|13}
import torch

modelo = torch.nn.Sequential(
    torch.nn.Linear(64, 32), torch.nn.ReLU(),
    torch.nn.Linear(32, 10),
)
otimizador = torch.optim.SGD(modelo.parameters(), lr=0.1)

for X_lote, y_lote in lotes:
    perda = torch.nn.functional.cross_entropy(modelo(X_lote), y_lote)   # ida + perda
    otimizador.zero_grad()
    perda.backward()                                                    # a volta
    otimizador.step()                                                   # a correção
```

<v-clicks at="6">

- Você escreve **só a ida**. A biblioteca monta o grafo de contas e faz a volta: `perda.backward()`.
- É o grafo de $f = (x + y) \cdot z$ da Parte 5, com milhões de nós.

</v-clicks>

<div class="fraco menor">

Este trecho não é executado nestes slides.

</div>

---

# O que muda nas redes de hoje, e o que não muda

<div class="cols">
<div>

### Muda

<v-clicks>

- A **arquitetura**: convoluções para imagens, *transformers* para texto.
- O **tamanho**: de 9 parâmetros para bilhões.
- O **otimizador**: variações do gradiente descendente, como o Adam.
- O **hardware**: GPUs fazendo as multiplicações de matriz.

</v-clicks>

</div>
<div>

### Não muda

<v-clicks>

- A <span class="ida">**ida**</span>: somas ponderadas e ativações, camada por camada.
- Uma **perda** que mede o erro na saída.
- A <span class="volta">**volta**</span>: a regra da cadeia, de trás para a frente.
- A **correção**: um passo contra o gradiente.

</v-clicks>

</div>
</div>

---

# A aula em um slide

<table class="pequeno nq">
<thead><tr><th></th><th>Perceptron</th><th>Neurônio&nbsp;sigmoide</th><th>Rede multicamada</th></tr></thead>
<tbody>
<tr v-click><td><b>1 · Prever</b></td><td>degrau(w·x + b)</td><td>σ(w·x + b)</td><td>a ida, camada por camada</td></tr>
<tr v-click><td><b>2 · Medir</b></td><td>certo ou errado</td><td>entropia cruzada</td><td>entropia cruzada (com softmax, se K classes)</td></tr>
<tr v-click><td><b>3 · Atribuir</b></td><td>entradas ativas</td><td>(ŷ − y)·x</td><td>backpropagation: δ de quem recebe × a de quem envia</td></tr>
<tr v-click><td><b>4 · Corrigir</b></td><td style="white-space: nowrap">w ← w + η(y − ŷ)x</td><td>w ← w − η·∂L/∂w</td><td>o mesmo, em todos os pesos</td></tr>
</tbody>
</table>

<div v-click class="conceito">

Em toda a tabela, a correção de um peso é **o erro de quem recebe vezes o sinal de quem envia**.

</div>

---
class: sua-vez
---

# Para levar: explique sem fórmula

Em duas frases cada, para um colega que faltou à aula:

1. Por que um neurônio sozinho não aprende o XOR, e o que a camada oculta muda?
2. O que o backpropagation calcula, e o que ele **não** faz?
3. Sua rede não está aprendendo: o custo não cai. Quais são as duas primeiras coisas que você confere?

<div v-click class="conta">

1\. A fronteira de um neurônio é uma reta; a camada oculta cria coordenadas novas em que uma reta basta.

2\. Calcula o gradiente da perda para todos os pesos, com uma ida e uma volta. Quem corrige os pesos é o gradiente descendente.

3\. A taxa de aprendizado e as formas (e o gradiente, contra o método ingênuo).

</div>

---

# Para continuar

<div class="pequeno">

- **3Blue1Brown**, série *Neural Networks*: a intuição visual da ida, do gradiente e do backpropagation. [3blue1brown.com/topics/neural-networks](https://www.3blue1brown.com/topics/neural-networks)
- **Michael Nielsen**, *Neural Networks and Deep Learning*: o capítulo 2 deriva as quatro equações. [neuralnetworksanddeeplearning.com](http://neuralnetworksanddeeplearning.com)
- **Stanford CS231n**, notas de curso: grafos de contas e backpropagation. [cs231n.github.io](https://cs231n.github.io)
- **Andrej Karpathy**, *The spelled-out intro to neural networks and backpropagation*: um motor de derivadas escrito do zero. [github.com/karpathy/micrograd](https://github.com/karpathy/micrograd)
- **DeepLearning.AI**, *Neural Networks and Deep Learning* (Andrew Ng): do neurônio logístico às redes profundas, com a notação $W^{[l]}$ usada aqui.
- **MIT 6.S191**, *Introduction to Deep Learning*: [introtodeeplearning.com](http://introtodeeplearning.com)

</div>

<div class="fraco menor">

Artigos originais: Rosenblatt (1958), *The perceptron*; Minsky e Papert (1969), *Perceptrons*; Rumelhart, Hinton e Williams (1986), *Learning representations by back-propagating errors*.

</div>
