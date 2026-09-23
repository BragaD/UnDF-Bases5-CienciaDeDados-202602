---
name: scaffold-exercises
description: Monta uma lista de exercícios para capítulos do livro — no formato manuscrito (conceitual e de conta, com gabarito, Quarto → PDF via Typst em duas versões) ou computacional (lista-comp, notebook do Colab derivado do .qmd, sem gabarito). Use quando o professor disser "monta uma lista sobre X", "exercícios para o capítulo 9", "questões de fixação", "gera lista com gabarito", "lista computacional". O gabarito nunca é versionado nem publicado.
argument-hint: "[capítulos ou tema] [--formato manuscrita|computacional] [--nivel intro|core|avancado] [--quantidade N] [--dataset caminho]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
---

# `/scaffold-exercises` — lista de exercícios

Dois formatos, com os modelos em `atividades/`:

| Formato | Modelo | Fonte | O aluno recebe | Gabarito |
|---|---|---|---|---|
| **manuscrita** | `atividades/lista-01-revisao.qmd` | um `.qmd` com as respostas em `::: {.content-visible when-meta="gabarito"}` | PDF em `atividades/publico/` | PDF `*-gabarito.pdf` em `atividades/`, **nunca** versionado |
| **computacional** | `atividades/lista-comp-01.qmd` | um `.qmd` com células de resposta marcadas (`# sua resposta` / `*sua resposta aqui*`) | notebook gerado por `scripts/gerar-lista.py` | não há, por decisão do autor (`docs/superpowers/specs/2026-09-13-listas-computacionais-design.md`) |

**Privacidade (INV-14):** o repositório é público. `atividades/lista-*.qmd` e
`atividades/prova-*.qmd` são ignorados pelo git (exceto `lista-comp-*`), e `**/*gabarito*`
também. Lista e gabarito **nunca** vão para `content/`, nunca usam `.spoiler` e o gabarito
nunca entra num commit. `tests/test_atividades.py` guarda isso.

## Tipos de questão

| Tipo | O aluno | Gabarito (manuscrita) |
|---|---|---|
| **conceitual** | explica, compara, escolhe o método e justifica | resposta curta + o erro comum |
| **conta** | resolve à mão (MSE, taxa de erro, matriz de confusão, um passo de *k*-NN) | passo a passo, número final em pt-BR |
| **código** (só computacional) | escreve `pandas`/`scikit-learn` no Colab | — |

Exercícios com dados usam os CSVs de `dados/` (com as colunas traduzidas) ou uma simulação
com semente explícita (INV-5). Nunca invente números "de cabeça".

## Fase 0 — Pré-voo

Leia os capítulos-alvo, `.claude/rules/knowledge-base.md`, o modelo do formato escolhido e as
listas existentes (para não repetir questões e manter a numeração/estilo). Produza:

```markdown
## Relatório de Pré-Voo — Lista
**Formato:** manuscrita | computacional · **Capítulos:** … · **Nível:** intro | core | avançado
**Tipos:** conceitual=N, conta=N, código=N (total N)
**Dados:** dados/<arquivo> | simulação com semente N | nenhum
**Objetivos de aprendizagem:** 2–4
**Matriz de cobertura:** seção → questões
**Arquivo:** atividades/<nome>.qmd
```

Tema vago demais para escrever objetivos → uma pergunta ao professor e para.

## Fase 1 — Questões

- **Motivação antes da mecânica:** uma frase dizendo por que a pergunta importa.
- **Notação da casa:** a do ISLP, como no livro; dado em português.
- **Calibração:** intro = um conceito; core = 2–3 passos encadeados; avançado = um insight não óbvio (ex.: por que o MSE de treino cai e o de teste não).
- **Autocontida:** cada questão diz suas hipóteses; nada de "como na aula".
- **Escopo:** só o que o livro cobre hoje, sem inferência (INV-3).
- Questões fechadas: alternativas plausíveis, uma só correta, distratores que capturam erros reais (treino × teste, taxa de erro × acurácia, `alpha` × $\lambda$, escala esquecida no *k*-NN).

## Fase 2 — Gabarito (manuscrita)

Para cada questão: solução completa e uma linha de "por que importa". Toda conta conferida no
`.venv` (`MPLBACKEND=Agg PYTHONHASHSEED=0 .venv/bin/python …`); cole o resultado real. Não
conferido → marque **RASCUNHO — NÃO CONFERIDO**.

## Fase 3 — Arquivos

- **Manuscrita:** `atividades/<nome>.qmd` com o front matter Typst do modelo e os blocos `when-meta="gabarito"`. Render (indicado ao professor): `make atividade FONTE=atividades/<nome>.qmd` — gera a versão do aluno em `atividades/publico/` e o gabarito fora dela.
- **Computacional:** `atividades/lista-comp-NN.qmd` com as marcas de resposta; `.venv/bin/python scripts/gerar-lista.py` gera o notebook; `.venv/bin/pytest tests/test_atividades.py -q`.

## Saída

Caminhos dos arquivos, contagem por tipo, semente usada, quais contas foram conferidas.
Confirme com `git check-ignore atividades/<nome>.qmd` que a lista manuscrita está ignorada.

## O que esta skill não faz

Não corrige respostas de alunos, não publica nada, não mexe em `content/` e não faz commit.
