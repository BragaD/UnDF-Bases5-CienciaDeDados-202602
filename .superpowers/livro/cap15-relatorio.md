# Cap. 15 — Redes Neurais: relatório de escrita

**Status:** 5 arquivos escritos (`index` + 4 seções). Nenhum arquivo criado, renomeado ou apagado.

**Verificação:** `render OK (tentativa 2)` no primeiro render. O aviso de edição concorrente
apontou `cap14/06`, `cap17/06` e `cap17/index` — **nenhum arquivo do cap. 15**, então o `_freeze`
deste capítulo é confiável. Conferi todas as saídas executadas dentro de
`_freeze/content/cap15/*/execute-results/html.json` e abri as três figuras: cada número do texto
bate com a saída, e cada figura mostra o que a prosa diz que ela mostra. Depois disso fiz três
correções de precisão (ver "Correções pós-render") e rodei um segundo render + `make teste`.

## Números — todos medidos no container, nenhum de memória

- **XOR** (`seed(0)`, 2→2→1, taxa 1,0, 20.000 épocas, 0,45 s): `[0,0]→0,009034` · `[0,1]→0,992329` ·
  `[1,0]→0,992328` · `[1,1]→0,007856`. Pesos finais **arredondam exatamente** para
  `[7,7,-3]`, `[5,5,-8]`, `[11,-12,-5]` — os três vetores que o Grus imprime. Camada escondida
  aprendida: neurônio 1 = **OU**, neurônio 2 = **E** — **ordem trocada** em relação à rede feita
  à mão na §2. Virou o gancho da interpretabilidade.
- **Correção ao brief (simetria):** a simetria do XOR relaciona só o par do meio (0,992329 /
  0,992328) e os pesos dentro de cada neurônio (6,9535/6,9528; 5,1159/5,1154). `[0,0]` e `[1,1]`
  são cada um a troca de si mesmos — nada força que sejam iguais, e não são (0,009034 × 0,007856).
  O texto diz isso explicitamente.
- **Fizz Buzz** (`seed(0)` fresco, 10→25→4, taxa 1,0, 500 épocas, 923 exemplos, ~47 s):
  **96/100** no teste (1–100, nunca vistos), 903/923 = 97,8% no treino. Erros: 4 e 34 (disse
  "fizz"), 70 e 100 (disse o número). Base do "sempre a classe majoritária" = 53/100.
- **O melhor achado, não previsto no brief — o platô É o palpite preguiçoso.** A perda cai de
  2768,9 para ~596 e fica quase parada da época 15 à 120. Medido: nas épocas **20 e 50 a rede
  responde "o próprio número" para os 923 exemplos**, acertando 493/923 = 53,4% — exatamente o
  classificador-base do cap. 8. Só depois ela escapa. Isso rende o fecho do "Na prática":
  `MLPClassifier(hidden_layer_sizes=(25,), activation='logistic')` **para na iteração 51** e
  devolve 0,53 — o critério `tol=1e-4`/`n_iter_no_change=10` lê o platô como convergência. O
  nosso laço atravessa o platô porque não tem critério de parada nenhum.
- **Outros valores do "Na prática" (sklearn 1.9, medidos):** `Perceptron` aprende E com
  `[[3,2]]/-4` e OU com `[[2,2]]/-1` (idênticos aos escolhidos à mão pelo Grus); no XOR devolve
  `coef_=[[0,0]]`, `intercept_=[0]`, acurácia 0,5, **sem aviso nenhum**. `MLPClassifier` no
  Fizz Buzz: `(100,)+relu` = 0,860 teste em ~2 s; `(25,)+logistic+lbfgs` = 0,850 em ~0,4 s.
  `coefs_`/`intercepts_` são separados (o truque do viés é contabilidade nossa);
  `out_activation_='softmax'`, `loss='log_loss'` no caso multiclasse.

## Decisões de escrita

- A troca degrau→sigmoide está na §2, num `.conceito`, dita como o brief pediu: a derivada do
  degrau é zero onde existe e indefinida no salto, então **nada do cap. 5 se aplica** sem a troca.
  Figura de duas faixas: as funções e as derivadas.
- §3 constrói a retropropagação pela ideia de **culpa** (∂perda/∂z) antes de qualquer álgebra:
  culpa direta na saída, culpa de um peso = culpa do neurônio × a entrada que ele multiplica,
  culpa emprestada nos escondidos. A derivação completa fica num `.exemplo` opcional.
- Dois achados de leitura do código viraram callout: **o fator 2 que sumiu** (`output_deltas` é o
  gradiente exato de *metade* da soma dos quadrados; a §4 imprime a soma inteira) e
  **`sqerror_gradients` só funciona para duas camadas** (`hidden_outputs, outputs = feed_forward(...)`
  desempacota exatamente dois) — que é a motivação direta do cap. 16.
- Arco da interpretabilidade: anunciado no `index`, plantado no `.conceito` do fim da §3 (a rede
  achou os mesmos dois atributos em ordem trocada; soluções equivalentes) e fechado na §4.

## Correções pós-render (minhas, na releitura)

Três afirmações que eu tinha escrito e que a verificação não sustentava:

1. **§1** dizia que, no XOR, "as correções da regra de treino se cancelam exatamente" — mecanismo
   que eu não medi. Testei seis sementes: os pesos finais **variam** (`[[0,0]]`, `[[0,-1]]`,
   `[[1,0]]`…), a acurácia dá **0,5 nas seis**. O texto agora afirma o que foi medido.
2. **§4** dizia que no platô "cada alteração isolada piora a perda". Falso: a perda **cai**, de
   ~597 (época 25) a ~589 (época 100) — o gradiente existe e aponta certo, só é minúsculo.
   Reescrito com os números.
3. **§2** o chunk da figura usava `dir` como nome de eixo, sombreando a builtin. Renomeado.

## O que ficou de fora, e por quê

- **Nenhum corte de iterações.** 20.000 épocas no XOR e 500 no Fizz Buzz, como o brief mandou.
- Não usei `MLPRegressor`, nem PyTorch/Keras em código: só afirmações que consegui medir no
  container. As menções a autodiff em §3 são conceituais, sem número.
- A `Figure 18-1` do Grus (espaço de decisão) foi refeita como três painéis E/OU/XOR em vez de
  reproduzida — a impossibilidade do XOR ficou mais visível assim, e ganhou prova algébrica de
  quatro desigualdades num `.exemplo`.

## Preocupações

1. A §4 é o chunk mais caro do livro (~1 min). Com `freeze: auto` isso só dói quando o arquivo
   muda, mas quem for corrigir a §4 paga o minuto a cada rodada.
2. A tabela do "Na prática" da §4 mostra a nossa rede (0,96) acima da melhor configuração de
   biblioteca testada (0,86). Escrevi explicitamente que isso **não** quer dizer que o nosso
   código é melhor — 100 números de teste, dez acertos de diferença. Se uma revisão quiser mexer
   nesse trecho, é aí que ele pode virar propaganda por acidente.
3. O `index` promete que o cap. 16 generaliza esta rede numa biblioteca de camadas. O cap. 16
   ainda é stub — é dívida a cobrar de quem o escrever.

---

# Adendo — aplicação das correções (`cap15-correcoes.md`)

Status: **todos os itens do contrato aplicados**. `make render` → `render OK (tentativa 1)`;
`make teste` → **24 passed**. Nada ficou de fora.

## Importantes (ambos em `04:238`, a frase foi reescrita e virou dois parágrafos)

- **I1** — Saiu a implicação falsa ("acertava 100% do treino **e por isso mesmo** não dizia
  nada"). Entrou a leitura correta: o que se lê é a **distância** entre treino e teste, e o
  exemplo agora vem da [seção 14.6], que é material bem mais forte — árvore sem poda 99,7%
  treino / 82,4% teste, contra a de profundidade 2 com 85,0% treino / **100%** teste. O link
  passou de `../cap14/index.qmd` para `../cap14/06-florestas-aleatorias.qmd`.
- **I2** — "Viés e variância equilibrados" removido. Ficou "não há sinal de sobreajuste" +
  "menos de dois pontos separam os dois números", sem nomear nada que o cap. 8 proíbe medir
  num único treino.

## Padronização

14 ocorrências de "época/épocas" → `epoch/epochs` (gênero masculino, como no cap. 5). Inclui
`plt.xlabel("epoch")`, o `fig-cap` "epoch a epoch", e o `print` do diagnóstico (variável de laço
`epoca` → `epoch`, para o rótulo impresso e o código não divergirem). **`grep -c época
content/cap15/` agora é 0**, e o eixo do gráfico foi conferido no PNG renderizado.

## Menores

- **M1** — Nota de meia linha no topo da caixa de derivação de `03` ("Desta caixa em diante, $i$
  numera os de saída e $h$, os escondidos; o `i` que percorre `hidden_outputs` é este $h$") e um
  aposto na ponte de `:123`, que é exatamente onde as duas convenções se encostam.
- **M2** — "é, exemplo a exemplo, o espelho" → "é praticamente o espelho — seria exatamente o
  espelho se os dois pesos já fossem iguais". A frase seguinte ("quase igualmente") ficou intacta.
- **M3** — `~0,4 s` → `~2 s` na linha `(25,) logistic lbfgs`. Não mexi na leitura de "uma a duas
  ordens de grandeza mais rápida", que continua válida (1 min contra 2 s).
- **M4** — "a rede **aprendeu** divisibilidade" → "construiu alguma coisa que **faz o papel** da
  divisibilidade", com um parágrafo novo cobrando o preço: 70 e 100 são múltiplos de 5 e ela erra
  os dois; 4 e 34 levam "fizz" chutado. Reusa a formulação já preparada no callout de `:77–79`.
- **M5** — Comentei a saída (não escondi): parágrafo curto após o chunk dos pesos iniciais dizendo
  o que são os nove números e mandando guardar a ordem de grandeza, que a subseção "O que a rede
  aprendeu" cobra de volta ($[7,7,-3]$, $[5,5,-8]$, $[11,-12,-5]$).

## Verificação

Reproduziu idêntico após o render: `96 / 100`, `erros: [(4,'fizz','4'), (34,'fizz','34'),
(70,'70','buzz'), (100,'100','buzz')]`, e as seis linhas do diagnóstico (199, 493, 493, 494, 632,
903 de 923). O PNG `fig-perda-fizz-buzz` foi aberto: eixo `epoch`, queda abrupta, platô em ~590
entre os epochs ~20 e ~125, descida real depois — exatamente o que a prosa descreve.

Nada da seção "Não mexa nisto" foi tocado.

## Preocupações

1. O `make render` avisou edição concorrente em `content/cap16/04-...qmd` (outro agente). **Não
   afeta o cap. 15** — `test_freeze_corresponde_ao_fonte` passa, e a própria rodada 3 do alvo já
   reexecutou o arquivo do cap. 16. Fica o registro para quem for fechar o cap. 16.
2. Verifiquei o HTML do `_book/` logo após o meu render; segundos depois outro `quarto render`
   começou e limpou `_book/content/`. As evidências acima foram colhidas antes disso, e o
   `_freeze/` do cap. 15 (que é o que o próximo render reusa) está correto.
3. M3 ficou como `~2 s` e a linha do `relu`/`adam` também diz `~2 s`. São duas medições
   independentes que calharam próximas, não um erro de cópia.

---

# Adendo — segunda rodada de correções (`cap15-correcoes-2.md`)

**Status: 8 Importantes e 5 Menores aplicados. `render OK`, `make teste` 24/24.**

## O que mudou, item a item

- **I1** — `04`: "distância" → **queda**, com os quatro números conferidos contra
  `content/cap14/06-florestas-aleatorias.qmd`: sem poda 99,7 → 82,4 (**cai** 17,3); profundidade 2
  85,0 → 100 (**sobe** 15,0); a nossa rede 97,8 → 96,0 (cai 1,8). O parágrafo agora diz
  explicitamente que as duas diferenças têm tamanho parecido e sentidos opostos, e que é o sinal
  que separa os casos. A frase final ("o modelo com o melhor número de treino era o pior") ficou.
- **I2** — `02`, logo após o `.conceito`: a regra do perceptron histórico ("a cada exemplo errado,
  empurre os pesos na direção da entrada") não é gradiente descendente, existe porque o gradiente
  não estava disponível, e só vale para um neurônio — com camadas escondidas ela não tem o que
  dizer. Fecha a pergunta que `01` abria com "regra de treino própria".
- **I3** — `03`: a nota de índice agora diz **qual `i` é qual** (`output_grads` → saída;
  `hidden_deltas`/`hidden_grads` → escondido; `[n[i] for n in network[-1]]` com os dois papéis na
  mesma linha) e nomeia o problema: o código reaproveita a letra, a matemática não.
- **I4** — `03`, chunk `uma-passada-para-tras` entre a rede aleatória e o treino. Uma passada para
  trás sobre `x = [1, 0]`, com três parágrafos lendo a saída.
- **I5** — `04`, dentro do `.conceito`: a regressão não resolve porque uma soma ponderada de bits
  não separa múltiplos de 3 — 0, 1, 2, 3 têm bits $[0,0]$, $[1,0]$, $[0,1]$, $[1,1]$ e os dois
  múltiplos caem em cantos opostos, que é o argumento das quatro desigualdades da §1; a árvore não
  resolve porque profundidade 10 é uma folha por padrão de bits, e nenhum dos padrões de 1 a 100
  apareceu no treino.
- **I6** — `04`, chunk `pesos-escondidos-fizz-buzz` logo antes do `.conceito`: dois dos 25 vetores.
- **I7** — `04:270`: cortado o mecanismo. Agora "alguma combinação desses bits que **funciona** —
  não necessariamente a soma alternada nem o ciclo módulo 4 (…), apenas algo que acerta 96 dos 100".
- **I8** — `03`: o treino é nomeado **gradiente descendente estocástico**, ligado à
  [seção 5.6](../cap05/06-minibatch-e-estocastico.qmd), com os 20.000 epochs × 4 exemplos =
  **80.000 passos**.
- **M1** — `04`: meia dúzia de linhas dizendo que `epoch_loss` soma previsões de redes que mudam
  durante o epoch — não é a perda de uma rede fixa —, e que é isso que produz os solavancos do fim
  da curva (conferidos no PNG antes de escrever).
- **M2** — índice: "cada uma das **três primeiras** seções existe por causa de um limite da
  anterior, e a quarta gasta tudo o que elas construíram num problema só".
- **M3** — uma frase de passagem para o cap. 16 **depois** do `.conceito`, antes do "Na prática".
  A frase de `:283` continua fechando o `.conceito`.
- **M4** — as cinco: "programador excepcional"; "no lugar dela vamos aplicar"; `*n*` → `$n$`;
  `## Olhando os erros de perto`; e o viés — `01` agora liga `bias` a "viés" e desarma a colisão
  (parâmetro, não erro sistemático; nada a ver com viés-variância do cap. 8; o cap. 12 chamava de
  *termo constante*).
- **M5** — o callout "A semente não é opcional" virou prosa; sobrou só o específico (inicializações
  diferentes → **soluções** diferentes). A §3 foi de nove caixas para oito.

## Os números novos na página

```
saída       0.7838  (alvo 1)         culpa -0.036630
escondido 1  0.7799   peso p/ a saída 0.7838   culpa -0.004929
escondido 2  0.6601   peso p/ a saída 0.3033   culpa -0.002493

escondido  0  [ -2.78,  -5.59, -11.34,  -9.80,  -2.69,  -6.25,   3.05, -19.00,  -2.73,  -5.97,  15.91]
escondido 13  [ -2.17,  -3.63, -14.70,   3.28,  -2.23,  -3.88,   1.93,   2.95,  -2.29,  -3.73,   8.06]
```

Nada da seção "Não mexa nisto" foi tocado.

## Preocupação — o I6 mostrou mais do que se esperava

Ao conferir os pesos impressos antes de escrever a prosa, apareceu **estrutura visível** neles, e
ela é real: os pesos dos bits **0, 4 e 8** saem quase idênticos em quase todos os 25 neurônios (e
os de 1, 5, 9 entre si, e assim por diante), porque $2^k \bmod 15$ tem **período 4** — bits da
mesma classe são literalmente intercambiáveis neste problema. Medi os 25 (script descartado):
o espalhamento dentro dos grupos é uma fração do espalhamento total. E há casos mais fortes:
o **neurônio 7** tem pesos alternando sinal a cada bit — que é a **soma alternada**, o critério de
divisibilidade por 3 —, e o **neurônio 16** é quase perfeitamente periódico com período 4.

Consequências, e o que fiz:

1. A prosa do I6 **não** afirma que nada se lê. Ela mostra os dois vetores, registra o fragmento
   (bits 0, 4 e 8; o resto módulo 15) e argumenta que isso não é uma resposta: saber que três bits
   são tratados como equivalentes não diz o que o neurônio responde. Escrever "ilegível" ali seria
   uma afirmação que um aluno derruba imprimindo os 25.
2. O `.conceito` **continua verdadeiro** e não foi mexido: nenhum neurônio isolado corresponde a "é
   múltiplo de 3", e não por acaso — divisibilidade não é monótona em soma ponderada nenhuma
   (soma alternada de 0 a 3 mod 3 são valores intercalados), então uma sigmoide sozinha não a
   calcula. A informação continua morando na combinação.
3. **Fica para uma terceira rodada, se você quiser:** o I7 me mandou cortar "aproxima a soma
   alternada e o ciclo módulo 4" por falta de sustentação, e a evidência dos pesos agora **sustenta**
   essa afirmação. Cortei, como o contrato pediu. Mas há aqui material para uma caixa curta — a
   rede reinventou o período 4 de $2^k \bmod 15$ — que seria um dos melhores momentos do capítulo
   e que eu não escrevi por estar fora do contrato.

## Verificação

`make render` → `render OK`; `make teste` → **24 passed**. Conferi no HTML publicado
(`_book/content/cap15/*.html`) as duas saídas novas e as marcas de texto de cada item (queda,
"Olhando os erros de perto", 80.000 passos, "regra do perceptron histórico", "três primeiras
seções", ausência do callout da semente). Foram precisas **quatro** chamadas a `make render`: uma
saiu por lock de outro agente e duas por orçamento de tempo (a corrida do bind mount), o que é
esperado e não é falha de conteúdo.

---

# Adendo — rodada 3 (item único: a simetria dos bits)

## O que eu medi

Reproduzi o treino da página fora do render (mesma semente 0, mesmos 500 epochs) e confirmei a
réplica pelos pesos publicados dos neurônios 0 e 13 — batem dígito a dígito. Métrica: para cada
par de bits $(j,k)$, a distância média $\frac{1}{25}\sum_i |w_{ij} - w_{ik}|$ sobre os 25
neurônios escondidos, dividida pela escala típica de um peso (média de $|w|$ sobre os 250 pesos
de bit, **5,70**). Os valores publicados:

| par | resíduo | distância |
|---|---|---|
| 0–4 / 0–8 / 4–8 | 1 | **2% / 4% / 3%** |
| 1–5 / 1–9 / 5–9 | 2 | 29% / 31% / **7%** |
| 2–6 | 4 | 95% |
| 3–7 | 8 | 150% |
| os 37 pares de resíduos diferentes | — | média **138%**, de **90%** a **200%** |

Os seus números de referência conferem (3 / 22 / 95 / 150). O único que difere é o de fora do
grupo: mediu-se **138%**, não 141% — a diferença deve estar em quais pares entram na média, e a
minha é sobre os 37 pares de resíduos distintos. Publiquei par a par em vez de agregado por
grupo: são só oito linhas, e assim nenhum número do texto depende de uma média que o leitor não
vê. O acréscimo que a sua tabela não tinha é a **faixa** dos pares não relacionados, 90%–200%: é
ela que impede ler os 95% do par 2–6 como simetria fraca — há pares de resíduos diferentes mais
próximos que ele.

## Onde ficou

`content/cap15/04-exemplo-fizz-buzz.qmd`, subseção `###` **"O que dá para achar nos pesos, se
você souber a pergunta"**, dentro de "O que a rede aprendeu, e por que não dá para saber":
depois do parágrafo "Quem procurar com afinco…" e **antes** do `.conceito`, que não foi tocado.
Encurtei aquele parágrafo — ele antecipava a conclusão inteira — deixando nele só a observação
crua (os seis pesos, e os outros sete espalhados por mais de vinte unidades) e o gancho.

## Preocupações

1. **Tensão com o parágrafo que já estava lá**, o que diz que a rede montou "não necessariamente
   a soma alternada nem o ciclo módulo 4". Não é contradição e não mexi nele, mas o texto novo
   precisa carregar a distinção para o leitor não sentir o atrito: o que se mediu é *quais bits
   o neurônio se recusa a distinguir*, não *como* ele os combina. Está dito explicitamente no
   último parágrafo da subseção. Se você quiser tornar isso mais nítido, é ali.
2. **O `.conceito` diz que nenhum neurônio corresponde "a coisa alguma que se diga em
   português"** — e a subseção acaba de dizer uma coisa em português sobre os 25. Vale a mesma
   distinção acima, e por isso a subseção fecha negando ser interpretabilidade antes de o
   `.conceito` começar. É o ponto do capítulo em que eu olharia primeiro numa revisão.
3. **A subseção depende da semente.** Ela é fixa (`random.seed(0)`) e o `_freeze` guarda a saída,
   mas qualquer mexida no treino da §4 — epochs, `learning_rate`, `NUM_HIDDEN` — refaz esses oito
   números e derruba cinco afirmações do texto de uma vez. Fica registrado aqui porque o próximo
   a mexer no chunk de treino não tem como adivinhar.
