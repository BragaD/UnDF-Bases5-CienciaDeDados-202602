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
# `Heart` entra com o capítulo 12 (ISLP 8.1.2): é o exemplo da árvore de
# classificação. Não está no wheel do pacote (conferido), só no site.
BASE_ISLP = "https://www.statlearning.com/s/"
for nome in ["Advertising", "Income1", "Income2", "Credit", "Auto", "College", "Heart"]:
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


# `Hitters` entra com o capítulo 12 (ISLP 8.1.1): é o exemplo da árvore de
# regressão e da poda. O site do livro devolve 404 para ele.
extrair_do_pacote(["Default", "Hitters"])


# `mnist_treino.csv.gz` e `mnist_teste.csv.gz` entram com o capítulo 14 (ISLP
# 10.2 e lab 10.9.2). São uma AMOSTRA FIXA do MNIST (LeCun, Cortes e Burges):
# as primeiras 6.000 imagens do treino e as primeiras 2.000 do teste, sem
# sorteio. O conjunto inteiro (60.000) custaria segundos demais por seção a
# cada render. Os arquivos idx originais são baixados em memória e nunca
# gravados; o que se grava é um CSV com `digito` e `pixel_000`…`pixel_783`
# (pixel 28*i + j, linha a linha), valores 0–255, comprimido com gzip e
# `mtime=0` para sair com os mesmos bytes a cada execução.
BASE_MNIST = "https://ossci-datasets.s3.amazonaws.com/mnist/"
MNIST = [
    ("mnist_treino.csv.gz", "train-images-idx3-ubyte.gz", "train-labels-idx1-ubyte.gz", 6000),
    ("mnist_teste.csv.gz", "t10k-images-idx3-ubyte.gz", "t10k-labels-idx1-ubyte.gz", 2000),
]


def amostra_mnist(destino: Path, imagens: str, rotulos: str, n: int) -> None:
    import gzip

    import numpy as np
    import pandas as pd

    if destino.exists():
        print(f"skip  {destino.relative_to(RAIZ)} (já existe)")
        return

    def ler(arquivo: str, offset: int) -> "np.ndarray":
        print(f"baixa {BASE_MNIST + arquivo} (em memória)")
        with urllib.request.urlopen(BASE_MNIST + arquivo) as r:
            return np.frombuffer(gzip.decompress(r.read()), np.uint8, offset=offset)

    x = ler(imagens, 16).reshape(-1, 784)[:n]
    y = ler(rotulos, 8)[:n]
    df = pd.DataFrame(x, columns=[f"pixel_{k:03d}" for k in range(784)])
    df.insert(0, "digito", y)
    df.to_csv(destino, index=False, compression={"method": "gzip", "mtime": 0})
    print(f"grava {destino.relative_to(RAIZ)} ({n} imagens)")


for destino, imagens, rotulos, n in MNIST:
    amostra_mnist(DADOS / destino, imagens, rotulos, n)


# `USArrests.csv` entra com o capítulo 15 (ISLP 12.2, PCA). Não está no site
# do livro nem no wheel (conferido): o ISLP o carrega do pacote `datasets` do
# R, e aqui ele vem do espelho Rdatasets. O original é lido EM MEMÓRIA e o que
# se grava é a versão já traduzida (colunas e nomes dos estados, ver a tabela
# em dados/README.md). A ordem das linhas é a do original, alfabética em
# inglês, e nenhum valor muda — inclusive Maryland com `pop_urbana` 67, que a
# documentação do R registra como erro de transcrição (seria 76): é o dado do
# ISLP e fica como está.
URL_USARRESTS = (
    "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/"
    "master/csv/datasets/USArrests.csv"
)
COLUNAS_USARRESTS = {
    "rownames": "estado",
    "Murder": "homicidio",
    "Assault": "agressao",
    "UrbanPop": "pop_urbana",
    "Rape": "estupro",
}
ESTADOS_PT = {
    "Alaska": "Alasca",
    "California": "Califórnia",
    "Florida": "Flórida",
    "Georgia": "Geórgia",
    "Hawaii": "Havaí",
    "Louisiana": "Luisiana",
    "Mississippi": "Mississípi",
    "New Hampshire": "Nova Hampshire",
    "New Jersey": "Nova Jersey",
    "New Mexico": "Novo México",
    "New York": "Nova York",
    "North Carolina": "Carolina do Norte",
    "North Dakota": "Dakota do Norte",
    "Pennsylvania": "Pensilvânia",
    "South Carolina": "Carolina do Sul",
    "South Dakota": "Dakota do Sul",
    "Virginia": "Virgínia",
    "West Virginia": "Virgínia Ocidental",
}


def traduzir_usarrests(destino: Path) -> None:
    import io

    import pandas as pd

    if destino.exists():
        print(f"skip  {destino.relative_to(RAIZ)} (já existe)")
        return
    print(f"baixa {URL_USARRESTS} (em memória)")
    with urllib.request.urlopen(URL_USARRESTS) as r:
        df = pd.read_csv(io.BytesIO(r.read()), dtype={"UrbanPop": "int64"})
    assert list(df.columns) == list(COLUNAS_USARRESTS), list(df.columns)
    assert set(ESTADOS_PT) <= set(df["rownames"]), "estado da tradução ausente"
    df = df.rename(columns=COLUNAS_USARRESTS)
    df["estado"] = df["estado"].replace(ESTADOS_PT)
    df.to_csv(destino, index=False)
    print(f"grava {destino.relative_to(RAIZ)} ({len(df)} estados)")


traduzir_usarrests(DADOS / "USArrests.csv")


# `NCI60.csv.gz` entra com o capítulo 15 (ISLP 12.2.4, 12.4 e lab 12.5.4):
# 64 linhagens de células de câncer × 6.830 genes. Vem do mesmo wheel do ISLP
# 0.4.1, lido em memória: `NCI60data.npy` (a matriz) e `NCI60labs.csv` (o tipo
# de câncer), juntados num arquivo só, com `tipo` na frente e
# `gene_0000`…`gene_6829`. Gravado com gzip e `mtime=0`, para sair com os
# mesmos bytes a cada execução. As réplicas `K562A-repro`, `K562B-repro`,
# `MCF7A-repro` e `MCF7D-repro` são nomes de linhagem e ficam sem tradução.
TIPOS_NCI60 = {
    "BREAST": "mama",
    "CNS": "SNC",
    "COLON": "cólon",
    "LEUKEMIA": "leucemia",
    "MELANOMA": "melanoma",
    "NSCLC": "pulmão",
    "OVARIAN": "ovário",
    "PROSTATE": "próstata",
    "RENAL": "rim",
    "UNKNOWN": "desconhecido",
}


def nci60_do_pacote(destino: Path) -> None:
    import io
    import zipfile

    import numpy as np
    import pandas as pd

    if destino.exists():
        print(f"skip  {destino.relative_to(RAIZ)} (já existe)")
        return
    print(f"baixa o wheel do ISLP {VERSAO_ISLP} para extrair o NCI60 (em memória)")
    with urllib.request.urlopen(WHEEL_ISLP) as r:
        wheel = zipfile.ZipFile(io.BytesIO(r.read()))
    matriz = np.load(io.BytesIO(wheel.read("ISLP/data/NCI60data.npy")))
    rotulos = pd.read_csv(io.BytesIO(wheel.read("ISLP/data/NCI60labs.csv")))
    assert matriz.shape == (64, 6830), matriz.shape
    assert len(rotulos) == 64, len(rotulos)
    tipo = rotulos["label"].str.strip().replace(TIPOS_NCI60)
    df = pd.DataFrame(matriz, columns=[f"gene_{k:04d}" for k in range(6830)])
    df.insert(0, "tipo", tipo.to_numpy())
    df.to_csv(destino, index=False, compression={"method": "gzip", "mtime": 0})
    print(f"grava {destino.relative_to(RAIZ)} ({destino.stat().st_size} bytes)")


nci60_do_pacote(DADOS / "NCI60.csv.gz")


# `Khan.csv.gz` entra com o capítulo 16 (ISLP 9.6.5): 83 amostras de tumores
# de pequenas células redondas e azuis × 2.308 genes. Vem do mesmo wheel do
# ISLP 0.4.1, lido em memória: `Khan_xtrain.csv` (63 × 2.308), `Khan_xtest.csv`
# (20 × 2.308), `Khan_ytrain.csv` e `Khan_ytest.csv` (coluna `x`, de 1 a 4),
# juntados num arquivo só, com `conjunto` ("treino" nas 63 primeiras linhas,
# "teste" nas 20 últimas, a divisão dos autores), `tumor` e
# `gene_0000`…`gene_2307`. Gravado com gzip e `mtime=0`.
#
# A correspondência 1–4 → tumor NÃO está na documentação do pacote. Ela foi
# deduzida pelas contagens no treino, que são distintas (8/23/12/20), contra
# as de Khan et al. (2001), Nature Medicine 7(6):673–679, doi
# 10.1038/89044: 8 BL, 23 EWS, 12 NB e 20 RMS no treino; 3, 6, 6 e 5 no
# teste. É também a ordem alfabética dos fatores do R. Ver dados/README.md.
TUMORES_KHAN = {
    1: "linfoma de Burkitt",
    2: "sarcoma de Ewing",
    3: "neuroblastoma",
    4: "rabdomiossarcoma",
}


def khan_do_pacote(destino: Path) -> None:
    import io
    import zipfile

    import pandas as pd

    if destino.exists():
        print(f"skip  {destino.relative_to(RAIZ)} (já existe)")
        return
    print(f"baixa o wheel do ISLP {VERSAO_ISLP} para extrair o Khan (em memória)")
    with urllib.request.urlopen(WHEEL_ISLP) as r:
        wheel = zipfile.ZipFile(io.BytesIO(r.read()))

    def ler(nome: str) -> "pd.DataFrame":
        return pd.read_csv(io.BytesIO(wheel.read(f"ISLP/data/Khan_{nome}.csv")))

    xtreino, xteste = ler("xtrain"), ler("xtest")
    ytreino, yteste = ler("ytrain"), ler("ytest")
    colunas_v = [f"V{k}" for k in range(1, 2309)]
    assert xtreino.shape == (63, 2308), xtreino.shape
    assert xteste.shape == (20, 2308), xteste.shape
    assert list(xtreino.columns) == colunas_v
    assert list(xteste.columns) == colunas_v
    assert list(ytreino.columns) == ["x"] and len(ytreino) == 63
    assert list(yteste.columns) == ["x"] and len(yteste) == 20
    # A dedução da correspondência depende destas contagens.
    assert ytreino["x"].value_counts().to_dict() == {1: 8, 2: 23, 3: 12, 4: 20}
    assert yteste["x"].value_counts().to_dict() == {1: 3, 2: 6, 3: 6, 4: 5}

    genes = pd.concat([xtreino, xteste], ignore_index=True)
    genes.columns = [f"gene_{k:04d}" for k in range(2308)]
    rotulo = pd.concat([ytreino["x"], yteste["x"]], ignore_index=True)
    df = pd.concat(
        [
            pd.DataFrame({
                "conjunto": ["treino"] * 63 + ["teste"] * 20,
                "tumor": rotulo.map(TUMORES_KHAN),
            }),
            genes,
        ],
        axis=1,
    )
    df.to_csv(destino, index=False, compression={"method": "gzip", "mtime": 0})
    print(f"grava {destino.relative_to(RAIZ)} ({destino.stat().st_size} bytes)")


khan_do_pacote(DADOS / "Khan.csv.gz")

print("---")
print("Revise os arquivos e commite-os. Este script não roda no render.")
