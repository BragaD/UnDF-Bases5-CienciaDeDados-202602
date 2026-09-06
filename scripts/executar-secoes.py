#!/usr/bin/env python3
"""Executa cada `.qmd` de um capítulo num kernel PRÓPRIO — como o site faz.

No livro, `quarto render` roda cada `.qmd` num kernel novo: um nome definido
numa seção não existe na seguinte. O notebook de aula (`executar-notebooks.py`)
roda o capítulo inteiro num kernel só e, por isso, deixa passar o `import` que
faltou numa seção porque foi feito na anterior. Este script é o análogo fiel
do render, sem o render: para cada `.qmd`, monta em memória um notebook só com
os chunks executáveis (reaproveitando o parser de `gerar-notebooks.py`, que já
sabe o que é callout e o que é `eval: false`) e o executa do zero, com o
diretório de trabalho na raiz — o que o `execute-dir: project` faz no Quarto.

Não toca em `_freeze/` nem em `.quarto/`, então pode rodar em paralelo com
outros agentes e nunca precisa do lock do `make render`.

uso:
    executar-secoes.py 11             # todas as seções do capítulo 11
    executar-secoes.py 11 12          # dois capítulos
    executar-secoes.py content/cap11/01-o-modelo.qmd   # um arquivo só
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import time

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

RAIZ = pathlib.Path(__file__).resolve().parent.parent

# O que o `execute-dir: project` dá de graça no Quarto: cwd na raiz (feito pelo
# nbclient, via `resources.metadata.path`) e a raiz no sys.path para
# `import scratch_np` resolver. O `%matplotlib inline` é o backend que o Quarto
# usa — `plt.show()` vira saída da célula em vez de janela.
PREPARO = "import os, sys\nsys.path.insert(0, os.getcwd())\n%matplotlib inline\n"


def carregar_gerador():
    caminho = RAIZ / "scripts" / "gerar-notebooks.py"
    spec = importlib.util.spec_from_file_location("gerar_notebooks", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def fonte(celula: dict) -> str:
    origem = celula["source"]
    return origem if isinstance(origem, str) else "".join(origem)


def alvos(argv: list[str], gerador) -> list[pathlib.Path]:
    capitulos = {c["numero"]: c for c in gerador.le_capitulos()}
    saida: list[pathlib.Path] = []
    for arg in argv:
        if arg.endswith(".qmd"):
            saida.append((RAIZ / arg).resolve())
            continue
        numero = int(arg)
        if numero not in capitulos:
            sys.exit(f"capítulo {numero} não existe no _quarto.yml")
        saida += [RAIZ / href for href in capitulos[numero]["arquivos"]]
    return saida


def celulas_de_codigo(qmd: pathlib.Path, gerador, curtas) -> list[str]:
    texto = gerador.LINHA_COLAB.sub("", qmd.read_text(encoding="utf-8"))
    dir_fonte = str(qmd.parent.relative_to(RAIZ))
    celulas = gerador.converte(texto, dir_fonte, 0, curtas)
    return [fonte(c) for c in celulas if c["cell_type"] == "code"]


def executa(codigos: list[str]) -> None:
    nb = nbformat.v4.new_notebook()
    nb.cells = [nbformat.v4.new_code_cell(PREPARO)]
    nb.cells += [nbformat.v4.new_code_cell(c) for c in codigos]
    cliente = NotebookClient(
        nb,
        timeout=1200,
        kernel_name="python3",
        resources={"metadata": {"path": str(RAIZ)}},
    )
    cliente.execute()


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    gerador = carregar_gerador()
    entradas = gerador.le_bibliografia()
    curtas = {k: gerador.citacao_curta(v) for k, v in entradas.items()}

    falhas: list[tuple[str, str]] = []
    for qmd in alvos(argv, gerador):
        rel = str(qmd.relative_to(RAIZ))
        codigos = celulas_de_codigo(qmd, gerador, curtas)
        if not codigos:
            print(f"--    {rel:60} (sem chunk executável)", flush=True)
            continue
        inicio = time.monotonic()
        try:
            executa(codigos)
            print(f"OK    {rel:60} {len(codigos):3} chunks {time.monotonic() - inicio:6.1f}s", flush=True)
        except CellExecutionError as erro:
            print(f"FALHA {rel:60} {time.monotonic() - inicio:6.1f}s", flush=True)
            falhas.append((rel, str(erro)))
        except Exception as erro:  # kernel morto, timeout, etc.
            print(f"ERRO  {rel:60} {erro.__class__.__name__}", flush=True)
            falhas.append((rel, f"{erro.__class__.__name__}: {erro}"))

    print()
    if not falhas:
        print("todas as seções executaram até o fim, cada uma no seu kernel.")
        return 0
    print(f"{len(falhas)} seção(ões) falharam:\n")
    for rel, mensagem in falhas:
        print("=" * 78)
        print(rel)
        print("=" * 78)
        print(mensagem[-3000:])
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
