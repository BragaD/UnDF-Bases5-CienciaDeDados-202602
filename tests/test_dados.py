"""Nenhum byte vem da rede em tempo de render — os dados são commitados."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"

ESPERADOS = [
    "estados.csv",
    "alugueis.csv",
    "cidades.csv",
    "Advertising.csv",
    "Income1.csv",
    "Income2.csv",
    "Credit.csv",
    "Auto.csv",
    "College.csv",
    "Default.csv",
    "Hitters.csv",
    "Heart.csv",
    "mnist_treino.csv.gz",
    "mnist_teste.csv.gz",
    "USArrests.csv",
    "NCI60.csv.gz",
    "Khan.csv.gz",
]

COLUNAS_ESPERADAS = {
    "estados.csv": ["estado", "populacao", "taxa_homicidios", "sigla"],
    "cidades.csv": ["cidade", "sigla", "regiao"],
    "Advertising.csv": ["tv", "radio", "jornal", "vendas"],
    "Income1.csv": ["escolaridade", "renda"],
    "Income2.csv": ["escolaridade", "senioridade", "renda"],
    "Credit.csv": [
        "renda", "limite", "pontuacao", "cartoes", "idade", "escolaridade",
        "imovel_proprio", "estudante", "casado", "regiao", "saldo",
    ],
    "Auto.csv": [
        "milhas_por_galao", "cilindros", "cilindrada", "potencia", "peso",
        "aceleracao", "ano", "origem", "nome",
    ],
    "College.csv": [
        "Unnamed: 0", "privada", "inscricoes", "aceitos", "matriculados",
        "perc_top10", "perc_top25", "graduacao_integral", "graduacao_parcial",
        "mensalidade_fora_do_estado", "moradia_e_alimentacao", "custo_livros",
        "gastos_pessoais", "perc_doutores", "perc_titulacao_maxima",
        "razao_aluno_professor", "perc_ex_alunos_doadores", "gasto_por_aluno",
        "taxa_conclusao",
    ],
    "Default.csv": ["inadimplente", "estudante", "saldo", "renda"],
    "Hitters.csv": [
        "vezes_ao_bastao", "rebatidas", "home_runs", "corridas",
        "impulsionadas", "bases_por_bolas", "anos", "vezes_ao_bastao_carreira",
        "rebatidas_carreira", "home_runs_carreira", "corridas_carreira",
        "impulsionadas_carreira", "bases_por_bolas_carreira", "liga", "divisao",
        "eliminacoes", "assistencias", "erros", "salario", "liga_seguinte",
    ],
    "Heart.csv": [
        "idade", "sexo", "dor_no_peito", "pressao_repouso", "colesterol",
        "glicemia_alta", "ecg_repouso", "freq_cardiaca_max", "angina_exercicio",
        "depressao_st", "inclinacao_st", "vasos_coloridos", "talio",
        "doenca_cardiaca",
    ],    "USArrests.csv": ["estado", "homicidio", "agressao", "pop_urbana", "estupro"],
}


def test_conjuntos_presentes():
    for nome in ESPERADOS:
        assert (DADOS / nome).is_file(), f"falta dados/{nome}"


def test_dados_README_documenta_cada_conjunto():
    texto = (DADOS / "README.md").read_text()
    for nome in ESPERADOS:
        assert nome in texto, f"dados/README.md não menciona {nome}"


def test_alugueis_preserva_a_armadilha_do_andar():
    """A seção 6.3 ensina sobre esta linha exata; se ela sumir, a seção mente.

    Alguém "consertando" o CSV — trocando os "-" por vazio, por exemplo — faria
    o pandas ler `andar` como número e a seção passaria a explicar um problema
    que o arquivo já não tem.
    """
    import csv
    with (RAIZ / "dados" / "alugueis.csv").open(encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert len(linhas) == 10692
    assert sum(1 for l in linhas if l["andar"] == "-") == 2461


def test_auto_preserva_a_armadilha_da_potencia():
    """A seção 8.5 ensina sobre estas cinco linhas exatas; se elas sumirem, a
    seção mente.

    Alguém "consertando" o CSV — preenchendo os `?` com a mediana, por
    exemplo — faria `potencia` chegar como número direto do `read_csv` e a
    seção passaria a explicar uma conversão de tipo que o arquivo já não
    precisa. O ISLP trabalha com as 392 linhas que sobram depois de
    descartar essas cinco.
    """
    import csv
    with (RAIZ / "dados" / "Auto.csv").open(encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert len(linhas) == 397
    assert sum(1 for l in linhas if l["potencia"] == "?") == 5


def test_hitters_preserva_os_salarios_ausentes():
    """A seção 12.1 descarta estas 59 linhas à vista; se elas sumirem, a
    seção mente.

    Alguém "consertando" o CSV — apagando os jogadores sem salário, ou
    preenchendo o salário com a mediana — faria o `dropna()` da seção não
    ter o que descartar, e as contas de 322 para 263 jogadores deixariam de
    bater. O ISLP trabalha com as 263 linhas que sobram.
    """
    import csv
    with (DADOS / "Hitters.csv").open(encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert len(linhas) == 322
    assert sum(1 for l in linhas if l["salario"] == "") == 59


def test_heart_preserva_os_vazios():
    """A seção 12.3 descarta estas seis linhas à vista; se elas sumirem, a
    seção mente.

    São 4 vazios em `vasos_coloridos` e 2 em `talio`, em seis pacientes
    diferentes. Alguém "consertando" o CSV — preenchendo os vazios ou
    apagando as linhas — faria o `dropna()` da seção não ter o que
    descartar. O ISLP trabalha com os 297 pacientes que sobram.
    """
    import csv
    with (DADOS / "Heart.csv").open(encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert len(linhas) == 303
    assert sum(1 for l in linhas if "" in l.values()) == 6


def test_college_preserva_a_coluna_de_indice_do_R():
    """A primeira coluna do College é o ASSUNTO de um exercício, não sujeira.

    Nos demais conjuntos do ISLP a coluna de índice do R foi removida na
    tradução. Aqui ela fica: o exercício 3 da lista computacional 1 (o 2.8 do
    livro) leva o aluno a descobrir que a primeira coluna é o nome da
    universidade e a reler o arquivo com `index_col=0`. Sem a coluna, o item
    perde o objeto.
    """
    import csv
    with (DADOS / "College.csv").open(encoding="utf-8") as f:
        cabecalho = next(csv.reader(f))
    assert cabecalho[0] == "Unnamed: 0", (
        "a coluna de índice do College sumiu; o exercício 3 da lista 1 depende dela"
    )


def test_colunas_estao_em_portugues():
    """Do capítulo 6 em diante, o dado que o aluno vê está em português.

    Minúsculas, snake_case, sem acento no nome da coluna; o valor de categoria
    mantém a grafia correta. O nome do ARQUIVO não muda — é a ponte com o site
    do ISLP, e `dados/README.md` guarda a tabela de-para.
    """
    import csv
    for nome, esperadas in COLUNAS_ESPERADAS.items():
        with (DADOS / nome).open(encoding="utf-8") as f:
            cabecalho = next(csv.reader(f))
        assert cabecalho == esperadas, f"{nome}: cabeçalho {cabecalho}"


def test_mnist_amostra_fixa():
    """As seções 14.2 e 14.3 contam erros em 2.000 imagens de teste; se a
    amostra mudar, os números da prosa deixam de bater.

    São as PRIMEIRAS 6.000 imagens do treino e as primeiras 2.000 do teste,
    sem sorteio. Um arquivo regravado com outro recorte, com pixels
    normalizados para [0, 1] ou sem a coluna `digito` na frente passaria
    em `test_conjuntos_presentes` e quebraria o capítulo em silêncio. Os
    `.gz` ficam fora de `COLUNAS_ESPERADAS`, que abre o arquivo como texto.
    """
    import pandas as pd

    for nome, linhas in [("mnist_treino.csv.gz", 6000), ("mnist_teste.csv.gz", 2000)]:
        df = pd.read_csv(DADOS / nome)
        assert df.shape == (linhas, 785), f"{nome}: shape {df.shape}"
        assert list(df.columns) == ["digito"] + [f"pixel_{k:03d}" for k in range(784)]
        assert df["digito"].between(0, 9).all()
        pixels = df.drop(columns="digito")
        assert all(pd.api.types.is_integer_dtype(t) for t in pixels.dtypes)
        assert pixels.min().min() >= 0 and pixels.max().max() <= 255

    treino = pd.read_csv(DADOS / "mnist_treino.csv.gz")
    contagem = treino["digito"].value_counts().sort_index().tolist()
    assert contagem == [592, 671, 581, 608, 623, 514, 608, 651, 551, 601]


def test_usarrests_preserva_maryland():
    """Maryland tem `pop_urbana` 67, e é esse o dado do ISLP.

    A documentação do R registra o 67 como erro de transcrição (seria 76).
    Alguém "consertando" a linha faria as cargas, os escores e as figuras do
    capítulo 15 deixarem de bater com as do livro-texto, sem erro nenhum na
    tela. Ver dados/README.md.
    """
    import csv
    with (DADOS / "USArrests.csv").open(encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert len(linhas) == 50
    maryland = [l for l in linhas if l["estado"] == "Maryland"]
    assert len(maryland) == 1
    assert maryland[0]["pop_urbana"] == "67"


def test_nci60_formato():
    """O capítulo 15 conta linhagens por tipo em `crosstab`; se o arquivo for
    regravado com outro recorte, outra ordem de colunas ou outra tradução
    das categorias, os números da prosa deixam de bater.

    O `.gz` fica fora de `COLUNAS_ESPERADAS`, que abre o arquivo como texto,
    como o MNIST.
    """
    import pandas as pd

    nci = pd.read_csv(DADOS / "NCI60.csv.gz")
    assert nci.shape == (64, 6831), f"shape {nci.shape}"
    assert list(nci.columns) == ["tipo"] + [f"gene_{k:04d}" for k in range(6830)]
    contagem = nci["tipo"].value_counts().to_dict()
    assert contagem == {
        "pulmão": 9, "rim": 9, "melanoma": 8, "mama": 7, "cólon": 7,
        "leucemia": 6, "ovário": 6, "SNC": 5, "próstata": 2,
        "desconhecido": 1, "K562A-repro": 1, "K562B-repro": 1,
        "MCF7A-repro": 1, "MCF7D-repro": 1,
    }, contagem
    assert len(contagem) == 14


def test_khan_formato():
    """O capítulo 16 separa treino e teste pela coluna `conjunto` e nomeia os
    tumores; se o arquivo for regravado com outra divisão, outra ordem de
    colunas ou outra correspondência entre o código 1–4 e o tumor, os números
    da prosa deixam de bater. A correspondência foi deduzida pelas contagens
    de Khan et al. (2001) — ver dados/README.md —, e é isso que as contagens
    abaixo travam.

    O `.gz` fica fora de `COLUNAS_ESPERADAS`, que abre o arquivo como texto,
    como o MNIST e o NCI60.
    """
    import pandas as pd

    khan = pd.read_csv(DADOS / "Khan.csv.gz")
    assert khan.shape == (83, 2310), f"shape {khan.shape}"
    assert list(khan.columns) == (
        ["conjunto", "tumor"] + [f"gene_{k:04d}" for k in range(2308)]
    )
    assert khan["conjunto"].tolist() == ["treino"] * 63 + ["teste"] * 20
    treino = khan.loc[khan["conjunto"] == "treino", "tumor"].value_counts().to_dict()
    teste = khan.loc[khan["conjunto"] == "teste", "tumor"].value_counts().to_dict()
    assert treino == {
        "sarcoma de Ewing": 23, "rabdomiossarcoma": 20,
        "neuroblastoma": 12, "linfoma de Burkitt": 8,
    }, treino
    assert teste == {
        "sarcoma de Ewing": 6, "neuroblastoma": 6,
        "rabdomiossarcoma": 5, "linfoma de Burkitt": 3,
    }, teste
    assert not khan.isna().any().any()
