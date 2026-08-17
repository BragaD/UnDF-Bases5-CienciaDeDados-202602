#!/usr/bin/env python3
"""Executa todos os notebooks de `notebooks/` e relata o que falhou.

Isto é a verificação dos notebooks, do mesmo jeito que `quarto render` é a
verificação do livro: os módulos de `scratch/` têm `assert` no nível do
módulo, então um notebook que executa até o fim provou bastante coisa.

Roda com o diretório de trabalho em `notebooks/` de propósito — é o caso
mais apertado, o do aluno que abriu o Jupyter dentro da pasta. A célula de
preparo de cada notebook tem que achar a raiz do projeto a partir dali.

As saídas **não** são gravadas de volta: os notebooks ficam limpos no git.
"""

from __future__ import annotations

import pathlib
import sys
import time

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PASTA = RAIZ / "notebooks"


def main(argv: list[str]) -> int:
    alvos = sorted(PASTA.glob("*.ipynb"))
    if argv:
        alvos = [n for n in alvos if any(a in n.name for a in argv)]
    if not alvos:
        print("nenhum notebook encontrado", file=sys.stderr)
        return 1

    falhas = []
    for caminho in alvos:
        nb = nbformat.read(caminho, as_version=4)
        cliente = NotebookClient(
            nb,
            timeout=1200,
            kernel_name="python3",
            resources={"metadata": {"path": str(PASTA)}},
        )
        inicio = time.monotonic()
        try:
            cliente.execute()
            print(f"OK    {caminho.name:52} {time.monotonic() - inicio:6.1f}s", flush=True)
        except CellExecutionError as erro:
            print(f"FALHA {caminho.name:52} {time.monotonic() - inicio:6.1f}s", flush=True)
            falhas.append((caminho.name, str(erro)))
        except Exception as erro:  # kernel morto, timeout, etc.
            print(f"ERRO  {caminho.name:52} {erro.__class__.__name__}", flush=True)
            falhas.append((caminho.name, f"{erro.__class__.__name__}: {erro}"))

    print()
    if not falhas:
        print(f"{len(alvos)} notebooks executaram até o fim.")
        return 0

    print(f"{len(falhas)} de {len(alvos)} falharam:\n")
    for nome, mensagem in falhas:
        print("=" * 78)
        print(nome)
        print("=" * 78)
        print(mensagem[-3000:])
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
