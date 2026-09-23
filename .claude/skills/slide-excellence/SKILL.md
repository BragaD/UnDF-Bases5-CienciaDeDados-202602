---
name: slide-excellence
description: Revisão completa e multiagente de uma seção ou capítulo do livro (visual + pedagogia + texto, e condicionalmente substância/ISLP, renderização e voz). Use quando o professor disser "revisão completa", "passa o pente fino", "revisa tudo antes da aula", "excelência", ou antes de publicar uma seção. Para uma lente só, use /visual-audit, /devils-advocate ou /humanize, ou chame o agente direto.
argument-hint: "[seção ou .qmd, ou 'capNN'] [--rapido] [--sem-substancia] [--com-voz]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash", "Agent"]
---

# Revisão de excelência

Vários agentes analisam o arquivo de forma independente; os achados tipados são reduzidos num
veredito. (O nome vem do workflow de slides de origem; aqui o objeto é a seção do livro.)

## Passo 1 — Arquivo

Resolva `$ARGUMENTS`: "9.5" → `content/cap09/05-*.qmd`; `capNN` → todos os `.qmd` do capítulo
(uma rodada por arquivo). Leia o arquivo e o `CLAUDE.md`.

## Passo 2 — Pré-voo: detectar condições

```bash
F="<arquivo>"
html="_book/${F%.qmd}.html"
has_code=$(grep -c '^```{python}' "$F")
has_plot=$(grep -c 'plt\.' "$F")
has_html=$([ -f "$html" ] && [ "$html" -nt "$F" ] && echo fresco || echo ausente-ou-velho)
cites_islp=$(grep -c '@james2023' "$F")
is_stub=$(grep -c -i 'em construção' "$F")
```

Ecoe:

```
Arquivo:        content/cap09/05-avaliando-um-classificador.qmd
Chunks Python:  11    Chunks que desenham: 3    HTML: fresco
Cita ISLP:      2     Stub: não
Lentes:         visual, pedagogia, texto, substância, renderização  (puladas: voz — sem --com-voz)
```

Stub → pare: não há o que revisar; sugira `/create-lecture`. HTML velho → **não** renderize
de dentro dos agentes; se a lente E for necessária, rode `make render` uma vez, aqui, antes do
fan-out (o render é serializado — CLAUDE.md).

## Passo 3 — Lentes em paralelo (uma única mensagem)

**Sempre:**
- **A · Visual** — agente `slide-auditor` → `quality_reports/<arq>_visual_audit.md`
- **B · Pedagogia** — agente `pedagogy-reviewer` → `quality_reports/<arq>_pedagogy_report.md`
- **C · Texto** — agente `proofreader` → `quality_reports/<arq>_proofread_report.md`

**Condicionais:**
- **D · Substância** — agente `domain-reviewer` (referência ISLP). Padrão: **ligado** sempre que houver fórmula, número ou citação; `--sem-substancia` desliga.
- **E · Renderização** — agente `quarto-critic` (uma rodada, sem consertador) se o HTML estiver fresco; se estiver velho, avise e sugira `/qa-quarto`.
- **F · Voz** — agente `humanize-auditor` só com `--com-voz`.

Se o professor já rodou uma dessas lentes nesta sessão no mesmo arquivo, reaproveite o relatório.

`--rapido`: em vez do fan-out, um único agente lê o arquivo e cobre A–D superficialmente
(mais barato, menos profundo).

## Passo 4 — Reduzir

Cada lente fecha com um `scorecard`; some os achados por severidade
(`.claude/references/orchestration-schemas.md`). O veredito é o predicado de portão
(`blocker > 0` → BLOCK; `major > 0` → REVISE; senão PASS). Um `blocker` que nenhuma lente
levantou passa pelo portão anti-alucinação (§4) antes de entrar.

```markdown
# Revisão de excelência: <arquivo>
**Detectado:** Python=N | figuras=N | HTML=fresco | ISLP=N
**Lentes:** A, B, C, D (puladas: E [HTML velho], F [sem --com-voz])

## Qualidade geral: EXCELENTE / BOA / PRECISA TRABALHO / FRACA

| Dimensão | blocker | major | minor |
|---|---|---|---|

### Críticos (antes da aula)
### Maiores (próxima revisão)
### Próximos passos
```

| Qualidade | blocker | major |
|---|---|---|
| Excelente | 0 | 0–3 |
| Boa | 0 | 4–10 |
| Precisa trabalho | 1–3 | qualquer |
| Fraca | 4+ | qualquer |

Salve em `quality_reports/<arq>_excellence.md`. Nenhum arquivo-fonte é editado.

## Passo 5 — Custo

Informe quantos agentes rodaram e sugira as lentes individuais quando só uma dimensão
interessar.
