"""Nenhum byte vem da rede em tempo de render — os dados são commitados."""
import csv
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"

ESPERADOS = [
    "stocks.csv",
    "comma_delimited_stock_prices.csv",
    "getting-data.html",
    "iris.data",
    "spam-assuntos.csv",
    "imagem-cores.jpg",
    "estados.csv",
    "alugueis.csv",
    "cidades.csv",
    "Advertising.csv",
    "Income1.csv",
    "Income2.csv",
]


def test_conjuntos_presentes():
    for nome in ESPERADOS:
        assert (DADOS / nome).is_file(), f"falta dados/{nome}"


def test_mnist_presente():
    arquivos = list((DADOS / "mnist").glob("*.gz"))
    assert len(arquivos) == 4, f"esperava 4 arquivos MNIST, achei {len(arquivos)}"


def test_iris_tem_150_linhas_e_4_medidas():
    linhas = [l for l in (DADOS / "iris.data").read_text().splitlines() if l.strip()]
    assert len(linhas) == 150
    primeira = linhas[0].split(",")
    assert len(primeira) == 5           # 4 medidas + a classe
    assert primeira[-1].startswith("Iris-")


def test_spam_tem_assunto_e_rotulo():
    with (DADOS / "spam-assuntos.csv").open(encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        assert leitor.fieldnames == ["assunto", "is_spam"]
        linhas = list(leitor)
    assert len(linhas) > 1000
    assert {l["is_spam"] for l in linhas} == {"True", "False"}


def test_dados_README_documenta_cada_conjunto():
    texto = (DADOS / "README.md").read_text()
    for nome in ESPERADOS + ["mnist"]:
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
