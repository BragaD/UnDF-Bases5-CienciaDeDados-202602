#!/usr/bin/env python3
"""Gera o notebook de uma lista computacional, a partir do .qmd em atividades/.

A lista é fonte igual a um capítulo do livro: um `.qmd`, e o notebook do aluno
é derivado dele. Mas não é capítulo — não mora em `content/cap*/`, não é
contada pelos testes de total do livro, e não tem gabarito nem PDF de
enunciado (decisão do autor: o notebook É o enunciado, sem a maquinaria de
dupla renderização que a lista 1 usa). Por isso o gerador é um script novo e
fino, que REUSA o parser de `scripts/gerar-notebooks.py` em vez de
duplicá-lo — o mesmo padrão que `scripts/gerar-stubs.py` já usa para importar
`apelido` de lá.

O contrato entre o enunciado, o aluno e a suíte é a marca literal de uma
célula de resposta: uma célula de código contém só `# sua resposta`; uma
célula de texto contém só `*sua resposta aqui*`. O parser importado já isola
sozinha uma célula de código de resposta — todo chunk ```{python}``` sempre
vira sua própria célula, porque um chunk sempre força a saída do parágrafo
acumulado antes dele. Uma célula de TEXTO de resposta não tem esse empurrão:
o parser só abre célula nova ao redor de um chunk ou de um div com código
dentro, então uma marca solta no meio de um parágrafo ficaria espremida na
mesma célula da pergunta — e o teste que proíbe resposta preenchida não
teria como reconhecer a célula.

A solução é dividir o corpo do `.qmd` nas linhas que são exatamente a marca
de texto, ANTES de entregar cada pedaço ao `G.converte`: a marca sempre sai
como o único conteúdo do pedaço que a contém, e vira uma célula sozinha; o
resto do parágrafo, antes e depois dela, vira outra(s).
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ATIVIDADES = RAIZ / "atividades"


def _carregar_gerador():
    """Importa scripts/gerar-notebooks.py (o hífen impede um `import` normal).

    Mesmo padrão de `scripts/gerar-stubs.py:_carregar_apelido` e de
    `tests/test_notebooks.py:carregar_gerador`.
    """
    caminho = RAIZ / "scripts" / "gerar-notebooks.py"
    spec = importlib.util.spec_from_file_location("gerar_notebooks", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


G = _carregar_gerador()

# Reexportados de gerar-notebooks.py para que quem gera e quem testa usem um
# módulo só — o teste de defasagem precisa serializar do mesmo jeito que o
# gerador, e importar os dois separadamente é como as duas pontas divergem.
normaliza = G.normaliza
serializa = G.serializa

MARCA_TEXTO = "*sua resposta aqui*"

# O cabeçalho YAML do .qmd (título, autor, idioma) não vira célula — é
# metadado do arquivo-fonte, não conteúdo do notebook.
FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.S)

# "lista-comp-01" -> "Lista Computacional 1". Só para o metadado `title` do
# notebook; não depende de biblioteca de YAML nenhuma.
NUMERO_NA_LISTA = re.compile(r"lista-comp-0*(\d+)")


def _remove_cabecalho(texto: str) -> str:
    return FRONTMATTER.sub("", texto, count=1)


def _linhas_livres_para_corte(linhas: list[str]) -> list[bool]:
    """Para cada linha, diz se ela está FORA de toda cerca e de todo div aberto.

    Espelha a MESMA leitura que `G.converte` faz de cerca (```` ``` ````) e de
    div (`::: {...}` / `:::`), para a partição nunca discordar do parser que
    processa o pedaço depois dela — inclusive a ordem de prioridade: uma vez
    dentro de um div, a varredura real não repara mais em cerca (é o laço
    "naive" de `converte` que só conta abertura/fechamento de `:::` até o div
    balancear, e só a chamada recursiva de `converte_div` sobre o corpo do
    div volta a reconhecer cerca); só fora de qualquer div é que uma cerca de
    código pode abrir.
    """
    livre = [False] * len(linhas)
    fence_fecho: str | None = None
    profundidade_div = 0
    for i, linha in enumerate(linhas):
        if profundidade_div > 0:
            if G.DIV_ABRE.match(linha):
                profundidade_div += 1
            elif G.DIV_FECHA.match(linha):
                profundidade_div -= 1
            continue
        if fence_fecho is not None:
            if linha.startswith(fence_fecho):
                fence_fecho = None
            continue
        if m := G.CERCA.match(linha):
            fence_fecho = m.group(1)
            continue
        if G.DIV_ABRE.match(linha):
            profundidade_div = 1
            continue
        livre[i] = True
    return livre


def _particiona_nas_marcas(corpo: str) -> list[str]:
    """Isola, num pedaço próprio, cada linha que é exatamente a marca de texto.

    `G.converte` só abre célula nova ao redor de um chunk `{python}` ou de um
    div com código dentro; um parágrafo solto nunca ganha célula própria.
    Chamar `G.converte` uma vez por pedaço, em vez de uma vez no corpo
    inteiro, é o que garante que a marca sempre saia isolada.

    Mas só é seguro cortar numa linha que esteja FORA de toda cerca e de todo
    div aberto: `G.converte`, chamado por pedaço e sem estado entre chamadas,
    não casa abertura de div/cerca com fechamento através da fronteira do
    corte — um corte no meio de um `::: {...} ... :::` deixaria o `:::` de
    fechamento sobrar como texto cru no pedaço seguinte, e um corte no meio
    de uma cerca quebraria o bloco de código da mesma forma. Por isso a marca
    só vira ponto de corte quando `_linhas_livres_para_corte` diz que ela está
    livre; uma marca dentro de cerca ou de div fica onde está, e o pedaço que
    a contém — cerca ou div inteiros — vai para `G.converte` de uma vez.
    """
    linhas = corpo.split("\n")
    livre = _linhas_livres_para_corte(linhas)
    partes: list[str] = []
    atual: list[str] = []
    for linha, esta_livre in zip(linhas, livre):
        if esta_livre and linha.strip() == MARCA_TEXTO:
            partes.append("\n".join(atual))
            partes.append(MARCA_TEXTO)
            atual = []
        else:
            atual.append(linha)
    partes.append("\n".join(atual))
    return partes


def titulo_da_lista(fonte: Path) -> str:
    m = NUMERO_NA_LISTA.match(fonte.stem)
    return f"Lista Computacional {m.group(1)}" if m else fonte.stem


def gerar_lista(fonte: Path) -> dict:
    """O notebook de uma lista, em memória, a partir do .qmd fonte.

    Monta o notebook nesta ordem: a célula de preparo (`G.CELULA_PREPARO`,
    que clona o repositório quando o Colab não encontra o projeto — é o que
    põe `dados/` ao alcance do aluno), e depois as células que `G.converte`
    produz a partir do corpo do `.qmd`. O cabeçalho YAML não vira célula.
    """
    texto = fonte.read_text(encoding="utf-8")
    corpo = _remove_cabecalho(texto)

    entradas = G.le_bibliografia()
    curtas = {chave: G.citacao_curta(campos) for chave, campos in entradas.items()}
    dir_fonte = str(fonte.resolve().parent.relative_to(RAIZ))

    celulas = [G.celula_codigo(G.CELULA_PREPARO)]
    for parte in _particiona_nas_marcas(corpo):
        celulas += G.converte(parte, dir_fonte, 0, curtas)

    return {
        "cells": celulas,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
            "title": titulo_da_lista(fonte),
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> int:
    fontes = sorted(ATIVIDADES.glob("lista-comp-*.qmd"))
    esperados = set()
    for fonte in fontes:
        nb = normaliza(gerar_lista(fonte))
        destino = fonte.with_suffix(".ipynb")
        esperados.add(destino.name)
        destino.write_text(serializa(nb), encoding="utf-8")
        codigo = sum(1 for c in nb["cells"] if c["cell_type"] == "code")
        print(f"{destino.name:32} {len(nb['cells']):3} células ({codigo} de código)")

    for orfao in sorted(ATIVIDADES.glob("lista-comp-*.ipynb")):
        if orfao.name not in esperados:
            orfao.unlink()
            print(f"removido (fonte não existe mais): {orfao.name}")

    print(f"\n{len(fontes)} lista(s) em {ATIVIDADES.relative_to(RAIZ)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
