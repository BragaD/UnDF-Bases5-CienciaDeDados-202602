# Estrutura do livro Bases 5 — Ciência de Dados

**Data:** 2026-08-15
**Status:** aprovado no brainstorming, pendente de revisão do autor

## Problema

Criar o site/livro da disciplina *Bases 5 — Ciência de Dados*, do curso de Ciência da Computação da UnDF, tendo como livro-texto Joel Grus, *Data Science from Scratch: First Principles with Python*, 2ª ed. (O'Reilly, 2019).

O repositório está vazio. Existem dois irmãos prontos que definem o padrão da casa: `../bases_3_estatistica/` (Quarto + Docker + `uv`, CI de três jobs — o modelo a seguir) e `../../202601/BasesIV_EngSoft_BD/` (mesma anatomia de `content/`, geração anterior em R/`renv`, e um diretório `atividades/` que o outro não tem).

## Identidade da disciplina

**Bases 5 abre as caixas-pretas que o aluno usou antes.** Ele já ajustou uma reta chamando uma função pronta; aqui ele descobre o que aquele `.fit()` fazia. A repetição de temas com *Bases 3 — Estatística* (regressão simples e múltipla) é o mecanismo pedagógico, não redundância a cortar.

**Restrição que molda tudo:** a turma **não** cursou Bases 3 com este professor. Cada aluno viu estatística com outro livro e outro tratamento. Consequências obrigatórias:

- O texto **nunca** faz referência específica a Bases 3 — nada de "como você viu com o `statsmodels`" ou de reaproveitar os dados brasileiros daquele livro. A referência é sempre genérica: *"você provavelmente já ajustou uma reta chamando uma função pronta"*.
- O que se pode assumir é o **tema** (média, mediana, desvio padrão, correlação, normal, testes), nunca o **tratamento**.
- Álgebra linear **não** pode ser assumida: não é estatística, e é a dependência mais pesada do livro. Por isso o capítulo 4 do Grus entrou no escopo.

## Escopo

**17 capítulos: Grus 1, 2, 3, 4 e 8 a 20.**

Fora: **Grus 5, 6 e 7** (Estatística, Probabilidade, Hipótese e Inferência), que qualquer ementa de Bases 3 cobre com qualquer livro. **Grus 21 a 27** (NLP, Redes, Recomendação, Bancos e SQL, MapReduce, Ética, Go Forth), por corte de escopo — o 24 já é uma disciplina inteira em `202601/BasesIV_EngSoft_BD`.

### Mapa Grus ↔ este livro

A numeração é **sequencial de 1 a 17**. Os capítulos 1–4 batem com os do Grus; de 5 em diante não batem.

| Nosso | Grus | Título | Arquivos de seção |
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

**Total: 88 arquivos de seção + 17 `index.qmd` = 105 `.qmd`.**

**Regra de citação:** o número dentro de um callout `de @grus2019` é sempre **do Grus**, nunca o nosso. No nosso Capítulo 9, "corresponde à seção 12.2 de @grus2019" está certo; "seção 9.2" está errado. Do lado do sistema de arquivos vale o **nosso** número: `content/cap09/` é k-Vizinhos.

> **Nota de correção (2026-08-15, Task 7 da execução):** a regra acima está errada e não foi seguida na implementação — foi corrigida durante a escrita do capítulo 9, quando ficou confirmado, contra o sumário do PDF, que **o Grus não numera as seções**: o sumário dele traz só títulos, sem "12.1", "12.2" etc. Não existe "seção 12.2 de @grus2019" para citar — inventar esse número é precisamente o que `test_nenhuma_secao_inventa_numero_de_secao_do_grus` (`tests/test_estrutura.py`) existe para proibir. A regra correta, em vigor: o callout cita o **capítulo** do Grus e o **título** (em itálico) da seção — `Esta seção corresponde a *The Model*, do capítulo 12 de @grus2019.` — nunca um número de seção do Grus. Ver `CLAUDE.md`, seção "Escopo e numeração", para o texto definitivo.

## Pedagogia

Cada seção implementa o algoritmo em Python puro, como o Grus faz, e **fecha com um callout mostrando o equivalente em `scikit-learn`** — o fecho do arco "abrir a caixa-preta". O `scikit-learn` nunca aparece na implementação de uma seção, só no callout de fechamento.

**Não reescrever o código do livro.** O pacote `scratch/` não importa numpy em lugar nenhum: `Vector = List[float]`, `dot` é um `sum(...)` sobre um `zip`. Trocar isso por `np.ndarray`, por broadcasting ou por uma chamada de `sklearn` destrói exatamente o que a disciplina existe para ensinar. A lentidão é o preço da transparência, e foi pago de propósito.

## Dados

**Os dados do Grus são mantidos como estão** — inclusive a rede social fictícia DataSciencester, que é o fio narrativo do livro. Não há localização para dados brasileiros: com a turma vindo de Bases 3 diferentes, o reencontro com um dataset específico não existiria para boa parte dela.

Fidelidade ao dado, **não** à forma de obtê-lo: nenhum byte vem da rede em tempo de render.

| Dado | Origem | Como entra em `dados/` |
|---|---|---|
| `stocks.csv`, `comma_delimited_stock_prices.csv` | repo do Grus | commitados como estão (~1,7 MB) |
| HTML do cap. 6 | `joelgrus/data` no GitHub | baixado uma vez, commitado |
| `iris.data` | UCI | baixado uma vez, commitado |
| Corpus SpamAssassin | tarballs de e-mails | **só os assuntos**, como CSV `(assunto, is_spam)` |
| MNIST | pacote `mnist` | os 4 `.idx.gz` originais, commitados (~11 MB) |
| Imagem do cap. 17 | o leitor fornece (`girl_with_book.jpg` no Grus) | ver abaixo |

**SpamAssassin:** o `naive_bayes.py` lê cada arquivo de e-mail e descarta tudo menos a linha `Subject:`. Baixar centenas de MB para usar uma linha por arquivo não se justifica. O CSV extraído tem alguns milhares de linhas (~200 KB). O código de varredura dos diretórios aparece no capítulo com `eval: false` — ele *é* parte da lição, só não precisa rodar a cada render.

**Imagem do capítulo 17:** o Grus usa `girl_with_book.jpg` e não a distribui — o texto manda o leitor apontar para uma imagem qualquer. O exemplo precisa de uma foto com poucas regiões de cor bem definidas, para o k-means produzir um resultado legível com k pequeno. Como o livro não fixa qual, a escolha é nossa; a exigência é ter licença que permita redistribuição (CC0 ou equivalente) e caber em ~200 KB depois de redimensionada. **O arquivo específico fica a definir na implementação** — é a única peça de dado ainda não escolhida, e é a de menor risco: qualquer imagem que atenda aos dois critérios serve.

> **Nota de correção (2026-08-15, Task 4 da execução): resolvido.** A imagem escolhida é *Composition II in Red, Blue, and Yellow* (1930), de Piet Mondriaan — poucos blocos de cor sólida (vermelho, azul, amarelo, branco, preto), domínio público (autor falecido em 1944; publicação pré-1931 nos EUA), redimensionada para no máximo 600 px no lado maior. Commitada em `dados/imagem-cores.jpg`; licença e conteúdo verificados na página real do Wikimedia Commons (ver `dados/README.md`).

Repositório final: ~13 MB de dados.

## O pacote `scratch/`

**Princípio: vendorizado literalmente, nunca editado.** Cópia fiel do repositório do Grus (MIT, licença preservada). Toda adaptação vive no `.qmd`. Assim um `diff` contra o upstream continua limpo.

Com `execute-dir: project`, o cwd de todo chunk é a raiz e `from scratch.linear_algebra import dot` resolve sem `PYTHONPATH` — que é o problema que o README do Grus manda o leitor resolver à mão.

Cada módulo tem um `if __name__ == "__main__":` com a demonstração do capítulo. Ele não roda no import; se o texto precisar daquele exemplo, chamar as funções explicitamente no chunk.

### Dois efeitos colaterais verificados no código

**1. Importar alguns módulos desenha gráficos, e um escreve arquivo.** Chamadas `plt.*` no nível do módulo: `statistics.py` (5), `probability.py` (18), `working_with_data.py` (8), `visualization.py` (63). E `working_with_data.py:41` faz `plt.savefig('im/working_scatter.png')` **no import**: um `from scratch.working_with_data import rescale` estoura com `FileNotFoundError` se `im/` não existir. Isso é atingido pelo capítulo 7 (que *é* esse módulo) e pelo 13, que importa `rescale` e `scale` dele.

Correção: criar `im/` vazio no repositório, como o Grus tem no dele. **Não** editar o pacote. Chunks que importam desses módulos vão com `include: false` e `plt.close('all')` na sequência, senão a figura do import vaza para a saída da célula.

**2. O capítulo 6 nunca importa o próprio módulo.** `getting_data.py:90` tem um `requests.get` no corpo do módulo — importar dispara rede. Nenhum outro módulo o importa (verificado), então basta não importá-lo: o capítulo 6 escreve os chunks direto, lendo o HTML vendorizado. O código do Grus continua visível e citável no repositório, sem ser executado por acidente.

> **Nota de correção (2026-08-15, Ruling E, Task 3 da execução):** o texto acima, escrito nesta spec original, ficou incompleto na implementação. `working_with_data.py` tem um SEGUNDO defeito, mais grave que o `FileNotFoundError` descrito no item 1: as linhas 44–49 calculam `xs`, `ys1`, `ys2` com `random.random()` **sem semente** e o módulo afirma `0.89 < correlation(xs, ys1) < 0.91` no nível do módulo — o valor real (~0,894) encosta na borda dessa janela, e o `assert` falhou cerca de 1 vez em 3 rodadas medidas. Vendorizar `stocks.csv` na raiz (a correção que o item 1 sugere) não resolve isso: a asserção sem semente continua sendo cara ou coroa a cada import, com ou sem o arquivo no lugar certo.
>
> Decisão tomada: `working_with_data` entra, ao lado de `getting_data`, na lista de módulos **nunca importados** (`tests/test_scratch.py`, dicionário `NAO_IMPORTAVEIS`, com o motivo de cada um escrito por extenso). Os capítulos **7** (que *é* esse módulo) e **13** (que importaria `rescale`/`scale` dele) escrevem essas funções **inline no `.qmd`**, em vez de importar — a mesma solução que o item 2 já usa para `getting_data`. Ver `CLAUDE.md`, seção "O pacote `scratch/`", para o texto corrigido e definitivo.

### Dependência dos capítulos pulados

Tirar os Grus 5 e 6 da ementa não tira o código deles do caminho:

| Módulo | Nossos capítulos que importam |
|---|---|
| `scratch/statistics.py` (Grus 5) | 7, 11, 12 |
| `scratch/probability.py` (Grus 6) | 7, 12, 16 |

Há também dependência de **dados**: `scratch/statistics.py` carrega `num_friends_good` e `daily_minutes_good`, e os nossos capítulos 11 e 12 fazem regressão em cima deles.

Consequência: `scratch/` é vendorizado **inteiro**, incluindo os módulos dos capítulos fora da ementa. Podar o pacote quebra o livro.

## Infraestrutura

Cópia do `bases_3_estatistica`. Herdado sem discussão: Docker + `uv` com `uv.lock`, venv em `/opt/venv`, `/etc/profile.d/venv.sh`, locale `pt_BR.UTF-8`, `MPLBACKEND=Agg`, Python 3.12, alvos do `Makefile`, `.devcontainer/`, `execute-dir: project`, `freeze: auto`, `styles.css` (`.conceito`, `.exemplo`, dark mode), `spoiler.html`.

Adaptações:

1. **Porta 4201**, para conviver com o preview do Bases 3 na 4200.
2. **Imagem `ghcr.io/bragad/undf-bases5-ciencia-de-dados-202602:latest`** — minúscula e literal; o GHCR rejeita maiúsculas, então não dá para usar `${{ github.repository_owner }}`.
3. **`site-url`/`repo-url`**: `https://BragaD.github.io/UnDF-Bases5-CienciaDeDados-202602`.
4. **Dependências:**

```toml
dependencies = [
    "jupyter>=1,<2",              # Quarto executa chunks Python via jupyter
    "matplotlib>=3,<4",           # cap. 3 e os gráficos do livro
    "tqdm>=4,<5",                 # caps. 7, 12, 17
    "requests>=2,<3",             # cap. 6
    "beautifulsoup4>=4,<5",       # cap. 6
    "html5lib>=1,<2",             # cap. 6
    "python-dateutil>=2,<3",      # cap. 7
    "pillow>=11,<12",             # cap. 17
    "scikit-learn>=1,<2",         # NOSSO, não do livro — os callouts de caixa-preta
]
```

Teto de versão em toda dependência; pacotes `0.x` levam teto no **minor**, porque em SemVer pré-1.0 é o minor que carrega mudança incompatível.

`mnist` e `twython` ficam de fora: o primeiro só serve para baixar o dataset (que será lido do disco), o segundo depende de uma API do Twitter que não é mais gratuita.

**`numpy` não está na lista e estará instalado assim mesmo**, como dependência transitiva do matplotlib e do scikit-learn. Isso não é contradição: a regra é *não reescrever o código do livro com numpy*, não *mantê-lo fora do ambiente*. A ausência deliberada no `pyproject.toml` é o sinal de que ele não é ferramenta desta disciplina.

## Verificação

Três camadas, em ordem de custo:

1. **O `quarto render` é o teste.** Os módulos do `scratch/` executam `assert` no nível do módulo (`assert add([1, 2, 3], [4, 5, 6]) == [5, 7, 9]`, `linear_algebra.py:21`). Importar o pacote roda a suíte do próprio livro: um upgrade que quebre `add`, `dot` ou `mean` derruba o render no import, em vez de publicar um número errado em silêncio — que foi exatamente a falha que o Bases 3 sofreu com o pandas 3.

2. **Render com a rede desligada** (`docker run --network none`), no CI. Específico deste livro: o risco de rede em tempo de render aparece em três lugares (o `requests.get` no import do cap. 6, o MNIST no cap. 16, as raspagens vivas do cap. 6) e nenhum falha de modo visível — com rede, tudo passa; o que se degrada é a reprodutibilidade, silenciosamente, até a página raspada mudar. Renderizar offline converte essa classe inteira de fragilidade num teste booleano.

   > **Nota de correção (2026-08-15, revisão final do branch):** "no CI" acima descrevia uma intenção que a implementação da Task 8 não executou — o `.github/workflows/quarto-render.yml` ganhou os jobs `build-image`, `testes`, `render` e `publish`, mas nenhum rodava o render offline; a invariante "nenhum byte vem da rede" só era verificada localmente, por disciplina de quem lembrasse de rodar `make offline` antes de publicar. Corrigido na revisão final: o workflow ganhou um job `offline`, que roda em paralelo a `testes` (após `build-image`) num runner comum, faz `docker pull` da imagem publicada e `docker run --network none` contra ela; `render` só roda se `testes` **e** `offline` passarem. Um checkout de CI nunca tem `_freeze/` (gitignorado), então o job já começa frio por construção — sem precisar do `rm -rf _freeze` que `make offline` faz localmente.

3. **`quarto check`**, diagnóstico do ambiente.

Não há equivalente ao teste de Playwright do Bases 3 — aquilo existe para células `{ojs}`, que este livro não tem.

### Modos de falha conhecidos

- `freeze` preso com saída velha → `make clean`.
- Lixo de render abortado travando o render seguinte (bind mount do Docker no macOS falhando com "Directory not empty") → o `make clean` do Bases 3 já remove os `*_files` e os `.html` órfãos.
- Shell de login recarregando `/etc/profile` e resolvendo o Python do sistema em vez do venv → conferir `/etc/profile.d/venv.sh`.

## Convenções de conteúdo

**Todo `.qmd` novo precisa ser registrado em `_quarto.yml`** sob `book.chapters`. Arquivo não listado não aparece no livro. A ordem vem do YAML, não do nome do arquivo; para reordenar, `git mv` e atualizar o YAML na mesma operação.

**Sementes obrigatórias.** `train_test_split`, inicialização de pesos, k-means, gradiente estocástico — metade do livro é aleatória. Todo chunk com RNG usa semente explícita, e o Grus usa o `random` da stdlib, não o `numpy.random`. Sem isso cada render produz números diferentes, o `freeze` perde o sentido e o diff do site publicado vira ruído.

**Caminhos de dados a partir da raiz** (`execute-dir: project`): `pd.read_csv("dados/stocks.csv")`, nunca `../../dados/`. Cuidado ao consultar o repo de BD do 202601 — lá a regra é a oposta.

**`spoiler.html` é ofuscação, não proteção.** O conteúdo viaja em texto puro no HTML publicado; o hash SHA-256 só alterna qual `<div>` fica visível. Nunca usar para gabarito ou prova. Material avaliativo segue o padrão de `202601/BasesIV_EngSoft_BD/atividades/`: uma fonte `.qmd` renderizada duas vezes (aluno e gabarito) via metadado + filtro Lua, fora do projeto-livro.

**"For Further Exploration"** fecha todos os capítulos do Grus. Não vira arquivo: vira uma seção *Leituras adicionais* no fim do `index.qmd` de cada capítulo.

### Agrupamentos que se afastam de "um arquivo por seção"

**Capítulo 2 (27 seções do Grus → 6 arquivos).** O Grus lista cada construção da linguagem como seção própria (*Strings*, *Lists*, *Tuples*, *Truthiness*). Um arquivo por item daria 27 páginas de meia tela e um sidebar em que o capítulo de Python é maior que o resto do livro somado. Agrupamento preservando a ordem do livro:

1. `01-ambiente-e-sintaxe.qmd` — Zen of Python, Getting Python, Virtual Environments, Whitespace Formatting, Modules
2. `02-funcoes-strings-excecoes.qmd` — Functions, Strings, Exceptions
3. `03-estruturas-de-dados.qmd` — Lists, Tuples, Dictionaries, defaultdict, Counters, Sets
4. `04-controle-de-fluxo.qmd` — Control Flow, Truthiness, Sorting, List Comprehensions
5. `05-testes-classes-e-geradores.qmd` — Automated Testing and assert, Object-Oriented Programming, Iterables and Generators
6. `06-ferramentas-e-tipos.qmd` — Randomness, Regular Expressions, Functional Programming, zip and Argument Unpacking, args and kwargs, Type Annotations, Welcome to DataSciencester!

**Capítulo 16 (12 seções → 8 arquivos).** Metade das seções são exemplos (*Example: XOR Revisited*, *Example: FizzBuzz Revisited*, *Example: MNIST*). Cada exemplo mora junto do conceito que demonstra, em vez de virar página própria.

As 27 e as 12 seções do Grus viram `##` dentro dos arquivos agrupados. Com `toc-depth: 4` já configurado, cada uma aparece no índice lateral — nada se perde na navegação.

Nos outros 15 capítulos, um `.qmd` por seção, títulos do Grus traduzidos.

## Entregável deste ciclo

- Infra completa: `Dockerfile`, `compose.yaml`, `Makefile`, `.devcontainer/`, `.gitignore`, `pyproject.toml` + `uv.lock`, `styles.css`, `spoiler.html`, CI publicando em `gh-pages`
- `scratch/` vendorizado + `im/` vazio + `dados/` com os seis conjuntos
- `_quarto.yml` com os 17 capítulos e as seções registrados
- **105 `.qmd`**: 17 `index.qmd` (visão geral, objetivos, tabela de seções, *Leituras adicionais*) + 88 stubs gerados por script, cada um com o callout `de @grus2019` citando capítulo **e** seção reais
- **Capítulo 9 (k-Vizinhos) escrito por inteiro**, como modelo de estilo: implementação em Python puro → Iris → maldição da dimensionalidade → callout `KNeighborsClassifier`. Escolhido por ser o menor capítulo que exercita tudo — importa de `linear_algebra`, usa dataset externo vendorizado, e fecha o arco da caixa-preta.
- `index.qmd`, `README.md`, `references.bib` com `@grus2019`
- `CLAUDE.md` atualizado para refletir este design

**Fora de escopo neste ciclo:** os outros 16 capítulos e qualquer material de avaliação (`atividades/`).

### Passos manuais no GitHub

Nenhum job automatiza, e são feitos uma única vez:

1. Criar o repositório e dar push na `main`.
2. **Settings → Actions → General → Workflow permissions** em "Read and write permissions" (o job `publish` precisa para dar push em `gh-pages`).
3. Depois do primeiro workflow verde, **Settings → Pages → Source** → "Deploy from a branch" → `gh-pages`, pasta `/ (root)`.

Até o passo 3, a URL do site retorna 404 mesmo com o workflow passando.

## Decisões registradas

| Decisão | Escolha | Por quê |
|---|---|---|
| Identidade | Reforço — abrir caixas-pretas | Aluno já usou as ferramentas; aqui constrói |
| Referência a Bases 3 | Genérica, nunca específica | Turma não cursou Bases 3 com este professor |
| Escopo | Grus 1–4, 8–20 (17 caps.) | 5–7 são estatística; 21–27 cortados |
| Grus 4 (Álgebra Linear) | **Dentro** do escopo | Não é estatística; era a dependência de 9 dos 16 capítulos originais |
| Dados | Do Grus, sem localização | Sem Bases 3 comum, o reencontro não existiria |
| Numeração | Sequencial 1–17 | Caps. 1–4 batem com o Grus; sidebar sem buracos |
| Granularidade dos stubs | Um por seção, títulos reais do livro | PDF disponível — nenhum título inventado |
| Entregável | Andaime + todos os stubs + 1 capítulo escrito | Padrão que funcionou no Bases 3 |
| `scratch/` | Vendorizado literalmente, nunca editado | `diff` limpo contra o upstream |
| SpamAssassin | Só os assuntos, como CSV | O código usa uma linha por arquivo |
