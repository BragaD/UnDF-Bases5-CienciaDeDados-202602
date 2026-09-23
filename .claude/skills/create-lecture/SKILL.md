---
name: create-lecture
description: Cria uma nova seção (ou preenche um stub) do livro Quarto de Bases 5 — Ciência de Dados a partir do ISLP (@james2023), com callout de correspondência, notação do livro-fonte, código scikit-learn com semente, figura com o estilo da casa, quadros .funcao e registro no LIVRO/_quarto.yml. Use quando o professor disser "cria a seção X", "escreve a 10.3", "preenche o stub de bootstrap", "nova seção sobre Y". Colaborativo e em lotes — não despeja a seção inteira de uma vez. Para um capítulo inteiro, o processo é o do CLAUDE.md (plano em docs/superpowers/plans/, implementador, revisor).
argument-hint: "[seção, ex.: 10.3 ou 'bootstrap']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Agent", "Skill"]
---

# Criar uma seção do livro

Colaborativo e iterativo: **o professor conduz, o Claude é parceiro de raciocínio.** O modelo
de estilo é o **capítulo 6** (`content/cap06/`, lido inteiro): abertura de seção sem "nesta
seção veremos", chunk de setup aplicando `estilo-figuras.mplstyle`, posição de `.conceito`,
`.exemplo` e `.funcao`. Para as seções com ISLP, o capítulo mais recente já escrito mostra o
callout de correspondência e o uso do `scikit-learn`.

Esta skill é para **uma seção**. Um capítulo inteiro segue o processo do `CLAUDE.md`: plano em
`docs/superpowers/plans/2026-09-10-islp-capNN.md`, implementador, revisor que lê o capítulo
inteiro, correções.

## Restrições (inegociáveis)

1. Ler a spec vigente, `.claude/rules/knowledge-base.md` e `.claude/rules/content-invariants.md` **antes** de escrever.
2. Notação do ISLP, conferida contra o registro; dado em português (colunas `snake_case` sem acento, categorias com acento).
3. Motivação antes da fórmula (INV-12); exemplo com o dado da seção do ISLP em até dois parágrafos de cada definição.
4. Callout de correspondência com o número **do ISLP** (INV-2); escopo da spec (INV-3); **nada de inferência**.
5. `scikit-learn` para ajustar; nada implementado à mão que o ISLP não mostre; biblioteca proibida fora (INV-7).
6. Semente no gerador que sorteia (INV-5); caminhos a partir da raiz (INV-6); **todo número da prosa sai da saída de um chunk**, superlativo inclusive (INV-8); o setup reconstrói o que a seção herda (INV-9).
7. Ao menos uma figura que carrega a ideia, com o estilo da casa (INV-11). **Carregue a skill `dataviz` antes de escrever o código de qualquer gráfico.**
8. `.funcao` na primeira aparição de cada função/método/atributo no capítulo.
9. No máximo dois blocos coloridos seguidos (INV-12).
10. **O texto é sobre o conteúdo (INV-13):** o ISLP aparece só no callout de correspondência — nada de "é assim que o ISLP abre", "os autores usaram", "este material não instala"; nenhuma abertura que resume a seção anterior. A seção abre pelo assunto.
11. **Lotes de uma subseção (`##`) por vez**, mostrando ao professor antes de seguir.

## Fase 0 — Pré-voo (obrigatório)

Leia: `CLAUDE.md`; a spec (a linha do capítulo na ementa); o plano do capítulo, se existir;
`.claude/rules/knowledge-base.md`; o `index.qmd` do capítulo; a seção anterior (fim) e a
seguinte (começo); o stub, se existir; a seção do ISLP (`pdftotext -layout
livros/ISLP_website.pdf` — ver o bloco "Acesso ao ISLP" em `.claude/agents/domain-reviewer.md`;
**nunca** copie texto dele para o repositório). Confira o de-para das colunas em
`dados/README.md`.

Produza:

```markdown
## Relatório de Pré-Voo
**Seção:** N.M — <título> · arquivo: content/capNN/MM-nome.qmd (novo | stub)
**ISLP:** seção(ões) X.Y — figuras/tabelas canônicas: <…>
**Callout:** "Esta seção corresponde à seção X.Y de @james2023."
**Notação:** novos: […] · reutilizados: […] (seção de origem) · conflitos: nenhum | […]
**Posição no arco (uso interno, não vira prosa):** a anterior terminou em … ; a próxima precisa de …
**Objetivo pedagógico:** <uma frase>
**Dados:** dados/<arquivo>.csv (colunas traduzidas: …) | precisa baixar (scripts/baixar-dados.py)
**Figura que carrega a ideia:** <qual, e de que figura do ISLP ela reproduz a ideia>
**Decisões herdadas a reconstruir no setup:** <…> | nenhuma
**Fora do escopo (INV-3):** <o que o ISLP tem e não entra — inferência, lab com statsmodels…>
```

Confirme o objetivo com o professor antes da Fase 1.

## Fase 1 — Estrutura

Proponha os `##` da seção: pergunta de abertura → conceito → exemplo com o dado → código →
figura → armadilha. Liste figuras, a página de `apoio/` (só se a lição for o que muda ao girar
um botão — critério da spec) e a notação nova.
**PORTÃO: o professor aprova antes da Fase 2.**

## Fase 2 — Redação em lotes

Uma subseção por vez. Chunk de setup `include: false` como no cap. 6. Se o arquivo é novo,
entre primeiro em `LIVRO` (`scripts/gerar-stubs.py`) e no `_quarto.yml` (INV-1). Se a seção
substitui um stub, remova o aviso de construção.

## Fase 3 — Código e figuras

Rode antes de escrever o número na prosa:

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0
.venv/bin/python scripts/executar-secoes.py NN
.venv/bin/python scripts/gerar-notebooks.py
.venv/bin/pytest tests/ -q
```

**Não renderize** — o `make render` é serializado e é de quem coordena.

## Fase 4 — Revisão

- `/humanize <arquivo> --so-novo` e corrigir os achados de gravidade alta.
- `/devils-advocate` na seção.
- Agente `domain-reviewer` (substância, referência ISLP).
- Agente `verifier` (suíte, execução, notebook, privacidade).
- Atualize `.claude/rules/knowledge-base.md` com notação e armadilhas novas.

## Checklist final

```
[ ] Registrada em LIVRO e no _quarto.yml; executar-secoes e pytest verdes
[ ] Callout de correspondência com o número do ISLP
[ ] Toda definição com motivação + exemplo; nada de inferência
[ ] Sementes no gerador certo; caminhos a partir da raiz
[ ] Todo número (e superlativo) da prosa sai de um chunk
[ ] Figura com o estilo da casa; .funcao na primeira aparição
[ ] 2–3 perguntas ao leitor; ≤ 2 blocos coloridos seguidos
[ ] Nenhum meta-texto sobre o ISLP/o material; abertura sem ponte com a seção anterior
[ ] Notebook regenerado
[ ] knowledge-base.md atualizada
[ ] humanize + devils-advocate + domain-reviewer + verifier rodados
```

## Ver também

`/scaffold-exercises` (lista para a seção) · `/qa-quarto` (renderização) · `/slide-excellence` (revisão completa).
