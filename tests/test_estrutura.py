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


def test_seis_capitulos():
    """Seis, e não dezessete.

    Os capítulos 6 a 17 saíram do livro em 2026-09-10, com o abandono da
    abordagem do Grus, e estão em `arquivo/grus/`. Este teste falha tanto se
    um deles voltar por engano quanto se um capítulo novo entrar em `content/`
    sem passar pelo `LIVRO` de `scripts/gerar-stubs.py`.
    """
    dirs = sorted(d.name for d in CONTENT.iterdir() if d.is_dir())
    assert dirs == [f"cap{n:02d}" for n in range(1, 7)]


def test_cada_capitulo_tem_index():
    for n in range(1, 7):
        assert (CONTENT / f"cap{n:02d}" / "index.qmd").is_file(), f"falta cap{n:02d}/index.qmd"


def test_livro_completo_27_secoes_33_arquivos():
    """Nenhum outro teste deste arquivo detecta uma seção inteira sumindo.

    `test_todo_qmd_esta_registrado_no_quarto_yml` e
    `test_todo_href_do_quarto_yml_existe_no_disco` são checagens de diferença
    simétrica: apagar um `.qmd` E as duas linhas correspondentes do
    `_quarto.yml` no mesmo commit passa nos dois. `test_seis_capitulos`
    só conta diretórios; `test_cada_capitulo_tem_index` só confere o
    `index.qmd`. A fonte da verdade sobre o que o livro DEVE conter é o
    `LIVRO` de `scripts/gerar-stubs.py`, então este teste confere, capítulo
    por capítulo, que cada arquivo esperado existe em disco E aparece no
    `_quarto.yml`, e fecha nos totais (6 capítulos, 27 seções, 33 arquivos).
    Como fim de linha, também pega um arquivo de seção com nome digitado
    errado (por exemplo com um `_` no início, que `qmds_no_disco()` ignora de
    propósito): o nome exato esperado não existiria em nenhum dos dois lados.

    Os totais eram 17 / 87 / 104 até 2026-09-10, quando os capítulos 6 a 17
    saíram do livro — ver a spec da ruptura com o Grus.
    """
    livro = carregar_livro()
    assert len(livro) == 6, f"esperava 6 capítulos no LIVRO, achei {len(livro)}"

    hrefs = hrefs_registrados()
    total_arquivos = 0
    total_secoes = 0
    for nosso, _titulo, _islp_cap, secoes in livro:
        d = CONTENT / f"cap{nosso:02d}"

        index = d / "index.qmd"
        assert index.is_file(), f"falta {index.relative_to(RAIZ)}"
        href_index = str(index.relative_to(RAIZ))
        assert href_index in hrefs, f"{href_index} não registrado no _quarto.yml"
        total_arquivos += 1

        for arquivo, _titulo_secao, _islp_secao in secoes:
            secao = d / f"{arquivo}.qmd"
            assert secao.is_file(), f"falta {secao.relative_to(RAIZ)}"
            href_secao = str(secao.relative_to(RAIZ))
            assert href_secao in hrefs, f"{href_secao} não registrado no _quarto.yml"
            total_arquivos += 1
            total_secoes += 1

    assert total_secoes == 27, f"esperava 27 seções, achei {total_secoes}"
    assert total_arquivos == 33, f"esperava 33 arquivos, achei {total_arquivos}"


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


# Marcas de meta-comentário editorial: texto que fala sobre a ESCRITA do
# material em vez de falar sobre ciência de dados. Cada padrão é ancorado no
# próprio material como sujeito ("este livro", "a versão anterior do
# capítulo"), e não em palavras soltas — "abordagem anterior" e "passou a ser"
# aparecem legitimamente no capítulo 5, falando de gradiente descendente, e um
# padrão frouxo os pegaria.
META_COMENTARIO = [
    r"(nest[ae]|noss?[ae]|ness[ae])\s+(nova\s+)?vers[ãa]o\s+d[eo]s?\s+(livro|material|cap[íi]tulo)",
    r"(vers[ãa]o|abordagem|edi[çc][ãa]o)\s+anterior\s+d[eo]s?\s+(livro|material|cap[íi]tulo)",
    r"\breescrit\w*[^.\n]{0,40}(livro|material|cap[íi]tulo|se[çc][ãa]o)",
    r"(livro|material|cap[íi]tulo|se[çc][ãa]o)[^.\n]{0,40}\breescrit\w*",
    r"antes,?\s+est[ea]\s+(livro|material)",
    r"est[ea]\s+(livro|material)\s+(agora|passou a|deixou de|usava|fazia)",
    r"decis[ãa]o\s+(do autor|editorial)",
    r"CLAUDE\.md",
    r"docs/superpowers",
    r"arquivo/grus",
]


def test_o_conteudo_nao_comenta_a_propria_escrita():
    """O site é sobre ciência de dados, não sobre como o material foi escrito.

    Regra do autor, fixada na spec da ruptura com o Grus (2026-09-10): nenhum
    `.qmd` de `content/` diz que houve mudança de abordagem, que um capítulo
    foi reescrito, que a versão anterior fazia de outro jeito, ou que o
    material "agora" usa tal ferramenta. O aluno lê o conteúdo; a história
    editorial vive em `docs/` e no `CLAUDE.md`.

    É a mesma disciplina que já tirou do livro a explicação de Shift+Enter,
    que foi parar no onboarding do Colab: texto sobre a ferramenta ou sobre o
    processo não é texto sobre o conteúdo.

    Falso positivo se corrige editando `META_COMENTARIO` com o motivo escrito
    — nunca silenciando o teste.
    """
    padroes = [re.compile(p, re.IGNORECASE) for p in META_COMENTARIO]
    ofensores = []
    for p in sorted(CONTENT.rglob("*.qmd")):
        for n, linha in enumerate(p.read_text(encoding="utf-8").split("\n"), start=1):
            for padrao in padroes:
                m = padrao.search(linha)
                if m:
                    ofensores.append(f"{p.relative_to(RAIZ)}:{n}: {m.group(0)!r}")
    assert not ofensores, "meta-comentário editorial no conteúdo:\n  " + "\n  ".join(ofensores)


def test_todo_link_interno_para_qmd_resolve():
    """Link relativo para um `.qmd` que não existe vira 404 no site publicado.

    O `quarto render` avisa (`WARN: Unable to resolve link target`), mas **não
    falha** — e o aviso se perde no meio de centenas de linhas de saída. Foi
    assim que a saída dos capítulos 6 a 17, em 2026-09-10, deixou 43 links
    quebrados nos capítulos 1 a 5 sem que nada ficasse vermelho.

    Vale para `content/**/*.qmd` e para o `index.qmd` da raiz, cujos caminhos
    são relativos ao próprio arquivo.
    """
    padrao = re.compile(r"\]\(([^)#\s]+\.qmd)(?:#[^)]*)?\)")
    quebrados = []
    fontes = sorted(CONTENT.rglob("*.qmd")) + [RAIZ / "index.qmd"]
    for p in fontes:
        for n, linha in enumerate(p.read_text(encoding="utf-8").split("\n"), start=1):
            for alvo in padrao.findall(linha):
                if not (p.parent / alvo).resolve().is_file():
                    quebrados.append(f"{p.relative_to(RAIZ)}:{n} -> {alvo}")
    assert not quebrados, "link para .qmd inexistente:\n  " + "\n  ".join(quebrados)


# Capítulos da abordagem nova. Os de 1 a 5 são da anterior e estão fora destes
# guardas de propósito: as figuras deles não usam estilo nenhum, e entram na
# rodada de reescrita daqueles capítulos.
CAPITULOS_NOVOS = [f"cap{n:02d}" for n in range(6, 18)]

ESTILO = 'plt.style.use("estilo-figuras.mplstyle")'

# Seções sem figura, e por quê. Cada entrada é uma decisão registrada, não um
# esquecimento — daí o dicionário em vez de uma lista.
SECOES_SEM_FIGURA: dict[str, str] = {
    "cap06/01-elementos-de-dados-estruturados.qmd": "stub; a figura entra quando a seção for escrita",
    "cap06/02-dados-retangulares.qmd": "stub; a figura entra quando a seção for escrita",
    "cap06/03-lendo-e-tipando-um-arquivo-real.qmd": "stub; a figura entra quando a seção for escrita",
    "cap06/04-limpando-e-transformando.qmd": "stub; a figura entra quando a seção for escrita",
    "cap06/05-agrupando-e-resumindo.qmd": "stub; a figura entra quando a seção for escrita",
    "cap06/06-da-tabela-para-o-modelo.qmd": "stub; a figura entra quando a seção for escrita",
}

# Usos de biblioteca proibida liberados: arquivo -> (biblioteca, motivo).
# `scipy` volta a ser permitido em um lugar só, o dendrograma da seção 15.5,
# porque desenhar a árvore É a lição daquela seção e o AgglomerativeClustering
# do scikit-learn agrupa sem desenhar.
BIBLIOTECA_LIBERADA: dict[str, tuple[str, str]] = {}

PROIBIDAS = {
    "statsmodels": "a disciplina não faz inferência — sem erro-padrão, t nem valor-p",
    "torch": "redes convolucionais e recorrentes são da disciplina de Deep Learning",
    "ISLP": "o pacote dos autores traz uma API que só existe no livro e quebra a regra de dados commitados",
    "scipy": "não é ferramenta da disciplina; a exceção do dendrograma vai em BIBLIOTECA_LIBERADA",
}


def corpos_de_chunks_executaveis(caminho: Path) -> list[str]:
    """Devolve o corpo de cada ```{python} que o Quarto realmente executa.

    Varre as cercas sem saber o que é callout — chunk dentro de `::: {.exemplo}`
    executa igual, e um parser que ignorasse divs deixaria justamente esses
    passarem. Chunks com `#| eval: false` ficam de fora: são os que só ilustram.
    """
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    corpos, i = [], 0
    while i < len(linhas):
        m = re.match(r"^(`{3,})(.*)$", linhas[i])
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
            corpos.append("\n".join(corpo))
    return corpos


def qmds_dos_capitulos_novos() -> list[Path]:
    return sorted(
        p for p in CONTENT.rglob("*.qmd") if p.parent.name in CAPITULOS_NOVOS
    )


def test_todo_chunk_que_desenha_aplica_o_estilo():
    """Figura sem o estilo compartilhado sai de fundo branco e estoura no escuro.

    O site tem tema claro e escuro. `estilo-figuras.mplstyle` fixa fundo
    transparente e cores medidas contra os dois; uma seção que esqueça de
    aplicá-lo produz uma figura que parece de outro material — e ninguém
    percebe até alguém abrir o site no tema escuro.
    """
    faltando = []
    for p in qmds_dos_capitulos_novos():
        texto = p.read_text(encoding="utf-8")
        desenha = any("plt." in c for c in corpos_de_chunks_executaveis(p))
        if desenha and ESTILO not in texto:
            faltando.append(str(p.relative_to(RAIZ)))
    assert not faltando, (
        f"chunk que desenha sem {ESTILO}: " + ", ".join(faltando)
    )


def test_toda_secao_tem_figura():
    """O material ensina por figura, como o livro-texto.

    Toda seção traz ao menos uma figura que carrega a ideia. Uma seção que
    realmente não precise de gráfico entra em SECOES_SEM_FIGURA com o motivo
    escrito — o mesmo padrão de NAO_IMPORTAVEIS em test_scratch.py, porque uma
    exceção sem motivo é um esquecimento disfarçado de decisão.
    """
    sem_figura = []
    for p in qmds_dos_capitulos_novos():
        if p.name == "index.qmd":
            continue
        chave = f"{p.parent.name}/{p.name}"
        if chave in SECOES_SEM_FIGURA:
            continue
        if not any("plt." in c for c in corpos_de_chunks_executaveis(p)):
            sem_figura.append(chave)
    assert not sem_figura, (
        "seção sem figura. Se for deliberado, registre em SECOES_SEM_FIGURA "
        "com o motivo:\n  " + "\n  ".join(sorted(sem_figura))
    )


def test_nenhum_chunk_executavel_usa_biblioteca_proibida():
    """As bibliotecas de fora da disciplina não entram em código que roda.

    Elas podem aparecer em bloco ```python que NÃO executa, para comparar — é
    assim que o material mostra o que existe lá fora sem passar a depender.
    """
    ofensores = []
    for p in qmds_dos_capitulos_novos():
        chave = f"{p.parent.name}/{p.name}"
        for corpo in corpos_de_chunks_executaveis(p):
            for nome in PROIBIDAS:
                if re.search(rf"\b(?:import|from)\s+{nome}\b", corpo):
                    liberado = BIBLIOTECA_LIBERADA.get(chave)
                    if liberado is not None and liberado[0] == nome:
                        continue
                    ofensores.append(f"{chave}: {nome}")
    assert not ofensores, (
        "biblioteca proibida em chunk que executa: " + ", ".join(sorted(set(ofensores)))
    )


def test_toda_excecao_de_figura_e_de_biblioteca_tem_motivo_e_arquivo_real():
    """Exceção sem motivo escrito é esquecimento disfarçado de decisão."""
    motivos = dict(SECOES_SEM_FIGURA)
    motivos.update({k: v[1] for k, v in BIBLIOTECA_LIBERADA.items()})
    for chave, motivo in motivos.items():
        assert (CONTENT / chave).is_file(), f"{chave} não existe mais"
        assert len(motivo) > 40, f"exceção de {chave} sem motivo de verdade"
