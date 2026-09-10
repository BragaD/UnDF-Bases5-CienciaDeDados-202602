# Fundação da estrutura nova e o Capítulo 6 — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pôr de pé a infraestrutura da abordagem nova (bibliografia, formato do `LIVRO`, estilo compartilhado de figuras, guardas novos, dados) e escrever o **Capítulo 6 — Dados: tipos, dados retangulares e `pandas`**, que é a aula de **16/09**.

**Architecture:** O capítulo é seis `.qmd` de seção mais um `index.qmd`, sobre dois conjuntos brasileiros commitados. Cada seção é uma task, verificada com `scripts/executar-secoes.py` (um kernel por página, o análogo fiel do render) e com a suíte de invariantes. A fundação vem antes porque a primeira seção já depende do estilo de figura e dos dados.

**Tech Stack:** Quarto book (engine Jupyter), Python 3.12, `pandas`, `matplotlib`, `pytest`. Sem Docker no caminho crítico: tudo roda no `.venv/` da raiz.

**Spec:** `docs/superpowers/specs/2026-09-10-estrutura-nova-islp-design.md`

## Global Constraints

- **`scikit-learn` de ponta a ponta; nada é escrito à mão.** Este capítulo não ajusta modelo nenhum — ele para em `X` e `y`.
- **Proibidos em chunk que executa:** `statsmodels`, `torch`, o pacote `ISLP`, `scipy`.
- **Nenhum byte vem da rede em tempo de render.** Dado vive em `dados/`, com caminho **a partir da raiz**: `pd.read_csv("dados/alugueis.csv")`, nunca `"../../dados/..."`.
- **Todo chunk com RNG usa semente explícita.** Neste capítulo, `rng = np.random.default_rng(42)` se houver sorteio.
- **Todo `.qmd` novo é registrado em `_quarto.yml`.** `make teste` falha se faltar.
- **O site não comenta a própria escrita.** Nenhuma linha sobre mudança de abordagem, reescrita ou decisão do autor. `test_o_conteudo_nao_comenta_a_propria_escrita` trava isso.
- **Toda seção tem ao menos uma figura que carrega a ideia**, e todo chunk que desenha aplica `estilo-figuras.mplstyle`.
- **O capítulo 6 não tem callout de correspondência ao ISLP** — não há seção correspondente. É exceção registrada nos testes com motivo escrito.
- **Editar um `.qmd` obriga a rodar `gerar-notebooks.py`**, senão `test_notebooks_estao_atualizados` derruba a suíte.
- **Não rode `make render` durante a implementação.** Ele é serializado, leva minutos e envenena o `_freeze/` se um `.qmd` mudar no meio. A verificação é `scripts/executar-secoes.py`. O render completo é a última task.
- Ambiente de toda verificação: `export MPLBACKEND=Agg PYTHONHASHSEED=0`.

---

### Task 1: Bibliografia e o formato do `LIVRO`

O `LIVRO` de `scripts/gerar-stubs.py` é a fonte da verdade sobre o que o material contém. Hoje ele é uma 3-tupla sem referência a fonte nenhuma, porque a abordagem anterior tinha acabado de sair. A abordagem nova cita o ISLP **com número de seção**, então o `LIVRO` precisa carregar essa referência e o gerador de stubs precisa emiti-la.

Esta task **não** acrescenta capítulo nenhum: só muda o formato e a bibliografia, e a suíte continua verde com os cinco capítulos que existem.

**Files:**
- Modify: `references.bib` (acrescentar `james2023`)
- Modify: `scripts/gerar-stubs.py` (formato do `LIVRO`, `stub_secao`, `stub_index`, `gerar`, `imprimir_yaml`)
- Modify: `tests/test_estrutura.py:155-200` (`test_livro_completo_21_secoes_26_arquivos`, o desempacotamento das tuplas)

**Interfaces:**
- Consumes: nada.
- Produces: `LIVRO` como lista de `(nosso: int, titulo: str, islp: int | None, secoes: list[tuple[str, str, str | None]])`, onde cada seção é `(arquivo, titulo_secao, islp_secao)`. `islp` e `islp_secao` são `None` quando não há correspondência. Tasks 4 e 11 consomem esse formato.

- [ ] **Step 1: Acrescentar o ISLP ao `references.bib`**

**Atenção:** já existe uma entrada `james2021` — é a **2ª edição em R**, outro livro. A nossa é a edição em Python, de 2023. As duas convivem.

Acrescente ao fim de `references.bib`:

```bibtex
@book{james2023,
  author    = {James, Gareth and Witten, Daniela and Hastie, Trevor and Tibshirani, Robert and Taylor, Jonathan},
  title     = {An Introduction to Statistical Learning with Applications in Python},
  publisher = {Springer},
  year      = {2023},
  isbn      = {978-3-031-38746-3}
}
```

- [ ] **Step 2: Mudar o formato do `LIVRO` e os stubs**

Em `scripts/gerar-stubs.py`, substitua o comentário e as cinco entradas do `LIVRO` por este bloco (os cinco capítulos são os mesmos; o que muda é a aridade das tuplas):

```python
# (nosso_num, titulo_capitulo, islp_cap, [(arquivo, titulo_secao, islp_secao), ...])
#
# `islp_cap` e `islp_secao` são o capítulo e a seção correspondentes em
# @james2023, ou None quando não há correspondência. O ISLP **numera** as
# seções — 3.3.1, 8.2.2, 12.4.1 estão no sumário —, então o callout de
# abertura cita o número. Os capítulos 1 a 5 são de outra abordagem e não
# citam o ISLP; o 6 e o 17 não têm correspondência nele.
LIVRO = [
    (1, "Introdução", None, [
        ("01-a-ascensao-dos-dados", "A Ascensão dos Dados", None),
        ("02-o-que-e-ciencia-de-dados", "O que é Ciência de Dados?", None),
        ("03-hipotese-motivadora-datasciencester", "Hipótese Motivadora: DataSciencester", None),
    ]),
    (2, "Um Curso Rápido de Python", None, [
        ("01-ambiente-e-sintaxe", "Ambiente e Sintaxe", None),
        ("02-funcoes-strings-excecoes", "Funções, Strings e Exceções", None),
        ("03-estruturas-de-dados", "Estruturas de Dados", None),
        ("04-controle-de-fluxo", "Controle de Fluxo", None),
        ("05-testes-classes-e-geradores", "Testes, Classes e Geradores", None),
        ("06-ferramentas-e-tipos", "Ferramentas e Anotações de Tipo", None),
    ]),
    (3, "Visualizando Dados", None, [
        ("01-matplotlib", "matplotlib", None),
        ("02-graficos-de-barras", "Gráficos de Barras", None),
        ("03-graficos-de-linhas", "Gráficos de Linhas", None),
        ("04-graficos-de-dispersao", "Gráficos de Dispersão", None),
    ]),
    (4, "Álgebra Linear", None, [
        ("01-vetores", "Vetores", None),
        ("02-matrizes", "Matrizes", None),
    ]),
    (5, "Gradiente Descendente", None, [
        ("01-a-ideia-por-tras-do-gradiente", "A Ideia por Trás do Gradiente Descendente", None),
        ("02-estimando-o-gradiente", "Estimando o Gradiente", None),
        ("03-usando-o-gradiente", "Usando o Gradiente", None),
        ("04-escolhendo-o-tamanho-do-passo", "Escolhendo o Tamanho do Passo", None),
        ("05-ajustando-modelos", "Ajustando Modelos com Gradiente Descendente", None),
        ("06-minibatch-e-estocastico", "Minibatch e Gradiente Estocástico", None),
    ]),
]
```

E substitua as quatro funções que consomem o `LIVRO`:

```python
def stub_secao(titulo: str, islp_secao) -> str:
    correspondencia = ""
    if islp_secao is not None:
        correspondencia = (
            "\n::: {.callout-note}\n"
            f"Esta seção corresponde à seção {islp_secao} de @james2023.\n"
            ":::\n"
        )
    return f"""# {titulo}
{correspondencia}
::: {{.callout-warning}}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
"""


def stub_index(nosso: int, titulo: str, islp_cap, secoes) -> str:
    linhas = [f"# {titulo}", ""]
    if islp_cap is not None:
        linhas += [
            "::: {.callout-note}",
            f"Este capítulo corresponde ao capítulo {islp_cap} de @james2023.",
            ":::",
            "",
        ]
    linhas += [
        "::: {.callout-warning}",
        "## Em construção",
        "A visão geral deste capítulo ainda será escrita.",
        ":::",
        "",
        "## Seções",
        "",
        "| Seção | Tópico |",
        "|---|---|",
    ]
    for i, (arquivo, titulo_secao, _islp) in enumerate(secoes, start=1):
        linhas.append(f"| [{nosso}.{i}]({arquivo}.qmd) | {titulo_secao} |")
    linhas += ["", "## Leituras adicionais", "", "*A escrever.*", ""]
    return "\n".join(linhas)


def gerar() -> None:
    criados = pulados = 0
    for nosso, titulo, islp_cap, secoes in LIVRO:
        d = CONTENT / f"cap{nosso:02d}"
        d.mkdir(parents=True, exist_ok=True)

        alvo = d / "index.qmd"
        if alvo.exists():
            pulados += 1
        else:
            alvo.write_text(stub_index(nosso, titulo, islp_cap, secoes), encoding="utf-8")
            criados += 1

        for arquivo, titulo_secao, islp_secao in secoes:
            alvo = d / f"{arquivo}.qmd"
            if alvo.exists():
                pulados += 1
                continue
            alvo.write_text(stub_secao(titulo_secao, islp_secao), encoding="utf-8")
            criados += 1
    print(f"criados: {criados}   pulados (já existiam): {pulados}")


def imprimir_yaml() -> None:
    print("  chapters:")
    print('    - text: "Início"')
    print("      href: index.qmd")
    for nosso, titulo, _islp_cap, secoes in LIVRO:
        print(f'    - part: "Capítulo {nosso}: {titulo}"')
        print("      chapters:")
        print(f"        - href: content/cap{nosso:02d}/index.qmd")
        print('          text: "Visão Geral"')
        for arquivo, titulo_secao, _islp in secoes:
            print(f"        - href: content/cap{nosso:02d}/{arquivo}.qmd")
            print(f'          text: "{titulo_secao}"')
```

- [ ] **Step 3: Ajustar o teste que desempacota as tuplas**

Em `tests/test_estrutura.py`, dentro de `test_livro_completo_21_secoes_26_arquivos`, troque as duas linhas de desempacotamento:

```python
    for nosso, _titulo, _islp_cap, secoes in livro:
```

e

```python
        for arquivo, _titulo_secao, _islp_secao in secoes:
```

- [ ] **Step 4: Rodar a suíte**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/pytest tests/ -q
```

Esperado: **43 passed**. Se `test_livro_completo_21_secoes_26_arquivos` falhar com `ValueError: too many values to unpack`, o Step 3 não foi aplicado.

- [ ] **Step 5: Verificar que o gerador é idempotente**

```bash
.venv/bin/python scripts/gerar-stubs.py
```

Esperado: `criados: 0   pulados (já existiam): 26`. Se criar qualquer arquivo, um nome de arquivo no `LIVRO` foi digitado errado — corrija antes de commitar, e apague o arquivo criado por engano.

- [ ] **Step 6: Commit**

```bash
git add references.bib scripts/gerar-stubs.py tests/test_estrutura.py
git commit -m "feat(fundacao): o LIVRO passa a carregar a correspondência com o ISLP

O ISLP numera as seções, então o stub de seção volta a ter callout de
correspondência — agora com o número, que é o que o livro-texto novo
permite e o anterior não permitia.

references.bib ganha james2023, a edição em Python. A james2021 que já
estava lá é a 2a edição em R, outro livro, e as duas convivem."
```

---

### Task 2: O estilo compartilhado das figuras, e os guardas novos

O site tem tema claro (`cosmo`) e escuro (`darkly`), e hoje **não existe estilo de figura nenhum** — três chunks em cinco capítulos definem `figsize` na mão. Setenta seções produzindo cada uma o seu gráfico sem estilo comum dá um material que parece montado por dez pessoas, e figura de fundo branco estoura no tema escuro.

As cores abaixo **foram medidas** contra `#FFFFFF` (fundo do `cosmo`) e `#222222` (fundo do `darkly`): todas passam de 3:1 nos dois. A malha é a exceção, e de propósito — malha a 3:1 seria alta demais —, então ela usa transparência, que se ajusta sozinha ao fundo.

**Files:**
- Create: `estilo-figuras.mplstyle`
- Modify: `tests/test_estrutura.py` (três testes novos, ao fim do arquivo)
- Modify: `tests/test_notebooks.py:9-12` (docstring do módulo, que ainda diz "19 dos chunks executáveis")

**Interfaces:**
- Consumes: nada.
- Produces: o arquivo `estilo-figuras.mplstyle`, aplicado por `plt.style.use("estilo-figuras.mplstyle")` no chunk de setup de toda seção que desenha (tasks 5 a 11). O caminho é relativo à raiz e resolve nos três contextos: no site (`execute-dir: project`), no notebook local (a célula de preparo faz `chdir` para a raiz) e no Colab (a célula de preparo clona o repositório e entra nele).

- [ ] **Step 1: Escrever o estilo**

Crie `estilo-figuras.mplstyle`:

```
# Estilo compartilhado das figuras do material.
#
# Aplicado por `plt.style.use("estilo-figuras.mplstyle")` no chunk de setup de
# toda seção que desenha. O caminho é relativo à raiz do projeto, que é o cwd
# em todos os contextos: no site (execute-dir: project), no notebook local (a
# célula de preparo faz chdir) e no Colab (a célula clona o repositório).
#
# O site tem tema CLARO e ESCURO. Por isso o fundo é transparente e todas as
# cores abaixo passam de 3:1 tanto sobre #FFFFFF (fundo do cosmo) quanto sobre
# #222222 (fundo do darkly) — medido, não estimado. A malha é a única exceção,
# e usa alfa em vez de cor fixa: malha a 3:1 competiria com o dado.
#
# A paleta é a mesma das páginas de apoio/: os azuis do logo da UnDF sobre o
# fundo e o texto do cosmo. A regra de leitura é a mesma também — azul é o
# terreno, laranja é o que se move.

figure.figsize:   6.4, 4.0
figure.dpi:       140
figure.facecolor: none
axes.facecolor:   none
savefig.facecolor: none
savefig.transparent: True
savefig.bbox:     tight

# #6C757D: 4.69 no claro, 3.39 no escuro.
text.color:       6C757D
axes.labelcolor:  6C757D
xtick.color:      6C757D
ytick.color:      6C757D

# #7A8894: 3.64 no claro, 4.38 no escuro. Cromo, não texto.
axes.edgecolor:   7A8894
axes.titlecolor:  6C757D

axes.spines.top:   False
axes.spines.right: False

axes.grid:        True
grid.color:       7A8894
grid.alpha:       0.25
grid.linewidth:   0.6

# Ciclo de cores: azul da marca, o laranja quente da casa, verde e roxo.
# Medidos (claro / escuro): 3.26/4.88, 4.30/3.70, 4.09/3.89, 3.36/4.73.
axes.prop_cycle: cycler('color', ['4195D1', 'D9480F', '2F8F46', '9775FA'])

lines.linewidth:  2.0
lines.markersize: 5
scatter.marker:   o

font.size:        10
axes.titlesize:   11
axes.labelsize:   10
legend.fontsize:  9
legend.frameon:   False

axes.autolimit_mode: round_numbers
```

- [ ] **Step 2: Escrever os três testes, que devem falhar**

Acrescente ao fim de `tests/test_estrutura.py`:

```python
# Capítulos da abordagem nova. Os de 1 a 5 são da anterior e estão fora destes
# guardas de propósito: as figuras deles não usam estilo nenhum, e entram na
# rodada de reescrita daqueles capítulos.
CAPITULOS_NOVOS = [f"cap{n:02d}" for n in range(6, 18)]

ESTILO = 'plt.style.use("estilo-figuras.mplstyle")'

# Seções sem figura, e por quê. Cada entrada é uma decisão registrada, não um
# esquecimento — daí o dicionário em vez de uma lista.
SECOES_SEM_FIGURA: dict[str, str] = {}

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
```

- [ ] **Step 3: Rodar e ver que passam por vacuidade**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/pytest tests/test_estrutura.py -q
```

Esperado: **passa**. Não há capítulo 6 a 17 ainda, então os três guardas varrem conjunto vazio. Isso é esperado, não é sinal de teste inútil: eles passam a morder na Task 5, e a Task 4 confirma isso.

- [ ] **Step 4: Provar que o estilo produz PNG transparente**

Este é o passo que vale por todos: sem ele o estilo "existe" e não faz o que promete.

```bash
export MPLBACKEND=Agg
.venv/bin/python - <<'EOF'
import matplotlib.pyplot as plt
from PIL import Image
plt.style.use("estilo-figuras.mplstyle")
fig, ax = plt.subplots()
ax.plot([0, 1, 2], [0, 1, 4])
fig.savefig("/tmp/estilo.png")
im = Image.open("/tmp/estilo.png").convert("RGBA")
print("modo:", im.mode, "canto superior esquerdo:", im.getpixel((0, 0)))
EOF
```

Esperado: `modo: RGBA` e o pixel do canto com **alfa 0** — algo como `(0, 0, 0, 0)`. Se o alfa vier 255, `savefig.transparent` não pegou: confira a grafia das quatro chaves de fundo no `.mplstyle` (`figure.facecolor`, `axes.facecolor`, `savefig.facecolor`, `savefig.transparent`).

- [ ] **Step 5: Corrigir a docstring obsoleta de `test_notebooks.py`**

O módulo ainda diz "19 dos chunks executáveis do livro moram dentro de callouts" — número da abordagem anterior; hoje são 2. Troque o parágrafo:

```python
Um chunk que fica de fora é o caso mais traiçoeiro: chunks executáveis moram
**dentro** de callouts, e uma conversão ingênua os transforma em texto. O
notebook continua abrindo, continua executando, e quebra várias células
adiante, num `NameError` que não aponta para a causa.
```

- [ ] **Step 6: Rodar a suíte inteira e commitar**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/pytest tests/ -q
```

Esperado: **47 passed**.

```bash
git add estilo-figuras.mplstyle tests/test_estrutura.py tests/test_notebooks.py
git commit -m "feat(figuras): estilo compartilhado, medido contra os dois temas

O site tem tema claro e escuro, e até aqui não havia estilo de figura
nenhum. O .mplstyle fixa fundo transparente e cores que passam de 3:1
sobre #FFFFFF e sobre #222222 — medido, não estimado. A malha é a
exceção e usa alfa, porque malha a 3:1 competiria com o dado.

Três guardas novos, todos restritos aos capítulos da abordagem nova:
todo chunk que desenha aplica o estilo, toda seção tem figura, e
nenhuma biblioteca de fora da disciplina entra em chunk que executa.
Exceções exigem motivo escrito."
```

---

### Task 3: Os dados do capítulo 6

Dois conjuntos brasileiros, ambos de autoria do próprio professor no livro irmão, mais uma tabelinha de apoio para o `merge`. **Nenhum é baixado em tempo de render** — entram commitados.

A escolha não é de conveniência: `alugueis.csv` traz uma armadilha real e **medida** que é a lição da seção 6.3 — a coluna `andar` vem com `"-"` em 2.461 das 10.692 linhas (23%), o que faz o `pandas` lê-la como texto.

**Files:**
- Create: `dados/estados.csv` (cópia de `../bases_3_estatistica/dados/estados.csv`)
- Create: `dados/alugueis.csv` (cópia de `../bases_3_estatistica/dados/alugueis.csv`)
- Create: `dados/cidades.csv` (escrito à mão nesta task)
- Modify: `dados/README.md` (proveniência dos três)
- Modify: `tests/test_dados.py` (os três entram na varredura)

**Interfaces:**
- Consumes: nada.
- Produces: `dados/estados.csv` com as colunas `Estado, Populacao, Taxa.Homicidios, Sigla` (27 linhas); `dados/alugueis.csv` com `cidade, area_m2, quartos, banheiros, vagas, andar, aceita_animal, mobiliado, condominio, aluguel, iptu, seguro_incendio, total` (10.692 linhas); `dados/cidades.csv` com `cidade, Sigla, regiao` (5 linhas). As tasks 5 a 10 leem esses arquivos.

- [ ] **Step 1: Copiar os dois conjuntos**

```bash
cp ../bases_3_estatistica/dados/estados.csv dados/estados.csv
cp ../bases_3_estatistica/dados/alugueis.csv dados/alugueis.csv
wc -l dados/estados.csv dados/alugueis.csv
```

Esperado: `28` e `10693` (o cabeçalho conta).

- [ ] **Step 2: Escrever a tabela de apoio para o `merge`**

`dados/cidades.csv` existe para a seção 6.5 ter um `merge` honesto: as cinco cidades de `alugueis.csv` ligadas à unidade federativa, o que por sua vez permite juntar com `estados.csv`. Duas cidades em São Paulo tornam o `merge` um muitos-para-um de verdade, não uma correspondência um-a-um disfarçada.

```bash
cat > dados/cidades.csv <<'EOF'
cidade,Sigla,regiao
São Paulo,SP,Sudeste
Campinas,SP,Sudeste
Rio de Janeiro,RJ,Sudeste
Belo Horizonte,MG,Sudeste
Porto Alegre,RS,Sul
EOF
```

- [ ] **Step 3: Conferir que os três casam entre si**

```bash
export MPLBACKEND=Agg
.venv/bin/python - <<'EOF'
import pandas as pd
alu = pd.read_csv("dados/alugueis.csv")
cid = pd.read_csv("dados/cidades.csv")
est = pd.read_csv("dados/estados.csv")
print("alugueis:", alu.shape, "| cidades distintas:", sorted(alu["cidade"].unique()))
print("cidades sem par:", set(alu["cidade"]) - set(cid["cidade"]))
print("siglas sem par:", set(cid["Sigla"]) - set(est["Sigla"]))
print("dtype de andar:", alu["andar"].dtype, "| linhas com '-':", (alu["andar"] == "-").sum())
EOF
```

Esperado, exatamente:

```
alugueis: (10692, 13) | cidades distintas: ['Belo Horizonte', 'Campinas', 'Porto Alegre', 'Rio de Janeiro', 'São Paulo']
cidades sem par: set()
siglas sem par: set()
dtype de andar: object | linhas com '-': 2461
```

Se `cidades sem par` não vier vazio, um nome tem acentuação diferente entre os dois arquivos — corrija `dados/cidades.csv`, nunca `dados/alugueis.csv`.

- [ ] **Step 4: Documentar a proveniência**

Acrescente ao **início** de `dados/README.md`, logo abaixo do título:

```markdown
## `estados.csv` — 27 unidades federativas

População e taxa de homicídios de **2024**.

| Coluna | Fonte |
|---|---|
| `Estado`, `Sigla` | IBGE — [API de localidades](https://servicodados.ibge.gov.br/api/v1/localidades/estados) |
| `Populacao` | IBGE — SIDRA, tabela 6579, variável 9324, ano 2024 |
| `Taxa.Homicidios` | Atlas da Violência (Ipea/FBSP), 2024 — por 100 mil habitantes |

## `alugueis.csv` — 10.692 imóveis para alugar em 5 cidades

São Paulo, Rio de Janeiro, Belo Horizonte, Porto Alegre e Campinas.

Fonte: *Brazilian houses to rent* (v2), publicado no Kaggle por rubenssjr sob
**CC0** (domínio público). Só os nomes das colunas e os dois campos binários
foram traduzidos para o português.

**Nada foi limpo, de propósito.** A coluna `andar` traz `"-"` em 2.461 das
10.692 linhas (23%), o que faz o `pandas` lê-la como `object` em vez de
número — é a armadilha que a seção 6.3 usa para mostrar que a inferência de
tipo é heurística, não garantia. Os outliers também ficaram: há um imóvel de
46.335 m² e um condomínio de R$ 1.117.000.

## `cidades.csv` — as 5 cidades, com UF e região

Escrito à mão. Existe para a seção 6.5 ter um `merge` de verdade: liga
`alugueis.csv` a `estados.csv` pela sigla. São Paulo e Campinas dividem a
mesma UF, então a junção é um muitos-para-um real.
```

- [ ] **Step 5: Pôr os três na varredura de `test_dados.py`**

Em `tests/test_dados.py`, a lista `ESPERADOS` (linhas 8-15) alimenta tanto `test_conjuntos_presentes` quanto `test_dados_README_documenta_cada_conjunto`. Acrescente os três nomes ao fim dela:

```python
ESPERADOS = [
    "stocks.csv",
    "comma_delimited_stock_prices.csv",
    "getting-data.html",
    "iris.data",
    "spam-assuntos.csv",
    "imagem-cores.jpg",
    "estados.csv",
    "alugueis.csv",
    "cidades.csv",
]
```

Depois acrescente este teste ao fim do arquivo:

```python
def test_alugueis_preserva_a_armadilha_do_andar():
    """A seção 6.3 ensina sobre esta linha exata; se ela sumir, a seção mente.

    Alguém "consertando" o CSV — trocando os "-" por vazio, por exemplo — faria
    o pandas ler `andar` como número e a seção passaria a explicar um problema
    que o arquivo já não tem.
    """
    import csv
    with (RAIZ / "dados" / "alugueis.csv").open(encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert len(linhas) == 10692
    assert sum(1 for l in linhas if l["andar"] == "-") == 2461
```

- [ ] **Step 6: Rodar a suíte e commitar**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/pytest tests/ -q
```

Esperado: **48 passed**. Se `test_dados_README_documenta_cada_conjunto` falhar, um dos três nomes não bate com o cabeçalho escrito no README.

```bash
git add dados/ tests/test_dados.py
git commit -m "feat(dados): os três conjuntos brasileiros do capítulo 6

estados.csv e alugueis.csv, e uma tabela de cidades escrita à mão para
o merge da seção 6.5 ligar os dois pela sigla.

O alugueis.csv entra SEM limpeza, de propósito: a coluna andar traz
'-' em 2.461 das 10.692 linhas, e é essa a armadilha que a seção 6.3
usa para mostrar que a inferência de tipo é heurística. Um teste trava
o número, para ninguém 'consertar' o arquivo e a seção passar a
explicar um problema que ele já não tem."
```

---

### Task 4: O capítulo 6 entra no livro

Só agora o capítulo entra no `LIVRO`, e por um motivo: entre esta task e a Task 11 o site publica seis páginas "Em construção". Quanto mais tarde isso começa, menos tempo elas ficam no ar.

**Files:**
- Modify: `scripts/gerar-stubs.py` (a entrada do capítulo 6 no `LIVRO`)
- Modify: `_quarto.yml` (a parte nova, antes de `page-navigation`)
- Modify: `tests/test_estrutura.py` (totais: 6 capítulos, 27 seções, 33 arquivos)
- Modify: `tests/test_notebooks.py` (`test_um_notebook_por_capitulo`: 6)
- Create: `content/cap06/*.qmd` (7 arquivos, gerados)
- Create: `notebooks/cap06-dados-tipos-dados-retangulares-e-pandas.ipynb` (gerado)

**Interfaces:**
- Consumes: o formato do `LIVRO` da Task 1.
- Produces: os sete `.qmd` do capítulo 6, com os nomes exatos que as tasks 5 a 11 preenchem.

- [ ] **Step 1: Acrescentar o capítulo ao `LIVRO`**

Em `scripts/gerar-stubs.py`, acrescente após a entrada do capítulo 5:

```python
    (6, "Dados: Tipos, Dados Retangulares e pandas", None, [
        ("01-elementos-de-dados-estruturados", "Elementos de Dados Estruturados", None),
        ("02-dados-retangulares", "Dados Retangulares", None),
        ("03-lendo-e-tipando-um-arquivo-real", "Lendo e Tipando um Arquivo Real", None),
        ("04-limpando-e-transformando", "Limpando e Transformando", None),
        ("05-agrupando-e-resumindo", "Agrupando e Resumindo", None),
        ("06-da-tabela-para-o-modelo", "Da Tabela para o Modelo", None),
    ]),
```

- [ ] **Step 2: Gerar os stubs**

```bash
.venv/bin/python scripts/gerar-stubs.py
```

Esperado: `criados: 7   pulados (já existiam): 26`.

- [ ] **Step 3: Registrar no `_quarto.yml`**

```bash
.venv/bin/python scripts/gerar-stubs.py --yaml | sed -n '/Capítulo 6:/,$p'
```

Cole a saída no `_quarto.yml`, **imediatamente antes** da linha `  page-navigation: true`, mantendo a indentação de quatro espaços do bloco `chapters`.

- [ ] **Step 4: Atualizar os totais**

Em `tests/test_estrutura.py`:

- renomeie `test_cinco_capitulos` para `test_seis_capitulos` e troque `range(1, 6)` por `range(1, 7)` nele e em `test_cada_capitulo_tem_index`;
- renomeie `test_livro_completo_21_secoes_26_arquivos` para `test_livro_completo_27_secoes_33_arquivos` e troque os três números: `len(livro) == 6`, `total_secoes == 27`, `total_arquivos == 33`.

Em `tests/test_notebooks.py`, troque `assert len(esperados) == 5` por `assert len(esperados) == 6` e ajuste o comentário acima dele.

- [ ] **Step 5: Gerar o notebook e rodar a suíte**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/gerar-notebooks.py
.venv/bin/pytest tests/ -q
```

Esperado: 6 notebooks listados, e **48 passed**.

**`test_toda_secao_tem_figura` VAI falhar neste passo, e isso é o correto:** os stubs não têm chunk nenhum, então as seis seções aparecem como "sem figura". É exatamente o que o teste existe para acusar.

Registre as seis em `SECOES_SEM_FIGURA`, em `tests/test_estrutura.py`:

```python
SECOES_SEM_FIGURA: dict[str, str] = {
    "cap06/01-elementos-de-dados-estruturados.qmd": "stub; a figura entra quando a seção for escrita",
    "cap06/02-dados-retangulares.qmd": "stub; a figura entra quando a seção for escrita",
    "cap06/03-lendo-e-tipando-um-arquivo-real.qmd": "stub; a figura entra quando a seção for escrita",
    "cap06/04-limpando-e-transformando.qmd": "stub; a figura entra quando a seção for escrita",
    "cap06/05-agrupando-e-resumindo.qmd": "stub; a figura entra quando a seção for escrita",
    "cap06/06-da-tabela-para-o-modelo.qmd": "stub; a figura entra quando a seção for escrita",
}
```

**Cada task de seção remove a sua entrada** ao escrever a seção, e a Task 11 confere que o dicionário voltou a ficar vazio. Rode a suíte de novo depois de registrar; aí sim deve passar.

- [ ] **Step 6: Commit**

```bash
git add scripts/gerar-stubs.py _quarto.yml content/cap06 notebooks tests/
git commit -m "feat(cap06): o capítulo entra no livro, ainda em stubs

Seis seções registradas no _quarto.yml e no LIVRO, notebook gerado, e
os totais da suíte em 6 capítulos / 27 seções / 33 arquivos.

As seis entram em SECOES_SEM_FIGURA como stub; cada seção remove a sua
ao ser escrita, e a task final confere que o dicionário esvaziou."
```

---

### Tasks 5 a 10: as seis seções

As seis seguem a **mesma forma**, e é a forma que este capítulo fixa para o material inteiro — ele é escrito primeiro justamente para virar o modelo de estilo, o papel que o capítulo 9 tinha na abordagem anterior.

**A forma de uma seção:**

1. `# Título` na primeira linha.
2. **Sem callout de correspondência** — o capítulo 6 não tem seção equivalente no ISLP. (Do capítulo 7 em diante, o callout vem aqui.)
3. Um parágrafo de abertura que **liga à seção anterior** e diz o que esta resolve. Nada de "nesta seção veremos".
4. Um chunk de setup, sempre com `#| include: false`, que importa e aplica o estilo:

```python
#| label: setup
#| include: false
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use("estilo-figuras.mplstyle")
pd.set_option("display.max_columns", None)
```

5. O conteúdo em `##`, alternando prosa curta e chunk que executa. Todo número afirmado na prosa **sai da saída do chunk**, nunca da cabeça.
6. **Ao menos uma figura** que carrega a ideia.
7. Callouts `::: {.conceito}` (azul) para o que precisa ficar, `::: {.exemplo}` (verde) para o caso concreto.

**Verificação, idêntica nas seis** (é o "rodar o teste" deste projeto):

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/executar-secoes.py 06
.venv/bin/python scripts/gerar-notebooks.py
.venv/bin/pytest tests/ -q
```

Esperado: `todas as seções executaram até o fim, cada uma no seu kernel.` e **48 passed**. `executar-secoes.py` roda cada `.qmd` num kernel **próprio**, com o cwd na raiz — é o análogo fiel do `quarto render`, e é ele que pega o `import` que faltou porque foi feito na seção anterior.

Cada task termina com: remover a entrada da seção em `SECOES_SEM_FIGURA`, rodar a verificação, e commitar `content/cap06/<arquivo>.qmd`, `notebooks/cap06-*.ipynb` e `tests/test_estrutura.py`.

---

### Task 5: Seção 6.1 — Elementos de Dados Estruturados

**Files:**
- Modify: `content/cap06/01-elementos-de-dados-estruturados.qmd`
- Modify: `tests/test_estrutura.py` (remover a entrada de `SECOES_SEM_FIGURA`)

**Interfaces:**
- Consumes: `dados/estados.csv` (Task 3), `estilo-figuras.mplstyle` (Task 2).
- Produces: o vocabulário *numérico contínuo / discreto*, *categórico nominal / ordinal / binário* e o `dtype` `category`, que as seções 6.3, 6.5 e 6.6 usam sem reapresentar.

- [ ] **Step 1: Escrever a seção**

Conteúdo obrigatório, nesta ordem:

- **A taxonomia.** Numérico: contínuo (qualquer valor num intervalo) e discreto (inteiro, tipicamente contagem). Categórico: nominal (sem ordem), ordinal (com ordem, sem distância) e binário (dois valores).
- **Por que a distinção importa**, em uma frase forte: o tipo decide qual gráfico faz sentido, qual estatística pode ser calculada e como o software valida. Tratar ordinal como numérico produz conclusão errada com aparência de rigor.
- **O que o `pandas` infere sozinho** — `pd.read_csv("dados/estados.csv")` e `.dtypes`. `Populacao` vira `int64` (contagem, discreto), `Taxa.Homicidios` vira `float64` (taxa, contínuo), e `Estado` e `Sigla` viram `object`: texto genérico. O `pandas` **não** sabe que são categóricos nominais.
- **Declarando o categórico** — `estado["Sigla"] = estado["Sigla"].astype("category")` e `.cat.categories`. O ganho aqui é **semântico**, não de memória: as 27 siglas são todas distintas, não há string repetida para deduplicar. A economia de memória aparece quando poucos valores se repetem em muitas linhas — e a seção 6.3 mostra exatamente esse caso com `cidade`, cinco valores em 10.692 linhas.
- **Ordinal** — construa uma faixa de população com `pd.cut` e `ordered=True`, mostrando que `<` funciona entre categorias ordenadas e não funciona entre nominais.

**A figura:** dois painéis lado a lado sobre `estados.csv` — barras horizontais das 10 maiores populações (a forma que serve a um categórico com um número) e um histograma de `Taxa.Homicidios` (a forma que serve a um contínuo). A legenda diz o que a figura ensina: **o tipo escolhe o gráfico**.

- [ ] **Step 2: Verificar**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/executar-secoes.py 06
```

Esperado: `todas as seções executaram até o fim, cada uma no seu kernel.`

- [ ] **Step 3: Conferir os números afirmados na prosa**

Toda contagem que o texto disser precisa vir da saída. Confira:

```bash
.venv/bin/python -c "
import pandas as pd
e = pd.read_csv('dados/estados.csv')
print(e.dtypes.to_string())
print('linhas:', len(e), '| siglas distintas:', e['Sigla'].nunique())
"
```

Esperado: `Populacao int64`, `Taxa.Homicidios float64`, `Estado object`, `Sigla object`; `linhas: 27 | siglas distintas: 27`.

- [ ] **Step 4: Remover a exceção, regerar o notebook e rodar a suíte**

Tire `"cap06/01-elementos-de-dados-estruturados.qmd"` de `SECOES_SEM_FIGURA`.

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/gerar-notebooks.py
.venv/bin/pytest tests/ -q
```

Esperado: **48 passed**. Se `test_toda_secao_tem_figura` acusar esta seção, o chunk da figura tem `#| eval: false` ou não chama `plt.`.

- [ ] **Step 5: Commit**

```bash
git add content/cap06/01-elementos-de-dados-estruturados.qmd notebooks tests/test_estrutura.py
git commit -m "feat(cap06): 6.1 — elementos de dados estruturados

A taxonomia numérico/categórico, o que o pandas infere sozinho e o que
ele não tem como saber, e o astype('category'). A figura mostra que o
tipo escolhe o gráfico: barras para o categórico, histograma para o
contínuo."
```

---

### Task 6: Seção 6.2 — Dados Retangulares

**Files:**
- Modify: `content/cap06/02-dados-retangulares.qmd`
- Modify: `tests/test_estrutura.py`

**Interfaces:**
- Consumes: `dados/estados.csv`, o vocabulário da 6.1.
- Produces: `shape`, `info`, o índice, `.loc` e `.iloc`, e a distinção `Series` × `DataFrame` — usados sem reapresentação de 6.3 em diante.

- [ ] **Step 1: Escrever a seção**

Conteúdo obrigatório:

- **A forma retangular é uma escolha, não uma lei**: linhas são registros, colunas são variáveis. `(27, 4)` só significa alguma coisa porque sabemos que cada linha é uma unidade federativa. Trocar as duas dimensões descreveria os mesmos números sem descrever o mesmo problema.
- `shape`, `head()`, `info()` — e o que o `info()` acrescenta ao `head()`: quantos não nulos por coluna e quanta memória.
- **O índice.** Por padrão é a posição: 0, 1, 2. `set_index("Sigla")` transforma `.loc["SP"]` de busca por posição em busca por rótulo — algo que a posição sozinha nunca permitiria com sentido.
- **`.loc` contra `.iloc`**, com o mesmo dado, mostrando que `.iloc[0]` continua sendo a primeira linha depois de mudar o índice, e `.loc["SP"]` não.
- **`Series` contra `DataFrame`:** `df["Populacao"]` devolve uma `Series` (uma coluna, com índice) e `df[["Populacao"]]` devolve um `DataFrame` de uma coluna. Confunde todo mundo uma vez, e a diferença aparece de novo na 6.6.

**A figura:** dispersão de `Populacao` (eixo x, escala log) contra `Taxa.Homicidios` (eixo y), com quatro ou cinco estados rotulados por `annotate`. Ela ensina o que a tabela não mostra — que não há relação óbvia entre tamanho e violência — e prepara a 6.5.

- [ ] **Step 2: Verificar e conferir os números**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/executar-secoes.py 06
.venv/bin/python -c "
import pandas as pd
e = pd.read_csv('dados/estados.csv')
print('shape:', e.shape)
print(e.set_index('Sigla').loc['SP'].to_string())
"
```

Esperado: `shape: (27, 4)` e a linha de São Paulo. Todo número da prosa sai daqui.

- [ ] **Step 3: Remover a exceção, regerar e rodar**

Tire `"cap06/02-dados-retangulares.qmd"` de `SECOES_SEM_FIGURA`.

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/gerar-notebooks.py && .venv/bin/pytest tests/ -q
```

Esperado: **48 passed**.

- [ ] **Step 4: Commit**

```bash
git add content/cap06/02-dados-retangulares.qmd notebooks tests/test_estrutura.py
git commit -m "feat(cap06): 6.2 — dados retangulares

Linhas são registros, colunas são variáveis, e o par (27, 4) só
significa algo porque sabemos o que é cada linha. O índice, .loc contra
.iloc, e a diferença entre Series e DataFrame, que volta na 6.6."
```

---

### Task 7: Seção 6.3 — Lendo e Tipando um Arquivo Real

**A seção mais importante do capítulo.** É onde o aluno vê que a inferência de tipo do `pandas` é heurística, não garantia — com um arquivo em que isso acontece de verdade.

**Files:**
- Modify: `content/cap06/03-lendo-e-tipando-um-arquivo-real.qmd`
- Modify: `tests/test_estrutura.py`

**Interfaces:**
- Consumes: `dados/alugueis.csv`, o vocabulário da 6.1 e da 6.2.
- Produces: `na_values`, `to_numeric(errors=...)` e a coluna `andar` já tipada — a 6.4 continua daí.

- [ ] **Step 1: Escrever a seção**

Conteúdo obrigatório, e a ordem importa porque é uma narrativa de descoberta:

1. `pd.read_csv("dados/alugueis.csv")`, `shape` → `(10692, 13)`, `head()`.
2. `dtypes` — e a surpresa: **`andar` veio como `object`**, no meio de doze colunas que o `pandas` tipou certo.
3. **Mostrar o estrago antes de explicar.** `alugueis["andar"].mean()` levanta `TypeError`. Capture e imprima **truncado**:

```python
try:
    alugueis["andar"].mean()
except TypeError as erro:
    print("TypeError:", str(erro)[:90], "...")
```

**Não use `#| error: true`.** Duas razões, as duas medidas: `scripts/executar-secoes.py:80` e `scripts/executar-notebooks.py:40` constroem o `NotebookClient` **sem** `allow_errors`, e `scripts/gerar-notebooks.py` só entende a opção `eval` — uma célula que levanta exceção mata a verificação e o `make notebooks-teste`. E a mensagem real do `TypeError` traz a coluna inteira concatenada: cerca de **8.000 caracteres** de lixo, que iriam parar na página publicada. O truncamento não é economia de espaço — é o que torna o erro legível.
4. **Descobrir a causa:** `alugueis["andar"].unique()[:10]` mostra o `"-"`. `(alugueis["andar"] == "-").sum()` dá **2.461**, que é **23%** das linhas.
5. **Por que o `pandas` não pegou:** ele tem uma lista padrão de marcadores nulos (`NA`, `NaN`, `null`, `n/a`, campo vazio...) e `"-"` não está nela. Uma coluna com um único valor não numérico vira `object` inteira.
6. **Os dois consertos**, e quando usar cada um:
   - `pd.read_csv(..., na_values=["-"])` — quando você **sabe** qual é o marcador. Resultado: `float64`, 2.461 nulos, média **6,58**.
   - `pd.to_numeric(alugueis["andar"], errors="coerce")` — quando você não sabe, e quer que tudo que não for número vire nulo. Mais forte e mais perigoso: converte em silêncio o que talvez você quisesse ver.
7. **A lição, num `::: {.conceito}`:** a inferência de tipo é uma heurística sobre os caracteres do arquivo, não um contrato. Confira `dtypes` sempre, logo depois de ler.
8. Uma nota curta: `cidade` tem cinco valores distintos em 10.692 linhas — **aqui** `astype("category")` economiza memória de verdade, ao contrário do caso da 6.1. Mostre o antes e o depois com `memory_usage(deep=True)`.

**A figura:** histograma de `aluguel`, que revela a cauda longa e o outlier. Ela não é ilustração: é o que motiva a 6.4.

- [ ] **Step 2: Verificar, e conferir cada número da prosa**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/executar-secoes.py 06
.venv/bin/python - <<'EOF'
import pandas as pd
a = pd.read_csv("dados/alugueis.csv")
print("shape:", a.shape, "| dtype andar:", a["andar"].dtype)
print("linhas com '-':", (a["andar"] == "-").sum(),
      "| %.0f%%" % (100 * (a["andar"] == "-").mean()))
b = pd.read_csv("dados/alugueis.csv", na_values=["-"])
print("com na_values:", b["andar"].dtype, "| nulos:", b["andar"].isna().sum(),
      "| média: %.2f" % b["andar"].mean())
print("memória cidade object:", a["cidade"].memory_usage(deep=True),
      "| category:", a["cidade"].astype("category").memory_usage(deep=True))
EOF
```

Esperado: `(10692, 13)`, `object`, `2461`, `23%`, `float64`, `2461` nulos, média `6.58`. **Se algum número da prosa não bater com esta saída, a prosa está errada, não o dado.**

- [ ] **Step 3: Confirmar que nenhuma célula levanta exceção**

`executar-secoes.py` aborta na primeira exceção não capturada — é o principal valor dele. Se o Step 2 falhar com `TypeError`, o `try/except` do item 3 não foi escrito ou não envolve a chamada certa.

- [ ] **Step 4: Remover a exceção, regerar e rodar**

Tire `"cap06/03-lendo-e-tipando-um-arquivo-real.qmd"` de `SECOES_SEM_FIGURA`.

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/gerar-notebooks.py && .venv/bin/pytest tests/ -q
```

Esperado: **48 passed**.

- [ ] **Step 5: Commit**

```bash
git add content/cap06/03-lendo-e-tipando-um-arquivo-real.qmd notebooks tests/test_estrutura.py
git commit -m "feat(cap06): 6.3 — lendo e tipando um arquivo real

A coluna andar vem como object porque 2.461 das 10.692 linhas trazem
'-', que não está na lista padrão de marcadores nulos do pandas. A
seção mostra o TypeError primeiro, descobre a causa depois, e só então
apresenta na_values e to_numeric — porque a inferência de tipo é
heurística sobre caracteres, não contrato."
```

---

### Task 8: Seção 6.4 — Limpando e Transformando

**Files:**
- Modify: `content/cap06/04-limpando-e-transformando.qmd`
- Modify: `tests/test_estrutura.py`

**Interfaces:**
- Consumes: `dados/alugueis.csv` lido com `na_values=["-"]` (idioma da 6.3).
- Produces: a coluna derivada `aluguel_por_m2`, usada na 6.5.

- [ ] **Step 1: Escrever a seção**

Conteúdo obrigatório:

- **Onde estão os nulos:** `alugueis.isna().sum()`. Depois da 6.3 só `andar` tem nulos, e são os 2.461.
- **Nulo não é uma coisa só.** Aqui `andar` nulo não é "o dado faltou": é "o imóvel é casa e não tem andar". `dropna()` jogaria fora 23% da tabela por uma informação que não estava faltando. **Preencher com 0 é decisão de modelagem, e o texto diz por quê** — 0 significa térreo, que é o que uma casa é.
- `fillna(0)` contra `dropna()`, com o `shape` dos dois lado a lado, para o custo ficar visível.
- **Duplicatas:** `duplicated().sum()`. Discuta o que uma linha repetida significa aqui — dois anúncios idênticos podem ser o mesmo imóvel ou dois imóveis iguais no mesmo prédio, e o dado não distingue. Não decidir é uma decisão.
- **Outliers:** `alugueis["area_m2"].max()` → 46.335 m²; `alugueis["condominio"].max()` → 1.117.000. `describe()` mostra a distância entre mediana e máximo. **Não remova** — mostre, e diga que a 6.5 vai preferir a mediana justamente por isso.
- **Coluna derivada:** `alugueis["aluguel_por_m2"] = alugueis["aluguel"] / alugueis["area_m2"]`. Uma linha, e ela cria a variável que a 6.5 compara entre cidades.

**A figura:** barras horizontais com a contagem de nulos por coluna, ou — melhor — um par de boxplots de `area_m2`, um com todos os dados e outro com o eixo cortado no percentil 99, mostrando o que o outlier faz com a escala.

- [ ] **Step 2: Verificar e conferir os números**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/executar-secoes.py 06
.venv/bin/python - <<'EOF'
import pandas as pd
a = pd.read_csv("dados/alugueis.csv", na_values=["-"])
print("nulos por coluna:\n", a.isna().sum()[lambda s: s > 0].to_string())
print("duplicadas:", a.duplicated().sum())
print("area max:", a["area_m2"].max(), "| condominio max:", a["condominio"].max())
print("shape com dropna:", a.dropna().shape, "| original:", a.shape)
EOF
```

Todo número da prosa sai desta saída.

- [ ] **Step 3: Remover a exceção, regerar e rodar**

Tire `"cap06/04-limpando-e-transformando.qmd"` de `SECOES_SEM_FIGURA`.

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/gerar-notebooks.py && .venv/bin/pytest tests/ -q
```

Esperado: **48 passed**.

- [ ] **Step 4: Commit**

```bash
git add content/cap06/04-limpando-e-transformando.qmd notebooks tests/test_estrutura.py
git commit -m "feat(cap06): 6.4 — limpando e transformando

Nulo não é uma coisa só: andar nulo aqui é casa sem andar, não dado
faltando, e dropna() jogaria 23% da tabela fora por uma informação que
não estava ausente. Os outliers ficam à vista, sem remoção, porque são
o motivo de a 6.5 preferir a mediana."
```

---

### Task 9: Seção 6.5 — Agrupando e Resumindo

**Files:**
- Modify: `content/cap06/05-agrupando-e-resumindo.qmd`
- Modify: `tests/test_estrutura.py`

**Interfaces:**
- Consumes: `dados/alugueis.csv`, `dados/cidades.csv`, `dados/estados.csv`, e `aluguel_por_m2` da 6.4.
- Produces: `groupby`, `agg`, `value_counts` e `merge`.

- [ ] **Step 1: Escrever a seção**

Conteúdo obrigatório:

- `describe()` sobre as colunas numéricas, e `value_counts()` sobre `cidade` — o resumo de um contínuo e o de um categórico são coisas diferentes, o que retoma a 6.1.
- **`groupby`:** `alugueis.groupby("cidade")["aluguel"].median()`. **Mediana, não média**, e o texto diz por quê, apontando para os outliers da 6.4. Mostre as duas lado a lado para a diferença ficar visível.
- **`agg` com várias funções e várias colunas**, produzindo a tabela de resultado do capítulo: por cidade, a contagem, a mediana do aluguel e a mediana de `aluguel_por_m2`.
- **`merge`:** juntar com `dados/cidades.csv` pela coluna `cidade` traz `Sigla` e `regiao`; juntar o resultado com `dados/estados.csv` pela `Sigla` traz `Populacao`. Dois `merge` encadeados, e é aqui que São Paulo e Campinas dividirem a mesma UF mostra o que é um muitos-para-um.
- **Um aviso que vale a seção inteira:** confira o `shape` antes e depois de todo `merge`. Um `merge` que multiplica linhas é o erro silencioso mais comum em trabalho com dados, e o único jeito de vê-lo é olhar.

**A figura:** barras horizontais da mediana de `aluguel_por_m2` por cidade, ordenadas. Uma frase, um gráfico: onde o metro quadrado é caro.

- [ ] **Step 2: Verificar e conferir os números**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/executar-secoes.py 06
.venv/bin/python - <<'EOF'
import pandas as pd
a = pd.read_csv("dados/alugueis.csv", na_values=["-"])
a["aluguel_por_m2"] = a["aluguel"] / a["area_m2"]
print(a.groupby("cidade")["aluguel"].agg(["count", "median", "mean"]).to_string())
m = a.merge(pd.read_csv("dados/cidades.csv"), on="cidade")
print("shape antes:", a.shape, "-> depois do merge:", m.shape)
EOF
```

**O `shape` depois do `merge` precisa ter as mesmas 10.692 linhas.** Se crescer, `dados/cidades.csv` tem cidade repetida.

- [ ] **Step 3: Remover a exceção, regerar e rodar**

Tire `"cap06/05-agrupando-e-resumindo.qmd"` de `SECOES_SEM_FIGURA`.

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/gerar-notebooks.py && .venv/bin/pytest tests/ -q
```

Esperado: **48 passed**.

- [ ] **Step 4: Commit**

```bash
git add content/cap06/05-agrupando-e-resumindo.qmd notebooks tests/test_estrutura.py
git commit -m "feat(cap06): 6.5 — agrupando e resumindo

groupby com mediana, e o texto diz por que não é média: os outliers da
6.4. Dois merge encadeados ligam aluguéis a cidades e cidades a
estados, e a seção cobra conferir o shape antes e depois — merge que
multiplica linha é o erro silencioso mais comum deste trabalho."
```

---

### Task 10: Seção 6.6 — Da Tabela para o Modelo

Fecha o capítulo montando `X` e `y`. **Não ajusta modelo nenhum** — isso é o próximo capítulo.

**Files:**
- Modify: `content/cap06/06-da-tabela-para-o-modelo.qmd`
- Modify: `tests/test_estrutura.py`

**Interfaces:**
- Consumes: tudo do capítulo.
- Produces: a convenção `X` (preditores) e `y` (alvo), que todo capítulo seguinte usa.

- [ ] **Step 1: Escrever a seção**

Conteúdo obrigatório:

- **A pergunta primeiro, a tabela depois.** "Quanto deveria custar o aluguel deste imóvel?" é o que decide qual coluna é `y` (`aluguel`) e quais são `X`.
- **`y` é uma `Series`, `X` é um `DataFrame`** — a distinção da 6.2 volta com consequência: `y = alugueis["aluguel"]`, `X = alugueis[["area_m2", "quartos", "banheiros", "vagas"]]`.
- **O modelo não sabe o que é "cidade".** Ele vê números. Uma coluna de texto precisa virar número, e a tradução ingênua — São Paulo=1, Rio=2, Campinas=3 — **inventa uma ordem e uma distância que não existem**, dizendo que Campinas está o dobro de longe de São Paulo que o Rio está. Mostre `pd.get_dummies(alugueis["cidade"])`: cinco colunas de 0 e 1, sem ordem inventada.
- **Uma coluna que não pode entrar.** `total` é a soma de `aluguel`, `condominio`, `iptu` e `seguro_incendio` — deixá-la em `X` entrega a resposta ao modelo. Confirme com uma linha (`(a["aluguel"] + a["condominio"] + a["iptu"] + a["seguro_incendio"] - a["total"]).abs().max()`) e nomeie o problema: **vazamento**. Não o desenvolva aqui — o capítulo 17 é sobre isso.
- `X.shape` e `y.shape` fecham o capítulo. Uma frase de ligação para o que vem: já há uma tabela pronta para um modelo; falta saber o que um modelo é, e como saber se ele presta.

**A figura:** matriz de correlação das colunas numéricas de `X` mais `y`, como mapa de calor com os valores anotados. Ela mostra quais preditores andam juntos — e, se `total` for incluída na figura de propósito, mostra visualmente o vazamento: correlação quase 1 com o alvo.

- [ ] **Step 2: Verificar e conferir os números**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/executar-secoes.py 06
.venv/bin/python - <<'EOF'
import pandas as pd
a = pd.read_csv("dados/alugueis.csv", na_values=["-"])
print("total é a soma? erro máximo:",
      (a["aluguel"] + a["condominio"] + a["iptu"] + a["seguro_incendio"] - a["total"]).abs().max())
X = a[["area_m2", "quartos", "banheiros", "vagas"]]
y = a["aluguel"]
print("X:", X.shape, "| y:", y.shape)
print("colunas de get_dummies(cidade):", list(pd.get_dummies(a["cidade"]).columns))
print("corr(total, aluguel): %.3f" % a["total"].corr(a["aluguel"]))
EOF
```

Se o erro máximo **não** for 0 (ou muito próximo), a afirmação sobre `total` está errada e a prosa precisa mudar — descreva o que a saída realmente mostra.

- [ ] **Step 3: Remover a exceção, regerar e rodar**

Tire `"cap06/06-da-tabela-para-o-modelo.qmd"` de `SECOES_SEM_FIGURA`.

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/gerar-notebooks.py && .venv/bin/pytest tests/ -q
```

Esperado: **48 passed**.

- [ ] **Step 4: Commit**

```bash
git add content/cap06/06-da-tabela-para-o-modelo.qmd notebooks tests/test_estrutura.py
git commit -m "feat(cap06): 6.6 — da tabela para o modelo

X e y, e por que o modelo não sabe o que é 'cidade': traduzir texto em
1, 2, 3 inventa uma ordem e uma distância que não existem. A coluna
total sai de X porque é a soma que contém a resposta — o nome do
problema é dado, o desenvolvimento fica para o capítulo 17."
```

---

### Task 11: O `index.qmd`, o link do Colab e o render

**Files:**
- Modify: `content/cap06/index.qmd`
- Modify: `tests/test_estrutura.py` (confirmar que `SECOES_SEM_FIGURA` esvaziou)

**Interfaces:**
- Consumes: as seis seções escritas.
- Produces: a página de abertura do capítulo, e o link do Colab que `test_todo_capitulo_tem_link_para_o_colab_e_nenhum_notebook_o_repete` cobra.

- [ ] **Step 1: Escrever o `index.qmd`**

Copie a estrutura de `content/cap05/index.qmd` — é o índice mais recente e traz o link do Colab e a tabela de seções no formato certo. O deste capítulo tem:

1. `# Dados: Tipos, Dados Retangulares e pandas`
2. **Sem callout de correspondência** (não há capítulo equivalente no ISLP).
3. O link do Colab, **em linha própria**, apontando para `https://colab.research.google.com/github/BragaD/UnDF-Bases5-CienciaDeDados-202602/blob/main/notebooks/cap06-dados-tipos-dados-retangulares-e-pandas.ipynb`. Confirme o nome exato do arquivo com `ls notebooks/`.
4. Dois ou três parágrafos de visão geral: o que o capítulo entrega e por que ele vem antes de qualquer modelo. A ideia central a transmitir — **a tabela é a mesa de trabalho, e quase todo erro de análise nasce antes do modelo, na hora de ler e tipar o dado**.
5. A tabela de seções, no formato `| [6.1](01-elementos-de-dados-estruturados.qmd) | Elementos de Dados Estruturados |`.
6. `## Leituras adicionais` com dois ou três ponteiros reais: a documentação do `pandas` (*10 minutes to pandas*, *Working with missing data*) e o *Data Wrangling* cheat sheet. Links reais, conferidos.

- [ ] **Step 2: Fazer o gerador de stubs emitir o link do Colab**

`test_todo_capitulo_tem_link_para_o_colab_e_nenhum_notebook_o_repete` exige que **todo** capítulo registrado tenha o link do Colab no seu `index.qmd`, e `stub_index` não o emite. A Task 4 descobriu isso na prática e resolveu à mão, para o capítulo 6. Sem esta correção, **cada um dos capítulos 7 a 17 vai bater na mesma parede**.

Em `scripts/gerar-stubs.py`, dentro de `stub_index`, acrescente a linha do Colab logo após o título (e após o callout de correspondência, quando houver). O formato exato está nos `index.qmd` dos capítulos 1 a 5 — copie de lá, trocando só o nome do notebook, que é `cap{nosso:02d}-{apelido(titulo)}.ipynb`. A função `apelido` vive em `scripts/gerar-notebooks.py`; importe-a por caminho, como `tests/test_notebooks.py` já faz com `carregar_gerador`, em vez de duplicar a tabela de acentos.

Confirme que o gerador continua idempotente:

```bash
.venv/bin/python scripts/gerar-stubs.py
```

Esperado: `criados: 0   pulados (já existiam): 33`.

- [ ] **Step 3: Conferir que o dicionário de exceções esvaziou**

```bash
grep -A2 "SECOES_SEM_FIGURA: dict" tests/test_estrutura.py
```

Esperado: `SECOES_SEM_FIGURA: dict[str, str] = {}`. Se ainda houver entrada, uma seção ficou sem figura.

- [ ] **Step 4: Rodar tudo, inclusive o capítulo num kernel só**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/gerar-notebooks.py
.venv/bin/python scripts/executar-secoes.py 06
.venv/bin/python scripts/executar-notebooks.py cap06
.venv/bin/pytest tests/ -q
```

Os dois modos são complementares: `executar-secoes.py` reproduz o **site** (um kernel por página) e `executar-notebooks.py` reproduz a **aula** (um kernel por capítulo). Esperado: os dois OK e **48 passed**.

- [ ] **Step 5: O render completo — a única vez neste plano**

```bash
make render
```

Se abortar com `ERROR: Directory not empty`, **não faça nada**: o alvo repete até seis vezes sozinho e imprime `render OK (tentativa N)`. Se sair com código 75 e `NÃO RENDERIZOU`, outro agente está renderizando — rode de novo. **Nunca** `make clean`.

Se o Docker não estiver no ar, o Quarto do host serve para conferir o conteúdo:

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0 PATH="$PWD/.venv/bin:$PATH"
quarto render 2>&1 | grep -E "Unable to resolve|ERROR|Output created"
```

Esperado: **só** `Output created: _book/index.html`. Qualquer `Unable to resolve link target` é link quebrado e precisa ser corrigido antes do commit — `test_todo_link_interno_para_qmd_resolve` existe para isso, mas o render pega também os links para recursos.

- [ ] **Step 6: Abrir a página no tema escuro**

O estilo de figura foi feito para os dois temas, e este é o único momento em que isso é conferido de fato. Abra `_book/content/cap06/01-elementos-de-dados-estruturados.html`, troque para o tema escuro no seletor do topo e confirme que os eixos, os rótulos e as barras continuam legíveis. Se alguma figura aparecer como um retângulo branco, o `savefig.transparent` não pegou naquele chunk.

- [ ] **Step 7: Commit**

```bash
git add content/cap06/index.qmd scripts/gerar-stubs.py notebooks tests/test_estrutura.py
git commit -m "feat(cap06): a visão geral, o link do Colab e o render

Fecha o capítulo 6. A tabela é a mesa de trabalho, e quase todo erro de
análise nasce antes do modelo — na hora de ler e tipar o dado.

Render limpo, sem aviso de link, e as figuras conferidas nos dois temas."
```

---

### Task 12: O `CLAUDE.md` alcança a realidade

O `CLAUDE.md` foi escrito quando as fontes ainda não tinham sido escolhidas, e hoje **mente sobre o estado do repositório** — um implementador da Task 5 o sinalizou depois de encontrar a divergência sozinho. Ele afirma cinco capítulos, 26 `.qmd` e 43 testes, e diz que nenhum capítulo novo deve ser escrito antes de as fontes serem definidas. As fontes foram definidas, e o capítulo 6 existe.

Isto é a última task porque só aqui os números finais são conhecidos.

**Files:**
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: o estado final do repositório, depois da Task 11.
- Produces: nada que outra task consuma.

- [ ] **Step 1: Medir o estado real, sem estimar**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
echo "capítulos: $(ls -d content/cap* | wc -l)"
echo "qmd: $(find content -name '*.qmd' | wc -l)"
echo "seções: $(find content -name '*.qmd' ! -name index.qmd | wc -l)"
echo "notebooks: $(ls notebooks/*.ipynb | wc -l)"
.venv/bin/pytest tests/ -q 2>&1 | tail -1
```

Use **esses** números no texto, não os do plano.

- [ ] **Step 2: Reescrever a seção "Estado atual"**

Ela precisa dizer: que a fonte é o ISLP (`@james2023`, PDF em `livros/`), com a spec `docs/superpowers/specs/2026-09-10-estrutura-nova-islp-design.md` mandando; que o capítulo 6 está escrito e é o **modelo de estilo da casa** — quem for escrever o capítulo 7 lê `content/cap06/` inteiro antes; que os capítulos 1 a 5 são de abordagem anterior, continuam citando o Grus e estão fora dos guardas novos; e quais capítulos faltam, com a ementa da spec.

**Apague** a seção "Nenhum capítulo novo antes das fontes" — ela cumpriu a função.

- [ ] **Step 3: Acrescentar a pedagogia nova**

Uma seção curta com: a tese (*o modelo é uma ferramenta que se escolhe, se ajusta e se julga*), `scikit-learn` de ponta a ponta sem nada à mão, nada de inferência, a tabela do que é proibido em chunk executável (`statsmodels`, `torch`, o pacote `ISLP`, `scipy` fora da exceção), a regra de citação com número de seção do ISLP, e a regra da figura obrigatória com `estilo-figuras.mplstyle`.

- [ ] **Step 4: Corrigir os números espalhados pelo arquivo**

Busque e atualize todas as ocorrências: a contagem de testes, a de capítulos, seções e arquivos, a lista de arquivos de teste (que ganhou guardas novos), e a menção a `make notebooks-teste`.

```bash
grep -nE "43 testes|26 \`|21 seções|Cinco capítulos|5 capítulos" CLAUDE.md
```

Esperado ao fim: nenhuma linha.

- [ ] **Step 5: Rodar a suíte e commitar**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/pytest tests/ -q
```

```bash
git add CLAUDE.md
git commit -m "docs: o CLAUDE.md alcança a realidade

Ele foi escrito antes de as fontes serem escolhidas e afirmava cinco
capítulos, 26 .qmd e 43 testes, mandando não escrever capítulo novo. As
fontes foram escolhidas, o capítulo 6 existe, e os números eram outros.

Entra a tese nova, a lista do que é proibido em chunk executável, a
regra de citação com número de seção do ISLP e a da figura obrigatória.
O capítulo 6 passa a ser o modelo de estilo da casa."
```

---

## O que vem depois deste plano

Os capítulos 7 a 17 **não** entram aqui. Cada um ganha o seu próprio plano em `docs/superpowers/plans/2026-09-10-islp-capNN.md`, escrito quando chegar a vez, no processo que as reescritas anteriores fixaram: um planejador com o mapa do capítulo no prompt, um implementador, um revisor que lê o capítulo inteiro com uma pergunta só — *o texto condiz com o que foi escrito?* — e o implementador corrigindo. **Um capítulo por vez**, sequencial; despachar todos em paralelo já estourou o limite de sessão da API sem produzir nada.

Três coisas que a fundação deixou de propósito para o plano do capítulo 7, porque só lá passam a ser necessárias:

- **`test_toda_secao_cita_o_islp`** — o capítulo 6 não cita, então o teste não teria o que travar ainda.
- **Os conjuntos de dados do ISLP.** As URLs foram conferidas nesta sessão e valem registrar: `Advertising`, `Auto`, `Credit`, `Heart`, `College` e `Income1` estão em `https://www.statlearning.com/s/<Nome>.csv`; `Carseats`, `Default`, `Smarket`, `Hitters`, `Wage`, `OJ`, `Caravan`, `NCI60data.npy` e `NCI60labs.csv` estão em `https://raw.githubusercontent.com/intro-stat-learning/ISLP/main/ISLP/data/<Nome>`; `USArrests` **não** está em nenhum dos dois e sai de `https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/USArrests.csv`. O California Housing, que substitui o `Boston`, sai de `sklearn.datasets.fetch_california_housing()` rodado uma vez e salvo como CSV.
- **`scipy` declarado no `pyproject.toml`** — só o capítulo 15 precisa, e declará-lo exige `make lock` e `make build`, que pedem Docker.
- **A primeira página interativa de `apoio/`** — flexibilidade contra erro, que anima as figuras 2.9 a 2.12 do ISLP. Ela é a de prioridade 1 na spec e pertence ao capítulo 7; as duas existentes têm 2.069 e 1.160 linhas escritas à mão, então ela é uma task própria dentro do plano daquele capítulo, não um apêndice dele.

E uma decisão que continua aberta e é do autor: **o cronograma publicado no `index.qmd` da raiz está uma semana atrasado** em relação ao que aconteceu de fato. Corrigi-lo depende de saber como as aulas 1 a 4 mapearam nos capítulos 1 a 5.
