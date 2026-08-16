# Capítulo 14 — Árvores de Decisão: correções

Duas revisões independentes, e **as duas elogiaram muito o capítulo**. A didática o chamou de
"o melhor capítulo do livro depois do 9 — talvez à frente dele". A de conteúdo reproduziu
**todos** os números por execução independente e confirmou que batem dígito a dígito com o HTML,
além de conferir a fidelidade ao capítulo 17 do Grus contra o PDF, seção por seção.

**Você não vai reescrever o capítulo.** Há um Crítico, um achado de enquadramento que muda a
conclusão de uma seção, e acabamento.

**A coluna `id` e o callout do `Intern` estão entre o melhor material do livro. Não os toque
além do que o contrato pedir.**

---

## Crítico

### C1 — A §14.6 ensina o contrário do que o próprio capítulo argumenta

`06-florestas-aleatorias.qmd:251` diz que combinamos "vários aprendizes fracos — tipicamente
modelos de **viés alto e variância baixa**". Isso é a receita do **boosting**, não da floresta.
É fiel ao Grus, e está errado aqui — **as duas revisões acharam isso de forma independente.**

O capítulo contradiz a si mesmo a duas telas de distância:

- `06:237` mede **0,9970 no treino contra 0,8239 no teste** — variância alta, viés baixo.
- `06:295` diz, corretamente, "a floresta reduz variância".
- `content/cap08/05-vies-e-variancia.qmd:20` define viés alto + variância baixa como
  **underfitting**.

A floresta parte de árvores de **variância alta**, que decoram, e reduz essa variância pela
média. Diga isso, e marque o escorregão do Grus num callout — o livro já trata erros do
livro-texto como conteúdo.

Aproveite e troque "aprendiz fraco" (`06:248`) por algo como "árvore deliberadamente pior" —
*weak learner* é termo técnico do boosting e aqui atrapalha.

---

## Importantes

### I1 — O experimento da §14.6 é honesto nos números e incompleto no enquadramento, e isso derruba o fecho da seção

Este é o achado mais sério, e ele **não** é sobre os números do capítulo, que estão certos.

A comparação publicada é floresta contra árvore **sem poda**. Mas a regra verdadeira do conjunto
sintético — `(a0 == 'x') or (a1 == 'y')` — usa exatamente dois atributos, então uma árvore rasa
a expressa perfeitamente. **Medido duas vezes, de forma independente**, na mesma base:

| modelo | acurácia no teste |
|---|---|
| árvore, `max_depth=1` | 0,7650 |
| árvore, **`max_depth=2`** | **1,0000** |
| árvore, `max_depth=3` | 0,9365 |
| árvore, sem limite | 0,8255 |
| floresta 3-de-8 (a melhor do capítulo) | 0,9284 |

**A árvore de duas perguntas acerta tudo, e nenhuma floresta chega perto.** Isso derruba o fecho
de `06:260` — "a floresta compra generalização com a única moeda que tornava a árvore especial"
— **neste conjunto**: aqui o modelo mais legível é também o mais preciso. E a §14.4 já
apresentou `max_depth` ao leitor, o que torna a omissão visível para quem prestou atenção.

**Não apague o experimento** — ele é a única medição do capítulo, e a revisão didática defendeu
com razão o desenho de quatro braços, que torna as duas fontes de aleatoriedade separadamente
visíveis. **Complete-o.** Acrescente o braço da árvore podada e escreva a conclusão honesta, que
é mais interessante que a atual:

> O ganho da floresta sobre a árvore **sem poda** é real, e é ganho de variância. Mas quando a
> estrutura verdadeira é simples o bastante para caber numa árvore rasa, a resposta mais barata
> não é a floresta: é uma regra de parada. A floresta ganha quando não se sabe de antemão que a
> estrutura é simples — que é o caso comum.

**Meça você mesmo** os braços que forem entrar. **Não use os meus números para outras regras** —
eu explorei uma regra de interação de três atributos com uma floresta improvisada mais fraca que
a do capítulo, e o resultado não é comparável. Se quiser mostrar um caso em que a floresta vence
de fato, construa-o e meça com o **mesmo** código de floresta do capítulo.

### I2 — "Nenhum atributo é puro ruído aqui" é um raciocínio inválido

`03-a-entropia-de-uma-particao.qmd:154` diz que "todos os quatro reduzem a incerteza inicial de
0,940 bit — **nenhum atributo é puro ruído aqui**".

O ganho de informação é **≥ 0 por construção**, então "reduziu a incerteza" não distingue sinal
de ruído. Medido: uma coluna 100% aleatória de três valores, sobre esses mesmos 14 candidatos,
ganha **0,128 bit em média** (mínimo 0,0013 em 1.000 sorteios, e **nunca** zero) — mais que os
0,048 do `phd`.

E a própria seção contradiz a frase 110 linhas depois, com o `id`. **Corrija a inferência** — e
note que o conserto reforça o material da coluna `id` em vez de competir com ele.

### I3 — A promessa que o capítulo 13 fez sobre este capítulo não é cumprida

`content/cap13/05-maquinas-de-vetores-de-suporte.qmd:292` promete que a árvore vai perguntar
"salário acima de 60.000?", com fronteira em **degraus paralelos aos eixos**, e que reescalonar é
indiferente. **O capítulo 14 não menciona reescalonamento, ordem, limiar numérico nem fronteira
de decisão** — o ID3 dele só divide atributos categóricos. Quem seguir a promessa não acha nada.

Pior, `01:92` afirma que a árvore "lida naturalmente com uma mistura de atributos numéricos e
categóricos", enquanto o `partition_by` implementado abriria **um ramo por valor distinto** numa
coluna contínua — exatamente a armadilha do `id` da §14.3.

Duas ou três frases na §14.4 fecham isso e ainda reforçam a §14.3: o ID3 deste capítulo só sabe
perguntar "qual é o valor?"; numa coluna contínua isso degenera no caso da matrícula, e é por
isso que o CART pergunta "está acima de tal limiar?".

### I4 — Referência quebrada

`05-juntando-tudo.qmd:256` cita a "**seção 8.4**" para treino/validação/teste. A §8.4 é
*Correção* (precisão e revocação); treino/validação/teste está na **§8.3**
(`content/cap08/03-overfitting-e-underfitting.qmd:197`).

Relacionado, mais frouxo: `06:158` atribui à §8.3 a lição "medição sobre poucas repetições é um
chute com aparência de número". O apoio mais próximo é o callout de estratificação
(`cap08/03:231`); ajuste a atribuição ou a frase.

### I5 — O capítulo não entrega o aluno em lugar nenhum

A §14.6 fecha em "O que a floresta cobra", que é bom, mas a última palavra **visível** é o
`callout-important` sobre a troca; a menção ao boosting está dentro do `callout-tip`
**colapsado**. Compare com `cap13/05:292`, que entrega este capítulo pelo nome e com promessa
concreta.

Faltam três frases depois do `callout-important`, e a dobradiça está pronta: a árvore comprou não
linearidade de graça, fazendo perguntas, e pagou em legibilidade ao virar floresta; o
[Capítulo 15](../cap15/index.qmd) compra a mesma não linearidade de volta ao gradiente do
[Capítulo 5](../cap05/index.qmd) — que este capítulo dispensou — e paga com um modelo que
ninguém lê nem por aproximação.

### I6 — A §14.4 reencena a §14.3 por três chunks

`criando-melhor-atributo`, `criando-ramos-level` e `criando-ramo-senior` reproduzem literalmente
a saída que a §14.3 já mostrou em código, em tabela **e** em figura. O aluno vê os mesmos quatro
números pela quarta vez antes de chegar ao único conteúdo novo (o ramo `Junior`).

Corte para uma frase de retomada e vá direto ao `Junior`. A §14.4 fica sendo o que ela deve ser:
a seção do **algoritmo** e da gulodez.

### I7 — A poda só existe dentro do callout de biblioteca

No corpo, a única resposta ao sobreajuste é a floresta, e o aluno sai achando que é a única. Uma
frase na §14.4, logo depois do ID3: o jeito mais simples de conter isso seria uma condição de
parada — profundidade máxima, mínimo de exemplos por folha —, o ID3 não tem nenhuma, e a §14.6
ataca o problema por outro caminho. **Isso também prepara o I1.**

### I8 — O experimento "guloso ≠ ótimo" está num callout, e é lição

`05-juntando-tudo.qmd:208-253` — são 30 linhas de código dentro de um `callout-warning`, e a
regra da casa é que **código que É a lição fica no corpo**. Promova a um `## O guloso não
encontra a menor árvore` e deixe no callout só a conclusão.

Aproveite: o texto pede que o aluno acredite em "seis folhas contra quatro", e a função `imprime`
já existe nessa página — **imprima as duas árvores**, e a diferença vira visível em vez de
numérica. A revisão de conteúdo mediu um reforço que o texto não usa: a árvore gulosa **erra 2
das 8 combinações** `(a,b,c)` e a enxuta acerta 8/8.

### I9 — A §14.2 põe a melhor intuição depois do código

A seção acerta a ordem geral, mas o `.conceito` que define $H$ **não menciona a unidade**, e o
título "Incerteza, medida em bits" abre um bloco onde a palavra *bit* não aparece. A leitura mais
valiosa — "entropia = quantas perguntas de sim/não faltam" — está no `.exemplo` de `02:101`,
**depois** do código. Suba uma frase para o `.conceito`.

### I10 — Ligação faltando: a §8.5 nunca é citada

A §14.6 é um argumento de **variância** do começo ao fim (ver C1), e
`content/cap08/05-vies-e-variancia.qmd` não é citada uma única vez. No mesmo espírito,
`cap08/06-extracao-e-selecao-de-atributos.qmd` é o par natural do "Na prática" da §14.3, que é
literalmente seleção de atributos.

---

## Menores

- **M1** — `06:42`: `oob_score` aparece no **corpo** de uma seção, única menção de
  `scikit-learn` fora de callout no capítulo, e antecipa o `oob_score=True` do fecho. Corte a
  frase; o conceito *out-of-bag* se sustenta sozinho.
- **M2** — `03:111` e `04:111`: "Nenhum doutorado sempre resultou em `True`, e doutorado sempre
  resultou em `False`" trava o leitor de português (lê-se como negativa de sentença). Sugestão:
  *"Entre os juniores, quem não tem doutorado se saiu bem — sempre; quem tem, se saiu mal —
  sempre."*
- **M3** — `03:273`: cita "os **cortes de idade**" do capítulo 1;
  `content/cap01/03-hipotese-motivadora-datasciencester.qmd:374` fala de **anos de experiência**
  (cortes em 3,0 e 8,5).
- **M4** — `03:156`: "Dá para ver por quê olhando a partição" — acento incorreto no meio da
  frase. Use *"A partição mostra por quê:"*.
- **M5** — `04:166`: "Na prática: o que a biblioteca faz com a mesma **gulodice**". Em pt-BR
  "gulodice" é guloseima, não a propriedade do algoritmo. Sugestão: *"Na prática: a biblioteca é
  gulosa igual — e o que ela acrescenta"*.
- **M6** — `05:29`: "São **doze** linhas"; o chunk tem onze. Números vêm da saída.
- **M7** — `06:127`: a saída imprime "**1 árvores**", e o rótulo "(folha só)" soa invertido.
  `f"{n:3d} árvore{'s' if n > 1 else ''}"` e "(só uma folha)".
- **M8** — `05:189`: o comentário `# Deve prever True` endossa a resposta que o callout logo
  abaixo critica. Mantenha o `assert`, troque o comentário.
- **M9** — `03:266`: "vence, com folga, e por goleada" é redundante; escolha uma.
- **M10** — `06:224`: a variável `mata` num laço que ao lado usa `floresta` e `bagging`. Prefira
  `floresta_k`.
- **M11** — `01:107`: vírgula deslocada em "que já dá bastante trabalho**,** para conjuntos
  grandes".
- **M12** — Boosting é mencionado **três** vezes (index, `01:126`, `06:295`) antes de o aluno ter
  qualquer ideia do que seja. Corte a de `01:126`, a mais cedo e a menos motivada.
- **M13** — `06:63-99`: `build_tree_forest` completa um fragmento do Grus que referencia um
  `self.num_split_candidates` inexistente. O texto diz "a diferença cabe em cinco linhas" sem
  registrar que o original é trecho incompleto, não função.
- **M14** — `01:92` reproduz do Grus que a árvore lida com atributos faltantes; verdade para
  árvores em geral, **falso para o ID3 construído aqui**. Some com o I3.
- **M15** — `fig-particao-barras` (`03:184`): a legenda diz "a barra verde é o atributo
  vencedor", mas no painel dos sêniores o vencedor é `tweets` com 0,000 — barra de largura zero,
  invisível. Um marcador (▸) ou o rótulo em verde resolve, e **o ponto alto do capítulo passa a
  aparecer na figura**, não só no texto.
- **M16** — **Inflação de callouts:** a §14.6 tem 8 boxes numa página e a §14.3 tem 7; o capítulo
  9 tem 3 por seção. Os itens I8 e M1 já removem dois — dê um passe olhando quais outros são
  prosa que fugiu do corpo.
- **M17** — Só para registro: `DecisionTreeClassifier(criterion='entropy')` aparece em três dos
  seis "Na prática". O da §14.4 pode delegar ao da §14.5.

---

## Não mexa nisto

- **A coluna `id` (§14.3)** é o melhor material do capítulo e a melhor aplicação da regra "os
  erros do livro-texto são conteúdo": o Grus adverte, aqui se executa, o callout generaliza para
  carimbo de tempo e número de pedido, e **reaparece** na §14.6 como o viés do
  `feature_importances_`.
- **O callout do `Intern` (`05:196`)** — mostra o mecanismo, nomeia o defeito como sendo da
  *interface*, generaliza, e é pago duas vezes depois. A revisão de conteúdo mediu que **61 de
  100 árvores** caem mesmo no `default_value` ali: a "maioria" do texto é literal.
- **O desenho de quatro braços do experimento sintético** — é o que torna as duas fontes de
  aleatoriedade separadamente visíveis, que é o que o Grus não faz. O I1 pede para **completá-lo**,
  não para desmontá-lo.
