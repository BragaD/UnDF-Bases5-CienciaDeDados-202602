# Conjuntos de Dados

Todos os arquivos deste diretório são **commitados**. Nenhum é baixado em tempo
de render: um livro que faz chamadas de rede a cada render é frágil — a página
raspada muda de layout, a API sai do ar, e o material quebra sem ninguém ter
tocado no repositório.

Do capítulo 6 em diante, coluna e variável estão em **português**: minúsculas,
`snake_case`, sem acento no nome; o valor de categoria preserva a grafia
correta (com acento, quando é o caso).

## `estados.csv` — 27 unidades federativas

População e taxa de homicídios de **2024**.

| Coluna | Fonte |
|---|---|
| `estado`, `sigla` | IBGE — [API de localidades](https://servicodados.ibge.gov.br/api/v1/localidades/estados) |
| `populacao` | IBGE — SIDRA, tabela 6579, variável 9324, ano 2024 |
| `taxa_homicidios` | Atlas da Violência (Ipea/FBSP), edição de 2024 — por 100 mil habitantes |

## `alugueis.csv` — 10.692 imóveis para alugar em 5 cidades

São Paulo, Rio de Janeiro, Belo Horizonte, Porto Alegre e Campinas.

Fonte: *Brazilian houses to rent* (v2), publicado no Kaggle por rubenssjr sob
**CC0** (domínio público). Só os nomes das colunas e os dois campos binários
foram traduzidos para o português.

**Nada foi limpo, de propósito.** A coluna `andar` traz `"-"` em 2.461 das
10.692 linhas (23%), o que faz o `pandas` lê-la como `object` em vez de
número — é a armadilha que a seção 6.3 usa para mostrar que a inferência de
tipo é heurística, não garantia. Os outliers também ficaram: há um imóvel de
46.335 m² e um condomínio de R$ 1.117.000.

## `cidades.csv` — as 5 cidades, com UF e região

Escrito à mão. Existe para a seção 6.5 ter um `merge` de verdade: liga
`alugueis.csv` a `estados.csv` pela sigla. São Paulo e Campinas dividem a
mesma UF, então a junção é um muitos-para-um real.

## `Advertising.csv`, `Income1.csv`, `Income2.csv` — os três do capítulo 7 (ISLP)

Do [site oficial de @james2023](https://www.statlearning.com/s/), *An
Introduction to Statistical Learning*. O capítulo 7 atual (*O que é
aprendizado estatístico*, ISLP) usa os três; o resto do capítulo roda sobre
dado simulado.

A coleta é feita uma única vez por `scripts/baixar-dados.py`, que baixa a
versão original — em inglês, com o índice do R:

```bash
docker compose run --rm --no-deps livro python scripts/baixar-dados.py
```

Depois do download, os cabeçalhos são traduzidos à mão e a coluna de índice
do R é removida. É essa tabela de-para que mantém a ponte com o livro-texto
— o **nome do arquivo** não muda, só o cabeçalho:

**`Advertising.csv`** — 200 mercados, investimento em publicidade e vendas.

| Original (R) | Traduzida |
|---|---|
| `Unnamed: 0` (índice do R) | *(removida)* |
| `TV` | `tv` |
| `radio` | `radio` |
| `newspaper` | `jornal` |
| `sales` | `vendas` |

**`Income1.csv`** — 30 pessoas, escolaridade e renda.

| Original (R) | Traduzida |
|---|---|
| `Unnamed: 0` (índice do R) | *(removida)* |
| `Education` | `escolaridade` |
| `Income` | `renda` |

**`Income2.csv`** — 30 pessoas, escolaridade, senioridade e renda.

| Original (R) | Traduzida |
|---|---|
| `Unnamed: 0` (índice do R) | *(removida)* |
| `Education` | `escolaridade` |
| `Seniority` | `senioridade` |
| `Income` | `renda` |

`Income1` e `Income2` são **simulados pelos autores** de @james2023, não são
dado observado. É por isso que o capítulo pode desenhar o *f* verdadeiro nas
figuras: quando o dado é gerado por uma função conhecida mais ruído, dá para
mostrar, ao lado do ajuste, o erro que nenhum modelo consegue eliminar —
coisa que não é possível fazer com dado real, onde o *f* verdadeiro é
justamente o que se está tentando estimar.

## `Credit.csv`, `Auto.csv` — os dois do capítulo 8 (ISLP)

Do mesmo [site oficial de @james2023](https://www.statlearning.com/s/). O
capítulo 8 (*Regressão Linear*, ISLP 3) usa os dois: `Credit` traz o
preditor qualitativo e a colinearidade; `Auto` traz o termo não linear e o
diagnóstico de resíduo.

A coleta é feita pelo mesmo `scripts/baixar-dados.py`, que baixa a versão
original em inglês:

```bash
docker compose run --rm --no-deps livro python scripts/baixar-dados.py
```

Depois do download, os cabeçalhos são traduzidos à mão. É essa tabela de-para
que mantém a ponte com o livro-texto — o **nome do arquivo** não muda, só o
cabeçalho:

**`Credit.csv`** — 400 clientes, renda, uso de crédito e dados
sociodemográficos. Não tem coluna de índice do R, só cabeçalho.

| Original (R) | Traduzida |
|---|---|
| `Income` | `renda` |
| `Limit` | `limite` |
| `Rating` | `pontuacao` |
| `Cards` | `cartoes` |
| `Age` | `idade` |
| `Education` | `escolaridade` |
| `Own` | `imovel_proprio` |
| `Student` | `estudante` |
| `Married` | `casado` |
| `Region` | `regiao` |
| `Balance` | `saldo` |

Categorias também traduzidas: `No`/`Yes` viram `não`/`sim` em
`imovel_proprio`, `estudante` e `casado`; em `regiao`, `East`/`South`/`West`
viram `Leste`/`Sul`/`Oeste`.

Unidades das colunas monetárias, como documentadas pelo ISLP: `renda` está
em milhares de dólares; `limite` e `saldo` estão em dólares.

**`Auto.csv`** — 397 automóveis, milhas por galão e características técnicas.

| Original (R) | Traduzida |
|---|---|
| `mpg` | `milhas_por_galao` |
| `cylinders` | `cilindros` |
| `displacement` | `cilindrada` |
| `horsepower` | `potencia` |
| `weight` | `peso` |
| `acceleration` | `aceleracao` |
| `year` | `ano` |
| `origin` | `origem` |
| `name` | `nome` |

Só o cabeçalho muda: `origem` fica com o código numérico do livro — 1 para
automóvel americano, 2 para europeu, 3 para japonês —, e `nome`, nome próprio
de modelo de carro, fica em inglês. **Os cinco `?` de
`potencia` foram preservados de propósito** — são a armadilha de tipo que uma
das seções do capítulo usa, e o ISLP trabalha com as 392 linhas restantes.

## `College.csv` — o conjunto da lista computacional 1

Do mesmo [site oficial de @james2023](https://www.statlearning.com/s/). O
exercício 3 da lista computacional 1 é o 2.8 do ISLP, e percorre o conjunto
inteiro com `read_csv`, `describe` e uma matriz de dispersão.

A coleta é feita pelo mesmo `scripts/baixar-dados.py`, que baixa a versão
original em inglês:

```bash
docker compose run --rm --no-deps livro python scripts/baixar-dados.py
```

Depois do download, os cabeçalhos são traduzidos à mão. É essa tabela de-para
que mantém a ponte com o livro-texto — o **nome do arquivo** não muda, só o
cabeçalho:

**`College.csv`** — 777 universidades americanas, com dados de inscrição,
custo e corpo docente.

| Original (R) | Traduzida |
|---|---|
| `Unnamed: 0` (índice do R) | **`Unnamed: 0` — preservada, não muda** |
| `Private` | `privada` |
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

Categorias também traduzidas: em `privada`, `Yes`/`No` viram `sim`/`não`.

**Diferente dos demais conjuntos do ISLP neste diretório, a coluna de índice
do R foi preservada**, com o nome `Unnamed: 0` que o `pandas` gera para ela, e
com os nomes de universidade em inglês — nome próprio não se traduz. Nos
outros CSV (`Advertising`, `Income1`, `Income2`, `Credit`, `Auto`) essa coluna
foi removida na tradução; aqui ela é o assunto do item (b) do exercício 3: o
aluno descobre que a primeira coluna é o nome da universidade e relê o
arquivo com `index_col=0`. Removê-la apagaria o exercício.

## `Default.csv` — 10.000 clientes de cartão de crédito, saldo, renda e inadimplência

Do capítulo 9 (*Classificação*, ISLP 4). É o conjunto sobre o qual o
capítulo inteiro é contado: as figuras 4.1 a 4.7, as tabelas 4.1 a 4.5 e a
matriz de confusão da seção 4.4.2 são todas dele.

**A proveniência é diferente dos demais conjuntos deste diretório.** O [site
oficial de @james2023](https://www.statlearning.com/s/) não publica todos os
catorze conjuntos previstos para este livro, e o `Default` não está entre
os publicados — pedi-lo devolve 404. Ele vem do **pacote `ISLP` dos próprios
autores**, na versão **0.4.1**, distribuído no PyPI, que traz os CSV prontos
em `ISLP/data/`. A coleta baixa o *wheel* dessa versão uma única vez e extrai
o arquivo de dentro dele — `scripts/baixar-dados.py` faz isso com
`extrair_do_pacote`, ao lado da função que baixa do site:

```bash
.venv/bin/python scripts/baixar-dados.py
```

**Isto não torna o `ISLP` uma dependência.** O pacote não entra no
`pyproject.toml` e nada o importa em código que executa; o que se extrai dele
é só o dado, uma vez, para virar este CSV commitado — exatamente o gesto que
já valia para os sete conjuntos do site.

Depois da extração, cabeçalho e categorias são traduzidos à mão. É essa
tabela de-para que mantém a ponte com o livro-texto — o **nome do arquivo**
não muda, só o conteúdo:

| Original | Traduzida |
|---|---|
| `default` | `inadimplente` |
| `student` | `estudante` |
| `balance` | `saldo` |
| `income` | `renda` |

Categorias também traduzidas: em `inadimplente` e em `estudante`, `Yes`/`No`
viram `sim`/`não`.

**O conjunto é simulado pelos autores** de @james2023, como `Income1` e
`Income2` — não é dado observado.

**`saldo` e `renda` também existem em `Credit.csv`, com outra escala.** No
`Default`, `renda` está em **dólares** (de 771,97 a 73.554,23) e `saldo`
também em **dólares** (de 0 a 2.654,32); no `Credit`, `renda` está em
**milhares** de dólares. Mesmo nome de coluna, arquivo diferente, unidade
diferente.

## `Hitters.csv`, `Heart.csv` — os dois do capítulo 12 (ISLP 8.1)

Do capítulo 12 (*Árvores de Decisão*, ISLP 8.1). O `Hitters` é o exemplo da
árvore de regressão e da poda (8.1.1, figuras 8.1 a 8.5); o `Heart`, o da
árvore de classificação (8.1.2, figura 8.6). Os dois voltam no capítulo 13
(*Bagging, Florestas e Boosting*, ISLP 8.2): o `Heart` nas figuras 8.8 e 8.9, e o
`Hitters` no bagging, na floresta e no boosting de regressão.

**As origens são diferentes.** O `Heart` vem do [site oficial de
@james2023](https://www.statlearning.com/s/), como os conjuntos dos capítulos
7 e 8, e não está no pacote (conferido). O `Hitters` não está no site (pedi-lo
devolve 404) e vem do *wheel* do pacote `ISLP` **0.4.1**, pela mesma
`extrair_do_pacote` do `Default` — ver a seção dele, acima, sobre por que isso
não torna o `ISLP` uma dependência. Os dois saem de uma única execução de
`scripts/baixar-dados.py`.

Depois da coleta, só o cabeçalho e as categorias foram traduzidos; nenhum
valor numérico mudou. O **nome do arquivo** fica, como ponte com o
livro-texto.

### `Hitters.csv` — 322 jogadores das grandes ligas de beisebol

Chega sem a coluna de índice do R. Estatísticas da temporada de **1986**,
acumuladas da carreira (as colunas `_carreira`) e **salário na temporada de
1987, em milhares de dólares**. `anos` são os anos do jogador nas grandes
ligas.

| Original | Traduzida | Original | Traduzida |
|---|---|---|---|
| `AtBat` | `vezes_ao_bastao` | `CAtBat` | `vezes_ao_bastao_carreira` |
| `Hits` | `rebatidas` | `CHits` | `rebatidas_carreira` |
| `HmRun` | `home_runs` | `CHmRun` | `home_runs_carreira` |
| `Runs` | `corridas` | `CRuns` | `corridas_carreira` |
| `RBI` | `impulsionadas` | `CRBI` | `impulsionadas_carreira` |
| `Walks` | `bases_por_bolas` | `CWalks` | `bases_por_bolas_carreira` |
| `Years` | `anos` | `PutOuts` | `eliminacoes` |
| `League` | `liga` | `Assists` | `assistencias` |
| `Division` | `divisao` | `Errors` | `erros` |
| `Salary` | `salario` | `NewLeague` | `liga_seguinte` |

Categorias: em `liga` e `liga_seguinte` (a liga do jogador no início de
1987), `A`/`N` viram `Americana`/`Nacional`; em `divisao`, `E`/`W` viram
`Leste`/`Oeste`.

**Os 59 `salario` vazios ficam no arquivo.** Descartá-los é passo à vista da
seção 12.1 (322 → 263 linhas), como os `?` da `potencia` no `Auto`.

### `Heart.csv` — 303 pacientes com dor no peito

Chega do site **com** a coluna de índice do R, que foi removida.

| Original | Traduzida | Valores |
|---|---|---|
| `Age` | `idade` | anos |
| `Sex` | `sexo` | código mantido: 1 = masculino, 0 = feminino |
| `ChestPain` | `dor_no_peito` | `typical`/`nontypical`/`nonanginal`/`asymptomatic` → `típica`/`atípica`/`não anginosa`/`assintomática` |
| `RestBP` | `pressao_repouso` | pressão em repouso |
| `Chol` | `colesterol` | |
| `Fbs` | `glicemia_alta` | código 0/1 (glicemia de jejum acima de 120 mg/dl) |
| `RestECG` | `ecg_repouso` | código 0/1/2 |
| `MaxHR` | `freq_cardiaca_max` | frequência cardíaca máxima |
| `ExAng` | `angina_exercicio` | código 0/1 (angina induzida por exercício) |
| `Oldpeak` | `depressao_st` | |
| `Slope` | `inclinacao_st` | código 1/2/3 |
| `Ca` | `vasos_coloridos` | 0 a 3 |
| `Thal` | `talio` | `normal`/`fixed`/`reversable` → `normal`/`defeito fixo`/`defeito reversível` |
| `AHD` | `doenca_cardiaca` | `Yes`/`No` → `sim`/`não` |

Os códigos numéricos são mantidos, como `origem` no `Auto`. As colunas
indicadoras que o `pd.get_dummies` cria herdam o acento e o espaço da
categoria (`dor_no_peito_não anginosa`).

**Os vazios ficam no arquivo**: 4 em `vasos_coloridos` e 2 em `talio`, em 6
linhas diferentes (os `NA` do original viraram célula vazia, que o `pandas` lê
como nulo sem `na_values`). Descartá-los é passo à vista da seção 12.3
(303 → 297 linhas).

## `mnist_treino.csv.gz`, `mnist_teste.csv.gz` — amostra fixa do MNIST (capítulo 14)

Do capítulo 14 (*Redes Neurais*, ISLP 10.2 e lab 10.9.2): a comparação entre
LDA, regressão logística e rede multicamada, e as curvas de perda por época.

**Origem.** O MNIST de LeCun, Cortes e Burges: 70.000 dígitos manuscritos em
tons de cinza, 28 × 28 pixels. Os quatro arquivos no formato idx
(`train-images-idx3-ubyte.gz`, `train-labels-idx1-ubyte.gz`,
`t10k-images-idx3-ubyte.gz`, `t10k-labels-idx1-ubyte.gz`) vêm do espelho
`https://ossci-datasets.s3.amazonaws.com/mnist/`, são lidos **em memória** por
`scripts/baixar-dados.py` e nunca gravados em disco.

**Recorte.** As **primeiras** 6.000 imagens do treino e as **primeiras** 2.000
do teste, na ordem do arquivo original, sem sorteio. O conjunto inteiro custaria
segundos demais de ajuste por seção, a cada render; com a amostra, a diferença
entre os métodos continua nítida. Contagem por dígito (0 a 9):

| Arquivo | Linhas | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `mnist_treino.csv.gz` | 6.000 | 592 | 671 | 581 | 608 | 623 | 514 | 608 | 651 | 551 | 601 |
| `mnist_teste.csv.gz` | 2.000 | 175 | 234 | 219 | 207 | 217 | 179 | 178 | 205 | 192 | 194 |

**Formato.** CSV comprimido com gzip (o `pandas` lê direto, pela extensão),
785 colunas: o rótulo e os 784 pixels, com a intensidade original, inteiro de
0 (fundo) a 255. Os pixels vêm linha a linha: `pixel_NNN` é o pixel da linha
`i` e coluna `j` da imagem, com `NNN = 28*i + j`. O gzip é gravado com
`mtime=0`, para o arquivo sair com os mesmos bytes a cada execução.

| Original | Traduzida |
|---|---|
| rótulo (arquivo `*-labels-idx1-ubyte`) | `digito` |
| pixel `k` da imagem (arquivo `*-images-idx3-ubyte`) | `pixel_000` … `pixel_783` |

## `USArrests.csv`, `NCI60.csv.gz` — os dois do capítulo 15 (ISLP 12)

Do capítulo 15 (*Aprendizado Não Supervisionado*, ISLP 12). O `USArrests` é
o exemplo da análise de componentes principais (12.2, figuras 12.1, 12.3 e
12.4, tabela 12.1) e volta no agrupamento hierárquico; o `NCI60` é o do
*scree plot*, das ligações do agrupamento hierárquico (figura 12.19) e da
comparação com o *k*-means (lab 12.5.4). Os dois saem de uma única execução
de `scripts/baixar-dados.py`, que lê os originais **em memória** e grava só a
versão traduzida.

### `USArrests.csv` — prisões nos 50 estados dos EUA, 1973

Prisões por 100.000 habitantes por homicídio, agressão e estupro, e o
percentual de população urbana, nos 50 estados dos EUA em 1973.

**Origem.** O conjunto `USArrests` do pacote `datasets` do R, pelo espelho
Rdatasets
(`https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/USArrests.csv`).
Não está no site do livro nem no *wheel* do `ISLP` (conferido); o ISLP o
carrega do R. Fontes primárias, segundo a documentação do R: McNeil,
*Interactive Data Analysis* (1977), a partir do *World Almanac and Book of
Facts* 1975 (crimes) e do *Statistical Abstracts of the United States* 1975
(população urbana).

| Original | Traduzida | Unidade |
|---|---|---|
| `rownames` (nome da linha no R) | `estado` | |
| `Murder` | `homicidio` | prisões por 100.000 habitantes |
| `Assault` | `agressao` | prisões por 100.000 habitantes |
| `UrbanPop` | `pop_urbana` | % da população em área urbana |
| `Rape` | `estupro` | prisões por 100.000 habitantes |

Os nomes dos estados vão para o exônimo em português onde há um de uso
corrente; os demais ficam como no original.

| Original | Traduzido | Original | Traduzido |
|---|---|---|---|
| Alaska | Alasca | New Mexico | Novo México |
| California | Califórnia | New York | Nova York |
| Florida | Flórida | North Carolina | Carolina do Norte |
| Georgia | Geórgia | North Dakota | Dakota do Norte |
| Hawaii | Havaí | Pennsylvania | Pensilvânia |
| Louisiana | Luisiana | South Carolina | Carolina do Sul |
| Mississippi | Mississípi | South Dakota | Dakota do Sul |
| New Hampshire | Nova Hampshire | Virginia | Virgínia |
| New Jersey | Nova Jersey | West Virginia | Virgínia Ocidental |

**A ordem das linhas é a do original**, alfabética pelo nome em inglês — por
isso `Washington` fica entre `Virgínia` e `Virgínia Ocidental`, e as
`Carolina`/`Dakota` estão entre os `N`. Nenhum valor numérico mudou.

**Maryland tem `pop_urbana` = 67, e fica assim.** A documentação do R
registra que esse valor é um erro de transcrição (o correto seria 76). É o
dado que o ISLP usa, e as figuras e tabelas do livro saem dele; corrigi-lo
aqui faria os números do capítulo deixarem de bater com o livro-texto.
`test_usarrests_preserva_maryland` trava isso.

### `NCI60.csv.gz` — 64 linhagens de câncer × 6.830 genes

Expressão gênica medida por microarranjo em 64 linhagens de células de
câncer, 6.830 genes por linhagem, com o tipo de câncer de cada uma.

**Origem.** O *wheel* do pacote `ISLP` **0.4.1** (o mesmo do `Default` e do
`Hitters`; ver a seção do `Default` sobre por que isso não torna o `ISLP`
uma dependência). Dois arquivos do pacote, lidos em memória e juntados num
só: `ISLP/data/NCI60data.npy` (a matriz 64 × 6.830, `float64`) e
`ISLP/data/NCI60labs.csv` (a coluna `label`, o tipo de cada linhagem).

**Formato.** CSV comprimido com gzip (o `pandas` lê direto, pela extensão),
gravado com `mtime=0` para sair com os mesmos bytes a cada execução
(cerca de 877 KB). São 6.831 colunas: `tipo` primeiro, depois `gene_0000` …
`gene_6829`, na ordem das colunas da matriz original.

| Original | Traduzida |
|---|---|
| `label` (de `NCI60labs.csv`) | `tipo` |
| coluna `k` da matriz (de `NCI60data.npy`) | `gene_0000` … `gene_6829` |

As categorias de `tipo`, com a contagem de linhagens:

| Original | Traduzida | Linhagens |
|---|---|---|
| `NSCLC` (câncer de pulmão de células não pequenas) | `pulmão` | 9 |
| `RENAL` | `rim` | 9 |
| `MELANOMA` | `melanoma` | 8 |
| `BREAST` | `mama` | 7 |
| `COLON` | `cólon` | 7 |
| `LEUKEMIA` | `leucemia` | 6 |
| `OVARIAN` | `ovário` | 6 |
| `CNS` (sistema nervoso central) | `SNC` | 5 |
| `PROSTATE` | `próstata` | 2 |
| `UNKNOWN` | `desconhecido` | 1 |
| `K562A-repro` | `K562A-repro` | 1 |
| `K562B-repro` | `K562B-repro` | 1 |
| `MCF7A-repro` | `MCF7A-repro` | 1 |
| `MCF7D-repro` | `MCF7D-repro` | 1 |

São 14 categorias. As quatro `-repro` **não são traduzidas**: são nomes de
linhagem, réplicas da leucemia K562 e da linhagem de mama MCF7.

**O CSV não é o `.npy` bit a bit.** Escrever os `float64` em texto e lê-los de
volta muda 337 dos 437.120 valores, cada um em menos de 1e−32; nada que se
veja em proporção de variância explicada nem em agrupamento. A fonte do
material é o CSV. Não leia com `float_precision="round_trip"` para tentar
recuperar o `.npy`: o arquivo já foi gravado com a representação padrão do
`pandas`.

## `Khan.csv.gz` — tumores de pequenas células redondas e azuis (capítulo 16, ISLP 9.6.5)

Expressão gênica medida por microarranjo de cDNA em 83 amostras de quatro
tipos de tumor infantil de pequenas células redondas e azuis, 2.308 genes por
amostra. É o exemplo de SVM com mais de duas classes do capítulo 16 (lab 9.6.5
do ISLP), com p ≫ n.

**Origem.** O *wheel* do pacote `ISLP` **0.4.1** (o mesmo do `Default`, do
`Hitters` e do `NCI60`; ver a seção do `Default` sobre por que isso não torna
o `ISLP` uma dependência). Quatro arquivos do pacote, lidos em memória por
`khan_do_pacote()`, em `scripts/baixar-dados.py`, e juntados num só:

| Arquivo do pacote | Forma | Conteúdo |
|---|---|---|
| `ISLP/data/Khan_xtrain.csv` | 63 × 2.308 | expressão, colunas `V1` … `V2308` |
| `ISLP/data/Khan_xtest.csv` | 20 × 2.308 | idem |
| `ISLP/data/Khan_ytrain.csv` | 63 × 1 | coluna `x`, o tipo de tumor codificado de 1 a 4 |
| `ISLP/data/Khan_ytest.csv` | 20 × 1 | idem |

O dado original é de Khan et al. (2001), *Classification and diagnostic
prediction of cancers using gene expression profiling and artificial neural
networks*, *Nature Medicine* 7(6):673–679, doi 10.1038/89044.

**Formato.** CSV comprimido com gzip (o `pandas` lê direto, pela extensão),
gravado com `mtime=0` para sair com os mesmos bytes a cada execução (845.601
bytes, gravado no container). São 83 linhas e 2.310 colunas; os valores de
expressão voltam do CSV exatamente iguais aos do pacote (`np.array_equal`,
conferido).

| Original | Traduzida |
|---|---|
| (arquivo de origem: `_xtrain`/`_ytrain` ou `_xtest`/`_ytest`) | `conjunto`: `"treino"` nas 63 primeiras linhas, `"teste"` nas 20 últimas |
| `x` (de `Khan_ytrain.csv` e `Khan_ytest.csv`) | `tumor` |
| `V1` … `V2308` | `gene_0000` … `gene_2307` |

A coluna `conjunto` preserva a divisão treino/teste dos autores do artigo; a
ordem das linhas dentro de cada conjunto é a do pacote.

**A correspondência entre o código 1–4 e o tipo de tumor.** Ela **não está na
documentação do pacote**: a página do conjunto no Rdatasets
(`Rdatasets/doc/ISLR/Khan.html`) diz só "four distinct types of small round
blue cell tumors". Foi deduzida pelas contagens. No treino, as quatro
contagens são distintas (8, 23, 12 e 20), e só uma atribuição as casa com as
do artigo; o teste confirma:

| Código | `tumor` | Sigla na página | Treino | Teste |
|---|---|---|---|---|
| 1 | `linfoma de Burkitt` | LB (BL no artigo) | 8 | 3 |
| 2 | `sarcoma de Ewing` | SE (EWS no artigo) | 23 | 6 |
| 3 | `neuroblastoma` | NB | 12 | 6 |
| 4 | `rabdomiossarcoma` | RMS | 20 | 5 |

A ordem é também a alfabética das siglas em inglês (BL, EWS, NB, RMS), que é
a ordem dos níveis de um fator do R.

**A conferência (2026-09-30).** As contagens do artigo foram lidas no texto
completo, na PubMed Central (PMC1282521). O artigo diz: "The 63 training
samples [...] included both tumor biopsy material (13 EWS and 10 RMS) and
cell lines (10 EWS, 10 RMS, 12 NB and 8 Burkitt lymphomas (BL; a subset of
NHL))", ou seja, 23 EWS, 20 RMS, 12 NB e 8 BL no treino; e "The test samples
contained both tumors (5 EWS, 5 RMS and 4 NB) and cell lines (1 EWS, 2 NB and
3 BL)", ou seja, 6 EWS, 5 RMS, 6 NB e 3 BL. O teste do artigo tem ainda 5
amostras que não são desses quatro tipos; elas não estão no pacote, que traz
só as 20. `khan_do_pacote()` asserta as contagens por código antes de gravar,
e `test_khan_formato` as trava no arquivo commitado.

## O que saiu

Os conjuntos da abordagem de obtenção de dados abandonada — `stocks.csv`,
`comma_delimited_stock_prices.csv`, `getting-data.html`, `iris.data`,
`spam-assuntos.csv`, `imagem-cores.jpg` e `mnist/` — saíram deste diretório.
Nenhum capítulo publicado os lia; continuam recuperáveis no histórico do git,
se algum dia forem necessários de novo.
