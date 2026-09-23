# Protocolo do orquestrador (o ciclo de revisão)

Adaptado de `pedrohcgs/claude-code-my-workflow`. Descreve como `/slide-excellence` e
`/qa-quarto` usam subagentes (`Agent`). Contratos de dados em
[`orchestration-schemas.md`](../references/orchestration-schemas.md).

## Proporcionalidade

Todo esse aparato é pesado. Aponte-o para o que vai ao aluno, não para cada rascunho.

| Superfície | Postura |
|---|---|
| Seção prestes a ir ao ar (push na `main` publica) | revisão completa, achados validados |
| Lista/atividade antes de distribuir | revisão completa + `domain-reviewer` |
| Rascunho, exploração, conversa | relato exato do estado, **cerimônia mínima** |

Relatar exatamente onde se chegou nunca é cortado.

## O ciclo

```
Skill invocada (com RUN_CONFIG)
  1. PRÉ-VOO — arquivo, condições detectadas, lentes que vão rodar
  2. VERIFICAR — `scripts/executar-secoes.py NN` + `pytest tests/` no .venv;
     render só se a lente precisar do HTML; falhou → para
  3. FAN-OUT — revisores em paralelo, numa única mensagem, cada um devolve FINDINGs
  4. REDUZIR — somar scorecards; predicado de portão → veredito; portão anti-alucinação
  5. CORRIGIR — só `mechanical: true`; o resto volta ao professor
  6. convergiu? (rodada sem id novo de blocker/major)
       SIM → resumo
       NÃO → volta ao 3 em contexto novo (teto: 5 rodadas)
```

- **Duas vezes o mesmo `id`** (rodadas N e N+2) → escala para o professor em vez de remendar
  uma terceira vez: o artefato está com a forma errada, não com a palavra errada.
- **Nada é automático.** Nenhum gatilho dispara este ciclo sozinho; o professor (ou a skill
  que ele chamou) inicia. "Pode fazer" dentro de uma skill dispensa a pausa final, **não**
  autoriza commit.
- **Render é serializado neste repositório** (ver CLAUDE.md): nenhum subagente de revisão
  renderiza; só quem coordena roda `make render`, uma vez, antes do fan-out. Revisores leem
  o HTML que existe e, se ele for mais velho que o `.qmd`, dizem isso.
- Relatórios vão para `quality_reports/` (gitignorado).
