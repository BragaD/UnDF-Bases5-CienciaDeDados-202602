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
]

COLUNAS_ESPERADAS = {
    "estados.csv": ["estado", "populacao", "taxa_homicidios", "sigla"],
    "cidades.csv": ["cidade", "sigla", "regiao"],
    "Advertising.csv": ["tv", "radio", "jornal", "vendas"],
    "Income1.csv": ["escolaridade", "renda"],
    "Income2.csv": ["escolaridade", "senioridade", "renda"],
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
