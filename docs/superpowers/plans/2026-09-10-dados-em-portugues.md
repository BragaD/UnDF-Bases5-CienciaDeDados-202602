# O dado fala português — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Traduzir para o português os conjuntos de dados que o material usa — nome de coluna, nome de variável e valor de categoria — e podar de `dados/` os conjuntos da abordagem abandonada.

**Architecture:** Quatro tasks. A primeira mexe nos dados e nos testes; a segunda e a terceira ajustam os capítulos que os leem; a quarta renderiza. O alcance foi medido, não estimado: **três seções do capítulo 6 e uma do capítulo 7**.

**Tech Stack:** Python 3.12, `pandas`, `pytest`, Quarto.

**Spec:** `docs/superpowers/specs/2026-09-10-estrutura-nova-islp-design.md` — a **emenda "o dado fala português"**.

**Por que agora:** o capítulo 6 está publicado e o 7 está pela metade. Feito hoje, custa quatro seções; feito depois de onze capítulos, custa onze.

## Global Constraints

- **Convenção de nome de coluna: minúsculas, `snake_case`, sem acento.** É a que `dados/alugueis.csv` já usa (`area_m2`, `aceita_animal`, `seguro_incendio`) e que os demais destoavam.
- **Valor de categoria mantém a grafia correta, com acento.** `São Paulo`, `não`, `Sudeste`.
- **O nome do arquivo NÃO muda.** `Advertising.csv` continua `Advertising.csv` — é a ponte com o site do ISLP.
- **A tabela de-para de cada conjunto traduzido vai para `dados/README.md`**, para a correspondência com o livro-texto ser sempre recuperável.
- **A coluna de índice do R sai** dos três conjuntos do ISLP.
- **`dados/alugueis.csv` não é tocado** — já está no padrão, e é o conjunto mais usado do material.
- Ambiente: `export MPLBACKEND=Agg PYTHONHASHSEED=0`; Python é `.venv/bin/python`. Não use Docker.
- **Não rode `make render`** a não ser na última task.
- Editar `.qmd` obriga a rodar `.venv/bin/python scripts/gerar-notebooks.py`.
- **Todo número afirmado na prosa sai da saída de um chunk.** Se um número mudar por causa da tradução, a prosa muda junto.
- A suíte está em **50 testes**; a task 1 a reduz para **47** ao remover os três testes dos conjuntos podados.

---

### Task 1: Os dados em português, e a poda

**Files:**
- Modify: `dados/estados.csv`, `dados/cidades.csv`, `dados/Advertising.csv`, `dados/Income1.csv`, `dados/Income2.csv`
- Delete: `dados/stocks.csv`, `dados/comma_delimited_stock_prices.csv`, `dados/getting-data.html`, `dados/iris.data`, `dados/spam-assuntos.csv`, `dados/imagem-cores.jpg`, `dados/mnist/`
- Modify: `dados/README.md`, `scripts/baixar-dados.py`, `tests/test_dados.py`

**Interfaces:**
- Consumes: nada.
- Produces: os cinco conjuntos com nomes em português. As tasks 2 e 3 leem esses nomes.

- [ ] **Step 1: Traduzir os cinco conjuntos**

Estas são as traduções. Use exatamente estes nomes — as tasks 2 e 3 dependem deles.

| Arquivo | De | Para |
|---|---|---|
| `estados.csv` | `Estado` | `estado` |
| | `Populacao` | `populacao` |
| | `Taxa.Homicidios` | `taxa_homicidios` |
| | `Sigla` | `sigla` |
| `cidades.csv` | `Sigla` | `sigla` |
| | (`cidade` e `regiao` já estão certos) | |
| `Advertising.csv` | `Unnamed: 0` | **removida** |
| | `TV` | `tv` |
| | `radio` | `radio` |
| | `newspaper` | `jornal` |
| | `sales` | `vendas` |
| `Income1.csv` | `Unnamed: 0` | **removida** |
| | `Education` | `escolaridade` |
| | `Income` | `renda` |
| `Income2.csv` | `Unnamed: 0` | **removida** |
| | `Education` | `escolaridade` |
| | `Seniority` | `senioridade` |
| | `Income` | `renda` |

Escreva um script de uso único para fazer isso, rode-o, e **apague o script depois** — ele não é infraestrutura do projeto. Preserve os valores exatamente como estão: **só os cabeçalhos mudam.**

**Nenhum valor de categoria precisa de tradução nestes cinco** — `cidade` e `regiao` já estão em português. Confirme isso antes de seguir; se achar algum valor em inglês, traduza e registre no relatório.

- [ ] **Step 2: Conferir que só os cabeçalhos mudaram**

```bash
export MPLBACKEND=Agg
.venv/bin/python - <<'EOF'
import pandas as pd
for nome, n_col in [("estados", 4), ("cidades", 3), ("Advertising", 4), ("Income1", 2), ("Income2", 3)]:
    d = pd.read_csv(f"dados/{nome}.csv")
    print(f"{nome:14s} {d.shape}  {list(d.columns)}")
    assert d.shape[1] == n_col, f"{nome}: esperava {n_col} colunas"
EOF
```

Esperado: `estados (27, 4)`, `cidades (5, 3)`, `Advertising (200, 4)`, `Income1 (30, 2)`, `Income2 (30, 3)` — os três do ISLP **com uma coluna a menos** que antes, porque o índice do R saiu.

**Confirme também que os valores não mudaram**, comparando uma estatística contra o `git stash`/`git show` da versão anterior — por exemplo, a soma de `vendas` do `Advertising` antes e depois. Registre no relatório.

- [ ] **Step 3: Podar os dormentes**

```bash
git rm -r dados/mnist
git rm dados/stocks.csv dados/comma_delimited_stock_prices.csv dados/getting-data.html \
       dados/iris.data dados/spam-assuntos.csv dados/imagem-cores.jpg
```

Foi verificado que **nenhum arquivo de `content/` os lê**. Se `git rm` reclamar de algum, confirme com `grep -rl` em `content/` antes de forçar — e **pare e reporte** se achar uso.

Remova de `scripts/baixar-dados.py` as entradas que baixavam esses conjuntos, para o script não os ressuscitar. **Mantenha** o bloco do ISLP e o cabeçalho do arquivo.

- [ ] **Step 4: Reescrever `dados/README.md`**

Ele hoje descreve conjuntos que deixaram de existir e traz uma tabela com a numeração de capítulos anterior à ruptura — a mesma que já causou uma ambiguidade. Reescreva:

- Uma seção por conjunto **que existe**: `alugueis.csv`, `estados.csv`, `cidades.csv`, `Advertising.csv`, `Income1.csv`, `Income2.csv`.
- Para cada um do ISLP, a **tabela de-para** (nome original → nome em português) e a nota de que o índice do R foi removido. É essa tabela que mantém a ponte com o livro-texto.
- Para `Income1` e `Income2`, preserve a explicação de que são **simulados pelos autores**, e por que isso importa.
- Uma linha dizendo que os conjuntos da abordagem anterior saíram e que estão recuperáveis no histórico do git.
- **Apague a tabela com a numeração antiga.**

- [ ] **Step 5: Ajustar `tests/test_dados.py`**

- `ESPERADOS` fica com os seis conjuntos que existem.
- **Remova** `test_mnist_presente`, `test_iris_tem_150_linhas_e_4_medidas` e `test_spam_tem_assunto_e_rotulo` — os dados que eles cobravam não existem mais.
- `test_alugueis_preserva_a_armadilha_do_andar` **fica**: `alugueis.csv` não foi tocado.
- Acrescente um teste que trave a tradução, para ninguém reverter sem perceber:

```python
COLUNAS_ESPERADAS = {
    "estados.csv": ["estado", "populacao", "taxa_homicidios", "sigla"],
    "cidades.csv": ["cidade", "sigla", "regiao"],
    "Advertising.csv": ["tv", "radio", "jornal", "vendas"],
    "Income1.csv": ["escolaridade", "renda"],
    "Income2.csv": ["escolaridade", "senioridade", "renda"],
}


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
```

- [ ] **Step 6: Rodar a suíte e commitar**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/pytest tests/ -q
```

Esperado: **48 passed** — 50 menos os três removidos, mais o novo.

**Os capítulos 6 e 7 vão quebrar neste ponto**, porque leem os nomes antigos. Isso é esperado: `pytest` não os executa. As tasks 2 e 3 os consertam. **Não rode `executar-secoes.py` agora** — ele vai falhar, e é normal.

```bash
git add -A dados scripts/baixar-dados.py tests/test_dados.py
git commit -m "feat(dados): os conjuntos falam português, e dados/ guarda só o que se usa

Coluna, variável e categoria em português a partir do capítulo 6, na
convenção que o alugueis.csv já usava: minúsculas, snake_case, sem
acento no nome; acento preservado no valor.

O nome do arquivo não muda — é a ponte com o site do ISLP —, e o README
guarda a tabela de-para. A coluna de índice do R sai: o arquivo
traduzido já não é o arquivo da fonte.

Os sete conjuntos da abordagem abandonada saem, com os três testes que
os cobravam. Nenhum arquivo de content/ os lia."
```

---

### Task 2: As três seções do capítulo 6

**Files:**
- Modify: `content/cap06/01-elementos-de-dados-estruturados.qmd`
- Modify: `content/cap06/02-dados-retangulares.qmd`
- Modify: `content/cap06/05-agrupando-e-resumindo.qmd`

**Interfaces:**
- Consumes: os nomes novos da Task 1.
- Produces: nada que outra task consuma.

- [ ] **Step 1: Trocar os nomes nas três seções**

As três leem `estados.csv` ou `cidades.csv`. Troque `Estado`→`estado`, `Populacao`→`populacao`, `Taxa.Homicidios`→`taxa_homicidios`, `Sigla`→`sigla`, **no código e na prosa** — inclusive dentro de crase, em legenda de figura e em rótulo de eixo.

**Cuidado com o que NÃO deve mudar:** a palavra "estado" no meio de uma frase em português (`a sigla de um estado`) não é o nome da coluna. Troque o que é identificador, não o substantivo.

- [ ] **Step 2: Verificar**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/executar-secoes.py 06
```

Esperado: as seis seções executando.

- [ ] **Step 3: Conferir que nenhum número mudou**

A tradução troca cabeçalho, não valor — então **nenhum número da prosa deveria mudar**. Confira os que as seções afirmam: a correlação de −0,41 da 6.2, a posição de Pernambuco, as medianas por cidade da 6.5. **Se algum mudar, algo além do cabeçalho foi alterado na Task 1** — pare e reporte.

- [ ] **Step 4: Regerar os notebooks, rodar a suíte e commitar**

```bash
.venv/bin/python scripts/gerar-notebooks.py
.venv/bin/pytest tests/ -q
```

Esperado: **48 passed**.

---

### Task 3: A seção 7.2

**Files:**
- Modify: `content/cap07/02-estimar-f.qmd`

**Interfaces:**
- Consumes: os nomes novos da Task 1.

- [ ] **Step 1: Trocar os nomes e remover o `index_col`**

A seção lê `Advertising.csv` e `Income1.csv`. Troque `TV`→`tv`, `newspaper`→`jornal`, `sales`→`vendas`, `Education`→`escolaridade`, `Income`→`renda`, no código e na prosa.

**E remova o `index_col=0`**: a coluna de índice do R não existe mais.

**Isso apaga um trecho de conteúdo**, e é de propósito. A seção trazia uma frase sobre conferir o que o arquivo traz, retomando a lição do capítulo 6, apoiada naquela coluna. Sem a coluna, a frase perde o objeto. **Remova a frase** — a lição continua viva no capítulo 6, sobre dado real, onde ela é verdadeira. Não invente outra armadilha para preservar o parágrafo.

- [ ] **Step 2: Verificar e conferir os números**

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/executar-secoes.py 07
```

A seção afirma números sobre `Advertising` e sobre os resíduos da curva de `Income1` — entre eles a média dos resíduos. **Confira cada um contra a saída nova.** A remoção da coluna de índice não muda nenhum deles, mas confirme em vez de supor.

- [ ] **Step 3: Regerar, rodar a suíte e commitar**

---

### Task 4: O render

**Files:** nenhum, salvo correção que o render revele.

- [ ] **Step 1: Render completo**

```bash
make render
```

Se abortar com `ERROR: Directory not empty`, **não faça nada** — o alvo repete sozinho. Se sair com 75, rode de novo. **Nunca `make clean`.** Não edite `.qmd` durante o render.

- [ ] **Step 2: Conferir que nenhuma página perdeu figura**

As figuras dos capítulos 6 e 7 dependem dos nomes de coluna. Confirme que os PNG de `_book/content/cap06/*_files/` e `_book/content/cap07/*_files/` existem e continuam em **RGBA com alfa 0 nos cantos**.

- [ ] **Step 3: Conferir que nenhum rótulo de eixo ficou em inglês**

O rótulo de um eixo costuma sair do nome da coluna. Procure por `Education`, `Income`, `sales`, `TV`, `Populacao`, `Sigla` no HTML gerado de `_book/content/cap06/` e `_book/content/cap07/`. Se algum aparecer num rótulo ou legenda, ficou para trás.

- [ ] **Step 4: Commitar o que a conferência exigir**
