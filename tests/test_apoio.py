"""As páginas de `apoio/` dos capítulos 12 e 13: dados embutidos e o núcleo de cada uma.

Os dados das duas páginas saem de `scripts/gerar-dados-arvores.py`, rodado no
container, e ficam numa tag `<script type="application/json" id="dados">`. Os
testes daqui leem essa tag e cobram que ela traga os números das seções 12.1
e 12.2: uma página projetada ao lado do texto não pode contradizê-lo.

As duas páginas do capítulo 13 recebem de `scripts/gerar-dados-ensembles.py`
só o dado cru e a divisão de treino e teste; as contas do bagging e do
boosting rodam na página, e os testes daqui as conferem, árvore a árvore,
contra o `scikit-learn`.

As três do capítulo 14 dividem um núcleo só, a rede dos dígitos em tamanho
pequeno (784, 16, 16 e 10), e recebem de `scripts/gerar-dados-redes.py` as
imagens e, na primeira, uma rede já ajustada. A ida, a retropropagação e as
épocas de gradiente são conferidas contra o `MLPClassifier`.
"""

import base64
import json
import warnings
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeRegressor

RAIZ = Path(__file__).resolve().parent.parent
CRESCIMENTO = RAIZ / "apoio/crescimento-da-arvore.html"
PODA = RAIZ / "apoio/poda-da-arvore.html"
BAGGING = RAIZ / "apoio/bagging-de-arvores.html"
BOOSTING = RAIZ / "apoio/boosting-passo-a-passo.html"
IDA = RAIZ / "apoio/do-pixel-ao-digito.html"
VOLTA = RAIZ / "apoio/retropropagacao.html"
AJUSTE = RAIZ / "apoio/lotes-penalidade-e-dropout.html"


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


@PRECISA_DE_NODE
def test_poda_no_node_reproduz_o_elo_mais_fraco_de_cada_degrau():
    d = dados_embutidos(PODA)
    calculado = no_node(PODA, """DADOS.degraus.map((_, j) => {
        const primeiro = candidatos(DADOS, cortadosAte(DADOS, j))[0];
        return {no: primeiro.no, custo: primeiro.custo,
                folhas: subarvore(DADOS, cortadosAte(DADOS, j + 1)).folhas};
    })""")
    for j, (degrau, js) in enumerate(zip(d["degraus"], calculado)):
        assert js["no"] == degrau["no"], f"degrau {j}"
        assert js["custo"] == pytest.approx(degrau["alpha"], rel=1e-9, abs=1e-12), f"degrau {j}"
        assert js["folhas"] == degrau["folhas"], f"degrau {j}"


@PRECISA_DE_NODE
def test_poda_no_node_no_degrau_de_3_para_2_folhas():
    d = dados_embutidos(PODA)
    j = next(j for j, g in enumerate(d["degraus"]) if g["folhas"] == 3) + 1
    r = no_node(PODA, f"""(() => {{
        const cortados = cortadosAte(DADOS, {j});
        return {{primeiro: candidatos(DADOS, cortados)[0], antes: subarvore(DADOS, cortados)}};
    }})()""")
    no = d["nos"][r["primeiro"]["no"]]
    assert (no["coluna"], round(no["limiar"], 1)) == ("impulsionadas_carreira", 70.5)
    assert round(r["primeiro"]["custo"], 2) == 8.94
    assert round(r["primeiro"]["custo"] / d["n_treino"], 4) == 0.0677
    assert r["antes"]["folhas"] == 3
    assert round(r["antes"]["mse"], 4) == 0.2258


@PRECISA_DE_NODE
def test_erro_na_curva_devolve_nulo_fora_da_grade():
    d = dados_embutidos(PODA)
    sem_curva = sorted({g["folhas"] for g in d["degraus"]} - {c["folhas"] for c in d["curva"]})
    assert 1 in sem_curva and len(sem_curva) > 1
    r = no_node(PODA, f"""[erroNaCurva(DADOS, 4), {json.dumps(sem_curva)}.map(f => erroNaCurva(DADOS, f))]""")
    assert round(r[0]["cv"], 4) == 0.2694
    assert r[1] == [None] * len(sem_curva)


@PRECISA_DE_NODE
def test_formato_brasileiro_na_poda():
    assert no_node(PODA, "fmt(1452, 1)") == "1.452,0"


# --------------------------- capítulo 13 ---------------------------------


def treino_e_teste_de_uma_coluna():
    """A divisão das seções 13.1 e 13.4, só com `vezes_ao_bastao_carreira`."""
    h = pd.read_csv(RAIZ / "dados/Hitters.csv").dropna()
    X = h[["vezes_ao_bastao_carreira"]]
    y = np.log(h["salario"])
    return train_test_split(X, y, train_size=132, random_state=12)


@pytest.mark.parametrize("pagina", [BAGGING, BOOSTING], ids=["bagging", "boosting"])
def test_ensembles_embutem_a_divisao_das_secoes_13_1_e_13_4(pagina):
    d = dados_embutidos(pagina)
    h = pd.read_csv(RAIZ / "dados/Hitters.csv").dropna()
    treino, teste = train_test_split(np.arange(len(h)), train_size=132, random_state=12)
    assert d["coluna"] == "vezes_ao_bastao_carreira"
    assert d["vezes"] == h["vezes_ao_bastao_carreira"].tolist()
    assert d["salario"] == h["salario"].tolist()
    assert d["treino"] == treino.tolist()
    assert d["teste"] == teste.tolist()


@PRECISA_DE_NODE
def test_bagging_no_node_segue_o_decision_tree_regressor_em_cada_amostra():
    treino_X, teste_X, treino_y, teste_y = treino_e_teste_de_uma_coluna()
    r = no_node(BAGGING, """(() => {
        const D = preparar(DADOS);
        const bag = novoBagging(D.treino, D.teste, 13);
        const previsoes = [];
        for (let b = 0; b < 60; b++) {
            const arvore = acrescentar(bag);
            previsoes.push(D.teste.x.map(v => prever(arvore, v)));
        }
        return {amostras: bag.amostras, previsoes, teste: bag.curvaTeste,
                oob: bag.curvaOob, fora: bag.fora,
                uma: erroDeUmaArvore(D.treino, D.teste)};
    })()""")
    n = len(treino_X)
    soma_teste = np.zeros(len(teste_X))
    soma_oob, conta_oob = np.zeros(n), np.zeros(n)
    for b, (amostra, previsto_js) in enumerate(zip(r["amostras"], r["previsoes"])):
        assert len(amostra) == n and min(amostra) >= 0 and max(amostra) < n
        arvore = DecisionTreeRegressor(random_state=12)
        arvore.fit(treino_X.iloc[amostra], treino_y.iloc[amostra])
        previsto = arvore.predict(teste_X)
        assert np.allclose(previsto_js, previsto, rtol=0, atol=1e-9), f"árvore {b + 1}"
        soma_teste += previsto
        assert r["teste"][b] == pytest.approx(
            mean_squared_error(teste_y, soma_teste / (b + 1)), abs=1e-9)
        fora = np.setdiff1d(np.arange(n), amostra)
        assert r["fora"][b] == pytest.approx(len(fora) / n)
        soma_oob[fora] += arvore.predict(treino_X.iloc[fora])
        conta_oob[fora] += 1
        com = conta_oob > 0
        oob = np.mean((treino_y.values[com] - soma_oob[com] / conta_oob[com]) ** 2)
        assert r["oob"][b] == pytest.approx(oob, abs=1e-9), f"B = {b + 1}"
    grande = DecisionTreeRegressor(random_state=12).fit(treino_X, treino_y)
    assert r["uma"] == pytest.approx(mean_squared_error(teste_y, grande.predict(teste_X)), abs=1e-9)
    # o que a página promete mostrar: a média erra menos que uma árvore só
    assert r["teste"][-1] < r["uma"] - 0.1


@PRECISA_DE_NODE
def test_bagging_no_node_repete_o_sorteio_com_a_mesma_semente():
    r = no_node(BAGGING, """[13, 13, 14].map(semente => {
        const D = preparar(DADOS);
        const bag = novoBagging(D.treino, D.teste, semente);
        acrescentar(bag);
        return bag.amostras[0];
    })""")
    assert r[0] == r[1]
    assert r[0] != r[2]


@PRECISA_DE_NODE
def test_bagging_no_node_sorteia_outro_conjunto_de_treino():
    r = no_node(BAGGING, """(() => {
        const sorteio = semente => sortearDivisao(gerador(semente), DADOS.vezes.length, 132);
        const divisao = sorteio(2024);
        const D = preparar(DADOS, divisao);
        return {divisao, de_novo: sorteio(2024), outra: sorteio(2025),
                x: D.treino.x, y: D.teste.y, padrao: preparar(DADOS).treino.x};
    })()""")
    d = dados_embutidos(BAGGING)
    treino, teste = r["divisao"]["treino"], r["divisao"]["teste"]
    assert (len(treino), len(teste)) == (132, 131)
    assert sorted(treino + teste) == list(range(263))
    assert r["de_novo"] == r["divisao"] and r["outra"] != r["divisao"]
    assert treino != d["treino"]
    assert r["x"] == [d["vezes"][i] for i in treino]
    assert np.allclose(r["y"], np.log([d["salario"][i] for i in teste]))
    assert r["padrao"] == [d["vezes"][i] for i in d["treino"]]


@PRECISA_DE_NODE
def test_boosting_no_node_tem_os_tres_primeiros_passos_da_secao_13_4():
    c = no_node(BOOSTING, """(() => {
        const D = preparar(DADOS);
        return caminho(D.treino, D.teste, 0.01, "zero", 3);
    })()""")
    assert c["cortes"] == [1452, 1452, 1452]
    assert c["nEsq"] == [54, 54, 54]
    assert (round(c["esq"][0], 2), round(c["dir"][0], 2)) == (5.11, 6.46)
    assert round(c["mseTreino"][0], 2) == 34.97


@PRECISA_DE_NODE
@pytest.mark.parametrize("taxa", [0.001, 0.01, 0.1, 1])
@pytest.mark.parametrize("partida", ["zero", "media"])
def test_boosting_no_node_segue_o_gradient_boosting_regressor(taxa, partida):
    treino_X, teste_X, treino_y, teste_y = treino_e_teste_de_uma_coluna()
    c = no_node(BOOSTING, f"""(() => {{
        const D = preparar(DADOS);
        const c = caminho(D.treino, D.teste, {taxa}, "{partida}", MAX_ARVORES);
        const f = degraus(c, 500);
        const grade = [20, 300, 1452, 1453, 5000, 14000];
        return {{treino: c.mseTreino, teste: c.mseTeste, cortes: c.cortes, nEsq: c.nEsq,
                 menor: indiceDoMenor(c.mseTeste, MAX_ARVORES) + 1,
                 direto: preverAte(c, 500, grade),
                 emDegraus: grade.map(x => f.valores[f.cortes.filter(k => x > k).length])}};
    }})()""")
    inicio = {"init": "zero"} if partida == "zero" else {}
    boost = GradientBoostingRegressor(n_estimators=3000, learning_rate=taxa, max_leaf_nodes=2,
                                      max_depth=None, random_state=13, **inicio)
    boost.fit(treino_X, treino_y)
    teste = np.array([mean_squared_error(teste_y, p) for p in boost.staged_predict(teste_X)])
    assert np.allclose(c["treino"], boost.train_score_, rtol=0, atol=1e-9)
    assert np.allclose(c["teste"], teste, rtol=0, atol=1e-9)
    assert c["menor"] == int(np.argmin(teste)) + 1
    assert np.allclose(c["direto"], c["emDegraus"], rtol=0, atol=1e-9)
    # o desenho de cada árvore: o corte da raiz e quantos jogadores caem à esquerda
    arvores = [e.tree_ for e in boost.estimators_[:, 0]]
    assert np.allclose(c["cortes"], [a.threshold[0] for a in arvores], rtol=0, atol=1e-9)
    assert c["nEsq"] == [int(a.n_node_samples[a.children_left[0]]) for a in arvores]


@PRECISA_DE_NODE
def test_formato_brasileiro_nos_ensembles():
    assert no_node(BAGGING, "fmt(1452, 0)") == "1.452"
    assert no_node(BOOSTING, "fmt(0.3443, 3)") == "0,344"


# --------------------------------------------------------------------------
# Capítulo 14: a rede dos dígitos (ida, retropropagação e ajuste por lotes)
# --------------------------------------------------------------------------

TAMANHOS = [784, 16, 16, 10]


def mnist(nome: str) -> tuple[np.ndarray, np.ndarray]:
    tabela = pd.read_csv(RAIZ / "dados" / nome)
    return tabela.drop(columns="digito").to_numpy(), tabela["digito"].to_numpy()


def imagens(texto: str) -> np.ndarray:
    """As imagens embutidas em base64, como a página as lê: uma linha por imagem."""
    return np.frombuffer(base64.b64decode(texto), dtype=np.uint8).reshape(-1, 784) / 255


def em_matrizes(pesos: list) -> list[np.ndarray]:
    """Os pesos de cada camada, do vetor da página para a forma de `coefs_`."""
    return [
        np.array(w).reshape(TAMANHOS[c], TAMANHOS[c + 1]) for c, w in enumerate(pesos)
    ]


def rede_do_sklearn(pesos: list, vieses: list, X, y, **opcoes) -> MLPClassifier:
    """Um `MLPClassifier` de gradiente simples que parte dos pesos dados.

    A primeira chamada de `partial_fit` só existe para o `scikit-learn` criar
    as matrizes; os pesos são escritos por cima, no lugar, porque o otimizador
    guarda referência a elas.
    """
    rede = MLPClassifier(
        hidden_layer_sizes=(16, 16), solver="sgd", momentum=0,
        nesterovs_momentum=False, shuffle=False, **opcoes,
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rede.partial_fit(X, y, classes=np.arange(10))
    for camada, W in enumerate(em_matrizes(pesos)):
        rede.coefs_[camada][...] = W
    for camada, v in enumerate(vieses):
        rede.intercepts_[camada][...] = v
    return rede


def test_as_tres_paginas_de_redes_tem_o_mesmo_nucleo():
    assert nucleo(IDA) == nucleo(VOLTA) == nucleo(AJUSTE)


def test_redes_embutem_as_imagens_das_secoes_14_2_e_14_3():
    treino_pixels, treino_y = mnist("mnist_treino.csv.gz")
    teste_pixels, teste_y = mnist("mnist_teste.csv.gz")

    ida = dados_embutidos(IDA)
    assert np.array_equal(imagens(ida["imagens"]), teste_pixels[:200] / 255)
    assert ida["digitos"] == teste_y[:200].tolist()
    assert ida["rede"]["tamanhos"] == TAMANHOS
    assert (ida["n_treino"], ida["n_teste"]) == (len(treino_y), len(teste_y))

    volta = dados_embutidos(VOLTA)
    assert volta["digitos"] == list(range(10)) * 3
    linhas = [np.flatnonzero(treino_y == d)[vez] for vez in range(3) for d in range(10)]
    assert np.array_equal(imagens(volta["imagens"]), treino_pixels[linhas] / 255)

    ajuste = dados_embutidos(AJUSTE)
    parte_ajuste, parte_validacao = train_test_split(
        np.arange(len(treino_y)), test_size=0.2, random_state=14, stratify=treino_y
    )
    assert np.array_equal(imagens(ajuste["ajuste"]), treino_pixels[parte_ajuste[:600]] / 255)
    assert ajuste["digitos_ajuste"] == treino_y[parte_ajuste[:600]].tolist()
    assert np.array_equal(
        imagens(ajuste["validacao"]), treino_pixels[parte_validacao[:400]] / 255
    )
    assert ajuste["digitos_validacao"] == treino_y[parte_validacao[:400]].tolist()


@PRECISA_DE_NODE
def test_ida_no_node_segue_o_predict_proba():
    d = dados_embutidos(IDA)
    X = imagens(d["imagens"])
    y = np.array(d["digitos"])
    rede = rede_do_sklearn(d["rede"]["W"], d["rede"]["v"], X, y)
    r = no_node(IDA, """(() => {
      const rede = redeDe(DADOS.rede);
      const idas = decodificar(DADOS.imagens).map(x => adiante(rede, x));
      return {
        f: idas.map(ida => Array.from(ida.f)),
        ligadas: idas.map(ida => ida.a[1].filter(a => a > 0).length),
        erros: medir(rede, decodificar(DADOS.imagens), DADOS.digitos).erros,
      };
    })()""")
    probabilidades = rede.predict_proba(X)
    assert np.allclose(r["f"], probabilidades, rtol=0, atol=1e-9)
    primeira = np.maximum(0, X @ rede.coefs_[0] + rede.intercepts_[0])
    assert r["ligadas"] == (primeira > 0).sum(axis=1).tolist()
    assert r["erros"] == int((probabilidades.argmax(axis=1) != y).sum())

    # O número de erros que a página afirma nas 2.000 imagens de teste.
    teste_pixels, teste_y = mnist("mnist_teste.csv.gz")
    assert d["erros_teste"] == int((rede.predict(teste_pixels / 255) != teste_y).sum())


@PRECISA_DE_NODE
@pytest.mark.parametrize("imagem", [0, 7, 15])
def test_volta_no_node_da_o_passo_do_mlpclassifier(imagem):
    d = dados_embutidos(VOLTA)
    X = imagens(d["imagens"])
    y = np.array(d["digitos"])
    r = no_node(VOLTA, f"""(() => {{
      const X = decodificar(DADOS.imagens), y = DADOS.digitos;
      const rede = iniciar(gerador(14), [784, 16, 16, 10]);
      const lista = r => ({{W: r.W.map(w => Array.from(w)), v: r.v.map(b => Array.from(b))}});
      const antes = lista(rede);
      const ida = adiante(rede, X[{imagem}]);
      const delta = atras(rede, ida, y[{imagem}]);
      const grad = gradiente(rede, X, y, [{imagem}]);
      passo(rede, grad, 0.03, 0, 1);
      return {{antes, depois: lista(rede), f: Array.from(ida.f),
               saida: Array.from(delta[2]), perda: grad.perda}};
    }})()""")
    # Na saída, a derivada é a probabilidade menos o alvo.
    alvo = np.eye(10)[y[imagem]]
    assert np.allclose(r["saida"], np.array(r["f"]) - alvo, rtol=0, atol=1e-12)
    assert r["perda"] == pytest.approx(-np.log(r["f"][y[imagem]]))

    um = slice(imagem, imagem + 1)
    rede = rede_do_sklearn(
        r["antes"]["W"], r["antes"]["v"], X[um], y[um],
        learning_rate_init=0.03, alpha=0, batch_size=1,
    )
    assert np.allclose(rede.predict_proba(X[um])[0], r["f"], rtol=0, atol=1e-12)
    rede.partial_fit(X[um], y[um])
    for camada, W in enumerate(em_matrizes(r["depois"]["W"])):
        assert np.allclose(rede.coefs_[camada], W, rtol=0, atol=1e-12)
        assert np.allclose(rede.intercepts_[camada], r["depois"]["v"][camada], rtol=0, atol=1e-12)


@PRECISA_DE_NODE
@pytest.mark.parametrize(
    "lote, taxa, alpha", [(600, 0.1, 0), (100, 0.1, 0), (20, 0.1, 0.3), (20, 0.1, 3), (1, 0.01, 0)]
)
def test_ajuste_no_node_segue_as_epocas_do_sgd(lote, taxa, alpha):
    d = dados_embutidos(AJUSTE)
    X, y = imagens(d["ajuste"]), np.array(d["digitos_ajuste"])
    XV, yv = imagens(d["validacao"]), np.array(d["digitos_validacao"])
    r = no_node(AJUSTE, f"""(() => {{
      const X = decodificar(DADOS.ajuste), y = DADOS.digitos_ajuste;
      const XV = decodificar(DADOS.validacao), yv = DADOS.digitos_validacao;
      const rede = iniciar(gerador(14), DADOS.tamanhos);
      const lista = r => ({{W: r.W.map(w => Array.from(w)), v: r.v.map(b => Array.from(b))}});
      const antes = lista(rede);
      let passos = 0;
      for (let e = 0; e < 3; e++) {{
        passos += epoca(rede, X, y, emOrdem(X.length), {{lote: {lote}, taxa: {taxa}, alpha: {alpha}, phi: 0}});
      }}
      return {{antes, depois: lista(rede), passos,
               ajuste: medir(rede, X, y), validacao: medir(rede, XV, yv)}};
    }})()""")
    assert r["passos"] == 3 * int(np.ceil(600 / lote))
    rede = rede_do_sklearn(
        r["antes"]["W"], r["antes"]["v"], X, y,
        learning_rate_init=taxa, alpha=alpha, batch_size=lote,
    )
    for _ in range(3):
        rede.partial_fit(X, y)
    for camada, W in enumerate(em_matrizes(r["depois"]["W"])):
        assert np.allclose(rede.coefs_[camada], W, rtol=0, atol=1e-9)
        assert np.allclose(rede.intercepts_[camada], r["depois"]["v"][camada], rtol=0, atol=1e-9)
    for parte, (Xp, yp) in {"ajuste": (X, y), "validacao": (XV, yv)}.items():
        probabilidades = rede.predict_proba(Xp)
        assert r[parte]["perda"] == pytest.approx(log_loss(yp, probabilidades, labels=np.arange(10)))
        assert r[parte]["erros"] == int((probabilidades.argmax(axis=1) != yp).sum())


@PRECISA_DE_NODE
def test_dropout_no_node_desliga_a_fracao_pedida_e_compensa_o_que_fica():
    r = no_node(AJUSTE, """(() => {
      const X = decodificar(DADOS.ajuste), y = DADOS.digitos_ajuste;
      const rede = iniciar(gerador(14), DADOS.tamanhos);
      const fracoes = [0.2, 0.5].map(phi => {
        const rng = gerador(7);
        let zeros = 0, total = 0, outros = new Set();
        for (let t = 0; t < 200; t++) {
          for (const m of sortearMascaras(rede, phi, rng)) {
            for (const fator of m) { total += 1; if (fator === 0) zeros += 1; else outros.add(fator); }
          }
        }
        return {phi, fracao: zeros / total, fatores: Array.from(outros)};
      });
      const tamanhos = sortearMascaras(rede, 0.5, gerador(7)).map(m => m.length);
      const linhas = emOrdem(20);
      const g = semente => Array.from(gradiente(rede, X, y, linhas, {phi: 0.5, rng: gerador(semente)}).W[2]);
      const mascaras = sortearMascaras(rede, 0.5, gerador(7));
      const ida = adiante(rede, X[0], mascaras);
      const delta = atras(rede, ida, y[0], mascaras);
      const desligadas = [0, 1].map(c => Array.from(mascaras[c + 1]).map((m, k) => m === 0 ? [ida.a[c + 1][k], delta[c][k]] : null).filter(p => p));
      return {fracoes, tamanhos, repete: g(3), deNovo: g(3), outro: g(4), desligadas,
              semDropout: medir(rede, X, y).perda};
    })()""")
    for caso in r["fracoes"]:
        assert caso["fracao"] == pytest.approx(caso["phi"], abs=0.01)
        assert caso["fatores"] == [pytest.approx(1 / (1 - caso["phi"]))]
    # Uma máscara para os pixels e uma para cada camada escondida.
    assert r["tamanhos"] == [784, 16, 16]
    assert r["repete"] == r["deNovo"]
    assert r["repete"] != r["outro"]
    # Unidade desligada: ativação zero na ida e nada volta por ela.
    for camada in r["desligadas"]:
        assert camada and all(par == [0, 0] for par in camada)


@PRECISA_DE_NODE
def test_formato_brasileiro_nas_redes():
    assert no_node(IDA, "fmt(6000, 0)") == "6.000"
    assert no_node(AJUSTE, "fmt(0.5632, 3)") == "0,563"
