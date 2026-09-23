---
name: devils-advocate
description: Desafio adversarial de 5–7 perguntas às escolhas pedagógicas de uma seção ou capítulo do livro — ordem, pré-requisitos, carga cognitiva, motivação, notação, escolha do exemplo e da figura. Use quando o professor disser "advogado do diabo", "cutuca essa seção", "o que um aluno cético perguntaria?", "testa o desenho da seção". Somente leitura; mais leve que o pedagogy-reviewer.
argument-hint: "[arquivo .qmd ou seção, ex.: 8.3]"
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
disallowed-tools: ["Edit", "Write"]
---

# Advogado do diabo

Examine a seção criticamente e desafie o desenho com 5–7 perguntas pedagógicas específicas.
**Filosofia:** a melhor seção sai do diálogo ativo.

## Preparação

1. Leia o arquivo-alvo (resolva "8.3" para `content/cap08/03-*.qmd`).
2. Leia `.claude/rules/knowledge-base.md` (notação, progressão, armadilhas), o `CLAUDE.md` e a linha do capítulo na spec vigente (escopo e o que fica de fora).
3. Leia o fim da seção anterior e o começo da seguinte.
4. Se a seção corresponde ao ISLP, abra a seção do livro (`pdftotext -layout livros/ISLP_website.pdf`) para comparar a ordem e as figuras.

## Categorias de desafio

1. **Ordem** — "O aluno entenderia melhor se X viesse antes de Y?" (e o ISLP faz em que ordem?)
2. **Pré-requisito** — "Um aluno de CC sem base sólida de estatística nem de Python tem base para isto aqui?" Álgebra linear não pode ser assumida; validação cruzada não existe antes do cap. 10.
3. **Lacuna** — "Falta um exemplo intuitivo antes desta fórmula?"
4. **Apresentação alternativa** — "Duas outras formas de mostrar isto" (figura, simulação com semente, página de `apoio/`, analogia de computação).
5. **Conflito de notação** — "Este símbolo colide com o uso em outra seção/no ISLP."
6. **Carga cognitiva** — "Símbolos, funções ou `.funcao` demais de uma vez. Dividir?"
7. **Exemplo, dado e figura** — "O dado escolhido mostra o fenômeno, ou o esconde? A figura carrega a ideia ou decora?"
8. **Tese** — "Este chunk ensina a escolher, ajustar e julgar, ou escorrega para implementação à mão ou para inferência?"

## Saída

```markdown
# Advogado do diabo: <seção>

### Desafio 1: <Categoria> — <título curto>
**Pergunta:** …
**Por que importa:** …
**Sugestão:** …
**Onde:** linha N / subtítulo
**Severidade:** Alta / Média / Baixa

(5–7 desafios)

## Veredito
**Pontos fortes:** 2–3
**Mudanças críticas antes da aula:** 0–2
**Melhorias desejáveis:** 2–3
```

## Princípios

- Específico: cite subtítulo, linha, símbolo.
- Construtivo: todo desafio traz uma sugestão.
- Honesto: se a seção está boa, diga.
- Prioridade: conflito de notação e erro de pré-requisito > metáfora perdida.
- Pense como o aluno: onde ele se perde?
