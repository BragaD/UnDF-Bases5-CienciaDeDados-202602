"""Nenhum byte vem da rede em tempo de render — os dados são commitados."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "dados"

ESPERADOS = [
    "estados.csv",
    "alugueis.csv",
    "cidades.csv",
    "Advertising.csv",
    "Income1.csv",
    "Income2.csv",
    "Credit.csv",
    "Auto.csv",
    "College.csv",
    "Default.csv",
]

COLUNAS_ESPERADAS = {
    "estados.csv": ["estado", "populacao", "taxa_homicidios", "sigla"],
    "cidades.csv": ["cidade", "sigla", "regiao"],
    "Advertising.csv": ["tv", "radio", "jornal", "vendas"],
    "Income1.csv": ["escolaridade", "renda"],
    "Income2.csv": ["escolaridade", "senioridade", "renda"],
    "Credit.csv": [
        "renda", "limite", "pontuacao", "cartoes", "idade", "escolaridade",
        "imovel_proprio", "estudante", "casado", "regiao", "saldo",
    ],
    "Auto.csv": [
        "milhas_por_galao", "cilindros", "cilindrada", "potencia", "peso",
        "aceleracao", "ano", "origem", "nome",
    ],
    "College.csv": [
        "Unnamed: 0", "privada", "inscricoes", "aceitos", "matriculados",
        "perc_top10", "perc_top25", "graduacao_integral", "graduacao_parcial",
        "mensalidade_fora_do_estado", "moradia_e_alimentacao", "custo_livros",
        "gastos_pessoais", "perc_doutores", "perc_titulacao_maxima",
        "razao_aluno_professor", "perc_ex_alunos_doadores", "gasto_por_aluno",
        "taxa_conclusao",
    ],
    "Default.csv": ["inadimplente", "estudante", "saldo", "renda"],
}


def test_conjuntos_presentes():
    for nome in ESPERADOS:
        assert (DADOS / nome).is_file(), f"falta dados/{nome}"


def test_dados_README_documenta_cada_conjunto():
    texto = (DADOS / "README.md").read_text()
    for nome in ESPERADOS:
        assert nome in texto, f"dados/README.md não menciona {nome}"


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


def test_auto_preserva_a_armadilha_da_potencia():
    """A seção 8.5 ensina sobre estas cinco linhas exatas; se elas sumirem, a
    seção mente.

    Alguém "consertando" o CSV — preenchendo os `?` com a mediana, por
    exemplo — faria `potencia` chegar como número direto do `read_csv` e a
    seção passaria a explicar uma conversão de tipo que o arquivo já não
    precisa. O ISLP trabalha com as 392 linhas que sobram depois de
    descartar essas cinco.
    """
    import csv
    with (RAIZ / "dados" / "Auto.csv").open(encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert len(linhas) == 397
    assert sum(1 for l in linhas if l["potencia"] == "?") == 5


def test_college_preserva_a_coluna_de_indice_do_R():
    """A primeira coluna do College é o ASSUNTO de um exercício, não sujeira.

    Nos demais conjuntos do ISLP a coluna de índice do R foi removida na
    tradução. Aqui ela fica: o exercício 3 da lista computacional 1 (o 2.8 do
    livro) leva o aluno a descobrir que a primeira coluna é o nome da
    universidade e a reler o arquivo com `index_col=0`. Sem a coluna, o item
    perde o objeto.
    """
    import csv
    with (DADOS / "College.csv").open(encoding="utf-8") as f:
        cabecalho = next(csv.reader(f))
    assert cabecalho[0] == "Unnamed: 0", (
        "a coluna de índice do College sumiu; o exercício 3 da lista 1 depende dela"
    )


def test_colunas_estao_em_portugues():
    """Do capítulo 6 em diante, o dado que o aluno vê está em português.

    Minúsculas, snake_case, sem acento no nome da coluna; o valor de categoria
    mantém a grafia correta. O nome do ARQUIVO não muda — é a ponte com o site
    do ISLP, e `dados/README.md` guarda a tabela de-para.
    """
    import csv
    for nome, esperadas in COLUNAS_ESPERADAS.items():
        with (DADOS / nome).open(encoding="utf-8") as f:
            cabecalho = next(csv.reader(f))
        assert cabecalho == esperadas, f"{nome}: cabeçalho {cabecalho}"
