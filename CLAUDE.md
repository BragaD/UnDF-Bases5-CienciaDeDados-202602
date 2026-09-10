# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Estado atual

**A fonte é o ISLP.** James, Witten, Hastie, Tibshirani e Taylor, *An Introduction to Statistical Learning with Applications in Python* (Springer, 2023) — chave `@james2023` em `references.bib`, PDF em `livros/ISLP_website.pdf`. A escolha fecha o que a ruptura com o Grus tinha deixado em aberto: a fonte, a postura pedagógica, o escopo e a numeração.

A decisão está em `docs/superpowers/specs/2026-09-10-estrutura-nova-islp-design.md`. **Leia essa spec antes de mexer em qualquer coisa de conteúdo.** Ela é a fonte — a tese, a ementa capítulo a capítulo com a correspondência ISLP, o que fica de fora e por quê, e a ordem de execução; este arquivo é o resumo operacional.

O que existe hoje:

- **Seis capítulos**, 27 seções + 6 `index.qmd` = **33 `.qmd`**, todos registrados em `_quarto.yml`. Os capítulos 1 a 5 (Introdução, Um Curso Rápido de Python, Visualizando Dados, Álgebra Linear, Gradiente Descendente) são da abordagem anterior — ver "Os capítulos 1 a 5", abaixo. O **capítulo 6 — Dados: Tipos, Dados Retangulares e `pandas`** é o primeiro escrito sob a spec do ISLP: não corresponde a nenhuma seção do livro-fonte, e **é o modelo de estilo da casa**, o papel que o capítulo 9 tinha na abordagem do Grus.
- **`arquivo/grus/`** — os capítulos 6 a 17 como estavam na abordagem do Grus, os notebooks derivados deles, o pacote `scratch_np/` e os planos das reescritas que morreram. Está no `.quartoignore`, fora da suíte, e **não é fonte para nada**.
- Container Docker (Quarto + `uv`), CI publicando em `gh-pages`, **48 testes** (`make teste`) guardando os invariantes.
- `notebooks/` com um `.ipynb` por capítulo (seis, hoje) para a aula, `atividades/` com o PID e as listas, `apoio/` com páginas HTML interativas para projetar em aula.

### Antes de escrever um capítulo

**Leia `content/cap06/` inteiro primeiro.** Foi o primeiro capítulo escrito sob a spec do ISLP, e fixa a forma: abertura de seção sem "nesta seção veremos", o chunk de setup aplicando `estilo-figuras.mplstyle`, a posição dos callouts `::: {.conceito}` e `::: {.exemplo}`. Um capítulo novo que copiar essa forma economiza rodadas de revisão; um que reinventar a forma provavelmente repete um erro que o cap. 6 já pagou.

**Todo número afirmado na prosa sai da saída de um chunk.** Duas exceções, e só duas:

1. **Aritmética sobre números impressos na mesma seção** — uma diferença, uma soma, uma razão, ou o arredondamento de uma delas. A prosa precisa **nomear os dois operandos**, para o leitor refazer a conta na página. Número de outra seção não vale: o kernel é outro e o leitor não tem os dois à vista.
2. Nada mais.

**Superlativo e comparação NÃO são aritmética.** "o maior", "a maior distância", "mais que o dobro", "o mais barato", "nenhum passa de" são afirmações sobre a **tabela inteira**, e é aí que quem escreve chuta com aparência de ter conferido. Um superlativo exige o chunk que ordena, conta ou compara — mesmo quando a tabela está impressa logo acima.

A cicatriz: a seção 6.5 afirmou que São Paulo tinha a maior distância entre média e mediana; era Belo Horizonte, e a tabela que desmentia estava impressa no chunk acima.

### O que falta

Onze capítulos, na ementa que a spec fixa:

| Capítulo | Título | ISLP |
|---|---|---|
| 7 | O que é aprendizado estatístico | 2 |
| 8 | Regressão linear | 3 |
| 9 | Classificação | 4 |
| 10 | Reamostragem | 5 |
| 11 | Seleção de modelos e regularização | 6 |
| 12 | Árvores de decisão | 8.1 |
| 13 | Bagging, florestas e boosting | 8.2 |
| 14 | Redes neurais | 10 (recorte denso — sem `torch`) |
| 15 | Aprendizado não supervisionado | 12 |
| 16 | Máquinas de vetores de suporte | 9 |
| 17 | Um problema do começo ao fim | — (sem ISLP; a leitura do seminário/HPE) |

Cada um ganha o seu próprio plano em `docs/superpowers/plans/2026-09-10-islp-capNN.md`, escrito quando chegar a vez — **um capítulo por vez**, sequencial, no processo que as reescritas anteriores fixaram: planejador com o mapa do capítulo no prompt, implementador, revisor que lê o capítulo inteiro com uma pergunta só (*o texto condiz com o que foi escrito?*), implementador corrigindo. O capítulo 17 sai de ordem, logo após o 9, porque tem prazo (o HPE de 14/10); o resto segue a ordem do livro. A ementa seção a seção está na spec.

### Os capítulos 1 a 5

São da abordagem anterior: citam o Grus, não o ISLP, e ficam **fora dos guardas novos** de propósito — `test_nenhum_chunk_executavel_usa_biblioteca_proibida`, `test_toda_secao_tem_figura` e `test_todo_chunk_que_desenha_aplica_o_estilo` (em `tests/test_estrutura.py`) só varrem `CAPITULOS_NOVOS`, isto é, `cap06` a `cap17`. `test_toda_secao_cita_o_islp` entra com o capítulo 7 e vale a mesma exclusão. A reescrita deles é decisão em aberto, registrada como tal na spec — não é tarefa deste plano.

### As specs, e o que sobrou de cada uma

| Spec | Estado |
|---|---|
| `2026-09-10-estrutura-nova-islp-design.md` | **vigente** — a fonte, a tese, a ementa e a ordem de execução |
| `2026-09-10-ruptura-com-o-grus-design.md` | **histórico** — fechou a abordagem do Grus e abriu as três perguntas (fonte, postura, escopo) que a spec do ISLP responde |
| `2026-08-15-estrutura-livro-bases5-design.md` | **vale só a infraestrutura**: Quarto, Docker, `uv`, CI, dados commitados, sementes, notebooks, `apoio/`, `atividades/`, a suíte |
| `2026-09-06-reescrita-numpy-design.md`, `2026-09-08-pandas-nos-dados-design.md` | **mortas** — governavam os capítulos 6 a 17 na abordagem do Grus |

## A pedagogia do ISLP

**A tese: o modelo é uma ferramenta que se escolhe, se ajusta e se julga** — não se implementa. Consequências que decidem toda dúvida:

- **`scikit-learn` de ponta a ponta. Nada é escrito à mão.** Todo capítulo é conceito mais `fit`/`predict`/`cross_val_score`/`Pipeline` sobre dado real. A matemática aparece em fórmula e em gráfico, nunca em implementação.
- **Nada de inferência.** Sem erro-padrão de coeficiente, estatística *t*, valor-p ou teste de hipótese — decisão explícita do autor.
- **O pacote `ISLP` não entra.** Ele existe para os labs do livro-fonte e traz uma API que só existe ali; os conjuntos de dados do ISLP entram como CSV commitado em `dados/`, como sempre.

| Pode e deve | Não pode em chunk que executa |
|---|---|
| `scikit-learn` inteiro: estimadores, `Pipeline`, `ColumnTransformer`, `GridSearchCV`, métricas | `statsmodels` — a disciplina não faz inferência |
| `pandas` para todo trabalho de dado, `numpy` para conta de array, `matplotlib` para todo gráfico | o pacote `ISLP`; `torch` (redes convolucionais e recorrentes são da disciplina de Deep Learning) |
| | `scipy`, **exceto** a exceção registrada do dendrograma do capítulo 15 |

`test_nenhum_chunk_executavel_usa_biblioteca_proibida` trava a tabela da direita; qualquer uma delas pode aparecer só num bloco ```` ```python ```` que **não executa**, para mostrar o que existe lá fora sem passar a depender.

**A citação inverte a regra do Grus.** O ISLP numera as seções (3.3.1, 8.2.2 estão no sumário dele), então o callout de correspondência cita o **número**:

```markdown
::: {.callout-note}
Esta seção corresponde à seção 8.2.2 de @james2023.
:::
```

`test_nenhuma_secao_inventa_numero_de_secao_do_grus` continua valendo para os capítulos 1 a 5, que seguem citando o Grus por título. Os capítulos 6 e 17 não têm correspondência no ISLP e não trazem o callout — exceção registrada com motivo.

**Toda seção dos capítulos 6 a 17 tem ao menos uma figura**, e todo chunk que chama `plt.` aplica `estilo-figuras.mplstyle` (na raiz — fundo transparente, cores medidas contra os temas claro e escuro do site). `test_toda_secao_tem_figura` e `test_todo_chunk_que_desenha_aplica_o_estilo` travam as duas regras; uma seção sem figura ou um chunk sem o estilo entra em `SECOES_SEM_FIGURA`/`BIBLIOTECA_LIBERADA` (`tests/test_estrutura.py`) só com o motivo escrito — `test_toda_excecao_de_figura_e_de_biblioteca_tem_motivo_e_arquivo_real` cobra isso. Antes de escrever o código de qualquer gráfico, carregue a skill `dataviz`.

**Epígrafes de capítulo são citações reais, verificadas em fonte primária.** Na escrita do capítulo 6, duas candidatas foram descartadas por falha de verificação — inclusive a célebre "In God we trust; all others must bring data", que não tem evidência de ser de Deming. A regra: **se a atribuição não se verifica em fonte primária, a citação não entra.** É preferível um capítulo sem epígrafe a uma citação inventada.

## A regra editorial: o site não comenta a própria escrita

Pedido explícito do autor, e vale para sempre:

> *"comentários sobre esse tipo de alteração não devem ser incluídos no conteúdo do site. O conteúdo do site é sobre ciência de dados, não sobre decisões do autor ou modificações ao escrevê-lo."*

Nenhum `.qmd` de `content/` diz que houve mudança de abordagem, que um capítulo foi reescrito, que a versão anterior fazia de outro jeito, ou que o material "agora" usa tal ferramenta. O aluno lê ciência de dados; a história editorial vive em `docs/` e aqui.

É a mesma disciplina que já tirou do livro a explicação de Shift+Enter, que foi parar no onboarding do Colab: **texto sobre a ferramenta ou sobre o processo não é texto sobre o conteúdo.**

`test_o_conteudo_nao_comenta_a_propria_escrita`, em `tests/test_estrutura.py`, guarda isso com uma lista curta de padrões ancorados no material como sujeito. Falso positivo se corrige editando `META_COMENTARIO` **com o motivo escrito**, nunca silenciando o teste. Os padrões são estreitos de propósito: o capítulo 5 diz "abordagem anterior" e "passou a ser" falando de gradiente descendente, e um padrão frouxo os pegaria.

## Visão geral

**Quarto book** da disciplina *Bases 5 — Ciência de Dados*, do curso de **Ciência da Computação** da UnDF. Português brasileiro, exemplos em Python, publicado no GitHub Pages a cada push na `main`.

### A restrição que molda o texto inteiro

**A turma não cursou Bases 3 com este professor.** Cada aluno viu estatística com outro livro e outro tratamento. Portanto:

- **Nunca** faça referência específica a Bases 3 — nada de "como você viu com o `statsmodels`", nada de reaproveitar os dados brasileiros daquele livro.
- Pode-se assumir o **tema** (média, mediana, desvio padrão, correlação, normal, testes), nunca o **tratamento**.
- **Álgebra linear não pode ser assumida** — não é estatística. É a dependência mais pesada do material, e é por isso que o capítulo 4 existe.

E uma premissa que **caiu**: não assuma que o aluno já treinou um modelo chamando uma função pronta. A antiga identidade do livro — *"abre as caixas-pretas que o aluno usou antes"* — se apoiava nisso, e a turma não confirmou a premissa. Nada de *"você provavelmente já ajustou uma reta com um `.fit()`"*.

## Comandos

O caminho canônico é o container — é ele que renderiza local e no CI.

```bash
make preview          # hot-reload em http://localhost:4201
make render           # renderiza para _book/
make refresh CAP=NN   # reexecuta UM capítulo do zero (apaga só o _freeze/ dele)
make secoes CAP=NN    # executa cada .qmd do capítulo num kernel próprio, sem render
make teste            # roda a suíte de invariantes estruturais (pytest, tests/)
make offline          # renderiza SEM REDE, com _freeze/ limpo antes — prova o isolamento
make jupyter          # JupyterLab em http://localhost:8901 (notebooks de aula)
make notebooks        # regenera notebooks/ a partir dos .qmd
make notebooks-teste  # executa os notebooks de ponta a ponta
make atividade FONTE= # gera as duas versões (aluno e gabarito) de uma atividade
make shell            # shell dentro do container
make check            # quarto check
make build            # reconstrói a imagem (após mudar Dockerfile ou uv.lock)
make lock             # regenera uv.lock após editar pyproject.toml
make clean            # remove _book/, _freeze/, .quarto/ e o lixo de render abortado
```

**`make teste` roda `pytest tests/`** — 48 testes em sete arquivos: `test_estrutura.py` (registro no `_quarto.yml`, caminhos de dados, os totais de 6 capítulos / 27 seções / 33 arquivos contra o `LIVRO` de `scripts/gerar-stubs.py`, todo link interno para `.qmd` resolvendo, a regra editorial acima, nenhuma seção inventando número do Grus, e os três guardas da spec do ISLP: nenhum chunk executável usa biblioteca proibida, toda seção dos capítulos novos tem figura, e todo chunk que desenha aplica `estilo-figuras.mplstyle`), `test_scratch.py` (o pacote vendorizado — inclusive um hash SHA-256 travando que `scratch/` continua verbatim upstream), `test_dados.py` (os conjuntos commitados, inclusive que `alugueis.csv` preserva a armadilha do `andar`), `test_freeze.py` (o cache envenenado), `test_gradiente.py` (toda subida de gradiente tem motivo registrado), `test_notebooks.py` (os notebooks de aula não podem defasar dos `.qmd`) e `test_atividades.py` (o gabarito não pode vazar para o site).

É o que garante a regra "todo `.qmd` novo precisa ser registrado em `_quarto.yml`" — sem essa suíte, um arquivo esquecido no YAML só aparece quando alguém percebe a seção faltando no site publicado.

### Verificar um capítulo sem renderizar o livro

O `make render` é **serializado** e leva minutos; vários agentes disputando o lock não funciona, e editar um `.qmd` enquanto um render roda envenena o `_freeze/` (as duas seções adiante). Por isso quem escreve um capítulo **não renderiza**: verifica com os comandos abaixo, e o render completo é feito uma vez, por quem coordena, ao fim de cada bloco de capítulos.

Há um `.venv/` na raiz (gitignorado, criado por `uv sync`) com o mesmo lock do container, e é nele que essa verificação roda — sem Docker, em paralelo, em segundos:

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0          # os mesmos ENV do Dockerfile
.venv/bin/python scripts/gerar-notebooks.py      # regenera os notebooks (idempotente)
.venv/bin/python scripts/executar-secoes.py 05   # cada .qmd do cap. 5 num kernel PRÓPRIO
.venv/bin/python scripts/executar-notebooks.py cap05   # o capítulo inteiro num kernel só
.venv/bin/pytest tests/ -q
```

**`scripts/executar-secoes.py` é o análogo fiel do `quarto render` para um capítulo.** Ele reaproveita o parser de `gerar-notebooks.py` (que já sabe o que é callout e o que é `eval: false`), monta em memória um notebook só de código para **cada** `.qmd` e o executa num kernel novo, com o cwd na raiz — que é o que o `execute-dir: project` faz no Quarto. É assim que se pega o `import` que falta numa seção porque foi feito na anterior: o notebook de aula, com um kernel só para o capítulo inteiro, deixa isso passar. Não toca em `_freeze/` nem em `.quarto/`, então pode rodar em paralelo e nunca precisa do lock. O alvo `make secoes CAP=NN` roda o mesmo script dentro do container.

Os dois modos são complementares e ambos importam: `executar-secoes.py` reproduz o **site** (um kernel por página), `executar-notebooks.py` reproduz a **aula** (um kernel por capítulo).

**Mostrar um erro na página exige `try/except`, nunca `#| error: true`.** A opção do Quarto que deixaria uma célula levantar exceção sem derrubar o render **não é honrada aqui**: `scripts/executar-secoes.py` e `scripts/executar-notebooks.py` constroem o `NotebookClient` sem `allow_errors`, e `scripts/gerar-notebooks.py` só entende a opção `eval`. Uma célula que levanta exceção mata a verificação e o `make notebooks-teste`. Para mostrar um erro como conteúdo — a seção 6.3 faz isso com um `TypeError` de conversão de tipo —, capture com `try/except` e **trunque** a mensagem antes de imprimir: a exceção crua do `TypeError` daquela seção tem 12.722 caracteres, porque o `pandas` concatena a coluna inteira dentro do texto do erro.

**Porta 4201, não 4200.** O `bases_3_estatistica` ocupa a 4200, e os dois livros são editados na mesma tarde.

Ao adicionar dependência: edite `pyproject.toml` → `make lock` → `make build`. **Teto de versão em todas**; pacotes `0.x` levam teto no **minor**, porque em SemVer pré-1.0 é o minor que carrega mudança incompatível. No Bases 3 isso não é teórico: o pandas 3 quebrou dois exemplos **sem levantar exceção**, só devolvendo a resposta errada.

`execute: freeze: auto` está ativo. Cache em `_freeze/` (gitignorado). Chunk preso com saída velha → `make clean`.

### `ERROR: Directory not empty` no fim do render — o que fazer

No macOS, o `make render` às vezes aborta com `ERROR: Directory not empty (os error 39): remove '/livro/content/capNN/xxx_files'`. **Não é erro de conteúdo.** Todas as células executaram; o que falha é a faxina que o Quarto faz no fim, ao remover os diretórios `*_files` temporários — eles ficam com `figure-html/` e `mediabag/` vazios dentro, e o bind mount do Docker no macOS não sincroniza a remoção a tempo.

A probabilidade cresce com o número de `*_files` criados numa rodada, ou seja, **piora conforme mais capítulos ganham figuras**. Ela é aleatória: cada tentativa aborta num arquivo diferente.

**O `make render` já lida com isso sozinho.** O alvo apaga o lixo da tentativa anterior e repete, até seis vezes, e imprime `render OK (tentativa N)` quando converge. Você não precisa fazer nada — e **não deve** tentar contornar a corrida manualmente.

Isso não é conselho de estilo: um agente já ficou preso em laço por horas tentando entender um render que abortava, e a tentativa de contorná-lo à mão foi o que produziu o laço.

Se o `make render` falhar nas seis tentativas, aí **não** é a corrida do bind mount. Rode `docker compose run --rm --no-deps livro quarto render` direto para ver o erro real.

**Nunca use `make clean` para tratar esse sintoma.** Ele apaga o `_freeze/` junto, e aí todos os chunks reexecutam — o que aumenta a janela da corrida e torna a falha *mais* provável, não menos. Medido: falhou três vezes seguidas com `_freeze` frio e passou de primeira com ele aquecido. É por isso que o alvo `render` nunca toca no `_freeze`.

O CI **não** é afetado: lá o checkout é limpo e o sistema de arquivos é nativo do Linux, sem bind mount.

### `make render` é serializado — um render por vez neste repositório

Este material é escrito por agentes, e mais de um pode estar ativo. Dois `quarto render` simultâneos sobre o mesmo `_freeze/` corrompem o cache: um grava a saída congelada de um chunk enquanto o outro lê o índice, e o livro sai com saída trocada entre páginas — **sem erro nenhum na tela**. É a pior classe de falha deste projeto, silenciosa e difícil de atribuir.

Quem escreve um capítulo verifica com `scripts/executar-secoes.py`, que não toca no `_freeze/`, e **só quem coordena renderiza**, uma vez por bloco de capítulos. Render em fila é o sintoma de que o trabalho está organizado errado, não um problema a contornar.

O alvo `render` toma um lock antes de começar. Se outro render estiver rodando, ele imprime `outro render em andamento neste repositório; aguardando a vez...` **uma vez** e espera, pegando a vez sozinho. Isso é comportamento normal: **não interrompa, não contorne, não mate o processo.**

Detalhes que importam se você for mexer nisso:

- O lock é um `mkdir` (`.render-lock/`, gitignorado), porque `mkdir` é atômico em qualquer POSIX. `flock` **não existe no macOS de fábrica** — foi por isso que não foi usado.
- Um `trap ... EXIT INT TERM` devolve o lock mesmo se o render abortar ou levar Ctrl-C.
- Depois de 30 minutos esperando, o lock é considerado preso (agente morto) e removido com aviso. Um agente que morreu não pode bloquear o material para sempre.
- `make offline` **não** pega o lock: ele apaga o `_freeze/` de propósito e é rodado deliberadamente antes de publicar, não em paralelo com escrita.
- **A espera é limitada a ~7 minutos, e o motivo não é o render.** A ferramenta de shell dos agentes aborta em 10 minutos; uma espera ilimitada estouraria esse teto e devolveria um timeout opaco, sem dizer se o material quebrou, se o lock travou ou se era só a vez de outro. **Isso já custou um capítulo entregue sem verificação.** Passado o limite, o alvo imprime `NÃO RENDERIZOU — a vez ainda é de outro agente` e sai com **75** (`EX_TEMPFAIL`): a instrução é rodar `make render` de novo, não investigar.

**Consequência prática de coordenação: não deixe mais de dois ou três agentes que precisem renderizar trabalhando ao mesmo tempo.** Cada render leva alguns minutos, e a fila cresce mais rápido que a paciência da ferramenta.

**Nunca edite `scripts/render-seguro.sh` (nem qualquer `.sh`) enquanto um agente pode estar rodando.** O bash lê o script **incrementalmente**, conforme executa — editar o arquivo no meio faz o interpretador perder a posição e estourar num erro de sintaxe que não existe, tipicamente `syntax error near unexpected token 'done'`. Isso já derrubou o render de um agente, que gastou tempo investigando um defeito que não era dele nem do conteúdo.

Se precisar mudar o script com agentes ativos, escreva num arquivo temporário e mova por cima (`mv` é atômico, e o bash em execução continua lendo o inode antigo). Editar direto só quando ninguém estiver renderizando.

### O `_freeze` envenenado — a falha mais silenciosa deste projeto

**Sintoma:** o `.qmd` está certo, o `make render` diz `render OK`, e a página publicada em `_book/` continua mostrando a versão antiga. Rodar `make render` de novo não muda nada. Nenhum erro, nenhum aviso.

**Causa:** o `freeze: auto` guarda, para cada arquivo, o par *(hash do fonte, markdown executado)*. Se alguém **edita o `.qmd` enquanto o render roda**, o Quarto executa a versão velha e grava esse resultado velho junto com o hash da versão **nova**. Dali em diante o hash bate, o cache é considerado válido, e aquele arquivo **nunca mais reexecuta sozinho**.

Isto não é hipótese: já publicou seções desatualizadas, e passou por um render inteiro sem uma linha de aviso. Foi encontrado só porque um revisor comparou o fonte com o HTML linha a linha.

**Não dá para detectar comparando hashes** — o hash bate; é exatamente esse o problema. O que se detecta é a *causa*: um `.qmd` cuja data de modificação mudou entre o começo e o fim do render.

**O `scripts/render-seguro.sh` faz isso automaticamente.** Ele fotografa os mtimes antes e depois, e se algum arquivo mudou no meio, apaga o `_freeze` só desses e renderiza de novo (até 3 rodadas). Se ainda assim houver edição concorrente, ele avisa em caixa alta, nomeia os arquivos e **sai com sucesso** — porque o render funcionou, e um agente que vê "falha" tende a rodar `make clean`, que é o remédio errado.

**Se você desconfiar de uma página específica**, o remédio manual é `make refresh CAP=NN` — apaga o `_freeze/` só daquele capítulo e renderiza. Nunca `make clean`.

**Não escreva `#| cache: true` num chunk.** Esse é o cache por-célula do motor **knitr** (R) e não existe para o motor **Jupyter**, que é o deste projeto (`jupyter: python3`) — a opção é silenciosamente ignorada. O Jupyter tem um cache próprio, o *Jupyter Cache*, mas ele funciona por **notebook inteiro** (qualquer célula mudar reexecuta todas) e depende do pacote opcional `jupyter-cache`, que não está no `uv.lock` deste projeto. Na prática, o `freeze: auto` já resolve o que interessa aqui — por **arquivo** `.qmd`, sem depender de nenhum pacote extra.

## Arquitetura

### Estrutura de conteúdo

Um diretório por capítulo, um `.qmd` por seção:

```
content/cap05/
├── index.qmd                          # Visão geral + tabela de seções + Leituras adicionais
├── 01-a-ideia-por-tras-do-gradiente.qmd
├── 02-estimando-o-gradiente.qmd
└── ...
```

**Todo `.qmd` novo precisa ser registrado em `_quarto.yml`** sob `book.chapters` — arquivo não listado não aparece no site. A ordem vem do YAML, não do nome do arquivo; para reordenar, `git mv` e atualize o YAML na mesma operação. `make teste` verifica isso: `test_todo_qmd_esta_registrado_no_quarto_yml` e o teste que confere os totais contra o `LIVRO` falham se um `.qmd` existir sem entrada no YAML.

**`LIVRO`, em `scripts/gerar-stubs.py`, é a fonte da verdade** sobre o que o material deve conter. Um capítulo novo entra ali primeiro; `python3 scripts/gerar-stubs.py` cria os stubs que faltam (nunca sobrescreve o que existe) e `--yaml` imprime o bloco `chapters` para colar no `_quarto.yml`.

### Cada seção roda no seu próprio kernel: reconstrua o que herda

No site, cada `.qmd` executa num kernel **próprio** e nome nenhum atravessa páginas — a razão de `import` se repetir de seção para seção. Isso tem uma consequência sobre **decisões**, não só sobre nomes: quando uma seção anterior decide algo sobre o dado e diz que a decisão fica, a seguinte não herda esse estado — precisa reconstruí-lo no chunk de setup, sem reexplicar.

Já produziu uma contradição visível no capítulo 6: a seção 6.4 preenche `andar` com zero e fecha dizendo "é essa a versão que fica"; a 6.5 relia o CSV aplicando só `na_values`, e mostrava um `describe()` com os 2.461 nulos de volta — ninguém errou um número, a arquitetura de um kernel por página desfez, em silêncio, uma promessa do texto. **Regra: a seção que herda uma decisão a reconstrói no chunk de setup; a seção que a tomou não precisa reexplicar por quê.**

### Os notebooks de aula — derivados do material, nunca editados à mão

`notebooks/` tem **um `.ipynb` por capítulo**, para executar ao vivo na aula. Eles são gerados por `scripts/gerar-notebooks.py` a partir dos `.qmd`, e a relação é a mesma do `scratch/` com o upstream: **o `.qmd` é a fonte, o notebook é cópia derivada.** Editar um `.ipynb` é trabalho perdido — o próximo `make notebooks` sobrescreve. Mudou a aula? Mude o `.qmd`.

`test_notebooks_estao_atualizados` regera cada notebook em memória e compara com o arquivo em disco, então um `.qmd` que anda sem o notebook derruba `make teste`. É o guarda contra a falha óbvia: a aula rodando uma versão do capítulo que o site publicado já não tem.

**Os chunks dentro de callouts.** Chunks `{python}` que **executam** moram dentro de `::: {.conceito}`, `::: {.exemplo}` e afins. Um conversor que trate todo `:::` como texto os transforma em markdown — e aí o notebook abre, executa, e quebra várias células adiante num `NameError` que não aponta para a causa. O gerador converte o corpo do callout recursivamente: o que é prosa vira blockquote, o que é código continua célula de código. `test_todo_chunk_executavel_do_livro_virou_celula` conta os chunks de forma independente do gerador e trava isso.

Três traduções que o gerador faz porque o Jupyter não entende o que o Quarto entende:

- **Callouts** viram blockquotes com rótulo e ícone.
- **Links entre `.qmd`** viram URLs absolutas do site publicado — um caminho relativo a `../cap05/index.qmd` não resolve de dentro de `notebooks/`.
- **Citações** viram o texto da citação, com a bibliografia numa célula final. As referências saem do `references.bib`, para não existir uma segunda cópia.

**A célula de preparo.** No site, `execute-dir: project` põe o cwd na raiz, e é isso que faz `from scratch...` e `dados/...` resolverem. O notebook não tem esse mecanismo, então a primeira célula de código de todo notebook sobe os diretórios até achar `_quarto.yml` e faz `os.chdir`. Funciona tanto com o Jupyter aberto na raiz quanto dentro de `notebooks/`.

**Os arquivos entram no git sem saída de execução**, de propósito: quem executa é o aluno. Saída congelada tornaria o diff ruído binário e tiraria o sentido de rodar o código. `test_nenhum_notebook_guarda_saida` trava isso.

**Uma diferença de execução em relação ao site, que vale conhecer:** lá, cada `.qmd` roda no **seu próprio kernel** e nomes não atravessam páginas — daí os `import` se repetirem de seção para seção. No notebook, o capítulo inteiro roda num kernel só. Na prática só ajuda (a ordem de leitura é a mesma), mas é a razão de um notebook poder executar uma célula que, isolada, faltaria um import.

**O Colab é o ambiente de aula, e é ele que dita a célula de preparo.** Cada `index.qmd` de capítulo traz, logo abaixo do topo, um link `colab.research.google.com/github/.../notebooks/capNN-*.ipynb`. No Colab não existe cópia do projeto: `scratch/` e `dados/` não estão lá, e a busca pelo `_quarto.yml` subindo diretórios não acha nada. Por isso a célula de preparo, além do `chdir`, **clona o repositório** quando não encontra o projeto — `git clone --depth 1` num `/content/bases5`. Sem isso, todo notebook quebraria na primeira célula quando aberto no Colab, que é justamente como o aluno vai abri-lo.

O link é do site para o notebook e **não** o contrário: `LINHA_COLAB`, no gerador, remove a linha do Colab ao converter o `index.qmd`, porque dentro do notebook ela mandaria o leitor abrir o notebook em que ele já está. `test_todo_capitulo_tem_link_para_o_colab_e_nenhum_notebook_o_repete` trava os dois lados.

**O onboarding do Colab vive em `scripts/onboarding-colab.md` e entra só no notebook do capítulo 2** — a aula 2 é a primeira em que a turma põe a mão no ambiente. Ele explica Shift+Enter, a armadilha da ordem de execução, o `assert` como idioma da casa, a semente obrigatória e o "salvar cópia no Drive". **Não está no site de propósito** — ver "A regra editorial", acima. Um teste confere que ele está no notebook e que não vazou para `content/`.

**Verificação:** `make notebooks-teste` executa os notebooks de ponta a ponta com o cwd em `notebooks/` — o caso mais apertado. É o análogo do `quarto render` para os notebooks, e pelo mesmo motivo: os módulos de `scratch/` têm `assert` no nível do módulo. Com seis capítulos leva cerca de **10 segundos**; a medição antiga de ~11 minutos era dos 17, dominada pelo MNIST e pelo bootstrap.

`notebooks/` está no **`.quartoignore`** — sem isso o Quarto trataria os `.ipynb` como conteúdo do site.

### `apoio/` — páginas interativas de aula, servidas junto do site

`apoio/` guarda páginas HTML autônomas para usar **ao vivo na aula**, ao lado do slide e do notebook. Hoje são duas, as duas do capítulo 5:

- **`gradiente-descendente.html`** (seções 5.1 a 5.4) — o aluno escolhe a função, mexe no tamanho do passo e vê, a cada iteração, a derivada, o passo e o rastro; em uma variável e em duas, com contorno e superfície 3D lado a lado.
- **`lote-minibatch-estocastico.html`** (seção 5.6) — os três métodos treinando ao mesmo tempo na regressão da seção 5.5, com a perda (log-log) e a reta ajustada em dois painéis simultâneos. **Um interruptor troca o que o relógio conta**, e é aí que mora a lição: em *chamadas a `gradient_step`* os três gastam o mesmo e os epochs saem diferentes (5.000 / 1.000 / 50), com o estocástico sete ordens de grandeza atrás; em *epochs* os três dão o mesmo número de passadas e o gasto sai diferente (1.200 / 6.000 / 120.000 chamadas), e aí o estocástico parece ganhar de longe. A mesma corrida, duas conclusões opostas, conforme a coluna que se decide manter fixa.

  Trocar de modo também troca a granularidade do registro: em *epochs* a perda é medida uma vez por epoch, isto é, só nas **fronteiras** — onde a cascata do estocástico já se autocorrigiu. Por isso o serrilhado some ao virar o interruptor, e isso não é bug: é a observação que a própria seção faz ao medir "só nas fronteiras de epoch".

**São arquivos estáticos, não conteúdo do site.** Um HTML só, sem build, sem dependência de rede, que abre com dois cliques e roda offline. Não têm `.qmd`, não entram no `book.chapters` e não aparecem no sidebar — o que os leva ao site é uma linha em `project.resources`, no `_quarto.yml`, que o Quarto copia para `_book/apoio/`. Sem essa linha, a página existe no repositório e **não** existe no site publicado.

As duas dividem tokens, tipografia e componentes de propósito — são irmãs, e uma terceira página deve copiar o mesmo bloco `:root` em vez de inventar outro.

Quatro decisões que não são óbvias e custam tempo a redescobrir:

- **O link no capítulo é relativo, e vira absoluto só dentro do notebook.** As duas pontas pedem coisas opostas e as duas falham em silêncio: com URL absoluta no `.qmd`, o `make preview` manda o leitor para o site publicado em vez da cópia local que ele está olhando; com caminho relativo no notebook, o link não resolve, porque de `notebooks/` (ou do Colab) nenhum caminho do site resolve. Por isso `reescreve_links`, em `scripts/gerar-notebooks.py`, reescreve **todo** link relativo para a URL do site, e o que é específico do `.qmd` passou a ser apenas trocar a extensão. `test_toda_pagina_de_apoio_esta_publicada_e_linkada_certo` trava os dois lados.
- **`apoio/` não entra no `.quartoignore`**, e a tentação existe (`notebooks/` e `arquivo/` estão lá). Aqui seria contraproducente: o `.quartoignore` tira arquivos do projeto, e é justamente o projeto que precisa enxergar `apoio/` para copiá-lo como recurso. A proteção que `notebooks/` precisa não se aplica — o Quarto só trata `.qmd`, `.md` e `.ipynb` como entrada, e não há nenhum desses aqui.
- **`test_quarto_publica_apenas_o_diretorio_publico` não barra isto.** O teste casa só entradas de `resources` que começam com `atividades`, porque o que ele guarda é o gabarito. Recurso fora de `atividades/` passa — o que é o comportamento certo, mas parece proibido à primeira leitura do teste.
- **Editar o `index.qmd` de um capítulo obriga a rodar `make notebooks`**, senão `test_notebooks_estao_atualizados` derruba a suíte. Vale para o link de `apoio/` como vale para qualquer outra linha.

`test_toda_pagina_de_apoio_esta_publicada_e_linkada_certo` varre `apoio/` inteiro e cobra as três primeiras: recurso declarado, link relativo no `.qmd`, URL absoluta no notebook. Página nova entra na varredura sozinha — não é preciso editar o teste.

**A paleta sai do material e do logo.** O fundo e o texto são os do tema `cosmo`, o mesmo do site em modo claro (`#FFFFFF`, `#373A3C`); os azuis são amostrados de `images/logo-undf.png` — `#2264AF`, `#4195D1`, `#8FCEF1` e o navy `#27316E`. Eles vestem a paisagem inteira: curvas de nível, malha 3d, curva de `f`, aba ativa, botão principal. A trajetória é a única coisa quente da página, e isso é decisão, não descuido: a marca é toda azul, e um rastro azul sobre um mapa azul sumiria justamente no que mais importa de ver. O laranja é o complementar daqueles azuis. A regra de leitura da página é essa — **azul é o terreno, laranja é a descida** —, e quem mexer nas cores deve mantê-la.

**O que é reprodutível dígito a dígito, e o que não é.** Na página da seção 5.6, o lote inteiro e o estocástico não embaralham nada: basta fixar o `theta` inicial de `random.seed(0)` e `random.seed(2)` como constante — está no topo do arquivo, com a origem escrita — e o resto é determinístico, então as duas curvas reproduzem os laços da seção exatamente (medido: lote com MSE `4,107 × 10⁻⁸` e estocástico com `0,3394` e `theta = [20.0100, 4.4998]` em 5.000 chamadas). O minibatch embaralha, e o Mersenne Twister do Python não existe no navegador: a curva dele bate em comportamento, não em número, **e a página diz isso ao leitor** em vez de deixar parecer exata.

**Os números da página são conferidos contra o Python, não estimados.** A superfície de erro quadrático médio usa os dados da seção 5.5 (`inputs = [(x, 20*x + 5) for x in range(-50, 50)]`) em forma fechada — média(x) = −0,5 e média(x²) = 833,5 —, e a trajetória bate dígito a dígito com o laço da seção: no passo 5, inclinação 22,5464 e intercepto 0,5475. As faixas de α de cada função foram medidas antes de escrever a página, e é isso que faz os presets ensinarem o que prometem (o poço duplo fica preso até α ≈ 0,15, escapa entre 0,17 e 0,25, e não assenta acima de 0,29). Mexeu na função ou no passo? Meça de novo — um preset que não faz o que o rótulo diz é pior que preset nenhum.

### O pacote `scratch/` — vendorizado literalmente, nunca editado

Cópia fiel do repositório de Joel Grus (MIT, licença preservada), e o código dos capítulos 1 a 5. **Toda adaptação vive no `.qmd`, nunca no pacote** — assim um `diff` contra o upstream continua limpo, e `test_scratch_e_verbatim_upstream` trava isso com um hash SHA-256.

Com `execute-dir: project`, o cwd de todo chunk é a raiz e `from scratch.linear_algebra import dot` resolve sem `PYTHONPATH`.

Cada módulo tem um `if __name__ == "__main__":` com a demonstração do capítulo; ele não roda no import. Se o texto precisa daquele exemplo, chame as funções explicitamente no chunk.

**Dois efeitos colaterais verificados no código, e dois módulos que nunca são importados.**

**1. Importar alguns módulos desenha gráficos, e um escreve arquivo.** Chamadas `plt.*` no nível do módulo: `statistics.py` (5), `probability.py` (18), `working_with_data.py` (8), `visualization.py` (63).

A correção **não** é editar o pacote: é manter `im/` vazio, como o upstream tem. Chunks que importam desses módulos vão com `include: false` e `plt.close('all')` na sequência, senão a figura do import vaza para a saída da célula.

**`visualization.py` é o caso mais sério: nove `plt.savefig('im/viz_*.png')` no corpo do módulo.** É o módulo do capítulo 3, então todo `import scratch.visualization` grava esses nove arquivos em `im/` a cada render, inclusive local. O `.gitignore` já tem a regra (`im/*` ignorado, exceto `.gitkeep`) para que isso não seja varrido para um commit por um `git add` amplo.

**2. `getting_data` e `working_with_data` nunca são importados — cada um por um motivo diferente, e nenhum se corrige editando o pacote:**

- **`getting_data.py:90`** faz `requests.get` no corpo do módulo — importar dispara rede.
- **`working_with_data.py:148`** abre `stocks.csv` com um caminho relativo ao **cwd** no corpo do módulo — o upstream mantém esse arquivo na raiz do repositório dele; na nossa convenção, dado vive em `dados/`, então o `open()` estoura com `FileNotFoundError`. E as linhas 28–30 calculam `xs`, `ys1`, `ys2` com `random.random()` **sem semente**, enquanto as linhas 48–49 afirmam `0.89 < correlation(xs, ys1) < 0.91` — o valor real (~0,894) encosta na borda dessa janela, e o `assert` falha em **cerca de 25% das execuções** (duas medições independentes de 20.000 rodadas: 25,0% e 24,6%).

`tests/test_scratch.py`'s `NAO_IMPORTAVEIS` documenta os dois motivos e trava com um teste que a exclusão precisa vir com motivo escrito.

> Uma versão anterior deste arquivo dizia "cerca de 1 vez em 3, medido em 5 rodadas". Cinco rodadas não distinguem 25% de 33%. Fica como lembrete: **amostra pequena demais é o mesmo que chute com aparência de medição.**

**O pacote é vendorizado inteiro**, incluindo módulos que nenhum capítulo usa hoje. Podar não vale a pena: o hash de `test_scratch_e_verbatim_upstream` cobre o diretório todo, e a licença MIT pede a cópia preservada.

### Dados

**Nenhum byte vem da rede em tempo de render.** Os conjuntos entram commitados em `dados/` (~13 MB); a proveniência de cada um está em `dados/README.md`, e `test_dados.py` cobra que o README documente todos.

O capítulo 6 já usa dado próprio, brasileiro e sem limpeza prévia — `alugueis.csv`, `estados.csv` e `cidades.csv`, com a proveniência em `dados/README.md`. Boa parte dos conjuntos restantes alimentava os capítulos 6 a 17 do Grus e hoje não é usada por nenhuma página nova; **ficam mesmo assim**, porque removê-los para reintroduzir em duas semanas é trabalho jogado fora. Do capítulo 7 em diante os dados são os do ISLP (`Advertising`, `Auto`, `Credit`, `Heart`, `College`, `Carseats`, `Default`, `Smarket`, `Hitters`, `Wage`, `OJ`, `Caravan`, `USArrests`, `NCI60` — as URLs de origem de cada um estão registradas no plano da fundação), baixados uma vez por `scripts/baixar-dados.py` e commitados, nunca em tempo de render. `pandas` já é usado (capítulo 6); `numpy` e `scikit-learn` seguem declarados no `pyproject.toml` sem uso executável ainda — só aparecem nos callouts ilustrativos dos capítulos 1 a 5 — e entram em uso de verdade a partir do capítulo 7. `requests`, `beautifulsoup4`, `html5lib`, `python-dateutil` e `pillow` são sobra da abordagem do Grus sem uso hoje; podá-los é limpeza que pode esperar (custa `make lock` e `make build`).

**Caminhos a partir da raiz**, sempre:

```python
acoes = pd.read_csv("dados/stocks.csv")        # ✓
acoes = pd.read_csv("../../dados/stocks.csv")  # ✗ nunca
```

### Armadilhas de `pandas` medidas

Três, e todas custam um número errado publicado sem erro nenhum na tela — vale conferir esta lista antes de desconfiar do dado:

- **`pd.read_html` precisa de `flavor="bs4"`** neste projeto: o padrão é `lxml`, que não está no `uv.lock`. Sem o argumento, `ImportError` e render no chão. **Não instale `lxml` para contornar.**
- **`na_values=["n/a"]` é redundante** — `n/a` já está na lista padrão de marcadores nulos do `pandas`. O marcador que *não* está é `N/D`: com ele a coluna inteira vira `object` e `Series.sum()` concatena strings em vez de somar, sem erro nenhum.
- **`memory_usage(deep=True)` numa coluna de texto não-ASCII é contaminado pela ordem dos chunks.** Chamar `nunique()` (ou qualquer coisa que use `hash()` das strings) **antes** de medir infla o resultado: no CPython, o hash de uma `str` não-ASCII popula um cache interno de UTF-8 que o `sys.getsizeof` passa a contar. Medido em `dados/alugueis.csv`, coluna `cidade`: **730.981 bytes** medindo antes, **795.738** medindo depois de um `nunique()` — 8,9% de diferença sem um byte de dado ter mudado. A coluna `Sigla` de `dados/estados.csv`, que é ASCII, dá 1.509 nos dois casos, o que isola a causa. Consequência prática: **meça a memória primeiro, explore a coluna depois.** Uma seção que inverta a ordem publica um número errado sem erro nenhum na tela.

### Sementes em chunks estocásticos — obrigatório

**Todo chunk com RNG usa semente explícita.** Sem isso, cada render produz números e gráficos diferentes: o `freeze` perde o sentido, o diff do site publicado vira ruído, e o material deixa de bater com o que o aluno vê na tela.

Nos capítulos 1 a 5 a forma é `random.seed(42)`, porque o código é `random` da stdlib. Qual gerador o material novo usa é decisão da spec das fontes; a regra da semente explícita **não** depende disso.

**Semear um gerador e sortear de outro é um jeito silencioso de achar que fixou a aleatoriedade sem ter fixado.** `random.seed` não tem efeito nenhum sobre o `numpy.random`, e nenhum dos dois é escutado pelo `scikit-learn`, que tem o próprio `random_state`.

**Sorteio novo, número novo.** `random.seed(12)` com `random.shuffle` e `default_rng(12).permutation` produzem divisões diferentes. Toda afirmação do texto que dependa de um sorteio específico — uma matriz de confusão, uma acurácia, um coeficiente de bootstrap — é **recalculada a partir da saída nova**, nunca copiada de uma versão anterior. Foi a principal fonte de trabalho de revisão na reescrita que morreu, e vai voltar a ser.

### Ambiente

Duas camadas travadas: `pyproject.toml` + `uv.lock` fixam as versões; o `Dockerfile` consome esse lock (`uv sync --frozen`) sobre um SO fixo com Quarto e locale `pt_BR.UTF-8`. O mesmo container renderiza local e no CI.

Dependências: `jupyter`, `matplotlib`, `numpy`, `pandas`, `tqdm`, `requests`, `beautifulsoup4`, `html5lib`, `python-dateutil`, `pillow`, `scikit-learn` e `pytest`. **Teto de major em todas**; `pandas>=2,<3` não é burocracia — é o pandas 3 que quebrou dois exemplos do livro irmão sem levantar exceção.

`scipy` **não** é dependência declarada — não use, mesmo que ele apareça instalado como transitiva do scikit-learn.

Dois detalhes herdados, já pagos no Bases 3:

- O venv fica em **`/opt/venv`**, não em `/livro/.venv`. O `compose.yaml` faz bind mount do projeto sobre `/livro`, o que apagaria um venv que estivesse ali.
- O `Dockerfile` grava `/etc/profile.d/venv.sh` reexportando o `PATH`. Um shell de **login** recarrega `/etc/profile`, que reescreve o `PATH` e descartaria o `ENV PATH` da imagem — fazendo `python` cair no interpretador do sistema. Se `make shell` resolver o Python errado, é o primeiro lugar a checar.

`MPLBACKEND=Agg` é obrigatório: sem display, o matplotlib estoura ao importar.

**`PYTHONHASHSEED=0` também é obrigatório, e o motivo é sutil.** `scratch/naive_bayes.py:113` tem, no nível do módulo, um `assert` de igualdade **exata** de float sobre uma soma que percorre um `Set[str]`. A ordem de iteração de um `set` depende do hash das strings, que o Python randomiza por processo, e soma de ponto flutuante não é associativa — então a ordem muda o último bit e o assert falha. Medido neste container: **2 de 15 sementes falham no import; com `PYTHONHASHSEED=0`, 15 de 15 passam.**

Isso torna instável qualquer coisa que importe aquele módulo — hoje, a suíte de testes, que importa `scratch/` inteiro. **Não afrouxe isso.** A correção fica no `Dockerfile`, não em `scratch/`, porque o pacote é vendorizado literalmente e nunca editado.

### Verificação

0. **`scripts/executar-secoes.py`**, o mais barato e o primeiro a rodar: executa cada `.qmd` de um capítulo num kernel próprio, sem render e sem lock (ver "Verificar um capítulo sem renderizar o livro"). É o que se usa enquanto se escreve.

1. **O `quarto render` é o teste.** Os módulos do `scratch/` executam `assert` no nível do módulo (`assert add([1, 2, 3], [4, 5, 6]) == [5, 7, 9]`, `linear_algebra.py:21`). Importar o pacote roda a suíte do próprio autor: um upgrade que quebre `add`, `dot` ou `mean` derruba o render no import, em vez de publicar um número errado em silêncio.

2. **Render com a rede desligada** — `docker run --network none`, tanto local (`make offline`) quanto no CI (job `offline`). O risco de rede em tempo de render não falha de modo visível: com rede, tudo passa; o que se degrada é a reprodutibilidade, silenciosamente, até a página raspada mudar. Renderizar offline converte essa classe de fragilidade num teste booleano.

   **`make offline` apaga `_freeze/` antes de renderizar, de propósito.** Com `freeze: auto`, um `.qmd` que não mudou não reexecuta — o Quarto devolve a saída congelada sem rodar um chunk sequer. Rodado de cache quente, `make offline` renderizaria "com sucesso" tendo executado zero código Python, o que não prova nada. Se um dia esse `rm -rf` parecer zelo exagerado e alguém cogitar tirá-lo para acelerar o alvo: **não tire** — é o que garante que "offline passou" significa "o código rodou sem rede", não "o cache existia".

3. **`quarto check`**, diagnóstico do ambiente.

Não há equivalente ao teste de Playwright do Bases 3 — aquilo existe para células `{ojs}`, que este material não tem.

### CI/CD

`.github/workflows/quarto-render.yml`: cinco jobs a cada push na `main` — `build-image` (constrói e envia ao GHCR); em seguida, em paralelo, `testes` (`pytest tests/` **dentro** da imagem) e `offline` (`docker pull` + `docker run --network none` num runner comum, contra um checkout novo que já não tem `_freeze/`); depois dos dois, `render` (roda **dentro** da imagem, `quarto render` → `_book/`, sobe como artefato); por fim `publish` (runner limpo, publica `_book/` em `gh-pages`). A cadeia de `needs` é sequencial o bastante para que uma falha em `testes` **ou** em `offline` bloqueie `render` e, por consequência, `publish` — nada quebrado chega a `gh-pages`.

**O nome da imagem precisa ser minúsculo e literal**: `ghcr.io/bragad/undf-bases5-ciencia-de-dados-202602:latest`. O GHCR rejeita maiúsculas, então não dá para usar `${{ github.repository_owner }}`, que resolveria para `BragaD`.

`_book/` e `_freeze/` são artefatos gitignorados. `docs/` **não** é gitignorado — guarda specs e planos.

Passos manuais no GitHub, uma única vez: **Settings → Actions → General → Workflow permissions** em "Read and write"; e, depois do primeiro workflow verde, **Settings → Pages → Source** → branch `gh-pages`, pasta `/ (root)`. Até isso, o site retorna 404 com o CI passando.

### Classes CSS e o spoiler

```markdown
::: {.conceito}
Conceito importante (azul).
:::

::: {.exemplo}
Exemplo (verde).
:::
```

`spoiler.html` protege um `<div>` com hash SHA-256. **Isso é ofuscação, não proteção.** O conteúdo viaja em texto puro no HTML publicado; o hash só alterna qual `<div>` fica visível, e qualquer aluno lê tudo com Ctrl+U. **Nunca** para gabarito, prova ou qualquer coisa que o aluno não deva ver antes da hora. Serve só para "revelar a resposta depois de tentar".

Material avaliativo segue o padrão de `../../202601/BasesIV_EngSoft_BD/atividades/`: uma fonte `.qmd` renderizada duas vezes (aluno e gabarito) via metadado + filtro Lua, fora do projeto-livro.

## Os repositórios irmãos

Convenção da casa, úteis quando uma dúvida de infraestrutura não estiver resolvida aqui:

- `../bases_3_estatistica/` — Quarto + Docker + `uv`, um `.qmd` por seção. Formato de `Makefile`, padrão de `.devcontainer/`, uso de `styles.css`. **Adapte, não copie por cima do que já funciona.**
- `../../202601/BasesIV_EngSoft_BD/` — livro de Banco de Dados, geração anterior (R + `renv`, sem container). Vale pelo `atividades/`. **Cuidado:** lá os caminhos de dados são relativos ao arquivo (`../../dados/`); aqui são relativos à raiz. Não copie esse padrão.
