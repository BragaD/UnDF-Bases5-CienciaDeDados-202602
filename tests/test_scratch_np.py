"""Invariantes da reescrita em numpy dos capítulos 6–17.

Spec: docs/superpowers/specs/2026-09-06-reescrita-numpy-design.md.

Os capítulos são reescritos um a um, em paralelo, então a lista dos que já
obedecem às regras cresce a cada entrega: quem implementa um capítulo acrescenta
o número dele em CAPITULOS_NUMPY, e a partir daí os invariantes valem para ele.
No fim da reescrita isto vira range(6, 18). O ganho é que `make teste` fica
verde em todo commit da branch — um teste vermelho por "ainda não chegou a
vez" ensina os agentes a ignorar teste vermelho.

Toda exceção (uma frase com "Python puro" que é contraste deliberado, um uso de
`random` da stdlib que tem motivo) vem com o motivo escrito, no padrão de
NAO_IMPORTAVEIS em test_scratch.py: exceção sem motivo é esquecimento
disfarçado de decisão.
"""
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONTENT = RAIZ / "content"
PACOTE = RAIZ / "scratch_np"

# Capítulos já reescritos em numpy. Cresce a cada entrega; no fim, range(6, 18).
CAPITULOS_NUMPY: set[int] = set()

# "Python puro" só pode aparecer num capítulo reescrito quando é contraste
# deliberado com os caps. 1–5. chave: "capNN/arquivo.qmd", valor: o motivo.
PYTHON_PURO_PERMITIDO: dict[str, str] = {}

# `random.` da stdlib ou `np.random.seed` num capítulo reescrito. Mesmo formato.
RANDOM_PERMITIDO: dict[str, str] = {}

# Arquivos de scratch_np/ que podem importar `scratch.` — só para reexportar
# DADOS (as listas hard-coded do Grus), nunca função. Mesmo formato.
REEXPORTA_DADOS: dict[str, str] = {
    "statistics.py": (
        "num_friends/daily_minutes e as versões _good moram em scratch/statistics.py; "
        "os caps. 11 e 12 fazem regressão em cima delas."
    ),
    "multiple_regression.py": (
        "`inputs` (200 linhas: constante, amigos, horas) mora em scratch/multiple_regression.py."
    ),
    "logistic_regression.py": (
        "`data` (200 linhas: experiência, salário, conta paga) mora em scratch/logistic_regression.py."
    ),
    "decision_trees.py": (
        "`inputs` (os 14 candidatos a entrevista) mora em scratch/decision_trees.py."
    ),
}

CHUNK = re.compile(r"^```\{python\}\n(.*?)^```", re.S | re.M)
IMPORTA_SCRATCH_PURO = re.compile(r"^\s*(from\s+scratch(?:\.|\s)|import\s+scratch\b(?!_np))", re.M)
IMPORTA_SCRATCH_QUALQUER = re.compile(r"^\s*(from\s+scratch(?:\.|\s+import)|import\s+scratch\b(?!_np))", re.M)
RANDOM_STDLIB = re.compile(
    r"(np\.random\.seed\(|\brandom\.(seed|random|shuffle|choice|choices|randrange|randint|gauss|sample|uniform)\()"
)


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


# --------------------------------------------------------------------------
# o pacote
# --------------------------------------------------------------------------

def modulos_do_pacote() -> list[Path]:
    return sorted(p for p in PACOTE.glob("*.py") if p.name != "__init__.py")


def test_pacote_existe_com_modulos():
    assert (PACOTE / "__init__.py").is_file()
    assert modulos_do_pacote(), "scratch_np/ sem módulos"


def test_todo_modulo_importa_numpy_e_nenhum_importa_sklearn():
    for p in modulos_do_pacote():
        fonte = p.read_text(encoding="utf-8")
        assert "import numpy as np" in fonte, f"{p.name} não importa numpy"
        assert "sklearn" not in fonte, f"{p.name} menciona sklearn"


def test_pacote_so_importa_scratch_para_reexportar_dados():
    for p in modulos_do_pacote():
        if IMPORTA_SCRATCH_QUALQUER.search(p.read_text(encoding="utf-8")):
            assert p.name in REEXPORTA_DADOS, (
                f"{p.name} importa scratch/ sem estar em REEXPORTA_DADOS — "
                "de scratch/ só entra dado, com motivo registrado"
            )
    for nome, motivo in REEXPORTA_DADOS.items():
        assert len(motivo) > 40, f"exceção de {nome} sem motivo real"


def test_pacote_importa_sem_rede_e_sem_erro():
    """Importa cada módulo num subprocesso limpo — os asserts de módulo rodam."""
    nomes = [p.stem for p in modulos_do_pacote()]
    codigo = "\n".join(f"import scratch_np.{m}" for m in nomes)
    r = subprocess.run(
        [sys.executable, "-c", codigo],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        env={
            "MPLBACKEND": "Agg",
            "PATH": "/opt/venv/bin:/usr/bin:/bin",
            "HOME": "/tmp",
            "LANG": "pt_BR.UTF-8",
            "LC_ALL": "pt_BR.UTF-8",
            "PYTHONHASHSEED": "0",
        },
    )
    assert r.returncode == 0, r.stderr


# --------------------------------------------------------------------------
# os capítulos reescritos
# --------------------------------------------------------------------------

def test_capitulos_numpy_sao_do_escopo():
    assert CAPITULOS_NUMPY <= set(range(6, 18)), "só os caps. 6–17 são reescritos"


def test_capitulo_numpy_importa_numpy():
    for cap in sorted(CAPITULOS_NUMPY):
        assert any(
            "import numpy as np" in corpo
            for p in qmds(cap)
            for corpo in chunks_executaveis(p.read_text(encoding="utf-8"))
        ), f"cap{cap:02d} está em CAPITULOS_NUMPY mas nenhum chunk importa numpy"


def test_capitulo_numpy_nao_importa_scratch_puro():
    """Só `scratch_np.` — o `scratch/` em listas é dos caps. 1–5."""
    ofensores = []
    for cap in sorted(CAPITULOS_NUMPY):
        for p in qmds(cap):
            for corpo in chunks_executaveis(p.read_text(encoding="utf-8")):
                m = IMPORTA_SCRATCH_PURO.search(corpo)
                if m:
                    ofensores.append(f"{chave(p)}: {m.group(0).strip()}")
    assert not ofensores, "import de scratch/ (Python puro) em capítulo numpy: " + "; ".join(ofensores)


def test_capitulo_numpy_usa_default_rng():
    """Semente explícita via `np.random.default_rng(...)`, nunca estado global."""
    ofensores = []
    for cap in sorted(CAPITULOS_NUMPY):
        for p in qmds(cap):
            for corpo in chunks_executaveis(p.read_text(encoding="utf-8")):
                if RANDOM_STDLIB.search(corpo) and chave(p) not in RANDOM_PERMITIDO:
                    ofensores.append(chave(p))
                    break
    assert not ofensores, (
        "random da stdlib ou np.random.seed em capítulo numpy (registre em "
        "RANDOM_PERMITIDO com motivo se for deliberado): " + ", ".join(sorted(set(ofensores)))
    )


def test_capitulo_numpy_sem_python_puro_na_prosa():
    """Detector de sobra: a frase que descrevia o código antigo."""
    ofensores = []
    for cap in sorted(CAPITULOS_NUMPY):
        for p in qmds(cap):
            texto = p.read_text(encoding="utf-8")
            if re.search(r"python puro", texto, re.IGNORECASE) and chave(p) not in PYTHON_PURO_PERMITIDO:
                ofensores.append(chave(p))
    assert not ofensores, (
        '"Python puro" em capítulo reescrito (se for contraste deliberado com os '
        "caps. 1–5, registre em PYTHON_PURO_PERMITIDO com o motivo): " + ", ".join(ofensores)
    )


def test_toda_excecao_tem_motivo_e_arquivo_real():
    for tabela in (PYTHON_PURO_PERMITIDO, RANDOM_PERMITIDO):
        for k, motivo in tabela.items():
            assert (CONTENT / k).is_file(), f"{k} não existe"
            assert len(motivo) > 40, f"exceção de {k} sem motivo real"


# --------------------------------------------------------------------------
# o livro inteiro
# --------------------------------------------------------------------------

def test_nenhum_chunk_executavel_usa_sklearn():
    """O scikit-learn só aparece nos callouts de fechamento, em ```python que não roda."""
    ofensores = [
        chave(p)
        for p in sorted(CONTENT.rglob("*.qmd"))
        if any("sklearn" in corpo for corpo in chunks_executaveis(p.read_text(encoding="utf-8")))
    ]
    assert not ofensores, "sklearn em chunk executável: " + ", ".join(ofensores)
