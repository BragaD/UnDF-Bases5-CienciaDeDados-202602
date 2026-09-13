# Lista Computacional 1 — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) ou superpowers:executing-plans para implementar este plano task a task. Os passos usam `- [ ]` para rastreio.

**Goal:** Construir a **lista computacional 1** — oito exercícios adaptados do ISLP, cobrindo os capítulos 6, 7 e 8 —, o gerador que a transforma em notebook do Colab, o conjunto `College` que ela exige, e a mudança de avaliação no site. **Entrega em 07/10.**

**Architecture:** A fonte é um `.qmd` em `atividades/`; o notebook do aluno é derivado dela por um script novo e fino que **importa o parser de `scripts/gerar-notebooks.py`** em vez de duplicá-lo. Não há gabarito e não há PDF do enunciado — o notebook é a lista. O aluno abre no Colab, a célula de preparo clona o repositório e põe `dados/` ao alcance, ele preenche as células marcadas, executa tudo e exporta em PDF.

**Tech Stack:** Quarto (só como formato de fonte, não como render), Python 3.12, `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `nbformat` pela via do gerador existente, `pytest`. Nenhuma dependência nova.

**Spec:** `docs/superpowers/specs/2026-09-13-listas-computacionais-design.md`

## Global Constraints

- **Máximo do enunciado original do ISLP.** Só duas coisas mudam: a **ferramenta** (`sm.OLS()`/`summarize()` viram `LinearRegression`) e os **itens de inferência**, que são **removidos**, não reescritos.
- **Nada de inferência, em lugar nenhum:** valor-p, estatística *t*, estatística *F*, `anova_lm`, erro-padrão de coeficiente, intervalo de confiança ou de predição, "estatisticamente significativo". `statsmodels` e o pacote `ISLP` são proibidos.
- **A lista não comenta a própria adaptação.** O enunciado é sobre ciência de dados, não sobre o que o professor cortou. A linha de correspondência diz de onde o exercício vem, e nada mais.
- **O dado fala português** — nome de coluna, de variável e de categoria. Exceção única e registrada: a coluna `Unnamed: 0` do `College.csv`, que é o assunto de um item.
- **A célula de resposta é reconhecível por marca literal:** uma célula de código de resposta contém **só** a linha `# sua resposta`; uma célula de texto de resposta contém **só** a linha `*sua resposta aqui*`. É o contrato entre o enunciado, o aluno e a suíte.
- **Nenhuma célula da lista guarda saída de execução**, e nenhuma célula de resposta vem preenchida.
- **O `.qmd` é a fonte, o `.ipynb` é derivado.** Editar o `.ipynb` é trabalho perdido.
- Caminho de dados **a partir da raiz**; nenhum byte vem da rede em tempo de execução (a célula de preparo do Colab clona o repositório, e isso é o aluno rodando, não render).
- Ambiente: `export MPLBACKEND=Agg PYTHONHASHSEED=0`; Python é `.venv/bin/python`. A suíte está em **50** testes e cresce nas tasks 1 e 2.
- **Não rode `make render`** durante a implementação — só na última task.

## Estrutura de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `dados/College.csv` | 777 universidades, 19 colunas; a de índice do R preservada de propósito |
| `scripts/gerar-lista.py` | `.qmd` de `atividades/` → `.ipynb`, reusando o parser dos notebooks de aula |
| `atividades/lista-comp-01.qmd` | a fonte da lista: cabeçalho, instruções, oito exercícios |
| `atividades/lista-comp-01.ipynb` | derivado; é o que o aluno abre no Colab |
| `tests/test_atividades.py` | os guardas da lista: defasagem, resposta preenchida, saída commitada |
| `index.qmd` | a avaliação sem prova, e o cronograma |

---

### Task 1: `College.csv` em `dados/`, traduzido, com a coluna de índice preservada

**Files:**
- Create: `dados/College.csv`
- Modify: `scripts/baixar-dados.py`, `dados/README.md`, `tests/test_dados.py`, `tests/test_estrutura.py`

**Interfaces:**
- Produces: `dados/College.csv` com as colunas `Unnamed: 0, privada, inscricoes, aceitos, matriculados, perc_top10, perc_top25, graduacao_integral, graduacao_parcial, mensalidade_fora_do_estado, moradia_e_alimentacao, custo_livros, gastos_pessoais, perc_doutores, perc_titulacao_maxima, razao_aluno_professor, perc_ex_alunos_doadores, gasto_por_aluno, taxa_conclusao`. **A task 4 depende desses nomes exatos.**

- [ ] **Step 1: Acrescentar o conjunto ao coletor**

Em `scripts/baixar-dados.py`, o laço passa a:

```python
# `College` entra com a lista computacional 1: o exercício 3 dela é o 2.8 do
# ISLP, que percorre o conjunto inteiro com `read_csv`, `describe` e uma matriz
# de dispersão.
for nome in ["Advertising", "Income1", "Income2", "Credit", "Auto", "College"]:
    baixar(BASE_ISLP + f"{nome}.csv", DADOS / f"{nome}.csv")
```

Rode `.venv/bin/python scripts/baixar-dados.py` e confira que chegaram 777 linhas e 19 colunas.

- [ ] **Step 2: Traduzir o cabeçalho e a categoria, PRESERVANDO a coluna de índice**

Script descartável (não commite) que aplica exatamente esta tabela:

| Original | Traduzida |
|---|---|
| `Unnamed: 0` | **`Unnamed: 0` — não muda** |
| `Private` | `privada` |
| `Apps` | `inscricoes` |
| `Accept` | `aceitos` |
| `Enroll` | `matriculados` |
| `Top10perc` | `perc_top10` |
| `Top25perc` | `perc_top25` |
| `F.Undergrad` | `graduacao_integral` |
| `P.Undergrad` | `graduacao_parcial` |
| `Outstate` | `mensalidade_fora_do_estado` |
| `Room.Board` | `moradia_e_alimentacao` |
| `Books` | `custo_livros` |
| `Personal` | `gastos_pessoais` |
| `PhD` | `perc_doutores` |
| `Terminal` | `perc_titulacao_maxima` |
| `S.F.Ratio` | `razao_aluno_professor` |
| `perc.alumni` | `perc_ex_alunos_doadores` |
| `Expend` | `gasto_por_aluno` |
| `Grad.Rate` | `taxa_conclusao` |

Categorias: em `privada`, `Yes` → `sim` e `No` → `não`.

**A primeira coluna fica como está, com o nome `Unnamed: 0` que o `pandas` gera, e com os nomes das universidades em inglês.** Nos outros CSV do ISLP essa coluna foi removida; aqui ela é o assunto de um item do exercício — o aluno descobre que a primeira coluna é o nome da universidade e a relê com `index_col=0`. Removê-la apagaria o exercício. Nomes de universidade são nomes próprios e não se traduzem.

**Cuidado ao reescrever:** o CSV tem vírgulas dentro de nomes de universidade. Leia e grave com o módulo `csv` ou com o `pandas`, nunca com substituição de texto.

- [ ] **Step 3: Documentar em `dados/README.md`**

Acrescente a seção no molde da que já existe para `Credit` e `Auto`: de onde vem (o site de `@james2023`), o que é (777 universidades americanas), a tabela de-para acima, e — **explicitamente** — que a coluna de índice do R **foi preservada**, com o motivo: o exercício que usa este conjunto é sobre ela.

- [ ] **Step 4: Fechar o guarda de nome antigo**

Em `tests/test_estrutura.py`, acrescente a `NOMES_ANTIGOS_DE_COLUNA`:

```python
    "Private",
    "Apps",
    "Accept",
    "Enroll",
    "Outstate",
    "Expend",
```

**Não acrescente `Books`, `Personal`, `Terminal`, `PhD`, `Top10perc`, `Room.Board`, `S.F.Ratio`, `Grad.Rate` nem `F.Undergrad`:** os quatro primeiros são palavras que aparecem em prosa sem relação com o conjunto, e os demais não ocorrem em português nem por acidente. Escreva esse motivo num comentário ao lado, como a lista já faz para `Age`, `year`, `weight` e `name`.

- [ ] **Step 5: Registrar em `tests/test_dados.py` e criar o guarda da coluna de índice**

Acrescente `College.csv` a `ESPERADOS` e as colunas a `COLUNAS_ESPERADAS`, na ordem real do arquivo. E crie o teste, no molde de `test_auto_preserva_a_armadilha_da_potencia`:

```python
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
```

- [ ] **Step 6: Rodar a suíte e commitar**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/pytest tests/ -q
```

Esperado: **51 passed** (um teste novo).

```bash
git add dados/ scripts/baixar-dados.py tests/
git commit -m "feat(dados): College, do site do ISLP, em português

O conjunto do exercício 3 da lista computacional 1. Cabeçalho e categoria
traduzidos; a coluna de índice do R fica, contra a convenção dos outros
conjuntos, porque é sobre ela que o item (b) do exercício trata."
```

---

### Task 2: `scripts/gerar-lista.py`, o esqueleto da lista, e os três guardas

**Files:**
- Create: `scripts/gerar-lista.py`, `atividades/lista-comp-01.qmd`, `atividades/lista-comp-01.ipynb` (gerado)
- Modify: `tests/test_atividades.py`

**Interfaces:**
- Consumes: de `scripts/gerar-notebooks.py`, por importação via caminho: `converte`, `celula_markdown`, `celula_codigo`, `CELULA_PREPARO`, `normaliza`, `serializa`, `le_bibliografia`, `citacao_curta`.
- Produces: `atividades/lista-comp-01.ipynb`, e o módulo `scripts/gerar-lista.py` expondo `gerar_lista(fonte: Path) -> dict`, `normaliza` e `serializa`. **Os testes desta task e a task 7 chamam os três.**

- [ ] **Step 1: Escrever o gerador**

`scripts/gerar-lista.py` importa o parser por caminho, no mesmo padrão que `scripts/gerar-stubs.py` já usa (o hífen no nome impede `import` normal):

```python
import importlib.util
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def _carregar_gerador():
    caminho = RAIZ / "scripts" / "gerar-notebooks.py"
    spec = importlib.util.spec_from_file_location("gerar_notebooks", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


G = _carregar_gerador()
```

O módulo expõe **três nomes**, e os três são o que os testes desta task chamam:

```python
def gerar_lista(fonte: Path) -> dict:
    # O notebook de uma lista, em memória, a partir do .qmd fonte.
    ...


# Reexportados de gerar-notebooks.py para que quem gera e quem testa use um
# módulo só — o teste de defasagem precisa serializar do mesmo jeito que o
# gerador, e importar os dois separadamente é como as duas pontas divergem.
normaliza = G.normaliza
serializa = G.serializa
```

`gerar_lista` monta o notebook nesta ordem: a **célula de preparo**
(`G.CELULA_PREPARO`, que clona o repositório quando o Colab não acha o projeto),
e depois as células que `G.converte` produzir a partir do corpo do `.qmd` — o
cabeçalho YAML não vira célula. O `main()` grava com
`serializa(normaliza(gerar_lista(fonte)))` para cada `atividades/lista-comp-*.qmd`.

**Por que um script novo e não estender o de capítulos:** `gerar-notebooks.py`
varre `content/cap*/` e é contado pelos testes de total do livro; uma lista
falsearia essa contagem.

- [ ] **Step 2: Escrever o esqueleto da lista**

`atividades/lista-comp-01.qmd`, com o cabeçalho YAML no molde de `atividades/lista-01-revisao.qmd` e, no corpo, nesta ordem:

1. **Como entregar** — abrir no Colab pelo link, `Arquivo → Salvar uma cópia no Drive`, preencher, **`Ambiente de execução → Executar tudo`**, `Arquivo → Imprimir → Salvar como PDF`, postar no AVA/Moodle. Diga que **sem executar tudo o PDF sai sem as saídas**, e que vale conferir se alguma saída larga ficou cortada na impressão.
2. **Prazo e peso:** entrega até **07/10/2026**, peso **10%**.
3. **A célula de identificação** — uma célula de texto pedindo nome e matrícula, com a marca de resposta.
4. **Um chunk de setup** com os `import` que a lista inteira usa, para o aluno não precisar descobri-los: `pandas as pd`, `numpy as np`, `matplotlib.pyplot as plt`, `from sklearn.linear_model import LinearRegression`, `from sklearn.metrics import r2_score, mean_squared_error`.

Os oito exercícios entram nas tasks 3 a 5; aqui o arquivo termina depois do setup.

- [ ] **Step 3: Escrever os três guardas**

Em `tests/test_atividades.py`:

```python
def test_a_lista_computacional_nao_defasou_da_fonte():
    """Irmão de test_notebooks_estao_atualizados, e não a mesma varredura.

    Aquela está presa a `content/` e alimenta os testes de total do livro, que
    uma lista falsearia. O invariante é o mesmo: o .qmd é a fonte, o .ipynb é
    derivado, e o aluno não pode abrir uma versão que a fonte já não tem.
    """
    gerar = carregar_gerador_de_lista()
    for fonte in sorted(ATIVIDADES.glob("lista-comp-*.qmd")):
        destino = fonte.with_suffix(".ipynb")
        assert destino.exists(), f"falta o notebook de {fonte.name}"
        em_memoria = gerar.serializa(gerar.normaliza(gerar.gerar_lista(fonte)))
        assert em_memoria == destino.read_text(encoding="utf-8"), (
            f"{destino.name} defasou de {fonte.name}; rode scripts/gerar-lista.py"
        )


def test_nenhuma_celula_de_resposta_vem_preenchida():
    """O guarda contra commitar o notebook depois de conferi-lo executando.

    A marca é literal: célula de código de resposta contém só `# sua resposta`,
    célula de texto contém só `*sua resposta aqui*`.
    """
    import json
    for nb_path in sorted(ATIVIDADES.glob("lista-comp-*.ipynb")):
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        for i, celula in enumerate(nb["cells"]):
            fonte = "".join(celula["source"]).strip()
            if fonte.startswith("# sua resposta"):
                assert fonte == "# sua resposta", (
                    f"{nb_path.name}, célula {i}: resposta de código preenchida"
                )
            if "*sua resposta aqui*" in fonte:
                assert fonte == "*sua resposta aqui*", (
                    f"{nb_path.name}, célula {i}: resposta de texto preenchida"
                )


def test_nenhuma_celula_da_lista_guarda_saida():
    """O mesmo invariante dos notebooks de aula, mais um motivo: saída entrega resposta."""
    import json
    for nb_path in sorted(ATIVIDADES.glob("lista-comp-*.ipynb")):
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        for i, celula in enumerate(nb["cells"]):
            if celula["cell_type"] != "code":
                continue
            assert not celula.get("outputs"), f"{nb_path.name}, célula {i}: saída commitada"
            assert celula.get("execution_count") is None, (
                f"{nb_path.name}, célula {i}: contador de execução commitado"
            )
```

`carregar_gerador_de_lista()` é um auxiliar no molde de `carregar_gerador` de `tests/test_notebooks.py`, importando `scripts/gerar-lista.py` por caminho.

- [ ] **Step 4: Gerar, rodar a suíte e commitar**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/gerar-lista.py
.venv/bin/pytest tests/ -q
```

Esperado: **54 passed** (três testes novos).

```bash
git add scripts/gerar-lista.py atividades/lista-comp-01.qmd atividades/lista-comp-01.ipynb tests/test_atividades.py
git commit -m "feat(atividades): o gerador da lista computacional e o esqueleto da lista 1"
```

---

### Task 3: Os quatro exercícios conceituais — 1, 2, 5 e 6

**Files:**
- Modify: `atividades/lista-comp-01.qmd`, `atividades/lista-comp-01.ipynb` (regenerado)

**Interfaces:**
- Consumes: o esqueleto da task 2.
- Produces: os exercícios 1, 2, 5 e 6. As tasks 4 e 5 acrescentam os demais **entre** eles, na ordem numérica.

Os quatro são de texto puro: enunciado, e uma célula de resposta `*sua resposta aqui*`. Nenhum pede código.

- [ ] **Step 1: Ler os enunciados no livro**

`livros/ISLP_website.pdf`, seção **2.4 Exercises**, itens **2** e **6**; seção **3.7 Exercises**, itens **3** e **4**. Traduza para o português mantendo a estrutura de sub-itens do original.

- [ ] **Step 2: Escrever os quatro**

- **Exercício 1** (ISLP 2.2) — os três cenários (a), (b) e (c); para cada um, classificação ou regressão, inferência ou predição, e *n* e *p*. **Sem adaptação:** o enunciado usa "inferência" no sentido de *entender a relação*, que é o sentido que a seção 7.2 do material estabelece — não no sentido de teste de hipótese.
- **Exercício 2** (ISLP 2.6) — diferenças entre paramétrico e não paramétrico, vantagens e desvantagens. Sem adaptação.
- **Exercício 5** (ISLP 3.3) — o modelo com GPA, QI, nível e as duas interações, com os seis coeficientes dados. Sem adaptação. **Traduza as variáveis** (`GPA`, `IQ`, `Level`) mantendo os valores dos coeficientes.
- **Exercício 6** (ISLP 3.4) — RSS de treino e de teste, reta contra cúbica, nos quatro cenários. Sem adaptação. É o exercício que mais amarra com a 8.7.

Cada um abre com a linha de correspondência, no molde: `*Adaptado do exercício 2 do capítulo 2 de James et al. (2023).*` — e, onde não houver adaptação nenhuma, `*Do exercício 6 do capítulo 2 de James et al. (2023).*`

- [ ] **Step 3: Regenerar, verificar e commitar**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/gerar-lista.py
.venv/bin/pytest tests/ -q
```

Esperado: **54 passed**.

```bash
git add atividades/
git commit -m "feat(atividades): lista 1 — os quatro exercícios conceituais"
```

---

### Task 4: Exercícios 3 e 4 — o `College` e o `Auto` descritivos

**Files:**
- Modify: `atividades/lista-comp-01.qmd`, `atividades/lista-comp-01.ipynb` (regenerado)

**Interfaces:**
- Consumes: `dados/College.csv` com os nomes da task 1; `dados/Auto.csv`, já em `dados/`.
- Produces: os exercícios 3 e 4, posicionados entre o 2 e o 5.

- [ ] **Step 1: Ler os enunciados**

`livros/ISLP_website.pdf`, seção 2.4, itens **8** e **9**, inteiros — o 8 tem sub-itens de (a) a (e), o 9 de (a) a (f).

- [ ] **Step 2: Escrever o exercício 3 (ISLP 2.8) — o `College`**

Mantém a espinha do original, com duas diferenças obrigatórias:

- Onde o livro manda ler `College.csv` de um caminho qualquer, a lista usa **`dados/College.csv`**, o caminho a partir da raiz, que a célula de preparo torna válido no Colab.
- Os nomes de coluna são os **traduzidos**. A lista da descrição das variáveis, que o livro traz no enunciado, entra em português.

**O item (b) é o coração do exercício e fica inteiro:** o aluno olha o `DataFrame`, descobre que a primeira coluna é o nome da universidade e chama-se `Unnamed: 0`, relê com `index_col=0`, e compara. É por isso que a coluna foi preservada.

Os itens de `describe()`, matriz de dispersão, `boxplot` e a variável derivada `Elite` — que vira **`elite`** — ficam como estão.

- [ ] **Step 3: Escrever o exercício 4 (ISLP 2.9) — o `Auto`**

Mantém todos os sub-itens. Três notas para o enunciado:

- O livro manda garantir que os valores faltantes foram removidos. **Mantenha essa instrução**: o nosso `Auto.csv` preserva os cinco `?` de `potencia`, e descartá-los é parte do exercício. O aluno usa `pd.to_numeric(..., errors="coerce")` e `dropna`, como o capítulo 6 ensinou.
- `origem` é código numérico (1, 2, 3) e **é qualitativa** — é a pegadinha do item (a), e o enunciado não deve entregá-la.
- `nome` é qualitativa e tem um valor quase por linha.

- [ ] **Step 4: Cada sub-item de código ganha as suas duas células**

Uma de código com `# sua resposta`, e uma de texto com `*sua resposta aqui*`, porque todo item destes pede interpretação junto da conta.

- [ ] **Step 5: Regenerar, verificar e commitar**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/gerar-lista.py
.venv/bin/pytest tests/ -q
```

Esperado: **54 passed**.

```bash
git add atividades/
git commit -m "feat(atividades): lista 1 — exercícios 3 e 4, o College e o Auto"
```

---

### Task 5: Exercícios 7 e 8 — a regressão no `Auto`, e a adaptação

**Files:**
- Modify: `atividades/lista-comp-01.qmd`, `atividades/lista-comp-01.ipynb` (regenerado)

**Interfaces:**
- Consumes: `dados/Auto.csv`.
- Produces: os exercícios 7 e 8, ao fim da lista.

**Esta é a task delicada do plano.** Os dois exercícios originais são construídos sobre `statsmodels` e sobre leitura de valor-p, e a adaptação é item a item. O que segue **é a decisão, não uma sugestão**.

- [ ] **Step 1: Escrever o exercício 7 (ISLP 3.8) — regressão simples**

| Item do ISLP | Destino |
|---|---|
| (a) `sm.OLS()` + `summarize()` | **a ferramenta muda:** `LinearRegression` sobre `milhas_por_galao ~ potencia` |
| (a.i) "há relação entre preditor e resposta?" | **SAI** — no livro é o valor-p |
| (a.ii) "quão forte é a relação?" | **FICA**, respondido com **R² e RSE**, e o enunciado pede que o aluno diga o que cada um mede |
| (a.iii) "a relação é positiva ou negativa?" | **FICA** — é o sinal do coeficiente, puramente descritivo |
| (a.iv) previsão para `potencia = 98` | **FICA a previsão**; os **intervalos de confiança e de predição SAEM** |
| (b) gráfico com a reta ajustada | **FICA** |
| (c) gráficos de diagnóstico, comente os problemas | **FICA inteiro** — é exatamente a seção 8.6 |

- [ ] **Step 2: Escrever o exercício 8 (ISLP 3.9) — regressão múltipla**

| Item do ISLP | Destino |
|---|---|
| (a) matriz de dispersão de todas as variáveis | **FICA** (`pd.plotting.scatter_matrix`) |
| (b) matriz de correlações com `.corr()` | **FICA** |
| (c) `sm.OLS()` + `summarize()`, todas menos `name` | **a ferramenta muda:** `LinearRegression` sobre todas menos `nome` |
| (c.i) "use `anova_lm()`" | **SAI inteiro** — é a estatística *F* |
| (c.ii) "quais preditores têm relação estatisticamente significativa?" | **SAI** |
| (c.iii) "o que o coeficiente de `ano` sugere?" | **FICA** — é leitura de coeficiente |
| (d) diagnóstico: resíduos, outliers, alavancagem | **FICA inteiro** — é a seção 8.6 |
| (e) "alguma interação parece estatisticamente significativa?" | **FICA a interação, SAI o "significativa"**: a pergunta vira se a interação **melhora o ajuste**, respondida por R² |
| (f) transformações `log(X)`, `√X`, `X²` | **FICA inteiro** — é a seção 8.5 |

**Duas notas para o enunciado do 8:** `nome` fica de fora dos preditores, como no original; e `origem` é código numérico que representa categoria — o aluno que a tratar como número está fazendo uma escolha, e o enunciado pode pedir que ele a justifique.

- [ ] **Step 3: Conferir que nada de inferência sobrou**

```bash
grep -n -iE "valor-p|p-valor|estatística t|estatística F|anova|significativ|intervalo de confian|intervalo de predi|erro-padrão do coef|statsmodels|sm\.OLS|summarize\(" atividades/lista-comp-01.qmd
```

Esperado: **nenhuma ocorrência**.

- [ ] **Step 4: Regenerar, verificar e commitar**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/gerar-lista.py
.venv/bin/pytest tests/ -q
```

Esperado: **54 passed**.

```bash
git add atividades/
git commit -m "feat(atividades): lista 1 — exercícios 7 e 8, regressão no Auto"
```

---

### Task 6: A avaliação sem prova, no `index.qmd`

**Files:**
- Modify: `index.qmd`

**Interfaces:**
- Consumes: nada.
- Produces: nada que outra task consuma.

- [ ] **Step 1: Trocar a tabela de avaliação**

A tabela de quatro linhas passa a:

| Instrumento | Peso | Quando |
|---|:--:|---|
| Lista 1 — revisão de pré-requisitos | 10% | entrega até 16/09/2026 (aula 5) |
| Listas computacionais 1 a 5 | 10% cada | 07/10, 28/10, 11/11, 25/11 e 09/12 |
| Seminário em grupo | 40% | apresentação em 16/12/2026 (aula 18) |

- [ ] **Step 2: Corrigir a frase sobre entrega manuscrita**

O texto diz hoje que "as duas listas são entregues manuscritas". **Passa a valer só para a lista 1.** As computacionais são feitas no Colab e entregues em PDF pelo AVA/Moodle — diga isso, e diga que elas são o instrumento que acompanha as aulas, entregues uma semana depois do capítulo que fecham.

- [ ] **Step 3: Corrigir o cronograma**

- A aula 5 (16/09) mantém a entrega da lista 1.
- A **aula 8 (07/10)** ganha **entrega da lista computacional 1**.
- As aulas 11, 13, 15 e 17 ganham as entregas das listas 2 a 5.
- **Some "revisão para a prova" da aula 16, "Prova" da aula 17 e "Revisão da prova" da aula 19.** As três aulas ficam com o conteúdo que já tinham, ou com *a definir* onde não havia outro.
- A frase de abertura do cronograma diz que "as três últimas são avaliativas" — **reescreva** para o que passa a ser verdade.

- [ ] **Step 4: Acrescentar o link do Colab para a lista**

Onde o cronograma cita a entrega da lista computacional 1, o link é o do Colab para `atividades/lista-comp-01.ipynb`, no mesmo formato dos notebooks de capítulo:
`https://colab.research.google.com/github/BragaD/UnDF-Bases5-CienciaDeDados-202602/blob/main/atividades/lista-comp-01.ipynb`

- [ ] **Step 5: Verificar e commitar**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/pytest tests/ -q
```

Esperado: **54 passed**. Atenção a `test_todo_link_interno_para_qmd_resolve` e a `test_todo_pdf_publicado_esta_linkado_no_site`, que reagem a mudança de link no `index.qmd`.

```bash
git add index.qmd
git commit -m "docs: a avaliação passa a ser por listas computacionais, sem prova"
```

---

### Task 7: O notebook executado de ponta a ponta, e o render

**Files:**
- Modify: nenhum, salvo o que a verificação exigir corrigir.

- [ ] **Step 1: Executar a lista como o aluno executaria**

O notebook do aluno tem células de resposta vazias, então ele **não** roda sozinho — o `# sua resposta` não faz nada, e os itens dependem de o aluno escrever. O que se verifica é outra coisa: que **todo chunk que a lista fornece pronta** (o setup, e qualquer leitura de dado que o enunciado já dê) executa, e que os caminhos de dado resolvem.

Escreva um script descartável que monte um notebook só com as células de código **não vazias** da lista, execute-o com o cwd na raiz, e reporte. Nenhuma célula fornecida pode falhar.

- [ ] **Step 2: Conferir os dois conjuntos pelos nomes que a lista usa**

```bash
.venv/bin/python -c "
import pandas as pd
c = pd.read_csv('dados/College.csv')
a = pd.read_csv('dados/Auto.csv')
print('College', c.shape, c.columns[0], '|', list(c.columns[1:4]))
print('Auto   ', a.shape, list(a.columns[:4]))
"
```

Confira que todo nome de coluna citado no `.qmd` existe de fato nos arquivos. **Um nome de coluna errado no enunciado é o defeito mais caro desta lista** — o aluno trava e não tem como saber que o erro não é dele.

- [ ] **Step 3: Render do site**

```bash
make render
```

O `make render` é serializado e leva minutos. Se abortar com `ERROR: Directory not empty`, **não faça nada** — é a corrida do bind mount do macOS, e o alvo repete sozinho até seis vezes. Se sair com 75, rode de novo. **Nunca `make clean`.** **Não edite nenhum `.qmd` enquanto o render roda.** **Não encerre o turno esperando o render.**

- [ ] **Step 4: As três conferências**

1. **A tabela de avaliação** em `_book/index.html` mostra os três instrumentos e soma 100%.
2. **O link do Colab para a lista** aparece no cronograma e aponta para `atividades/lista-comp-01.ipynb`.
3. **Nenhum termo de inferência** no `.qmd` da lista nem no notebook — repita o `grep` do Step 3 da task 5, agora também sobre o `.ipynb`.

- [ ] **Step 5: Commitar o que a verificação tiver corrigido**

```bash
git add -A atividades/ index.qmd dados/
git commit -m "fix(atividades): correções da verificação de ponta a ponta da lista 1"
```
