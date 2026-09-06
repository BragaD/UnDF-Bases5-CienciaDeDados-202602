# Reescrita em numpy — instruções para planejadores, implementadores e revisores

Leia **nesta ordem**, antes de qualquer coisa:

1. `docs/superpowers/specs/2026-09-06-reescrita-numpy-design.md` — a decisão e as regras. É a fonte.
2. `CLAUDE.md` — convenções da casa (citação, sementes, caminhos, chunks, notebooks).
3. `content/cap09/` inteiro — o modelo de estilo do livro (ainda em Python puro; o que se copia é a **forma**).
4. O seu capítulo inteiro: `content/capNN/*.qmd`, e o módulo correspondente em `scratch/` (o código do Grus em listas, que a seção hoje espelha).
5. `scratch_np/` — os módulos do andaime já existem (`gradient_descent`, `machine_learning`, `probability`, `statistics`); os contratos entre capítulos estão na spec.

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
