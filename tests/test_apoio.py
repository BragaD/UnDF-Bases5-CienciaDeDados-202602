"""As páginas de `apoio/` do capítulo 12: dados embutidos e o núcleo de cada uma.

Os dados das duas páginas saem de `scripts/gerar-dados-arvores.py`, rodado no
container, e ficam numa tag `<script type="application/json" id="dados">`. Os
testes daqui leem essa tag e cobram que ela traga os números das seções 12.1
e 12.2: uma página projetada ao lado do texto não pode contradizê-lo.
"""

import json
import re
from pathlib import Path

import pandas as pd

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
