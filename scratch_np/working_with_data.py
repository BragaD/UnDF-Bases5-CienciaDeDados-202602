"""Trabalhando com dados em numpy — a contraparte em arrays de `scratch/working_with_data.py`.

O módulo do Grus (capítulo 10) NÃO é importável neste projeto: abre `stocks.csv`
com caminho relativo ao cwd e afirma uma correlação sem semente, tudo no corpo
do módulo (`NAO_IMPORTAVEIS`, em tests/test_scratch.py). Este aqui é o mesmo
código, em arrays, sem efeito colateral no import: nenhum arquivo é lido,
nenhum sorteio sem semente é feito, nenhuma figura é desenhada.

Convenções: `X` tem forma (n, d) — uma linha por observação, uma coluna por
atributo; `ddof=1` onde o Grus usa a fórmula amostral (`standard_deviation`);
toda função estocástica recebe `rng: np.random.Generator` obrigatório.

O capítulo 7 escreve cada função inline na seção que a ensina; as seções e os
capítulos seguintes importam daqui O MESMO código. Os `assert`s abaixo rodam no
import — o render é o teste.
"""
import datetime
import re
from typing import List, NamedTuple, Optional, Tuple

import numpy as np
import tqdm
from dateutil.parser import parse
from matplotlib import pyplot as plt

from scratch_np.gradient_descent import gradient_step
from scratch_np.probability import inverse_normal_cdf


# --------------------------------------------------------------------------
# 7.1 Explorando seus dados
# --------------------------------------------------------------------------

def bucketize(points, bucket_size: float) -> np.ndarray:
    """Arredonda cada ponto para baixo até o múltiplo mais próximo de bucket_size"""
    return bucket_size * np.floor(np.asarray(points, dtype=float) / bucket_size)


def make_histogram(points, bucket_size: float) -> Tuple[np.ndarray, np.ndarray]:
    """Distribui os pontos nos buckets e conta quantos caem em cada um.

    Devolve dois arrays alinhados — os buckets, em ordem, e as contagens —,
    o par que `plt.bar` recebe direto. É o `Counter` do Grus, em arrays.
    """
    buckets, counts = np.unique(bucketize(points, bucket_size), return_counts=True)
    return buckets, counts


assert np.array_equal(bucketize([-3.2, 0.5, 7.9, 10.0], 5), [-5, 0, 5, 10])
_buckets, _counts = make_histogram([0.0, 10.0, 0.0, -10.0], 10)
assert np.array_equal(_buckets, [-10, 0, 10]) and np.array_equal(_counts, [1, 2, 1])


def plot_histogram(points, bucket_size: float, title: str = ""):
    buckets, counts = make_histogram(points, bucket_size)
    plt.bar(buckets, counts, width=bucket_size)
    plt.xlabel("valor")
    plt.ylabel("frequência")
    plt.title(title)


def random_normal(n: int, rng: np.random.Generator) -> np.ndarray:
    """n amostras da normal padrão, pela inversa da acumulada"""
    return inverse_normal_cdf(rng.random(n))


_amostra = random_normal(2000, np.random.default_rng(0))
assert _amostra.shape == (2000,)
assert abs(_amostra.mean()) < 0.1 and abs(_amostra.std(ddof=1) - 1) < 0.1


def correlation_matrix(X: np.ndarray) -> np.ndarray:
    """
    Devolve a matriz d x d cuja entrada (i, j) é a correlação
    entre a coluna i e a coluna j de X.

    `np.corrcoef` assume, por padrão, uma variável POR LINHA (`rowvar=True`);
    a convenção deste livro é uma variável por coluna — daí o `rowvar=False`.
    """
    return np.corrcoef(np.asarray(X, dtype=float), rowvar=False)


_X = np.array([[1.0, 2.0], [2.0, 4.0], [3.0, 6.5]])
_M = correlation_matrix(_X)
assert _M.shape == (2, 2) and np.allclose(np.diag(_M), 1)
assert np.isclose(_M[0, 1], np.corrcoef(_X[:, 0], _X[:, 1])[0, 1])


# --------------------------------------------------------------------------
# 7.2 NamedTuples e 7.4 Limpeza — o registro heterogêneo (texto, data, número)
# não é array; é o que fica de fora dele, de propósito.
# --------------------------------------------------------------------------

class StockPrice(NamedTuple):
    symbol: str
    date: datetime.date
    closing_price: float

    def is_high_tech(self) -> bool:
        """É uma classe — então também dá para acrescentar métodos"""
        return self.symbol in ['MSFT', 'GOOG', 'FB', 'AMZN', 'AAPL']


_price = StockPrice('MSFT', datetime.date(2018, 12, 14), 106.03)
assert _price.symbol == 'MSFT'
assert _price.closing_price == 106.03
assert _price.is_high_tech()


def parse_row(row: List[str]) -> StockPrice:
    symbol, date, closing_price = row
    return StockPrice(symbol=symbol,
                      date=parse(date).date(),
                      closing_price=float(closing_price))


_stock = parse_row(["MSFT", "2018-12-14", "106.03"])
assert _stock.symbol == "MSFT"
assert _stock.date == datetime.date(2018, 12, 14)
assert _stock.closing_price == 106.03


def try_parse_row(row: List[str]) -> Optional[StockPrice]:
    symbol, date_, closing_price_ = row

    # o símbolo da ação deveria ser só letras maiúsculas
    if not re.match(r"^[A-Z]+$", symbol):
        return None

    try:
        date = parse(date_).date()
    except ValueError:
        return None

    try:
        closing_price = float(closing_price_)
    except ValueError:
        return None

    return StockPrice(symbol, date, closing_price)


# deveria devolver None para erros
assert try_parse_row(["MSFT0", "2018-12-14", "106.03"]) is None  # símbolo ruim
assert try_parse_row(["MSFT", "2018-12--14", "106.03"]) is None  # data ruim
assert try_parse_row(["MSFT", "2018-12-14", "x"]) is None        # preço ruim

# mas deveria devolver o mesmo de antes se o dado é bom
assert try_parse_row(["MSFT", "2018-12-14", "106.03"]) == _stock


# --------------------------------------------------------------------------
# 7.5 Manipulando dados
# --------------------------------------------------------------------------

def day_over_day_changes(closes: np.ndarray) -> np.ndarray:
    """Variações percentuais dia a dia. Assume preços de uma única ação, em ordem."""
    closes = np.asarray(closes, dtype=float)
    return closes[1:] / closes[:-1] - 1


assert np.allclose(day_over_day_changes([100.0, 110.0, 99.0]), [0.1, -0.1])


# --------------------------------------------------------------------------
# 7.6 Reescalonamento
# --------------------------------------------------------------------------

def scale(X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """devolve a média e o desvio padrão de cada coluna"""
    X = np.asarray(X, dtype=float)
    means = X.mean(axis=0)
    stdevs = X.std(axis=0, ddof=1)
    return means, stdevs


def rescale(X: np.ndarray) -> np.ndarray:
    """
    Reescalona os dados de entrada para que cada coluna tenha
    média 0 e desvio padrão 1. (Deixa uma coluna como está se
    o desvio padrão dela é 0.)
    """
    X = np.asarray(X, dtype=float)
    means, stdevs = scale(X)

    rescaled = X.copy()                 # não mexe no original
    varia = stdevs > 0                  # máscara sobre as colunas
    rescaled[:, varia] = (X[:, varia] - means[varia]) / stdevs[varia]
    return rescaled


_vectors = np.array([[-3, -1, 1], [-1, 0, 1], [1, 1, 1]], dtype=float)
_means, _stdevs = scale(_vectors)
assert np.array_equal(_means, [-1, 0, 1])
assert np.array_equal(_stdevs, [2, 1, 0])

_means, _stdevs = scale(rescale(_vectors))
assert np.array_equal(_means, [0, 0, 1])
assert np.array_equal(_stdevs, [1, 1, 0])
assert np.array_equal(_vectors[0], [-3, -1, 1])   # o original ficou intacto


# --------------------------------------------------------------------------
# 7.8 Redução de dimensionalidade (PCA por subida de gradiente)
# --------------------------------------------------------------------------

def de_mean(X: np.ndarray) -> np.ndarray:
    """Recentra os dados para que cada coluna tenha média 0"""
    return X - X.mean(axis=0)


def direction(w: np.ndarray) -> np.ndarray:
    return w / np.linalg.norm(w)


def directional_variance(X: np.ndarray, w: np.ndarray) -> float:
    """Devolve a variância de X na direção de w"""
    w_dir = direction(w)
    return np.sum((X @ w_dir) ** 2)


def directional_variance_gradient(X: np.ndarray, w: np.ndarray) -> np.ndarray:
    """O gradiente da variância direcional em relação a w"""
    w_dir = direction(w)
    return 2 * (X @ w_dir) @ X


def first_principal_component(X: np.ndarray,
                              n: int = 100,
                              step_size: float = 0.1) -> np.ndarray:
    # começa com um palpite aleatório
    guess = np.ones(X.shape[1])

    with tqdm.trange(n) as t:
        for _ in t:
            dv = directional_variance(X, guess)
            gradient = directional_variance_gradient(X, guess)
            guess = gradient_step(guess, gradient, step_size)
            t.set_description(f"dv: {dv:.3f}")

    return direction(guess)


def project(v: np.ndarray, w: np.ndarray) -> np.ndarray:
    """devolve a projeção de v na direção w"""
    projection_length = v @ w
    return projection_length * w


def remove_projection_from_vector(v: np.ndarray, w: np.ndarray) -> np.ndarray:
    """projeta v em w e subtrai o resultado de v"""
    return v - project(v, w)


def remove_projection(X: np.ndarray, w: np.ndarray) -> np.ndarray:
    """remove de cada linha de X a projeção dela em w"""
    return X - np.outer(X @ w, w)


def pca(X: np.ndarray, num_components: int) -> np.ndarray:
    """Devolve as componentes como linhas de uma matriz (num_components, d)"""
    components = []
    for _ in range(num_components):
        component = first_principal_component(X)
        components.append(component)
        X = remove_projection(X, component)

    return np.array(components)


def transform_vector(v: np.ndarray, components: np.ndarray) -> np.ndarray:
    return components @ v


def transform(X: np.ndarray, components: np.ndarray) -> np.ndarray:
    return X @ components.T


# Um conjunto com direção principal conhecida POR CONSTRUÇÃO: soma de quadrados
# 2000 ao longo de u = (1, 2)/√5 e 126 ao longo da perpendicular p. `t` e `s`
# somam zero (já centrado) e são ortogonais (sem termo cruzado em XᵀX), então
# u é exatamente a primeira componente e p a segunda.
_u = np.array([1.0, 2.0]) / np.sqrt(5)
_p = np.array([-2.0, 1.0]) / np.sqrt(5)
_t = np.array([-3.0, -1.0, 0.0, 1.0, 3.0]) * 10
_s = np.array([1.0, -2.0, 2.0, -2.0, 1.0]) * 3
_X = np.outer(_t, _u) + np.outer(_s, _p)

assert np.allclose(de_mean(_X), _X)
assert np.isclose(np.linalg.norm(direction(np.array([3.0, 4.0]))), 1)
assert np.isclose(directional_variance(_X, _u), 2000)
assert np.isclose(directional_variance(_X, 2 * _u), 2000)      # só a direção importa
assert np.allclose(project(np.array([1.0, 1.0]), np.array([1.0, 0.0])), [1, 0])
assert np.allclose(remove_projection_from_vector(np.array([1.0, 1.0]), np.array([1.0, 0.0])), [0, 1])

# A subida do gradiente, sem a barra de progresso — é o laço de
# `first_principal_component`, que escreveria em stderr a cada import.
_w = np.ones(2)
for _ in range(100):
    _w = gradient_step(_w, directional_variance_gradient(_X, _w), 0.1)
_c1 = direction(_w)
assert np.allclose(np.abs(_c1), _u, atol=1e-3)

_R = remove_projection(_X, _c1)
assert np.allclose(_R @ _c1, 0)                                  # nada sobrou na direção de c1
assert np.allclose(np.abs(transform(_X, np.array([_c1]))[:, 0]), np.abs(_t), atol=0.05)
assert np.allclose(transform_vector(_X[0], np.array([_c1])), transform(_X, np.array([_c1]))[0])
