# Capítulo 12 — Regressão Múltipla: relatório da rodada de correções

**Status: todos os 23 itens aplicados** (2 Críticos, 10 Importantes, 11 Menores).
`make render` → `render OK (tentativa 2)`, sem aviso de edição concorrente na rodada final.
`make teste` → **24 passed**.

## A raiz comum (I2, I3, I4) — o que foi feito

Antes de escrever, remedi tudo no container. Os números do contrato bateram:

| modelo | β exato de `amigos` | β do nosso GD |
|---|---|---|
| `amigos` | 0,903866 | 0,841484 |
| `amigos` + `horas` | 0,927439 | 0,925095 |
| `amigos` + `doutorado` | 0,963918 | 0,936224 |
| completo | 0,972505 | 0,974827 |

Subida exata: **+7,593962%**. Solução exata do modelo completo: `[30.579, 0.9725, -1.865, 0.9232]` —
dígito a dígito o que o Grus imprime. E a medição decisiva, que eu refiz: **sementes 0, 1, 2 e 7,
com 5.000 e com 20.000 passos, devolvem `0.8414839625196929` — o mesmo `float`, os oito casos.**

Por isso o ciclo-limite não ficou como afirmação: virou o chunk `ciclo-limite`, dentro do callout da
§2 (2 sementes × 2 contagens de passos, `!r` para mostrar todos os dígitos). Custa ~40 s de render e
mata as três explicações erradas com saída, não com prosa.

- **§2** — a tabela de valores exatos entrou como tabela markdown, atribuída à equação normal e
  remetendo à §12.3. **Não escrevi um resolvedor de equação normal**: a §12.3 diz que essa álgebra
  ficou fora de escopo, e um solver de eliminação de Gauss na §2 desmentiria aquele callout duas
  seções antes de ele existir. O precedente é o próprio capítulo, que já imprime os coeficientes
  exatos do Grus como fórmula, sem calculá-los. Os quatro valores foram medidos aqui (acima).
- **§2** — o chunk `modelos-aninhados` continua rodando GD e imprimindo 0,8415, como o contrato pede;
  a prosa argumenta pelos exatos e diz por que a primeira linha do GD está contaminada.
- **§2 (M5)** — título do callout: "Por que este 0,84 não bate com o 0,904 do Capítulo 11".
- **§3 (I2)** — a explicação da semente saiu; a punchline ("o Grus imprimiu a solução exata; nós
  imprimimos uma aproximação dela") entrou na frente; "terceira casa" virou "da terceira à segunda",
  com os dois exemplos.
- **§4 (I4)** — 0,84/0,97 → 0,904/0,973.

## Críticos

- **C1** — a frase "mais reamostras aproximariam os dois" foi substituída por três parágrafos: os
  números de B=400 (1,302 / 0,102 / 0,154 / 1,236, com o termo constante *subindo*), o argumento de
  que o desvio padrão de B réplicas não tem viés para cima, e a explicação verdadeira — **os dois
  medem alvos diferentes**, e discordar é informação sobre os dados.
- **C2** — nova seção visível `## O que este capítulo amarra` no fim da §8, **antes** do callout
  colapsado, no molde do "Onde este capítulo deságua" (cap. 8) e do "O que isso amarra" (cap. 11).
  Três parágrafos: o arco ajuste → interpretação → R² cego → bootstrap → erro padrão → encolhimento,
  e as três peças que viajam (bootstrap, erro padrão, regularização) entregando ao capítulo 13. O
  último parágrafo do callout foi promovido para lá e o callout ficou só com o aviso do `C`.

## Importantes

- **I1 + M8** — a caixa da §5 virou `.callout-note` e passou a se apoiar em saída: o chunk `ruido`
  agora inclui `k = 1`, e a tabela imprime **0,6800 → 0,6825**. A fórmula $(1-R^2)/(n-k)$ saiu; ficou
  "uns poucos milésimos com 203 pontos" citando a regra de bolso. A imprecisão do otimizador está
  dita como ~0,000025 (GD 0,679986 contra exata 0,680011), duas ordens de grandeza abaixo.
- **I5** — o chunk duplicado da §4 foi removido (ficou a prosa que ele sustentava; o import de `mean`
  saiu junto); a §7 reduziu a "os 22 usuários daquela seção".
- **I6** — a §4 abre com a dobradiça sugerida, antes de qualquer chunk.
- **I7** — `sharex=True`, `sharey=True` e `range` comum aos três painéis, `bins=30`. **Abri o PNG
  renderizado**: `amigos` e `horas` são picos estreitos de um lado do zero, `doutorado` se espalha por
  quase toda a largura e atravessa o zero. A prosa foi reescrita para descrever isso, dizendo que é a
  escala compartilhada que torna a comparação legítima. Legenda atualizada.
- **I8** — parágrafo novo apresentando a *t* de Student e definindo graus de liberdade; comentário no
  chunk dos `assert` explicando a troca pelos valores do livro (exatos) com erros padrão nossos.
- **I9** — "o arco que se fechou **até aqui**", mais um parágrafo entregando à §8 (diagnosticar à mão
  contra encolher sozinho).
- **I10** — os três `.exemplo` indevidos corrigidos: §4 virou prosa corrida, §5 e §8 viraram
  `.callout-note` com título. Os dois `.exemplo` legítimos (§2:84, §3:47) ficaram.

## Menores

M1 "duas funções, um `return` cada" · M2 `get_sample` declarada imaginária · M3 abertura invertida
("O título do Grus chama isto de digressão. É a ideia mais reaproveitável do capítulo") · M4 "força"
e "Ponha as variáveis na mesma escala antes de regularizar" · M5 acima · M6 chunk virou bloco
```python não executado · M7 ponteiro para árvores (cap. 14) e redes (cap. 15), com o preço:
a leitura direta do coeficiente · M8 acima · M9 o `trange` → `range` do `least_squares_fit_ridge`
registrado como diferença não conceitual · M10 "minilotes" → "minibatch" · M11 **cumprida**: callout
visível na §7, "A hipótese que o bootstrap não precisou fazer", nomeando homocedasticidade, dizendo o
que quebra sem ela (o erro padrão, o *t* e o valor-p — não os coeficientes) e amarrando com C1.

## Extra não pedido

O chunk da §5 imprimia "1 colunas de puro ruído" depois de eu acrescentar `k = 1`; ficou plural
condicional.

## Preocupações

1. **A tabela de exatos da §2 é hardcoded.** Verificada duas vezes (o contrato e eu, pela equação
   normal), e os dados são fixos, então ela não pode "envelhecer" — mas nenhum chunk a recalcula. Se
   um dia o livro construir álgebra linear, ela vira chunk.
2. **A §2 ficou mais cara**: o chunk `ciclo-limite` acrescenta 50.000 passos de GD (~40 s). A §5
   acrescentou um sexto ajuste de 15.000 passos. Achei o custo bem gasto — as duas afirmações que
   mais erraram nesta revisão agora são saída de código.
3. **`_book/` estava sendo reescrito pelo agente do capítulo 13** enquanto eu conferia. Minha
   verificação de números e do PNG foi feita sobre o meu próprio render bem-sucedido, antes disso.
   A última rodada mexeu só em prosa da §8.
