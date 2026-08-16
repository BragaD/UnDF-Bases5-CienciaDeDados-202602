"""Pega o `_freeze` envenenado — a falha mais silenciosa deste projeto.

O `freeze: auto` do Quarto guarda, para cada `.qmd`, o par
*(hash MD5 do fonte, markdown executado)*. Se alguém **edita o arquivo enquanto
o render roda**, o Quarto executa a versão velha e grava esse resultado velho
junto com o hash da versão **nova**. Dali em diante o hash bate, o cache é
considerado válido, e aquele arquivo **nunca mais reexecuta sozinho**: o livro
publica conteúdo antigo para sempre, sem uma linha de erro na tela.

Isso não é hipótese. Já publicou três seções do capítulo 10 e uma do 7
desatualizadas, e só foi encontrado porque um revisor comparou fonte e HTML
linha a linha.

**Comparar hashes não detecta nada** — o hash bate; é justamente esse o
problema. O que denuncia é a combinação:

    hash guardado == hash do fonte   E   a prosa do fonte não está no markdown

O `scripts/render-seguro.sh` **previne** o envenenamento dali em diante,
detectando quem foi editado durante o render. Este teste é a rede embaixo: pega
o que já está envenenado, inclusive o que foi envenenado antes de o script
existir, ou por um render feito fora dele.

Remédio quando falhar: `make refresh CAP=NN` para cada capítulo acusado.
**Nunca `make clean`** — ele esfria o `_freeze` inteiro e aumenta a chance da
corrida do bind mount.
"""
import hashlib
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONTENT = RAIZ / "content"
FREEZE = RAIZ / "_freeze"

# Um arquivo precisa de pelo menos DUAS linhas de prosa ausentes para ser
# acusado. Uma linha só pode ser transformação legítima do Quarto em alguma
# marcação incomum; duas ou mais é conteúdo de outra versão. Na medição que
# motivou este teste, 40 dos 45 arquivos tinham exatamente ZERO ausentes, e os
# envenenados tinham de 2 a 11 — não há zona cinzenta na prática.
MINIMO_PARA_ACUSAR = 2

# Só linhas longas o bastante para serem inconfundíveis, e sem marcação que o
# Quarto reescreve (atributos de chunk, cercas de div, tabelas, HTML, display math).
TAMANHO_MINIMO = 60
PREFIXOS_IGNORADOS = ("#|", ":::", "|", "<", "$$")


def linhas_de_prosa(texto: str) -> list[str]:
    """Linhas de prosa distintivas, fora de blocos de código."""
    linhas, dentro_de_codigo = [], False
    for linha in texto.split("\n"):
        if linha.startswith("```"):
            dentro_de_codigo = not dentro_de_codigo
            continue
        if dentro_de_codigo:
            continue
        despida = linha.strip()
        if len(despida) >= TAMANHO_MINIMO and not despida.startswith(PREFIXOS_IGNORADOS):
            linhas.append(despida)
    return linhas


def test_freeze_corresponde_ao_fonte():
    """Todo `_freeze` cujo hash bate com o fonte precisa conter a prosa do fonte.

    Arquivos cujo hash NÃO bate são ignorados de propósito: eles foram editados
    depois do último render, o Quarto vai reexecutá-los na próxima rodada, e
    isso é o funcionamento normal do cache — não um defeito.
    """
    if not FREEZE.is_dir():
        return  # checkout limpo (o CI começa assim): não há o que conferir

    envenenados = []
    for qmd in sorted(CONTENT.rglob("*.qmd")):
        resultado = FREEZE / qmd.relative_to(RAIZ).with_suffix("") / "execute-results" / "html.json"
        if not resultado.is_file():
            continue

        try:
            dados = json.loads(resultado.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            # O arquivo está sendo ESCRITO agora, por um render em andamento.
            # Um JSON pela metade não é evidência de envenenamento — é evidência
            # de que alguém está trabalhando. Já derrubou uma rodada de `make
            # teste` sem nenhum defeito real por trás.
            continue

        fonte = qmd.read_text(encoding="utf-8")

        # Hash diferente => o Quarto vai reexecutar sozinho. Nada a checar.
        if dados.get("hash") != hashlib.md5(fonte.encode("utf-8")).hexdigest():
            continue

        markdown = dados.get("result", {}).get("markdown", "")
        ausentes = [l for l in linhas_de_prosa(fonte) if l not in markdown]
        if len(ausentes) >= MINIMO_PARA_ACUSAR:
            capitulo = qmd.parent.name.replace("cap", "").lstrip("0")
            envenenados.append(
                f"{qmd.relative_to(RAIZ)} ({len(ausentes)} linhas de prosa fora do "
                f"cache; conserte com 'make refresh CAP={capitulo}')"
            )

    assert not envenenados, (
        "_freeze envenenado — o hash bate com o fonte mas o conteúdo guardado é de "
        "outra versão, então estes arquivos NUNCA reexecutariam sozinhos e o livro "
        "publicaria texto velho em silêncio:\n  " + "\n  ".join(envenenados)
    )
