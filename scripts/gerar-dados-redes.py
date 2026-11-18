"""Escreve os dados das páginas de apoio do capítulo 14 dentro delas.

As três páginas, `apoio/do-pixel-ao-digito.html` (seção 14.2),
`apoio/retropropagacao.html` e `apoio/lotes-penalidade-e-dropout.html`
(seção 14.3), são arquivos únicos que abrem com dois cliques e rodam sem
rede. Os dados vão embutidos numa tag
`<script type="application/json" id="dados">`, e é este script que a preenche.

As imagens são as do MNIST de `dados/`, um byte por pixel, em base64. A rede
das páginas é menor que a das seções (duas camadas escondidas de 16
unidades, não 256 e 128), para caber num desenho e treinar no navegador:

- a primeira página recebe uma rede já ajustada pelo `MLPClassifier`
  (`alpha=1`) às 6.000 imagens de treino, com os pesos arredondados a quatro casas, e 200
  imagens de teste;
- a segunda recebe 30 imagens de treino, três de cada dígito;
- a terceira recebe 600 imagens de ajuste e 400 de validação, tiradas da
  divisão da seção 14.3 (`test_size=0.2`, `random_state=14`, estratificada).

Os pesos da primeira dependem da máquina nas últimas casas; nenhuma seção
cita essa rede, e os testes conferem a conta da página com os pesos que
estiverem embutidos. Pode rodar no host:

    .venv/bin/python scripts/gerar-dados-redes.py
"""

import base64
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

RAIZ = Path(__file__).resolve().parent.parent
IDA = RAIZ / "apoio/do-pixel-ao-digito.html"
VOLTA = RAIZ / "apoio/retropropagacao.html"
AJUSTE = RAIZ / "apoio/lotes-penalidade-e-dropout.html"
ESCONDIDAS = (16, 16)
TAG = re.compile(r'(<script type="application/json" id="dados">)(.*?)(</script>)', re.S)


def ler(nome: str) -> tuple[np.ndarray, np.ndarray]:
    """Os pixels (inteiros de 0 a 255) e os dígitos de uma das tabelas do MNIST."""
    tabela = pd.read_csv(RAIZ / "dados" / nome)
    pixels = tabela.drop(columns="digito").to_numpy(dtype=np.uint8)
    return pixels, tabela["digito"].to_numpy()


def em_base64(pixels: np.ndarray) -> str:
    return base64.b64encode(pixels.astype(np.uint8).tobytes()).decode("ascii")


def previsoes(pesos: list, vieses: list, X: np.ndarray) -> np.ndarray:
    """O dígito previsto pela rede de pesos dados, na conta da seção 14.2."""
    ativacao = X
    for camada, (W, v) in enumerate(zip(pesos, vieses)):
        ativacao = ativacao @ W + v
        if camada < len(pesos) - 1:
            ativacao = np.maximum(0, ativacao)
    return ativacao.argmax(axis=1)


def dados_ida() -> dict:
    """A rede ajustada, 200 imagens de teste e os erros dela nas 2.000."""
    treino_pixels, treino_y = ler("mnist_treino.csv.gz")
    teste_pixels, teste_y = ler("mnist_teste.csv.gz")
    # A penalidade alpha=1 segura os pesos: sem ela, a rede dá probabilidade 1,00
    # a quase toda imagem, e a softmax da página não teria o que mostrar.
    rede = MLPClassifier(
        hidden_layer_sizes=ESCONDIDAS, alpha=1, random_state=14, max_iter=400
    )
    rede.fit(treino_pixels / 255, treino_y)
    pesos = [np.round(W, 4) for W in rede.coefs_]
    vieses = [np.round(v, 4) for v in rede.intercepts_]
    erros = int((previsoes(pesos, vieses, teste_pixels / 255) != teste_y).sum())
    return {
        "imagens": em_base64(teste_pixels[:200]),
        "digitos": [int(d) for d in teste_y[:200]],
        "rede": {
            "tamanhos": [784, *ESCONDIDAS, 10],
            "W": [[float(w) for w in W.ravel()] for W in pesos],
            "v": [[float(b) for b in v] for v in vieses],
        },
        "n_treino": int(len(treino_y)),
        "n_teste": int(len(teste_y)),
        "erros_teste": erros,
    }


def dados_volta() -> dict:
    """Trinta imagens de treino: as três primeiras de cada dígito."""
    pixels, y = ler("mnist_treino.csv.gz")
    linhas = []
    for vez in range(3):
        for digito in range(10):
            linhas.append(int(np.flatnonzero(y == digito)[vez]))
    return {
        "imagens": em_base64(pixels[linhas]),
        "digitos": [int(y[i]) for i in linhas],
    }


def dados_ajuste() -> dict:
    """As 600 primeiras imagens de ajuste e as 400 primeiras de validação da 14.3."""
    pixels, y = ler("mnist_treino.csv.gz")
    posicoes = np.arange(len(y))
    ajuste, validacao = train_test_split(
        posicoes, test_size=0.2, random_state=14, stratify=y
    )
    ajuste, validacao = ajuste[:600], validacao[:400]
    return {
        "ajuste": em_base64(pixels[ajuste]),
        "digitos_ajuste": [int(d) for d in y[ajuste]],
        "validacao": em_base64(pixels[validacao]),
        "digitos_validacao": [int(d) for d in y[validacao]],
        "tamanhos": [784, *ESCONDIDAS, 10],
    }


def embutir(pagina: Path, conteudo: dict) -> None:
    """Troca o conteúdo da tag `id="dados"` da página pelo JSON de `conteudo`."""
    html = pagina.read_text(encoding="utf-8")
    if not TAG.search(html):
        raise ValueError(f"{pagina.name} não tem a tag de dados")
    texto = json.dumps(conteudo, ensure_ascii=False, separators=(",", ":"))
    html = TAG.sub(lambda m: m.group(1) + texto + m.group(3), html, count=1)
    pagina.write_text(html, encoding="utf-8")


def main():
    embutir(IDA, dados_ida())
    embutir(VOLTA, dados_volta())
    embutir(AJUSTE, dados_ajuste())


if __name__ == "__main__":
    main()
