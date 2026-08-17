# Capítulo 15 — Redes Neurais: correções

A revisão de conteúdo **reproduziu tudo de forma independente** no container e não achou
**nenhum Crítico**: nenhum número, nenhuma derivação e nenhuma legenda estão errados. Ela
conferiu inclusive os quatro callouts de `scikit-learn`, que não executam no render — todos
corretos —, e as três figuras, que descrevem exatamente o que a prosa diz.

**Você não vai reescrever o capítulo.** São dois Importantes (na mesma frase), uma
padronização de vocabulário e cinco Menores.

---

## Importantes — os dois estão em `04-exemplo-fizz-buzz.qmd:238`

A frase contradiz **dois** capítulos vizinhos de uma vez.

### I1 — Ela ensina a implicação falsa que o capítulo 14 gastou uma seção refutando

O texto diz que a árvore do capítulo 14 "acertava 100% do treino **e por isso mesmo** não
dizia nada".

`content/cap14/05-juntando-tudo.qmd:251` diz que **as duas** árvores acertam os oito exemplos
de treino — a enxuta também faz 100%, **e generaliza perfeitamente** (8/8 nas oito
combinações). `cap14:279` localiza a culpa no **número de folhas**, não no acerto em treino.

Acertar tudo no treino não é, por si, sinal de nada. Reescreva sem a implicação — e note que o
capítulo 14 agora tem material ainda mais forte para citar: a árvore `max_depth=2` acerta
**1,0000** no teste, contra 0,8239 da árvore sem poda.

### I2 — "Viés e variância equilibrados", lido de um único treino

A mesma frase chama o resultado de "o retrato que o capítulo 8 chama de modelo com viés e
variância equilibrados". Mas `content/cap08/05-vies-e-variancia.qmd:17` afirma **explicitamente**
que não dá para medir viés e variância olhando um modelo treinado uma vez só, e `cap08/05:167`
alerta contra exatamente essa leitura.

A própria frase já contém a formulação neutra e suficiente — "não há sinal de sobreajuste".
Fique com ela.

---

## Padronização — `epoch`, não `época`

O capítulo 5 estabelece o termo em inglês (`content/cap05/03-usando-o-gradiente.qmd:41`:
"*epoch* é só o nome que damos…"), e os capítulos 5, 11 e 13 usam `epoch` em rótulo de eixo. Os
capítulos 1 a 14 têm hoje **zero** ocorrências de "época".

**O capítulo 15 tem 14**, incluindo `plt.xlabel("época")` em
`04-exemplo-fizz-buzz.qmd:173` e o `fig-cap` "época a época" em `:167`. O livro publicado hoje
diz `epoch` no eixo de quatro capítulos e `época` no eixo deste. Uniformize em `epoch`.

---

## Menores

- **M1** — `03-retropropagacao.qmd:86` × `:93–123`: **colisão de índice na seção mais difícil do
  livro.** A prosa usa $i$ como índice do neurônio **escondido** (seguindo
  `enumerate(hidden_outputs)`), enquanto a caixa de derivação usa $i$ para o de **saída** e $h$
  para o escondido. A ponte em `:123` está certa como objeto, mas ali o `i` do código é o $h$ da
  matemática. Meia linha de nota resolve, e nesta seção vale muito.
- **M2** — `03:222`: "o gradiente que chega ao peso da primeira entrada é, **exemplo a exemplo**,
  o espelho do que chega ao peso da segunda". Exato só no subespaço simétrico ($w_1 = w_2$); com
  inicialização aleatória é aproximado. A frase seguinte já diz "quase igualmente" — basta
  afrouxar o "exemplo a exemplo". (Medido: a diferença vai de 0,086 a 0,0007, então a conclusão
  está certa.)
- **M3** — `04:313`: a linha `(25,) logistic lbfgs` da tabela diz "~0,4 s"; medido **1,8 s**
  (`n_iter_=520`) neste container. As outras três linhas batem.
- **M4** — `04:268`: "a rede **aprendeu** divisibilidade por 3 e por 5" exagera um modelo 96/100
  que erra 70 e 100 — **ambos múltiplos de 5** — e chuta "fizz" em 4 e 34. O callout de `:77–79`
  já preparou a formulação honesta ("terá construído alguma coisa que faz esse papel").
- **M5** — `03:168`: o chunk imprime os pesos iniciais e nenhuma linha de prosa volta a eles. É
  a única saída do capítulo que não é comentada — ou comente, ou use `#| echo: false`.

---

## Não mexa nisto

Tudo o que a revisão verificou e aprovou, que é quase o capítulo inteiro: as saídas do XOR
(`0,009034 · 0,992329 · 0,992328 · 0,007856`), os pesos aprendidos que arredondam para os do
Grus, os 96/100 do Fizz Buzz com erros em 4, 34, 70 e 100, a perda 597,1 → 589,0, a geometria
da §1 (as retas do gráfico **são** as fronteiras reais), a derivação da §3 inteira, o callout
"O fator 2 que sumiu", e os quatro callouts de `scikit-learn`, todos rodados e corretos.
