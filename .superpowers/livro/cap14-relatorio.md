# Capítulo 14 — Árvores de Decisão: relatório

**Status: pronto.** 7 arquivos preenchidos, nenhum criado/renomeado. `make render` → `render OK (tentativa 1)`; `make teste` → 24/24. Cinco figuras, todas abertas e conferidas contra a prosa.

## Números que saíram (todos da saída, não da memória)

- Entropia: `[1.0]`→0,000000; `[0.5,0.5]`→1,000000; `[0.25,0.75]`→0,811278; 4 classes iguais→2 bits; 3 classes→1,584963.
- Partição sobre os 14: `level` **0,693536** (vence), `tweets` 0,788450, `lang` 0,860132, `phd` 0,892159. Entropia antes: **0,940286** (9 True / 5 False) → ganho de 0,246750.
- Sêniores (H=0,970951): `tweets` **0,000000**, `lang` 0,400000, `phd` 0,950978. Juniores: `phd` **0,000000**.
- Atributo-armadilha: coluna `id` com 14 valores → **0,000000**, vence `level` por goleada. Demonstrado, não só afirmado.
- Árvore construída = a da figura; **14/14** no treino; `Intern` → `True` via `default_value`.
- Guloso ≠ ótimo (8 linhas, alvo `a != b`): `a`=`b`=1,000000, `c`=0,811278 → raiz `c`, **6 folhas**; sem `c`, **4 folhas**; ambas 8/8.
- Floresta (seed 12, 100 árvores): raízes `level` 37 / `tweets` 31 / `lang` 18 / `phd` 13 / 1 folha pura. Votos 78-22, 27-73, 71-29.
- Medição sintética (seed 0, 20 repetições, 200 treino com 15% de ruído / 1.000 teste limpo): árvore no próprio treino **0,9970**; teste — árvore **0,8239**, só bagging **0,9076**, floresta 2 de 8 **0,9165**, floresta 3 de 8 **0,9284**. Custo: ~5 s.

## O que ficou de fora, e por quê

- **Sem `mermaid`.** Nenhum capítulo usa; as árvores são desenhadas em matplotlib puro, coerente com o resto do livro.
- **Leave-one-out sobre os 14 candidatos**: medido (árvore 10/14, floresta 9/14) e **descartado** — 14 pontos não distinguem método de sorteio. Virou callout dizendo isso, e a medição honesta foi para o conjunto sintético.
- **Poda** só aparece no callout de biblioteca (`ccp_alpha`, `max_depth`): o Grus não implementa, e implementar seria "melhorar" o código dele.

## Preocupações

- A **armadilha do `print` no import** foi tratada com `#| output: false` nos três chunks que importam `scratch.decision_trees` (§14.4, §14.5, §14.6), com callout explicando o efeito colateral. Conferido: nenhuma das 16 casas decimais vaza para o HTML.
- O experimento sintético da §14.6 é **invenção minha** (o Grus só afirma que árvores sobreajustam). Achei que valia: sem ele, a seção seria a única do capítulo a pedir fé. Se destoar, corta-se sem afetar o resto.
- O `render` reclamou de edição concorrente em `content/cap08/*` na primeira rodada — outro agente, não este capítulo. A segunda rodada saiu limpa.
