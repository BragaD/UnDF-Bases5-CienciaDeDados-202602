# Capítulo 15 — Redes Neurais: terceira rodada, um item só

**Esta rodada existe porque o corretor da rodada 2 fez a coisa certa: obedeceu ao contrato
e reportou que o contrato estava errado.**

O item I7 da rodada anterior mandou cortar a afirmação de que a rede "aproxima a soma alternada
e o ciclo módulo 4", por falta de sustentação — e o corretor cortou, como devia. Depois foi
medir os pesos, e achou que a afirmação **estava** sustentada. Eu verifiquei de forma
independente, e ela está — em parte, e a parte é o que torna a história boa.

---

## O achado, medido duas vezes

**A aritmética primeiro.** Fizz buzz depende de $n \bmod 15$. E $2^k \bmod 15$ é **periódico com
período 4**:

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| $2^k \bmod 15$ | 1 | 2 | 4 | 8 | **1** | **2** | **4** | **8** | **1** | **2** |

Ou seja: para decidir fizz buzz, **os bits 0, 4 e 8 são intercambiáveis** — os três contribuem
com o mesmo resíduo. O mesmo vale para {1, 5, 9}, para {2, 6} e para {3, 7}.

**O que a rede treinada faz com isso.** Medi a distância média entre os pesos de cada par de
bits, nos 25 neurônios escondidos, como fração da escala típica de um peso:

| grupo de bits | resíduo | distância interna |
|---|---|---|
| **{0, 4, 8}** | 1 | **3%** |
| {1, 5, 9} | 2 | 22% |
| {2, 6} | 4 | 95% |
| {3, 7} | 8 | 150% |
| **entre resíduos diferentes** | — | **141%** |

**A rede aprendeu que os bits 0, 4 e 8 são a mesma coisa.** Três por cento contra cento e
quarenta e um: uma diferença de quase cinquenta vezes. Aprendeu **meia** simetria em {1, 5, 9}.
E **não** aprendeu as outras duas.

---

## O que escrever

Uma subseção curta na §4 — `04-exemplo-fizz-buzz.qmd` —, logo depois do bloco que imprime os
dois vetores de pesos escondidos (o item I6 da rodada anterior). O texto atual mostra os
vetores e argumenta que eles não respondem o que o neurônio calcula. **Isto acrescenta o que
eles respondem.**

Três coisas, nesta ordem:

1. **A aritmética**, em duas linhas: fizz buzz depende de $n \bmod 15$, e $2^k \bmod 15$ cicla
   com período 4. Portanto os bits 0, 4 e 8 carregam a mesma informação para esta tarefa.
2. **A medição**, num chunk que roda: a distância média entre os pesos, dentro de cada grupo e
   entre grupos. Os números acima são a referência — **meça de novo**, porque a rede da página é
   a que vale.
3. **A leitura honesta, que é a parte boa.** A rede achou **uma** das quatro simetrias com
   clareza, metade de outra, e perdeu duas. Ninguém lhe contou o que é divisibilidade, e ela
   descobriu sozinha um fato de teoria dos números — **parcialmente**, do jeito irregular como
   essas coisas acontecem de verdade. Não escreva isto como triunfo. O interessante é justamente
   que é incompleto: uma rede que tivesse achado as quatro simetrias seria uma anedota bonita e
   suspeita; esta é o que redes fazem.

**E amarre ao arco de interpretabilidade**, que é o assunto da seção: os pesos continuam
ilegíveis um a um, e ainda assim há estrutura recuperável neles **se você souber que pergunta
fazer**. Isso não é o mesmo que interpretabilidade — é o contrário do que o capítulo 12 oferece,
onde o coeficiente já vem com significado. Aqui foi preciso ter a hipótese antes de encontrar a
evidência.

---

## Limites — não exagere

- **Não** diga que a rede "aprendeu aritmética modular". Ela aprendeu **uma** equivalência entre
  três bits, e não as outras.
- **Não** reintroduza a frase que a rodada 2 cortou sobre "a soma alternada e o ciclo módulo 4"
  como se fosse fato geral. O corretor anterior mediu que o neurônio 7 alterna sinal e que o 16
  é quase periódico — **se você quiser citar isso, meça e cite o neurônio específico**, não a
  camada.
- O `.conceito` que fecha a seção **continua verdadeiro e não deve ser tocado**: nenhuma sigmoide
  sozinha calcula divisibilidade, que não é monótona em soma ponderada.

---

## Verificação

Este item acrescenta chunk com saída. Renderize, e **confira os números publicados** em
`_book/content/cap15/04-exemplo-fizz-buzz.html` (ou no `_freeze`, se outro agente estiver
renderizando e o `_book` estiver sendo reescrito — é o mesmo conteúdo).
