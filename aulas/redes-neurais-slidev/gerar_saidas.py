"""Executa os trechos de snippets/ na ordem de snippets/_ordem.txt, num espaço de nomes só.

Grava a saída de cada trecho em saidas/ (texto impresso em .txt, DataFrame em .html)
e as figuras em public/fig/. Os slides mostram o código de snippets/ e a saída de saidas/:
nenhum número de saída é digitado à mão.

Uso (na pasta deste arquivo):
    MPLBACKEND=Agg PYTHONHASHSEED=0 ../../.venv/bin/python gerar_saidas.py
"""
import ast
import contextlib
import io
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RAIZ = Path(__file__).parent
SAIDAS = RAIZ / "saidas"
FIGURAS = RAIZ / "public" / "fig"


def salvar(nome):
    plt.gcf().savefig(FIGURAS / f"{nome}.svg", bbox_inches="tight", metadata={"Date": None})
    plt.close("all")


SAIDAS.mkdir(exist_ok=True)
FIGURAS.mkdir(parents=True, exist_ok=True)
warnings.filterwarnings("ignore")
nomes = {"salvar": salvar}

for nome in (RAIZ / "snippets" / "_ordem.txt").read_text().split():
    arvore = ast.parse((RAIZ / "snippets" / f"{nome}.py").read_text())
    ultima = None
    if arvore.body and isinstance(arvore.body[-1], ast.Expr):
        ultima = ast.Expression(arvore.body.pop().value)
    impresso = io.StringIO()
    with contextlib.redirect_stdout(impresso):
        exec(compile(arvore, nome, "exec"), nomes)
        valor = eval(compile(ultima, nome, "eval"), nomes) if ultima is not None else None
    texto, tabela = impresso.getvalue(), ""
    if isinstance(valor, pd.DataFrame):
        tabela = valor.to_html(border=0)
    elif valor is not None:
        texto += repr(valor) + "\n"
    (SAIDAS / f"{nome}.txt").write_text(texto)
    (SAIDAS / f"{nome}.html").write_text(tabela)
    print(f"{nome}: {len(texto.splitlines())} linha(s) de texto" + (" + tabela" if tabela else ""))
