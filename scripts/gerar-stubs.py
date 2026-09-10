#!/usr/bin/env python3
"""Gera os stubs de seção e o bloco `chapters` do _quarto.yml.

Idempotente: nunca sobrescreve um arquivo que já existe. Rodar de novo depois
de escrever um capítulo é seguro.

Uso:
    python3 scripts/gerar-stubs.py            # cria os .qmd faltantes
    python3 scripts/gerar-stubs.py --yaml     # imprime o bloco chapters

`LIVRO` é a fonte da verdade sobre o que o livro DEVE conter: é contra ela que
`tests/test_estrutura.py` confere, capítulo por capítulo, que cada arquivo
esperado existe em disco E aparece no `_quarto.yml`. Um capítulo novo entra
aqui primeiro.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONTENT = RAIZ / "content"

# (nosso_num, titulo_capitulo, [(arquivo, titulo_secao), ...])
#
# Só os capítulos 1 a 5. Os 6 a 17 saíram do livro em 2026-09-10, com o
# abandono da abordagem do Grus — ver
# docs/superpowers/specs/2026-09-10-ruptura-com-o-grus-design.md. O material
# novo, de outras fontes, entra aqui quando o escopo estiver decidido; até lá
# a lista termina no 5 de propósito, e não por esquecimento.
LIVRO = [
    (1, "Introdução", [
        ("01-a-ascensao-dos-dados", "A Ascensão dos Dados"),
        ("02-o-que-e-ciencia-de-dados", "O que é Ciência de Dados?"),
        ("03-hipotese-motivadora-datasciencester", "Hipótese Motivadora: DataSciencester"),
    ]),
    (2, "Um Curso Rápido de Python", [
        ("01-ambiente-e-sintaxe", "Ambiente e Sintaxe"),
        ("02-funcoes-strings-excecoes", "Funções, Strings e Exceções"),
        ("03-estruturas-de-dados", "Estruturas de Dados"),
        ("04-controle-de-fluxo", "Controle de Fluxo"),
        ("05-testes-classes-e-geradores", "Testes, Classes e Geradores"),
        ("06-ferramentas-e-tipos", "Ferramentas e Anotações de Tipo"),
    ]),
    (3, "Visualizando Dados", [
        ("01-matplotlib", "matplotlib"),
        ("02-graficos-de-barras", "Gráficos de Barras"),
        ("03-graficos-de-linhas", "Gráficos de Linhas"),
        ("04-graficos-de-dispersao", "Gráficos de Dispersão"),
    ]),
    (4, "Álgebra Linear", [
        ("01-vetores", "Vetores"),
        ("02-matrizes", "Matrizes"),
    ]),
    (5, "Gradiente Descendente", [
        ("01-a-ideia-por-tras-do-gradiente", "A Ideia por Trás do Gradiente Descendente"),
        ("02-estimando-o-gradiente", "Estimando o Gradiente"),
        ("03-usando-o-gradiente", "Usando o Gradiente"),
        ("04-escolhendo-o-tamanho-do-passo", "Escolhendo o Tamanho do Passo"),
        ("05-ajustando-modelos", "Ajustando Modelos com Gradiente Descendente"),
        ("06-minibatch-e-estocastico", "Minibatch e Gradiente Estocástico"),
    ]),
]


def stub_secao(titulo: str) -> str:
    return f"""# {titulo}

::: {{.callout-warning}}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
"""


def stub_index(nosso: int, titulo: str, secoes) -> str:
    linhas = [
        f"# {titulo}",
        "",
        "::: {.callout-warning}",
        "## Em construção",
        "A visão geral deste capítulo ainda será escrita.",
        ":::",
        "",
        "## Seções",
        "",
        "| Seção | Tópico |",
        "|---|---|",
    ]
    for i, (arquivo, titulo_secao) in enumerate(secoes, start=1):
        linhas.append(f"| [{nosso}.{i}]({arquivo}.qmd) | {titulo_secao} |")
    linhas += ["", "## Leituras adicionais", "", "*A escrever.*", ""]
    return "\n".join(linhas)


def gerar() -> None:
    criados = pulados = 0
    for nosso, titulo, secoes in LIVRO:
        d = CONTENT / f"cap{nosso:02d}"
        d.mkdir(parents=True, exist_ok=True)

        alvo = d / "index.qmd"
        if alvo.exists():
            pulados += 1
        else:
            alvo.write_text(stub_index(nosso, titulo, secoes), encoding="utf-8")
            criados += 1

        for arquivo, titulo_secao in secoes:
            alvo = d / f"{arquivo}.qmd"
            if alvo.exists():
                pulados += 1
                continue
            alvo.write_text(stub_secao(titulo_secao), encoding="utf-8")
            criados += 1
    print(f"criados: {criados}   pulados (já existiam): {pulados}")


def imprimir_yaml() -> None:
    print("  chapters:")
    print('    - text: "Início"')
    print("      href: index.qmd")
    for nosso, titulo, secoes in LIVRO:
        print(f'    - part: "Capítulo {nosso}: {titulo}"')
        print("      chapters:")
        print(f"        - href: content/cap{nosso:02d}/index.qmd")
        print('          text: "Visão Geral"')
        for arquivo, titulo_secao in secoes:
            print(f"        - href: content/cap{nosso:02d}/{arquivo}.qmd")
            print(f'          text: "{titulo_secao}"')


if __name__ == "__main__":
    if "--yaml" in sys.argv:
        imprimir_yaml()
    else:
        gerar()
