"""Invariantes dos notebooks de aula.

Os notebooks de `notebooks/` são **derivados** dos `.qmd`, não uma segunda
fonte de conteúdo. A falha que este arquivo existe para pegar é a mesma que
assombra o resto do projeto, na sua versão local: alguém edita um `.qmd`,
esquece de rodar `make notebooks`, e a aula roda com uma versão do capítulo
que o livro publicado já não tem — sem erro nenhum na tela.

Um chunk que fica de fora é o caso mais traiçoeiro: 19 dos chunks executáveis
do livro moram **dentro** de callouts, e uma conversão ingênua os transforma
em texto. O notebook continua abrindo, continua executando, e quebra várias
células adiante, num `NameError` que não aponta para a causa.
"""
import importlib.util
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NOTEBOOKS = RAIZ / "notebooks"
CERCA = re.compile(r"^(`{3,})(.*)$")


def carregar_gerador():
    """Importa scripts/gerar-notebooks.py (o hífen impede um `import` normal)."""
    caminho = RAIZ / "scripts" / "gerar-notebooks.py"
    spec = importlib.util.spec_from_file_location("gerar_notebooks", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def chunks_executaveis(caminho: Path) -> int:
    """Conta os ```{python} de um .qmd que o Quarto realmente executa.

    Contagem deliberadamente independente da do gerador: varre as cercas de
    código sem saber o que é callout. Um teste que reusasse o parser do
    gerador concordaria com ele até quando os dois estivessem errados.
    """
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    total, i = 0, 0
    while i < len(linhas):
        m = CERCA.match(linhas[i])
        if not m:
            i += 1
            continue
        cerca, info = m.group(1), m.group(2).strip()
        corpo = []
        i += 1
        while i < len(linhas) and not linhas[i].startswith(cerca):
            corpo.append(linhas[i])
            i += 1
        i += 1
        if info == "{python}" and not any(
            re.match(r"#\|\s*eval:\s*false", l) for l in corpo
        ):
            total += 1
    return total


def notebooks_esperados() -> dict[str, dict]:
    gerador = carregar_gerador()
    return {gerador.nome_do_arquivo(c): c for c in gerador.le_capitulos()}


def fonte(celula: dict) -> str:
    origem = celula["source"]
    return origem if isinstance(origem, str) else "".join(origem)


def carregados() -> dict[str, dict]:
    return {
        c.name: json.loads(c.read_text(encoding="utf-8"))
        for c in sorted(NOTEBOOKS.glob("*.ipynb"))
    }


def test_um_notebook_por_capitulo():
    esperados = notebooks_esperados()
    encontrados = set(carregados())
    assert encontrados == set(esperados), (
        f"sobrando: {sorted(encontrados - set(esperados))}; "
        f"faltando: {sorted(set(esperados) - encontrados)}"
    )
    assert len(esperados) == 17


def test_notebooks_estao_atualizados():
    """Regerar não pode produzir diferença — senão o .qmd andou sem o notebook."""
    gerador = carregar_gerador()
    entradas = gerador.le_bibliografia()
    curtas = {k: gerador.citacao_curta(v) for k, v in entradas.items()}
    desatualizados = []
    for cap in gerador.le_capitulos():
        nome = gerador.nome_do_arquivo(cap)
        atual = (NOTEBOOKS / nome).read_text(encoding="utf-8")
        novo = gerador.serializa(
            gerador.normaliza(gerador.monta_notebook(cap, curtas, entradas))
        )
        if atual != novo:
            desatualizados.append(nome)
    assert not desatualizados, (
        f"notebooks defasados em relação aos .qmd: {desatualizados}. "
        f"Rode `make notebooks`."
    )


def test_nenhum_notebook_guarda_saida():
    """Quem executa é o aluno, na aula. Saída gravada tira o sentido disso."""
    for nome, nb in carregados().items():
        for i, celula in enumerate(nb["cells"]):
            if celula["cell_type"] != "code":
                continue
            assert not celula.get("outputs"), f"{nome}: célula {i} tem saída gravada"
            assert celula.get("execution_count") is None, (
                f"{nome}: célula {i} tem execution_count gravado"
            )


def test_primeira_celula_de_codigo_acha_a_raiz():
    """Sem o chdir, `from scratch...` e `dados/...` estouram fora da raiz."""
    for nome, nb in carregados().items():
        codigo = [c for c in nb["cells"] if c["cell_type"] == "code"]
        assert codigo, f"{nome}: nenhuma célula de código"
        preparo = fonte(codigo[0])
        assert "_quarto.yml" in preparo and "os.chdir" in preparo, (
            f"{nome}: a primeira célula de código não é a de preparo"
        )


def test_todo_chunk_executavel_do_livro_virou_celula():
    """19 chunks que executam moram dentro de callouts; nenhum pode virar texto."""
    esperados = notebooks_esperados()
    carregado = carregados()
    for nome, cap in esperados.items():
        do_livro = sum(chunks_executaveis(RAIZ / href) for href in cap["arquivos"])
        no_notebook = sum(
            1 for c in carregado[nome]["cells"] if c["cell_type"] == "code"
        )
        assert no_notebook == do_livro + 1, (
            f"{nome}: {no_notebook - 1} células de código para {do_livro} chunks "
            f"executáveis no livro (a mais é a de preparo)"
        )


def test_nenhum_link_aponta_para_qmd():
    """Um link relativo a .qmd não resolve de dentro de notebooks/."""
    for nome, nb in carregados().items():
        for i, celula in enumerate(nb["cells"]):
            if celula["cell_type"] != "markdown":
                continue
            for alvo in re.findall(r"\]\(([^)]+)\)", fonte(celula)):
                assert not alvo.endswith(".qmd"), (
                    f"{nome}: célula {i} liga para {alvo}, que não existe daqui"
                )


def test_nenhuma_citacao_ficou_por_resolver():
    """`@grus2019` só vira texto legível se o gerador conhecer a chave."""
    chaves = carregar_gerador().le_bibliografia()
    for nome, nb in carregados().items():
        for i, celula in enumerate(nb["cells"]):
            if celula["cell_type"] != "markdown":
                continue
            pendentes = [c for c in chaves if f"@{c}" in fonte(celula)]
            assert not pendentes, f"{nome}: célula {i} tem citação crua {pendentes}"


def test_quarto_ignora_a_pasta_de_notebooks():
    """Sem isto, o Quarto tentaria publicar os notebooks como páginas do livro."""
    ignore = RAIZ / ".quartoignore"
    assert ignore.exists(), ".quartoignore não existe"
    linhas = [
        l.strip()
        for l in ignore.read_text(encoding="utf-8").splitlines()
        if l.strip() and not l.strip().startswith("#")
    ]
    assert "notebooks/" in linhas
