# Reescrita em numpy — instruções para planejadores, implementadores e revisores

Leia **nesta ordem**, antes de qualquer coisa:

1. `docs/superpowers/specs/2026-09-06-reescrita-numpy-design.md` — a decisão e as regras. É a fonte.
2. `CLAUDE.md` — convenções da casa (citação, sementes, caminhos, chunks, notebooks).
3. `content/cap09/` inteiro — o modelo de estilo do livro (ainda em Python puro; o que se copia é a **forma**).
4. O seu capítulo inteiro: `content/capNN/*.qmd`, e o módulo correspondente em `scratch/` (o código do Grus em listas, que a seção hoje espelha).
5. `scratch_np/` — os módulos do andaime já existem (`gradient_descent`, `machine_learning`, `probability`, `statistics`); os contratos entre capítulos estão na spec.
6. Os capítulos são reescritos **em sequência** (6, 7, 8, …). Se o seu capítulo não é o 6, leia também os capítulos já reescritos antes dele (`git log --oneline -- content/`, e os planos `2026-09-06-numpy-capNN.md` anteriores): o bloco "De listas a arrays" do cap. 7, o jeito de apresentar `rng`, `axis`, máscaras e `@` já foi decidido lá — reaproveite a forma e o vocabulário, e importe de `scratch_np/` o que já existe em vez de reescrever.

Ambiente de verificação (host, sem Docker):

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/executar-secoes.py NN          # cada .qmd num kernel próprio (como o site)
.venv/bin/python scripts/gerar-notebooks.py             # regenera os 17 notebooks
.venv/bin/python scripts/executar-notebooks.py capNN    # o capítulo num kernel só (como a aula)
.venv/bin/pytest tests/ -q
```

**Ninguém além do orquestrador roda `make render`, `make refresh`, `make offline` ou `make clean`.**

## O plano de cada capítulo (`docs/superpowers/plans/2026-09-06-numpy-capNN.md`)

Escrito pelo planejador; executado pelo implementador; conferido pelo revisor. Em português, no tom da casa. Seções obrigatórias:

### 1. Inventário

Por arquivo `.qmd` do capítulo (index incluído): os chunks executáveis (label, o que fazem, o que importam de `scratch.`), os números que a prosa afirma e de onde saem (`assert`, saída de célula, frase), as figuras, e **as frases que descrevem o código em listas/Python puro** e vão deixar de ser verdade. Cite as frases literalmente — é essa lista que o revisor vai conferir.

### 2. O módulo `scratch_np/<nome>.py`

O **código completo** do módulo, pronto para salvar, obedecendo aos contratos da spec (assinaturas fixadas ali não mudam). Convenções: `X (n, d)`, `y (n,)`, parâmetros `(d,)`, `dtype=float`, `rng: np.random.Generator` obrigatório em toda função estocástica, `ddof=1` onde o Grus usa a fórmula amostral. `assert`s no nível do módulo, como o Grus faz — o render é o teste. Dados hard-coded do Grus entram por reexportação (`from scratch import <modulo> as _grus` + `np.array(...)`), nunca copiados; se o módulo do Grus desenha no import, `plt.close('all')` em seguida.

Se o capítulo não tem módulo (cap. 6, cap. 8 já tem o do andaime), diga isso e siga.

### 3. Plano seção a seção

Para cada `.qmd`, na ordem do `_quarto.yml`:

- **Chunks**: para cada chunk, o código **novo por inteiro** (ou "mantém" com o motivo — um `eval: false` de download, por exemplo). Chunks de figura recebem arrays direto. A seção que ensina o algoritmo escreve o código inline; as seguintes importam de `scratch_np.` **o mesmo código**, e a prosa diz isso.
- **Prosa**: cada frase que muda, no formato `antes → depois`, ou `sai` com motivo. Inclua o texto do callout de fechamento `scikit-learn` (que fica, comparando agora com a versão em numpy). Frases que continuam valendo não precisam aparecer.
- **Números a recalcular**: quais, e por que mudam (sorteio novo, `ddof`, vetorização não muda número mas muda tempo). O implementador executa e escreve o número real; o plano marca onde.
- **Semente**: qual `default_rng(...)` cada chunk estocástico usa, e onde a prosa a justifica.
- **Objetivos do `index.qmd`**: só o que fala de Python puro/listas muda.

### 4. Riscos e decisões

`assert`s do Grus que podem deixar de valer; tempos de execução; o que fica como laço e por quê (o laço que *é* o algoritmo fica; o laço sobre pontos vira array); qualquer desvio da spec, com a razão.

### 5. Verificação

Os quatro comandos acima, mais: acrescentar `NN` a `CAPITULOS_NUMPY` em `tests/test_scratch_np.py` e registrar em `PYTHON_PURO_PERMITIDO`/`RANDOM_PERMITIDO`, com motivo, o que for exceção deliberada.

## Regras para o implementador

- Execute o plano. Onde ele estiver errado (um `assert` que não fecha, um número diferente), **corrija e registre** a diferença no fim do plano, numa seção "Desvios na implementação" — não afrouxe `assert` sem escrever por quê.
- Nunca edite `scratch/`. Nunca importe `sklearn` em chunk executável. Nunca deixe `random` da stdlib ou `np.random.seed`.
- Todo número que a prosa afirma foi lido da saída real, nesta execução.
- Ao terminar: `gerar-notebooks.py`, `executar-secoes.py NN`, `executar-notebooks.py capNN`, `pytest tests/ -q` — os quatro verdes. Só então acrescente `NN` a `CAPITULOS_NUMPY`. Commit atômico do capítulo (`.qmd` + módulo + notebooks + teste), mensagem `feat(capNN): reescrita em numpy — <resumo>`. Não faça `git add -A`: adicione os caminhos.

## Regras para o revisor

A pergunta única do autor: **o texto condiz com o que foi reescrito?** Leia cada `.qmd` do capítulo de ponta a ponta e execute-o (`executar-secoes.py NN`). Procure: frase que descreve código que não existe mais (listas, `zip`, `sum(...)`, "Python puro", "lento", "trinta linhas"); número na prosa que não bate com a saída; `import` de `scratch.` sobrando; nome de função citado que o módulo não tem; semente sem justificativa; callout `scikit-learn` comparando com o código antigo; objetivo do `index.qmd` desatualizado; e o inverso — código novo que a prosa não explica (um `axis=0`, uma máscara booleana, um `@`) num ponto em que o aluno vê aquilo pela primeira vez. Devolva uma lista numerada de discrepâncias com arquivo, trecho e correção sugerida. Não edite os arquivos; quem corrige é o implementador.

## Briefing para o planejador

*(Acrescentado em 2026-09-07. A partir do cap. 8 o planejador roda em Opus, com o mapa do capítulo já pronto no prompt do orquestrador; esta seção é o contexto comum que esse prompt assume.)*

### O que o plano é, em uma frase

O plano é o capítulo reescrito **por antecipação, em forma de instruções verificáveis**: o implementador não deve precisar decidir nada de conteúdo — só executar, medir e registrar. Se uma decisão ficou em aberto no plano, ela vai ser tomada às pressas por quem implementa, e o revisor vai apontar.

### Como ler o capítulo sem gastar contexto à toa

- Leia cada `.qmd` **uma vez**, por faixas de linhas (`sed -n 1,120p`), e anote o inventário à medida que lê. Não releia arquivos inteiros para conferir um detalhe: use `grep -n`.
- O módulo do Grus em `scratch/` é o espelho do capítulo em listas: leia-o para as assinaturas e os `assert`s, não para copiar prosa.
- Experimentos no scratchpad são bem-vindos **quando decidem algo** (um `assert` fecha com `ddof=1`? qual número sai com `default_rng(12)`? a versão vetorizada reproduz o resultado da versão em listas?). Registre a saída no plano. Não meça tempo "por curiosidade": só quando a prosa vai afirmar algo sobre tempo.
- Não escreva no plano o que já está na spec ou nestas instruções; cite a seção.

### O que os capítulos anteriores já fixaram (vocabulário e forma)

- **Cap. 6 (6.1)** apresentou `np.loadtxt`/`np.genfromtxt`, `shape`, `dtype`, `X[:, j]`, `v - w`, `2 * v`, `.max()/.min()/.mean()`, `np.isnan`, e o `nan` silencioso do `genfromtxt`. Não voltou a máscaras, `axis` nem broadcasting: deixou-os para a 7.1.
- **Cap. 7 (7.1)** abre com o bloco `## De listas a arrays`, com os `###` *Forma e tipo*, *Índices, fatias e colunas*, *Máscaras booleanas*, *Broadcasting*, *`axis`: em que direção reduzir* e *O laço que some*. Tudo o que um capítulo posterior usa dessas seis coisas está apresentado ali e **pode ser assumido** — cite o bloco em vez de reexplicar. O cap. 7 também fixou o callout *Uma afirmação sobre dado aleatório precisa de semente* como forma de justificar o `rng = np.random.default_rng(...)` na primeira vez que ele aparece numa seção, e é o dono de `scratch_np/working_with_data.py` (`rescale`, `pca`, `transform`, ...).
- **Andaime** (`scratch_np/`): `gradient_descent.gradient_step(v, gradient, step_size)` e `minibatches(n, batch_size, rng, shuffle=True)` (gera arrays de índices); `machine_learning.split_data(data, prob, rng)`, `train_test_split(xs, ys, test_pct, rng)`, `accuracy/precision/recall/f1_score(tp, fp, fn, tn)`; `probability.normal_cdf(x, mu, sigma)` e `inverse_normal_cdf(p, mu, sigma, tolerance)` vetorizadas; `statistics.num_friends`, `daily_minutes`, `num_friends_good`, `daily_minutes_good` como arrays float.
- **Forma dos capítulos** (cap. 9 é o modelo): abertura curta; `::: {.callout-note}` de correspondência ("Esta seção corresponde a *Título*, do capítulo N de @grus2019."); `::: {.conceito}` para a ideia central, `::: {.exemplo}` para o comentário de código; chunks com `#| label:`; figuras com `#| fig-cap:`; callout de fechamento `::: {.callout-tip collapse="true"}` com `## Na prática: \`scikit-learn\`` e um bloco ```` ```python ```` que **não executa**.

### Armadilhas conhecidas (cada uma já custou uma rodada de revisão)

1. **Cada `.qmd` é um kernel.** Todo arquivo importa o que usa (`import numpy as np`, `from scratch_np.x import ...`), mesmo que a seção anterior já tenha importado. O notebook de aula (um kernel só) não pega isso; `executar-secoes.py` pega.
2. **Chunk começa em coluna zero.** Uma classe ou função não pode ser partida entre chunks (`test_nenhum_chunk_comeca_com_linha_indentada`).
3. **`#| error: true` não sobrevive ao gerador de notebooks** — a célula estoura na aula. Para mostrar um erro, `try/except` imprimindo a mensagem.
4. **Módulos que desenham no import** (`scratch.statistics`, `scratch.probability`, `scratch.working_with_data`): nunca importá-los num `.qmd` reescrito. O dado que eles carregam entra por `scratch_np/` (reexportação com `plt.close('all')`).
5. **`ddof`.** O Grus usa $n-1$ em `variance`/`standard_deviation`. `np.std` sem `ddof` usa $n$. Onde o texto afirma um número, o plano diz qual `ddof` reproduz o Grus e o experimento comprova.
6. **Igualdade exata de float** em `assert` do Grus (`== (-5, 3)`, soma sobre um `set`) vira `np.isclose`/`np.allclose` **com a explicação na prosa** — não silenciosamente.
7. **Sorteio novo, número novo.** `random.seed(12)` + `random.shuffle` e `default_rng(12).permutation` não dão a mesma divisão. Todo número que vem de sorteio recebe a marca `[RECALCULAR]` no plano, com o valor medido no scratchpad quando possível.
8. **"Python puro" na prosa** de um capítulo reescrito dispara `test_capitulo_numpy_sem_python_puro_na_prosa`; só sobrevive registrado em `PYTHON_PURO_PERMITIDO` com motivo (contraste deliberado com os caps. 1–5). Sinônimos ("em listas", "laço a laço") não disparam teste, mas o revisor procura.
9. **Velocidade.** Não afirmar "mais rápido" sem medida; quando medir, dizer o que domina (leitura de arquivo, por exemplo, não a conta).
10. **O callout `scikit-learn` fica**, mas o texto compara com a versão em numpy: "sete linhas contra trinta" e "força bruta em Python puro" não valem mais.
11. **Nada de `scipy`** (não é dependência declarada) e nada de `np.linalg.lstsq`/`np.polyfit` como implementação — a spec explica.

### Formato de cada entrada do plano seção a seção

Para cada chunk, nesta ordem e sem omitir campos:

```
#### chunk `label-do-chunk` — mantém | reescreve | sai | novo
Motivo: <uma linha>
Código novo (completo):
```{python}
#| label: ...
...
```
Saída esperada: <a saída literal, ou "[RECALCULAR] — depende de rng" com o valor medido se houver>
Prosa afetada:
- antes: "<frase literal>" → depois: "<frase nova>"
- sai: "<frase literal>" — motivo
```

A tabela de **números a recalcular** de cada seção lista: onde o número aparece (arquivo, linha aproximada, se é `assert`, saída de célula ou frase), por que muda, e o valor novo medido ou `[RECALCULAR]`.
