# Esquemas de orquestração (contratos de dados das revisões)

Adaptado de `pedrohcgs/claude-code-my-workflow`. As skills que distribuem revisão entre
subagentes (`/slide-excellence`, `/qa-quarto`) reduzem **achados tipados**, não markdown lido
no olho. O contrato legível está aqui; o contrato que vale é
[`finding-schema.json`](finding-schema.json), checado por `scripts/validate-findings.py`.

## 1. `FINDING`

Relatórios são **arrays JSON** (sem invólucro `{"findings": [...]}`). Exemplo ilustrativo:

```json
[
  {
    "id": "<sha1 de 'arquivo:linha:locus'>",
    "file": "content/cap09/02-regressao-logistica.qmd",
    "line": 34,
    "locus": "coeficientes da logística",
    "lens": "code-quality",
    "severity": "major",
    "rule": "knowledge-base.md: LogisticRegression é regularizada por padrão",
    "claim": "O texto compara os coeficientes com os da tabela 4.1 do ISLP, mas o chunk ajusta com C=1.0.",
    "evidence": "chunk `ajuste-logistica` chama LogisticRegression() sem C; beta_1 impresso = 0,0047",
    "failing_case": "Default, balance → default: com C=np.inf beta_1 = 0,0055, o valor do ISLP",
    "suggested_fix": "Ajustar com C=np.inf e dizer por quê.",
    "mechanical": false,
    "confidence": "high"
  }
]
```

- **`id` é calculado, nunca inventado:** `python3 scripts/validate-findings.py --id ARQUIVO LINHA LOCUS`. Não inclui a lente, então o mesmo defeito achado por duas lentes vira um só.
- **`rule` é obrigatório** e cita `CLAUDE.md`, a spec vigente, `.claude/rules/content-invariants.md` (INV-n) ou `.claude/rules/knowledge-base.md`. Achado sem regra é opinião.
- **`failing_case` é obrigatório:** o caso concreto em que a afirmação quebra. "Poderia ser mais claro" não valida.
- **`mechanical: true`** só para o que não muda resultado: erro de digitação, referência cruzada, chave de citação, formatação, rótulo. **Nunca** para definição, hipótese, fórmula, número reportado ou escolha pedagógica — isso volta para o professor.
- Validar antes de reduzir: `python3 scripts/validate-findings.py <relatorio>.json` (exit 0).

**Severidade** — vocabulário único entre skills:

| Termo local | `severity` |
|---|---|
| CRÍTICO / portão rígido / conta errada / erro conceitual | `blocker` |
| MAIOR / hipótese faltando / enganoso | `major` |
| MENOR / poderia ser mais claro | `minor` |
| detalhe cosmético | `nit` |

## 2. `SCORECARD`

Cada revisor fecha o relatório com uma linha:

```yaml
scorecard: { lens: pedagogy, blocker: 0, major: 2, minor: 5, score: 7, verdict: REVISE }
```

## 3. Predicados de portão

| Predicado | Regra |
|---|---|
| **PASS / APPROVED** | `blocker == 0` e `major == 0` |
| **REVISE** | `blocker == 0` e `major > 0` |
| **BLOCK** | `blocker > 0` |
| **convergiu** | uma rodada não produz nenhum `id` novo de `blocker`/`major` |

O veredito é função determinística dos achados, não um re-julgamento.

## 4. Portão contra alucinação do sintetizador

Quem sintetiza pode **rebaixar** ou **deduplicar** achados livremente, mas um `blocker` que
nenhuma lente levantou só entra se for confirmado por um subagente novo (contexto limpo) que
localize a evidência no arquivo. Sem evidência, vira nota `[JUIZ-ALUCINOU]` e o veredito é
recalculado sem ele.

## 5. `RUN_CONFIG`

Subagente não pergunta nada ao usuário. Toda escolha (arquivo, flags, pular lentes, rodadas
máximas) é coletada **antes** do disparo e ecoada como **Relatório de Pré-Voo**.

## 6. O que NÃO conta como achado

- **Simplificação didática deliberada** para graduação não é erro, a menos que engane.
- **Alternativa documentada e defensável** (ex.: `C=np.inf` declarado no texto, dado substituto registrado na spec) é explicada, não "corrigida".
- **Gosto de prosa** não é achado se não muda o sentido.
- **Conteúdo cortado de propósito** (INV-3: inferência, ISLP 7/11/13, CNN/RNN…) não é "lacuna".
- **Capítulos 1 a 5 fora dos guardas novos** (sem ISLP, sem estilo de figura) não são defeito.

## Ônus de evidência por lente

| Lente | O que o achado precisa trazer |
|---|---|
| `numeric-claim` | valor no texto, valor recalculado (comando + saída) e tolerância |
| `citation` | trecho do ISLP (seção/figura/tabela) que sustenta ou não a afirmação |
| `code-quality` | arquivo:linha e a entrada que dispara o defeito |
| `parity` | os dois artefatos (`.qmd` × HTML, livro × notebook) e o elemento que difere |
| `pedagogy` | o ponto exato em que o aluno perde o fio e por quê |
| `visual` | a página renderizada e o elemento que transborda/some |
