# Listas computacionais no Colab — a avaliação da disciplina muda

**Data:** 2026-09-13
**Status:** decidido pelo autor
**Altera:** a avaliação fixada em `index.qmd` e no PID

## A decisão

**Não haverá mais prova.** No lugar dela e da lista 2, entram **cinco listas
computacionais**, feitas no Google Colab. A lista 1 — revisão de pré-requisitos,
manuscrita — já foi enviada e permanece como está.

O caminho do aluno, fixado: abre o notebook no Colab pelo link do repositório,
salva uma cópia no próprio Drive, preenche as células de resposta, **executa
tudo**, exporta em PDF e posta no AVA/Moodle.

### Os pesos

| Instrumento | Peso |
|---|:--:|
| Lista 1 — revisão de pré-requisitos (manuscrita, já enviada) | 10% |
| Listas computacionais 1 a 5 | 10% cada, 50% |
| Seminário em grupo | 40% |

## O que a lista é, como arquivo

A fonte é **`atividades/lista-comp-01.qmd`**, no mesmo formato de
`atividades/lista-01-revisao.qmd`. O notebook do aluno é **derivado** dela.

O gerador é um script novo e fino, **`scripts/gerar-lista.py`**, que **importa o
parser de `scripts/gerar-notebooks.py`** em vez de duplicá-lo — o mesmo padrão
que `scripts/gerar-stubs.py` já usa para pegar `apelido` de lá. Duas razões para
não estender o gerador de capítulos: ele varre `content/cap*/` e é contado pelos
testes de total do livro, e uma lista não é capítulo.

O que vem de graça nessa reutilização: prosa vira célula de texto, chunk vira
célula de código, callout vira blockquote, link relativo vira URL do site, e —
o que mais importa aqui — a **célula de preparo que clona o repositório quando o
Colab não encontra o projeto**, que é o que põe `dados/` ao alcance do aluno.

**Não há gabarito** — decisão do autor. Por isso a maquinaria de dupla
renderização de `scripts/render-atividade.sh` (o filtro de `content-visible`,
usado pela lista 1) **não entra aqui**.

**Não há PDF do enunciado.** O notebook é o enunciado, e um PDF ao lado
duplicaria a fonte. O cronograma do site aponta para o link do Colab, como já
faz com os notebooks de aula.

A relação é a mesma do resto do repositório: **o `.qmd` é a fonte, o `.ipynb` é
cópia derivada.** Editar o `.ipynb` é trabalho perdido.

## Os oito exercícios da lista 1

Numerados **1 a 8**, cada um com uma linha dizendo qual exercício do ISLP ele
adapta. A numeração do livro não é usada como nossa: "exercício 2.2" confundiria,
porque aqui o capítulo é o 7.

| Nº | Origem | Tipo | Cobre |
|---|---|---|---|
| 1 | ISLP 2.2 | conceitual | 7.2, 7.5 |
| 2 | ISLP 2.6 | conceitual | 7.3 |
| 3 | ISLP 2.8 | código | 6 |
| 4 | ISLP 2.9 | código | 6, 7 |
| 5 | ISLP 3.3 | conceitual | 8.4, 8.5 |
| 6 | ISLP 3.4 | conceitual | 8.5, 8.7 |
| 7 | ISLP 3.8 | código | 8.1, 8.2, 8.6 |
| 8 | ISLP 3.9 | código | 8.3, 8.5, 8.6 |

### A regra de adaptação

**Mantém-se o máximo possível do enunciado original.** Só duas coisas mudam, e
as duas por decisão de escopo já tomada:

1. **A ferramenta.** Onde o ISLP pede `sm.OLS()` e `summarize()`, a lista pede
   `LinearRegression`. `statsmodels` e o pacote `ISLP` são proibidos nesta
   disciplina, e o aluno nunca os viu.
2. **Os itens de inferência saem.** Todo sub-item que peça valor-p, estatística
   *t*, estatística *F*, erro-padrão de coeficiente, intervalo de confiança ou a
   palavra "estatisticamente significativo" é **removido**, não reescrito. A
   seção 3.1.2 do ISLP está fora da ementa inteira.

O que sobra dos exercícios 7 e 8 continua substancial: a força da relação vira
**R² e RSE**; a direção vira o **sinal do coeficiente**; o diagnóstico de
resíduo contra previsto e de alavancagem fica inteiro; e o item de termo não
linear do 3.9 também.

**A lista não comenta essa adaptação para o aluno.** A mesma regra editorial do
site vale aqui: o enunciado é sobre ciência de dados, não sobre o que o
professor decidiu cortar. A linha de correspondência diz de onde o exercício
vem, e nada mais.

## O que o aluno preenche

- **Uma primeira célula** pede nome e matrícula.
- **Cada exercício traz a sua célula de resposta logo abaixo do enunciado.**
  Conceitual: uma célula de texto. De código: uma célula de código **e** uma de
  texto, porque todo enunciado de código desta lista pede interpretação junto da
  conta.
- **A célula de resposta é reconhecível por marca literal**, e é isso que torna o
  teste possível. Na fonte e no notebook, uma célula de código de resposta começa
  com a linha `# sua resposta` e nada mais; uma célula de texto de resposta contém
  só a linha `*sua resposta aqui*`. A marca é o contrato entre o enunciado, o
  aluno e a suíte.
- **Duas instruções que a lista precisa dar**, porque o caminho até o PDF tem
  armadilha: *executar tudo antes de exportar* (`Ambiente de execução → Executar
  tudo`), senão o PDF sai sem as saídas; e conferir se alguma saída larga ficou
  cortada na impressão.

## Os dados

**`College.csv` entra em `dados/`** — 777 linhas, 19 colunas —, baixado uma vez
por `scripts/baixar-dados.py` e commitado, com a proveniência e a tabela de-para
em `dados/README.md`, no molde de `Credit` e `Auto`.

**A coluna de índice do R é PRESERVADA neste conjunto, e isso é exceção.** Nos
demais CSV do ISLP ela foi removida na tradução. Aqui ela fica, com o nome
`Unnamed: 0` que o `pandas` gera, porque **o item (b) do exercício é sobre ela**:
o aluno é levado a descobrir que a primeira coluna é o nome da universidade, a
relê-la com `index_col=0`, e a entender a diferença. Remover a coluna apagaria o
exercício.

O de-para dos 18 nomes restantes:

| Original | Traduzida |
|---|---|
| `Private` | `privada` (`Yes`/`No` → `sim`/`não`) |
| `Apps` | `inscricoes` |
| `Accept` | `aceitos` |
| `Enroll` | `matriculados` |
| `Top10perc` | `perc_top10` |
| `Top25perc` | `perc_top25` |
| `F.Undergrad` | `graduacao_integral` |
| `P.Undergrad` | `graduacao_parcial` |
| `Outstate` | `mensalidade_fora_do_estado` |
| `Room.Board` | `moradia_e_alimentacao` |
| `Books` | `custo_livros` |
| `Personal` | `gastos_pessoais` |
| `PhD` | `perc_doutores` |
| `Terminal` | `perc_titulacao_maxima` |
| `S.F.Ratio` | `razao_aluno_professor` |
| `perc.alumni` | `perc_ex_alunos_doadores` |
| `Expend` | `gasto_por_aluno` |
| `Grad.Rate` | `taxa_conclusao` |

**Por que traduzir:** no mesmo notebook o aluno usa o `Auto` com `potencia` e
`milhas_por_galao`. Deixar o `College` em inglês criaria duas convenções na
mesma página. A consistência dentro do notebook vale mais que a fidelidade aos
nomes de variável do livro.

`Auto.csv` já está em `dados/`, traduzido, com os cinco `?` de `potencia`
preservados e guardados por teste.

## O que muda no site

`index.qmd` perde a prova. A tabela de avaliação passa a ter os quatro
instrumentos da seção "Os pesos". O texto que diz que "as duas listas são
entregues manuscritas" passa a valer **só para a lista 1** — as computacionais
são entregues em PDF pelo Moodle.

O cronograma perde "revisão para a prova" (aula 16), "Prova" (aula 17) e
"Revisão da prova" (aula 19). **As três aulas ficam livres, e o que entra nelas
é decisão de outro momento** — esta spec não a toma.

### As datas de entrega

A lista 1 cobre os capítulos 6, 7 e 8, dados nas aulas 5, 6 e 7 (16/09, 23/09 e
30/09). **Entrega até 21/10 (aula 10)** — três semanas depois do capítulo 8, e
depois do HPE de 14/10, para não competir com o trabalho dos grupos.

O formato das demais, derivado da ementa: cada lista cobre os capítulos dados
desde a anterior, com entrega a cada duas aulas — listas 2 a 5 fechando em
04/11, 18/11, 02/12 e 09/12, esta última na data que era da prova. **Só a data
da lista 1 é fixada aqui**; as demais se confirmam quando cada lista for
escrita, porque dependem dos capítulos existirem.

## Testes

A suíte ganha o que o padrão da casa já cobra dos outros derivados:

- **`College.csv` documentado em `dados/README.md`** — `test_dados_README_documenta_cada_conjunto` já cobra isso sozinho quando o arquivo entra em `ESPERADOS`.
- **Os nomes antigos de coluna do `College`** entram em `NOMES_ANTIGOS_DE_COLUNA`, com a mesma exclusão de palavras genéricas demais que a lista já pratica. **`Private`, `Apps`, `Accept`, `Enroll`, `Outstate`, `Expend` entram; `Books`, `Personal`, `Terminal` e `PhD` ficam de fora** por serem palavras que aparecem em prosa corrente ou em contexto sem relação.
- **`College.csv` preserva a coluna de índice** — teste próprio, no molde de
  `test_auto_preserva_a_armadilha_da_potencia`, com o motivo escrito: o item (b)
  do exercício 3 da lista depende dela.
- **O notebook da lista não pode defasar da fonte** — **teste irmão** de
  `test_notebooks_estao_atualizados`, em `tests/test_atividades.py`, regerando a
  lista em memória e comparando com o arquivo em disco. Irmão, e não a mesma
  varredura: a atual está presa a `content/` e alimenta os testes de total do
  livro, que uma lista falsearia.
- **Nenhuma célula de resposta vem preenchida** — teste que varre o `.ipynb` da
  lista e falha se uma célula marcada com `# sua resposta` ou `*sua resposta
  aqui*` tiver qualquer outra coisa dentro. É o guarda contra o acidente de
  commitar o notebook depois de tê-lo executado para conferir.
- **Nenhuma célula da lista guarda saída de execução** — o mesmo invariante que
  `test_nenhum_notebook_guarda_saida` cobra dos notebooks de aula, pelo mesmo
  motivo, e mais um: uma saída commitada entregaria resposta.

## O que fica de fora, de propósito

- **O gabarito.** Decisão do autor; a correção é individual e a discussão
  acontece em aula.
- **As listas 2 a 5.** Esta spec fixa o formato e a infraestrutura; o conteúdo de
  cada uma sai quando os capítulos dela existirem.
- **O conteúdo das três aulas liberadas** pela saída da prova.
- **A atualização do PID** (`atividades/PID - ...xlsx`), que é documento
  institucional e não se edita por script.
