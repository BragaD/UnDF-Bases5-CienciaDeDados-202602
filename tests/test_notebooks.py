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


def eh_preparo(src: str) -> bool:
    return "_quarto.yml" in src and "os.chdir" in src


def test_a_celula_de_preparo_vem_antes_de_quem_depende_dela():
    """Sem o chdir, `from scratch...` e `dados/...` estouram fora da raiz.

    Nos notebooks gerados o preparo é a primeira célula de código, sempre. No
    de onboarding ele aparece depois da explicação do que ele faz — o que é
    deliberado, e por isso o invariante checado aqui é o que de fato importa:
    o preparo tem de vir **antes** da primeira célula que usa `scratch` ou
    `dados/`. Exigir a primeira posição seria mais fácil de escrever e testaria
    a convenção em vez da propriedade.
    """
    for nome, nb in carregados().items():
        codigo = [fonte(c) for c in nb["cells"] if c["cell_type"] == "code"]
        assert codigo, f"{nome}: nenhuma célula de código"

        preparos = [i for i, src in enumerate(codigo) if eh_preparo(src)]
        assert preparos, f"{nome}: não tem célula de preparo"

        dependentes = [
            i for i, src in enumerate(codigo)
            if ("scratch" in src or "dados/" in src) and not eh_preparo(src)
        ]
        if dependentes:
            assert preparos[0] < dependentes[0], (
                f"{nome}: a célula {dependentes[0]} usa scratch/dados antes de "
                f"o preparo rodar (preparo está em {preparos[0]})"
            )

        assert eh_preparo(codigo[0]), (
            f"{nome}: o notebook tem de abrir com a célula de preparo"
        )


def test_todo_chunk_executavel_do_livro_virou_celula():
    """19 chunks que executam moram dentro de callouts; nenhum pode virar texto.

    A contagem esperada é: os chunks do capítulo, mais a célula de preparo,
    mais — só no capítulo do onboarding — os chunks do texto de onboarding.
    Todas contadas por este arquivo, sem reusar o parser do gerador.
    """
    gerador = carregar_gerador()
    esperados = notebooks_esperados()
    carregado = carregados()
    for nome, cap in esperados.items():
        do_livro = sum(chunks_executaveis(RAIZ / href) for href in cap["arquivos"])
        extras = 1  # a célula de preparo
        if cap["numero"] == gerador.CAP_ONBOARDING:
            extras += chunks_executaveis(gerador.ONBOARDING)
        no_notebook = sum(
            1 for c in carregado[nome]["cells"] if c["cell_type"] == "code"
        )
        assert no_notebook == do_livro + extras, (
            f"{nome}: {no_notebook} células de código para {do_livro} chunks "
            f"do livro mais {extras} de infraestrutura"
        )


def test_o_onboarding_esta_no_notebook_da_aula_2():
    """O onboarding do Colab não existe no livro; se sumir daqui, some de tudo."""
    gerador = carregar_gerador()
    assert gerador.ONBOARDING.exists(), "scripts/onboarding-colab.md não existe"

    cap = next(c for c in gerador.le_capitulos()
               if c["numero"] == gerador.CAP_ONBOARDING)
    nb = carregados()[gerador.nome_do_arquivo(cap)]
    texto = "\n".join(fonte(c) for c in nb["cells"])
    for marca in ("Shift + Enter", "Reiniciar sessão", "Salvar uma cópia no Drive"):
        assert marca in texto, f"o onboarding perdeu a menção a {marca!r}"

    # E não pode ter vazado para o livro: lá seria comentário sobre ferramenta.
    livro = "\n".join(
        f.read_text(encoding="utf-8") for f in (RAIZ / "content").rglob("*.qmd")
    )
    assert "Shift + Enter" not in livro, (
        "instrução de Colab apareceu no livro; ela pertence só ao notebook"
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


def test_todo_capitulo_tem_link_para_o_colab_e_nenhum_notebook_o_repete():
    """O link mora no site, para levar ao notebook; dentro dele é redundante."""
    gerador = carregar_gerador()
    carregado = carregados()
    for cap in gerador.le_capitulos():
        idx = RAIZ / f"content/cap{cap['numero']:02d}/index.qmd"
        texto = idx.read_text(encoding="utf-8")
        nb = gerador.nome_do_arquivo(cap)
        assert "colab.research.google.com" in texto, (
            f"{idx.relative_to(RAIZ)} não tem link para o Colab"
        )
        assert nb in texto, (
            f"{idx.relative_to(RAIZ)} liga para o Colab, mas não para {nb}"
        )
        dentro = "\n".join(fonte(c) for c in carregado[nb]["cells"])
        assert "colab.research.google.com" not in dentro, (
            f"{nb} repete o link do Colab; quem está lendo já está nele"
        )


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
