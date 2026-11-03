# Páginas de apoio do capítulo 12 (crescimento e poda) — Plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Duas páginas interativas em `apoio/` — `crescimento-da-arvore.html` (seção 12.1) e `poda-da-arvore.html` (seção 12.2) — que mostram a árvore de regressão crescendo corte a corte e sendo podada degrau a degrau, com os números das seções.

**Architecture:** Cada página é um HTML único, estático, com CSS e JS inline. Os dados entram num `<script type="application/json" id="dados">`, escrito por `scripts/gerar-dados-arvores.py` (que roda no container). As contas da página ficam num `<script id="nucleo">` sem DOM, que os testes extraem e executam com `node` para comparar com o `scikit-learn`. A interface (SVG, controles) fica num segundo `<script>`, que só chama o núcleo.

**Tech Stack:** HTML/CSS/JS sem dependências, SVG; Python 3 com `pandas` e `scikit-learn` no gerador; `pytest` e `node` (host) nos testes.

**Spec:** `docs/superpowers/specs/2026-11-03-apoio-arvores-design.md`

## Global Constraints

- Um `.html` por página, CSS e JS inline, nenhum `<script src>`; fontes do Google Fonts como nas irmãs, com fallback, e a página roda offline.
- Copiar o bloco de tokens de `apoio/polinomios-e-ruido.html` (`:root`, `@media (prefers-color-scheme: dark)` com `:root:not([data-theme="light"])`, e `:root[data-theme="dark"]`). Laranja = token `--ajuste` (`#D9480F` claro, `#FF7A45` escuro), só para o que está mudando; azul é o que está parado.
- Repintar em `resize` e na troca de `prefers-color-scheme`, como as irmãs (`pintar`).
- Texto da página em português, números em pt-BR via `Intl.NumberFormat("pt-BR")` (vírgula decimal, ponto de milhar: `1.452,0`).
- Notação: "folha", "nó", "ramo", "raiz", RSS, α; `ccp_alpha` = α/n com n = 132.
- Perguntas: no crescimento, `coluna < corte` (como a (8.2) da 12.1); na poda, `coluna ≤ limiar` (como `fig-poda`).
- Nada de texto sobre o material, a página ou o ISLP (INV-13).
- Desktop e projetor, temas claro e escuro; celular não é requisito.
- Carregar a skill `dataviz` antes de escrever código de gráfico (tarefas 3 e 5).
- O gerador roda **no container**: `docker compose run --rm --no-deps livro python scripts/gerar-dados-arvores.py`.
- Verificação no host: `export MPLBACKEND=Agg PYTHONHASHSEED=0` e `.venv/bin/pytest`.
- Commit por tarefa, sem push (push na `main` publica o site). Mensagens no estilo `feat(apoio): …`, terminando com as linhas de atribuição da sessão.

## Review Focus

1. **Região sem corte possível** (todos os jogadores com o mesmo valor numa coluna): o botão daquela coluna fica desabilitado, não aparece fantasma, nada de `NaN` na tela. Teste `test_regiao_sem_corte_possivel` (tarefa 2).
2. **Botões na ponta** ("próximo corte" em `MAX_FOLHAS`, "desfazer" na raiz, "próxima poda" com a raiz sozinha, "desfazer" na árvore grande): desabilitados, sem erro no console. Conferido na verificação visual (tarefas 3 e 5).
3. **Tamanho sem erro de validação cruzada** (degraus de α repetido ou quase zero, e 1 folha): o gráfico fica vazio ali e o rótulo da posição atual diz "sem validação cruzada neste tamanho", nunca `NaN`. Teste `test_erro_na_curva_devolve_nulo_fora_da_grade` (tarefa 4).
4. **Empate de custo entre galhos** (vários α ≈ 2e−16 no começo do caminho): o elo mais fraco é o de menor índice de nó, como no `scikit-learn`. Coberto por `test_poda_no_node_reproduz_o_elo_mais_fraco_de_cada_degrau` (tarefa 4).
5. **Troca de tema e redimensionamento com a página aberta**: o gradiente troca para o do tema, e o desenho se refaz sem perder o estado (passo atual, região, coluna, posição da linha). Conferido na verificação visual (tarefas 3 e 5).

---

### Task 1: Gerador de dados, esqueletos das páginas e integração no livro

**Files:**
- Create: `scripts/gerar-dados-arvores.py`
- Create: `apoio/crescimento-da-arvore.html` (esqueleto)
- Create: `apoio/poda-da-arvore.html` (esqueleto)
- Create: `tests/test_apoio.py`
- Modify: `_quarto.yml` (`project.resources`, depois de `apoio/polinomios-e-ruido.html`)
- Modify: `content/cap12/index.qmd` (logo depois da linha do Colab)
- Regenerate: `notebooks/cap12-arvores-de-decisao.ipynb`

**Interfaces:**
- Produces, em `scripts/gerar-dados-arvores.py`:
  - `dados_crescimento() -> dict` → `{"anos": list[int], "rebatidas": list[int], "salario": list[float]}`, os 263 jogadores de `pd.read_csv("dados/Hitters.csv").dropna()`, na ordem do arquivo.
  - `dados_poda() -> dict` → o esquema abaixo.
  - `embutir(pagina: Path, dados: dict) -> None` → troca o conteúdo de `<script type="application/json" id="dados">…</script>` por `json.dumps(dados, ensure_ascii=False, separators=(",", ":"))`; `ValueError` se a tag não existir.
  - `main()` → embute nas duas páginas.
- Produces, em `tests/test_apoio.py`: `dados_embutidos(pagina: Path) -> dict` (lê o JSON da tag `id="dados"`).
- Esquema de `dados_poda()` (só tipos do Python, nada de `numpy`):
  ```
  n_treino: 132
  arvore:  {folhas, rss, mse}                       # a árvore grande, antes de qualquer degrau
  nos:     [{esq, dir, coluna, limiar, n, media, rss}]   # índices do tree_; esq = dir = -1 na folha; coluna/limiar null na folha
  degraus: [{no, alpha, ccp_alpha, folhas, rss, mse}]    # um por entrada 1..fim do cost_complexity_pruning_path; folhas/rss/mse = subárvore DEPOIS do degrau
  curva:   [{folhas, ccp_alpha, cv, desvio, mse_treino}] # a tabela `curvas` da 12.2, ordenada por folhas
  ```
  `rss` de um nó = `impurity × n_node_samples`; `alpha` = 132 × `ccp_alpha`.

- [ ] **Step 1: Escrever os testes dos dados embutidos**

Em `tests/test_apoio.py`, com `RAIZ`, `CRESCIMENTO = RAIZ / "apoio/crescimento-da-arvore.html"`, `PODA = RAIZ / "apoio/poda-da-arvore.html"` e `dados_embutidos`:

```python
def test_crescimento_embute_os_263_jogadores_de_hitters():
    d = dados_embutidos(CRESCIMENTO)
    h = pd.read_csv(RAIZ / "dados/Hitters.csv").dropna()
    assert d["anos"] == h["anos"].tolist()
    assert d["rebatidas"] == h["rebatidas"].tolist()
    assert d["salario"] == h["salario"].tolist()


def test_poda_embute_os_numeros_da_secao_12_2():
    d = dados_embutidos(PODA)
    assert d["n_treino"] == 132
    raiz = d["nos"][0]
    assert (raiz["coluna"], round(raiz["limiar"], 1)) == ("vezes_ao_bastao_carreira", 1452.0)
    de_3_para_2 = next(g for g in d["degraus"] if g["folhas"] == 2)
    no = d["nos"][de_3_para_2["no"]]
    assert (no["coluna"], round(no["limiar"], 1), no["n"], round(no["media"], 2)) == (
        "impulsionadas_carreira", 70.5, 54, 5.11)
    assert round(de_3_para_2["ccp_alpha"], 4) == 0.0677
    assert round(de_3_para_2["alpha"], 2) == 8.94
    assert round(de_3_para_2["mse"], 4) == 0.2935
    curva = pd.DataFrame(d["curva"]).set_index("folhas")
    assert round(curva.loc[3, "mse_treino"], 4) == 0.2258
    ordem = curva["cv"].sort_values()
    assert ordem.index[:2].tolist() == [4, 7]
    assert [round(v, 4) for v in ordem.iloc[:2]] == [0.2694, 0.2841]
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `.venv/bin/pytest tests/test_apoio.py -v`
Expected: FAIL (as páginas não existem).

- [ ] **Step 3: Criar os dois esqueletos de página**

Cada um com `<title>` (`Crescendo a Árvore` / `Podando a Árvore`), o bloco de tokens das Global Constraints, um cabeçalho com o título e uma frase sobre o conteúdo, `<script type="application/json" id="dados">{}</script>`, `<script id="nucleo">"use strict";</script>` e um `<script>` de interface vazio. É o mesmo esqueleto das irmãs; o corpo vem nas tarefas 2 a 5.

- [ ] **Step 4: Implementar `scripts/gerar-dados-arvores.py`**

`dados_poda()` refaz o preparo da 12.2 (`get_dummies(drop_first=True, dtype=float)`, `train_test_split(train_size=132, random_state=12)`, `DecisionTreeRegressor(random_state=12)`, `cost_complexity_pruning_path`, a grade `np.r_[0.0, np.sqrt(alfas[1:-1] * alfas[2:])]`, `GridSearchCV` em `grade[::-1]` com `KFold(6, shuffle=True, random_state=12)`, e `curvas` com `drop_duplicates("folhas")` e o MSE de treino de cada `ccp_alpha`, exatamente como os chunks `folhas-na-grade`, `curvas` e `teste` da 12.2).

Os `degraus` saem da poda do elo mais fraco feita à mão sobre o `tree_`, que precisa coincidir com o caminho do `scikit-learn` (conferido no planejamento: 116 degraus na árvore de 120 folhas do host, diferença máxima de α 1,4e−17):

```python
# r[i] = impurity[i] * weighted_n_node_samples[i] / weighted_n_node_samples[0]
# enquanto a raiz não for folha:
#   para cada nó i interno, alcançável (nenhum ancestral cortado) e não cortado, em ordem de índice:
#       custo = (r[i] - soma de r nas folhas do galho de i) / (folhas do galho - 1)
#   corta o de menor custo (estritamente menor: empate fica com o menor índice)
#   registra no, ccp_alpha = custo, e folhas/rss/mse da subárvore resultante
assert np.allclose(ccp_alphas_à_mão, caminho.ccp_alphas[1:], rtol=0, atol=1e-12)
assert np.allclose(mse_à_mão, caminho.impurities[1:], rtol=0, atol=1e-12)
```

- [ ] **Step 5: Gerar os dados no container**

Run: `docker compose run --rm --no-deps livro python scripts/gerar-dados-arvores.py`
Expected: termina sem `AssertionError`; as duas tags `id="dados"` ficam preenchidas.

- [ ] **Step 6: Rodar os testes de dados**

Run: `.venv/bin/pytest tests/test_apoio.py -v`
Expected: PASS nos dois.

- [ ] **Step 7: Integrar no livro**

Em `_quarto.yml`, depois de `- apoio/polinomios-e-ruido.html`, um comentário de uma linha por página e as entradas `- apoio/crescimento-da-arvore.html` e `- apoio/poda-da-arvore.html`. Em `content/cap12/index.qmd`, depois da linha do Colab e antes da epígrafe, duas linhas separadas por linha em branco, como em `content/cap07/index.qmd`:

```markdown
🎛️ [**Crescendo a árvore ↗**](../../apoio/crescimento-da-arvore.html): os jogadores no plano de anos e rebatidas, com a cor do salário. Arraste o ponto de corte e veja o RSS de cada posição; a cada passo, o melhor corte de cada folha aparece debaixo dela, e o que mais derruba o RSS vira galho.

🎛️ [**Podando a árvore ↗**](../../apoio/poda-da-arvore.html): a árvore grande perde um galho por vez, o que menos aumenta o RSS por folha perdida, com o antes e o depois lado a lado e o erro de validação cruzada contra o número de folhas.
```

Run: `.venv/bin/python scripts/gerar-notebooks.py && .venv/bin/pytest tests/ -q`
Expected: tudo passa, inclusive `test_toda_pagina_de_apoio_esta_publicada_e_linkada_certo` e `test_notebooks_estao_atualizados`.

- [ ] **Step 8: Commit**

```bash
git add scripts/gerar-dados-arvores.py apoio/crescimento-da-arvore.html apoio/poda-da-arvore.html tests/test_apoio.py _quarto.yml content/cap12/index.qmd notebooks/cap12-arvores-de-decisao.ipynb
git commit -m "feat(apoio): dados e esqueletos das páginas de crescimento e poda (cap. 12)"
```

---

### Task 2: Núcleo do crescimento

**Files:**
- Modify: `apoio/crescimento-da-arvore.html` (`<script id="nucleo">`)
- Modify: `tests/test_apoio.py`

**Interfaces:**
- Consumes: `DADOS` (o JSON da tag `id="dados"`, tarefa 1).
- Produces, no núcleo (funções puras; `X = {anos: number[], rebatidas: number[]}`, `y = salario.map(Math.log)`):
  - `const COLUNAS = ["anos", "rebatidas"]`, `const MAX_FOLHAS = 8`
  - `preparar(DADOS) -> {X, y}`
  - `cortesDaRegiao(linhas: number[], coluna: string, X, y) -> {cortes: number[], rss: number[]}`: pontos médios entre valores distintos vizinhos, em ordem crescente, e o RSS (8.3) de cada um.
  - `melhorCorte(linhas: number[], X, y) -> {coluna, corte, rss, queda} | null`: mínimo estrito (o primeiro corte em empate), `anos` antes de `rebatidas` em empate; `null` se nenhuma coluna tem dois valores distintos.
  - `raiz(X, y) -> Arvore`, `proximoCorte(arv: Arvore, X, y) -> Arvore` (nova árvore; corta a folha de maior `queda`, a de menor índice em empate), `crescer(X, y, folhas: number) -> Arvore`.
  - `Arvore = {nos: [{linhas, n, media, rss, coluna, corte, esq, dir}]}`, raiz no índice 0, `esq = dir = null` na folha; `rssTotal(arv) -> number` soma o `rss` das folhas.
  - `fmt(x: number, casas: number) -> string` em pt-BR.
- Produces, em `tests/test_apoio.py`: `no_node(pagina: Path, expressao: str) -> Any`, que monta um arquivo temporário com `const DADOS = <json>;`, o texto do núcleo e `console.log(JSON.stringify(<expressao>))`, roda `node` e devolve o `json.loads` da saída. Os testes que o usam levam `@pytest.mark.skipif(shutil.which("node") is None, reason="node só existe no host, não no container")`.

- [ ] **Step 1: Escrever os testes**

```python
def test_crescimento_no_node_segue_o_decision_tree_regressor():
    # para k de 2 a MAX_FOLHAS (lido do núcleo): os cortes da árvore do JS,
    # como conjunto de (coluna, corte), e o RSS total, contra
    # DecisionTreeRegressor(max_leaf_nodes=k, random_state=12) em anos e rebatidas
    # (feature -> nome da coluna, threshold, RSS = soma de (y - predict)²); RSS com atol 1e-9.
    ...


def test_curva_do_rss_no_node_bate_com_a_da_secao_12_1():
    # cortesDaRegiao(todas as linhas, coluna) para anos e rebatidas contra a mesma conta
    # em pandas (rss_do_corte da 12.1): cortes iguais, RSS com atol 1e-9,
    # e os mínimos 115,06 em 4,5 (anos) e 160,97 em 117,5 (rebatidas).
    ...


def test_segundo_corte_tem_as_quedas_da_secao_12_1():
    # depois de crescer(X, y, 2): melhorCorte dos novatos = rebatidas < 15,5, queda 9,34;
    # dos veteranos = rebatidas < 117,5, queda 23,73; rssTotal(crescer(X, y, 3)) = 91,33.
    ...


def test_regiao_sem_corte_possivel():
    # linhas com o mesmo anos e o mesmo rebatidas (dois jogadores repetidos, achados no teste
    # com groupby): cortesDaRegiao devolve listas vazias nas duas colunas, melhorCorte devolve null.
    ...


def test_formato_brasileiro():
    assert no_node(CRESCIMENTO, "fmt(1452, 1)") == "1.452,0"
    assert no_node(CRESCIMENTO, "fmt(0.26941, 4)") == "0,2694"
```

Os `...` são para o implementador escrever a comparação descrita no comentário; os valores esperados são os do comentário.

- [ ] **Step 2: Rodar e ver falhar**

Run: `.venv/bin/pytest tests/test_apoio.py -v -k "crescimento or curva or segundo or regiao or formato"`
Expected: FAIL (`ReferenceError` no node: as funções não existem).

- [ ] **Step 3: Implementar o núcleo**

O RSS de cada lado em duas passadas (média, depois a soma dos quadrados), como o (8.3). Nada de DOM no núcleo.

- [ ] **Step 4: Rodar e ver passar**

Run: `.venv/bin/pytest tests/test_apoio.py -v`
Expected: PASS. Se algum k falhar por empate exato entre dois cortes, **parar e relatar** em vez de mudar a regra de desempate para fazer o teste passar.

- [ ] **Step 5: Commit**

```bash
git add apoio/crescimento-da-arvore.html tests/test_apoio.py
git commit -m "feat(apoio): núcleo do crescimento da árvore, conferido contra o DecisionTreeRegressor"
```

---

### Task 3: Interface do crescimento

**Files:**
- Modify: `apoio/crescimento-da-arvore.html` (CSS, marcação e `<script>` de interface)

**Interfaces:**
- Consumes: núcleo da tarefa 2 (`preparar`, `cortesDaRegiao`, `melhorCorte`, `raiz`, `proximoCorte`, `rssTotal`, `fmt`, `COLUNAS`, `MAX_FOLHAS`).
- Estado da interface: pilha de `Arvore` (para "desfazer"), índice do nó selecionado, coluna selecionada, índice do corte arrastado.

- [ ] **Step 1: Carregar a skill `dataviz`** e definir o gradiente do salário: sobre `log(salario)`, legenda em mil dólares (67,5 a 2.460), com mais salário = mais contraste com o fundo nos dois temas (claro: do azul claro ao navy; escuro: o contrário). Passar as duas rampas pelo validador da skill.

- [ ] **Step 2: Montar o layout do spec**

Esquerda: a árvore com caixas e os fantasmas tracejados com a queda do RSS; o melhor em laranja com "← melhor"; folhas e RSS no título. Direita, em cima: o gráfico de dispersão `anos` × `rebatidas`, com os pontos no gradiente, os cortes feitos em linha sólida e o corte em teste em laranja arrastável. Direita, embaixo: a curva do RSS da região e da coluna selecionadas, com a tracejada cinza do RSS sem corte, o marcador do mínimo e o laranja da posição atual com o valor. Controles: botões de coluna, "ir ao melhor corte", "próximo corte", "desfazer". Quando o corte arrastado não é o melhor, o RSS dele aparece junto da folha selecionada.

- [ ] **Step 3: Verificar no navegador** (Claude in Chrome, `file://` da página), nos temas claro e escuro:

| Ação | Esperado na tela |
|---|---|
| abrir | 1 folha, RSS 207,15; fantasma `anos < 4,5` com −92,10 |
| "próximo corte" | 2 folhas, RSS 115,06; fantasmas `rebatidas < 15,5` −9,34 (novatos) e `rebatidas < 117,5` −23,73 ← melhor (veteranos) |
| selecionar veteranos, coluna `rebatidas`, "ir ao melhor corte" | linha em 117,5; marcador da curva em 48,98 |
| arrastar a linha nos novatos | o RSS do corte arrastado aparece junto dos novatos; o "← melhor" continua nos veteranos |
| "próximo corte" | 3 folhas, RSS 91,33; galho novo em laranja |
| avançar até `MAX_FOLHAS` | 8 folhas, RSS 59,25; "próximo corte" desabilitado |
| "desfazer" até a raiz | "desfazer" desabilitado |
| trocar o tema e redimensionar | gradiente do tema certo, estado preservado, nenhum ponto some |

Console sem erro em todas as ações. O −92,10 é a queda exata (o 207,15 − 115,06 dos valores arredondados daria 92,09), e 48,98 é o RSS dos veteranos depois do corte.

- [ ] **Step 4: Rodar a suíte**

Run: `.venv/bin/pytest tests/ -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apoio/crescimento-da-arvore.html
git commit -m "feat(apoio): crescimento da árvore — fantasmas, corte arrastável e salário em gradiente (seção 12.1)"
```

---

### Task 4: Núcleo da poda

**Files:**
- Modify: `apoio/poda-da-arvore.html` (`<script id="nucleo">`)
- Modify: `tests/test_apoio.py`
- Modify: `CLAUDE.md` (lista da suíte e seção `apoio/`)

**Interfaces:**
- Consumes: `DADOS` com o esquema da tarefa 1; `no_node` (tarefa 2).
- Produces, no núcleo (funções puras; `cortados` é um array de índices de nó):
  - `cortadosAte(dados, j: number) -> number[]`: os nós dos `j` primeiros degraus.
  - `subarvore(dados, cortados) -> {folhas: number, rss: number, mse: number}`.
  - `candidatos(dados, cortados) -> [{no, custo, folhas}]`: todo nó interno alcançável e não cortado, com `custo` = (rss do nó − rss das folhas do galho) / (folhas do galho − 1), na escala do RSS (= α); ordenados por custo crescente, empate pelo menor índice.
  - `erroNaCurva(dados, folhas: number) -> {cv, desvio, mse_treino} | null`.
  - `fmt(x, casas)` igual ao do crescimento.

- [ ] **Step 1: Escrever os testes**

```python
def test_poda_no_node_reproduz_o_elo_mais_fraco_de_cada_degrau():
    # para todo j: candidatos(dados, cortadosAte(dados, j))[0] tem no == degraus[j].no
    # e custo == degraus[j].alpha (rel 1e-9, abs 1e-12);
    # subarvore(dados, cortadosAte(dados, j + 1)).folhas == degraus[j].folhas.
    ...


def test_poda_no_node_no_degrau_de_3_para_2_folhas():
    # no estado com 3 folhas: o primeiro candidato é o nó impulsionadas_carreira ≤ 70,5,
    # custo 8,94 (2 casas), custo / 132 = 0,0677 (4 casas); subarvore dá mse 0,2258.
    ...


def test_erro_na_curva_devolve_nulo_fora_da_grade():
    # erroNaCurva(dados, 4) = {cv 0,2694, ...}; erroNaCurva(dados, 1) é null,
    # e também é null para um tamanho de degraus que não está em curva (achado no teste).
    ...
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `.venv/bin/pytest tests/test_apoio.py -v -k "poda_no_node or erro_na_curva"`
Expected: FAIL (`ReferenceError`).

- [ ] **Step 3: Implementar o núcleo**

- [ ] **Step 4: Rodar e ver passar**

Run: `.venv/bin/pytest tests/ -q`
Expected: PASS.

- [ ] **Step 5: Atualizar o `CLAUDE.md`**

Na frase de `make teste`, acrescentar `test_apoio.py` (as páginas de `apoio/` do capítulo 12: dados embutidos com os números das seções, e o núcleo de cada página conferido contra o `scikit-learn` com `node`, que só existe no host, então esses testes são pulados no container) e corrigir a contagem de testes e de arquivos pelo `pytest --collect-only -q`. Na seção `apoio/`, uma linha por página nova, dizendo que os dados da poda saem de `scripts/gerar-dados-arvores.py` rodado **no container** (a árvore grande difere entre host e container).

- [ ] **Step 6: Commit**

```bash
git add apoio/poda-da-arvore.html tests/test_apoio.py CLAUDE.md
git commit -m "feat(apoio): núcleo da poda, conferido degrau a degrau contra o caminho da seção 12.2"
```

---

### Task 5: Interface da poda

**Files:**
- Modify: `apoio/poda-da-arvore.html` (CSS, marcação e `<script>` de interface)

**Interfaces:**
- Consumes: núcleo da tarefa 4 (`cortadosAte`, `subarvore`, `candidatos`, `erroNaCurva`, `fmt`) e `DADOS`.
- Estado da interface: `j`, o número de degraus aplicados (0 = árvore grande, `degraus.length` = raiz sozinha).

- [ ] **Step 1: Carregar a skill `dataviz`** (gráfico do erro, cores das linhas nos dois temas).

- [ ] **Step 2: Montar o layout do spec**

Três colunas: **antes** (subárvore com `j` degraus, galho que vai cair em laranja), **galhos candidatos** (os cinco primeiros de `candidatos`, barras com "+custo", o primeiro em laranja como elo mais fraco) e **depois** (subárvore com `j + 1`, folha nova em laranja). Cada título mostra folhas, RSS e MSE de treino. Junto do degrau, "α = … · `ccp_alpha` = …". A árvore aparece em miniatura (pontos e traços) enquanto não couber com texto, e em caixas com `coluna ≤ limiar`, jogadores e média quando couber. Embaixo, o MSE de treino (cinza) e o erro de validação cruzada (azul) contra as folhas em escala log, um × no mínimo, um vazio onde `erroNaCurva` é `null` e uma linha laranja na posição atual com o rótulo. Controles: "próxima poda", "desfazer" e um controle deslizante sobre `j`, rotulado pelas folhas.

- [ ] **Step 3: Verificar no navegador**, nos temas claro e escuro:

| Ação | Esperado na tela |
|---|---|
| abrir | a árvore grande em miniatura, com as folhas de `arvore.folhas`; "desfazer" desabilitado |
| deslizar até 3 folhas | primeiro candidato `impulsionadas_carreira ≤ 70,5` (54 jog.) com +8,94; "α = 8,94 · `ccp_alpha` = 0,0677"; o depois com 2 folhas e MSE 0,2935 |
| olhar o gráfico | × em 4 folhas, 0,2694; a linha laranja segue o controle |
| deslizar até 4 folhas | rótulo com CV 0,2694; a árvore em caixas é a de `fig-podada` (raiz `vezes_ao_bastao_carreira ≤ 1.452,0`) |
| deslizar até um tamanho sem validação cruzada | rótulo "sem validação cruzada neste tamanho", sem `NaN` |
| "próxima poda" até a raiz | "próxima poda" desabilitado |
| trocar o tema e redimensionar | estado preservado, linhas legíveis |

Console sem erro.

- [ ] **Step 4: Verificação final**

Run: `.venv/bin/python scripts/gerar-notebooks.py && .venv/bin/pytest tests/ -q && make render`
Expected: suíte verde; `render OK`; `_book/apoio/crescimento-da-arvore.html` e `_book/apoio/poda-da-arvore.html` existem, e o link do `_book/content/cap12/index.html` abre cada uma.

- [ ] **Step 5: Commit**

```bash
git add apoio/poda-da-arvore.html
git commit -m "feat(apoio): poda da árvore — antes, galhos candidatos, depois e erro de validação (seção 12.2)"
```
