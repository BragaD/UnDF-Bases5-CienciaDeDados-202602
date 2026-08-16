# Capítulo 12 — Regressão Múltipla: brief de escrita

Corresponde ao **capítulo 15 do Grus**, *Multiple Regression*. Oito seções — o maior capítulo
do livro até aqui. Os arquivos já existem como stubs em `content/cap12/`, registrados no
`_quarto.yml`. **Não crie nem renomeie arquivo nenhum.**

| arquivo | título | seção do Grus |
|---|---|---|
| `01-o-modelo.qmd` | O Modelo | *The Model* |
| `02-hipoteses-do-minimos-quadrados.qmd` | Outras Hipóteses do Modelo de Mínimos Quadrados | *Further Assumptions of the Least Squares Model* |
| `03-ajustando-o-modelo.qmd` | Ajustando o Modelo | *Fitting the Model* |
| `04-interpretando-o-modelo.qmd` | Interpretando o Modelo | *Interpreting the Model* |
| `05-qualidade-do-ajuste.qmd` | Qualidade do Ajuste | *Goodness of Fit* |
| `06-digressao-o-bootstrap.qmd` | Digressão: O Bootstrap | *Digression: The Bootstrap* |
| `07-erros-padrao-dos-coeficientes.qmd` | Erros Padrão dos Coeficientes | *Standard Errors of Regression Coefficients* |
| `08-regularizacao.qmd` | Regularização | *Regularization* |

No PDF na raiz do repositório: **página do livro impresso = página do PDF − 20.** O capítulo 14
do Grus (nosso 11) ocupou as páginas 199–204 do PDF. O capítulo 15 começa logo depois;
confirme abrindo o PDF antes de escrever.

---

## A espinha narrativa — escreva o capítulo em torno dela

Este capítulo tem o melhor arco do livro, e ele é fácil de perder escrevendo oito seções como
oito tópicos independentes. **O arco é este:**

> Ajustamos o modelo → interpretamos os coeficientes → descobrimos que o R² **mente**, porque
> ele sempre sobe quando se acrescenta variável → o bootstrap nos dá incerteza sem teoria
> nenhuma → os erros padrão daí dizem quais coeficientes são reais e quais são ruído → a
> regularização encolhe os que não se sustentam.

Cada seção deve **puxar** a seguinte. A 5 termina com um problema; a 6 traz a ferramenta; a 7 a
aplica; a 8 resolve. Se o aluno chegar na 8 sem sentir que ela responde a uma pergunta feita na
5, o capítulo falhou, mesmo que cada seção esteja correta isoladamente.

**A 5 é o coração.** R² sempre aumenta ao acrescentar variável — inclusive variável aleatória
sem relação nenhuma com o alvo. Isso é uma armadilha concreta, e vale **demonstrar rodando**:
acrescente uma coluna de `random.random()` ao modelo e mostre o R² subir. É o tipo de material
que o guia chama de melhor do livro.

---

## Números já medidos — use estes, não os da memória

O dado é o mesmo do capítulo 11, agora com mais variáveis. `scratch.multiple_regression`
importa em 1,2 s e expõe `inputs` no nível do módulo:

- `inputs`: 203 pontos, 4 valores cada — `[1.0, num_friends, work_hours, phd]`. O primeiro é a
  constante. Exemplo: `[1.0, 49, 4, 0]`.
- `least_squares_fit(inputs, daily_minutes_good, 0.001, 5000, 25)` com `random.seed(0)` dá
  **`beta = [30.5148, 0.9748, -1.8507, 0.9141]`**
- **R² = 0,679985**
- Um ajuste custa **0,9 s**. O bootstrap de 100 amostras do Grus custa **~90 s** de render —
  perfeitamente pagável. **Não reduza o número de amostras**; faça a coisa real.

**Atenção:** o Grus imprime `30.58, 0.972, -1.865, 0.923` nos `assert` de `p_value` do módulo.
Nossos valores diferem no terceiro dígito. **Use os que saírem da sua execução**, não os do
livro impresso — e se a diferença for visível no texto, ela não precisa de explicação
elaborada: gradiente descendente estocástico com semente própria não reproduz dígito a dígito
o que o autor imprimiu.

---

## Armadilhas concretas deste capítulo

1. **`least_squares_fit` chama `tqdm.trange` por dentro.** Todo chunk que a chamar precisa de
   `#| warning: false`, senão a barra de progresso despeja dezenas de linhas de lixo no livro.
   Isto já está resolvido nos capítulos 7 e 9 — **e o [Capítulo 7](../cap07/07-um-parenteses-tqdm.qmd)
   é literalmente a seção que ensina `tqdm`.** Aponte para lá; é uma ponte de graça, e é a
   primeira vez que o aluno vê a ferramenta que aprendeu sendo usada por dentro de outra coisa.
2. **Cada `.qmd` renderiza com um kernel próprio.** Nomes definidos numa seção **não existem**
   na outra. Importe de `scratch.multiple_regression` (com um callout explicando que é o mesmo
   código) ou redefina.
3. **Todo chunk com aleatoriedade leva `random.seed(N)` explícito**, do `random` da stdlib.
   Sem isso os números mudam a cada render e o texto para de bater com a saída.
4. **Nunca importe** `scratch.getting_data` (faz `requests.get` no nível do módulo) nem
   `scratch.working_with_data` (abre `stocks.csv` relativo ao cwd, e afirma sobre correlação
   sem semente).
5. `scratch.statistics` chama `plt.*` no nível do módulo — se importar, use `#| include: false`
   e `plt.close('all')` na sequência.
6. **Não invente número de seção do Grus.** Ele não numera seções: cite capítulo + título em
   itálico. A nossa numeração (`12.3`) é legítima.

---

## Pontos onde é fácil escrever mal

- **§2 (Outras Hipóteses)** vira lista chata por padrão. As hipóteses só significam algo se o
  texto disser **o que quebra quando cada uma é violada**. Colunas linearmente dependentes: o
  ajuste não é único. Variável explicativa correlacionada com o erro: o coeficiente absorve o
  que não é dele. Torne concreto.
- **§4 (Interpretando)** contém a frase mais perigosa da estatística aplicada: *"mantendo todo
  o resto constante"*. O coeficiente de `num_friends` não é o efeito de ter mais um amigo — é o
  efeito de ter mais um amigo **entre pessoas com as mesmas horas de trabalho e o mesmo
  doutorado**. E se duas variáveis andam juntas no dado, "manter o resto constante" descreve
  uma situação que **nunca aparece nos dados**. O capítulo 11 já avisou sobre causalidade;
  este é o aprofundamento.
- **§6 (O Bootstrap)** é uma digressão, e a tentação é tratá-la como intervalo. É a ideia mais
  reaproveitável do capítulo: **medir incerteza reamostrando o próprio dado, sem teoria
  nenhuma**. O Grus dá o exemplo perfeito — 101 pontos colados em 100 versus 101 pontos
  metade perto de 0 e metade perto de 200, ambos com **mediana ~100**, e o bootstrap
  distinguindo os dois casos (desvio < 1 contra > 90). Esses dois números estão nos `assert`
  do módulo, linhas 103–104. Rode e mostre.
- **§8 (Regularização)** precisa fechar o arco. Diga por que encolher coeficientes ataca
  exatamente o problema levantado na 5, e por que o termo constante normalmente **não** é
  penalizado.

---

## Ligações que o livro já deixou prontas

- **[Capítulo 11](../cap11/index.qmd)** é o pai direto: mesmo dado, mesma suposição de erros
  normais, uma variável explicativa virando várias. O capítulo 11 diz que lá "a álgebra ainda
  fecha, mas fica pesada" — **a regressão múltipla tem, sim, fórmula fechada** (a equação
  normal, β = (XᵀX)⁻¹Xᵀy). Não escreva a fórmula matricial (o livro não construiu inversão de
  matriz), mas **não afirme que ela não existe**.
- **[Capítulo 5](../cap05/index.qmd)** deu o `gradient_step` e o minibatch que ajustam isto.
- **[Capítulo 8](../cap08/index.qmd)** deu o vocabulário de sobreajuste — a 8 (regularização) é
  a resposta direta ao que aquele capítulo diagnosticou.
- **[Capítulo 7](../cap07/07-um-parenteses-tqdm.qmd)** ensinou `tqdm` (armadilha 1).
- **[Capítulo 13](../cap13/index.qmd)** (Regressão Logística) é o próximo e ainda é stub —
  aponte para frente sem prometer detalhe que você não pode conferir.
