# Antes do capítulo: o Colab e o ambiente

Esta parte não existe no livro — ela é sobre a **ferramenta**, não sobre o
conteúdo. São dez minutos, e depois deles você consegue abrir qualquer capítulo
da disciplina e executar tudo.

## O que a célula acima fez

O **Google Colab** roda Python numa máquina do Google, pelo navegador. Nada para
instalar. Mas essa máquina começa vazia: não tem o código nem os dados da
disciplina.

Por isso todo notebook daqui abre com aquela célula. Ela procura o projeto na
máquina e, se não achar, baixa uma cópia — e depois muda o diretório de trabalho
para a raiz dele. É isso que faz `from scratch...` e `"dados/..."` funcionarem
nas células seguintes.

Se você reiniciar o ambiente, rode-a de novo antes de qualquer outra.

```{python}
import os

print("estou em:", os.getcwd())
print("scratch/ existe:", os.path.isdir("scratch"))
print("dados/ existe:  ", os.path.isdir("dados"))
```

## Executando células

Um notebook é uma sequência de **células**: as de texto (como esta) e as de
código. Para executar uma célula de código, clique nela e aperte
**Shift + Enter**.

```{python}
print("Se você está lendo esta linha, a célula rodou.")
```

::: {.callout-warning}
## A ordem é a da execução, não a da tela

As células compartilham um mesmo interpretador, e cada uma enxerga o que as
anteriores definiram. Mas quem manda é a **ordem em que você executou**, não a
ordem em que elas aparecem na página.

Rodar fora de ordem, ou editar uma célula lá em cima sem executá-la de novo,
produz um estado que não corresponde ao que está escrito. É o defeito mais comum
de quem trabalha com notebook, e ele não levanta erro: devolve resposta errada.

Quando desconfiar, use **Ambiente de execução → Reiniciar sessão e executar
tudo**. É o botão que devolve o notebook ao que o texto dele diz.
:::

## O que é diferente aqui

Se você já usou Python para dados, provavelmente usou `numpy` e `pandas`. Nesta
disciplina, **não**. Os algoritmos são construídos do zero, e é essa a razão de
ser da matéria.

Veja o que é um vetor neste curso:

```{python}
from scratch.linear_algebra import Vector, dot, distance

# Vector não é uma classe nova: é um apelido para List[float].
print("Vector é:", Vector)
print("produto escalar:", dot([3, -1, 2], [1, 4, -2]))
print("distância:", distance([0, 0], [3, 4]))
```

E o produto escalar, por dentro, é um `sum` sobre um `zip`:

```python
def dot(v: Vector, w: Vector) -> float:
    """Calcula v_1 * w_1 + ... + v_n * w_n"""
    assert len(v) == len(w), "vetores devem ter o mesmo comprimento"
    return sum(v_i * w_i for v_i, w_i in zip(v, w))
```

É mais lento que a versão de biblioteca, e é mais lento de propósito: a lentidão
é o preço da transparência. O `numpy` faria a mesma conta muito mais rápido, e
você não veria conta nenhuma.

## O `assert` é o idioma da casa

O código da disciplina usa `assert` o tempo todo, como especificação executável:
a afirmação diz o que a função deveria fazer, e quebra na hora em que ela para de
fazer.

A célula abaixo não imprime nada além da última linha — e é esse o ponto: nenhuma
afirmação falhou.

```{python}
from scratch.linear_algebra import add, subtract, magnitude

assert add([1, 2, 3], [4, 5, 6]) == [5, 7, 9]
assert subtract([5, 7, 9], [4, 5, 6]) == [1, 2, 3]
assert magnitude([3, 4]) == 5

print("todos os asserts passaram")
```

## Todo sorteio leva semente

Metade do livro é aleatória — divisão treino/teste, inicialização de pesos,
gradiente estocástico, k-means. **Todo trecho que sorteia fixa a semente antes.**

Sem isso, cada execução dá um número diferente, e aí não há como saber se a
diferença que você viu veio do método ou do sorteio.

```{python}
import random

random.seed(42)
print("com semente 42:", [round(random.random(), 4) for _ in range(3)])

random.seed(42)
print("de novo, 42:   ", [round(random.random(), 4) for _ in range(3)])

random.seed(99)
print("com semente 99:", [round(random.random(), 4) for _ in range(3)])
```

O livro usa o `random` da biblioteca padrão, não o `numpy.random`. São geradores
**independentes**: fixar a semente de um não fixa a do outro.

::: {.callout-tip}
## Salve o seu trabalho no Drive

Ao abrir um notebook da disciplina, o Colab mostra uma cópia **somente leitura**.
Para editar e guardar o que você fez, use **Arquivo → Salvar uma cópia no Drive**.

Entre com a **conta institucional**: o Colab salva no Drive da conta com que você
entrou, e aí o seu trabalho fica acessível de qualquer computador — o do
laboratório, o de casa — sem pen drive e sem anexar arquivo em e-mail.

Uma consequência que vale saber: quando o material for atualizado, a **sua** cópia
não muda. Para pegar a versão nova de um capítulo, abra o link do Colab de novo.
:::

Pronto. O capítulo começa aqui.
