# Capítulo 11 — Regressão Linear Simples: correções

Duas revisões independentes rodaram. **A de conteúdo voltou limpa**: nenhum Crítico,
nenhum Importante. A matemática, os números, a derivação de máxima verossimilhança e a
dívida do capítulo 5 conferem todos. Os dois achados dela estão abaixo como M1 e I3.

**Portanto esta rodada é quase inteiramente didática — e é exatamente por isso que ela é
perigosa.** O padrão observado neste livro, capítulo após capítulo, é que toda rodada de
correção tem chance alta de *introduzir* um defeito novo. Aqui você vai mexer em prosa e em
callouts de um capítulo tecnicamente correto. **Não quebre o que já está certo.** Todo
número que você tocar, rode e confira contra a saída.

---

## Críticos

### C1 — O argumento de por que os dois métodos concordam está partido, e nunca é dito inteiro

Esta é a demonstração central do capítulo e a dívida que o capítulo 5 deixou.

- `01-o-modelo.qmd:108` dá metade: "derive, iguale a zero, resolva o sistema".
- `02-usando-gradiente-descendente.qmd:107` dá a outra: "é convexa, logo o mesmo fundo".

Falta a frase que junta as duas, e sem ela "convergem porque é o mesmo fundo" é asserção, não
demonstração. O aluno sai sabendo *que* concordaram, não *por quê*.

Escreva, no `.exemplo` de `02:107`, **antes** da menção à convexidade, a ideia inteira:

> O gradiente descendente procura **numericamente** o ponto onde o gradiente se anula. A
> fórmula fechada resolve **algebricamente** a mesma equação — derivar a soma dos quadrados,
> igualar a zero, isolar. É a mesma equação, resolvida de dois jeitos. A convexidade é o que
> garante que esse ponto existe e é único: não há um segundo fundo em que o gradiente
> também se anule e para onde o método iterativo pudesse escorregar.

Use as suas palavras, mas os três elementos — mesma equação, dois métodos de resolução,
convexidade garante unicidade — precisam estar juntos, num lugar só.

### C2 — O clímax do capítulo não tem figura

A seção 11.2 é o ponto alto do livro até aqui e entrega **dois `tuple` sem rótulo**
(`02:96` e `02:101`). O leitor decodifica `(22.947552413..., 22.947552155..., 2.58e-07)`
sozinho.

O chunk já calcula a perda a cada epoch e **joga fora** (`02:69`). Guardar numa lista custa
uma linha e rende o gráfico que fecha o capítulo:

- **perda por epoch**, em escala log no eixo y, com uma **linha horizontal** na perda da
  solução fechada, e a curva encostando nela.

Rotule os eixos em português, dê `#| label: fig-...` e `#| fig-cap:`, e **escreva na prosa o
que a figura mostra depois de abri-la** — não antes. Se a curva não encostar visivelmente na
horizontal, diga isso, não o contrário.

---

## Importantes

### I1 — A prosa subestima o próprio resultado

`02:104` diz "a mesma resposta até a quarta casa decimal" — e mostra os dois valores já
arredondados a quatro casas, o que faz a frase parecer tautológica em vez de evidência.

Medido: as diferenças são **2,58 × 10⁻⁷ em α** e **2,07 × 10⁻⁸ em β**. Escreva o número:

> as duas respostas diferem em 2,6 × 10⁻⁷ — depois de dez mil passos partindo de um `theta`
> sorteado ao acaso.

### I2 — Falta o passo do log em 11.3, e ele é caixa-preta pura

A seção passa do produto (`03:56`) direto para a exponencial da soma, e "log-verossimilhança"
aparece pela primeira vez em `03:111` sem nunca ter sido definida.

Falta o passo que mais fala com este leitor: **um produto de 203 densidades normais estoura
para `0.0` em float64**. O log não é elegância de notação — é a única forma de a conta existir
num computador. Isto é exatamente a caixa-preta que a disciplina abre, e está de graça aqui.
O capítulo 10 já fez este mesmo argumento para o Naive Bayes; aponte para lá.

**Meça antes de escrever**: calcule o produto direto das 203 densidades e mostre que dá `0.0`,
e a soma dos logs, que dá um número finito.

### I3 — 11.3 é a única seção sem código que o aluno constrói

`03:91` só chama `sum_of_sqerrors` importado. Três linhas — uma `log_likelihood(alpha, beta,
x, y, sigma)` e o valor para dois modelos diferentes — transformam o argumento verbal de
`03:101` ("o expoente é menos negativo") em número na tela, no idioma do livro. Encaixa com I2.

### I4 — `θ` muda de significado sem aviso

O capítulo 5 fixou `theta` = vetor de parâmetros do modelo (`cap05/05:21`, "a convenção deste
livro"), e a 11.2 usa `theta` assim. Em `03:13` θ vira "parâmetro desconhecido de uma
distribuição". Uma oração resolve.

### I5 — A história do outlier está contada pela metade, e a metade que falta é a melhor

`01:22` diz que os dados "já vêm sem um usuário-outlier removido pelo próprio livro-texto" —
frase que, além de agramatical (ver M2), desperdiça o material.

**Medido agora, use estes números:** o usuário removido declarava **100 amigos e 1 minuto por
dia**. Com ele dentro, a correlação é **0,2474**; sem ele, **0,5737**. Um ponto em 204
derruba a correlação para **43%** do valor.

Isto é o `callout-warning` que o guia pede ("os erros do livro-texto são conteúdo"), e explica
*por que* remover em vez de só afirmar que se removeu. Custa três linhas e uma chamada a
`correlation(num_friends, daily_minutes)` — os dois nomes existem em `scratch.statistics`.

### I6 — Os dois enunciados mais importantes do capítulo estão marcados como `.exemplo`

`01:105` (a fórmula fechada é a dívida do cap. 5 paga) e `02:106` (os dois caminhos convergem)
são **conceitos centrais**, não casos concretos que iluminam um conceito. Promova os dois a
`.conceito`. Hoje a hierarquia visual diz ao leitor que o clímax é ilustração.

### I7 — Trivia de build ocupa o slot de maior atenção

O `callout-note` de `01:19-23` é a **segunda coisa da página**: cinco `plt.*` soltas,
`plt.close('all')`, a bateria de `assert` do módulo — e só no último parágrafo a informação que
o leitor precisa, que é o que são os dados. Mesmo problema em `02:23-27`.

Separe: o que são os dados fica onde está (e cresce, com I5); a mecânica do matplotlib desce
para o fim da seção ou vira `collapse="true"`.

### I8 — O "Na prática" descreve a igualdade em vez de mostrá-la

`01:196-212` acerta o essencial: nomeia a SVD, diz que `LinearRegression` não itera nem pede
taxa, desmonta `.score()`. Mas este callout específico é **o momento simbólico do livro** — a
caixa-preta que a disciplina inteira existe para abrir.

Falta o gesto: **rodar as duas e mostrar os mesmos números**. Três valores lado a lado (α, β,
R² à mão × `sklearn`). O chunk é `python` puro não executado, então os números que você
escrever ali precisam ser conferidos por você **rodando de verdade** antes — e se o
`scikit-learn` não estiver no ambiente, diga isso no relatório em vez de inventar a saída.

### I9 — A alegação de primazia é genérica e os capítulos vizinhos a contradizem

`index:13` afirma "É o primeiro capítulo deste livro em que isso acontece de ponta a ponta",
mas o cap. 9 já classificou íris do dado bruto à previsão e o cap. 10 já treinou um filtro de
spam. Os dois **qualificam** a primazia deles ("primeiro *classificador* completo", "primeiro
modelo *probabilístico*"); este não.

Qualifique também — e a afirmação fica **mais forte**: é o primeiro em que o ajuste produz um
**parâmetro interpretável, com unidade do mundo**: 0,9 minuto por amigo.

### I10 — Faltam duas ligações prometidas de fora

- `cap01/03-hipotese-motivadora-datasciencester.qmd:352` **promete este capítulo pelo nome**:
  "o que queríamos era uma afirmação sobre o efeito de mais um ano de experiência sobre o
  salário médio — é o que a regressão linear faz, no Capítulo 11". O cap. 11 nunca menciona o
  cap. 1. Mesma dívida estrutural do cap. 5, paga com uma frase.
- `cap10/index.qmd` diz "a sequência de regressão, começando no próximo capítulo". O cap. 11
  não tem link nenhum para os caps. 9 ou 10; `index:13` pula do 8 para "aqui".

### I11 — O capítulo se despede do capítulo 13, não do 12

O último parágrafo visível (`03:111`) termina em regressão logística. O cap. 12 só aparece
dentro do callout colapsado (`03:118`), que o leitor pode não abrir. Uma frase ao fim de
`03:111` recoloca o próximo passo à vista: o cap. 12 mantém a suposição de erros normais e só
troca uma variável explicativa por várias.

### I12 — Contradição interna sobre o capítulo 12

`index:36` diz que o cap. 12 é "sem a fórmula fechada"; `02:110` diz que lá "a álgebra ainda
fecha, mas fica pesada".

**A segunda está certa** — a regressão múltipla tem, sim, solução fechada:
β = (XᵀX)⁻¹Xᵀy, a equação normal. Corrija `index:36`. Não escreva a fórmula matricial no
capítulo 11 (o livro não construiu inversão de matriz); basta não afirmar que ela não existe.

### I13 — Prosa: dois calques e uma contradição de tom

- `index:13` — "cada amigo a mais **custa** quase um minuto a mais". "Custa" carrega custo e
  causalidade, e **contradiz o `callout-important` de `01:40`**, que gasta um parágrafo
  avisando que a causalidade é suposta. A frase-manchete é mais descuidada que a seção que ela
  resume. → "**corresponde a** quase um minuto a mais".
- `03:33` — "algum desvio padrão σ (conhecido)" é calque de *known*, e colide com `03:77`
  ("vale para qualquer σ fixo"). → "um desvio padrão σ **fixo, o mesmo para todos os pontos**"
  — que ainda nomeia de graça a homocedasticidade, e o cap. 12 vai cobrar isso.
- `01:43` — "**hipotetizamos** que existem constantes" é calque de *we hypothesize*. →
  "supomos que existam".

---

## Menores

- **M1** — `01:135` arredonda β para "0,904"; o Grus imprime "0.903" (truncamento dele;
  0,9038659… arredonda para 0,904). **Nosso número está certo — não mude.** Registrado aqui só
  para que a próxima revisão não o "conserte".
- **M2** — `01:22`: "já vêm **sem** um usuário-outlier removido pelo próprio livro-texto" é
  agramatical (dupla negação: vêm sem um usuário que foi removido). → "já vêm **com** um
  usuário-outlier **descartado** pelo próprio livro-texto". Some com I5.
- **M3** — `01:70`: "somar os erros direto **não presta**" — registro coloquial destoante. →
  "não serve".
- **M4** — `02:86`: "com o mesmo **alcance** de grandeza" não é idiomático. → "**ordem** de
  grandeza".
- **M5** — `01:184` e `03:77`: "o **pior** modelo linear razoável" confunde — não é o pior, é a
  linha de base. → "o modelo de referência mais simples possível: sempre prever a média".
- **M6** — `02:104`: "Dez mil epochs" sem itálico; o cap. 5 grafa *epochs*. Padronize.
- **M7** — `01:111`: o parágrafo sobre desvios padrão perfeitamente correlacionados /
  anticorrelacionados / zero repete em prosa o que a fórmula já diz. Encolha pela metade.
- **M8** — `02:36` diz que o problema é "idêntico" ao da 5.5 e que "a diferença é só o dado".
  Acrescente o que **não** é idêntico e por que não muda nada (soma em vez de média — hoje isso
  só aparece 50 linhas depois, em `02:84`).
- **M9** — `01:139` linka o cap. 3, que já desenhou "amigos × minutos" — mas com 9 pontos
  inventados numa escala completamente outra (60–72 amigos, 105–220 minutos). Meia frase evita
  a falsa memória: lá eram nove pontos ilustrativos, aqui são os 203 reais.
