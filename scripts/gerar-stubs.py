#!/usr/bin/env python3
"""Gera os stubs de seção e o bloco `chapters` do _quarto.yml.

Idempotente: nunca sobrescreve um arquivo que já existe. Rodar de novo depois
de escrever um capítulo é seguro.

Uso:
    python3 scripts/gerar-stubs.py            # cria os .qmd faltantes
    python3 scripts/gerar-stubs.py --yaml     # imprime o bloco chapters
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONTENT = RAIZ / "content"

# (nosso_num, grus_num, titulo_capitulo, leitura_adicional, [(arquivo, titulo_nosso, titulo_grus), ...])
# leitura_adicional: título real da seção de leituras adicionais com que o
# capítulo do Grus termina, ou None se o capítulo não tem uma. A maioria
# fecha com "For Further Exploration"; o capítulo 16 do Grus (Regressão
# Logística) fecha com "For Further Investigation"; o capítulo 1 do Grus
# não tem seção de leituras adicionais — termina em "Onward" (p.12).
# ATENÇÃO: preencher com o mapa completo da seção "Mapa completo de capítulos e
# seções" do plano. Reproduzido aqui na íntegra — 17 capítulos, 88 seções.
LIVRO = [
    (1, 1, "Introdução", None, [
        ("01-a-ascensao-dos-dados", "A Ascensão dos Dados", "The Ascendance of Data"),
        ("02-o-que-e-ciencia-de-dados", "O que é Ciência de Dados?", "What Is Data Science?"),
        ("03-hipotese-motivadora-datasciencester", "Hipótese Motivadora: DataSciencester", "Motivating Hypothetical: DataSciencester"),
    ]),
    (2, 2, "Um Curso Rápido de Python", "For Further Exploration", [
        ("01-ambiente-e-sintaxe", "Ambiente e Sintaxe", "The Zen of Python; Getting Python; Virtual Environments; Whitespace Formatting; Modules"),
        ("02-funcoes-strings-excecoes", "Funções, Strings e Exceções", "Functions; Strings; Exceptions"),
        ("03-estruturas-de-dados", "Estruturas de Dados", "Lists; Tuples; Dictionaries; defaultdict; Counters; Sets"),
        ("04-controle-de-fluxo", "Controle de Fluxo", "Control Flow; Truthiness; Sorting; List Comprehensions"),
        ("05-testes-classes-e-geradores", "Testes, Classes e Geradores", "Automated Testing and assert; Object-Oriented Programming; Iterables and Generators"),
        ("06-ferramentas-e-tipos", "Ferramentas e Anotações de Tipo", "Randomness; Regular Expressions; Functional Programming; zip and Argument Unpacking; args and kwargs; Type Annotations; Welcome to DataSciencester!"),
    ]),
    (3, 3, "Visualizando Dados", "For Further Exploration", [
        ("01-matplotlib", "matplotlib", "matplotlib"),
        ("02-graficos-de-barras", "Gráficos de Barras", "Bar Charts"),
        ("03-graficos-de-linhas", "Gráficos de Linhas", "Line Charts"),
        ("04-graficos-de-dispersao", "Gráficos de Dispersão", "Scatterplots"),
    ]),
    (4, 4, "Álgebra Linear", "For Further Exploration", [
        ("01-vetores", "Vetores", "Vectors"),
        ("02-matrizes", "Matrizes", "Matrices"),
    ]),
    (5, 8, "Gradiente Descendente", "For Further Exploration", [
        ("01-a-ideia-por-tras-do-gradiente", "A Ideia por Trás do Gradiente Descendente", "The Idea Behind Gradient Descent"),
        ("02-estimando-o-gradiente", "Estimando o Gradiente", "Estimating the Gradient"),
        ("03-usando-o-gradiente", "Usando o Gradiente", "Using the Gradient"),
        ("04-escolhendo-o-tamanho-do-passo", "Escolhendo o Tamanho do Passo", "Choosing the Right Step Size"),
        ("05-ajustando-modelos", "Ajustando Modelos com Gradiente Descendente", "Using Gradient Descent to Fit Models"),
        ("06-minibatch-e-estocastico", "Minibatch e Gradiente Estocástico", "Minibatch and Stochastic Gradient Descent"),
    ]),
    (6, 9, "Obtendo Dados", "For Further Exploration", [
        ("01-stdin-e-stdout", "stdin e stdout", "stdin and stdout"),
        ("02-lendo-arquivos", "Lendo Arquivos", "Reading Files"),
        ("03-raspando-a-web", "Raspando a Web", "Scraping the Web"),
        ("04-usando-apis", "Usando APIs", "Using APIs"),
        ("05-exemplo-apis-do-twitter", "Exemplo: As APIs do Twitter", "Example: Using the Twitter APIs"),
    ]),
    (7, 10, "Trabalhando com Dados", "For Further Exploration", [
        ("01-explorando-seus-dados", "Explorando Seus Dados", "Exploring Your Data"),
        ("02-namedtuples", "Usando NamedTuples", "Using NamedTuples"),
        ("03-dataclasses", "Dataclasses", "Dataclasses"),
        ("04-limpeza-e-transformacao", "Limpeza e Transformação", "Cleaning and Munging"),
        ("05-manipulando-dados", "Manipulando Dados", "Manipulating Data"),
        ("06-reescalonamento", "Reescalonamento", "Rescaling"),
        ("07-um-parenteses-tqdm", "Um Parêntese: tqdm", "An Aside: tqdm"),
        ("08-reducao-de-dimensionalidade", "Redução de Dimensionalidade", "Dimensionality Reduction"),
    ]),
    (8, 11, "Machine Learning", "For Further Exploration", [
        ("01-modelagem", "Modelagem", "Modeling"),
        ("02-o-que-e-machine-learning", "O que é Machine Learning?", "What Is Machine Learning?"),
        ("03-overfitting-e-underfitting", "Overfitting e Underfitting", "Overfitting and Underfitting"),
        ("04-correcao", "Correção", "Correctness"),
        ("05-vies-e-variancia", "O Compromisso Viés-Variância", "The Bias-Variance Tradeoff"),
        ("06-extracao-e-selecao-de-atributos", "Extração e Seleção de Atributos", "Feature Extraction and Selection"),
    ]),
    (9, 12, "k-Vizinhos Mais Próximos", "For Further Exploration", [
        ("01-o-modelo", "O Modelo", "The Model"),
        ("02-exemplo-o-dataset-iris", "Exemplo: O Dataset Iris", "Example: The Iris Dataset"),
        ("03-a-maldicao-da-dimensionalidade", "A Maldição da Dimensionalidade", "The Curse of Dimensionality"),
    ]),
    (10, 13, "Naive Bayes", "For Further Exploration", [
        ("01-um-filtro-de-spam-bem-burro", "Um Filtro de Spam Bem Burro", "A Really Dumb Spam Filter"),
        ("02-um-filtro-mais-sofisticado", "Um Filtro de Spam Mais Sofisticado", "A More Sophisticated Spam Filter"),
        ("03-implementacao", "Implementação", "Implementation"),
        ("04-testando-o-modelo", "Testando o Modelo", "Testing Our Model"),
        ("05-usando-o-modelo", "Usando o Modelo", "Using Our Model"),
    ]),
    (11, 14, "Regressão Linear Simples", "For Further Exploration", [
        ("01-o-modelo", "O Modelo", "The Model"),
        ("02-usando-gradiente-descendente", "Usando Gradiente Descendente", "Using Gradient Descent"),
        ("03-maxima-verossimilhanca", "Estimação por Máxima Verossimilhança", "Maximum Likelihood Estimation"),
    ]),
    (12, 15, "Regressão Múltipla", "For Further Exploration", [
        ("01-o-modelo", "O Modelo", "The Model"),
        ("02-hipoteses-do-minimos-quadrados", "Outras Hipóteses do Modelo de Mínimos Quadrados", "Further Assumptions of the Least Squares Model"),
        ("03-ajustando-o-modelo", "Ajustando o Modelo", "Fitting the Model"),
        ("04-interpretando-o-modelo", "Interpretando o Modelo", "Interpreting the Model"),
        ("05-qualidade-do-ajuste", "Qualidade do Ajuste", "Goodness of Fit"),
        ("06-digressao-o-bootstrap", "Digressão: O Bootstrap", "Digression: The Bootstrap"),
        ("07-erros-padrao-dos-coeficientes", "Erros Padrão dos Coeficientes", "Standard Errors of Regression Coefficients"),
        ("08-regularizacao", "Regularização", "Regularization"),
    ]),
    (13, 16, "Regressão Logística", "For Further Investigation", [
        ("01-o-problema", "O Problema", "The Problem"),
        ("02-a-funcao-logistica", "A Função Logística", "The Logistic Function"),
        ("03-aplicando-o-modelo", "Aplicando o Modelo", "Applying the Model"),
        ("04-qualidade-do-ajuste", "Qualidade do Ajuste", "Goodness of Fit"),
        ("05-maquinas-de-vetores-de-suporte", "Máquinas de Vetores de Suporte", "Support Vector Machines"),
    ]),
    (14, 17, "Árvores de Decisão", "For Further Exploration", [
        ("01-o-que-e-uma-arvore-de-decisao", "O que é uma Árvore de Decisão?", "What Is a Decision Tree?"),
        ("02-entropia", "Entropia", "Entropy"),
        ("03-a-entropia-de-uma-particao", "A Entropia de uma Partição", "The Entropy of a Partition"),
        ("04-criando-uma-arvore", "Criando uma Árvore de Decisão", "Creating a Decision Tree"),
        ("05-juntando-tudo", "Juntando Tudo", "Putting It All Together"),
        ("06-florestas-aleatorias", "Florestas Aleatórias", "Random Forests"),
    ]),
    (15, 18, "Redes Neurais", "For Further Exploration", [
        ("01-perceptrons", "Perceptrons", "Perceptrons"),
        ("02-redes-feed-forward", "Redes Neurais Feed-Forward", "Feed-Forward Neural Networks"),
        ("03-retropropagacao", "Retropropagação", "Backpropagation"),
        ("04-exemplo-fizz-buzz", "Exemplo: Fizz Buzz", "Example: Fizz Buzz"),
    ]),
    (16, 19, "Deep Learning", "For Further Exploration", [
        ("01-o-tensor", "O Tensor", "The Tensor"),
        ("02-a-abstracao-de-camada", "A Abstração de Camada", "The Layer Abstraction"),
        ("03-a-camada-linear", "A Camada Linear", "The Linear Layer"),
        ("04-redes-como-sequencia-de-camadas", "Redes como Sequência de Camadas", "Neural Networks as a Sequence of Layers"),
        ("05-perda-e-otimizacao", "Perda e Otimização", "Loss and Optimization; Example: XOR Revisited"),
        ("06-outras-funcoes-de-ativacao", "Outras Funções de Ativação", "Other Activation Functions; Example: FizzBuzz Revisited"),
        ("07-softmax-e-dropout", "Softmax, Entropia Cruzada e Dropout", "Softmaxes and Cross-Entropy; Dropout"),
        ("08-exemplo-mnist", "Exemplo: MNIST", "Example: MNIST; Saving and Loading Models"),
    ]),
    (17, 20, "Clustering", "For Further Exploration", [
        ("01-a-ideia", "A Ideia", "The Idea"),
        ("02-o-modelo", "O Modelo", "The Model"),
        ("03-exemplo-encontros", "Exemplo: Encontros", "Example: Meetups"),
        ("04-escolhendo-k", "Escolhendo k", "Choosing k"),
        ("05-exemplo-clustering-de-cores", "Exemplo: Clustering de Cores", "Example: Clustering Colors"),
        ("06-clustering-hierarquico", "Clustering Hierárquico Bottom-Up", "Bottom-Up Hierarchical Clustering"),
    ]),
]


def stub_secao(titulo: str, grus_cap: int, titulo_grus: str) -> str:
    return f"""# {titulo}

::: {{.callout-note}}
Esta seção corresponde a *{titulo_grus}*, do capítulo {grus_cap} de @grus2019.
:::

::: {{.callout-warning}}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
"""


def stub_index(nosso: int, grus_cap: int, titulo: str, leitura_titulo, secoes) -> str:
    linhas = [
        f"# {titulo}",
        "",
        "::: {.callout-note}",
        f"Este capítulo corresponde ao capítulo {grus_cap} de @grus2019.",
        ":::",
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
    for i, (arquivo, titulo_secao, _) in enumerate(secoes, start=1):
        linhas.append(f"| [{nosso}.{i}]({arquivo}.qmd) | {titulo_secao} |")
    linhas += ["", "## Leituras adicionais", ""]
    if leitura_titulo is None:
        linhas += [
            f"*O capítulo {grus_cap} de @grus2019 não traz uma seção de leituras "
            "adicionais — sugestões para este capítulo entram aqui.*",
            "",
        ]
    else:
        linhas += [
            f"*A seção “{leitura_titulo}” do capítulo {grus_cap} de @grus2019 entra aqui.*",
            "",
        ]
    return "\n".join(linhas)


def gerar() -> None:
    criados = pulados = 0
    for nosso, grus_cap, titulo, leitura_titulo, secoes in LIVRO:
        d = CONTENT / f"cap{nosso:02d}"
        d.mkdir(parents=True, exist_ok=True)

        alvo = d / "index.qmd"
        if alvo.exists():
            pulados += 1
        else:
            alvo.write_text(stub_index(nosso, grus_cap, titulo, leitura_titulo, secoes), encoding="utf-8")
            criados += 1

        for arquivo, titulo_secao, titulo_grus in secoes:
            alvo = d / f"{arquivo}.qmd"
            if alvo.exists():
                pulados += 1
                continue
            alvo.write_text(stub_secao(titulo_secao, grus_cap, titulo_grus), encoding="utf-8")
            criados += 1
    print(f"criados: {criados}   pulados (já existiam): {pulados}")


def imprimir_yaml() -> None:
    print("  chapters:")
    print('    - text: "Início"')
    print("      href: index.qmd")
    for nosso, grus_cap, titulo, leitura_titulo, secoes in LIVRO:
        print(f'    - part: "Capítulo {nosso}: {titulo}"')
        print("      chapters:")
        print(f"        - href: content/cap{nosso:02d}/index.qmd")
        print('          text: "Visão Geral"')
        for arquivo, titulo_secao, _ in secoes:
            print(f"        - href: content/cap{nosso:02d}/{arquivo}.qmd")
            print(f'          text: "{titulo_secao}"')


if __name__ == "__main__":
    if "--yaml" in sys.argv:
        imprimir_yaml()
    else:
        gerar()
