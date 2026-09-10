"""k-Vizinhos Mais Próximos com numpy — o que o capítulo 9 ensina.

A seção 9.1 escreve `raw_majority_vote`, `majority_vote` e `knn_classify`
inline; a seção 9.2 importa `knn_classify` daqui; a seção 9.3 escreve
`random_distances`. O código é o mesmo dos chunks — o módulo é o chunk salvo
em arquivo. Nenhum outro capítulo importa deste módulo.
"""
import numpy as np


def raw_majority_vote(labels) -> str:
    valores, contagens = np.unique(labels, return_counts=True)
    return valores[np.argmax(contagens)]


assert raw_majority_vote(['a', 'b', 'c', 'b']) == 'b'


def majority_vote(labels) -> str:
    """Assume que os rótulos estão ordenados do mais próximo ao mais distante."""
    valores, contagens = np.unique(labels, return_counts=True)
    vencedores = valores[contagens == contagens.max()]

    if len(vencedores) == 1:
        return vencedores[0]                # vencedor único
    else:
        return majority_vote(labels[:-1])   # tenta de novo sem o mais distante


# Empate: olha os 4 primeiros, então 'b'
assert majority_vote(['a', 'b', 'c', 'b', 'a']) == 'b'


def knn_classify(k: int,
                 X_train: np.ndarray,
                 y_train: np.ndarray,
                 new_point: np.ndarray) -> str:
    # A distância do ponto novo a cada linha de X_train, de uma vez.
    dists = np.linalg.norm(X_train - new_point, axis=1)

    # Os índices que ordenam os pontos do mais próximo ao mais distante...
    ordem = np.argsort(dists)

    # ...e os rótulos dos k primeiros votam.
    return majority_vote(y_train[ordem[:k]])


# Dois pontos perto da origem, três longe dela.
_X = np.array([[0.0, 0.0], [0.0, 1.0], [3.0, 3.0], [3.0, 4.0], [4.0, 3.0]])
_y = np.array(['perto', 'perto', 'longe', 'longe', 'longe'])
assert knn_classify(3, _X, _y, np.array([0.5, 0.5])) == 'perto'
assert knn_classify(3, _X, _y, np.array([3.5, 3.5])) == 'longe'


def random_distances(dim: int, num_pairs: int,
                     rng: np.random.Generator) -> np.ndarray:
    """Distâncias de `num_pairs` pares sorteados no cubo unitário de dimensão `dim`."""
    return np.linalg.norm(rng.random((num_pairs, dim))
                          - rng.random((num_pairs, dim)), axis=1)


_d = random_distances(3, 1000, np.random.default_rng(0))
assert _d.shape == (1000,)
assert 0.0 < _d.min() and _d.max() < np.sqrt(3)
