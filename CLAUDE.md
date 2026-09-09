# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Estado atual

Três specs governam este repositório, e as três precisam ser lidas antes de mexer na estrutura ou no código dos capítulos:

- `docs/superpowers/specs/2026-08-15-estrutura-livro-bases5-design.md` — a **estrutura** do livro (escopo, numeração, dados, infra). Carrega notas de correção pós-implementação; leia-as também, elas registram onde a decisão original mudou depois de escrita.
- `docs/superpowers/specs/2026-09-06-reescrita-numpy-design.md` — a **reescrita dos capítulos 6 a 17 em numpy**, decidida pelo autor e em curso na branch `reescrita-numpy`. Ela inverte, para esses capítulos, a decisão pedagógica original ("tudo em Python puro"). Ver "Pedagogia" e "A reescrita em numpy", abaixo.
- `docs/superpowers/specs/2026-09-08-pandas-nos-dados-design.md` — **`pandas` no trabalho com dados**, decidida pelo autor e **em curso na branch `pandas-nos-dados`**. Tira o `pandas` dos callouts e o põe no corpo do texto onde o assunto é obter, limpar, agrupar e apresentar dado, aproximando o livro do uso real. Não afrouxa nada sobre os algoritmos. Ver "Pedagogia" e "A conversão para pandas", abaixo.

Este arquivo é o resumo operacional; as specs são a fonte das decisões e das razões.

**O livro está escrito e publicado.** 17 capítulos, 87 seções + 17 `index.qmd` = 104 `.qmd`, todos registrados em `_quarto.yml`. Nenhum stub restante. Container Docker (Quarto + `uv`), CI publicando em `gh-pages`, 62 testes (`make teste`) guardando os invariantes. O **capítulo 9 (k-Vizinhos Mais Próximos)** foi o primeiro escrito e segue sendo o **modelo de estilo** da casa: leia `content/cap09/` antes de mexer em qualquer capítulo, para o formato pegar (ver "Antes de escrever um capítulo", abaixo).

Além do livro, `notebooks/` traz **um `.ipynb` por capítulo**, gerado a partir dos `.qmd` para executar ao vivo na aula (ver "Os notebooks de aula", abaixo), `atividades/` guarda o PID da disciplina, e `apoio/` traz páginas HTML interativas para projetar em aula (ver "`apoio/`", abaixo).

Os irmãos já prontos definiram o padrão da casa **na hora de montar o andaime**; agora servem como referência de convenção, não como fonte para copiar arquivo — a infra já existe aqui e já está adaptada:

- `../bases_3_estatistica/` — Quarto + Docker + `uv`, um `.qmd` por seção. Se uma dúvida de convenção não estiver resolvida aqui (formato de `Makefile`, padrão de `.devcontainer/`, uso de `styles.css`), é lá que a resposta provavelmente já foi pensada uma vez — mas adapte, não copie por cima do que já funciona.
- `../../202601/BasesIV_EngSoft_BD/` — livro de Banco de Dados, geração anterior (R + `renv`, sem container). Vale pelo `atividades/`: provas e trabalhos em `.qmd` que renderizam para PDF **fora** do projeto-livro, com gabarito via metadado + filtro Lua — ainda fora de escopo aqui. **Cuidado:** lá os caminhos de dados são relativos ao arquivo (`../../dados/`); aqui são relativos à raiz. Não copie esse padrão.

### A reescrita em numpy (branch `reescrita-numpy`)

**Os capítulos 6 a 17 estão sendo reescritos para construir os modelos com numpy**, um capítulo por vez. A branch `reescrita-numpy` já foi mesclada na `main`. Os capítulos 1 a 5 **não** mudam: eles continuam em Python puro e são a motivação do numpy — quem escreveu `dot` como um `sum` sobre um `zip` entende o que o `@` faz.

Estado: **6 a 13 concluídos** (planejados, implementados, revisados e corrigidos); 14 a 17 pendentes, com o mapa de cada um em `docs/superpowers/plans/2026-09-08-retomada-caps-14-17.md`. Cada capítulo tem um plano em `docs/superpowers/plans/2026-09-06-numpy-capNN.md` — o plano do capítulo é a memória do que foi decidido, medido e desviado ali, e é o primeiro lugar a olhar antes de mexer num capítulo já reescrito.

O processo, fixado em `docs/superpowers/plans/2026-09-06-numpy-00-instrucoes.md`, é **um capítulo por vez**: um agente planejador (Opus, com o mapa do capítulo já no prompt) escreve o plano; um implementador o executa e verifica; um revisor lê o capítulo inteiro com uma única pergunta — *o texto condiz com o que foi reescrito?* — e devolve discrepâncias; o implementador corrige. Doze planejadores em paralelo estouraram o limite de sessão da API sem produzir nada; a sequência não é preferência de estilo, é o que cabe no orçamento.

Ao terminar os 17, falta um **passe de coerência global**: `content/cap01`, `content/cap04/index.qmd` e o callout de `content/cap04/01-vetores.qmd` (que ainda diz "a regra deste livro — nada de NumPy", e é o destino de links dos capítulos 6 e 7), o `index.qmd` da raiz, o `README.md`, este arquivo e uma nota de correção na spec de 2026-08-15.

### A conversão para pandas (branch `pandas-nos-dados`)

**Onde o assunto é *dado*, e não *modelo*, a ferramenta passa a ser o `pandas`** — spec de 2026-09-08, um capítulo por vez, no mesmo processo da reescrita em numpy (planejador Opus → implementador → revisor → correções), com os planos em `docs/superpowers/plans/2026-09-08-pandas-capNN.md`.

Estado: **fundação e capítulos 6 e 7 concluídos**. Faltam, na ordem da spec: 9 e 10 (leitura de arquivo real), 11, 12 e 13 (colunas nomeadas e as tabelas de resultado), 8 (o menor retrabalho), e 14 a 17 — que ainda não existem em numpy e **já nascem com as duas specs valendo juntas**.

`CAPITULOS_PANDAS`, em `tests/test_pandas.py`, cresce a cada capítulo convertido, no mesmo molde de `CAPITULOS_NUMPY`: um teste vermelho nunca significa "ainda não chegou a vez".

Três decisões dos capítulos 6 e 7 que os seguintes herdam, e que não devem ser redecididas:

- **A ordem da 6.1 é `csv` → `DataFrame` → `array`.** O módulo `csv` fica, encolhido, porque o `read_csv` só é convincente contra o laço que ele substitui; e o `np.loadtxt` fica no fim porque a 7.1 o cita nominalmente.
- **A fronteira é batizada em `### Do `DataFrame` para o array: a fronteira`**, no fim do bloco *De listas a arrays* da 7.1. Todo capítulo que ajusta modelo cita esse `###` e mostra a linha; nenhum reexplica.
- **"À mão uma vez, `pandas` ao lado, `pandas` daí em diante"** é o limite do capítulo 7, e o que impede a hipocrisia pedagógica. Onde um exemplo à mão sobrevive, **o texto diz por que** — o `max` por símbolo da 7.5 sobrevive para mostrar o que o `groupby` faz por baixo; o `scale`/`rescale` da 7.6 sobrevive porque deixar uma coluna constante em paz é decisão de modelagem, e `(df - df.mean()) / df.std()` a transforma em `NaN` sem avisar.

Duas armadilhas medidas, que valem para quem converter os próximos capítulos:

- **`pd.read_html` precisa de `flavor="bs4"`** neste projeto: o padrão é `lxml`, que não está no `uv.lock`. Sem o argumento, `ImportError` e render no chão. **Não instale `lxml` para contornar.**
- **`na_values=["n/a"]` é redundante** — `n/a` já está na lista padrão de marcadores nulos do `pandas`. O marcador que *não* está, e que o livro usa, é `N/D`: com ele a coluna inteira vira `object` e `Series.sum()` concatena strings em vez de somar, sem erro nenhum.

### Antes de escrever um capítulo

**Leia `content/cap09/` inteiro primeiro.** Foi o primeiro capítulo escrito e foi revisado por rodadas sucessivas até fixar a forma: abertura de seção, posição dos callouts, formato de citação (capítulo + título em itálico, nunca um número de seção do Grus), justificativa de semente em chunk estocástico, e o callout de fechamento em `scikit-learn`. Um capítulo novo que copiar essa forma economiza rodadas de revisão; um que reinventar a forma provavelmente repete um erro que o cap. 9 já pagou.

## Visão geral

**Quarto book** da disciplina *Bases 5 — Ciência de Dados*, do curso de **Ciência da Computação** da UnDF. Português brasileiro, exemplos em Python, publicado no GitHub Pages a cada push na `main`.

Livro-texto: Joel Grus — *Data Science from Scratch: First Principles with Python*, 2ª ed. (O'Reilly, 2019). Código original: <https://github.com/joelgrus/data-science-from-scratch> (MIT). O PDF do livro **não faz parte do repositório** — `*.pdf` está no `.gitignore`, então um clone novo não o tem. Quem trabalha aqui mantém uma cópia local na raiz do projeto; é dela que saem os títulos reais das seções e o texto que os capítulos citam.

**Identidade: Bases 5 abre as caixas-pretas que o aluno usou antes.** Ele já ajustou uma reta chamando uma função pronta; aqui descobre o que aquele `.fit()` fazia.

### A restrição que molda o texto inteiro

**A turma não cursou Bases 3 com este professor.** Cada aluno viu estatística com outro livro e outro tratamento. Portanto:

- **Nunca** faça referência específica a Bases 3 — nada de "como você viu com o `statsmodels`", nada de reaproveitar os dados brasileiros daquele livro. A referência é sempre genérica: *"você provavelmente já ajustou uma reta chamando uma função pronta"*.
- Pode-se assumir o **tema** (média, mediana, desvio padrão, correlação, normal, testes), nunca o **tratamento**.
- **Álgebra linear não pode ser assumida** — não é estatística. É por isso que o capítulo 4 do Grus entrou no escopo.

## Escopo e numeração

**17 capítulos: Grus 1, 2, 3, 4 e 8 a 20.** Fora: Grus 5–7 (Estatística, Probabilidade, Hipótese e Inferência), cobertos por qualquer Bases 3; e Grus 21–27, por corte de escopo.

A numeração é **sequencial de 1 a 17**. Os capítulos 1–4 batem com os do Grus; de 5 em diante **não batem**:

| Nosso | Grus | Título | Seções |
|---|---|---|---|
| 1 | 1 | Introdução | 3 |
| 2 | 2 | Um Curso Rápido de Python | 6 (agrupados de 27) |
| 3 | 3 | Visualizando Dados | 4 |
| 4 | 4 | Álgebra Linear | 2 |
| 5 | 8 | Gradiente Descendente | 6 |
| 6 | 9 | Obtendo Dados | 4 |
| 7 | 10 | Trabalhando com Dados | 8 |
| 8 | 11 | Machine Learning | 6 |
| 9 | 12 | k-Vizinhos Mais Próximos | 3 |
| 10 | 13 | Naive Bayes | 5 |
| 11 | 14 | Regressão Linear Simples | 3 |
| 12 | 15 | Regressão Múltipla | 8 |
| 13 | 16 | Regressão Logística | 5 |
| 14 | 17 | Árvores de Decisão | 6 |
| 15 | 18 | Redes Neurais | 4 |
| 16 | 19 | Deep Learning | 8 (agrupados de 12) |
| 17 | 20 | Clustering | 6 |

**Regra de citação: o Grus não numera as seções — o sumário dele traz só títulos —, então nenhum callout pode inventar um número de seção do Grus.** O callout cita o **capítulo** do Grus e o **título** (em itálico) da seção, exatamente como o Capítulo 9 faz: `Esta seção corresponde a *The Model*, do capítulo 12 de @grus2019.` Nunca "seção 12.2 de @grus2019" — essa seção não existe no livro-texto, e `test_nenhuma_secao_inventa_numero_de_secao_do_grus` falha se um padrão desses aparecer perto de `@grus2019`. No sistema de arquivos vale o **nosso** número: `content/cap09/` é k-Vizinhos, e referências como "seção 9.2" são legítimas quando apontam para este livro, não para o Grus.

**Total: 87 arquivos de seção + 17 `index.qmd` = 104 `.qmd`.**

Os capítulos 2 e 16 são os únicos que se afastam de "um `.qmd` por seção" — o 2 porque o Grus lista cada construção da linguagem como seção (27 delas, o que daria um sidebar maior que o resto do livro somado), o 16 porque metade das seções são exemplos que moram melhor junto do conceito que demonstram. Os agrupamentos exatos estão na spec. As seções do Grus viram `##` dentro dos arquivos agrupados, e o `toc-depth: 4` as mantém no índice lateral.

## Pedagogia

Cada seção **implementa o algoritmo**, como o Grus faz, e **fecha com um callout mostrando o equivalente em `scikit-learn`** — o fecho do arco "abrir a caixa-preta". O `scikit-learn` nunca aparece na implementação de uma seção, só no callout, sempre num bloco ```` ```python ```` que **não executa** (`test_nenhum_chunk_executavel_usa_sklearn` trava isso no livro inteiro).

O que muda de um capítulo para outro é a **calculadora**:

- **Capítulos 1 a 5: Python puro.** `Vector = List[float]`, `dot` é um `sum(...)` sobre um `zip`. Não "melhore" esse código — trocá-lo por `np.ndarray` ou por uma chamada de `sklearn` destrói exatamente o que esses capítulos existem para ensinar. O instinto é forte, porque o código é lento e verboso para padrões de produção; a lentidão é o preço da transparência, pago de propósito. O pacote `scratch/` (vendorizado, com hash travado em teste) é o desses capítulos.
- **Capítulos 6 a 17: numpy.** Vetores e matrizes são `np.ndarray`, produto escalar é `@`, somas sobre pontos viram reduções com `axis`, laços sobre os dados viram operações vetorizadas. O algoritmo continua sendo escrito por nós, linha a linha, no `.qmd`. O pacote `scratch_np/` (nosso, editável) é o desses capítulos.

**A regra que decide cada dúvida: numpy é a calculadora, não o modelo.** Numpy entra para fazer álgebra linear, broadcasting, reduções, indexação booleana e sorteio. O que o capítulo existe para ensinar — a regra de atualização do gradiente, o critério de partição da árvore, a votação do k-NN, a verossimilhança do Naive Bayes, os passos do k-means, a retropropagação — continua escrito à mão.

### `pandas` é a mesa de trabalho (spec de 2026-09-08)

**Onde o assunto é *dado*, e não *modelo*, a ferramenta é o `pandas`** — ler arquivo, tipar, limpar, juntar, agrupar, resumir, apresentar. É o que se faz no trabalho real, e escrever um leitor de CSV à mão não ensina ciência de dados: ensina *parsing*, e mal. A caixa-preta que esta disciplina abre é a do **modelo**.

O dado atravessa uma **fronteira explícita** para virar `ndarray` quando o modelo começa, e essa linha é conteúdo, não detalhe — é onde o aluno vê que o modelo não sabe o que é uma coluna chamada "amigos":

```python
X = df[["amigos", "horas_trabalho"]].to_numpy()   # a fronteira
beta = least_squares_fit(X, y, rng)               # daqui para a frente, numpy
```

| `pandas` (mesa de trabalho) | `numpy` (calculadora) |
|---|---|
| `read_csv`, `read_html`, `json_normalize` | a matriz `X` e o vetor `y` do modelo |
| `parse_dates`, `na_values`, `to_numeric(errors=...)`, `dropna` | toda a álgebra: `@`, `.T`, `solve`, `norm` |
| `groupby`, `agg`, `merge`, `resample`, `pct_change` | reduções e máscaras dentro do algoritmo |
| `describe`, `corr`, `value_counts`, as tabelas de resultado | o sorteio e os parâmetros ajustados |

**`pandas` não entra em `scratch_np/`** (os módulos recebem e devolvem `ndarray`, sempre), nem no dado não tabular (MNIST binário, imagem), nem em nada que seja trabalho de modelo disfarçado. O teste de desempate: *isto é trabalho de dado ou trabalho de modelo?*

Continuam proibidos na implementação, como sempre: `sklearn`, `scipy`, `np.polyfit` e `np.linalg.lstsq` (`np.linalg.solve` é permitido — mostra as equações normais em vez de escondê-las).

| Pode e deve | Não pode |
|---|---|
| `X @ w`, `X.T @ X`, `np.linalg.solve`, `np.linalg.norm` | `np.linalg.lstsq` **como** implementação (só como conferência, em callout) |
| `np.mean`, `np.std(ddof=1)`, `np.corrcoef`, `np.cov` | `np.polyfit` |
| `np.argmax`, `np.argsort`, `np.unique(return_counts=True)` | qualquer `sklearn.*` em chunk executável |
| `rng.permutation`, `rng.random`, `rng.normal`, `rng.integers` | `np.random.seed` global, `random` da stdlib |
| máscaras booleanas, `np.isin`, `np.where` | `scipy.*` (não é dependência declarada) |

A pergunta de desempate é: **o aluno ainda vê a fórmula?** `beta = np.linalg.solve(X.T @ X, X.T @ y)` mostra as equações normais; `np.linalg.lstsq(X, y)` esconde.

**Laços continuam existindo** onde o laço *é* o algoritmo: a iteração do gradiente descendente, as épocas de treino, a recursão da árvore, a repetição do k-means até convergir, a fusão par a par do clustering hierárquico. O que sai é o laço **sobre os pontos de dados** — esse vira uma operação de array.

**Onde cada ferramenta é apresentada ao leitor.** São três blocos, e um capítulo posterior **cita** o bloco em vez de reexplicar — e não usa vocabulário que o bloco não apresentou sem apresentá-lo ali mesmo:

- o callout de fechamento do capítulo 4 mostra `np.array`/`np.dot` de relance;
- **`## O DataFrame`, no meio da seção 6.1**, apresenta o `pandas`: `read_csv` com `parse_dates` e `na_values`, `head`, `dtypes`, `describe`, `Series`, seleção de coluna e de linha, `.loc`/`.iloc`, e a inferência de tipo como **heurística, não garantia**. A ordem da 6.1 é `csv` (o mecanismo) → `DataFrame` (o caminho) → `array` (o atalho para o modelo): o `read_csv` só é convincente contra o laço que ele substitui, e o `np.loadtxt` fica no fim porque a 7.1 o cita nominalmente;
- **`## De listas a arrays`, que abre a seção 7.1**, é a apresentação de verdade do array — forma e tipo, indexação e fatias, máscaras booleanas, broadcasting, `axis`, e o laço em Python que some — e fecha com **`### Do `DataFrame` para o array: a fronteira`**, onde `.to_numpy()` é batizado. É esse `###` que os capítulos 8 a 17 citam.

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
make notebooks-teste  # executa os 17 notebooks de ponta a ponta (demora)
make atividade FONTE= # gera as duas versões (aluno e gabarito) de uma atividade
make shell            # shell dentro do container
make check            # quarto check
make build            # reconstrói a imagem (após mudar Dockerfile ou uv.lock)
make lock             # regenera uv.lock após editar pyproject.toml
make clean            # remove _book/, _freeze/, .quarto/ e o lixo de render abortado
```

**`make teste` roda `pytest tests/`** — 62 testes em nove arquivos: `test_estrutura.py` (registro no `_quarto.yml`, caminhos de dados, citações, e os totais de 17 capítulos / 87 seções / 104 arquivos contra o `LIVRO` de `scripts/gerar-stubs.py`), `test_scratch.py` (o pacote vendorizado — inclusive um hash SHA-256 travando que `scratch/` continua verbatim upstream), `test_scratch_np.py` (os invariantes da reescrita em numpy, abaixo), `test_pandas.py` (os invariantes do `pandas` como mesa de trabalho — a fronteira `.to_numpy()`, o `csv` à mão só onde é lição, nenhum algoritmo pronto em chunk executável), `test_dados.py` (os seis conjuntos commitados), `test_freeze.py` (o cache envenenado), `test_gradiente.py` (toda subida de gradiente tem motivo registrado), `test_notebooks.py` (os notebooks de aula não podem defasar dos `.qmd`) e `test_atividades.py` (o gabarito não pode vazar para o site). É o que garante a regra "todo `.qmd` novo precisa ser registrado em `_quarto.yml`", abaixo — sem essa suíte, um arquivo esquecido no YAML só aparece quando alguém percebe a seção faltando no site publicado.

### Verificar um capítulo sem renderizar o livro

O `make render` é **serializado** e leva minutos; vários agentes disputando o lock não funciona, e editar um `.qmd` enquanto um render roda envenena o `_freeze/` (as duas seções adiante). Por isso quem escreve um capítulo **não renderiza**: verifica com os três comandos abaixo, e o render completo é feito uma vez, por quem coordena, ao fim de cada bloco de capítulos.

Há um `.venv/` na raiz (gitignorado, criado por `uv sync`) com o mesmo lock do container, e é nele que essa verificação roda — sem Docker, em paralelo, em segundos:

```bash
export MPLBACKEND=Agg PYTHONHASHSEED=0          # os mesmos ENV do Dockerfile
.venv/bin/python scripts/gerar-notebooks.py      # regenera os 17 notebooks (idempotente)
.venv/bin/python scripts/executar-secoes.py 11   # cada .qmd do cap. 11 num kernel PRÓPRIO
.venv/bin/python scripts/executar-notebooks.py cap11   # o capítulo inteiro num kernel só
.venv/bin/pytest tests/ -q
```

**`scripts/executar-secoes.py` é o análogo fiel do `quarto render` para um capítulo.** Ele reaproveita o parser de `gerar-notebooks.py` (que já sabe o que é callout e o que é `eval: false`), monta em memória um notebook só de código para **cada** `.qmd` e o executa num kernel novo, com o cwd na raiz — que é o que o `execute-dir: project` faz no Quarto. É assim que se pega o `import` que falta numa seção porque foi feito na anterior: o notebook de aula, com um kernel só para o capítulo inteiro, deixa isso passar. Não toca em `_freeze/` nem em `.quarto/`, então pode rodar em paralelo e nunca precisa do lock. O alvo `make secoes CAP=NN` roda o mesmo script dentro do container.

Os dois modos são complementares e ambos importam: `executar-secoes.py` reproduz o **site** (um kernel por página), `executar-notebooks.py` reproduz a **aula** (um kernel por capítulo).

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

Este livro é escrito por agentes, e mais de um pode estar ativo. Dois `quarto render` simultâneos sobre o mesmo `_freeze/` corrompem o cache: um grava a saída congelada de um chunk enquanto o outro lê o índice, e o livro sai com saída trocada entre páginas — **sem erro nenhum na tela**. É a pior classe de falha deste projeto, silenciosa e difícil de atribuir.

A reescrita em numpy tirou a pressão daqui, e vale manter a prática: quem escreve um capítulo verifica com `scripts/executar-secoes.py`, que não toca no `_freeze/`, e **só quem coordena renderiza**, uma vez por bloco de capítulos. Render em fila é o sintoma de que o trabalho está organizado errado, não um problema a contornar.

O alvo `render` toma um lock antes de começar. Se outro render estiver rodando, ele imprime `outro render em andamento neste repositório; aguardando a vez...` **uma vez** e espera, pegando a vez sozinho. Isso é comportamento normal: **não interrompa, não contorne, não mate o processo.**

Detalhes que importam se você for mexer nisso:

- O lock é um `mkdir` (`.render-lock/`, gitignorado), porque `mkdir` é atômico em qualquer POSIX. `flock` **não existe no macOS de fábrica** — foi por isso que não foi usado.
- Um `trap ... EXIT INT TERM` devolve o lock mesmo se o render abortar ou levar Ctrl-C.
- Depois de 30 minutos esperando, o lock é considerado preso (agente morto) e removido com aviso. Um agente que morreu não pode bloquear o livro para sempre.
- `make offline` **não** pega o lock: ele apaga o `_freeze/` de propósito e é rodado deliberadamente antes de publicar, não em paralelo com escrita.
- **A espera é limitada a ~7 minutos, e o motivo não é o render.** A ferramenta de shell dos agentes aborta em 10 minutos; uma espera ilimitada estouraria esse teto e devolveria um timeout opaco, sem dizer se o livro quebrou, se o lock travou ou se era só a vez de outro. **Isso já custou um capítulo entregue sem verificação.** Passado o limite, o alvo imprime `NÃO RENDERIZOU — a vez ainda é de outro agente` e sai com **75** (`EX_TEMPFAIL`): a instrução é rodar `make render` de novo, não investigar. Um lock parado há mais de 30 minutos é considerado órfão e removido.

**Consequência prática de coordenação: não deixe mais de dois ou três agentes que precisem renderizar trabalhando ao mesmo tempo.** Cada render leva alguns minutos, e a fila cresce mais rápido que a paciência da ferramenta.

**Nunca edite `scripts/render-seguro.sh` (nem qualquer `.sh`) enquanto um agente pode estar rodando.** O bash lê o script **incrementalmente**, conforme executa — editar o arquivo no meio faz o interpretador perder a posição e estourar num erro de sintaxe que não existe, tipicamente `syntax error near unexpected token 'done'`. Isso já derrubou o render de um agente, que gastou tempo investigando um defeito que não era dele nem do conteúdo.

Se precisar mudar o script com agentes ativos, escreva num arquivo temporário e mova por cima (`mv` é atômico, e o bash em execução continua lendo o inode antigo). Editar direto só quando ninguém estiver renderizando.

### O `_freeze` envenenado — a falha mais silenciosa deste projeto

**Sintoma:** o `.qmd` está certo, o `make render` diz `render OK`, e a página publicada em `_book/` continua mostrando a versão antiga. Rodar `make render` de novo não muda nada. Nenhum erro, nenhum aviso.

**Causa:** o `freeze: auto` guarda, para cada arquivo, o par *(hash do fonte, markdown executado)*. Se alguém **edita o `.qmd` enquanto o render roda**, o Quarto executa a versão velha e grava esse resultado velho junto com o hash da versão **nova**. Dali em diante o hash bate, o cache é considerado válido, e aquele arquivo **nunca mais reexecuta sozinho**.

Isto não é hipótese: já publicou três seções desatualizadas do capítulo 10 e uma do capítulo 7, e passou por um render inteiro sem uma linha de aviso. Foi encontrado só porque um revisor comparou o fonte com o HTML linha a linha.

**Não dá para detectar comparando hashes** — o hash bate; é exatamente esse o problema. O que se detecta é a *causa*: um `.qmd` cuja data de modificação mudou entre o começo e o fim do render.

**O `scripts/render-seguro.sh` faz isso automaticamente.** Ele fotografa os mtimes antes e depois, e se algum arquivo mudou no meio, apaga o `_freeze` só desses e renderiza de novo (até 3 rodadas). Se ainda assim houver edição concorrente, ele avisa em caixa alta, nomeia os arquivos e **sai com sucesso** — porque o render funcionou, e um agente que vê "falha" tende a rodar `make clean`, que é o remédio errado.

**Se você desconfiar de uma página específica**, o remédio manual é `make refresh CAP=NN` — apaga o `_freeze/` só daquele capítulo e renderiza. Nunca `make clean`.

**Não escreva `#| cache: true` num chunk.** Esse é o cache por-célula do motor **knitr** (R) e não existe para o motor **Jupyter**, que é o deste livro (`jupyter: python3`) — a opção é silenciosamente ignorada. O Jupyter tem um cache próprio, o *Jupyter Cache*, mas ele funciona por **notebook inteiro** (qualquer célula mudar reexecuta todas) e depende do pacote opcional `jupyter-cache`, que não está no `uv.lock` deste projeto. Na prática, o `freeze: auto` já resolve o que interessa aqui — por **arquivo** `.qmd`, sem depender de nenhum pacote extra — então é nele que os capítulos devem confiar, não em `cache:`.

## Arquitetura

### Estrutura de conteúdo

Um diretório por capítulo, um `.qmd` por seção:

```
content/cap09/
├── index.qmd                          # Visão geral + objetivos + tabela de seções + Leituras adicionais
├── 01-o-modelo.qmd
├── 02-exemplo-o-dataset-iris.qmd
└── 03-a-maldicao-da-dimensionalidade.qmd
```

**Todo `.qmd` novo precisa ser registrado em `_quarto.yml`** sob `book.chapters` — arquivo não listado não aparece no livro. A ordem vem do YAML, não do nome do arquivo; para reordenar, `git mv` e atualize o YAML na mesma operação. `make teste` verifica isso: `test_todo_qmd_esta_registrado_no_quarto_yml` (e o teste que confere os totais contra o `LIVRO`) falham se um `.qmd` existir sem entrada no YAML.

"For Further Exploration" fecha quase todo capítulo do Grus. Não vira arquivo: vira uma seção *Leituras adicionais* no fim do `index.qmd` do capítulo.

**Duas exceções, ambas conferidas no PDF e já codificadas no `LIVRO` de `scripts/gerar-stubs.py`:** o capítulo 16 do Grus (o nosso 13, Regressão Logística) fecha com "For Further **Investigation**", e o capítulo 1 não tem seção de leituras — termina em "Onward". Duas revisões independentes já apontaram o "Investigation" como inconsistência a uniformizar; **não é.** O comentário no gerador avisa isso na fonte.

### Os notebooks de aula — derivados do livro, nunca editados à mão

`notebooks/` tem **um `.ipynb` por capítulo**, para executar ao vivo na aula. Eles são gerados por `scripts/gerar-notebooks.py` a partir dos `.qmd`, e a relação é a mesma do `scratch/` com o upstream: **o livro é a fonte, o notebook é cópia derivada.** Editar um `.ipynb` é trabalho perdido — o próximo `make notebooks` sobrescreve. Mudou a aula? Mude o `.qmd`.

`test_notebooks_estao_atualizados` regera cada notebook em memória e compara com o arquivo em disco, então um `.qmd` que anda sem o notebook derruba `make teste`. É o guarda contra a falha óbvia: a aula rodando uma versão do capítulo que o site publicado já não tem.

**Os 19 chunks dentro de callouts.** No livro, 19 chunks `{python}` que **executam** moram dentro de `::: {.conceito}`, `::: {.exemplo}` e afins. Um conversor que trate todo `:::` como texto os transforma em markdown — e aí o notebook abre, executa, e quebra várias células adiante num `NameError` que não aponta para a causa. O gerador converte o corpo do callout recursivamente: o que é prosa vira blockquote, o que é código continua célula de código. `test_todo_chunk_executavel_do_livro_virou_celula` conta os chunks de forma independente do gerador e trava isso.

Três traduções que o gerador faz porque o Jupyter não entende o que o Quarto entende:

- **Callouts** viram blockquotes com rótulo e ícone.
- **Links entre `.qmd`** viram URLs absolutas do site publicado — um caminho relativo a `../cap05/index.qmd` não resolve de dentro de `notebooks/`.
- **Citações `@grus2019`** viram o texto da citação, com a bibliografia numa célula final. As referências saem do `references.bib`, para não existir uma segunda cópia.

**A célula de preparo.** No livro, `execute-dir: project` põe o cwd na raiz, e é isso que faz `from scratch...` e `dados/...` resolverem. O notebook não tem esse mecanismo, então a primeira célula de código de todo notebook sobe os diretórios até achar `_quarto.yml` e faz `os.chdir`. Funciona tanto com o Jupyter aberto na raiz quanto dentro de `notebooks/`.

**Os arquivos entram no git sem saída de execução**, de propósito: quem executa é o aluno. Saída congelada tornaria o diff ruído binário e tiraria o sentido de rodar o código. `test_nenhum_notebook_guarda_saida` trava isso.

**Uma diferença de execução em relação ao livro, que vale conhecer:** no site, cada `.qmd` roda no **seu próprio kernel** e nomes não atravessam páginas — daí os `import` se repetirem de seção para seção. No notebook, o capítulo inteiro roda num kernel só. Na prática só ajuda (a ordem de leitura é a mesma), mas é a razão de um notebook poder executar uma célula que, isolada, faltaria um import.

**O Colab é o ambiente de aula, e é ele que dita a célula de preparo.** Cada `index.qmd` de capítulo traz, logo abaixo do callout de correspondência, um link `colab.research.google.com/github/.../notebooks/capNN-*.ipynb`. No Colab não existe cópia do projeto: `scratch/` e `dados/` não estão lá, e a busca pelo `_quarto.yml` subindo diretórios não acha nada. Por isso a célula de preparo, além do `chdir`, **clona o repositório** quando não encontra o projeto — `git clone --depth 1` num `/content/bases5`. Sem isso, todo notebook quebraria na primeira célula quando aberto no Colab, que é justamente como o aluno vai abri-lo.

O link é do site para o notebook e **não** o contrário: `LINHA_COLAB`, no gerador, remove a linha do Colab ao converter o `index.qmd`, porque dentro do notebook ela mandaria o leitor abrir o notebook em que ele já está. `test_todo_capitulo_tem_link_para_o_colab_e_nenhum_notebook_o_repete` trava os dois lados.

**O onboarding do Colab vive em `scripts/onboarding-colab.md` e entra só no notebook do capítulo 2** — a aula 2 é a primeira em que a turma põe a mão no ambiente. Ele explica Shift+Enter, a armadilha da ordem de execução, o `assert` como idioma da casa, a semente obrigatória e o "salvar cópia no Drive". **Não está no livro de propósito:** explicar Shift+Enter numa página HTML seria comentário sobre a ferramenta, e não sobre o conteúdo — exatamente a classe de texto que a revisão de bastidor tirou do livro. Um teste confere que ele está no notebook e que não vazou para `content/`.

**Verificação:** `make notebooks-teste` executa os 17 de ponta a ponta com o cwd em `notebooks/` — o caso mais apertado. É o análogo do `quarto render` para os notebooks, e pelo mesmo motivo: os módulos de `scratch/` têm `assert` no nível do módulo. Demora — medido: **~11 minutos no total**, dominado pelo cap. 16 (MNIST, 343 s) e pelo cap. 12 (bootstrap, 157 s). Não roda no CI por isso; é alvo deliberado.

`notebooks/` está no **`.quartoignore`** — sem isso o Quarto trataria os `.ipynb` como conteúdo do livro.

### `apoio/` — páginas interativas de aula, servidas junto do livro

`apoio/` guarda páginas HTML autônomas para usar **ao vivo na aula**, ao lado do slide e do notebook. Hoje são duas, as duas do capítulo 5:

- **`gradiente-descendente.html`** (seções 5.1 a 5.4) — o aluno escolhe a função, mexe no tamanho do passo e vê, a cada iteração, a derivada, o passo e o rastro; em uma variável e em duas, com contorno e superfície 3D lado a lado.
- **`lote-minibatch-estocastico.html`** (seção 5.6) — os três métodos treinando ao mesmo tempo na regressão da seção 5.5, com a perda (log-log) e a reta ajustada em dois painéis simultâneos. **Um interruptor troca o que o relógio conta**, e é aí que mora a lição: em *chamadas a `gradient_step`* os três gastam o mesmo e os epochs saem diferentes (5.000 / 1.000 / 50), com o estocástico sete ordens de grandeza atrás; em *epochs* os três dão o mesmo número de passadas e o gasto sai diferente (1.200 / 6.000 / 120.000 chamadas), e aí o estocástico parece ganhar de longe. A mesma corrida, duas conclusões opostas, conforme a coluna que se decide manter fixa.

  Trocar de modo também troca a granularidade do registro: em *epochs* a perda é medida uma vez por epoch, isto é, só nas **fronteiras** — onde a cascata do estocástico já se autocorrigiu. Por isso o serrilhado some ao virar o interruptor, e isso não é bug: é a observação que a própria seção faz ao medir "só nas fronteiras de epoch".

**São arquivos estáticos, não conteúdo do livro.** Um HTML só, sem build, sem dependência de rede, que abre com dois cliques e roda offline. Não têm `.qmd`, não entram no `book.chapters` e não aparecem no sidebar — o que os leva ao site é uma linha em `project.resources`, no `_quarto.yml`, que o Quarto copia para `_book/apoio/`. Sem essa linha, a página existe no repositório e **não** existe no site publicado.

As duas dividem tokens, tipografia e componentes de propósito — são irmãs, e uma terceira página deve copiar o mesmo bloco `:root` em vez de inventar outro.

Quatro decisões que não são óbvias e custam tempo a redescobrir:

- **O link no capítulo é relativo, e vira absoluto só dentro do notebook.** As duas pontas pedem coisas opostas e as duas falham em silêncio: com URL absoluta no `.qmd`, o `make preview` manda o leitor para o site publicado em vez da cópia local que ele está olhando; com caminho relativo no notebook, o link não resolve, porque de `notebooks/` (ou do Colab) nenhum caminho do livro resolve. Por isso `reescreve_links`, em `scripts/gerar-notebooks.py`, reescreve **todo** link relativo para a URL do site — não só os `.qmd`, como fazia antes —, e o que é específico do `.qmd` passou a ser apenas trocar a extensão. `test_link_de_apoio_e_relativo_no_qmd_e_absoluto_no_notebook` trava os dois lados.
- **`apoio/` não entra no `.quartoignore`**, e a tentação existe (`notebooks/` está lá). Aqui seria contraproducente: o `.quartoignore` tira arquivos do projeto, e é justamente o projeto que precisa enxergar `apoio/` para copiá-lo como recurso. A proteção que `notebooks/` precisa não se aplica — o Quarto só trata `.qmd`, `.md` e `.ipynb` como entrada, e não há nenhum desses aqui.
- **`test_quarto_publica_apenas_o_diretorio_publico` não barra isto.** O teste casa só entradas de `resources` que começam com `atividades`, porque o que ele guarda é o gabarito. Recurso fora de `atividades/` passa — o que é o comportamento certo, mas parece proibido à primeira leitura do teste.
- **Editar o `index.qmd` de um capítulo obriga a rodar `make notebooks`**, senão `test_notebooks_estao_atualizados` derruba a suíte. Vale para o link de `apoio/` como vale para qualquer outra linha.

`test_toda_pagina_de_apoio_esta_publicada_e_linkada_certo` varre `apoio/` inteiro e cobra as três primeiras: recurso declarado, link relativo no `.qmd`, URL absoluta no notebook. Página nova entra na varredura sozinha — não é preciso editar o teste.

**A paleta sai do livro e do logo.** O fundo e o texto são os do tema `cosmo`, o mesmo do livro em modo claro (`#FFFFFF`, `#373A3C`); os azuis são amostrados de `images/logo-undf.png` — `#2264AF`, `#4195D1`, `#8FCEF1` e o navy `#27316E`. Eles vestem a paisagem inteira: curvas de nível, malha 3d, curva de `f`, aba ativa, botão principal. A trajetória é a única coisa quente da página, e isso é decisão, não descuido: a marca é toda azul, e um rastro azul sobre um mapa azul sumiria justamente no que mais importa de ver. O laranja é o complementar daqueles azuis. A regra de leitura da página é essa — **azul é o terreno, laranja é a descida** —, e quem mexer nas cores deve mantê-la.

**O que é reprodutível dígito a dígito, e o que não é.** Na página da seção 5.6, o lote inteiro e o estocástico não embaralham nada: basta fixar o `theta` inicial de `random.seed(0)` e `random.seed(2)` como constante — está no topo do arquivo, com a origem escrita — e o resto é determinístico, então as duas curvas reproduzem os laços do livro exatamente (medido: lote com MSE `4,107 × 10⁻⁸` e estocástico com `0,3394` e `theta = [20.0100, 4.4998]` em 5.000 chamadas, contra os `4,1 × 10⁻⁸` e `0,34` da seção). O minibatch embaralha, e o Mersenne Twister do Python não existe no navegador: a curva dele bate em comportamento, não em número, **e a página diz isso ao leitor** em vez de deixar parecer exata.

**Os números da página são conferidos contra o Python, não estimados.** A superfície de erro quadrático médio usa os dados da seção 5.5 (`inputs = [(x, 20*x + 5) for x in range(-50, 50)]`) em forma fechada — média(x) = −0,5 e média(x²) = 833,5 —, e a trajetória bate dígito a dígito com o laço do livro: no passo 5, inclinação 22,5464 e intercepto 0,5475. As faixas de α de cada função foram medidas antes de escrever a página, e é isso que faz os presets ensinarem o que prometem (o poço duplo fica preso até α ≈ 0,15, escapa entre 0,17 e 0,25, e não assenta acima de 0,29). Mexeu na função ou no passo? Meça de novo — um preset que não faz o que o rótulo diz é pior que preset nenhum.

### O pacote `scratch/` — vendorizado literalmente, nunca editado

Cópia fiel do repositório do Grus (MIT, licença preservada). **Toda adaptação vive no `.qmd`, nunca no pacote** — assim um `diff` contra o upstream continua limpo.

Com `execute-dir: project`, o cwd de todo chunk é a raiz e `from scratch.linear_algebra import dot` resolve sem `PYTHONPATH` — que é o problema que o README do Grus manda o leitor resolver à mão.

Cada módulo tem um `if __name__ == "__main__":` com a demonstração do capítulo; ele não roda no import. Se o texto precisa daquele exemplo, chame as funções explicitamente no chunk.

**Dois efeitos colaterais verificados no código, e dois módulos que nunca são importados.**

**1. Importar alguns módulos desenha gráficos, e um escreve arquivo.** Chamadas `plt.*` no nível do módulo: `statistics.py` (5), `probability.py` (18), `working_with_data.py` (8), `visualization.py` (63).

A correção **não** é editar o pacote: é criar `im/` vazio, como o Grus tem no dele. Chunks que importam desses módulos vão com `include: false` e `plt.close('all')` na sequência, senão a figura do import vaza para a saída da célula.

**`visualization.py` é o caso mais sério: nove `plt.savefig('im/viz_*.png')` no corpo do módulo**, um para cada figura do capítulo (`viz_gdp`, `viz_movies`, `viz_grades`, `viz_misleading_y_axis`, `viz_non_misleading_y_axis`, `viz_line_chart`, `viz_scatterplot`, `viz_scatterplot_axes_not_comparable`, `viz_scatterplot_axes_comparable`). Nenhum `.qmd` ainda importa esse módulo — ele é do capítulo 3, hoje stub —, então isso ainda não aconteceu. Mas assim que o capítulo 3 for escrito, todo `import scratch.visualization` vai gravar esses nove arquivos em `im/` a cada render, inclusive local. O `.gitignore` já tem a regra (`im/*` ignorado, exceto `.gitkeep`) para que isso não seja varrido para um commit por um `git add` amplo — mas quem escrever o capítulo 3 deve saber que os PNGs vão aparecer no disco de qualquer forma.

**2. `getting_data` e `working_with_data` nunca são importados — cada um por um motivo diferente, e nenhum se corrige editando o pacote:**

- **`getting_data.py:90`** faz `requests.get` no corpo do módulo — importar dispara rede. Nenhum outro módulo o importa, então basta não importá-lo: o capítulo 6 (que *é* esse módulo) escreve os chunks direto, lendo o HTML vendorizado. O código do Grus continua visível e citável, sem ser executado por acidente.
- **`working_with_data.py:148`** abre `stocks.csv` com um caminho relativo ao **cwd** no corpo do módulo — o upstream do Grus mantém esse arquivo na raiz do repositório dele; na nossa convenção, dado vive em `dados/`, então o `open()` estoura com `FileNotFoundError`. E as linhas 28–30 calculam `xs`, `ys1`, `ys2` com `random.random()` **sem semente**, enquanto as linhas 48–49 afirmam `0.89 < correlation(xs, ys1) < 0.91` — o valor real (~0,894) encosta na borda dessa janela, e o `assert` falha em **cerca de 25% das execuções** — duas medições independentes de 20.000 rodadas deram 25,0% (5.006 falhas) e 24,6%. A diferença entre as duas é de pouco mais de um erro padrão (~0,3 pp), então o número honesto é "cerca de uma em quatro", não a terceira casa. Vendorizar `stocks.csv` na raiz não resolve nada disso: a asserção sem semente continua sendo cara ou coroa a cada import.

> Uma versão anterior deste arquivo dizia "cerca de 1 vez em 3, medido em 5 rodadas", e citava as linhas erradas para a geração. Cinco rodadas não distinguem 25% de 33%. O número acima vem de 20.000 execuções, e foi confirmado de forma independente por dois agentes. Fica como lembrete: **amostra pequena demais é o mesmo que chute com aparência de medição** — que é, aliás, a lição do capítulo 8 deste livro.

`tests/test_scratch.py`'s `NAO_IMPORTAVEIS` documenta os dois motivos e trava com um teste que a exclusão precisa vir com motivo escrito. Consequência de conteúdo: os capítulos **7** (que *é* o módulo `working_with_data`) e **13** (que precisaria de `rescale`/`scale` de lá) não importam `working_with_data` — escrevem essas funções **inline no `.qmd`**, exatamente como o capítulo 6 já faz com o código de `getting_data`.

### O pacote `scratch_np/` — o código dos capítulos 6 a 17, em numpy

Contraparte em arrays do `scratch/`, e o oposto dele em quase tudo: é **nosso**, editável, sem hash travado, testado em `tests/test_scratch_np.py`. Espelha os módulos do Grus **com os mesmos nomes de função** sempre que a função existe nos dois lados — assim o aluno acha no livro-texto a versão em listas do que está lendo em arrays.

| Módulo | Dono | Conteúdo |
|---|---|---|
| `gradient_descent.py` | andaime | `gradient_step`, `minibatches` (gera arrays de índices) |
| `machine_learning.py` | cap. 8 | `split_data`, `train_test_split`, `accuracy`, `precision`, `recall`, `f1_score` |
| `probability.py` | andaime | `normal_cdf`, `inverse_normal_cdf` (vetorizadas) |
| `statistics.py` | andaime | os dados da DataSciencester como arrays |
| `working_with_data.py` | cap. 7 | `scale`, `rescale`, `de_mean`, `pca`, `transform`, ... |
| `k_nearest_neighbors.py` | cap. 9 | `majority_vote`, `knn_classify`, `random_distances` |
| `naive_bayes.py` | cap. 10 | `tokenize`, `Message`, `NaiveBayesClassifier` |
| `simple_linear_regression.py` | cap. 11 | `least_squares_fit`, `total_sum_of_squares`, `r_squared`, ... |
| `multiple_regression.py` | cap. 12 | `inputs`, `least_squares_fit`, bootstrap, `p_value`, ridge, lasso |
| `logistic_regression.py` | cap. 13 | `logistic`, `negative_log_likelihood`, `negative_log_gradient` |

Faltam os dos capítulos 14 a 17 (`decision_trees`, `neural_networks`, `deep_learning`, `clustering`), que entram com os capítulos.

**`pandas` não entra aqui.** Os módulos recebem e devolvem `np.ndarray`, sempre — é o contrato dos capítulos entre si, e um `DataFrame` tornaria o algoritmo dependente de nomes de coluna. Os módulos que reexportam dados podem expor um `DataFrame` **ao lado** do array (o `DataFrame` é o que o capítulo mostra; o array é o que o modelo recebe).

**Não existe `linear_algebra` aqui, de propósito:** ele *é* o numpy — `dot` é `@`, `distance` é `np.linalg.norm(a - b)`, `vector_mean` é `X.mean(axis=0)`.

**A única importação permitida de `scratch/` é de DADOS, nunca de função.** As listas hard-coded do Grus (`statistics.num_friends`, `multiple_regression.inputs`, `logistic_regression.data`, `decision_trees.inputs`) são reexportadas como arrays pelo módulo correspondente; importar o módulo do Grus desenha figuras no nível do módulo, então o reexportador faz `plt.close("all")` em seguida. `REEXPORTA_DADOS`, em `tests/test_scratch_np.py`, exige o motivo escrito de cada uma dessas exceções — o mesmo padrão de `NAO_IMPORTAVEIS`.

**"A seção implementa, a próxima importa."** Cada `.qmd` roda no seu próprio kernel, então a seção que ensina o algoritmo o escreve inline num chunk, e as seções (e capítulos) seguintes importam **o mesmo código** de `scratch_np/`. O código do módulo e o do chunk são idênticos — o módulo é o chunk salvo em arquivo. Quando o texto diz *"não é redefinida aqui: vem de `scratch_np.k_nearest_neighbors`, o mesmo código que você escreveu na seção anterior"*, isso precisa ser verdade, e os revisores conferem caractere a caractere.

Convenções de array, seguidas por todos os módulos e chunks:

- `X` tem forma `(n, d)` — uma linha por observação; `y` tem `(n,)`; parâmetros (`beta`, `theta`, `w`) têm `(d,)`; um único ponto é `(d,)`.
- `dtype=float` explícito ao construir array a partir de dado lido.
- Anotações de tipo usam `np.ndarray` direto — sem alias `Vector`.
- Onde o Grus usa a fórmula amostral (variância, desvio padrão), `ddof=1`.
- Funções escalares devolvem `float(...)`, para a saída da célula não vir como `np.float64(...)`.

### Dependência dos capítulos fora da ementa

Tirar os Grus 5 e 6 da ementa não tira o código deles do caminho:

| Módulo | Quem depende |
|---|---|
| `scratch/statistics.py` (Grus 5) | os **dados** da DataSciencester, reexportados por `scratch_np/statistics.py` → capítulos 7, 11, 12 |
| `scratch/probability.py` (Grus 6) | `normal_cdf` / `inverse_normal_cdf`, reescritas em `scratch_np/probability.py` → capítulos 7, 12, 16 |

`scratch/statistics.py` carrega `num_friends_good` e `daily_minutes_good` — o dataset da rede social —, e os capítulos 11 e 12 fazem regressão em cima dele. Depois da reescrita a dependência ficou **indireta** (o capítulo importa de `scratch_np/`, que reexporta como array), mas não sumiu.

Consequência: `scratch/` é vendorizado **inteiro**, incluindo os módulos fora da ementa. Podar o pacote quebra o livro — e agora quebra por dois caminhos, o dos capítulos 1 a 5 e o dos reexportadores.

### Dados

**Os dados do Grus são mantidos como estão**, inclusive a rede social fictícia DataSciencester, que é o fio narrativo do livro. Não há localização para dados brasileiros: sem um Bases 3 comum, o reencontro com um dataset específico não existiria para boa parte da turma.

Fidelidade ao dado, **não** à forma de obtê-lo — **nenhum byte vem da rede em tempo de render.** Os seis conjuntos entram commitados em `dados/` (~13 MB); o inventário e a razão de cada um estão na spec. O caso que mais surpreende: do corpus SpamAssassin entram **só os assuntos**, como CSV, porque o `naive_bayes.py` lê cada e-mail e descarta tudo menos a linha `Subject:`.

**Caminhos a partir da raiz**, sempre:

```python
acoes = pd.read_csv("dados/stocks.csv")        # ✓
acoes = pd.read_csv("../../dados/stocks.csv")  # ✗ nunca
```

### Sementes em chunks estocásticos — obrigatório

`train_test_split`, inicialização de pesos, k-means, gradiente estocástico: metade do livro é aleatória. **Todo chunk com RNG usa semente explícita**, e a forma depende do capítulo:

```python
random.seed(42)                        # capítulos 1 a 5 (o Grus usa o random da stdlib)
rng = np.random.default_rng(42)        # capítulos 6 a 17
```

Sem isso, cada render produz números e gráficos diferentes: o `freeze` perde o sentido, o diff do site publicado vira ruído, e o material deixa de bater com o que o aluno vê na tela.

Nos capítulos reescritos, o gerador é **explícito e passado adiante**: toda função estocástica de `scratch_np/` recebe `rng: np.random.Generator` como parâmetro **obrigatório**, sem valor padrão, para a semente ficar visível no chunk de quem chama. Nunca `np.random.seed(...)` (estado global) nem `random` da stdlib — `test_capitulo_numpy_usa_default_rng` falha se aparecerem, e uma exceção deliberada precisa de motivo escrito em `RANDOM_PERMITIDO`.

**Semear um gerador e sortear de outro é um jeito silencioso de achar que fixou a aleatoriedade sem ter fixado.** `random.seed` não tem efeito nenhum sobre o `numpy.random`, e nenhum dos dois é escutado pelo `scikit-learn`, que tem o próprio `random_state`.

**Sorteio novo, número novo.** `random.seed(12)` com `random.shuffle` e `default_rng(12).permutation` produzem divisões diferentes. Toda afirmação do texto que dependia de um sorteio específico — uma matriz de confusão, uma acurácia, um coeficiente de bootstrap — é **recalculada a partir da saída nova**, nunca copiada da versão anterior. Foi a principal fonte de trabalho de revisão da reescrita.

### Ambiente

Duas camadas travadas: `pyproject.toml` + `uv.lock` fixam as versões; o `Dockerfile` consome esse lock (`uv sync --frozen`) sobre um SO fixo com Quarto e locale `pt_BR.UTF-8`. O mesmo container renderiza local e no CI.

Dependências (a lista completa e comentada está na spec): `jupyter`, `matplotlib`, `numpy`, `pandas`, `tqdm`, `requests`, `beautifulsoup4`, `html5lib`, `python-dateutil`, `pillow`, `scikit-learn` e `pytest`. **`pandas>=2,<3` é dependência direta desde a spec de 2026-09-08**, e o teto `<3` não é burocracia: é o pandas 3 que quebrou dois exemplos do livro irmão sem levantar exceção.

**`numpy` é dependência direta desde a reescrita dos capítulos 6 a 17**, e o teto é `<3`. Antes ele estava instalado assim mesmo, como dependência transitiva do matplotlib e do scikit-learn, mas ficava deliberadamente fora do `pyproject.toml` — a ausência era o sinal de que não era ferramenta da disciplina. Deixou de ser: a partir do capítulo 6 os modelos são construídos com arrays, e o pacote precisa estar declarado e travado como qualquer outro. Os capítulos 1 a 5 continuam sem ele.

O `scikit-learn` é **nosso**, não do livro — entra só pelos callouts de caixa-preta, e nunca em chunk que executa. Os pacotes `mnist` e `twython` do `requirements.txt` do Grus ficam de fora: o primeiro só serve para baixar dataset que será lido do disco, o segundo depende de uma API do Twitter que não é mais gratuita. `scipy` **não** é dependência declarada — não use em implementação, mesmo que ele apareça instalado como transitiva do scikit-learn.

Dois detalhes herdados, já pagos no Bases 3:

- O venv fica em **`/opt/venv`**, não em `/livro/.venv`. O `compose.yaml` faz bind mount do projeto sobre `/livro`, o que apagaria um venv que estivesse ali.
- O `Dockerfile` grava `/etc/profile.d/venv.sh` reexportando o `PATH`. Um shell de **login** recarrega `/etc/profile`, que reescreve o `PATH` e descartaria o `ENV PATH` da imagem — fazendo `python` cair no interpretador do sistema. Se `make shell` resolver o Python errado, é o primeiro lugar a checar.

`MPLBACKEND=Agg` é obrigatório: sem display, o matplotlib estoura ao importar.

**`PYTHONHASHSEED=0` também é obrigatório, e o motivo é sutil.** `scratch/naive_bayes.py:113` tem, no nível do módulo, um `assert` de igualdade **exata** de float sobre uma soma que percorre um `Set[str]`. A ordem de iteração de um `set` depende do hash das strings, que o Python randomiza por processo, e soma de ponto flutuante não é associativa — então a ordem muda o último bit e o assert falha. Medido neste container: **2 de 15 sementes falham no import; com `PYTHONHASHSEED=0`, 15 de 15 passam.**

Isso torna instável qualquer coisa que importe aquele módulo — hoje, a suíte de testes. A correção fica no `Dockerfile`, não em `scratch/`, porque o pacote é vendorizado literalmente e nunca editado: é propriedade do ambiente, e combina com a postura do livro de fixar semente em todo chunk estocástico.

**Não afrouxe isso** por achar que a reescrita resolveu. O capítulo 10 deixou de depender do `PYTHONHASHSEED` — `scratch_np/naive_bayes.py` guarda o vocabulário num array ordenado, então a soma tem ordem fixa e o resultado é determinístico —, mas `scratch/naive_bayes.py` continua vendorizado com o `assert` exato, e `tests/test_scratch.py` continua importando o módulo.

### Verificação

0. **`scripts/executar-secoes.py`**, o mais barato e o primeiro a rodar: executa cada `.qmd` de um capítulo num kernel próprio, sem render e sem lock (ver "Verificar um capítulo sem renderizar o livro"). É o que se usa enquanto se escreve.

1. **O `quarto render` é o teste.** Os módulos do `scratch/` **e** do `scratch_np/` executam `assert` no nível do módulo (`assert add([1, 2, 3], [4, 5, 6]) == [5, 7, 9]`, `linear_algebra.py:21`). Importar o pacote roda a suíte do próprio livro: um upgrade que quebre `add`, `dot` ou `mean` derruba o render no import, em vez de publicar um número errado em silêncio. Os módulos de `scratch_np/` seguem a mesma disciplina, com os `assert` do Grus traduzidos para arrays — e onde o Grus comparava float por igualdade exata, vira `np.isclose` **com a explicação na prosa**, nunca em silêncio.

2. **Render com a rede desligada** — `docker run --network none`, tanto local (`make offline`) quanto no CI (job `offline` do workflow, ver "CI/CD"). Específico deste livro: o risco de rede em tempo de render aparece em três lugares e nenhum falha de modo visível — com rede, tudo passa; o que se degrada é a reprodutibilidade, silenciosamente, até a página raspada mudar. Renderizar offline converte essa classe de fragilidade num teste booleano.

   **`make offline` apaga `_freeze/` antes de renderizar, de propósito.** Com `freeze: auto`, um `.qmd` que não mudou não reexecuta — o Quarto devolve a saída congelada sem rodar um chunk sequer. Rodado de cache quente, `make offline` renderizaria "com sucesso" tendo executado zero código Python, o que não prova nada sobre depender ou não de rede: é exatamente o tipo de verificação que passa sem testar o que diz testar. Por isso o alvo começa com `rm -rf _freeze` — o teste é honesto por construção, não por quem lembra de limpar o cache à mão antes de rodar. Se um dia esse `rm -rf` parecer zelo exagerado e alguém cogitar tirá-lo para acelerar o alvo: não tire — é o que garante que "offline passou" significa "o código rodou sem rede", não "o cache existia". O custo é um render mais lento (sem `_freeze/`); aceitável, porque é um alvo rodado deliberadamente antes de publicar, não a cada save. O CI não é afetado — `_freeze/` é gitignorado, então um checkout limpo já começa frio.

3. **`quarto check`**, diagnóstico do ambiente.

Não há equivalente ao teste de Playwright do Bases 3 — aquilo existe para células `{ojs}`, que este livro não tem.

### CI/CD

`.github/workflows/quarto-render.yml`, adaptado do Bases 3: cinco jobs a cada push na `main` — `build-image` (constrói e envia ao GHCR); em seguida, em paralelo, `testes` (`pytest tests/` **dentro** da imagem) e `offline` (`docker pull` + `docker run --network none` num runner comum, contra um checkout novo que já não tem `_freeze/` — o guard automático da invariante "nenhum byte vem da rede em tempo de render"); depois dos dois, `render` (roda **dentro** da imagem, `quarto render` → `_book/`, sobe como artefato); por fim `publish` (runner limpo, publica `_book/` em `gh-pages`). A cadeia de `needs` é sequencial o bastante para que uma falha em `testes` **ou** em `offline` bloqueie `render` e, por consequência, `publish` — nada quebrado chega a `gh-pages`.

**O nome da imagem precisa ser minúsculo e literal**: `ghcr.io/bragad/undf-bases5-ciencia-de-dados-202602:latest`. O GHCR rejeita maiúsculas, então não dá para usar `${{ github.repository_owner }}`, que resolveria para `BragaD`.

`_book/` e `_freeze/` são artefatos gitignorados. `docs/` **não** é gitignorado — guarda specs e planos.

Passos manuais no GitHub, uma única vez: **Settings → Actions → General → Workflow permissions** em "Read and write"; e, depois do primeiro workflow verde, **Settings → Pages → Source** → branch `gh-pages`, pasta `/ (root)`. Até isso, o site retorna 404 com o CI passando.

### Classes CSS e o spoiler

Copiar `styles.css` e `spoiler.html` do Bases 3:

```markdown
::: {.conceito}
Conceito importante (azul).
:::

::: {.exemplo}
Exemplo (verde).
:::
```

`spoiler.html` protege um `<div>` com hash SHA-256. **Isso é ofuscação, não proteção.** O conteúdo viaja em texto puro no HTML publicado; o hash só alterna qual `<div>` fica visível, e qualquer aluno lê tudo com Ctrl+U. **Nunca** para gabarito, prova ou qualquer coisa que o aluno não deva ver antes da hora. Serve só para "revelar a resposta depois de tentar".

Material avaliativo segue o padrão de `202601/BasesIV_EngSoft_BD/atividades/`: uma fonte `.qmd` renderizada duas vezes (aluno e gabarito) via metadado + filtro Lua, fora do projeto-livro.
