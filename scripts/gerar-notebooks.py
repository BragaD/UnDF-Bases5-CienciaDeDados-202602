#!/usr/bin/env python3
"""Gera um notebook Jupyter por capítulo, a partir dos .qmd do livro.

O livro é a fonte da verdade. Este script não guarda conteúdo próprio: cada
notebook é derivado dos `.qmd` do capítulo, na ordem em que o `_quarto.yml`
os registra. Editou um `.qmd`? Rode `make notebooks` de novo.

Os notebooks saem **sem saídas gravadas**, de propósito: quem executa é o
aluno, ao vivo, na aula. Saída congelada no arquivo faria o diff do git virar
ruído binário e tiraria o sentido de executar.

Três traduções acontecem aqui, porque o Quarto entende construções que o
Jupyter não entende:

- Divs de callout (`::: {.callout-note}`) viram blockquotes com rótulo.
- Links entre `.qmd` viram URLs absolutas do site publicado — um link
  relativo a `../cap05/index.qmd` não resolve de dentro de `notebooks/`.
- Citações `@grus2019` viram o texto da citação, com a bibliografia
  completa numa célula ao final.

Uma diferença de execução que vale conhecer: no livro, **cada `.qmd` roda no
seu próprio kernel**, e nomes não atravessam páginas. No notebook, o capítulo
inteiro roda num kernel só. A ordem de leitura é a mesma, então o efeito
prático é apenas que nomes definidos numa seção continuam vivos na seguinte.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CONTEUDO = RAIZ / "content"
SAIDA = RAIZ / "notebooks"
BIB = RAIZ / "references.bib"
QUARTO_YML = RAIZ / "_quarto.yml"
SITE = "https://bragad.github.io/UnDF-Bases5-CienciaDeDados-202602"

TITULO_LEITURAS = "## Leituras adicionais"

# Rótulo e ícone de cada div do livro. O Jupyter não conhece callouts do
# Quarto; o blockquote com rótulo é o que mais se aproxima sem depender de
# CSS que o notebook não carrega.
ROTULOS = {
    "callout-note": ("📌", "Nota"),
    "callout-tip": ("💡", "Dica"),
    "callout-warning": ("⚠️", "Atenção"),
    "callout-important": ("❗", "Importante"),
    "conceito": ("🔷", "Conceito"),
    "exemplo": ("🟩", "Exemplo"),
}

CERCA = re.compile(r"^(`{3,})(.*)$")
DIV_ABRE = re.compile(r"^::: *\{([^}]*)\}\s*$")
DIV_FECHA = re.compile(r"^::: *$")
TITULO_ATX = re.compile(r"^(#{1,5}) (.*)$")
LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
OPCAO = re.compile(r"^#\|\s*([a-z-]+):\s*(.*)$")

CELULA_PREPARO = '''\
# Põe o diretório de trabalho na raiz do projeto. É o que faz
# `from scratch...` e os caminhos `dados/...` funcionarem daqui —
# no livro isso vem do `execute-dir: project` do Quarto.
import os
import sys

_raiz = os.path.abspath(os.getcwd())
while not os.path.exists(os.path.join(_raiz, "_quarto.yml")):
    _pai = os.path.dirname(_raiz)
    if _pai == _raiz:
        raise RuntimeError("raiz do projeto não encontrada (procurando _quarto.yml)")
    _raiz = _pai
os.chdir(_raiz)
if _raiz not in sys.path:
    sys.path.insert(0, _raiz)

%matplotlib inline
print("diretório de trabalho:", os.getcwd())'''


# --------------------------------------------------------------------------
# bibliografia
# --------------------------------------------------------------------------

def le_bibliografia() -> dict[str, dict[str, str]]:
    """Lê o references.bib para não manter uma segunda cópia das referências."""
    texto = BIB.read_text(encoding="utf-8")
    entradas: dict[str, dict[str, str]] = {}
    for bloco in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", texto, re.S):
        chave, corpo = bloco.group(1).strip(), bloco.group(2)
        campos = {}
        for campo in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}\s*,?\s*\n", corpo, re.S):
            campos[campo.group(1).lower()] = " ".join(campo.group(2).split())
        entradas[chave] = campos
    return entradas


def sobrenomes(autores: str) -> list[str]:
    return [a.split(",")[0].strip() for a in autores.split(" and ")]


def citacao_curta(campos: dict[str, str]) -> str:
    nomes = sobrenomes(campos.get("author", ""))
    ano = campos.get("year", "s.d.")
    if len(nomes) == 1:
        autor = nomes[0]
    elif len(nomes) == 2:
        autor = f"{nomes[0]} e {nomes[1]}"
    else:
        autor = f"{nomes[0]} et al."
    return f"{autor} ({ano})"


def referencia_completa(campos: dict[str, str]) -> str:
    nomes = sobrenomes(campos.get("author", ""))
    partes = [f"**{'; '.join(nomes)}**. *{campos.get('title', '')}*"]
    if campos.get("edition"):
        partes.append(f"{campos['edition']} ed.")
    if campos.get("publisher"):
        partes.append(campos["publisher"])
    if campos.get("year"):
        partes.append(campos["year"])
    linha = ". ".join(partes) + "."
    if campos.get("isbn"):
        linha += f" ISBN {campos['isbn']}."
    return linha


# --------------------------------------------------------------------------
# capítulos
# --------------------------------------------------------------------------

def le_capitulos() -> list[dict]:
    """Extrai a ordem dos capítulos e das seções do `_quarto.yml`.

    A ordem do livro vem do YAML, não do nome do arquivo — então é o YAML que
    manda aqui também, senão os notebooks poderiam divergir do site.
    """
    import yaml

    config = yaml.safe_load(QUARTO_YML.read_text(encoding="utf-8"))
    capitulos = []
    for parte in config["book"]["chapters"]:
        if not isinstance(parte, dict) or "part" not in parte:
            continue
        titulo = parte["part"]
        arquivos = [item["href"] for item in parte["chapters"]]
        numero = int(re.match(r"Capítulo (\d+):", titulo).group(1))
        capitulos.append(
            {
                "numero": numero,
                "titulo": titulo.split(": ", 1)[1],
                "arquivos": arquivos,
            }
        )
    return capitulos


def apelido(titulo: str) -> str:
    tabela = str.maketrans("áàâãéêíóôõúüç", "aaaaeeiooouuc")
    s = titulo.lower().translate(tabela)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


# --------------------------------------------------------------------------
# conversão
# --------------------------------------------------------------------------

def reescreve_links(texto: str, dir_fonte: str) -> str:
    """Troca links entre .qmd por URLs do site publicado."""

    def troca(m: re.Match) -> str:
        rotulo, alvo = m.group(1), m.group(2)
        if alvo.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        if ".qmd" not in alvo:
            return m.group(0)
        caminho, _, ancora = alvo.partition("#")
        destino = os.path.normpath(os.path.join(dir_fonte, caminho))
        destino = destino[: -len(".qmd")] + ".html"
        url = f"{SITE}/{destino}"
        if ancora:
            url += f"#{ancora}"
        return f"[{rotulo}]({url})"

    return LINK.sub(troca, texto)


def reescreve_citacoes(texto: str, curtas: dict[str, str]) -> str:
    for chave, curta in curtas.items():
        autor_ano = curta.rsplit(" (", 1)
        entre_parenteses = f"({autor_ano[0]}, {autor_ano[1].rstrip(')')})"
        texto = texto.replace(f"[@{chave}]", entre_parenteses)
        texto = texto.replace(f"@{chave}", curta)
    return texto


def separa_opcoes(corpo: list[str]) -> tuple[list[str], dict[str, str]]:
    opcoes: dict[str, str] = {}
    i = 0
    while i < len(corpo) and corpo[i].startswith("#|"):
        m = OPCAO.match(corpo[i])
        if m:
            opcoes[m.group(1)] = m.group(2).strip().strip('"')
        i += 1
    return corpo[i:], opcoes


def converte_div(
    classe: str, corpo: list[str], dir_fonte: str, rebaixa: int, curtas: dict[str, str]
) -> list[dict]:
    """Converte um callout do Quarto em células.

    Quase todo callout é só texto, e vira um blockquote com rótulo. Mas 19
    deles, no livro, embrulham um chunk `{python}` que **executa** — e o
    resultado costuma ser usado logo adiante. Esses não podem virar texto:
    o corpo é convertido recursivamente, o que sai como código continua
    célula de código, e só o que é prosa ganha o prefixo de citação.
    """
    nome = classe.split()[0].lstrip(".")
    icone, rotulo = ROTULOS.get(nome, ("", nome))
    linhas = list(corpo)
    while linhas and not linhas[0].strip():
        linhas.pop(0)
    while linhas and not linhas[-1].strip():
        linhas.pop()
    titulo = None
    if linhas and (m := TITULO_ATX.match(linhas[0])):
        titulo = m.group(2)
        linhas.pop(0)
        while linhas and not linhas[0].strip():
            linhas.pop(0)

    cabecalho = f"**{icone} {rotulo}"
    cabecalho += f" — {titulo}**" if titulo else "**"

    saida: list[dict] = []
    pendente = True
    for celula in converte("\n".join(linhas), dir_fonte, rebaixa, curtas):
        if celula["cell_type"] == "markdown":
            citado = "\n".join(
                ("> " + l).rstrip() for l in celula["source"].split("\n")
            )
            if pendente:
                citado = f"> {cabecalho}\n>\n{citado}"
                pendente = False
            saida.append(celula_markdown(citado))
        else:
            if pendente:
                saida.append(celula_markdown(f"> {cabecalho}"))
                pendente = False
            saida.append(celula)
    if pendente:
        saida.append(celula_markdown(f"> {cabecalho}"))
    return saida


def ajusta_titulo(linha: str, rebaixa: int) -> str:
    if not rebaixa:
        return linha
    m = TITULO_ATX.match(linha)
    if not m:
        return linha
    return "#" * (len(m.group(1)) + rebaixa) + " " + m.group(2)


def converte(texto: str, dir_fonte: str, rebaixa: int, curtas: dict[str, str]) -> list[dict]:
    """Transforma o texto de um .qmd numa lista de células."""
    linhas = texto.splitlines()
    celulas: list[dict] = []
    md: list[str] = []

    def descarrega_md() -> None:
        while md and not md[-1].strip():
            md.pop()
        if md:
            bruto = "\n".join(md)
            bruto = reescreve_links(bruto, dir_fonte)
            bruto = reescreve_citacoes(bruto, curtas)
            bruto = re.sub(r"\n{3,}", "\n\n", bruto).strip("\n")
            celulas.append(celula_markdown(bruto))
        md.clear()

    i = 0
    while i < len(linhas):
        linha = linhas[i]

        if m := CERCA.match(linha):
            cerca, info = m.group(1), m.group(2).strip()
            corpo: list[str] = []
            i += 1
            while i < len(linhas) and not linhas[i].startswith(cerca):
                corpo.append(linhas[i])
                i += 1
            i += 1
            if info == "{python}":
                codigo, opcoes = separa_opcoes(corpo)
                if opcoes.get("eval") == "false":
                    # Pseudocódigo do livro: não roda nem no Quarto, então
                    # vira bloco de markdown para não quebrar o notebook.
                    md += ["```python", *codigo, "```", ""]
                else:
                    descarrega_md()
                    prefixo = []
                    if legenda := opcoes.get("fig-cap"):
                        prefixo = [f"# Figura: {legenda}"]
                    while codigo and not codigo[0].strip():
                        codigo.pop(0)
                    celulas.append(celula_codigo("\n".join(prefixo + codigo)))
            else:
                md += [cerca + info, *corpo, cerca, ""]
            continue

        if m := DIV_ABRE.match(linha):
            classe = m.group(1)
            corpo = []
            profundidade = 1
            i += 1
            while i < len(linhas):
                if DIV_ABRE.match(linhas[i]):
                    profundidade += 1
                elif DIV_FECHA.match(linhas[i]):
                    profundidade -= 1
                    if profundidade == 0:
                        i += 1
                        break
                corpo.append(linhas[i])
                i += 1
            sub = converte_div(classe, corpo, dir_fonte, rebaixa, curtas)
            if all(c["cell_type"] == "markdown" for c in sub):
                # Callout só de texto: fica junto da prosa ao redor, sem
                # ganhar célula própria. Reescrever links e citações de novo
                # em `descarrega_md` é inofensivo — as duas trocas são idempotentes.
                for c in sub:
                    md += c["source"].split("\n")
                md.append("")
            else:
                descarrega_md()
                celulas += sub
            continue

        md.append(ajusta_titulo(linha, rebaixa))
        i += 1

    descarrega_md()
    return celulas


# --------------------------------------------------------------------------
# células e notebook
# --------------------------------------------------------------------------

def celula_markdown(texto: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": texto}


def celula_codigo(texto: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": texto,
    }


def monta_notebook(cap: dict, curtas: dict[str, str], entradas: dict) -> dict:
    numero, titulo = cap["numero"], cap["titulo"]
    url = f"{SITE}/content/cap{numero:02d}/index.html"
    celulas = [
        celula_markdown(
            f"# Capítulo {numero}: {titulo}\n\n"
            f"**Bases 5 — Ciência de Dados** · notebook de aula\n\n"
            f"Cada célula de código é a mesma do livro e roda na ordem em que "
            f"aparece — execute de cima para baixo. Versão publicada deste "
            f"capítulo: [{url}]({url})\n\n"
            f"> **Gerado automaticamente a partir dos `.qmd` do livro por "
            f"`scripts/gerar-notebooks.py`.** Edições feitas aqui se perdem no "
            f"próximo `make notebooks`; para mudar o conteúdo, edite o `.qmd`."
        ),
        celula_codigo(CELULA_PREPARO),
    ]

    leituras: list[dict] = []
    for pos, href in enumerate(cap["arquivos"]):
        caminho = RAIZ / href
        dir_fonte = str(pathlib.Path(href).parent)
        texto = caminho.read_text(encoding="utf-8")
        # O index abre o capítulo, então mantém os níveis de título. As
        # seções entram um nível abaixo, para o notebook ter uma hierarquia só.
        if pos == 0:
            corpo, _, resto = texto.partition("\n" + TITULO_LEITURAS + "\n")
            if resto:
                leituras = converte(
                    TITULO_LEITURAS + "\n" + resto, dir_fonte, 0, curtas
                )
            # O H1 do index repete o título do capítulo, que já abre o
            # notebook na célula de cabeçalho.
            texto = re.sub(r"\A#(?!#) .*\n", "", corpo)
            rebaixa = 0
        else:
            rebaixa = 1
        celulas += converte(texto, dir_fonte, rebaixa, curtas)

    celulas += leituras

    usadas = sorted(
        chave
        for chave in entradas
        if any(curtas[chave] in c["source"] for c in celulas if c["cell_type"] == "markdown")
    )
    if usadas:
        linhas = ["## Referências", ""]
        linhas += [f"- {referencia_completa(entradas[c])}" for c in usadas]
        celulas.append(celula_markdown("\n".join(linhas)))

    return {
        "cells": celulas,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
            "title": f"Capítulo {numero}: {titulo}",
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def normaliza(nb: dict) -> dict:
    """Passa `source` de string para lista de linhas terminadas em \\n.

    Uma string única também é válida no formato .ipynb, mas põe a célula
    inteira numa linha de JSON — e aí o diff do git deixa de ser legível.
    """
    for celula in nb["cells"]:
        if isinstance(celula["source"], str):
            linhas = celula["source"].split("\n")
            celula["source"] = [l + "\n" for l in linhas[:-1]] + linhas[-1:]
    return nb


def nome_do_arquivo(cap: dict) -> str:
    return f"cap{cap['numero']:02d}-{apelido(cap['titulo'])}.ipynb"


def serializa(nb: dict) -> str:
    return json.dumps(nb, ensure_ascii=False, indent=1) + "\n"


def main() -> int:
    entradas = le_bibliografia()
    curtas = {chave: citacao_curta(campos) for chave, campos in entradas.items()}
    capitulos = le_capitulos()

    SAIDA.mkdir(exist_ok=True)
    esperados = set()
    for cap in capitulos:
        nb = normaliza(monta_notebook(cap, curtas, entradas))
        nome = nome_do_arquivo(cap)
        esperados.add(nome)
        destino = SAIDA / nome
        destino.write_text(serializa(nb), encoding="utf-8")
        codigo = sum(1 for c in nb["cells"] if c["cell_type"] == "code")
        print(f"{nome:52} {len(nb['cells']):3} células ({codigo} de código)")

    for orfao in sorted(SAIDA.glob("*.ipynb")):
        if orfao.name not in esperados:
            orfao.unlink()
            print(f"removido (capítulo não existe mais): {orfao.name}")

    print(f"\n{len(capitulos)} notebooks em {SAIDA.relative_to(RAIZ)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
