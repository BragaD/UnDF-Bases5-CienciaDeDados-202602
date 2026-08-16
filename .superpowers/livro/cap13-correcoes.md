# Capítulo 13 — Regressão Logística: correções

Duas revisões independentes. **As duas elogiaram o capítulo** — a didática disse que é "o melhor
uso de callouts do livro depois do 9", a de conteúdo reproduziu todos os números e confirmou que
a §5 prova mesmo o que afirma, por dois caminhos independentes. **Você não vai reescrever o
capítulo.**

Há **um Crítico**, e ele é bom: uma afirmação sobre ponto flutuante que soa erudita, é falsa, e
**contradiz frontalmente o que o capítulo 10 ensina**.

---

## Crítico

### C1 — O callout do `assert` de igualdade exata inventa um mecanismo, e absolve o que o capítulo 10 condena

`03-aplicando-o-modelo.qmd:240`. O callout diz, sobre o `assert` que compara a
log-verossimilhança nas duas escalas:

> "Não é sorte nem descuido: (…) para cada ponto o produto escalar reescalonado e o
> desescalonado produzem o mesmo `float64` bit a bit (…) o Grus a escreveu de modo que as
> operações se cancelem exatamente."

**Isso é falso, e foi medido duas vezes de forma independente:**

- **Ponto a ponto não se cancela.** Numa série, 8 de 200 produtos escalares são bit-idênticos;
  noutra, 35 de 200. A diferença máxima fica na casa de 10⁻¹⁵. A igualdade **só aparece na
  soma** — e por arredondamento, não por álgebra.
- **E nem na soma ela é confiável.** Reavaliando o mesmo `assert` com o β de cada 100 épocas do
  próprio treino: vale em 33 de 59 numa medição e em 18 de 30 na outra. **É cara ou coroa.** O
  `assert` do Grus passa para o β final específico dele, e passaria a falhar com outro.

**O problema maior é que isto contradiz o capítulo 10.** `content/cap10/04-testando-o-modelo.qmd:74-84`
ensina exatamente este construto — `assert` de igualdade exata de float — como **um erro
instrutivo do próprio livro-texto**, e prescreve `math.isclose`. O capítulo 13 pega o mesmo
construto e o absolve, com um mecanismo que não existe. Pior: ele conclui que isso "só se faz
quando se sabe *por que* os bits têm de coincidir", então o aluno sai com uma **regra falsa** e
com a impressão de que os dois capítulos discordam.

**O conserto é melhor do que o texto atual, e é conteúdo de primeira.** A verdade é mais
interessante que a ficção: o `assert` passa, e passa por sorte. Duas somas de ponto flutuante em
ordens diferentes coincidiram nos últimos bits para *este* β; para outros, não coincidem. Isso é
a mesma lição do capítulo 10, agora com uma demonstração mais afiada — **mostre o `assert`
falhando** com um β do meio do treino, e feche apontando para a §10.4 e para `math.isclose`.

**Consertos menores no mesmo callout:** o link aponta para `../cap10/03-implementacao.qmd`; o
exemplo está em `04-testando-o-modelo.qmd`.

---

## Importantes

### I1 — A tese do capítulo está atrás de uma dobra, e o índice a contradiz

A encenação da falha **funciona** — a sequência `estouro` → `dissecando` → `dois-modos-de-falhar`
→ o callout "Duas falhas, e a silenciosa é a pior" é excelente, e "perfeição — para um β que foi
sorteado ao acaso segundos atrás" é a frase certa.

O problema é o que vem depois. A generalização — *o número na sua tela pode ser mentira e você
não tem como saber* — aparece **uma única vez**, na última linha do "Na prática" da §3, que é
`collapse="true"` e portanto **fechado por padrão**. A frase que define a disciplina está
escondida. E o objetivo nº 5 do `index` reduz tudo a "por que reescalonar os dados é obrigatório
neste modelo" — exatamente a leitura rasa que a seção existe para evitar.

Três movimentos:

1. Trocar o objetivo do índice por algo como *"Explicar por que um ajuste pode reportar perda
   zero e estar completamente errado, e por que nenhuma biblioteca teria mostrado isso a você"*.
2. Levar a ideia para a **prosa corrida** da §3, logo depois do `callout-warning` e antes de "O
   conserto". O ponto a fazer: `LogisticRegression().fit()` não teria produzido **nenhuma** das
   duas falhas — nem o `ValueError`, porque a biblioteca calcula a perda por rotinas que nunca
   formam `1 - 1.0`; nem o `-0.0`, porque ela nem expõe a perda de um ponto isolado. Os dois
   números que o aluno acabou de ver só são visíveis de dentro.
3. No "Na prática" da §3, o parágrafo "A biblioteca não quebra com os dados brutos" hoje só
   responde ao `ValueError`. Ele precisa rebater também a falha **silenciosa**.

**Efeito colateral a corrigir junto:** a §2 já entrega mecanismo, lugar e conserto ("uma bomba
armada… vai explodir na próxima seção… na primeira conta do primeiro ponto… se um único passo
preparatório for esquecido"). Quando a §3 pergunta "O que acontece se você simplesmente
ajustar?", o leitor já sabe. **Corte da §2 o trecho a partir de "não em algum caso patológico
raro"** — o aviso continua armando a bomba sem dizer onde ela está. O `-0.0` não é antecipado em
lugar nenhum, e isso está certo: é a surpresa que sobrevive.

### I2 — O capítulo não entrega o aluno em lugar nenhum

A §5 termina no "Na prática" colapsado e para. Não há fecho de capítulo — compare com "O que
isso amarra", da §11.3 — e **o capítulo 14 não é citado uma única vez** nos seis arquivos.

A ponte está pronta e é forte: todo modelo do livro até aqui traça uma fronteira **linear** no
espaço dos atributos; o kernel compra curvatura trocando o espaço; a árvore chega à curvatura
por um caminho que não tem produto escalar, não tem coeficiente e não tem gradiente — e para o
qual **medir salário em reais ou em desvios padrão é rigorosamente indiferente**, o que fecha
justamente a lição desta seção. Escreva um `## O que este capítulo deixa` **antes** do callout
final, retomando também a escada 11 → 12 → 13 das fórmulas fechadas.

### I3 — A repetição são quatro cópias, e a §5 não a reconhece

`rescale` é definida na §1, §3, §4 e §5; o ajuste de 5.000 épocas é refeito na §3, §4 e §5. A §3
e a §4 explicam por quê; **a §5 não diz uma palavra** — o leitor abre a seção e leva 40 linhas de
código já visto na cara, sem aviso.

Ordem de ataque, do mais barato ao mais estrutural:

1. **A §5 ganha a frase que a §4 já tem** (custo zero): *"De novo o de sempre: kernel próprio,
   `beta` não atravessa páginas. O bloco abaixo é o ajuste da [seção 13.3](03-aplicando-o-modelo.qmd),
   letra por letra."*
2. **`#| echo: false` nos chunks que refazem o ajuste na §4 e na §5**, deixando a saída visível.
   Já é convenção da casa — "código que não é a lição" —, e ali o código de fato não é a lição
   da seção. Ponha um `.callout-note` de duas linhas dizendo o que rodou.
3. Um callout único na §3 explicando a regra do kernel de uma vez, com a §4 e a §5 apontando de
   volta para ele.

**Não** use `code-fold: true`: não há um único uso disso no livro, e convenção nova precisa de
decisão explícita, não de estreia numa rodada de correção.

### I4 — "espaço de parâmetros" está errado, e o Grus erra junto

`05-maquinas-de-vetores-de-suporte.qmd:101` diz "um **hiperplano** que corta o **espaço de
parâmetros** em dois semiespaços". A fronteira $\{x : \beta \cdot x = 0\}$ vive no espaço de
**atributos** (experiência × salário) — é o plano da figura logo acima. O espaço de parâmetros é
onde mora o β.

O Grus escreve o mesmo erro na p. 205 ("splits the parameter space"). **Este livro já trata erros
do livro-texto como conteúdo** — então corrija o texto e marque o erro num callout, em vez de
reproduzi-lo em silêncio ou de sumir com ele.

### I5 — Uma dívida do capítulo 11 fica sem o nome que ela prometeu

A §11.3 anunciou explicitamente a troca "de normal para **Bernoulli**". A §2 deriva
$f^{y}(1-f)^{1-y}$ sem nunca dizer a palavra. Acrescente, depois de "Uma fórmula, os dois casos,
sem `if`", uma frase nomeando a distribuição de Bernoulli e apontando para a
[seção 11.3](../cap11/03-maxima-verossimilhanca.qmd). Fecha a dívida com o nome que o aluno foi
mandado procurar.

---

## Menores

- **M1** — `02-a-funcao-logistica.qmd:58`, título "Por que não dá para minimizar quadrados". Dá,
  sim. O Grus (p. 200-201) diz que soma de quadrados e máxima verossimilhança **deixam de ser
  equivalentes**, não que uma seja impossível. O corpo da seção está certo; só o título afirma
  impossibilidade.
- **M2** — `02:180` diz "$\log(1{,}11\times10^{-16}) \approx -36{,}74$ — esse é o limiar
  preciso". O limiar é **+36,7368** = $-\log(2^{-53})$ = $53\ln 2$ (conferido por bissecção até o
  último dígito). Base e magnitude certas, sinal apresentado de lado.
- **M3** — `03:210`: "as 4.000 épocas restantes mexem na quarta casa decimal". Medido: perda
  39,96350015 → 39,96349522, diferença 4,9 × 10⁻⁶ — **sexta** casa. O que muda na terceira é o β
  (4,6903 → 4,6930). Diga qual dos dois.
- **M4** — `04:167`: "Dois dos três falsos negativos estão logo abaixo do limiar, em 0,457 e
  0,163". **0,163 não é limítrofe** — é o modelo 84% confiante do lado errado. Sugestão: *"Um dos
  três, com 0,457, é limítrofe: o tipo de erro que se aceita. Outro, com 0,163, já é uma aposta
  errada com alguma convicção."* E "os quatro falsos positivos… com confiança moderada" cobre mal
  um 0,845; prefira *"com confiança que vai da dúvida (0,535) à convicção (0,845)"*.
- **M5** — `03:259`: 0,0013 é 0,13%, e o texto arredonda para "0,1%" na mesma frase em que diz
  "99%" para 0,9922. Padronize a precisão.
- **M6** — `01`: "Boa parte dos pontos está fora delas" — são **38 em 200**, e o número já está na
  saída logo abaixo. Use o número.
- **M7** — `05`: `erros-na-fronteira` devolve a string com aspas (`'21 dos 200 usuários…'`) e
  `separavel(pontos, ys)` devolve um `False` pelado depois de dois parágrafos de construção. Use
  `print()` nos dois; o segundo merece uma frase ("Nenhuma reta separa estes dados.").
- **M8** — `05`: `xs_sep` usa 8 pontos enquanto `fig-margem` usa 10 (caem os dois mais
  distantes). O leitor tenta casar os dois. Uma cláusula resolve: *"os mesmos pontos da figura,
  sem os dois mais afastados"*.
- **M9** — Prosa: "solucionador" (§3 e §5) é tradução dura de *solver* — use "otimizador padrão
  (`lbfgs`)" na §3 e, na §5, "a implementação honesta seria um algoritmo de programação
  quadrática com restrições". "gente com a expertise adequada" → "quem tem o preparo para isso".
  "dominado a classificação **por** uma década" → "durante uma década". "Não é nada mau" → "Nada
  mau, para um conjunto deste tamanho."
- **M10** — `01` tem três `.callout-note`, dois sobre encanamento de render. O do `warning: false`
  já é discutido na §12.3, para onde ele mesmo aponta — o link basta; o callout é decoração.
- **M11** — `05:284`: "obter probabilidades dele exige `probability=True`". No `scikit-learn` 1.9
  instalado, `SVC(probability='deprecated')` avisa: depreciado na 1.9, removido na 1.11, use
  `CalibratedClassifierCV(SVC(), ensemble=False)`. **A ironia da calibração logística sobrevive**
  — e fica até melhor, porque agora o nome da classe diz o que ela faz. Atualize.
- **M12** — `05:265` e `01`(cap. 1)`/03:413` usam o título "Na prática: o que se faz com isso" e
  em seguida **mostram código de biblioteca**. Pelo contrato do guia, essa variante é para quando
  **não há** análogo direto. Renomeie para "Na prática: `scikit-learn`" e "Na prática: `networkx`".

---

## Não mexa nisto

- **`index.qmd` diz "For Further Investigation", e está certo.** O capítulo 16 do Grus usa esse
  título; os outros usam "Exploration". Duas revisões já apontaram isso como inconsistência a
  uniformizar. Não é. O `CLAUDE.md` e o comentário em `scripts/gerar-stubs.py` registram a
  exceção.
- **Os `[-2.11, 4.53, -4.40]` do callout de biblioteca** saem com desvio populacional (`ddof=0`,
  o do `StandardScaler`), não com o `rescale` do próprio livro (que dá `4.546`). É reprodutível e
  está certo para o que o callout mostra — mas se você tocar nesse trecho, saiba disso.
