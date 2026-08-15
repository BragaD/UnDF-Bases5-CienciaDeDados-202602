"""Invariantes que o Quarto não checa sozinho.

A pior falha deste tipo de projeto é silenciosa: um .qmd que existe no disco,
não está no _quarto.yml, e simplesmente não aparece no livro. Ninguém percebe
até alguém procurar a seção.
"""
import importlib.util
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
QUARTO_YML = RAIZ / "_quarto.yml"
CONTENT = RAIZ / "content"


def hrefs_registrados() -> set[str]:
    """Extrai os href: do _quarto.yml sem depender de um parser YAML.

    Ignora linhas comentadas (lstrip() começando com '#'). Sem isso,
    `# - href: content/cap12/08-regularizacao.qmd` conta como registrado: um
    capítulo comentado por engano fica "presente" para o teste enquanto as
    páginas somem do livro renderizado — o oposto do que este arquivo existe
    para pegar.
    """
    linhas = QUARTO_YML.read_text(encoding="utf-8").split("\n")
    ativas = "\n".join(l for l in linhas if not l.lstrip().startswith("#"))
    return set(re.findall(r"href:\s*(\S+\.qmd)", ativas))


def carregar_livro():
    """Importa LIVRO de scripts/gerar-stubs.py.

    O nome do arquivo tem hífen, então não é um módulo importável por
    `import`; carrega por caminho.
    """
    caminho = RAIZ / "scripts" / "gerar-stubs.py"
    spec = importlib.util.spec_from_file_location("gerar_stubs", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo.LIVRO


def qmds_no_disco() -> set[str]:
    return {
        str(p.relative_to(RAIZ))
        for p in CONTENT.rglob("*.qmd")
        if not p.name.startswith("_")
    }


def test_todo_qmd_esta_registrado_no_quarto_yml():
    faltando = qmds_no_disco() - hrefs_registrados()
    assert not faltando, (
        "arquivos no disco que não aparecem no livro: " + ", ".join(sorted(faltando))
    )


def test_todo_href_do_quarto_yml_existe_no_disco():
    quebrados = {h for h in hrefs_registrados() if not (RAIZ / h).is_file()}
    assert not quebrados, "hrefs apontando para nada: " + ", ".join(sorted(quebrados))


def test_nenhum_qmd_usa_caminho_relativo_de_dados():
    """execute-dir: project => o cwd é a raiz. '../../dados/' nunca resolve.

    Detecta construções `../dados/` e `Path("../dados")` na mesma linha.
    Deixa passar navegação cross-capítulo legítima como `[Capítulo 5](../cap05/index.qmd)`.
    Limite conhecido: construções multi-linha (prefixo atribuído em uma linha, usado em outra)
    não são detectadas.
    """
    ofensores = [
        str(p.relative_to(RAIZ))
        for p in CONTENT.rglob("*.qmd")
        if any(
            re.search(r"\.\.[/\\]", line) and "dados" in line
            for line in p.read_text(encoding="utf-8").split("\n")
        )
    ]
    assert not ofensores, "caminho relativo de dados em: " + ", ".join(sorted(ofensores))


def test_toda_secao_cita_o_grus():
    """Todo .qmd de seção traz um callout `de @grus2019`.

    É o que ancora a seção no livro-texto e o que permite conferir o
    conteúdo depois.
    """
    sem_citacao = [
        str(p.relative_to(RAIZ))
        for p in CONTENT.rglob("*.qmd")
        if p.name != "index.qmd" and "@grus2019" not in p.read_text(encoding="utf-8")
    ]
    assert not sem_citacao, "seções sem citação: " + ", ".join(sorted(sem_citacao))


def test_nenhuma_secao_inventa_numero_de_secao_do_grus():
    """O Grus NÃO numera as seções — o sumário só traz títulos.

    Escrever "seção 12.1 de @grus2019" seria inventar uma referência que o
    livro não tem. O callout cita capítulo + título da seção.

    Detecta qualquer `seção N.N` que tenha `grus` nos ~80 caracteres seguintes.
    Deixa passar referências legítimas aos capítulos deste livro como "veja a seção 9.2
    deste capítulo" ou tabelas de sumário como `| [9.1](01-o-modelo.qmd) |`.
    """
    padrao_numero = re.compile(r"se[çc][ãa]o\s+\d+\.\d+", re.IGNORECASE)
    ofensores = []
    for p in CONTENT.rglob("*.qmd"):
        texto = p.read_text(encoding="utf-8")
        for match in padrao_numero.finditer(texto):
            # Verifica se 'grus' aparece nos ~80 caracteres após a correspondência
            trecho = texto[match.start() : match.start() + 80].lower()
            if "grus" in trecho:
                ofensores.append(str(p.relative_to(RAIZ)))
                break
    assert not ofensores, "número de seção inventado em: " + ", ".join(sorted(ofensores))


def test_dezessete_capitulos():
    dirs = sorted(d.name for d in CONTENT.iterdir() if d.is_dir())
    assert dirs == [f"cap{n:02d}" for n in range(1, 18)]


def test_cada_capitulo_tem_index():
    for n in range(1, 18):
        assert (CONTENT / f"cap{n:02d}" / "index.qmd").is_file(), f"falta cap{n:02d}/index.qmd"


def test_livro_completo_88_secoes_105_arquivos():
    """Nenhum outro teste deste arquivo detecta uma seção inteira sumindo.

    `test_todo_qmd_esta_registrado_no_quarto_yml` e
    `test_todo_href_do_quarto_yml_existe_no_disco` são checagens de diferença
    simétrica: apagar um `.qmd` E as duas linhas correspondentes do
    `_quarto.yml` no mesmo commit passa nos dois. `test_dezessete_capitulos`
    só conta diretórios; `test_cada_capitulo_tem_index` só confere o
    `index.qmd`. A fonte da verdade sobre o que o livro DEVE conter é o
    `LIVRO` de `scripts/gerar-stubs.py` — foi dali que os 105 `.qmd` foram
    gerados —, então este teste confere, capítulo por capítulo, que cada
    arquivo esperado existe em disco E aparece no `_quarto.yml`, e fecha nos
    totais (17 capítulos, 88 seções, 105 arquivos). Como fim de linha, também
    pega um arquivo de seção com nome digitado errado (por exemplo com um
    `_` no início, que `qmds_no_disco()` ignora de propósito): o nome exato
    esperado não existiria em nenhum dos dois lados.
    """
    livro = carregar_livro()
    assert len(livro) == 17, f"esperava 17 capítulos no LIVRO, achei {len(livro)}"

    hrefs = hrefs_registrados()
    total_arquivos = 0
    total_secoes = 0
    for nosso, _grus_cap, _titulo, _leitura, secoes in livro:
        d = CONTENT / f"cap{nosso:02d}"

        index = d / "index.qmd"
        assert index.is_file(), f"falta {index.relative_to(RAIZ)}"
        href_index = str(index.relative_to(RAIZ))
        assert href_index in hrefs, f"{href_index} não registrado no _quarto.yml"
        total_arquivos += 1

        for arquivo, _titulo_secao, _titulo_grus in secoes:
            secao = d / f"{arquivo}.qmd"
            assert secao.is_file(), f"falta {secao.relative_to(RAIZ)}"
            href_secao = str(secao.relative_to(RAIZ))
            assert href_secao in hrefs, f"{href_secao} não registrado no _quarto.yml"
            total_arquivos += 1
            total_secoes += 1

    assert total_secoes == 88, f"esperava 88 seções, achei {total_secoes}"
    assert total_arquivos == 105, f"esperava 105 arquivos, achei {total_arquivos}"
