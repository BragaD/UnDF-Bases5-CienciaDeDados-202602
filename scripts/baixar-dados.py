#!/usr/bin/env python3
"""Coleta única dos dados externos do livro. Os resultados são COMMITADOS.

Rodar com:
    docker compose run --rm --no-deps livro python scripts/baixar-dados.py

Isto não é um chunk do livro. Um livro que faz chamadas de rede a cada render
é frágil: a página raspada muda de layout, a API sai do ar, e o material
quebra sem ninguém ter tocado no repositório.
"""
import shutil
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"
DADOS.mkdir(exist_ok=True)


def baixar(url: str, destino: Path) -> None:
    if destino.exists():
        print(f"skip  {destino.relative_to(RAIZ)} (já existe)")
        return
    destino.parent.mkdir(parents=True, exist_ok=True)
    print(f"baixa {destino.relative_to(RAIZ)} <- {url}")
    with urllib.request.urlopen(url) as r, destino.open("wb") as f:
        shutil.copyfileobj(r, f)


# Conjuntos do ISLP (@james2023), do site do livro. O capítulo 7 usa os três:
# Advertising abre o capítulo 2; Income1 e Income2 são as figuras em que o f
# verdadeiro é conhecido. Os cabeçalhos são traduzidos manualmente depois do
# download — ver a tabela de-para em dados/README.md — e este script baixa
# sempre a versão original em inglês, com o índice do R.
BASE_ISLP = "https://www.statlearning.com/s/"
for nome in ["Advertising", "Income1", "Income2"]:
    baixar(BASE_ISLP + f"{nome}.csv", DADOS / f"{nome}.csv")

print("---")
print("Revise os arquivos e commite-os. Este script não roda no render.")
