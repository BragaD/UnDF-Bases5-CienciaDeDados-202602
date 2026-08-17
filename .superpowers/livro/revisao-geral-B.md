# Revisão geral do livro — lote B: promessas, superlativos e notação

Quatro frentes varreram o livro completo. Este lote traz o que cai nos capítulos **4, 5, 8, 11,
13, 14 e 15**.

**Não toque nos capítulos 16 e 17** — outro agente está com eles, no lote A. A **única** coisa
do capítulo 14 que é do lote A é o `max_features='sqrt'` na §14.6; todo o resto do 14 é seu.

---

## Crítico

### B1 — O livro enuncia uma regra sobre si mesmo e a quebra

`content/cap05/05-ajustando-modelos.qmd:21` diz: "Vamos chamar os parâmetros de `theta` (θ) […]
**Os capítulos 11 a 13 herdam o mesmo nome**."

Falso para 12 e 13: `theta` tem **zero** ocorrências neles, e os dois usam `beta` exclusivamente
(só o `cap13/03` o faz 44 vezes). E `content/cap12/01-o-modelo.qmd:40` rebatiza para $\beta$ sem
citar a promessa.

**É a única regra de nomenclatura que o livro enuncia sobre si mesmo, e ela não se cumpre.**
Correção sugerida: "O Capítulo 11 herda o mesmo nome; do 12 em diante o vetor passa a se chamar
`beta`, seguindo a notação usual de regressão."

---

## Importantes

### B2 — A promessa do capítulo 4 aponta para o capítulo errado

`content/cap04/02-matrizes.qmd:139` afirma que "as camadas de uma rede neural, no
**[Capítulo 15]**, são exatamente isso" (uma matriz *n*×*k* como função linear).

No capítulo 15 a camada é uma **lista de vetores de neurônio**; a única matriz aparece dentro de
um callout de `scikit-learn` (`cap15/02:197`), descrevendo a convenção da biblioteca — e ainda
transposta. **A dívida é paga de fato em `content/cap16/03-a-camada-linear.qmd:172`**, num
callout que se chama, literalmente, "A dívida do Capítulo 4, cobrada", onde `self.w` tem forma
`[output_dim, input_dim]`.

Redirecione a promessa para o capítulo 16 (ou cite os dois, com o 16 como o lugar onde vira
matriz).

### B3 — Superlativo do capítulo 14, contradito por dois outros capítulos

`content/cap14/index.qmd:15` e `content/cap14/06-florestas-aleatorias.qmd:366` dizem que a
árvore tem "uma propriedade que **nenhum modelo anterior deste livro tinha**: um humano consegue
lê-la" e que ela é "o **primeiro modelo deste livro** que um humano lê".

Mas `content/cap11/index.qmd:13` diz que o capítulo 11 é "o primeiro capítulo deste livro em que
o ajuste produz um **parâmetro interpretável, com unidade do mundo**", e
`content/cap15/index.qmd:20` diz "O Capítulo 12 entregou coeficientes que se leem em português".

**O próprio `content/cap14/01-o-que-e-uma-arvore-de-decisao.qmd:97` já escapa disso**,
restringindo-se a **classificadores**. Adote esse escopo nos dois lugares: "o primeiro
**classificador**" / "nenhum classificador anterior".

### B4 — "Quatro classificadores" e a lista tem três

`content/cap14/01-o-que-e-uma-arvore-de-decisao.qmd:97` diz "Você já construiu **quatro**
classificadores neste livro", e a lista das linhas 99–101 tem **três**: k-vizinhos, Naive Bayes,
regressão logística.

O quarto candidato plausível é o classificador improvisado de
`content/cap01/03-hipotese-motivadora-datasciencester.qmd:408`, que `cap13/01:7` e
`cap08/index.qmd:18` citam. **Ou troque para "três", ou acrescente o quarto marcador** — e a
segunda opção é melhor, porque aquele classificador é material recorrente do livro.

### B5 — Superlativo do capítulo 15 sobre o custo de render

`content/cap15/04-exemplo-fizz-buzz.qmd:161` diz ser "de longe o chunk mais caro **deste
livro**" (~1 minuto). O MNIST do capítulo 16 custa ~3 minutos, e
`content/cap16/index.qmd:26` diz textualmente "Este é o capítulo mais caro do livro para
renderizar".

→ "deste **capítulo**", que é a fórmula que `content/cap12/07-erros-padrao-dos-coeficientes.qmd:57`
já usa.

### B6 — Duas figuras do capítulo 15 sem rótulo de eixo

O capítulo 3 gasta uma figura inteira ensinando que gráfico sem rótulo é defeito, e uma revisão
anterior já corrigiu 15 figuras por isso. Estas duas escaparam:

- **`content/cap15/01-perceptrons.qmd:119-124`** (`fig-portas`): só `set_xticks`/`set_yticks`.
  Faltam `$x_1$` e `$x_2$`. **E a legenda (`:93`) descreve só os quatro pontos** — metade da tinta
  é a região cinza e a reta de fronteira, explicadas apenas na prosa da linha 130. Acrescente à
  legenda o que a região cinza significa e que no XOR não há reta que separe.
- **`content/cap15/02-redes-feed-forward.qmd:64-66` e `:79-81`** (`fig-degrau-sigmoide`): **nenhum
  rótulo nos dois painéis**, enquanto a prosa da linha 87 fala em "chega a 0,25 em $t = 0$" — o
  leitor não tem como saber que a abscissa é $t$. Compare com `fig-ativacoes` do capítulo 16, que
  rotula `x`, `f(x)` e `f'(x)`.

**Abra as duas figuras depois do render.**

### B7 — Prosa e código discordam na mesma página

`content/cap11/02-usando-gradiente-descendente.qmd:38, 106, 128, 130` — a prosa diz `theta`
(em crase, como identificador) quatro vezes; o chunk das linhas 76–92 chama a variável de
`guess`. Quem procurar `theta` no bloco não acha.

→ "o palpite (`guess`, no código)" na primeira menção, ou renomeie no chunk.

---

## Menores

- **M1** — `content/cap13/03-aplicando-o-modelo.qmd:176` diz "sem **minilotes**". É a **única**
  ocorrência no livro; *minibatch* aparece 29 vezes, inclusive no título da §5.6. Este caso já
  foi corrigido uma vez e reapareceu. → "sem minibatches".
- **M2** — `content/cap13/05-maquinas-de-vetores-de-suporte.qmd:203`: "é por isso que esta seção
  **não tem implementação**". A seção tem três chunks executáveis. O sentido é "não implementa a
  SVM". → "não implementa a máquina de vetores de suporte".
- **M3** — `content/cap08/06-extracao-e-selecao-de-atributos.qmd:29` diz que "as árvores de
  decisão, do Capítulo 14, lidam com dados numéricos ou categóricos". O `cap14/01:95` separa
  explicitamente árvores em geral do que o capítulo constrói — o ID3 **não** trata coluna
  numérica. → "as árvores de decisão em geral lidam com…; o ID3 do Capítulo 14 trata toda coluna
  como categórica".
- **M4** — `content/cap14/01-o-que-e-uma-arvore-de-decisao.qmd:126` usa a variante "Na prática: o
  que se faz com isso" **tendo análogo de biblioteca** — o terço final é uma comparação detalhada
  com `DecisionTreeClassifier`. E essa comparação reaparece quase palavra por palavra em
  `content/cap14/05-juntando-tudo.qmd:302`, sem que nenhum aponte para o outro. Ou o 14.1 encurta
  e delega, ou o 14.5 remete ao 14.1.
- **M5 — notação de escalar.** `*k*` (77 ocorrências) contra `$k$` (12), dividido por capítulo,
  sem convenção declarada. Dois pontos onde dói:
  - `content/cap04/02-matrizes.qmd` usa `*n*` e `*k*` nas linhas 55 e 139 e `$n$`, `$m$`,
    `$O(m)$`, `$n^2$` nas linhas 193–227 — **mesma variável, duas grafias, mesmo arquivo**, e é o
    capítulo que funda a notação do livro.
  - `content/cap09/01-o-modelo.qmd:117` mistura na mesma frase: "sobre *n* pontos custa
    $O(n \log n)$ […] as *n* distâncias".
  **Regra sugerida: `$k$`/`$n$` para escalar matemático, crase só para identificador Python.**
  Aplique **onde a mistura está na mesma frase ou no mesmo arquivo**; não varra o livro inteiro.
- **M6** — `content/cap11/index.qmd:25` e `content/cap11/01-o-modelo.qmd:47` dizem "valor
  extremo"; `content/cap11/01-o-modelo.qmd:145` diz "outlier" para o **mesmo ponto, na mesma
  página**. Os capítulos 7 e 9 dizem "outlier". Escolha um; se ficar em inglês, itálico na
  estreia, como o livro faz com *feature* e *overfitting*.
- **M7** — `content/cap11/01-o-modelo.qmd:132` é a **única** ocorrência de "variável
  independente"/"variável dependente" no livro (o padrão é "variável explicativa", 10x, e
  "alvo", 52x). E `content/cap12/08-regularizacao.qmd:60` é a única de "variável resposta" —
  **mas o 12 é do outro lote; não toque nele.**
- **M8** — *epoch* é introduzido em itálico em `cap05/03:41` e fica romano no resto do capítulo 5,
  no 15 e no 16 — a regra da casa (itálico na estreia, romano depois, como em *bootstrap* e
  *overfitting*). Mas volta a itálico em `content/cap07/07-um-parenteses-tqdm.qmd:79` e cinco
  vezes em `content/cap11/02-usando-gradiente-descendente.qmd`. Uniformize em romano.

---

## Figuras que faltam — só uma, e vale

`content/cap15/03-retropropagacao.qmd` **não tem nenhuma figura**, e é o mecanismo central do
capítulo — a seção mais difícil do livro. A de maior retorno: **as duas retas que os neurônios
ocultos aprendem, desenhadas sobre o mesmo quadrado do `fig-portas`**. Ela fecha explicitamente
a pergunta que o `fig-portas` deixa aberta — *duas retas resolvem o que uma não resolve* — e
reaproveita uma moldura que já existe no capítulo.

**Escreva-a**, e **abra o PNG depois do render** para conferir que a prosa descreve o que se vê.
Se as duas retas não separarem visivelmente as regiões do XOR, diga isso em vez de afirmar o
contrário.
