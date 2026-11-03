"""As páginas de `apoio/` do capítulo 12: dados embutidos e o núcleo de cada uma.

Os dados das duas páginas saem de `scripts/gerar-dados-arvores.py`, rodado no
container, e ficam numa tag `<script type="application/json" id="dados">`. Os
testes daqui leem essa tag e cobram que ela traga os números das seções 12.1
e 12.2: uma página projetada ao lado do texto não pode contradizê-lo.
"""

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.tree import DecisionTreeRegressor

RAIZ = Path(__file__).resolve().parent.parent
CRESCIMENTO = RAIZ / "apoio/crescimento-da-arvore.html"
PODA = RAIZ / "apoio/poda-da-arvore.html"


def dados_embutidos(pagina: Path) -> dict:
    """O JSON da tag `id="dados"` da página."""
    html = pagina.read_text(encoding="utf-8")
    achado = re.search(
        r'<script type="application/json" id="dados">(.*?)</script>', html, re.S
    )
    assert achado, f"{pagina.name} não tem a tag de dados"
    return json.loads(achado.group(1))


def nucleo(pagina: Path) -> str:
    """O texto do `<script id="nucleo">` da página: as contas, sem DOM."""
    html = pagina.read_text(encoding="utf-8")
    achado = re.search(r'<script id="nucleo">(.*?)</script>', html, re.S)
    assert achado, f"{pagina.name} não tem o núcleo"
    return achado.group(1)


def no_node(pagina: Path, expressao: str):
    """Avalia `expressao` com o núcleo e os dados da página, no `node`."""
    codigo = (
        nucleo(pagina)
        + f"\nconst DADOS = {json.dumps(dados_embutidos(pagina))};\n"
        + f"console.log(JSON.stringify({expressao}));\n"
    )
    with tempfile.TemporaryDirectory() as pasta:
        arquivo = Path(pasta) / "nucleo.js"
        arquivo.write_text(codigo, encoding="utf-8")
        saida = subprocess.run(["node", str(arquivo)], capture_output=True, text=True)
    assert saida.returncode == 0, saida.stderr[-2000:]
    return json.loads(saida.stdout)


PRECISA_DE_NODE = pytest.mark.skipif(
    shutil.which("node") is None, reason="node só existe no host, não no container"
)


def hitters() -> pd.DataFrame:
    return pd.read_csv(RAIZ / "dados/Hitters.csv").dropna().reset_index(drop=True)


def rss_do_corte(X: pd.DataFrame, y: pd.Series, coluna: str) -> pd.Series:
    """O RSS (8.3) de cada ponto de corte da coluna, como na seção 12.1."""
    valores = np.sort(X[coluna].unique())
    cortes = (valores[:-1] + valores[1:]) / 2
    rss = []
    for s in cortes:
        esq = X[coluna] < s
        rss.append(((y[esq] - y[esq].mean()) ** 2).sum()
                   + ((y[~esq] - y[~esq].mean()) ** 2).sum())
    return pd.Series(rss, index=cortes)


def test_crescimento_embute_os_263_jogadores_de_hitters():
    d = dados_embutidos(CRESCIMENTO)
    h = pd.read_csv(RAIZ / "dados/Hitters.csv").dropna()
    assert d["anos"] == h["anos"].tolist()
    assert d["rebatidas"] == h["rebatidas"].tolist()
    assert d["salario"] == h["salario"].tolist()


def test_poda_embute_os_numeros_da_secao_12_2():
    d = dados_embutidos(PODA)
    assert d["n_treino"] == 132
    raiz = d["nos"][0]
    assert (raiz["coluna"], round(raiz["limiar"], 1)) == ("vezes_ao_bastao_carreira", 1452.0)
    de_3_para_2 = next(g for g in d["degraus"] if g["folhas"] == 2)
    no = d["nos"][de_3_para_2["no"]]
    assert (no["coluna"], round(no["limiar"], 1), no["n"], round(no["media"], 2)) == (
        "impulsionadas_carreira", 70.5, 54, 5.11)
    assert round(de_3_para_2["ccp_alpha"], 4) == 0.0677
    assert round(de_3_para_2["alpha"], 2) == 8.94
    assert round(de_3_para_2["mse"], 4) == 0.2935
    curva = pd.DataFrame(d["curva"]).set_index("folhas")
    assert round(curva.loc[3, "mse_treino"], 4) == 0.2258
    ordem = curva["cv"].sort_values()
    assert ordem.index[:2].tolist() == [4, 7]
    assert [round(v, 4) for v in ordem.iloc[:2]] == [0.2694, 0.2841]


@PRECISA_DE_NODE
def test_crescimento_no_node_segue_o_decision_tree_regressor():
    h = hitters()
    X2 = h[["anos", "rebatidas"]]
    y = np.log(h["salario"])
    maximo = no_node(CRESCIMENTO, "MAX_FOLHAS")
    assert maximo >= 6
    arvores = no_node(CRESCIMENTO, """(() => {
        const {X, y} = preparar(DADOS);
        const saida = [];
        for (let k = 2; k <= MAX_FOLHAS; k++) {
            const a = crescer(X, y, k);
            saida.push({
                cortes: a.nos.filter(n => n.esq !== null).map(n => [n.coluna, n.corte]),
                folhas: a.nos.filter(n => n.esq === null).length,
                rss: rssTotal(a),
            });
        }
        return saida;
    })()""")
    for k, arvore in zip(range(2, maximo + 1), arvores):
        sk = DecisionTreeRegressor(max_leaf_nodes=k, random_state=12).fit(X2, y)
        t = sk.tree_
        cortes = sorted(
            (X2.columns[t.feature[i]], float(t.threshold[i]))
            for i in range(t.node_count) if t.children_left[i] != -1
        )
        assert sorted(tuple(c) for c in arvore["cortes"]) == cortes, f"k = {k}"
        assert arvore["folhas"] == k
        rss = ((y - sk.predict(X2)) ** 2).sum()
        assert arvore["rss"] == pytest.approx(rss, abs=1e-9), f"k = {k}"


@PRECISA_DE_NODE
def test_curva_do_rss_no_node_bate_com_a_da_secao_12_1():
    h = hitters()
    X2 = h[["anos", "rebatidas"]]
    y = np.log(h["salario"])
    curvas = no_node(CRESCIMENTO, """(() => {
        const {X, y} = preparar(DADOS);
        const todas = y.map((_, i) => i);
        return Object.fromEntries(COLUNAS.map(c => [c, cortesDaRegiao(todas, c, X, y)]));
    })()""")
    minimos = {}
    for coluna in ["anos", "rebatidas"]:
        esperado = rss_do_corte(X2, y, coluna)
        assert curvas[coluna]["cortes"] == esperado.index.tolist()
        assert np.allclose(curvas[coluna]["rss"], esperado.values, rtol=0, atol=1e-9)
        i = int(np.argmin(curvas[coluna]["rss"]))
        minimos[coluna] = (round(curvas[coluna]["rss"][i], 2), curvas[coluna]["cortes"][i])
    assert minimos == {"anos": (115.06, 4.5), "rebatidas": (160.97, 117.5)}


@PRECISA_DE_NODE
def test_segundo_corte_tem_as_quedas_da_secao_12_1():
    r = no_node(CRESCIMENTO, """(() => {
        const {X, y} = preparar(DADOS);
        const folhas = crescer(X, y, 2).nos.filter(n => n.esq === null);
        return {
            melhores: folhas.map(f => ({n: f.n, melhor: melhorCorte(f.linhas, X, y)})),
            rss3: rssTotal(crescer(X, y, 3)),
        };
    })()""")
    por_tamanho = {f["n"]: f["melhor"] for f in r["melhores"]}
    novatos, veteranos = por_tamanho[90], por_tamanho[173]
    assert (novatos["coluna"], novatos["corte"], round(novatos["queda"], 2)) == (
        "rebatidas", 15.5, 9.34)
    assert (veteranos["coluna"], veteranos["corte"], round(veteranos["queda"], 2)) == (
        "rebatidas", 117.5, 23.73)
    assert round(r["rss3"], 2) == 91.33


@PRECISA_DE_NODE
def test_regiao_sem_corte_possivel():
    h = hitters()
    par = next(list(v) for v in h.groupby(["anos", "rebatidas"]).groups.values()
               if len(v) > 1)
    linhas = json.dumps([int(i) for i in par])
    r = no_node(CRESCIMENTO, f"""(() => {{
        const {{X, y}} = preparar(DADOS);
        const linhas = {linhas};
        return {{
            anos: cortesDaRegiao(linhas, "anos", X, y),
            rebatidas: cortesDaRegiao(linhas, "rebatidas", X, y),
            melhor: melhorCorte(linhas, X, y),
        }};
    }})()""")
    assert r["anos"] == {"cortes": [], "rss": []}
    assert r["rebatidas"] == {"cortes": [], "rss": []}
    assert r["melhor"] is None


@PRECISA_DE_NODE
def test_formato_brasileiro():
    assert no_node(CRESCIMENTO, "fmt(1452, 1)") == "1.452,0"
    assert no_node(CRESCIMENTO, "fmt(0.26941, 4)") == "0,2694"
