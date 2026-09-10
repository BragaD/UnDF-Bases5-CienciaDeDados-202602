"""Gradiente descendente em numpy — a versão em arrays do capítulo 5.

O capítulo 5 ensina `gradient_step` sobre listas (`scratch/gradient_descent.py`):
`add(v, scalar_multiply(step_size, gradient))`. Com arrays isso é uma linha,
`v + step_size * gradient`, e a convenção de sinal é a mesma: passo negativo
desce (minimiza), passo positivo sobe (maximiza).
"""
from typing import Iterator

import numpy as np


def gradient_step(v: np.ndarray, gradient: np.ndarray, step_size: float) -> np.ndarray:
    """Anda `step_size` na direção de `gradient` a partir de `v`.

    Passo negativo = descida, positivo = subida — a convenção do capítulo 5.
    """
    v = np.asarray(v, dtype=float)
    gradient = np.asarray(gradient, dtype=float)
    assert v.shape == gradient.shape, "v e gradient precisam ter a mesma forma"
    return v + step_size * gradient


assert np.array_equal(
    gradient_step(np.array([1.0, 2.0]), np.array([1.0, 1.0]), -0.5),
    np.array([0.5, 1.5]),
)


def minibatches(n: int,
                batch_size: int,
                rng: np.random.Generator,
                shuffle: bool = True) -> Iterator[np.ndarray]:
    """Gera arrays de índices de tamanho `batch_size` cobrindo 0..n-1.

    Quem chama fatia os dados: `X[idx], y[idx]`. Como no Grus, o que se
    embaralha é a ORDEM DOS LOTES, não os pontos dentro deles; e a semente é
    decisão de quem chama — o `rng` é obrigatório.
    """
    starts = np.arange(0, n, batch_size)
    if shuffle:
        starts = rng.permutation(starts)
    for start in starts:
        yield np.arange(start, min(start + batch_size, n))


_lotes = list(minibatches(10, 4, np.random.default_rng(0), shuffle=False))
assert [len(lote) for lote in _lotes] == [4, 4, 2]
assert np.array_equal(np.concatenate(_lotes), np.arange(10))
