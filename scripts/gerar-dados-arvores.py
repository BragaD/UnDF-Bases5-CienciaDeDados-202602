"""Escreve os dados das páginas de apoio do capítulo 12 dentro delas.

As duas páginas, `apoio/crescimento-da-arvore.html` (seção 12.1) e
`apoio/poda-da-arvore.html` (seção 12.2), são arquivos únicos que abrem com
dois cliques e rodam sem rede. Os dados vão embutidos numa tag
`<script type="application/json" id="dados">`, e é este script que a preenche.

Rode no container, que é a máquina que gera o site:

    docker compose run --rm --no-deps livro python scripts/gerar-dados-arvores.py

A árvore grande da 12.2 difere entre o host e o container (120 × 121 folhas);
da poda em diante os números são os mesmos, mas a página tem de mostrar a
árvore que o site mostra.
"""

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.tree import DecisionTreeRegressor

RAIZ = Path(__file__).resolve().parent.parent
CRESCIMENTO = RAIZ / "apoio/crescimento-da-arvore.html"
PODA = RAIZ / "apoio/poda-da-arvore.html"
TAG = re.compile(r'(<script type="application/json" id="dados">)(.*?)(</script>)', re.S)


def dados_crescimento() -> dict:
    """Os 263 jogadores com salário da seção 12.1, na ordem do arquivo."""
    hitters = pd.read_csv(RAIZ / "dados/Hitters.csv").dropna()
    return {
        "anos": [int(v) for v in hitters["anos"]],
        "rebatidas": [int(v) for v in hitters["rebatidas"]],
        "salario": [float(v) for v in hitters["salario"]],
    }


def _poda_do_elo_mais_fraco(arvore: DecisionTreeRegressor) -> list[dict]:
    """A sequência de podas, um nó por degrau, feita sobre o `tree_`.

    É a mesma conta do `cost_complexity_pruning_path`, mas guarda qual nó
    virou folha em cada degrau, o que o caminho do `scikit-learn` não diz.
    """
    t = arvore.tree_
    n_total = t.weighted_n_node_samples[0]
    r = t.impurity * t.weighted_n_node_samples / n_total
    esq, dir_ = t.children_left, t.children_right
    pai = np.full(t.node_count, -1)
    for i in range(t.node_count):
        if esq[i] != -1:
            pai[esq[i]] = i
            pai[dir_[i]] = i
    cortado = np.zeros(t.node_count, dtype=bool)

    def eh_folha(i):
        return esq[i] == -1 or cortado[i]

    def alcancavel(i):
        p = pai[i]
        while p != -1:
            if cortado[p]:
                return False
            p = pai[p]
        return True

    def galho(i):
        """Soma de r e número de folhas do galho que começa em i."""
        if eh_folha(i):
            return r[i], 1
        r_esq, f_esq = galho(esq[i])
        r_dir, f_dir = galho(dir_[i])
        return r_esq + r_dir, f_esq + f_dir

    degraus = []
    while not cortado[0]:
        melhor, qual = np.inf, -1
        for i in range(t.node_count):
            if eh_folha(i) or not alcancavel(i):
                continue
            r_galho, folhas = galho(i)
            custo = (r[i] - r_galho) / (folhas - 1)
            if custo < melhor:
                melhor, qual = custo, i
        cortado[qual] = True
        mse, folhas = galho(0)
        degraus.append({
            "no": int(qual),
            "ccp_alpha": float(melhor),
            "alpha": float(n_total * melhor),
            "folhas": int(folhas),
            "rss": float(n_total * mse),
            "mse": float(mse),
        })
    return degraus


def dados_poda() -> dict:
    """A árvore grande da 12.2, a sequência de podas e a curva de validação cruzada."""
    hitters = pd.read_csv(RAIZ / "dados/Hitters.csv").dropna()
    y = np.log(hitters["salario"])
    X = pd.get_dummies(hitters.drop(columns="salario"), drop_first=True, dtype=float)
    treino_X, _, treino_y, _ = train_test_split(X, y, train_size=132, random_state=12)
    n_treino = len(treino_X)

    grande = DecisionTreeRegressor(random_state=12)
    grande.fit(treino_X, treino_y)
    caminho = grande.cost_complexity_pruning_path(treino_X, treino_y)
    alfas = caminho.ccp_alphas

    degraus = _poda_do_elo_mais_fraco(grande)
    assert np.allclose([g["ccp_alpha"] for g in degraus], alfas[1:], rtol=0, atol=1e-12)
    assert np.allclose([g["mse"] for g in degraus], caminho.impurities[1:], rtol=0, atol=1e-12)

    t = grande.tree_
    nos = []
    for i in range(t.node_count):
        interno = t.children_left[i] != -1
        nos.append({
            "esq": int(t.children_left[i]),
            "dir": int(t.children_right[i]),
            "coluna": str(X.columns[t.feature[i]]) if interno else None,
            "limiar": float(t.threshold[i]) if interno else None,
            "n": int(t.n_node_samples[i]),
            "media": float(t.value[i][0][0]),
            "rss": float(t.impurity[i] * t.n_node_samples[i]),
        })

    # A curva de validação cruzada, como nos chunks `grade`, `folhas-na-grade`,
    # `busca`, `curvas` e `teste` da 12.2.
    grade = np.r_[0.0, np.sqrt(alfas[1:-1] * alfas[2:])]
    folhas = []
    for ccp_alpha in grade:
        podada = DecisionTreeRegressor(ccp_alpha=ccp_alpha, random_state=12)
        podada.fit(treino_X, treino_y)
        folhas.append(podada.get_n_leaves())
    grupos = KFold(6, shuffle=True, random_state=12)
    busca = GridSearchCV(
        DecisionTreeRegressor(random_state=12),
        {"ccp_alpha": grade[::-1]},
        cv=grupos,
        scoring="neg_mean_squared_error",
    )
    busca.fit(treino_X, treino_y)
    erros = np.array([
        -busca.cv_results_[f"split{k}_test_score"] for k in range(grupos.get_n_splits())
    ])
    curvas = pd.DataFrame({
        "ccp_alpha": grade[::-1],
        "folhas": np.array(folhas)[::-1],
        "cv": erros.mean(axis=0),
        "desvio": erros.std(axis=0, ddof=1) / np.sqrt(grupos.get_n_splits()),
    }).drop_duplicates("folhas")
    mse_treino = []
    for ccp_alpha in curvas["ccp_alpha"]:
        podada = DecisionTreeRegressor(ccp_alpha=ccp_alpha, random_state=12)
        podada.fit(treino_X, treino_y)
        mse_treino.append(float(np.mean((treino_y - podada.predict(treino_X)) ** 2)))
    curvas["mse_treino"] = mse_treino
    curvas = curvas.sort_values("folhas")

    return {
        "n_treino": n_treino,
        "arvore": {
            "folhas": int(grande.get_n_leaves()),
            "rss": float(caminho.impurities[0] * n_treino),
            "mse": float(caminho.impurities[0]),
        },
        "nos": nos,
        "degraus": degraus,
        "curva": [
            {
                "folhas": int(linha.folhas),
                "ccp_alpha": float(linha.ccp_alpha),
                "cv": float(linha.cv),
                "desvio": float(linha.desvio),
                "mse_treino": float(linha.mse_treino),
            }
            for linha in curvas.itertuples()
        ],
    }


def embutir(pagina: Path, dados: dict) -> None:
    """Troca o conteúdo da tag `id="dados"` da página pelo JSON de `dados`."""
    html = pagina.read_text(encoding="utf-8")
    if not TAG.search(html):
        raise ValueError(f"{pagina.name} não tem a tag de dados")
    texto = json.dumps(dados, ensure_ascii=False, separators=(",", ":"))
    html = TAG.sub(lambda m: m.group(1) + texto + m.group(3), html, count=1)
    pagina.write_text(html, encoding="utf-8")


def main():
    embutir(CRESCIMENTO, dados_crescimento())
    embutir(PODA, dados_poda())


if __name__ == "__main__":
    main()
