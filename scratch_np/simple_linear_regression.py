"""Regressão linear simples com numpy — o que o capítulo 11 ensina.

A seção 11.1 escreve `predict`, `error`, `sum_of_sqerrors`, `least_squares_fit`,
`total_sum_of_squares` e `r_squared` inline; as seções 11.2 e 11.3 — e o
capítulo 12 — importam daqui O MESMO código. O módulo é o chunk salvo em
arquivo.

Como no Grus, o ajuste sobre os dados da DataSciencester acontece no import:
`alpha` e `beta` são os valores de mínimos quadrados sobre `num_friends_good` e
`daily_minutes_good`, e os quatro arrays de dados são reexportados daqui para
que a 11.2 e a 11.3 importem tudo de um lugar só. Os `assert`s no nível do
módulo são a suíte do próprio livro: o import é o teste.

Convenções: `x` e `y` têm forma (n,); `ddof=1` onde o Grus usa a fórmula
amostral (`standard_deviation`); as funções que devolvem escalar devolvem
`float`, não `np.float64`, para a saída na tela ser a do Python.
"""
from typing import Tuple

import numpy as np

from scratch_np.statistics import (num_friends, daily_minutes,
                                   num_friends_good, daily_minutes_good)


def predict(alpha: float, beta: float, x):
    """beta * x + alpha. Escalar -> float; array -> array."""
    return beta * x + alpha


def error(alpha: float, beta: float, x, y):
    """
    O erro ao prever beta * x + alpha
    quando o valor real é y
    """
    return predict(alpha, beta, x) - y


def sum_of_sqerrors(alpha: float, beta: float,
                    x: np.ndarray, y: np.ndarray) -> float:
    return float(np.sum(error(alpha, beta, x, y) ** 2))


def least_squares_fit(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
    """
    Dados dois arrays x e y,
    encontra os valores de alpha e beta de mínimos quadrados
    """
    beta = np.corrcoef(x, y)[0, 1] * np.std(y, ddof=1) / np.std(x, ddof=1)
    alpha = y.mean() - beta * x.mean()
    return float(alpha), float(beta)


# Uma reta perfeita: y = 3x - 5. A igualdade é exata — ver o plano/seção 11.1.
_x = np.arange(-100, 110, 10)
_y = 3 * _x - 5
assert least_squares_fit(_x, _y) == (-5, 3)

alpha, beta = least_squares_fit(num_friends_good, daily_minutes_good)
assert 22.9 < alpha < 23.0
assert 0.9 < beta < 0.905


def total_sum_of_squares(y: np.ndarray) -> float:
    """a variação quadrática total dos y_i em torno da média deles"""
    return float(np.sum((y - y.mean()) ** 2))


def r_squared(alpha: float, beta: float,
              x: np.ndarray, y: np.ndarray) -> float:
    """
    a fração da variação em y capturada pelo modelo, que é igual a
    1 menos a fração da variação em y NÃO capturada pelo modelo
    """
    return 1.0 - (sum_of_sqerrors(alpha, beta, x, y) /
                  total_sum_of_squares(y))


rsq = r_squared(alpha, beta, num_friends_good, daily_minutes_good)
assert 0.328 < rsq < 0.330
