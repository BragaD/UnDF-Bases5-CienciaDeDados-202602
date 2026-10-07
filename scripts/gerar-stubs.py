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
import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONTENT = RAIZ / "content"


def _carregar_apelido():
    """Importa `apelido` de scripts/gerar-notebooks.py (o hífen impede `import` normal).

    Mesmo padrão de `tests/test_notebooks.py:carregar_gerador` — importar por
    caminho em vez de duplicar a tabela de acentos aqui.
    """
    caminho = RAIZ / "scripts" / "gerar-notebooks.py"
    spec = importlib.util.spec_from_file_location("gerar_notebooks", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo.apelido


apelido = _carregar_apelido()

# (nosso_num, titulo_capitulo, islp_cap, [(arquivo, titulo_secao, islp_secao), ...])
#
# `islp_cap` e `islp_secao` são o capítulo e a seção correspondentes em
# @james2023, ou None quando não há correspondência. `islp_cap` é um `int`
# quando o nosso capítulo cobre um capítulo inteiro do ISLP, ou uma `str`
# ("8.1") quando cobre só uma seção dele — o capítulo 8 do ISLP vira os
# nossos 12 (8.1) e 13 (8.2); `stub_index` ajusta a frase a partir do tipo. O ISLP **numera** as
# seções — 3.3.1, 8.2.2, 12.4.1 estão no sumário —, então o callout de
# abertura cita o número. Os capítulos 1 a 5 são de outra abordagem e não
# citam o ISLP; o 6 e o 17 não têm correspondência nele.
#
# `islp_secao` é `None`, uma `str` ("2.1.2") ou uma `tuple[str, ...]`
# ("2.1.4", "2.1.5") quando a nossa seção cobre mais de uma subseção do
# ISLP — comum a partir do capítulo 8, onde quase toda seção nossa mapeia
# para mais de uma subseção. `stub_secao` cuida da concordância (singular
# contra plural) a partir do tipo.
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
    (6, "Dados: Tipos, Dados Retangulares e pandas", None, [
        ("01-elementos-de-dados-estruturados", "Elementos de Dados Estruturados", None),
        ("02-dados-retangulares", "Dados Retangulares", None),
        ("03-lendo-e-tipando-um-arquivo-real", "Lendo e Tipando um Arquivo Real", None),
        ("04-limpando-e-transformando", "Limpando e Transformando", None),
        ("05-agrupando-e-resumindo", "Agrupando e Resumindo", None),
        ("06-da-tabela-para-o-modelo", "Da Tabela para o Modelo", None),
    ]),
    (7, "O que é Aprendizado Estatístico", 2, [
        ("01-o-array", "O Array", "2.3"),
        ("02-estimar-f", "Estimar f: Predição e Inferência", ("2.1", "2.1.1")),
        ("03-parametrico-e-nao-parametrico", "Paramétrico e Não Paramétrico", "2.1.2"),
        ("04-precisao-contra-interpretabilidade", "Precisão contra Interpretabilidade", "2.1.3"),
        ("05-supervisionado-e-nao-supervisionado", "Supervisionado e Não Supervisionado", ("2.1.4", "2.1.5")),
        ("06-qualidade-do-ajuste-e-vies-variancia", "Qualidade do Ajuste e o Compromisso Viés-Variância", ("2.2.1", "2.2.2")),
        ("07-classificacao-e-o-classificador-de-bayes", "Classificação e o Classificador de Bayes", "2.2.3"),
    ]),
    (8, "Regressão Linear", 3, [
        ("01-regressao-linear-simples", "Regressão Linear Simples", ("3.1", "3.1.1")),
        ("02-avaliando-o-ajuste", "Avaliando o Ajuste: R² e Erro", "3.1.3"),
        ("03-regressao-multipla", "Regressão Múltipla", "3.2"),
        ("04-preditores-qualitativos", "Preditores Qualitativos", "3.3.1"),
        ("05-interacao-e-termos-nao-lineares", "Interação e Termos Não Lineares", "3.3.2"),
        ("06-outliers-alavancagem-e-colinearidade", "Outliers, Alavancagem e Colinearidade", "3.3.3"),
        ("07-regressao-linear-contra-k-vizinhos", "Regressão Linear contra k-NN", "3.5"),
    ]),
    (9, "Classificação", 4, [
        ("01-por-que-nao-regressao-linear", "Por que Não Regressão Linear", ("4.1", "4.2")),
        ("02-regressao-logistica", "Regressão Logística", ("4.3.1", "4.3.2", "4.3.3", "4.3.4")),
        ("03-logistica-multinomial", "Logística Multinomial", "4.3.5"),
        ("04-naive-bayes", "Naive Bayes", ("4.4", "4.4.4", "4.5.1")),
        ("05-avaliando-um-classificador", "Avaliando um Classificador", "4.4.2"),
        ("06-comparando-os-metodos", "Comparando os Métodos", "4.5"),
        ("07-leitura-complementar-lda-e-qda", "Leitura Complementar: LDA e QDA", ("4.4.1", "4.4.2", "4.4.3", "4.5.1")),
    ]),
    (10, "Reamostragem", 5, [
        ("01-o-conjunto-de-validacao", "O Conjunto de Validação", "5.1.1"),
        ("02-leave-one-out", "Validação Cruzada Leave-One-Out", "5.1.2"),
        ("03-validacao-cruzada-k-fold", "Validação Cruzada k-Fold", "5.1.3"),
        ("04-vies-e-variancia-na-validacao-cruzada", "Viés e Variância na Validação Cruzada", "5.1.4"),
        ("05-validacao-cruzada-em-classificacao", "Validação Cruzada em Classificação", "5.1.5"),
        ("06-vazamento", "Vazamento: o Pré-processamento Dentro da Validação", None),
    ]),
    (11, "Seleção de Modelos e Regularização", 6, [
        ("01-selecao-de-subconjuntos", "Seleção de Subconjuntos", ("6.1.1", "6.1.2")),
        ("02-escolhendo-o-modelo", "Escolhendo o Modelo: Cp, AIC, BIC e Validação", "6.1.3"),
        ("03-regressao-ridge", "Regressão Ridge", "6.2.1"),
        ("04-o-lasso", "O Lasso", "6.2.2"),
        ("05-escolhendo-o-parametro-de-regularizacao", "Escolhendo o Parâmetro de Regularização", "6.2.3"),
        ("06-regressao-por-componentes-principais", "Regressão por Componentes Principais", "6.3.1"),
        ("07-o-que-muda-em-alta-dimensao", "O que Muda em Alta Dimensão", "6.4"),
    ]),
    (12, "Árvores de Decisão", "8.1", [
        ("01-arvores-de-regressao", "Árvores de Regressão", "8.1.1"),
        ("02-podando-a-arvore", "Podando a Árvore", "8.1.1"),
        ("03-arvores-de-classificacao", "Árvores de Classificação", "8.1.2"),
        ("04-arvores-contra-modelos-lineares", "Árvores contra Modelos Lineares", "8.1.3"),
        ("05-vantagens-e-desvantagens", "Vantagens e Desvantagens das Árvores", "8.1.4"),
    ]),
    (13, "Bagging, Florestas e Boosting", "8.2", [
        ("01-bagging", "Bagging", "8.2.1"),
        ("02-erro-out-of-bag", "Erro Out-of-Bag", "8.2.1"),
        ("03-florestas-aleatorias", "Florestas Aleatórias", "8.2.2"),
        ("04-boosting", "Boosting", "8.2.3"),
        ("05-importancia-de-variaveis", "Importância de Variáveis", "8.2.1"),
        ("06-resumo-dos-metodos-de-ensemble", "Resumo dos Métodos de Ensemble", "8.2.5"),
    ]),
    (14, "Redes Neurais", 10, [
        ("01-uma-rede-de-camada-unica", "Uma Rede de Camada Única", "10.1"),
        ("02-redes-multicamada", "Redes Multicamada", "10.2"),
        ("03-ajustando-uma-rede", "Ajustando uma Rede: Retropropagação, Gradiente Estocástico e Regularização", "10.7"),
        ("04-mlpclassifier-e-mlpregressor-na-pratica", "MLPClassifier e MLPRegressor na Prática", ("10.7.4", "10.9.1")),
        ("05-quando-usar-deep-learning", "Quando Usar Deep Learning", "10.6"),
    ]),
    (15, "Aprendizado Não Supervisionado", 12, [
        ("01-o-desafio-do-nao-supervisionado", "O Desafio do Não Supervisionado", "12.1"),
        ("02-componentes-principais", "Componentes Principais", ("12.2.1", "12.2.2")),
        ("03-proporcao-da-variancia-explicada", "Proporção da Variância Explicada", ("12.2.3", "12.2.4", "12.2.5")),
        ("04-k-means", "k-Means", "12.4.1"),
        ("05-clustering-hierarquico", "Clustering Hierárquico", "12.4.2"),
        ("06-questoes-praticas-em-clustering", "Questões Práticas em Clustering", ("12.4.3", "12.5.4")),
    ]),
    (16, "Máquinas de Vetores de Suporte", 9, [
        ("01-hiperplanos-e-o-classificador-de-margem-maxima", "Hiperplanos e o Classificador de Margem Máxima", "9.1"),
        ("02-o-classificador-de-vetores-de-suporte", "O Classificador de Vetores de Suporte", ("9.2", "9.5", "9.6.1")),
        ("03-kernels", "Kernels", ("9.3", "9.6.2", "9.6.3")),
        ("04-mais-de-duas-classes", "Mais de Duas Classes", ("9.4", "9.6.4", "9.6.5")),
    ]),
    (17, "Um Problema do Começo ao Fim", None, [
        ("01-o-problema-e-o-dado-cru", "O Problema e o Dado Cru", None),
        ("02-separar-antes-de-olhar", "Separar antes de Olhar: Treino, Teste e Vazamento", None),
        ("03-pre-processamento-como-parte-do-modelo", "Pré-processamento como Parte do Modelo: ColumnTransformer e Pipeline", None),
        ("04-comparando-modelos-por-validacao-cruzada", "Comparando Modelos por Validação Cruzada", None),
        ("05-ajuste-de-hiperparametros-com-gridsearchcv", "Ajuste de Hiperparâmetros com GridSearchCV", None),
        ("06-reportar", "Reportar: a Métrica Certa, e o que o Resultado Não Diz", None),
    ]),
]


def _citacao_islp(islp_secao: str | tuple[str, ...]) -> str:
    """Formata a frase do callout de correspondência, com a concordância certa.

    Uma seção só: "corresponde à seção 2.1.2". Mais de uma: "corresponde às
    seções 2.1.4 e 2.1.5" (ou, com três ou mais, "2.2.1, 2.2.2 e 2.2.3").
    """
    if isinstance(islp_secao, str):
        return f"Esta seção corresponde à seção {islp_secao} de @james2023."
    secoes = list(islp_secao)
    if len(secoes) == 1:
        return f"Esta seção corresponde à seção {secoes[0]} de @james2023."
    juntas = ", ".join(secoes[:-1]) + f" e {secoes[-1]}"
    return f"Esta seção corresponde às seções {juntas} de @james2023."


def stub_secao(titulo: str, islp_secao: str | tuple[str, ...] | None) -> str:
    correspondencia = ""
    if islp_secao is not None:
        correspondencia = (
            "\n::: {.callout-note}\n"
            f"{_citacao_islp(islp_secao)}\n"
            ":::\n"
        )
    return f"""# {titulo}
{correspondencia}
::: {{.callout-warning}}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
"""


def stub_index(nosso: int, titulo: str, islp_cap: int | str | None, secoes) -> str:
    linhas = [f"# {titulo}", ""]
    if islp_cap is not None:
        if isinstance(islp_cap, str):
            frase = f"Este capítulo corresponde à seção {islp_cap} de @james2023."
        else:
            frase = f"Este capítulo corresponde ao capítulo {islp_cap} de @james2023."
        linhas += [
            "::: {.callout-note}",
            frase,
            ":::",
            "",
        ]
    notebook = f"cap{nosso:02d}-{apelido(titulo)}.ipynb"
    linhas += [
        f"📓 [**Abrir o notebook deste capítulo no Colab ↗**](https://colab.research.google.com/github/BragaD/UnDF-Bases5-CienciaDeDados-202602/blob/main/notebooks/{notebook}) — só o código, pronto para rodar.",
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
