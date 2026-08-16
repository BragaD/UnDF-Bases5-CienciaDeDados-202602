# Capítulo 5 — apontamentos consolidados das duas revisões

Duas revisões independentes (conteúdo técnico e didática) somaram 34 apontamentos.
Consolidados e priorizados por mim, com adjudicação onde as duas divergiram do escritor.

**Corrija tudo o que está aqui.** Se discordar de algum item, não o ignore em silêncio:
implemente o resto e diga no relatório qual você recusou e por quê.

---

## CRÍTICOS

### C1 — `05-ajustando-modelos.qmd:106` — explicação matematicamente errada

O texto diz que a perda cai sempre "**porque cada passo segue a direção que garantidamente
reduz a perda em primeira ordem**".

A garantia de primeira ordem vale para passo **infinitesimal**, não para o passo finito
que de fato é dado. Decréscimo monotônico com passo fixo depende do tamanho do passo
frente à curvatura — que é exatamente o que a **sua própria seção 5.4** ensina, duas
seções antes, com o contraexemplo do `step_size` que diverge seguindo a direção correta.

O fato empírico está certo (0 de 5.000 épocas sobem). O *porquê* contradiz o capítulo.

Reescreva sem invocar "primeira ordem" como garantia incondicional. Algo na linha de:
*"porque `learning_rate = 0.001` é pequeno o bastante frente à curvatura desta perda — a
mesma lição da seção 5.4, agora do lado seguro."*

### C2 — a ponte de 5.2 para 5.3 não existe

5.2 termina estimando o gradiente numericamente e comentando que o exato seria `[6,8,10]`.
5.3 abre com `sum_of_squares_gradient(v) = [2*v_i for v_i in v]` caindo do céu: sem
derivação, e sem dizer que é exatamente aquele `[6,8,10]`.

O leitor faz todo o trabalho de 5.2 para nunca mais usá-lo, e a única coisa que 5.2
comprava — confiança de que a fórmula analítica está certa — é jogada fora.

Acrescente um parágrafo no topo de 5.3, mais ou menos assim:

> Derivando à mão, a derivada parcial de $\sum v_j^2$ em relação a $v_i$ é $2v_i$. Confira
> contra a seção anterior: `estimate_gradient` em `[3,4,5]` devolveu algo indistinguível
> de `[6,8,10]`. Daqui em diante calculamos gradientes assim — a estimativa numérica passa
> a ser o instrumento de **conferência**, não o de produção.

### C3 — o capítulo não fecha

O `index.qmd` promete "a engrenagem central do livro" e 5.6 termina numa frase de
manutenção. Os capítulos a jusante são citados **cinco vezes como a mesma lista de cinco
links**, e o aluno nunca aprende o que varia entre eles.

Escreva um fechamento em 5.6 que entregue a promessa e diga **o que muda** em cada
capítulo a jusante: o laço é o mesmo, o que troca é o gradiente — erro quadrático nos
capítulos 11 e 12, log-verossimilhança no 13, retropropagação no 15 e 16.

---

## IMPORTANTES

### I1 — `04-escolhendo-o-tamanho-do-passo.qmd:70` — número errado por uma ordem de grandeza

"a essa taxa, chegar perto de zero levaria **dezenas de milhares** de epochs."

Recalculei: partindo de 8.75158864609029, com fator 0.99998 por epoch, até ficar abaixo
de 0.001, são **453.845 epochs**. São *centenas de milhares*. Corrija o número e a ordem
de grandeza.

### I2 — o motivo do serrilhado do minibatch está incompleto, e é o melhor material do capítulo

**Adjudiquei este com evidência: o revisor está certo e o seu diagnóstico anterior era a
causa menor.**

`minibatches` faz `random.shuffle(batch_starts)` — embaralha os **índices de início**, não
os elementos. Como `inputs = [(x, 20*x + 5) for x in range(-50, 50)]` está ordenado por x,
cada lote é sempre a **mesma fatia contígua**: um lote só com x de −50 a −31, outro só com
x de −30 a −11, e assim por diante.

Ou seja, **cada lote é uma amostra sistematicamente enviesada**, e é isso que faz o
gradiente de cada um apontar torto. Embaralhar a ordem de blocos enviesados não desfaz o
viés de nenhum deles.

É um parâmetro chamado `shuffle` que parece embaralhar os dados e não embaralha — um erro
instrutivo do livro-texto, do tipo que o guia manda marcar. Dê a ele um
`.callout-warning` próprio, com o experimento de uma linha (`random.shuffle(dataset)`
antes de gerar os lotes) que alisa a curva. Rode o experimento e mostre o resultado real.

### I3 — as três curvas de convergência não são comparáveis, e o texto as compara

5.5 roda 5.000 epochs (MSE final ~4×10⁻⁸), 5.6 minibatch 1.000 (~10⁻¹⁰), estocástico 100
(~4×10⁻³). Dizer que o estocástico "acha os parâmetros ótimos num número de epochs muito
menor" é comparar corridas paradas em precisões diferentes.

Substitua os três gráficos separados — em três páginas, com três escalas de x — por **um
único gráfico com as três curvas contra o número de chamadas a `gradient_step`, com x em
escala log**. É o maior ganho didático disponível no capítulo: torna visível numa imagem
o argumento que hoje custa centenas de palavras.

### I4 — falta o aviso sobre `h` pequeno demais

O capítulo diz "um `h` bem pequeno" três vezes e nunca menciona que `h` pequeno **demais**
piora a estimativa, por cancelamento em ponto flutuante. Para um aluno de Ciência da
Computação que conhece float, é a coisa mais interessante da seção.

Além disso, `fig-derivada-estimativa` não ensina nada — os dois marcadores coincidem e o
texto já disse que coincidiriam. **Troque-a por um gráfico de erro contra `h` em eixos
log-log**, que mostra a curva em U: o erro cai com `h` até o cancelamento dominar e voltar
a subir. Resolve a figura e o callout de uma vez.

### I5 — `fig-ideia-gradiente` ilustra em vez de ensinar

As curvas de nível são círculos, então a trajetória é uma reta radial e a afirmação "move-se
sempre perpendicular à curva de nível" fica invisível por coincidência geométrica.

Use uma tigela anisotrópica (`x² + 5y²`): o caminho encurva, a perpendicularidade aparece,
e a figura já prepara o argumento de curvatura de 5.4.

### I6 — `.conceito` ausente nas três seções que carregam o capítulo

5.4, 5.5 e 5.6 não têm nenhum. Falta pelo menos um em 5.5 enunciando a receita que o livro
inteiro vai repetir: **parâmetros aleatórios → gradiente da perda → um passo contra ele →
repete**. É a entrega do capítulo e ela nunca é enunciada como conceito.

### I7 — "epoch" usado antes de existir, com dois sentidos

5.3 e 5.4 chamam de epoch uma iteração sobre uma função sem dados nenhum; 5.5 define epoch
como "cada passagem completa pelo conjunto de dados". São coisas diferentes. Defina em 5.3,
onde a palavra aparece pela primeira vez.

### I8 — `05-ajustando-modelos.qmd` — definição incoerente de perda

"uma função de **perda** que mede **o quão bem** o modelo se ajusta... Quanto menor, melhor."
A perda mede o quanto ele **erra**. Corrija: *"uma função de **perda** (*loss*) que mede o
quanto o modelo erra nos dados — quanto menor, melhor o ajuste."*

### I9 — `01-a-ideia...qmd` repete o `index.qmd` quase palavra por palavra

O leitor acabou de ler aquilo. Corte para uma frase e vá direto à função.

---

## MENORES — corrija todos

**Números e fatos**
- `index.qmd:13` — "uma única função de **onze linhas**, `gradient_step`". São **5 linhas**.
  Ambos os revisores pegaram isto de forma independente. Corrija, e note que ela não
  "termina" o capítulo: chega em 5.3.
- `index.qmd` — "constrói essa ideia em camadas — o que é o gradiente, como estimá-lo, como
  usá-lo, quanto andar" lista 4 das 6 seções, calando justamente as duas que sustentam o
  resto do livro.

**Conceitos que faltam**
- `theta` entra em 5.5 sem uma palavra de explicação, e é a notação que os capítulos 11 a 13
  herdam. Uma frase resolve: `theta` (θ) é a convenção para "o vetor de parâmetros do
  modelo, sejam eles quais forem".
- **Convexidade** nunca é mencionada. 5.1 avisa sobre mínimos locais e o aviso nunca é
  resolvido: o aluno não fica sabendo que a perda quadrática da regressão linear é convexa,
  e por isso 5.5 e 5.6 sempre chegam ao mesmo lugar. Uma frase em 5.5 fecha o laço com 5.1.
- `gradient_step` recebe `step_size` **negativo** para descer. Toda biblioteca do mundo
  recebe `learning_rate` positivo com o sinal embutido. Uma linha em 5.3 avisando disso
  evita que o aluno se perca ao ver `lr=0.001` no PyTorch.

**Conexões**
- Falta o link para o capítulo 9, e ele é grátis: o k-vizinhos é o **único** modelo do livro
  que não passa por aqui, porque não é treinado — não tem parâmetro a ajustar. Uma frase
  ensina os dois capítulos de uma vez.
- `minibatches` é o primeiro gerador que o livro usa para valer, e o capítulo 2 tem uma
  seção sobre geradores que não é citada.

**Callouts**
- Duas seções seguidas gastam um callout inteiro com encanamento do repositório: o
  `.callout-warning` "Uma pegadinha do módulo vendorizado" (5.2) e o `.callout-note` "Por
  que importar, e não reescrever" (5.4). Somados são mais texto que o `.conceito` de 5.3.
  Reduza a **um** callout curto em 5.4; a pegadinha do `NameError` vira duas linhas de nota
  em 5.2.
- "vendorizado" é jargão de casa. Troque por "uma cópia do código do livro-texto que mora
  dentro deste repositório".
- 5.1, o `.callout-note` sobre mínimos locais deveria ser `.callout-warning`: é armadilha
  real, não observação lateral.
- 5.6, o `.callout-important` final tem ~600 palavras e três argumentos empilhados. Divida:
  a contagem de passos fica no callout; a análise do ruído vira prosa com subtítulo próprio;
  a frase sobre vetorização migra para o "Na prática".
- O callout do `TypeVar` em 5.6 não se paga para quem já viu genéricos. Uma frase no corpo.

**Prosa — use estas reescritas**
- 5.1 §2: "do zero" três vezes em duas frases → *"Isso significa resolver vários problemas
  de otimização sem chamar um otimizador pronto. A técnica que vamos usar, o **gradiente
  descendente**, é justamente a que melhor se presta a isso: cabe em poucas linhas e não
  esconde nada."*
- 5.1 `.conceito`: "a direção **de entrada** em que a função cresce" é decalque de *input
  direction* → *"aponta, no espaço de entrada, a direção em que a função cresce mais rápido"*.
- 5.2: "Muita gente que aprende cálculo trava exatamente aqui... Vamos trapacear" e "nada
  além de álgebra do ensino médio" são condescendentes para este leitor → *"Não vamos
  precisar da definição formal de limite: aqui, 'limite' é o valor do qual a expressão se
  aproxima conforme `h` encolhe."* e corte a segunda.
- 5.3: "Se você rodar isso, vai ver que `v` **sempre** acaba muito perto de `[0,0,0]`" logo
  abaixo de uma saída com semente fixa → *"A semente fixa esconde o que importa: troque-a e
  o ponto de partida muda, mas o destino não — `v` termina praticamente na origem em
  qualquer partida."*
- 5.3 "Na prática": o parágrafo "O motivo de este livro ficar na versão simples não é
  ignorância do que existe" soa defensivo, e o guia proíbe exatamente isso. Corte-o; a
  última frase já faz o trabalho.
- 5.4: "podem fazer a função crescer — ou até **ficar indefinida**" → *"...ou levá-la para
  fora do domínio: um overflow, ou um logaritmo de número negativo."*
- 5.5: "diz o quão bons ou ruins são quaisquer parâmetros específicos" → *"diz o quanto um
  conjunto específico de parâmetros é bom ou ruim"*.
- 5.5 "Na prática": `LinearRegression().fit(X, y)` instanciado e ajustado na mesma linha.
  Atribua a uma variável — o leitor é programador e vai reparar.
- 5.6: "Os seus modelos vão frequentemente ter conjuntos de dados grandes" (modelos não têm
  datasets) → *"Na prática, porém, você vai trabalhar com conjuntos de dados grandes e
  gradientes caros de calcular."*
- 5.6: fixe o vocabulário — **lote** para *batch*, **minibatch** só para o nome da técnica.
  Hoje oscila entre "batch", "lote", "minibatch", "lote inteiro", "batches".
- 5.6: "Entre os epochs 80 e 140 **registrados nesta renderização**" — corte "registrados",
  confunde.

---

## NÃO MEXA NISTO

Os dois revisores destacaram como bom:

- O `.callout-important` do `index.qmd` ("Por que este capítulo pesa mais que os outros") —
  chamado de a melhor abertura do livro até aqui.
- O `.conceito` de 5.3 sobre decaimento geométrico e escala log.
- O `.callout-warning` de 5.4 sobre divergência.
- O `.exemplo` de 5.5 que liga à fórmula fechada do capítulo 8 — apontado como a melhor
  conexão do capítulo; use-o como modelo para as conexões que faltam.
- Os cinco callouts "Na prática", em especial o de autodiff (5.2) e o de
  `SGDRegressor` vs `LinearRegression` (5.5).
