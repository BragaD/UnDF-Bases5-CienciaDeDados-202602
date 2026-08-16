# Capítulo 14 — Árvores de Decisão: brief de escrita

Corresponde ao **capítulo 17 do Grus**, *Decision Trees*. Seis seções. Os arquivos já existem
como stubs em `content/cap14/`, registrados no `_quarto.yml`. **Não crie nem renomeie arquivo.**

| arquivo | título | seção do Grus |
|---|---|---|
| `01-o-que-e-uma-arvore-de-decisao.qmd` | O que é uma Árvore de Decisão? | *What Is a Decision Tree?* |
| `02-entropia.qmd` | Entropia | *Entropy* |
| `03-a-entropia-de-uma-particao.qmd` | A Entropia de uma Partição | *The Entropy of a Partition* |
| `04-criando-uma-arvore.qmd` | Criando uma Árvore de Decisão | *Creating a Decision Tree* |
| `05-juntando-tudo.qmd` | Juntando Tudo | *Putting It All Together* |
| `06-florestas-aleatorias.qmd` | Florestas Aleatórias | *Random Forests* |

No PDF na raiz: **página do livro impresso = página do PDF − 20.**

---

## O que muda de categoria neste capítulo

Todos os modelos do livro até aqui foram **numéricos**: um vetor de parâmetros ajustado por
gradiente. A árvore não tem parâmetro contínuo, não tem gradiente, não tem taxa de aprendizado
— ela é construída por uma **decisão gulosa repetida**. É a primeira vez que o aluno vê um
modelo que não se ajusta minimizando uma perda diferenciável, e vale dizer isso explicitamente:
o capítulo 5 não ajuda aqui, e não é por falta.

Em compensação, é o primeiro modelo do livro que um humano **lê** — a árvore explica a própria
decisão. Contraste com a regressão logística do capítulo 13, cujos coeficientes dizem pouco
sozinhos, e com o k-vizinhos do capítulo 9, que não explica nada.

## Números já medidos — use estes

Os dados são 14 candidatos a emprego, com `level`, `lang`, `tweets`, `phd` e o alvo `did_well`.

**Entropia (§2):**

- `entropy([1.0])` = **0.0** — certeza total, zero surpresa
- `entropy([0.5, 0.5])` = **1.0** — o máximo para duas classes
- `entropy([0.25, 0.75])` = **0,811278**

**Entropia da partição por atributo (§3), sobre os 14 candidatos** — o **menor** vence e vira
a raiz:

| atributo | entropia da partição |
|---|---|
| `level` | **0,693536** ← escolhido |
| `tweets` | 0,788450 |
| `lang` | 0,860132 |
| `phd` | 0,892159 |

**Entre os 5 candidatos sêniores** (o próximo nível da árvore):

| atributo | entropia da partição |
|---|---|
| `tweets` | **0,000000** ← separação perfeita |
| `lang` | 0,400000 |
| `phd` | 0,950978 |

O zero exato é o melhor momento da seção: particionar os sêniores por `tweets` separa
perfeitamente quem se saiu bem de quem não se saiu. **Diga por que zero significa isso** — cada
lado da partição ficou puro, e não há mais nada a perguntar.

**A árvore construída (§5)** classifica:

- `Candidate("Junior", "Java", tweets=True, phd=False)` → **True**
- `Candidate("Junior", "Java", tweets=True, phd=True)` → **False**
- `Candidate("Intern", "Java", True, True)` → **True** — e este é o caso interessante: `Intern`
  **não aparece nos dados de treino**. A implementação tem um ramo padrão para valor não visto.
  Vale um `callout-warning`: o modelo responde com confiança sobre algo que nunca viu.

## Armadilha: importar o módulo imprime quatro linhas

`scratch/decision_trees.py` tem um `print` **no nível do módulo** (linha 89, dentro de um laço
sobre os atributos). Importá-lo despeja, sem que ninguém peça:

```
level 0.6935361388961919
lang 0.8601317128547441
tweets 0.7884504573082896
phd 0.8921589282623617
```

Se um chunk importar `scratch.decision_trees`, ou use `#| include: false` e mostre os valores
você mesmo formatados, ou reconstrua o que precisa inline. **Não deixe a saída crua vazar** —
ela aparece antes de o texto ter explicado o que é entropia de partição, e com 16 casas
decimais.

O módulo é barato (import em 0,0 s) e não usa `plt` fora de `main()`. Ele expõe no nível do
módulo: `entropy`, `class_probabilities`, `data_entropy`, `partition_entropy`, `partition_by`,
`partition_entropy_by`, `build_tree_id3`, `classify`, `Candidate`, `Leaf`, `Split`,
`DecisionTree`, `inputs`, `senior_inputs`, `tree`, `hiring_tree`.

## Pontos onde é fácil escrever mal

- **§2 (Entropia)** vira fórmula sem intuição por padrão. Entropia aqui é **quanta incerteza
  resta**, medida em bits. Construa a intuição com os três números acima antes de escrever
  −Σ p log p, e diga por que o log é base 2.
- **§4 (Criando)** é onde o algoritmo aparece, e ele é **guloso**: escolhe o melhor atributo
  agora, sem olhar adiante, e nunca revê. Isso não garante a menor árvore possível. Diga.
- **§6 (Florestas Aleatórias)** existe porque uma árvore só **sobreajusta com facilidade** —
  ela pode crescer até isolar cada exemplo. É a resposta direta ao capítulo 8. Duas fontes de
  aleatoriedade: reamostrar os dados (*bootstrap* — que o **capítulo 12, §12.6** acabou de
  ensinar, aponte para lá) e sortear um subconjunto de atributos em cada divisão.

## Ligações

- **[Capítulo 8](../cap08/index.qmd)** — sobreajuste; a §6 é a resposta a ele.
- **[Capítulo 12, §12.6](../cap12/06-digressao-o-bootstrap.qmd)** — o bootstrap que a floresta
  aleatória reaproveita.
- **[Capítulo 9](../cap09/index.qmd)** e **[13](../cap13/index.qmd)** — o contraste de
  interpretabilidade.
- **[Capítulo 5](../cap05/index.qmd)** — para dizer que aqui ele **não** se aplica.
- **[Capítulo 15](../cap15/index.qmd)** (Redes Neurais) é o próximo e ainda é stub.

## Regras da casa (as que mais pegam)

1. Semente explícita em todo chunk com aleatoriedade (a §6 tem), do `random` da stdlib.
2. Sem numpy nem scikit-learn na implementação — só no `.callout-tip collapse="true"`
   intitulado "Na prática: ...", no fim da seção.
3. Nunca invente número de seção do Grus: capítulo + título em itálico.
4. Nunca importe `scratch.getting_data` nem `scratch.working_with_data`.
5. Cada `.qmd` renderiza com kernel próprio — nomes não cruzam de página.
