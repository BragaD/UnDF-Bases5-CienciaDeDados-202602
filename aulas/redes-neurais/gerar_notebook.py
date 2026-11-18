"""Gera `redes-neurais.ipynb` a partir dos slides.

O notebook é derivado: a fonte são os `_N-*.qmd`. Cada título de slide vira uma
célula de texto e cada chunk de Python vira uma célula de código, na mesma
ordem. Ficam de fora os chunks que só desenham os diagramas em SVG dos slides
(`#| output: asis`), que não fazem conta nenhuma.

Uso:  python gerar_notebook.py
"""

import re
from pathlib import Path

import nbformat

AQUI = Path(__file__).parent
PARTES = sorted(AQUI.glob("_[1-6]-*.qmd"))

PREPARO = '''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.set_printoptions(precision=4, suppress=True)
pd.set_option("display.precision", 4)
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25})

AZUL, CEU, NAVY, LARANJA, CINZA = "#2264AF", "#8FCEF1", "#27316E", "#D9480F", "#8A99A5"


def regiao(ax, f, lim=(-0.5, 1.5)):
    """Pinta de azul claro a região em que f(pontos) >= 0,5."""
    g = np.linspace(lim[0], lim[1], 300)
    G1, G2 = np.meshgrid(g, g)
    S = f(np.column_stack([G1.ravel(), G2.ravel()])).reshape(G1.shape)
    ax.contourf(G1, G2, S, levels=[0.5, 1e9], colors=[CEU], alpha=0.45)
    ax.contour(G1, G2, S, levels=[0.5], colors=[LARANJA], linewidths=2.5)


def pontos(ax, X, y, titulo="", lim=(-0.5, 1.5)):
    """Classe 0 vazada, classe 1 cheia."""
    ax.scatter(X[y == 0, 0], X[y == 0, 1], s=170, facecolor="white", edgecolor=NAVY, linewidth=2.5, zorder=3)
    ax.scatter(X[y == 1, 0], X[y == 1, 1], s=170, color=NAVY, zorder=3)
    ax.set(xlim=lim, ylim=lim, xticks=[0, 1], yticks=[0, 1], title=titulo, aspect="equal")'''

CHUNK = re.compile(r"^```\{python\}\n(.*?)^```$", re.S | re.M)


def celulas_da_parte(texto):
    celulas = []
    pos = 0
    for m in CHUNK.finditer(texto):
        for titulo in re.findall(r"^(#{1,2}) (.+?)(?: \{.*\})?$", texto[pos : m.start()], re.M):
            nivel, nome = titulo
            celulas.append(nbformat.v4.new_markdown_cell(f"{'#' * (len(nivel) + 1)} {nome}"))
        pos = m.end()
        codigo = m.group(1)
        if "#| output: asis" in codigo:
            continue
        linhas = [l for l in codigo.splitlines() if not l.startswith("#|")]
        celulas.append(nbformat.v4.new_code_cell("\n".join(linhas).strip()))
    return celulas


def main():
    nb = nbformat.v4.new_notebook()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.cells.append(
        nbformat.v4.new_markdown_cell(
            "# Redes neurais: do perceptron ao backpropagation\n\n"
            "O código dos slides, na ordem em que aparece na aula. Execute de cima para baixo."
        )
    )
    nb.cells.append(nbformat.v4.new_code_cell(PREPARO))
    for parte in PARTES:
        nb.cells.extend(celulas_da_parte(parte.read_text()))
    # um título seguido de outro título não tem código: sai o primeiro
    limpas = []
    for i, c in enumerate(nb.cells):
        proxima = nb.cells[i + 1] if i + 1 < len(nb.cells) else None
        if c.cell_type == "markdown" and c.source.startswith("### ") and (proxima is None or proxima.cell_type == "markdown"):
            continue
        limpas.append(c)
    nb.cells = limpas
    for i, c in enumerate(nb.cells):
        c["id"] = f"c{i:03d}"
    destino = AQUI / "redes-neurais.ipynb"
    nbformat.write(nb, destino)
    print(f"{destino.name}: {len(nb.cells)} células")


if __name__ == "__main__":
    main()
