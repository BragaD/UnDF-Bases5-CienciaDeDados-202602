"""A normal, vetorizada — `normal_cdf` e a inversa por busca binária.

O capítulo 6 do Grus (Probabilidade) está fora da ementa, mas os capítulos 7,
12 e 16 precisam destas duas funções. São as do Grus, aceitando arrays: a
busca binária da inversa roda para todos os elementos de uma vez, cada um com
o seu próprio intervalo, apertado por `np.where`.
"""
import math

import numpy as np

_erf = np.vectorize(math.erf, otypes=[float])


def _normal_cdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    return (1 + _erf((x - mu) / math.sqrt(2) / sigma)) / 2


def normal_cdf(x, mu: float = 0, sigma: float = 1):
    """P(X <= x) para X ~ Normal(mu, sigma). Escalar -> float; array -> array."""
    out = _normal_cdf(np.asarray(x, dtype=float), mu, sigma)
    return float(out) if out.ndim == 0 else out


assert abs(normal_cdf(0) - 0.5) < 1e-12
assert np.allclose(normal_cdf(np.array([-1.96, 1.96])), [0.025, 0.975], atol=1e-3)


def inverse_normal_cdf(p, mu: float = 0, sigma: float = 1, tolerance: float = 0.00001):
    """Inversa aproximada por busca binária, elemento a elemento em paralelo."""
    p = np.asarray(p, dtype=float)
    low_z = np.full(p.shape, -10.0)   # normal_cdf(-10) é (praticamente) 0
    hi_z = np.full(p.shape, 10.0)     # normal_cdf(10) é (praticamente) 1
    mid_z = (low_z + hi_z) / 2
    while np.any(hi_z - low_z > tolerance):
        mid_z = (low_z + hi_z) / 2                 # o ponto médio de cada intervalo
        mid_p = _normal_cdf(mid_z, 0, 1)           # e a cdf lá
        low_z = np.where(mid_p < p, mid_z, low_z)  # baixo demais: procura acima
        hi_z = np.where(mid_p < p, hi_z, mid_z)    # alto demais: procura abaixo
    z = mu + sigma * mid_z
    return float(z) if z.ndim == 0 else z


assert abs(inverse_normal_cdf(0.975) - 1.96) < 1e-3
assert abs(inverse_normal_cdf(0.5, mu=3, sigma=2) - 3) < 1e-3
assert np.allclose(inverse_normal_cdf(np.array([0.025, 0.5, 0.975])), [-1.96, 0, 1.96], atol=1e-3)
