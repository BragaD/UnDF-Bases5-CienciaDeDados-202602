# Ruptura com o Grus — os capítulos 6 em diante recomeçam

**Data:** 2026-09-10
**Status:** decidido pelo autor; este documento fixa a ruptura e o que fica em aberto
**Supera:** `2026-08-15-estrutura-livro-bases5-design.md` (parcialmente), `2026-09-06-reescrita-numpy-design.md` (por inteiro), `2026-09-08-pandas-nos-dados-design.md` (por inteiro)

## A decisão

O autor pediu, textualmente:

> *"na prática, essa abordagem do livro do Joel Grus não está sendo interessante para as aulas. até agora foram abordados os capítulos até o 5 e há pouco engajamento dos alunos. vou mudar a abordagem e partir para um ensino mais tradicional de machine learning, tendo outras referências para os próximos capítulos. para isso, primeiro, me ajude a tirar as restrições e informações referentes ao livro do Joel (from scratch, python puro, assumir que os alunos já utilizaram modelos, entre outros) e vamos reescrever os capítulos de 6 em diante, com nada de dependência no livro ou abordagem do Grus. podemos mudar totalmente inclusive a estrutura e programação das aulas."*

A evidência é de sala de aula, não de projeto: cinco aulas dadas, pouco engajamento. O material estava tecnicamente correto e completo — 17 capítulos, 104 arquivos, suíte verde, CI publicando — e isso não é o que estava em questão.

**A partir do capítulo 6, nada é herdado do Grus:** nem o escopo, nem a numeração, nem a sequência dos assuntos, nem a tese pedagógica, nem os exemplos, nem a narrativa da DataSciencester, nem o pacote `scratch/`. O material novo nasce de outras referências, ainda a escolher, e de um ensino tradicional de machine learning.

## O que morre

Três decisões que governaram o livro inteiro e deixam de valer do capítulo 6 em diante:

- **"Todo algoritmo é construído do zero, em Python puro."** Era a tese da spec de 2026-08-15. Deixa de ser promessa do material.
- **"Numpy é a calculadora, não o modelo."** Era a tese da spec de 2026-09-06, que já tinha invertido a anterior para os capítulos 6 a 17. Morre com os capítulos que governava.
- **"`pandas` é a mesa de trabalho, com uma fronteira `.to_numpy()` explícita."** Era a spec de 2026-09-08, com fundação e três capítulos convertidos. Morre pelo mesmo motivo.

Morrem junto:

- **A identidade "abrir as caixas-pretas que o aluno usou antes."** Ela assume que o aluno já chamou um `.fit()` e ficou com a curiosidade — premissa que a turma não confirmou. O material novo não pode se apoiar nela, nem em nenhuma variação de *"você provavelmente já treinou um modelo chamando uma função pronta"*.
- **O `scikit-learn` só em callout que não executa.** A restrição existia para proteger a tese "from scratch". Sem a tese, ela não tem razão de ser — mas o que entra no lugar ainda não está decidido (ver "O que fica em aberto").
- **A regra de citação do Grus** (capítulo + título em itálico, nunca número de seção) e o teste que exigia uma citação ao Grus em toda seção.
- **A tabela de correspondência "nosso capítulo ↔ capítulo do Grus"** e, com ela, a numeração de 17 capítulos.

## O que sobrevive

A infraestrutura, que não tem nada a ver com o Grus e custou caro a acertar. **Continua valendo, sem revisão**, a parte da spec de 2026-08-15 que trata de:

- Quarto book em português, um diretório por capítulo, um `.qmd` por seção, todo arquivo registrado no `_quarto.yml`.
- Container Docker com Quarto e `uv`, `uv.lock` travado, teto de versão em toda dependência.
- CI de cinco jobs publicando em `gh-pages`, incluindo o job `offline`.
- **Nenhum byte vem da rede em tempo de render.** Os dados entram commitados em `dados/`, com caminhos a partir da raiz.
- **Semente explícita em todo chunk estocástico.**
- Os notebooks de aula derivados dos `.qmd` (`scripts/gerar-notebooks.py`), o link para o Colab e a célula de preparo que clona o repositório.
- `apoio/` — as páginas interativas de aula, servidas como recurso do projeto.
- `atividades/` — provas e listas fora do projeto-livro.
- A suíte de invariantes como guarda contra falha silenciosa.

Sobrevivem também, por serem dos capítulos 1 a 5: o pacote `scratch/` vendorizado com hash travado, e as páginas de `apoio/` do capítulo 5.

## Os capítulos 1 a 5

**Ficam intocados por ora.** A turma já cursou por eles, e mexer no material que os alunos têm anotado não tem ganho agora.

Mas eles seguem carregando as marcas do Grus — os callouts *"corresponde a X, do capítulo N de @grus2019"*, a narrativa da DataSciencester no capítulo 1, o `Vector = List[float]` do capítulo 4 — e por isso **entram numa rodada posterior de reescrita**, junto com as fontes novas. O que eles viram então (revisão de pré-requisitos, fundamentos de Python e ferramental, ou nada) é decisão de outra spec.

Enquanto isso, o `references.bib` mantém `@grus2019` e a página inicial o lista entre as referências, porque os capítulos 1 a 5 realmente o citam. O que a página inicial deixa de dizer é que ele é *o livro-texto da disciplina*.

## Os capítulos 6 a 17 saem do site agora

Ruptura limpa: **nenhum dos doze fica publicado**, nem os capítulos 6, 7 e 8, que eram os menos dependentes do Grus e os únicos já convertidos para `pandas`. Metade da abordagem antiga no ar seria pior que nenhuma — o site passaria a ensinar duas coisas incompatíveis sem poder explicar por quê (ver "O site não comenta a própria escrita").

Consequência assumida: **a aula de 23/09 e as seguintes ficam sem material publicado** até o capítulo novo existir, e o cronograma da página inicial fica "a definir" da aula 6 em diante.

### Para onde vão

`arquivo/grus/`, na raiz, versionado, com um `README.md` na porta dizendo que aquilo é material morto e não é fonte para nada. Entra no `.quartoignore`, para o Quarto não tratar os `.qmd` como entrada.

Mudam de lugar:

| O quê | Por quê |
|---|---|
| `content/cap06/` a `content/cap17/` | os doze capítulos que saem |
| `notebooks/cap06-*.ipynb` a `cap17-*.ipynb` | derivados desses capítulos |
| `scratch_np/` | existia só para os capítulos 6 a 17 |
| `docs/superpowers/plans/2026-09-06-numpy-*.md` | planos da reescrita que morreu |
| `docs/superpowers/plans/2026-09-08-pandas-*.md` | idem |

**Ficam onde estão**, de propósito:

- **`dados/`**, com os seis conjuntos commitados. O material novo quase certamente usa iris e MNIST; remover para reintroduzir em duas semanas é trabalho jogado fora. A proveniência continua documentada em `dados/README.md`.
- **`numpy`, `pandas` e `scikit-learn` no `pyproject.toml`**, pelo mesmo motivo. Desdeclarar exigiria `make lock` e `make build` agora, e outro par em seguida.
- **`scratch/`**, que os capítulos 1 a 5 usam.

## O site não comenta a própria escrita

Regra editorial, fixada a pedido do autor:

> *"comentários sobre esse tipo de alteração não devem ser incluídos no conteúdo do site. O conteúdo do site é sobre ciência de dados, não sobre decisões do autor ou modificações ao escrevê-lo."*

Nenhum `.qmd` de `content/` diz que houve mudança de abordagem, que um capítulo foi reescrito, que a versão anterior fazia de outro jeito, ou que o material "agora" usa tal ferramenta. O aluno lê ciência de dados; a história editorial vive aqui, nos `docs/`, e no CLAUDE.md.

Isso vale para a transição e para sempre — é a mesma disciplina que já tirou do livro a explicação de Shift+Enter (que foi parar no onboarding do Colab): **texto sobre a ferramenta ou sobre o processo não é texto sobre o conteúdo.**

Um teste guarda isso: `test_o_conteudo_nao_comenta_a_propria_escrita`, em `tests/test_estrutura.py`, varre `content/**/*.qmd` procurando uma lista curta de marcas de meta-comentário editorial. A lista é concreta e revisável — falso positivo se corrige editando a lista com o motivo escrito, não silenciando o teste.

## As consequências na suíte de testes

A suíte é o que impede uma transição desta de deixar buraco silencioso, então nenhum teste some sem decisão registrada.

| Teste | Destino |
|---|---|
| `test_toda_secao_cita_o_grus` | **removido** — era a âncora ao livro-texto que deixou de existir |
| `test_livro_completo_87_secoes_104_arquivos` | vira **21 seções / 26 arquivos**; renomeado |
| `test_dezessete_capitulos`, `test_cada_capitulo_tem_index` | passam a esperar 5 capítulos |
| `test_um_notebook_por_capitulo` | passa a esperar 5 |
| `tests/test_scratch_np.py` | **removido** com `scratch_np/` |
| `tests/test_pandas.py` | **removido** — governava a spec de 2026-09-08 |
| `test_nenhuma_secao_inventa_numero_de_secao_do_grus` | **fica** — os capítulos 1 a 5 ainda citam o Grus |
| `tests/test_scratch.py`, incluindo o hash SHA-256 | **fica** — os capítulos 1 a 5 são Python puro sobre `scratch/`; só mudam os motivos escritos em `NAO_IMPORTAVEIS`, que hoje apontam para os capítulos 6 e 7 |
| `test_gradiente.py`, `test_dados.py`, `test_freeze.py`, `test_atividades.py` | intactos |

O `LIVRO` de `scripts/gerar-stubs.py` — a fonte da verdade sobre o que o livro deve conter — encolhe para os cinco capítulos, e perde a coluna do capítulo correspondente no Grus.

## O que fica em aberto, de propósito

Esta spec **não** decide o material novo. Ela limpa o terreno e registra a ruptura. Ficam para a spec seguinte, depois de escolhidas as referências:

- **As fontes.** O autor pediu explicitamente para buscá-las num próximo momento.
- **A postura sobre implementar algoritmo à mão.** Se o `scikit-learn` passa a ser a ferramenta de ponta a ponta, ou se um ou dois algoritmos ganham versão curta à mão onde ver o mecanismo é a lição do dia — e qual é o critério. Enquanto não houver decisão, **nenhum capítulo novo é escrito**: escrever antes de decidir isso é o que produziria um terceiro estilo para depois desfazer.
- **O escopo, a numeração e a divisão em capítulos e seções.**
- **O cronograma das aulas 6 em diante**, e o que muda na avaliação (a prova cobre "os algoritmos construídos ao longo do semestre" — frase que precisa ser reescrita quando o conteúdo novo existir).
- **A reescrita dos capítulos 1 a 5.**

## Ordem de execução

1. Esta spec, commitada.
2. `arquivo/grus/` criado; os doze capítulos, os notebooks, `scratch_np/` e os planos movidos; `_quarto.yml` termina no capítulo 5; `.quartoignore` ganha `arquivo/`.
3. Testes e `scripts/gerar-stubs.py` ajustados; `test_o_conteudo_nao_comenta_a_propria_escrita` criado.
4. `index.qmd` da raiz e `README.md` limpos das promessas globais.
5. `CLAUDE.md` reescrito.
6. `make teste` verde e um render completo.
