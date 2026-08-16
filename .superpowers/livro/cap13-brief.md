# Capítulo 13 — Regressão Logística: brief de escrita

Corresponde ao **capítulo 16 do Grus**, *Logistic Regression*. Cinco seções. Os arquivos já
existem como stubs em `content/cap13/`, registrados no `_quarto.yml`. **Não crie nem renomeie
arquivo nenhum.**

| arquivo | título | seção do Grus |
|---|---|---|
| `01-o-problema.qmd` | O Problema | *The Problem* |
| `02-a-funcao-logistica.qmd` | A Função Logística | *The Logistic Function* |
| `03-aplicando-o-modelo.qmd` | Aplicando o Modelo | *Applying the Model* |
| `04-qualidade-do-ajuste.qmd` | Qualidade do Ajuste | *Goodness of Fit* |
| `05-maquinas-de-vetores-de-suporte.qmd` | Máquinas de Vetores de Suporte | *Support Vector Machines* |

No PDF na raiz: **página do livro impresso = página do PDF − 20.**

---

## A espinha narrativa

O capítulo 12 acabou de ensinar a ajustar um modelo linear a várias variáveis. **A §1 pega
exatamente essa ferramenta e a aponta para um alvo 0/1** — comprou conta paga ou não — e mostra
por que ela não serve: um modelo linear prevê valores fora de [0, 1], e o coeficiente perde
sentido como probabilidade. A §2 conserta o alcance com a função logística. A §3 ajusta. A §4
avalia com o vocabulário do capítulo 8. A §5 mostra a alternativa geométrica.

**O capítulo 5 deixou uma dívida explícita:** ele diz que a regressão logística **não tem
fórmula fechada** — não há duas médias e uma covariância que resolvam. Aqui o gradiente
descendente deixa de ser uma alternativa ao caminho algébrico e passa a ser **o único caminho**.
Diga isso em voz alta; é a diferença de status entre este capítulo e o 11.

---

## O melhor material do capítulo, já medido

**Sem reescalonar os dados, o ajuste não converge devagar — ele estoura na primeira conta.**

O dado tem `experiência` entre 0,1 e 10 e `salário` entre 30.000 e 107.000: as amplitudes
diferem por um fator de **7.778**. Com `random.seed(0)`, o β inicial é
`[0.844422, 0.757954, 0.420572]`, e no primeiro ponto `x = [1.0, 0.7, 48000]`:

- `dot(x, beta)` = **20.188,81** — dominado inteiramente pelo salário
- `logistic(20188.81)` = **`1.0`**, e a saturação é **exata em float64**: `logistic(x) == 1.0`
  já a partir de **x ≈ 37**
- logo `1 - 1.0` = `0.0`, e `math.log(0)` levanta **`ValueError: math domain error`**

Reescalonado, o mesmo ponto dá `dot = -0,8059` e `logistic = 0,3088` — inofensivo.

Isto é caixa-preta pura: quem chama `LogisticRegression().fit()` nunca vê esse erro, porque a
biblioteca reescalona (ou usa um solver que não se importa). **Mostre o erro acontecendo de
verdade** — capture o `ValueError` e imprima, como o capítulo 10 fez com o `ZeroDivisionError`
da precisão indefinida. Não simule em prosa.

## Armadilha: `rescale` vem de um módulo proibido

O `main()` do Grus faz `from scratch.working_with_data import rescale`. **Esse módulo é um dos
dois que este livro nunca importa** — ele abre `stocks.csv` com caminho relativo ao cwd, no
nível do módulo, e estoura com `FileNotFoundError`.

Escreva `rescale` (e o `scale` de que ela depende) **inline**, e aponte para o
[Capítulo 7, §7.6](../cap07/06-reescalonamento.qmd), que é onde este livro ensinou
reescalonamento e onde a função já aparece — `content/cap07/06-reescalonamento.qmd:86`. É uma
ponte de graça e fecha um arco: lá o aluno aprendeu a técnica em abstrato, aqui ela é a
diferença entre o modelo existir e o programa quebrar.

Lembre que **cada `.qmd` renderiza com um kernel próprio** — nomes não cruzam de página.

## Números do ajuste, medidos e conferidos

Com `random.seed(0)`, `train_test_split(rescaled_xs, ys, 0.33)`, taxa 0,01, 5000 passos:

- **n = 200** (134 de treino, 66 de teste)
- **β reescalado = `[-2.0239, 4.693, -4.4698]`**
- perda final (log-verossimilhança negativa, treino) = **39,9635**
- matriz de confusão no teste: **tp=12, fp=4, fn=3, tn=47**
- **precisão = 0,75** e **revocação = 0,8** — batem exatamente com os `assert` do Grus

O Grus também mostra como **desescalonar** β para unidades interpretáveis, e verifica que a
verossimilhança é idêntica nas duas escalas. É um bom fecho para a §3: o modelo é o mesmo, só
as unidades mudaram.

## Ligações

- **[Capítulo 12](../cap12/index.qmd)** — a §1 usa a ferramenta dele e mostra onde ela falha.
- **[Capítulo 11, §11.3](../cap11/03-maxima-verossimilhanca.qmd)** — introduziu máxima
  verossimilhança. Aqui **maximizar a verossimilhança = minimizar a log-verossimilhança
  negativa**, e é isso que o gradiente descendente faz. A ligação é obrigatória, não decorativa.
- **[Capítulo 8](../cap08/index.qmd)** — precisão e revocação da §4 vêm de lá.
- **[Capítulo 7, §7.6](../cap07/06-reescalonamento.qmd)** — reescalonamento (ver acima).
- **[Capítulo 5](../cap05/index.qmd)** — a dívida da fórmula fechada que não existe.
- **[Capítulo 14](../cap14/index.qmd)** (Árvores de Decisão) é o próximo e ainda é stub.

## Sobre a §5 (Máquinas de Vetores de Suporte)

O Grus **não implementa** SVM — a seção é descritiva, explica a ideia do hiperplano de margem
máxima e o truque do kernel sem código. **Não invente uma implementação**, e não deixe a seção
virar um resumo vago. O que ela precisa entregar: por que separar com margem é um critério
diferente de maximizar verossimilhança, e o que o kernel compra. Esta é a seção certa para a
variante **"Na prática: o que se faz com isso"** do callout de fechamento.

## Regras da casa (as que mais pegam)

1. Semente explícita em todo chunk com aleatoriedade, do `random` da stdlib.
2. Sem numpy nem scikit-learn na implementação — só no callout `.callout-tip collapse="true"`
   intitulado "Na prática: ...", no fim da seção.
3. Nunca invente número de seção do Grus: cite capítulo + título em itálico.
4. Nunca importe `scratch.getting_data` nem `scratch.working_with_data`.
5. `scratch.logistic_regression` **é seguro importar** (1,0 s; `plt` só é usado dentro de
   `main()`), e expõe `xs`, `ys`, `logistic`, `negative_log_likelihood`,
   `negative_log_gradient` no nível do módulo.
6. Se um chunk chamar `least_squares_fit` (§1), ele precisa de `#| warning: false` — a função
   usa `tqdm.trange` por dentro e a barra de progresso vaza para o livro.
