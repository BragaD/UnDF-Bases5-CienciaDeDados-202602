---
name: qa-quarto
description: QA adversarial da renderização de uma seção do livro. Um agente crítico compara o .qmd com o HTML em _book/ (e com o notebook do capítulo) — chunks com erro, citações/refs não resolvidas, figuras ausentes ou fora do estilo, números da prosa divergentes, _freeze envenenado; um agente consertador aplica o que é mecânico e verifica sem renderizar; quem coordena renderiza uma vez por rodada; repete até convergir (máx. 5 rodadas). Use quando o professor disser "qa da seção", "confere o render", "o HTML bate com o qmd?", ou antes de dar push numa seção.
argument-hint: "[seção, ex.: 9.5, ou caminho do .qmd]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Agent"]
---

# QA adversarial: `.qmd` × página renderizada

**Filosofia:** o `.qmd` é o que o professor quis dizer; o HTML em `_book/` é o que o aluno vê.
Tudo o que se perde no caminho é defeito.

```
Pré-voo → [render] → crítico (rodada 1) → consertador → [render] → crítico (rodada 2) → … até convergir
```

**Quem renderiza é esta skill, não os agentes** — o `make render` é serializado neste
repositório (CLAUDE.md). O alvo espera a vez sozinho e sai com **75** se outro agente segurar o
lock por mais de ~7 minutos: nesse caso, rode `make render` de novo; não investigue, não mate
processo, **nunca** `make clean`.

## Portões rígidos

| Portão | Condição |
|---|---|
| Execução | nenhum chunk com erro |
| Citações / refs | nada `?@...` no HTML |
| Figuras | todo chunk que desenha gerou imagem, com o estilo da casa |
| Números | prosa = saída do código (superlativo inclusive) |
| Render fresco | HTML mais novo que o `.qmd` **e** com o conteúdo dele (`_freeze` envenenado) |

## Fase 0 — Pré-voo

1. Resolva a seção para `content/capNN/MM-*.qmd`, `_book/content/capNN/MM-*.html` e `notebooks/capNN-*.ipynb`.
2. Frescor: se o `.qmd` for mais novo que o HTML, `make render`. Se o conteúdo não bater mesmo com o HTML novo, `make refresh CAP=NN`. Docker parado → pare e avise (não audite HTML velho).
3. Teste o validador: `echo '[]' | python3 scripts/validate-findings.py`.
4. Ecoe o Relatório de Pré-Voo (arquivos, condições, rodadas máximas = 5).

## Fase 1 — Crítico

Agente `quarto-critic` com seção, rodada e condições. Relatório em
`quality_reports/<secao>_qa_critic_round1.md` + `.json`.

## Fase 2 — Consertos

Se não APROVADO: agente `quarto-fixer`. Ele aplica só `mechanical: true` e o que o crítico
especificou sem ambiguidade, verifica com `executar-secoes.py` e `pytest`, e regenera o
notebook; o que toca definição, fórmula, número reportado ou escolha pedagógica volta ao
professor como **Bloqueado**. Depois, esta skill roda `make render`.

## Fase 3 — Nova auditoria

Crítico de novo, **em contexto novo**, com o relatório anterior para deduplicar por `id`.

## Convergência

- Para quando uma rodada não traz nenhum `id` novo de `blocker`/`major`
  (`.claude/rules/orchestrator-protocol.md`).
- Teto: 5 rodadas → apresenta com pendências.
- **Duas vezes o mesmo `id`** (rodadas N e N+2) → escala ao professor em vez de remendar de novo.
- APROVADO ⇔ todos os portões passam.

## Relatório final

`quality_reports/<secao>_qa_final.md`: status dos portões, resumo por rodada, pendências e o
que ficou bloqueado para decisão do professor. Antes de apresentar, valide cada `.json` com
`python3 scripts/validate-findings.py`. Nunca faça commit.
