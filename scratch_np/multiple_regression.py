"""Regressão múltipla com numpy — o que o capítulo 12 ensina.

As seções 12.3, 12.5, 12.6, 12.7 e 12.8 escrevem estas funções inline num
chunk; as seções seguintes — e o capítulo 13 — importam daqui O MESMO código.
O módulo é o chunk salvo em arquivo.

Os dados (`inputs`: 203 linhas de [1, amigos, horas de trabalho, doutorado])
moram em `scratch/multiple_regression.py` e entram aqui como array. É a única
razão para um arquivo de `scratch_np/` importar `scratch.`: dado, nunca função.

Importar o módulo do Grus tem dois efeitos colaterais, e nenhum se corrige
editando o pacote vendorizado. Ele desenha figuras (via `scratch.statistics` e
`scratch.probability`) — daí o `plt.close("all")`. E ele roda, no nível do
módulo, um bootstrap de medianas com o `random` da stdlib SEM semente: os dois
`assert` daquele bootstrap são robustos, mas o sorteio não é reprodutível. O
`random.seed(0)` abaixo o torna reprodutível. É a única linha de `random` da
stdlib deste pacote, e existe só para o import ser determinístico.

Convenções: `X` tem forma (n, d), `y` tem forma (n,), `beta` tem forma (d,).
As funções que devolvem escalar devolvem `float`, com uma exceção deliberada:
`predict`, `error` e `squared_error` aceitam um ponto (d,) OU uma matriz
(n, d) e devolvem, respectivamente, um escalar ou um array de n valores. É
essa polimorfia que faz `multiple_r_squared` caber numa linha.
"""
import random
from typing import Callable

import numpy as np
from matplotlib import pyplot as plt

# ver o docstring: sem isto, o import sorteia
random.seed(0)
from scratch import multiple_regression as _grus

plt.close("all")

from scratch_np.gradient_descent import gradient_step
from scratch_np.probability import normal_cdf
from scratch_np.simple_linear_regression import total_sum_of_squares

# 203 usuários: [1, número de amigos, horas de trabalho por dia, tem doutorado]
inputs: np.ndarray = np.array(_grus.inputs, dtype=float)

assert inputs.shape == (203, 4)
assert inputs[0].tolist() == [1.0, 49.0, 4.0, 0.0]


def predict(x: np.ndarray, beta: np.ndarray):
    """assume que o primeiro elemento de x é 1"""
    return x @ beta


def error(x: np.ndarray, y, beta: np.ndarray):
    return predict(x, beta) - y


def squared_error(x: np.ndarray, y, beta: np.ndarray):
    return error(x, y, beta) ** 2


_x = np.array([1.0, 2.0, 3.0])
_y = 30.0
_beta = np.array([4.0, 4.0, 4.0])   # previsão = 4 + 8 + 12 = 24

assert error(_x, _y, _beta) == -6
assert squared_error(_x, _y, _beta) == 36


def sqerror_gradient(x: np.ndarray, y: float, beta: np.ndarray) -> np.ndarray:
    """o gradiente do erro quadrático de UM ponto x, com forma (d,)"""
    return 2 * error(x, y, beta) * x


assert np.array_equal(sqerror_gradient(_x, _y, _beta), [-12, -24, -36])


def least_squares_fit(xs: np.ndarray,
                      ys: np.ndarray,
                      rng: np.random.Generator,
                      learning_rate: float = 0.001,
                      num_steps: int = 1000,
                      batch_size: int = 1) -> np.ndarray:
    """
    Encontra o beta que minimiza a soma dos erros ao quadrado,
    supondo o modelo y = x @ beta.
    """
    # Começa com um chute aleatório
    guess = rng.random(xs.shape[1])

    for _ in range(num_steps):
        for start in range(0, len(xs), batch_size):
            batch_xs = xs[start:start + batch_size]
            batch_ys = ys[start:start + batch_size]

            # a média, sobre o lote, de 2 * erro_i * x_i
            erros = batch_xs @ guess - batch_ys
            gradient = 2 * batch_xs.T @ erros / len(batch_xs)

            guess = gradient_step(guess, gradient, -learning_rate)

    return guess


def multiple_r_squared(xs: np.ndarray, ys: np.ndarray, beta: np.ndarray) -> float:
    sum_of_squared_errors = float(np.sum(error(xs, ys, beta) ** 2))
    return 1.0 - sum_of_squared_errors / total_sum_of_squares(ys)


def bootstrap_sample(data: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """sorteia len(data) linhas de data, com reposição"""
    return data[rng.integers(0, len(data), len(data))]


def bootstrap_statistic(data: np.ndarray,
                        stats_fn: Callable,
                        num_samples: int,
                        rng: np.random.Generator) -> np.ndarray:
    """avalia stats_fn sobre num_samples amostras bootstrap de data"""
    return np.array([stats_fn(bootstrap_sample(data, rng))
                     for _ in range(num_samples)])


# 101 pontos todos perto de 100; e 101 pontos, 50 perto de 0 e 50 perto de 200
_rng = np.random.default_rng(0)
_close_to_100 = 99.5 + _rng.random(101)
_far_from_100 = np.concatenate([99.5 + _rng.random(1),
                                _rng.random(50),
                                200 + _rng.random(50)])

_rng = np.random.default_rng(0)
assert np.std(bootstrap_statistic(_close_to_100, np.median, 100, _rng), ddof=1) < 1
assert np.std(bootstrap_statistic(_far_from_100, np.median, 100, _rng), ddof=1) > 90


def p_value(beta_hat_j: float, sigma_hat_j: float) -> float:
    if beta_hat_j > 0:
        # se o coeficiente é positivo, precisamos calcular o dobro da
        # probabilidade de ver um valor ainda *maior*
        return float(2 * (1 - normal_cdf(beta_hat_j / sigma_hat_j)))
    else:
        # caso contrário, o dobro da probabilidade de ver um valor *menor*
        return float(2 * normal_cdf(beta_hat_j / sigma_hat_j))


assert p_value(30.58, 1.27)   < 0.001  # termo constante
assert p_value(0.972, 0.103)  < 0.001  # amigos
assert p_value(-1.865, 0.155) < 0.001  # horas de trabalho
assert p_value(0.923, 1.249)  > 0.4    # doutorado


# alpha é um *hiperparâmetro* que controla a força da penalidade.
# Às vezes ele é chamado de "lambda", mas isso já significa algo em Python.
def ridge_penalty(beta: np.ndarray, alpha: float) -> float:
    return float(alpha * (beta[1:] @ beta[1:]))


def squared_error_ridge(x: np.ndarray, y: float,
                        beta: np.ndarray, alpha: float) -> float:
    """erro estimado mais a penalidade ridge sobre beta"""
    return error(x, y, beta) ** 2 + ridge_penalty(beta, alpha)


def ridge_penalty_gradient(beta: np.ndarray, alpha: float) -> np.ndarray:
    """gradiente apenas da penalidade ridge"""
    return np.concatenate([[0.0], 2 * alpha * beta[1:]])


def sqerror_ridge_gradient(x: np.ndarray, y: float,
                           beta: np.ndarray, alpha: float) -> np.ndarray:
    """
    o gradiente correspondente ao i-ésimo termo de erro quadrático,
    incluindo a penalidade ridge
    """
    return sqerror_gradient(x, y, beta) + ridge_penalty_gradient(beta, alpha)


def least_squares_fit_ridge(xs: np.ndarray,
                            ys: np.ndarray,
                            alpha: float,
                            rng: np.random.Generator,
                            learning_rate: float = 0.001,
                            num_steps: int = 1000,
                            batch_size: int = 1) -> np.ndarray:
    guess = rng.random(xs.shape[1])

    for _ in range(num_steps):
        for start in range(0, len(xs), batch_size):
            batch_xs = xs[start:start + batch_size]
            batch_ys = ys[start:start + batch_size]

            # a penalidade não depende do ponto: a média dela sobre o lote é
            # ela mesma, e por isso ela entra somada uma vez só
            erros = batch_xs @ guess - batch_ys
            gradient = (2 * batch_xs.T @ erros / len(batch_xs)
                        + ridge_penalty_gradient(guess, alpha))

            guess = gradient_step(guess, gradient, -learning_rate)

    return guess


def lasso_penalty(beta: np.ndarray, alpha: float) -> float:
    return float(alpha * np.abs(beta[1:]).sum())


# estes dois não são do Grus: são a conferência do módulo, com números exatos
assert ridge_penalty(np.array([0.0, 3.0, 4.0]), 1.0) == 25
assert lasso_penalty(np.array([0.0, 3.0, -4.0]), 1.0) == 7
