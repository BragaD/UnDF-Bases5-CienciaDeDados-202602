"""Invariantes do `pandas` como mesa de trabalho dos dados (caps. 6–17).

Spec: docs/superpowers/specs/2026-09-08-pandas-nos-dados-design.md.

A regra que este arquivo guarda, em uma frase: **`pandas` é a mesa de trabalho,
`numpy` é a calculadora do modelo.** O dado entra pelo `pandas` (ler, tipar,
limpar, juntar, agrupar, apresentar) e atravessa uma fronteira explícita —
`.to_numpy()` — para virar `ndarray` no momento em que o modelo começa.

Como em test_scratch_np.py, os capítulos são convertidos um a um e a lista dos
que já obedecem às regras cresce a cada entrega: quem implementa um capítulo
acrescenta o número dele em CAPITULOS_PANDAS. No fim isto vira range(6, 18).
O ganho é o mesmo: `make teste` fica verde em todo commit da branch, e um teste
vermelho nunca significa "ainda não chegou a vez".

Toda exceção vem com o motivo escrito, no padrão de NAO_IMPORTAVEIS em
test_scratch.py: exceção sem motivo é esquecimento disfarçado de decisão.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONTENT = RAIZ / "content"
PACOTE = RAIZ / "scratch_np"

# Capítulos já convertidos para `pandas` no trabalho com dados. Cresce a cada
# entrega; no fim da conversão, range(6, 18).
CAPITULOS_PANDAS: set[int] = {6}

# Capítulos que ajustam um modelo — é neles que a fronteira `.to_numpy()` tem
# de aparecer. O 7 entra porque a 7.6 e a 7.8 (reescalonamento e PCA) já são
# conta de modelo; os caps. 1–5 não usam `pandas` e não têm modelo ajustado.
CAPITULOS_COM_MODELO: set[int] = set(range(7, 18))

# `csv.reader`/`csv.DictReader` num capítulo convertido só sobrevive onde ler à
# mão É a lição. chave: "capNN/arquivo.qmd", valor: o motivo.
CSV_A_MAO: dict[str, str] = {
    "cap06/01-lendo-arquivos.qmd": (
        "o módulo `csv` da biblioteca padrão é o que existe por baixo do "
        "`read_csv`; a seção o mostra uma vez para o aluno ver o mecanismo e "
        "entender por que não se faz o parsing na mão."
    ),
    "cap07/04-limpeza-e-transformacao.qmd": (
        "`try_parse_row` com `csv.reader` é a lição da seção — o mecanismo do "
        "descarte explícito de linha ruim, comparado logo em seguida com a "
        "coerção silenciosa de `to_numeric(errors='coerce')`."
    ),
}

# Módulos de scratch_np/ que podem importar `pandas` — só os que reexportam
# dados, e só para expor o DataFrame AO LADO do array. Mesmo formato.
EXPORTA_DATAFRAME: dict[str, str] = {}

CHUNK = re.compile(r"^```\{python\}\n(.*?)^```", re.S | re.M)

# `import pandas` / `from pandas import ...` / uso de `pd.`
USA_PANDAS = re.compile(r"^\s*(import\s+pandas\b|from\s+pandas\b)", re.M)

CSV_MANUAL = re.compile(r"\bcsv\.(reader|DictReader|DictWriter|writer)\b")

# A fronteira entre a mesa de trabalho e a calculadora.
FRONTEIRA = re.compile(r"\.to_numpy\(|\.values\b")

# Algoritmo pronto: proibido em chunk que executa. `np.linalg.solve` NÃO entra
# aqui de propósito — ele mostra as equações normais em vez de escondê-las.
# Casa importação e uso qualificado, não a palavra solta: a lista de interesses
# da DataSciencester (cap. 1) tem a *string* "scipy" e não é uso nenhum.
ALGORITMO_PRONTO = re.compile(
    r"(?:^\s*(?:import|from)\s+(?:sklearn|scipy)\b|\b(?:sklearn|scipy)\.|"
    r"np\.polyfit\(|np\.linalg\.lstsq\(|\blstsq\()",
    re.M,
)

# `resample("M")` foi depreciado no pandas 2.2 em favor de `"ME"` (month end).
RESAMPLE_DEPRECIADO = re.compile(r"resample\(\s*[\"']M[\"']")


def chunks_executaveis(texto: str):
    for m in CHUNK.finditer(texto):
        corpo = m.group(1)
        if re.search(r"^#\|\s*eval:\s*false", corpo, re.M):
            continue
        yield corpo


def qmds(cap: int) -> list[Path]:
    return sorted((CONTENT / f"cap{cap:02d}").glob("*.qmd"))


def chave(p: Path) -> str:
    return f"{p.parent.name}/{p.name}"


def modulos_do_pacote() -> list[Path]:
    return sorted(p for p in PACOTE.glob("*.py") if p.name != "__init__.py")


# --------------------------------------------------------------------------
# o ambiente
# --------------------------------------------------------------------------

def test_pandas_e_dependencia_direta_com_teto_na_major():
    """O teto <3 não é burocracia: o pandas 3 quebrou o livro irmão em silêncio."""
    pyproject = (RAIZ / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'"pandas([^"]*)"', pyproject)
    assert m, "pandas não está declarado em pyproject.toml"
    assert "<3" in m.group(1), f'pandas sem teto na major: "pandas{m.group(1)}"'
    lock = (RAIZ / "uv.lock").read_text(encoding="utf-8")
    assert 'name = "pandas"' in lock, "uv.lock não travou o pandas — falta `make lock`"


# --------------------------------------------------------------------------
# o pacote: pandas não entra em scratch_np/
# --------------------------------------------------------------------------

def test_pacote_nao_importa_pandas():
    """Os módulos recebem e devolvem ndarray — é o contrato dos capítulos entre si.

    Um DataFrame ali tornaria o algoritmo dependente de nomes de coluna. A
    exceção é o módulo que reexporta dados: ele pode expor o DataFrame AO LADO
    do array, e precisa dizer por quê.
    """
    for p in modulos_do_pacote():
        if USA_PANDAS.search(p.read_text(encoding="utf-8")):
            assert p.name in EXPORTA_DATAFRAME, (
                f"{p.name} importa pandas sem estar em EXPORTA_DATAFRAME — "
                "em scratch_np/ o pandas só entra para reexportar dado, com motivo"
            )
    for nome, motivo in EXPORTA_DATAFRAME.items():
        assert (PACOTE / nome).is_file(), f"scratch_np/{nome} não existe"
        assert len(motivo) > 40, f"exceção de {nome} sem motivo real"


# --------------------------------------------------------------------------
# os capítulos convertidos
# --------------------------------------------------------------------------

def test_capitulos_pandas_sao_do_escopo():
    assert CAPITULOS_PANDAS <= set(range(6, 18)), "só os caps. 6–17 usam pandas"


def test_capitulo_pandas_importa_pandas():
    for cap in sorted(CAPITULOS_PANDAS):
        assert any(
            USA_PANDAS.search(corpo)
            for p in qmds(cap)
            for corpo in chunks_executaveis(p.read_text(encoding="utf-8"))
        ), f"cap{cap:02d} está em CAPITULOS_PANDAS mas nenhum chunk importa pandas"


def test_fronteira_para_o_modelo_e_explicita():
    """Onde há DataFrame e há modelo, há `.to_numpy()`.

    O dado não atravessa para o modelo por acidente: a linha da fronteira é
    conteúdo do livro — é onde o aluno vê que o modelo não sabe o que é uma
    coluna chamada "amigos".
    """
    faltando = []
    for cap in sorted(CAPITULOS_PANDAS & CAPITULOS_COM_MODELO):
        corpos = [
            corpo
            for p in qmds(cap)
            for corpo in chunks_executaveis(p.read_text(encoding="utf-8"))
        ]
        if any(USA_PANDAS.search(c) for c in corpos) and not any(FRONTEIRA.search(c) for c in corpos):
            faltando.append(f"cap{cap:02d}")
    assert not faltando, (
        "capítulo com DataFrame e modelo, sem `.to_numpy()` em chunk nenhum: "
        + ", ".join(faltando)
    )


def test_csv_a_mao_so_onde_esta_registrado():
    """Ler CSV à mão é lição em dois pontos do livro, e sobra em nenhum outro."""
    ofensores = []
    for cap in sorted(CAPITULOS_PANDAS):
        for p in qmds(cap):
            for corpo in chunks_executaveis(p.read_text(encoding="utf-8")):
                if CSV_MANUAL.search(corpo) and chave(p) not in CSV_A_MAO:
                    ofensores.append(chave(p))
                    break
    assert not ofensores, (
        "csv.reader/DictReader em capítulo convertido (se ler à mão for a lição "
        "ali, registre em CSV_A_MAO com o motivo): " + ", ".join(sorted(set(ofensores)))
    )


def test_capitulo_pandas_nao_usa_resample_depreciado():
    """`resample("M")` saiu no pandas 2.2; é `"ME"`. O material antigo ensina errado."""
    ofensores = [
        chave(p)
        for cap in sorted(CAPITULOS_PANDAS)
        for p in qmds(cap)
        if RESAMPLE_DEPRECIADO.search(p.read_text(encoding="utf-8"))
    ]
    assert not ofensores, 'resample("M") depreciado — use "ME": ' + ", ".join(ofensores)


def test_toda_excecao_tem_motivo_e_arquivo_real():
    for k, motivo in CSV_A_MAO.items():
        assert (CONTENT / k).is_file(), f"{k} não existe"
        assert len(motivo) > 40, f"exceção de {k} sem motivo real"


# --------------------------------------------------------------------------
# o livro inteiro: o algoritmo continua sendo nosso
# --------------------------------------------------------------------------

def test_nenhum_chunk_executavel_usa_algoritmo_pronto():
    """O acréscimo desta spec é realismo no DADO, não conveniência no ALGORITMO.

    `sklearn` e `scipy` só nos callouts de fechamento; `np.polyfit` e
    `np.linalg.lstsq` em lugar nenhum como implementação — eles escondem a
    conta que o capítulo existe para mostrar. `np.linalg.solve` é permitido.
    """
    ofensores = []
    for p in sorted(CONTENT.rglob("*.qmd")):
        for corpo in chunks_executaveis(p.read_text(encoding="utf-8")):
            m = ALGORITMO_PRONTO.search(corpo)
            if m:
                ofensores.append(f"{chave(p)}: {m.group(0)}")
                break
    assert not ofensores, "algoritmo pronto em chunk executável: " + "; ".join(ofensores)
