"""Regressão logística com numpy — o que o capítulo 13 ensina.

As seções 13.1, 13.2 e 13.3 escrevem estas funções inline num chunk; as seções
13.3, 13.4 e 13.5 importam daqui O MESMO código. O módulo é o chunk salvo em
arquivo.

Os dados (200 usuários: anos de experiência, salário, conta paga) moram em
`scratch/logistic_regression.py` e entram aqui como arrays. É a única razão
para um arquivo de `scratch_np/` importar `scratch.`: dado, nunca função.

Ao contrário de `statistics.py` e de `multiple_regression.py`, este módulo NÃO
precisa de `plt.close("all")`: o módulo do Grus importa `pyplot` no topo, mas
todas as chamadas de desenho dele estão dentro de `main()`, que não roda no
import. Conferido: `plt.get_fignums()` volta vazio depois de importá-lo.

Convenções: `X` tem forma (n, d), `y` tem forma (n,), `beta` tem forma (d,).
`logistic` e `logistic_prime` são deliberadamente polimórficas — aceitam um
escalar ou um array e devolvem o que receberam —, porque a 13.2 desenha a curva
com uma chamada só sobre a grade inteira e a 13.4 avalia os 66 pontos de teste
de uma vez. As funções de perda e de gradiente sempre recebem a matriz.

Este código NÃO é numericamente estável, e isso é deliberado: `np.log(0.0)` é
`-inf`, `0 * -inf` é `nan`, e a seção 13.3 existe para mostrar o que acontece
quando um desses aparece sem parar o programa. O callout da 13.2 explica o que
uma biblioteca séria faria no lugar.
"""
import numpy as np

from scratch import logistic_regression as _grus

# 200 usuários: [anos de experiência, salário, conta paga]
data: np.ndarray = np.array(_grus.data, dtype=float)

# xs tem a coluna de 1 na frente, pela convenção do capítulo 12
xs: np.ndarray = np.array(_grus.xs, dtype=float)    # (200, 3): [1, experiência, salário]
ys: np.ndarray = np.array(_grus.ys, dtype=float)    # (200,): conta paga, 0 ou 1

assert data.shape == (200, 3)
assert xs.shape == (200, 3) and ys.shape == (200,)
assert xs[0].tolist() == [1.0, 0.7, 48000.0] and ys[0] == 1.0
assert ys.sum() == 52       # 52 dos 200 usuários pagaram


def logistic(x):
    """A função logística. Aceita um escalar ou um array."""
    return 1.0 / (1 + np.exp(-x))


def logistic_prime(x):
    """A derivada da logística, escrita em função dela mesma."""
    y = logistic(x)
    return y * (1 - y)


assert logistic(0.0) == 0.5
assert np.allclose(logistic(np.array([-2.0, 0.0, 2.0])),
                   [0.11920292, 0.5, 0.88079708])
assert np.isclose(logistic_prime(0.0), 0.25)


def _negative_log_likelihood(x: np.ndarray, y: float, beta: np.ndarray) -> float:
    """A log-verossimilhança negativa de UM ponto.

    A versão vetorizada abaixo é a que o livro usa para ajustar. Esta existe
    porque as duas discordam exatamente onde o modelo satura, e a seção 13.3 vive
    dessa discordância: aqui o `if` evita calcular `log(1 - p)` quando y é 1, e
    lá as duas parcelas são sempre calculadas.
    """
    if y == 1:
        return float(-np.log(logistic(x @ beta)))
    else:
        return float(-np.log(1 - logistic(x @ beta)))


def negative_log_likelihood(X: np.ndarray, y: np.ndarray, beta: np.ndarray) -> float:
    """A log-verossimilhança negativa do conjunto inteiro."""
    p = logistic(X @ beta)
    return float(-np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)))


def negative_log_gradient(X: np.ndarray, y: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """O gradiente da log-verossimilhança negativa, somado sobre os pontos.

    A j-ésima parcial de um ponto é `(p_i - y_i) * x_ij`; somar sobre os pontos é
    o `X.T @ (...)` da seção 12.3.
    """
    return X.T @ (logistic(X @ beta) - y)


# quatro pontos inventados, longe da saturação, para conferir as duas funções
_X = np.array([[1.0, 0.5, -1.0],
               [1.0, -0.5, 2.0],
               [1.0, 1.5, 0.5],
               [1.0, -1.0, -0.5]])
_y = np.array([1.0, 0.0, 1.0, 0.0])
_b = np.array([0.1, 0.4, -0.3])

# a versão vetorizada é a soma das versões por ponto
assert np.isclose(negative_log_likelihood(_X, _y, _b),
                  sum(_negative_log_likelihood(_X[i], _y[i], _b)
                      for i in range(len(_y))))

# e o gradiente bate com a derivada numérica, coordenada a coordenada
_h = 1e-6
_numerico = np.array([
    (negative_log_likelihood(_X, _y, _b + _h * np.eye(3)[j])
     - negative_log_likelihood(_X, _y, _b - _h * np.eye(3)[j])) / (2 * _h)
    for j in range(3)
])
assert np.allclose(negative_log_gradient(_X, _y, _b), _numerico, atol=1e-6)
