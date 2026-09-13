"""Invariantes do material avaliativo.

A falha que este arquivo existe para impedir é a mais cara do projeto inteiro:
**publicar o gabarito junto com a lista.** O site é público, o repositório é
público, e a diferença entre a versão do aluno e a do professor é uma linha de
metadado. Um deslize aqui não quebra nada — só entrega as respostas.

Por isso a separação é de **diretório**, e não de nome de arquivo:
`atividades/publico/` é o que o `project.resources` do `_quarto.yml` copia para
o site, e nada mais de `atividades/` vai junto. Nome de arquivo é convenção que
alguém erra; diretório é caminho que o Quarto obedece.

Não dá para conferir o conteúdo do PDF: o Typst codifica o texto por glifo, e a
palavra "Resposta" não aparece nem descomprimindo os streams. Então os testes
abaixo travam as três camadas que **são** verificáveis — o que o Quarto publica,
o que o git versiona, e o que existe no diretório servido.
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ATIVIDADES = RAIZ / "atividades"
PUBLICO = ATIVIDADES / "publico"
QUARTO_YML = RAIZ / "_quarto.yml"
GITIGNORE = RAIZ / ".gitignore"

MARCA = "gabarito"


def carregar_gerador_de_lista():
    """Importa scripts/gerar-lista.py (o hífen impede um `import` normal).

    Mesmo padrão de `tests/test_notebooks.py:carregar_gerador`.
    """
    caminho = RAIZ / "scripts" / "gerar-lista.py"
    spec = importlib.util.spec_from_file_location("gerar_lista", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def ignorado(caminho: str) -> bool:
    """True se o git ignoraria esse caminho (o arquivo não precisa existir)."""
    r = subprocess.run(
        ["git", "check-ignore", "-q", caminho],
        cwd=RAIZ, capture_output=True,
    )
    return r.returncode == 0


def test_nenhum_gabarito_no_diretorio_publicado():
    """O teste mais direto: o que está em publico/ vai para a internet."""
    if not PUBLICO.exists():
        return
    ofensores = [p.name for p in PUBLICO.rglob("*") if MARCA in p.name.lower()]
    assert not ofensores, (
        f"arquivo com '{MARCA}' no nome dentro de {PUBLICO.relative_to(RAIZ)}/, "
        f"que é servido no site: {ofensores}"
    )


def test_quarto_publica_apenas_o_diretorio_publico():
    """`resources` é o que decide o que sai no site. Ele não pode alargar."""
    yml = QUARTO_YML.read_text(encoding="utf-8")
    recursos = re.findall(r"^\s+-\s+(atividades\S*)\s*$", yml, re.M)
    assert recursos, "nenhum recurso de atividades declarado no _quarto.yml"
    for r in recursos:
        assert r.startswith("atividades/publico/"), (
            f"o _quarto.yml publica {r!r}, fora de atividades/publico/ — "
            f"isso alcançaria o gabarito"
        )


def test_gitignore_barra_gabarito_em_qualquer_lugar():
    """A regra tem que valer inclusive dentro de publico/, onde há uma exceção.

    No .gitignore a última regra que casa é a que vale, então a regra de
    gabarito precisa vir DEPOIS da exceção que libera publico/. Este teste
    confere o efeito, não a ordem das linhas.
    """
    for caminho in (
        "atividades/lista-99-gabarito.pdf",
        "atividades/publico/lista-99-gabarito.pdf",
        "atividades/publico/gabarito.pdf",
    ):
        assert ignorado(caminho), (
            f"o git versionaria {caminho!r} — a regra de gabarito no "
            f".gitignore foi enfraquecida ou ficou antes da exceção de publico/"
        )


def test_fonte_com_respostas_nao_e_versionada():
    """Todo .qmd de atividade com bloco de gabarito fica fora do repositório."""
    if not ATIVIDADES.exists():
        return
    vazando = []
    for qmd in ATIVIDADES.rglob("*.qmd"):
        texto = qmd.read_text(encoding="utf-8")
        if 'when-meta="gabarito"' not in texto:
            continue
        rel = qmd.relative_to(RAIZ).as_posix()
        if not ignorado(rel):
            vazando.append(rel)
    assert not vazando, (
        "fonte com respostas seria versionada num repositório público: "
        f"{vazando}"
    )


def test_o_que_esta_em_publico_e_versionado():
    """A contrapartida: o CI só publica o que está no repositório.

    Se o PDF do aluno estiver sendo ignorado, o site sai com link quebrado —
    falha silenciosa, porque o render local funciona.
    """
    if not PUBLICO.exists():
        return
    for pdf in PUBLICO.glob("*.pdf"):
        rel = pdf.relative_to(RAIZ).as_posix()
        assert not ignorado(rel), (
            f"{rel} está gitignorado; o CI não vai publicá-lo e o link do site "
            f"vai quebrar"
        )


def test_todo_pdf_publicado_esta_linkado_no_site():
    """PDF publicado que ninguém alcança é peso morto; link quebrado é pior."""
    if not PUBLICO.exists():
        return
    fontes = [RAIZ / "index.qmd", *(RAIZ / "content").rglob("*.qmd")]
    texto = "\n".join(f.read_text(encoding="utf-8") for f in fontes if f.exists())
    for pdf in PUBLICO.glob("*.pdf"):
        rel = pdf.relative_to(RAIZ).as_posix()
        assert rel in texto, f"{rel} é publicado mas não está linkado em nenhum .qmd"


# --------------------------------------------------------------------------
# listas computacionais — sem gabarito, o notebook do Colab É o enunciado
# --------------------------------------------------------------------------
#
# Três invariantes diferentes dos de cima, porque a lista computacional não
# segue a maquinaria de dupla renderização (sem gabarito, sem PDF de
# enunciado): o `.qmd` é fonte de um `.ipynb`, não de um PDF, e a "resposta
# que vaza" aqui não é um bloco de gabarito — é uma célula que o professor
# esqueceu de limpar antes de commitar.


def test_a_lista_computacional_nao_defasou_da_fonte():
    """Irmão de test_notebooks_estao_atualizados, e não a mesma varredura.

    Aquela está presa a `content/` e alimenta os testes de total do livro, que
    uma lista falsearia. O invariante é o mesmo: o .qmd é a fonte, o .ipynb é
    derivado, e o aluno não pode abrir uma versão que a fonte já não tem.
    """
    gerar = carregar_gerador_de_lista()
    for fonte in sorted(ATIVIDADES.glob("lista-comp-*.qmd")):
        destino = fonte.with_suffix(".ipynb")
        assert destino.exists(), f"falta o notebook de {fonte.name}"
        em_memoria = gerar.serializa(gerar.normaliza(gerar.gerar_lista(fonte)))
        assert em_memoria == destino.read_text(encoding="utf-8"), (
            f"{destino.name} defasou de {fonte.name}; rode scripts/gerar-lista.py"
        )


def test_nenhuma_celula_de_resposta_vem_preenchida():
    """O guarda contra commitar o notebook depois de conferi-lo executando.

    A marca é literal: célula de código de resposta contém só `# sua resposta`,
    célula de texto contém só `*sua resposta aqui*`.
    """
    for nb_path in sorted(ATIVIDADES.glob("lista-comp-*.ipynb")):
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        for i, celula in enumerate(nb["cells"]):
            fonte = "".join(celula["source"]).strip()
            if fonte.startswith("# sua resposta"):
                assert fonte == "# sua resposta", (
                    f"{nb_path.name}, célula {i}: resposta de código preenchida"
                )
            if "*sua resposta aqui*" in fonte:
                assert fonte == "*sua resposta aqui*", (
                    f"{nb_path.name}, célula {i}: resposta de texto preenchida"
                )


def test_nenhuma_celula_da_lista_guarda_saida():
    """O mesmo invariante dos notebooks de aula, mais um motivo: saída entrega resposta."""
    for nb_path in sorted(ATIVIDADES.glob("lista-comp-*.ipynb")):
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        for i, celula in enumerate(nb["cells"]):
            if celula["cell_type"] != "code":
                continue
            assert not celula.get("outputs"), f"{nb_path.name}, célula {i}: saída commitada"
            assert celula.get("execution_count") is None, (
                f"{nb_path.name}, célula {i}: contador de execução commitado"
            )
