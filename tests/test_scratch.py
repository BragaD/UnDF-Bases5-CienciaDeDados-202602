"""O pacote scratch/ é vendorizado literalmente do repositório do Grus.

Estes testes travam duas coisas que já quebraram na análise do código:
importar working_with_data grava um PNG em im/, e importar getting_data
dispara uma requisição HTTP.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# SHA-256 sobre a concatenação dos *.py de scratch/, em ordem alfabética de
# nome de arquivo, gerado no momento em que o pacote foi vendorizado
# (commits 997435d..c1a1141) e conferido byte a byte contra o upstream
# nessa ocasião (ver .superpowers/sdd/2026-08-15-andaime-livro-bases5/progress.md,
# Task 3).
HASH_SCRATCH_VENDORIZADO = (
    "d91be62c54d84e8b9cac44c4b278f5cfeb4c191939f3d830eafa82da80aaca6c"
)

MODULOS_EM_ESCOPO = [
    "linear_algebra",
    "statistics",
    "probability",
    "gradient_descent",
    "getting_data",
    "working_with_data",
    "machine_learning",
    "k_nearest_neighbors",
    "naive_bayes",
    "simple_linear_regression",
    "multiple_regression",
    "logistic_regression",
    "decision_trees",
    "neural_networks",
    "deep_learning",
    "clustering",
]

# Módulos que NÃO podem ser importados, e por quê. Cada exclusão é uma decisão
# registrada, não um esquecimento — daí o dicionário em vez de um `!=` solto.
NAO_IMPORTAVEIS = {
    "getting_data": (
        "getting_data.py:90 faz requests.get no corpo do módulo — importar dispara rede."
    ),
    "working_with_data": (
        "working_with_data.py:148 abre 'stocks.csv' com caminho relativo ao cwd no corpo "
        "do módulo (upstream mantém o arquivo na raiz do repo; aqui dado vive em dados/), "
        "e as linhas 44-49 afirmam correlation(xs, ys1) numa janela cujo valor real "
        "(~0.894) encosta na borda de (0.89, 0.91) SEM semente — falha ~1 vez em 3."
    ),
}


def test_todos_os_modulos_em_escopo_existem():
    for nome in MODULOS_EM_ESCOPO:
        assert (RAIZ / "scratch" / f"{nome}.py").is_file(), f"falta scratch/{nome}.py"


def test_toda_exclusao_de_import_tem_motivo_registrado():
    """Uma exclusão sem motivo escrito é um esquecimento disfarçado de decisão."""
    for nome, motivo in NAO_IMPORTAVEIS.items():
        assert nome in MODULOS_EM_ESCOPO, f"{nome} nem está em escopo"
        assert motivo and len(motivo) > 40, f"exclusão de {nome} sem motivo real"


def test_diretorio_im_existe():
    """visualization.py tem NOVE plt.savefig('im/...') no nível do módulo — e o
    capítulo 3 (visualização) está em escopo, então essas chamadas rodam de verdade.

    Sem im/, importar visualization.py estoura com FileNotFoundError na primeira
    delas. working_with_data.py:41 tem a mesma exigência, mas esse módulo está em
    NAO_IMPORTAVEIS: a razão principal para im/ existir é visualization.py.
    """
    assert (RAIZ / "im").is_dir()


def test_vector_e_lista_de_float_nao_numpy():
    """A tese pedagógica do livro. Se alguém 'otimizar' isto, o teste cai."""
    fonte = (RAIZ / "scratch" / "linear_algebra.py").read_text()
    assert "Vector = List[float]" in fonte
    assert "import numpy" not in fonte


def test_scratch_nao_importa_numpy_em_lugar_nenhum():
    for py in (RAIZ / "scratch").glob("*.py"):
        assert "import numpy" not in py.read_text(), f"{py.name} importa numpy"


def test_scratch_e_verbatim_upstream():
    """scratch/ é vendorizado literalmente do repositório do Grus (MIT) e
    NUNCA deve ser editado — toda adaptação vive no `.qmd`, para que um
    `diff` contra o upstream continue limpo (CLAUDE.md, seção "O pacote
    scratch/"). Nenhum outro teste deste projeto verifica isso; é o
    princípio mais fácil de violar por acidente (um "conserto" de passagem
    num módulo, por exemplo) e o que não tinha nenhuma guarda.

    Este teste não busca o upstream pela rede a cada rodada — o render deste
    livro é offline por invariante, e um teste que baixasse algo da internet
    contradiria a própria coisa que o projeto garante. Em vez disso, trava
    um hash calculado e verificado uma única vez, no momento da
    vendorização.

    Se este teste falhar, o motivo quase certo é que scratch/ foi editado.
    A resposta correta é REVERTER a edição, não atualizar
    `HASH_SCRATCH_VENDORIZADO` acima — trocar a constante para acomodar uma
    mudança é remover a própria garantia que este teste existe para dar. Uma
    atualização legítima do pacote (ex.: um upgrade deliberado do upstream)
    é uma decisão grande o bastante para merecer revisão explícita, não uma
    troca silenciosa de constante.
    """
    arquivos = sorted((RAIZ / "scratch").glob("*.py"))
    h = hashlib.sha256()
    for p in arquivos:
        h.update(p.read_bytes())
    assert h.hexdigest() == HASH_SCRATCH_VENDORIZADO, (
        "scratch/ não bate mais com o hash vendorizado — foi editado? "
        "Se sim, reverta a edição; não atualize a constante do teste."
    )


def test_modulos_importaveis_sem_rede():
    """Importa cada módulo em escopo, menos os listados em NAO_IMPORTAVEIS.

    getting_data.py:90 tem um requests.get no corpo do módulo — importá-lo
    dispara rede. working_with_data.py:148 abre 'stocks.csv' relativo ao cwd
    (o arquivo não vive na raiz deste repo) e suas linhas 44-49 afirmam uma
    correlação sem semente que falha ~1 vez em 3. Nenhum dos dois é escondido:
    NAO_IMPORTAVEIS documenta o motivo de cada exclusão.
    """
    alvos = [m for m in MODULOS_EM_ESCOPO if m not in NAO_IMPORTAVEIS]
    codigo = "\n".join(f"import scratch.{m}" for m in alvos)
    r = subprocess.run(
        [sys.executable, "-c", codigo],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        # Este dicionário SUBSTITUI o ambiente inteiro do subprocess — nada que
        # esteja no ambiente do container chega aqui se não estiver listado.
        # É por isso que PYTHONHASHSEED precisa ser repetido: o `ENV` do
        # Dockerfile existe (e é obrigatório, ver CLAUDE.md), mas fica invisível
        # para este subprocess justamente por causa desta substituição. Sem ele,
        # naive_bayes.py:113 — um assert de igualdade exata de float sobre uma
        # soma que percorre um Set[str] — falha em ~1 de 8 rodadas.
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
