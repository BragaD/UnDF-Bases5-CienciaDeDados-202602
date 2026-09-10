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

# (nosso_num, titulo_capitulo, islp_cap, [(arquivo, titulo_secao, islp_secao), ...])
#
# `islp_cap` e `islp_secao` são o capítulo e a seção correspondentes em
# @james2023, ou None quando não há correspondência. O ISLP **numera** as
# seções — 3.3.1, 8.2.2, 12.4.1 estão no sumário —, então o callout de
# abertura cita o número. Os capítulos 1 a 5 são de outra abordagem e não
# citam o ISLP; o 6 e o 17 não têm correspondência nele.
LIVRO = [
    (1, "Introdução", None, [
        ("01-a-ascensao-dos-dados", "A Ascensão dos Dados", None),
        ("02-o-que-e-ciencia-de-dados", "O que é Ciência de Dados?", None),
        ("03-hipotese-motivadora-datasciencester", "Hipótese Motivadora: DataSciencester", None),
    ]),
    (2, "Um Curso Rápido de Python", None, [
        ("01-ambiente-e-sintaxe", "Ambiente e Sintaxe", None),
        ("02-funcoes-strings-excecoes", "Funções, Strings e Exceções", None),
        ("03-estruturas-de-dados", "Estruturas de Dados", None),
        ("04-controle-de-fluxo", "Controle de Fluxo", None),
        ("05-testes-classes-e-geradores", "Testes, Classes e Geradores", None),
        ("06-ferramentas-e-tipos", "Ferramentas e Anotações de Tipo", None),
    ]),
    (3, "Visualizando Dados", None, [
        ("01-matplotlib", "matplotlib", None),
        ("02-graficos-de-barras", "Gráficos de Barras", None),
        ("03-graficos-de-linhas", "Gráficos de Linhas", None),
        ("04-graficos-de-dispersao", "Gráficos de Dispersão", None),
    ]),
    (4, "Álgebra Linear", None, [
        ("01-vetores", "Vetores", None),
        ("02-matrizes", "Matrizes", None),
    ]),
    (5, "Gradiente Descendente", None, [
        ("01-a-ideia-por-tras-do-gradiente", "A Ideia por Trás do Gradiente Descendente", None),
        ("02-estimando-o-gradiente", "Estimando o Gradiente", None),
        ("03-usando-o-gradiente", "Usando o Gradiente", None),
        ("04-escolhendo-o-tamanho-do-passo", "Escolhendo o Tamanho do Passo", None),
        ("05-ajustando-modelos", "Ajustando Modelos com Gradiente Descendente", None),
        ("06-minibatch-e-estocastico", "Minibatch e Gradiente Estocástico", None),
    ]),
]


def stub_secao(titulo: str, islp_secao) -> str:
    correspondencia = ""
    if islp_secao is not None:
        correspondencia = (
            "\n::: {.callout-note}\n"
            f"Esta seção corresponde à seção {islp_secao} de @james2023.\n"
            ":::\n"
        )
    return f"""# {titulo}
{correspondencia}
::: {{.callout-warning}}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
"""


def stub_index(nosso: int, titulo: str, islp_cap, secoes) -> str:
    linhas = [f"# {titulo}", ""]
    if islp_cap is not None:
        linhas += [
            "::: {.callout-note}",
            f"Este capítulo corresponde ao capítulo {islp_cap} de @james2023.",
            ":::",
            "",
        ]
    linhas += [
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
    for i, (arquivo, titulo_secao, _islp) in enumerate(secoes, start=1):
        linhas.append(f"| [{nosso}.{i}]({arquivo}.qmd) | {titulo_secao} |")
    linhas += ["", "## Leituras adicionais", "", "*A escrever.*", ""]
    return "\n".join(linhas)


def gerar() -> None:
    criados = pulados = 0
    for nosso, titulo, islp_cap, secoes in LIVRO:
        d = CONTENT / f"cap{nosso:02d}"
        d.mkdir(parents=True, exist_ok=True)

        alvo = d / "index.qmd"
        if alvo.exists():
            pulados += 1
        else:
            alvo.write_text(stub_index(nosso, titulo, islp_cap, secoes), encoding="utf-8")
            criados += 1

        for arquivo, titulo_secao, islp_secao in secoes:
            alvo = d / f"{arquivo}.qmd"
            if alvo.exists():
                pulados += 1
                continue
            alvo.write_text(stub_secao(titulo_secao, islp_secao), encoding="utf-8")
            criados += 1
    print(f"criados: {criados}   pulados (já existiam): {pulados}")


def imprimir_yaml() -> None:
    print("  chapters:")
    print('    - text: "Início"')
    print("      href: index.qmd")
    for nosso, titulo, _islp_cap, secoes in LIVRO:
        print(f'    - part: "Capítulo {nosso}: {titulo}"')
        print("      chapters:")
        print(f"        - href: content/cap{nosso:02d}/index.qmd")
        print('          text: "Visão Geral"')
        for arquivo, titulo_secao, _islp in secoes:
            print(f"        - href: content/cap{nosso:02d}/{arquivo}.qmd")
            print(f'          text: "{titulo_secao}"')


if __name__ == "__main__":
    if "--yaml" in sys.argv:
        imprimir_yaml()
    else:
        gerar()
