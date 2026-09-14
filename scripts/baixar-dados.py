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
# `Credit` e `Auto` entram com o capítulo 8 (ISLP 3): o primeiro é o exemplo
# de preditor qualitativo e de colinearidade, o segundo o de termo não linear
# e o de diagnóstico de resíduo.
# `College` entra com a lista computacional 1: o exercício 3 dela é o 2.8 do
# ISLP, que percorre o conjunto inteiro com `read_csv`, `describe` e uma matriz
# de dispersão.
BASE_ISLP = "https://www.statlearning.com/s/"
for nome in ["Advertising", "Income1", "Income2", "Credit", "Auto", "College"]:
    baixar(BASE_ISLP + f"{nome}.csv", DADOS / f"{nome}.csv")

# O site do livro publica só uma parte dos conjuntos. O resto vem do pacote
# dos próprios autores, que os traz como CSV prontos — ver a emenda de
# 2026-09-14 na spec da estrutura. Isto NÃO torna o ISLP uma dependência: o
# pacote nunca é importado, e o que se extrai dele é o dado, uma vez.
VERSAO_ISLP = "0.4.1"
WHEEL_ISLP = (
    "https://files.pythonhosted.org/packages/52/75/"
    "32fbb4fee997971aa0535790fe2e161cfb6307171ae882aa47c36d7a4719/"
    f"islp-{VERSAO_ISLP}-py3-none-any.whl"
)


def extrair_do_pacote(nomes: list[str]) -> None:
    """Baixa o wheel do ISLP uma vez e extrai os CSV pedidos."""
    import io
    import zipfile

    faltando = [n for n in nomes if not (DADOS / f"{n}.csv").exists()]
    if not faltando:
        for n in nomes:
            print(f"skip  dados/{n}.csv (já existe)")
        return
    print(f"baixa o wheel do ISLP {VERSAO_ISLP} para extrair: {', '.join(faltando)}")
    with urllib.request.urlopen(WHEEL_ISLP) as r:
        wheel = zipfile.ZipFile(io.BytesIO(r.read()))
    for n in faltando:
        (DADOS / f"{n}.csv").write_bytes(wheel.read(f"ISLP/data/{n}.csv"))
        print(f"extrai dados/{n}.csv")


extrair_do_pacote(["Default"])

print("---")
print("Revise os arquivos e commite-os. Este script não roda no render.")
