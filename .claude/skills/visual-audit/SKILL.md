---
name: visual-audit
description: Auditoria adversarial de layout de uma seção renderizada do livro — saídas que transbordam, DataFrames largos, figuras sem legenda/rótulo ou fora do estilo da casa, fadiga de callouts, tema escuro, celular. Use quando o professor disser "auditoria visual", "confere o layout", "isso transborda?", "como fica no celular?", "a figura some no escuro?". Não avalia texto nem pedagogia.
argument-hint: "[seção ou .qmd] [--capturas]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash", "Agent"]
disallowed-tools: ["Edit"]
---

# Auditoria visual de uma seção

## Passos

1. Resolva a seção para `content/capNN/MM-*.qmd` e `_book/content/capNN/MM-*.html`.
2. Se o `.qmd` for mais novo que o HTML: `make render` (serializado; espera a vez sozinho — CLAUDE.md). Docker parado → avise e audite só o fonte, dizendo isso no relatório.
3. **`--capturas`** (opcional): capture a página em desktop (1280 px), celular (390 px) e tema escuro com `scripts/captura-pagina.py`, na imagem oficial do Playwright (nada disso entra no `uv.lock`). Saída em `quality_reports/capturas/` (gitignorado); depois leia os PNGs com a ferramenta Read.

   ```bash
   docker run --rm -v "$PWD/_book:/site:ro" -v "$PWD/scripts:/scripts:ro" \
     -v "$PWD/quality_reports:/out" mcr.microsoft.com/playwright/python:v1.61.0-noble \
     bash -c "pip install --quiet playwright==1.61.0 && \
              python /scripts/captura-pagina.py content/capNN/MM-nome.html"
   ```
4. Chame o agente `slide-auditor` com o `.qmd`, o HTML e as capturas (se houver).
5. Salve o relatório em `quality_reports/<arq>_visual_audit.md`, organizado por subtítulo, com severidade e recomendação.

## Princípio de conserto: espaço antes de fonte

1. Encurtar a saída (`.head()`, menos colunas, setup em `include: false`).
2. Quebrar tabela/fórmula; `panel-tabset` para 4+ itens irmãos.
3. `::: {.columns}` para texto + figura pequena.
4. Reduzir `figsize`/`fig-width`.
5. Último recurso: fonte menor, nunca abaixo de 0,85em.

Conserto de cor ou de forma de gráfico passa pela skill `dataviz` e pelo
`estilo-figuras.mplstyle` — não por cor fixada no chunk.

A skill não edita o `.qmd`: o professor decide (ou roda `/qa-quarto` para os consertos mecânicos).
