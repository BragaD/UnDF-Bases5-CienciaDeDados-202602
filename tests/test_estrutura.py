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


# Alvo de link markdown que não aponta para o DIRETÓRIO de dados.
#
# O lookahead exige `dados/` com barra, não a palavra `dados` solta. A primeira
# versão pedia só a palavra, e isso quebrou: as seções do capítulo 7 se chamam
# `01-explorando-seus-dados.qmd` e `05-manipulando-dados.qmd`, então QUALQUER
# capítulo que linkasse para lá era acusado de usar caminho relativo de dados.
# Pego pelo capítulo 10, que legitimamente aponta para o 7.
#
# Com a barra, `](../dados/x.csv)` continua não casando — e portanto continua
# sendo pego pela regra abaixo, que é o defeito que este teste existe para achar.
LINK_MD_SEM_DADOS = re.compile(r"\]\((?![^)]*dados/)[^)]*\)")


def test_nenhum_qmd_usa_caminho_relativo_de_dados():
    """execute-dir: project => o cwd é a raiz. '../../dados/' nunca resolve.

    Detecta `../dados/`, `../../dados/` e `Path("../dados")` — a co-ocorrência de
    um caminho-pai com a palavra `dados` na mesma linha.

    Antes de aplicar a regra, remove o ALVO de links markdown que não mencionem
    `dados`. Sem isso o teste acusa prosa legítima, e não em casos raros: este é um
    livro em português sobre *dados*, cujos capítulos se referenciam com
    `[Capítulo 6](../cap06/index.qmd)` — a palavra e o `../` caem na mesma linha o
    tempo todo. O caso que motivou isto foi
    `content/cap01/03-hipotese-motivadora-datasciencester.qmd`.

    Isto aumenta a PRECISÃO sem reduzir a cobertura: um link markdown que aponte
    para `dados` (`[x](../dados/y.csv)`) não é removido e continua acusado, e
    nenhuma outra forma de escrever um caminho deixa de ser vista.

    Limite conhecido, o mesmo de antes: construções multi-linha (prefixo atribuído
    numa linha, usado noutra) não são detectadas.
    """
    ofensores = [
        str(p.relative_to(RAIZ))
        for p in CONTENT.rglob("*.qmd")
        if any(
            re.search(r"\.\.[/\\]", limpa) and "dados" in limpa
            for line in p.read_text(encoding="utf-8").split("\n")
            for limpa in [LINK_MD_SEM_DADOS.sub("]()", line)]
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
    padrao_numero = re.compile(r"se[çc][ãa]o\s+(\d+)\.\d+", re.IGNORECASE)
    ofensores = []
    for p in CONTENT.rglob("*.qmd"):
        # O número do NOSSO capítulo, tirado do caminho: content/cap07/... -> 7
        m_cap = re.search(r"cap(\d+)", str(p))
        nosso_cap = int(m_cap.group(1)) if m_cap else None

        texto = p.read_text(encoding="utf-8")
        for match in padrao_numero.finditer(texto):
            # "seção 7.1" dentro de content/cap07/ é a NOSSA numeração, legítima
            # mesmo perto de uma citação ao Grus — o capítulo 7 daqui é o 10 dele.
            if nosso_cap is not None and int(match.group(1)) == nosso_cap:
                continue
            trecho = texto[match.start() : match.start() + 80].lower()
            if "grus" in trecho:
                ofensores.append(f"{p.relative_to(RAIZ)}: {match.group(0)}")
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


def test_nenhum_chunk_comeca_com_linha_indentada():
    """Um chunk que abre com linha indentada é um bloco partido entre células — e
    ele falha em SILÊNCIO.

    O caso que motivou este teste: no capítulo 10, uma classe estava dividida em
    quatro chunks, cada um com um `def` indentado, sem reabrir o `class`. O
    `quarto render` não acusa nada; o IPython aceita a célula indentada e
    simplesmente **não anexa o método à classe**. O livro publicaria uma classe
    quebrada, sem erro, sem teste vermelho, sem nada na tela que denunciasse.

    Cada `.qmd` roda num kernel próprio, mas os chunks DENTRO de um arquivo
    compartilham estado — o que torna tentador continuar um bloco na célula
    seguinte. Não funciona: o Python fecha o bloco no fim da célula.

    A regra: todo chunk começa em coluna zero. Se um bloco (classe, função, laço,
    `with`) precisa de mais de uma célula, ele está no chunk errado — junte tudo
    numa célula só.
    """
    ofensores = []
    for p in sorted(CONTENT.rglob("*.qmd")):
        texto = p.read_text(encoding="utf-8")
        for m in re.finditer(r"^```\{python\}\n(.*?)^```", texto, re.S | re.M):
            for linha in m.group(1).split("\n"):
                despido = linha.strip()
                if not despido or despido.startswith("#"):
                    continue  # opções `#|` e comentários não contam
                if linha[:1] in (" ", "\t"):
                    ofensores.append(f"{p.relative_to(RAIZ)}: {linha.strip()[:50]}")
                break  # só a primeira linha de código de cada chunk importa
    assert not ofensores, (
        "chunk começando com linha indentada (bloco partido entre células, "
        "falha silenciosa): " + "; ".join(ofensores)
    )


def test_modo_leitura_esta_ligado_de_ponta_a_ponta():
    """O CSS e o script do modo leitura precisam existir E estar registrados.

    Isto não é hipotético: por um tempo o `styles.css` deste livro já trazia
    todas as regras de `.btn-modo-leitura` e de `html.modo-leitura`, herdadas
    da cópia da infra do Bases 3 — mas sem o `modo-leitura.html` e sem o
    `include-in-header` no `_quarto.yml`. Resultado: dezenas de linhas de CSS
    válido para um botão que nunca era criado, e nenhum erro em lugar nenhum.

    Uma peça de front-end só está entregue quando as três metades se encontram:
    o CSS, o script que injeta o elemento, e o registro que manda o Quarto
    incluir o script.
    """
    script = RAIZ / "modo-leitura.html"
    css = (RAIZ / "styles.css").read_text(encoding="utf-8")
    yml = QUARTO_YML.read_text(encoding="utf-8")

    assert script.exists(), "modo-leitura.html não existe"
    corpo = script.read_text(encoding="utf-8")

    assert re.search(r"^\s*include-in-header:\s*modo-leitura\.html\s*$", yml, re.M), (
        "modo-leitura.html não está em include-in-header — o script nunca "
        "chega à página, e o CSS vira código morto"
    )

    # As duas pontas têm que concordar no nome das classes.
    for classe in ("modo-leitura", "btn-modo-leitura"):
        assert classe in corpo, f"o script não usa a classe {classe!r}"
        assert classe in css, f"styles.css não estiliza a classe {classe!r}"

    # O estado precisa sobreviver à troca de página, e a chave não pode
    # colidir com a do Bases 3: os dois livros dividem o mesmo domínio,
    # logo o mesmo localStorage.
    assert "localStorage" in corpo
    assert "bases5-" in corpo, "a chave do localStorage precisa ser própria deste livro"
