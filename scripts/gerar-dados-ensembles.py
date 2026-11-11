"""Escreve os dados das páginas de apoio do capítulo 13 dentro delas.

As duas páginas, `apoio/bagging-de-arvores.html` (seções 13.1 e 13.2) e
`apoio/boosting-passo-a-passo.html` (seção 13.4), são arquivos únicos que
abrem com dois cliques e rodam sem rede. Os dados vão embutidos numa tag
`<script type="application/json" id="dados">`, e é este script que a preenche.

As duas usam o mesmo dado: os 263 jogadores de `Hitters` com salário, uma
coluna só (`vezes_ao_bastao_carreira`, a raiz das árvores dos capítulos 12 e
13) e a divisão de treino e teste das seções 13.1 e 13.4 (132 de treino,
`random_state=12`). Toda conta de árvore roda na própria página; aqui só vão
o dado cru e a divisão, que não dependem da plataforma:

    .venv/bin/python scripts/gerar-dados-ensembles.py
"""

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

RAIZ = Path(__file__).resolve().parent.parent
PAGINAS = [
    RAIZ / "apoio/bagging-de-arvores.html",
    RAIZ / "apoio/boosting-passo-a-passo.html",
]
COLUNA = "vezes_ao_bastao_carreira"
TAG = re.compile(r'(<script type="application/json" id="dados">)(.*?)(</script>)', re.S)


def dados() -> dict:
    """A coluna, o salário e as posições de treino e de teste, na ordem do sorteio."""
    hitters = pd.read_csv(RAIZ / "dados/Hitters.csv").dropna()
    posicoes = np.arange(len(hitters))
    treino, teste = train_test_split(posicoes, train_size=132, random_state=12)
    return {
        "coluna": COLUNA,
        "vezes": [int(v) for v in hitters[COLUNA]],
        "salario": [float(v) for v in hitters["salario"]],
        "treino": [int(i) for i in treino],
        "teste": [int(i) for i in teste],
    }


def embutir(pagina: Path, conteudo: dict) -> None:
    """Troca o conteúdo da tag `id="dados"` da página pelo JSON de `conteudo`."""
    html = pagina.read_text(encoding="utf-8")
    if not TAG.search(html):
        raise ValueError(f"{pagina.name} não tem a tag de dados")
    texto = json.dumps(conteudo, ensure_ascii=False, separators=(",", ":"))
    html = TAG.sub(lambda m: m.group(1) + texto + m.group(3), html, count=1)
    pagina.write_text(html, encoding="utf-8")


def main():
    conteudo = dados()
    for pagina in PAGINAS:
        embutir(pagina, conteudo)


if __name__ == "__main__":
    main()
