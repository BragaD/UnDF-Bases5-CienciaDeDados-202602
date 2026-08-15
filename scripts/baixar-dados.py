#!/usr/bin/env python3
"""Coleta única dos dados externos do livro. Os resultados são COMMITADOS.

Rodar com:
    docker compose run --rm --no-deps livro python scripts/baixar-dados.py

Isto não é um chunk do livro. Um livro que faz chamadas de rede a cada render
é frágil: a página raspada muda de layout, a API sai do ar, e o material
quebra sem ninguém ter tocado no repositório.
"""
import csv
import gzip
import io
import shutil
import tarfile
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


# 1-2. CSVs de ações, do próprio repositório do Grus
BASE_GRUS = "https://raw.githubusercontent.com/joelgrus/data-science-from-scratch/master/"
baixar(BASE_GRUS + "stocks.csv", DADOS / "stocks.csv")
baixar(BASE_GRUS + "comma_delimited_stock_prices.csv",
       DADOS / "comma_delimited_stock_prices.csv")

# 3. HTML de exemplo do capítulo 6 (Grus 9)
baixar("https://raw.githubusercontent.com/joelgrus/data/master/getting-data.html",
       DADOS / "getting-data.html")

# 4. Iris, do capítulo 9 (Grus 12)
baixar("https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data",
       DADOS / "iris.data")

# 5. MNIST, do capítulo 16 (Grus 19)
MNIST = "https://ossci-datasets.s3.amazonaws.com/mnist/"
for nome in ["train-images-idx3-ubyte.gz", "train-labels-idx1-ubyte.gz",
             "t10k-images-idx3-ubyte.gz", "t10k-labels-idx1-ubyte.gz"]:
    baixar(MNIST + nome, DADOS / "mnist" / nome)

# 6. SpamAssassin — extraímos SÓ os assuntos.
#
# O naive_bayes.py do Grus lê cada arquivo de e-mail e descarta tudo menos a
# linha "Subject:". Baixar centenas de MB de corpus para usar uma linha por
# arquivo não se justifica num repositório de livro. O código de varredura dos
# diretórios continua no capítulo 10, com eval: false — ele É parte da lição,
# só não precisa rodar a cada render.
SPAM_BASE = "https://spamassassin.apache.org/old/publiccorpus/"
TARBALLS = [
    ("20021010_easy_ham.tar.bz2", False),
    ("20021010_hard_ham.tar.bz2", False),
    ("20021010_spam.tar.bz2", True),
]

saida = DADOS / "spam-assuntos.csv"
if saida.exists():
    print(f"skip  {saida.relative_to(RAIZ)} (já existe)")
else:
    linhas = []
    for nome, is_spam in TARBALLS:
        print(f"lê    {nome}")
        with urllib.request.urlopen(SPAM_BASE + nome) as r:
            bruto = io.BytesIO(r.read())
        with tarfile.open(fileobj=bruto, mode="r:bz2") as tar:
            for membro in tar.getmembers():
                if not membro.isfile():
                    continue
                f = tar.extractfile(membro)
                if f is None:
                    continue
                for linha in io.TextIOWrapper(f, errors="ignore"):
                    if linha.startswith("Subject:"):
                        linhas.append({
                            "assunto": linha[len("Subject:"):].strip(),
                            "is_spam": is_spam,
                        })
                        break
    with saida.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["assunto", "is_spam"])
        escritor.writeheader()
        escritor.writerows(linhas)
    print(f"ok    {saida.relative_to(RAIZ)} ({len(linhas)} assuntos)")

print("---")
print("Revise os arquivos e commite-os. Este script não roda no render.")
