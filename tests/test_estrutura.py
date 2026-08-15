"""Invariantes que o Quarto não checa sozinho.

A pior falha deste tipo de projeto é silenciosa: um .qmd que existe no disco,
não está no _quarto.yml, e simplesmente não aparece no livro. Ninguém percebe
até alguém procurar a seção.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
QUARTO_YML = RAIZ / "_quarto.yml"
CONTENT = RAIZ / "content"


def hrefs_registrados() -> set[str]:
    """Extrai os href: do _quarto.yml sem depender de um parser YAML."""
    texto = QUARTO_YML.read_text(encoding="utf-8")
    return set(re.findall(r"href:\s*(\S+\.qmd)", texto))


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
