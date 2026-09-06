"""Divisão treino/teste e métricas — o que o capítulo 8 ensina.

O capítulo 8 escreve este código inline; os capítulos 9, 10 e 13 importam daqui.
Toda função estocástica recebe o `rng` como parâmetro obrigatório: a semente é
decisão visível de quem chama, nunca estado global.
"""
from typing import Sequence, Tuple, TypeVar

import numpy as np

X = TypeVar("X")  # um ponto de dado qualquer


def split_data(data, prob: float, rng: np.random.Generator):
    """Divide `data` nas frações [prob, 1 - prob], em ordem sorteada.

    Array -> dois arrays, fatiados pelas mesmas linhas.
    Sequência qualquer (lista de mensagens, de pontos rotulados) -> duas listas.
    """
    idx = rng.permutation(len(data))       # uma permutação dos índices...
    cut = int(len(data) * prob)            # ...cortada na proporção pedida
    if isinstance(data, np.ndarray):
        return data[idx[:cut]], data[idx[cut:]]
    return [data[i] for i in idx[:cut]], [data[i] for i in idx[cut:]]


_dados = np.arange(1000)
_treino, _teste = split_data(_dados, 0.75, np.random.default_rng(0))
assert len(_treino) == 750 and len(_teste) == 250
assert np.array_equal(np.sort(np.concatenate([_treino, _teste])), _dados)

_lista = list(range(1000))
_treino_l, _teste_l = split_data(_lista, 0.75, np.random.default_rng(0))
assert len(_treino_l) == 750 and sorted(_treino_l + _teste_l) == _lista


def train_test_split(xs: np.ndarray,
                     ys: np.ndarray,
                     test_pct: float,
                     rng: np.random.Generator
                     ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """-> (x_train, x_test, y_train, y_test), fatiados pelos MESMOS índices."""
    xs = np.asarray(xs)
    ys = np.asarray(ys)
    assert len(xs) == len(ys), "xs e ys precisam ter o mesmo número de linhas"
    train_idx, test_idx = split_data(np.arange(len(xs)), 1 - test_pct, rng)
    return xs[train_idx], xs[test_idx], ys[train_idx], ys[test_idx]


_xs = np.arange(1000)
_ys = 2 * _xs
_x_tr, _x_te, _y_tr, _y_te = train_test_split(_xs, _ys, 0.25, np.random.default_rng(0))
assert len(_x_tr) == len(_y_tr) == 750
assert len(_x_te) == len(_y_te) == 250
assert np.all(_y_tr == 2 * _x_tr) and np.all(_y_te == 2 * _x_te)


def accuracy(tp: int, fp: int, fn: int, tn: int) -> float:
    correct = tp + tn
    total = tp + fp + fn + tn
    return correct / total


assert accuracy(70, 4930, 13930, 981070) == 0.98114


def precision(tp: int, fp: int, fn: int, tn: int) -> float:
    return tp / (tp + fp)


assert precision(70, 4930, 13930, 981070) == 0.014


def recall(tp: int, fp: int, fn: int, tn: int) -> float:
    return tp / (tp + fn)


assert recall(70, 4930, 13930, 981070) == 0.005


def f1_score(tp: int, fp: int, fn: int, tn: int) -> float:
    p = precision(tp, fp, fn, tn)
    r = recall(tp, fp, fn, tn)
    return 2 * p * r / (p + r)
