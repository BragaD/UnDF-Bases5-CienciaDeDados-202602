# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Estado atual

O design está aprovado e escrito em `docs/superpowers/specs/2026-08-15-estrutura-livro-bases5-design.md` — **leia essa spec antes de mexer na estrutura.** Este arquivo é o resumo operacional; a spec é a fonte das decisões e das razões. A spec carrega algumas notas de correção pós-implementação — leia-as também; elas registram onde a decisão original mudou depois de escrita.

**O andaime está construído.** 17 capítulos, 88 seções + 17 `index.qmd` = 105 `.qmd`, todos registrados em `_quarto.yml`. Container Docker (Quarto + `uv`), CI publicando em `gh-pages`, 20 testes (`make teste`) guardando os invariantes estruturais. O **capítulo 9 (k-Vizinhos Mais Próximos) está escrito por inteiro** — é o único capítulo de conteúdo pronto e é o **modelo de estilo** para os outros 16: leia `content/cap09/` antes de escrever qualquer outro capítulo, para o formato pegar (ver "Antes de escrever um capítulo", abaixo). **Os outros 16 capítulos são stubs** — callout `de @grus2019` citando capítulo e título da seção reais, mais um callout "Em construção" — aguardando conteúdo.

Os irmãos já prontos definiram o padrão da casa **na hora de montar o andaime**; agora servem como referência de convenção, não como fonte para copiar arquivo — a infra já existe aqui e já está adaptada:

- `../bases_3_estatistica/` — Quarto + Docker + `uv`, um `.qmd` por seção. Se uma dúvida de convenção não estiver resolvida aqui (formato de `Makefile`, padrão de `.devcontainer/`, uso de `styles.css`), é lá que a resposta provavelmente já foi pensada uma vez — mas adapte, não copie por cima do que já funciona.
- `../../202601/BasesIV_EngSoft_BD/` — livro de Banco de Dados, geração anterior (R + `renv`, sem container). Vale pelo `atividades/`: provas e trabalhos em `.qmd` que renderizam para PDF **fora** do projeto-livro, com gabarito via metadado + filtro Lua — ainda fora de escopo aqui. **Cuidado:** lá os caminhos de dados são relativos ao arquivo (`../../dados/`); aqui são relativos à raiz. Não copie esse padrão.

### Antes de escrever um capítulo

**Leia `content/cap09/` inteiro primeiro.** É o único capítulo escrito e foi revisado por rodadas sucessivas até fixar a forma: abertura de seção, posição dos callouts, formato de citação (capítulo + título em itálico, nunca um número de seção do Grus), justificativa de semente em chunk estocástico, e o callout de fechamento em `scikit-learn`. Um capítulo novo que copiar essa forma economiza rodadas de revisão; um que reinventar a forma provavelmente repete um erro que o cap. 9 já pagou.

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
| 6 | 9 | Obtendo Dados | 5 |
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

**Total: 88 arquivos de seção + 17 `index.qmd` = 105 `.qmd`.**

Os capítulos 2 e 16 são os únicos que se afastam de "um `.qmd` por seção" — o 2 porque o Grus lista cada construção da linguagem como seção (27 delas, o que daria um sidebar maior que o resto do livro somado), o 16 porque metade das seções são exemplos que moram melhor junto do conceito que demonstram. Os agrupamentos exatos estão na spec. As seções do Grus viram `##` dentro dos arquivos agrupados, e o `toc-depth: 4` as mantém no índice lateral.

## Pedagogia

Cada seção implementa o algoritmo em Python puro, como o Grus faz, e **fecha com um callout mostrando o equivalente em `scikit-learn`** — o fecho do arco. O `scikit-learn` nunca aparece na implementação de uma seção, só no callout.

**Não "melhore" o código do livro.** O pacote `scratch/` não importa numpy em lugar nenhum: `Vector = List[float]`, `dot` é um `sum(...)` sobre um `zip`. Trocar isso por `np.ndarray`, por broadcasting ou por uma chamada de `sklearn` destrói exatamente o que a disciplina existe para ensinar. O instinto de fazer isso é forte, porque o código é de fato lento e verboso para padrões de produção — a lentidão é o preço da transparência, pago de propósito.

## Comandos

Tudo roda dentro do container — não há Python instalado no host.

```bash
make preview   # hot-reload em http://localhost:4201
make render    # renderiza para _book/
make teste     # roda a suíte de invariantes estruturais (pytest, tests/)
make offline   # renderiza SEM REDE, com _freeze/ limpo antes — prova o isolamento
make shell     # shell dentro do container
make check     # quarto check
make build     # reconstrói a imagem (após mudar Dockerfile ou uv.lock)
make lock      # regenera uv.lock após editar pyproject.toml
make clean     # remove _book/, _freeze/, .quarto/ e o lixo de render abortado
```

**`make teste` roda `pytest tests/`** — 20 testes em três arquivos: `test_estrutura.py` (registro no `_quarto.yml`, caminhos de dados, citações, e os totais de 17 capítulos / 88 seções / 105 arquivos contra o `LIVRO` de `scripts/gerar-stubs.py`), `test_scratch.py` (o pacote vendorizado — inclusive um hash SHA-256 travando que `scratch/` continua verbatim upstream) e `test_dados.py` (os seis conjuntos commitados). É o que garante a regra "todo `.qmd` novo precisa ser registrado em `_quarto.yml`", abaixo — sem essa suíte, um arquivo esquecido no YAML só aparece quando alguém percebe a seção faltando no site publicado.

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

"For Further Exploration" fecha todo capítulo do Grus. Não vira arquivo: vira uma seção *Leituras adicionais* no fim do `index.qmd` do capítulo.

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
- **`working_with_data.py:148`** abre `stocks.csv` com um caminho relativo ao **cwd** no corpo do módulo — o upstream do Grus mantém esse arquivo na raiz do repositório dele; na nossa convenção, dado vive em `dados/`, então o `open()` estoura com `FileNotFoundError`. E as linhas 44–49 calculam `xs`, `ys1`, `ys2` com `random.random()` **sem semente** e afirmam `0.89 < correlation(xs, ys1) < 0.91` — o valor real (~0,894) encosta na borda dessa janela, e o `assert` falha cerca de 1 vez em 3 (medido em 5 rodadas). Vendorizar `stocks.csv` na raiz não resolve nada disso: a asserção sem semente continua sendo cara ou coroa a cada import.

`tests/test_scratch.py`'s `NAO_IMPORTAVEIS` documenta os dois motivos e trava com um teste que a exclusão precisa vir com motivo escrito. Consequência de conteúdo: os capítulos **7** (que *é* o módulo `working_with_data`) e **13** (que precisaria de `rescale`/`scale` de lá) não importam `working_with_data` — escrevem essas funções **inline no `.qmd`**, exatamente como o capítulo 6 já faz com o código de `getting_data`.

### Dependência dos capítulos fora da ementa

Tirar os Grus 5 e 6 da ementa não tira o código deles do caminho:

| Módulo | Nossos capítulos que importam |
|---|---|
| `scratch/statistics.py` (Grus 5) | 7, 11, 12 |
| `scratch/probability.py` (Grus 6) | 7, 12, 16 |

Há também dependência de **dados**: `scratch/statistics.py` carrega `num_friends_good` e `daily_minutes_good` — o dataset da rede social — e os capítulos 11 e 12 fazem regressão em cima dele.

Consequência: `scratch/` é vendorizado **inteiro**, incluindo os módulos fora da ementa. Podar o pacote quebra o livro.

### Dados

**Os dados do Grus são mantidos como estão**, inclusive a rede social fictícia DataSciencester, que é o fio narrativo do livro. Não há localização para dados brasileiros: sem um Bases 3 comum, o reencontro com um dataset específico não existiria para boa parte da turma.

Fidelidade ao dado, **não** à forma de obtê-lo — **nenhum byte vem da rede em tempo de render.** Os seis conjuntos entram commitados em `dados/` (~13 MB); o inventário e a razão de cada um estão na spec. O caso que mais surpreende: do corpus SpamAssassin entram **só os assuntos**, como CSV, porque o `naive_bayes.py` lê cada e-mail e descarta tudo menos a linha `Subject:`.

**Caminhos a partir da raiz**, sempre:

```python
acoes = pd.read_csv("dados/stocks.csv")        # ✓
acoes = pd.read_csv("../../dados/stocks.csv")  # ✗ nunca
```

### Sementes em chunks estocásticos — obrigatório

`train_test_split`, inicialização de pesos, k-means, gradiente estocástico: metade do livro é aleatória. **Todo chunk com RNG usa semente explícita** — e o Grus usa o `random` da stdlib, não o `numpy.random`:

```python
random.seed(42)
```

Sem isso, cada render produz números e gráficos diferentes: o `freeze` perde o sentido, o diff do site publicado vira ruído, e o material deixa de bater com o que o aluno vê na tela.

### Ambiente

Duas camadas travadas: `pyproject.toml` + `uv.lock` fixam as versões; o `Dockerfile` consome esse lock (`uv sync --frozen`) sobre um SO fixo com Quarto e locale `pt_BR.UTF-8`. O mesmo container renderiza local e no CI.

Dependências (a lista completa e comentada está na spec): `jupyter`, `matplotlib`, `tqdm`, `requests`, `beautifulsoup4`, `html5lib`, `python-dateutil`, `pillow` e `scikit-learn`.

O `scikit-learn` é **nosso**, não do livro — entra só pelos callouts de caixa-preta. Os pacotes `mnist` e `twython` do `requirements.txt` do Grus ficam de fora: o primeiro só serve para baixar dataset que será lido do disco, o segundo depende de uma API do Twitter que não é mais gratuita.

**`numpy` não está na lista e estará instalado assim mesmo**, como dependência transitiva do matplotlib e do scikit-learn. Não é contradição: a regra é *não reescrever o código do livro com numpy*, não *mantê-lo fora do ambiente*. A ausência deliberada no `pyproject.toml` é o sinal de que ele não é ferramenta desta disciplina.

Dois detalhes herdados, já pagos no Bases 3:

- O venv fica em **`/opt/venv`**, não em `/livro/.venv`. O `compose.yaml` faz bind mount do projeto sobre `/livro`, o que apagaria um venv que estivesse ali.
- O `Dockerfile` grava `/etc/profile.d/venv.sh` reexportando o `PATH`. Um shell de **login** recarrega `/etc/profile`, que reescreve o `PATH` e descartaria o `ENV PATH` da imagem — fazendo `python` cair no interpretador do sistema. Se `make shell` resolver o Python errado, é o primeiro lugar a checar.

`MPLBACKEND=Agg` é obrigatório: sem display, o matplotlib estoura ao importar.

**`PYTHONHASHSEED=0` também é obrigatório, e o motivo é sutil.** `scratch/naive_bayes.py:113` tem, no nível do módulo, um `assert` de igualdade **exata** de float sobre uma soma que percorre um `Set[str]`. A ordem de iteração de um `set` depende do hash das strings, que o Python randomiza por processo, e soma de ponto flutuante não é associativa — então a ordem muda o último bit e o assert falha. Medido neste container: **2 de 15 sementes falham no import; com `PYTHONHASHSEED=0`, 15 de 15 passam.**

Isso torna instável qualquer coisa que importe aquele módulo — hoje a suíte de testes, e o **render do capítulo 10** (que *é* Naive Bayes) assim que ele for escrito. A correção fica no `Dockerfile`, não em `scratch/`, porque o pacote é vendorizado literalmente e nunca editado: é propriedade do ambiente, e combina com a postura do livro de fixar semente em todo chunk estocástico.

### Verificação

1. **O `quarto render` é o teste.** Os módulos do `scratch/` executam `assert` no nível do módulo (`assert add([1, 2, 3], [4, 5, 6]) == [5, 7, 9]`, `linear_algebra.py:21`). Importar o pacote roda a suíte do próprio livro: um upgrade que quebre `add`, `dot` ou `mean` derruba o render no import, em vez de publicar um número errado em silêncio.

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
