# pandas no trabalho com dados

**Data:** 2026-09-08
**Status:** decidido pelo autor; este documento fixa as regras e a execução
**Implementação:** em curso na branch `pandas-nos-dados` — fundação e capítulos 6, 7 e 8 concluídos (ver a nota de correção no fim)
**Precede:** `2026-09-06-reescrita-numpy-design.md`, que continua valendo para os algoritmos

## A decisão

O autor pediu, textualmente:

> *"vamos fazer algumas melhorias mesmo na parte já escrita com numpy. Sempre que formos trabalhar com dados, onde faça sentido pandas, ele deverá ser utilizado. Desde leitura de csvs, entre outros. Deixar mais perto do uso real, só não utilizar os algoritmos de machine learning já prontos do scikit ou de regressão do próprio numpy. Pensar sempre como seria um uso mais próximo da realidade."*

Hoje o livro faz o contrário: `pandas` aparece em onze arquivos e **sempre num callout de fechamento**, como "o que você usaria na vida real". A leitura de dado é feita à mão com `csv.reader`, `csv.DictReader`, `np.loadtxt` e `np.genfromtxt`; o agrupamento por símbolo da seção 7.5 é escrito com máscaras, e o callout no fim lista as linhas de `pandas` que fariam o mesmo. Esta spec inverte isso: **o `pandas` sai do callout e entra no corpo do texto**, onde o assunto é *obter, limpar, agrupar e apresentar dados*.

## O que NÃO muda

A tese do livro. **A caixa-preta que esta disciplina abre é a do modelo, não a do parser de CSV.** Escrever um leitor de CSV à mão não ensina ciência de dados — ensina *parsing*, e mal, porque a versão à mão erra com aspas, separador dentro do campo e quebra de linha (a própria seção 6.1 já avisa isso: *"nunca faça o parsing na mão"*). Escrever um gradiente descendente à mão, esse sim, ensina o que a disciplina existe para ensinar.

Portanto seguem valendo, sem exceção:

- **Nenhum algoritmo de aprendizado pronto.** Nada de `sklearn` em chunk que executa — ele continua só nos callouts de fechamento, em bloco ```` ```python ```` que não roda.
- **Nenhuma regressão pronta**, nem do `numpy`: `np.polyfit` e `np.linalg.lstsq` continuam proibidos como implementação (`np.linalg.solve` segue permitido, porque mostra as equações normais em vez de escondê-las).
- **Nada de `scipy`.**
- Os modelos continuam construídos com `numpy`, linha a linha, como a spec de 2026-09-06 fixou.

O acréscimo é de **realismo no manuseio do dado**, não de conveniência no algoritmo.

## A regra que decide cada dúvida

**`pandas` é a mesa de trabalho; `numpy` é a calculadora do modelo.**

O dado entra pelo `pandas` (ler, tipar, limpar, juntar, agrupar, resumir, apresentar), e **atravessa uma fronteira explícita** para virar `ndarray` no momento em que o modelo começa:

```python
X = df[["amigos", "horas_trabalho"]].to_numpy()   # a fronteira
y = df["minutos"].to_numpy()
beta = least_squares_fit(X, y, rng)               # daqui para a frente, numpy
```

Essa linha de fronteira é **conteúdo, não detalhe**: ela é onde o aluno vê que o modelo não sabe o que é uma coluna chamada "amigos" — ele vê uma matriz de números. Ela deve aparecer explicitamente em todo capítulo que ajusta um modelo, e a prosa deve nomeá-la na primeira vez (capítulo 7).

| `pandas` (mesa de trabalho) | `numpy` (calculadora) |
|---|---|
| ler arquivo: `read_csv`, `read_html`, `read_json`, `json_normalize` | a matriz `X` e o vetor `y` que entram no modelo |
| tipar e limpar: `parse_dates`, `na_values`, `to_numeric(errors=...)`, `dropna`, `astype` | toda a álgebra: `@`, `.T`, `solve`, `norm` |
| explorar: `describe`, `head`, `value_counts`, `corr`, `hist` | reduções e máscaras dentro do algoritmo |
| reorganizar: `groupby`, `agg`, `merge`, `sort_values`, `pivot`, `resample`, `pct_change` | o sorteio: `rng.permutation`, `rng.random`, ... |
| apresentar: a tabela final de coeficientes, de métricas, de erros-padrão | os parâmetros ajustados |

**Teste de desempate: o `pandas` está fazendo trabalho de dado ou trabalho de modelo?** `df.groupby("simbolo")["fechamento"].max()` é trabalho de dado — entra. `df.corr()` para explorar as colunas antes de modelar é trabalho de dado — entra. Calcular o gradiente com operações de `DataFrame` seria trabalho de modelo disfarçado — **não** entra.

**Onde o `pandas` não deve entrar, mesmo sendo capaz:**

- Dentro de `scratch_np/`. Os módulos recebem e devolvem `np.ndarray`, sempre. É o contrato dos capítulos entre si, e um `DataFrame` ali tornaria o algoritmo dependente de nomes de coluna.
- Onde o dado não é tabular: o MNIST (binário `.idx.gz`, lido com `np.frombuffer`) e a imagem do capítulo 17 (`PIL` → `np.asarray`). Forçar `pandas` ali seria decoração.
- Como substituto de uma lição que o capítulo existe para dar. O capítulo 7 do Grus *é* sobre trabalhar dado à mão; ver o que o `groupby` faz por baixo tem valor. A resposta não é escolher um dos dois: é **fazer à mão uma vez, mostrar a linha de `pandas` em seguida, e usar `pandas` daí em diante** (detalhe na seção do capítulo 7, adiante).

## Onde o `pandas` é apresentado ao leitor

Hoje a apresentação das ferramentas segue esta ordem: o callout do capítulo 4 mostra `numpy` de relance, a seção 6.1 faz o primeiro contato (`np.loadtxt`), e o bloco `## De listas a arrays`, que abre a 7.1, é a apresentação de verdade do `ndarray`.

Com o `pandas`, a ordem passa a ser **a ordem do trabalho real: primeiro se lê o dado, depois se calcula**.

1. **Seção 6.1 ganha o bloco `## O DataFrame`**, e é ali que o `pandas` é apresentado: o que é um `DataFrame` (colunas nomeadas, cada uma com o seu tipo — o que um array não faz), `read_csv` com `parse_dates` e `na_values`, `head`, `dtypes`, `describe`, seleção de coluna e de linha, e a inferência de tipo como **heurística, não garantia**. O texto sobre os riscos da coerção silenciosa já existe hoje no callout de fechamento da 6.1 e é bom: ele **sobe para o corpo** do bloco, porque deixa de ser curiosidade e passa a ser o aviso que acompanha a ferramenta que o leitor vai usar.
   O `np.loadtxt` **não some**: vira o contraponto curto — "quando o arquivo é uma tabela só de números e o destino é o modelo, dá para ir direto ao array" —, e o `csv.reader` continua aparecendo uma vez, para mostrar o que existe por baixo e por que não se faz à mão.
   Tamanho-alvo do bloco: 80 a 120 linhas de `.qmd`, o mesmo do `## De listas a arrays`.

2. **O bloco `## De listas a arrays` da 7.1 continua onde está**, e ganha um fecho novo: **a ponte**. Duas ou três frases mais um chunk mostrando `df[["a", "b"]].to_numpy()`, `df["y"].to_numpy()` e `.shape` — a fronteira nomeada de uma vez, para os capítulos 8 a 17 poderem citá-la em vez de reexplicar.

3. **Cada capítulo posterior cita esses dois blocos** em vez de reapresentar `read_csv` ou `groupby`, do mesmo jeito que hoje citam o bloco de arrays.

## Contratos entre capítulos

Os contratos da spec de 2026-09-06 **continuam iguais**: todas as assinaturas de `scratch_np/` recebem e devolvem `np.ndarray`. Nenhuma delas muda por causa desta spec.

O que muda é a **origem** dos dados que os módulos reexportam. Onde hoje um módulo faz

```python
from scratch import statistics as _grus
num_friends = np.array(_grus.num_friends, dtype=float)
```

ele passa a expor **também** um `DataFrame` com colunas nomeadas, e o array continua existindo:

```python
usuarios = pd.DataFrame({"amigos": ..., "minutos": ...})   # a mesa de trabalho
num_friends = usuarios["amigos"].to_numpy()                # o que o modelo consome
```

Regra: **o `DataFrame` é o que o capítulo mostra; o array é o que o modelo recebe.** Módulos que hoje só exportam arrays ganham o `DataFrame` ao lado, sem perder o array — nenhum capítulo já escrito quebra por isso.

## O que muda em cada capítulo

Concreto, para o planejador de cada capítulo não ter de redescobrir. O planejador confere contra o arquivo; esta lista é ponto de partida, não verdade final.

### Capítulo 6 — Obtendo Dados (o mais afetado)

- **6.1 Lendo Arquivos.** Recebe o bloco `## O DataFrame` (acima). O `csv.reader`/`DictReader` encolhe para uma passagem curta ("o que há por baixo, e por que não se faz à mão"); `read_csv` vira o caminho principal, lendo `dados/stocks.csv` com `parse_dates=["Date"]`. O callout de fechamento deixa de ser "na prática, `pandas`" — porque agora é o corpo do texto — e passa a ser sobre o que a conveniência esconde (a coerção silenciosa, os zeros à esquerda do CEP, `n/a` virando `NaN`), material que já existe e só muda de lugar.
- **6.2 Raspando a Web.** `BeautifulSoup` continua sendo o assunto (é raspagem, não tabela). Acrescentar, no fim, `pd.read_html` como o atalho real para tabelas em HTML, e mostrar o resultado da raspagem virando `DataFrame`.
- **6.3 Usando APIs.** `json.loads` continua; acrescentar `pd.json_normalize` para achatar o JSON aninhado numa tabela — que é o que se faz de verdade com resposta de API.
- **6.4 Twitter.** Sem execução (`eval: false`); ajustar só a prosa se ela prometer algo que mudou.

### Capítulo 7 — Trabalhando com Dados (o mais delicado)

Este capítulo **é** sobre manusear dado à mão, e a reescrita precisa preservar a lição sem virar hipocrisia ("faça à mão" seguido de "na vida real ninguém faz"). A regra para ele:

> Faz à mão **uma vez**, para mostrar o mecanismo; mostra a linha de `pandas` imediatamente ao lado; e **daí em diante, no resto do livro, usa `pandas`**.

- **7.1 Explorando.** Mantém `## De listas a arrays` e ganha a ponte `.to_numpy()`. A exploração em si (histograma, `describe`, matriz de correlação) passa a ser feita com `DataFrame` — `df.hist()`, `df.describe()`, `df.corr()` —, com o array aparecendo onde a conta é do modelo.
- **7.2 NamedTuples** e **7.3 Dataclasses.** Continuam: o argumento do Grus (um registro heterogêneo pede estrutura própria) é válido e o `dtype` único do array já foi discutido na 7.1. **Acrescentar o terceiro caminho**: uma linha de uma tabela — e é por isso que o `DataFrame` existe. Uma seção fecha apontando para a outra; ninguém precisa de código novo grande aqui.
- **7.4 Limpeza.** É o caso mais claro. `try_parse_row`, com regex e dois `try/except`, é escrito uma vez para mostrar o mecanismo e comparado com `read_csv(parse_dates=[...], na_values=["n/a"])` + `to_numeric(errors="coerce")`. **A lição fica mais forte, não mais fraca**: o texto atual já explica que a coerção do `pandas` é silenciosa e que a linha ruim *sobrevive* como `NaN` em vez de ser descartada. Isso passa a ser demonstrado com o dado real, e o `.isna().sum()` vira o hábito ensinado.
- **7.5 Manipulando.** A inversão mais visível do livro. Hoje a seção faz à mão o que o callout final lista em `pandas`: `groupby("Symbol")["Close"].max()`, `pct_change()`, `resample("ME")`. Passa a fazer com `pandas`, mantendo **um** exemplo à mão (o `max` por símbolo com máscara) para o leitor ver o que o `groupby` faz por baixo. Atenção ao `"ME"` (o `"M"` foi depreciado no `pandas` 2.2 e o texto já registra isso).
- **7.6 Reescalonamento.** `scale`/`rescale` continuam em `numpy` — são modelo, não dado. Acrescentar meia frase: o mesmo cálculo em `DataFrame` seria `(df - df.mean()) / df.std()`, e por que preferimos o array aqui (é o que o modelo consome, e a coluna constante precisa de tratamento explícito).
- **7.7 tqdm** e **7.8 PCA.** Não mudam. A PCA é modelo puro, e continua sendo a única subida de gradiente do livro (`tests/test_gradiente.py`).

### Capítulos 8 a 13 (já escritos em numpy — retrabalho pontual)

- **8 Machine Learning.** `split_data`/`train_test_split` continuam em arrays (contrato). Acrescentar, onde couber, que na prática se divide um `DataFrame` e as duas metades continuam sendo `DataFrame` — e que o modelo recebe `.to_numpy()` depois.
- **9 k-NN.** `dados/iris.data` passa a ser lido com `pd.read_csv(..., names=[...])`, o que resolve com elegância o que hoje exige dois `np.loadtxt` (um para as medidas, outro para os rótulos com `dtype=str`) e o `np.char.replace` do prefixo `"Iris-"` (vira `.str.removeprefix("Iris-")`). A fronteira aparece logo em seguida: `X = df[medidas].to_numpy()`, `y = df["especie"].to_numpy()`. A matriz de confusão final vira um `DataFrame` com índice e colunas nomeados — que é como se apresenta uma matriz de confusão de verdade.
- **10 Naive Bayes.** `dados/spam-assuntos.csv` com `read_csv` no lugar do `csv.DictReader`; a lista de `Message` continua (é o que o classificador consome). A tabela das palavras mais e menos "spammy" vira `DataFrame` ordenado — hoje é impressa à mão.
- **11 e 12 Regressão.** Os dados da DataSciencester passam a existir como `DataFrame` com colunas nomeadas (`amigos`, `minutos`, `horas_trabalho`, `doutorado`), o que torna o texto muito mais legível: hoje o leitor precisa lembrar que `inputs[:, 2]` é "horas de trabalho". A tabela final de coeficientes, erros-padrão e valores-p da 12.7 vira um `DataFrame` — é literalmente uma tabela de regressão, e é assim que ela aparece em qualquer relatório.
- **13 Regressão Logística.** Mesma coisa: `experiencia`, `salario`, `conta_paga` como colunas nomeadas. A tabela de limiares da 13.4 (hoje montada à mão) vira `DataFrame`.

### Capítulos 14 a 17 (ainda não escritos — já nascem assim)

- **14 Árvores.** O maior ganho do livro inteiro: os 14 candidatos são um `DataFrame` categórico (`level`, `lang`, `tweets`, `phd`, `did_well`), e `partition_by` vira `df.groupby(atributo)` — que é exatamente o que uma árvore faz. As entropias continuam em `numpy`. Cuidado: a árvore em si (recursão, `Leaf`/`Split`) continua em Python puro/numpy.
- **15 Redes Neurais.** Pouco afetado: os dados do XOR e do Fizz Buzz são gerados, não lidos. `pandas` só se aparecer uma tabela de resultados.
- **16 Deep Learning.** MNIST é binário: `np.frombuffer`, sem `pandas`. As tabelas comparativas de perda/acurácia por epoch, sim, viram `DataFrame`.
- **17 Clustering.** A imagem é `numpy`. Os 20 pontos dos encontros podem ser `DataFrame`; a tabela de erro por *k* vira `DataFrame`.

## Ambiente

`pandas` passa a ser dependência **direta**, declarada em `pyproject.toml`:

```toml
"pandas>=2,<3",               # a mesa de trabalho dos dados (caps. 6-17)
```

**O teto `<3` não é burocracia.** O `CLAUDE.md` deste projeto registra que, no livro irmão, *"o pandas 3 quebrou dois exemplos sem levantar exceção, só devolvendo a resposta errada"*. É a classe de falha mais cara deste projeto, e o teto existe por causa dela.

Sequência obrigatória: editar `pyproject.toml` → `make lock` → `make build` → `uv sync --frozen` (para o `.venv` do host, que é onde os agentes verificam).

Duas armadilhas de versão a respeitar no texto, porque o material antigo da internet ensina errado:

- `resample("M")` foi depreciado no `pandas` 2.2 em favor de `"ME"` (*month end*). O livro já registra isso.
- `df.append` não existe mais; é `pd.concat`.

## Testes novos (`tests/test_pandas.py`)

Mesma disciplina de `test_scratch_np.py`, com exceções que exigem motivo escrito:

1. **`pandas` não entra em `scratch_np/`.** Nenhum módulo do pacote importa `pandas` — exceto os que reexportam dados, que ganham entrada em `EXPORTA_DATAFRAME` com o motivo (o padrão de `REEXPORTA_DADOS`).
2. **A fronteira é explícita.** Em todo capítulo que ajusta um modelo, se há `DataFrame`, há `.to_numpy()` (ou `.values`) em algum chunk — o dado não atravessa para o modelo por acidente.
3. **Nenhum `csv.reader`/`csv.DictReader` sobra fora dos lugares registrados.** O dicionário `CSV_A_MAO` guarda os poucos pontos em que ler à mão é a lição (6.1 e 7.4), cada um com o motivo.
4. **Nenhum chunk executável usa `sklearn`, `scipy`, `np.polyfit` ou `np.linalg.lstsq`** — a proibição da spec anterior, agora com teste próprio para `polyfit`/`lstsq`, que hoje não têm guarda.
5. Os testes de `test_scratch_np.py` continuam valendo sem mudança.

## Processo e ordem de execução

O processo da casa não muda: **um capítulo por vez**, planejador (Opus, com o mapa no prompt) → implementador → revisor → correções, com os planos em `docs/superpowers/plans/2026-09-08-pandas-capNN.md`. As regras de verificação são as mesmas (`executar-secoes.py`, `executar-notebooks.py`, `pytest`; só quem coordena renderiza).

Ordem recomendada, e o motivo de cada posição:

| Ordem | Capítulos | Por quê |
|---|---|---|
| 1 | **Fundação**: `pyproject.toml`, `make lock`, `make build`, `tests/test_pandas.py` | nada mais roda sem a dependência |
| 2 | **6** | apresenta o `DataFrame`; todos os outros citam esse bloco |
| 3 | **7** | a ponte `.to_numpy()` e o `groupby`; é a referência de vocabulário |
| 4 | **9, 10** | leitura de arquivo real (Iris, spam) — o ganho mais direto |
| 5 | **11, 12, 13** | colunas nomeadas e as tabelas de resultado |
| 6 | **8** | o menor retrabalho; pode vir junto com o 11 |
| 7 | **14 a 17** | já nascem com `pandas`, seguindo a spec de numpy **e** esta |

Os capítulos 14 a 17 ainda não existem em `numpy`: para eles, **as duas specs valem juntas**, e o planejador deve ler as duas. O documento `docs/superpowers/plans/2026-09-08-retomada-caps-14-17.md` traz o mapa de cada um.

## Riscos

1. **Hipocrisia pedagógica.** O risco maior não é técnico: é o livro dizer "escreva do zero" e, na página seguinte, chamar uma função pronta. A defesa é a fronteira desta spec, dita em voz alta no capítulo 7 e repetida onde importa — *o que é do dado vai para o `pandas`; o que é do modelo você escreve*. Se um revisor não conseguir explicar por que uma chamada de `pandas` está de um lado da linha, ela está do lado errado.
2. **Números mudam.** Trocar `csv.reader` + `float()` por `read_csv` muda dtypes (`int64` onde antes havia `float`), a ordem das linhas em alguns agrupamentos, e o tratamento de valores ausentes. **Todo número afirmado na prosa dos capítulos 6 a 13 precisa ser reconferido**, e essa é a maior parte do trabalho — a mesma lição da reescrita em `numpy`.
3. **Escopo inflando.** É tentador reescrever o capítulo 7 inteiro em `pandas`. Não: ele é o capítulo que ensina o mecanismo. A regra "à mão uma vez, `pandas` ao lado, `pandas` daí em diante" é o limite.
4. **O `pandas` sabe demais.** `df.corr()`, `df.describe()`, `pct_change()` são estatística pronta — e são aceitáveis, porque estatística é assunto de Bases 3, assumido como tema (ver a restrição no `CLAUDE.md`). Mas `df.rolling().mean()` para suavizar uma série antes de um modelo, por exemplo, é uma decisão de modelagem: aí a conta é nossa.
5. **Tamanho do diff.** São doze capítulos e dois pacotes. Fazer tudo numa sessão estoura o limite da API — foi o que aconteceu na reescrita em `numpy`, e a lição está registrada em `2026-09-08-retomada-caps-14-17.md`.

## Decisões registradas

| Decisão | Escolha | Por quê |
|---|---|---|
| Onde o `pandas` entra | ler, limpar, agrupar, apresentar | é o trabalho de dado, e é assim no uso real |
| Onde não entra | dentro de `scratch_np/`, no modelo, no dado não tabular | o algoritmo é o que a disciplina ensina |
| A fronteira | `.to_numpy()` explícito, nomeado no cap. 7 | o modelo não conhece nomes de coluna — o aluno precisa ver isso |
| Apresentação | bloco `## O DataFrame` na 6.1 | primeiro se lê o dado, depois se calcula |
| Capítulo 7 | à mão uma vez, `pandas` ao lado, `pandas` depois | preserva a lição sem virar hipocrisia |
| `sklearn`, `scipy`, `polyfit`, `lstsq` | continuam proibidos na implementação | a decisão original do autor, reafirmada |
| Versão | `pandas>=2,<3` | o pandas 3 já quebrou o livro irmão em silêncio |

---

## Nota de correção — 2026-09-08, depois dos capítulos 6 e 7

Escrita durante a execução, contra medições. **Onde esta nota discorda do corpo da spec, é ela que vale** — o corpo foi escrito antes de o `pandas` ser instalado.

**1. A linha que esta spec sugere para a 7.4 tem os dois argumentos errados.** O texto propõe comparar `try_parse_row` com `read_csv(..., parse_dates=[...], na_values=["n/a"])`. Medido, com `pandas` 2.3.3:

- **`na_values=["n/a"]` é redundante.** `n/a` já está na lista padrão de marcadores nulos (`pandas._libs.parsers.STR_NA_VALUES`). O marcador que *não* está, e que o livro já usava em `precos_com_erro.txt`, é `N/D` — e com ele a coluna inteira vira `object`, `Series.sum()` **concatena strings** (`'1250.00N/D980.50'`) e nada avisa. É material melhor, e é o que os capítulos 6 e 7 passaram a usar.
- **`parse_dates` não faz nada sobre esse arquivo, e não avisa.** A linha `FB,6/20/3014` estoura o `datetime64[ns]` (`pd.Timestamp.max` é 2262-04-11), o `pandas` desiste da coluna inteira e a devolve como `object`. Zero avisos, medido com `warnings.simplefilter("always")`.

**2. O capítulo 7 inverte de um jeito que esta spec não previu, e a favor dela.** Com `pd.to_datetime(..., errors="coerce")` seguido de `dropna()`, sobram **4** linhas — contra as **5** de `try_parse_row`. Ou seja: **o `pandas` pega o outlier de ano 3014 que a função à mão deixou passar.** O callout *O erro que passa pelo filtro* deixa de ser curiosidade e vira a causa do silêncio do `parse_dates`. A 7.4 **cresce** cerca de sessenta linhas em vez de encolher, e passa a ser a melhor seção do capítulo: quatro leitores diante da mesma linha ruim, cada um com a sua noção de dado ruim.

**3. A 7.5 guarda dois exemplos à mão, não um.** A spec nomeia o `max` por símbolo. Ficou também o `day_over_day_changes` com as fatias deslocadas, porque a função mora em `scratch_np/working_with_data.py` e tirar o chunk deixaria o módulo com código que o livro não mostra.

**4. `pd.read_html` exige `flavor="bs4"`** neste projeto: o padrão é `lxml`, que não está no `uv.lock`. Não é contorno — é ganho, porque o `read_html` passa a rodar sobre o mesmo BeautifulSoup + `html5lib` que a seção 6.2 acabou de apresentar. HTML literal também precisa de `io.StringIO`, senão vem `FutureWarning`.

**5. O bloco `## O DataFrame` entra no meio da 6.1, não no começo.** A spec pede a ordem do trabalho real ("primeiro se lê o dado, depois se calcula"), o que empurraria o bloco para o topo. Três coisas empurram de volta, e a decisão foi documentada no plano do capítulo 6: o `read_csv` só é convincente contra o laço que ele substitui; o `np.loadtxt` não pode vir antes, senão a seção ensina o leitor mais restrito e depois desdiz; e o fecho da 6.1 precisa continuar amarrando o `numpy` ao bloco *De listas a arrays* da 7.1, que o cita nominalmente. A ordem publicada é **`csv` → `DataFrame` → `array`**.

**6. O bloco `## O DataFrame` saiu com 133 linhas**, acima das 80 a 120 que a spec estipula. Três subtítulos quebram a leitura e cada chunk ensina uma coisa; o corte, se um dia for preciso, é o par do TSV de brinquedo.

**7. `scratch_np/working_with_data.py` não mudou uma linha, e `EXPORTA_DATAFRAME` continua vazio.** Mas a 7.5 era o **único** `.qmd` do livro que importava esse módulo, e a importação saiu com a conversão: hoje `grep -rn "working_with_data" content/` não devolve nada. Nenhuma função ficou órfã — todas continuam num chunk do capítulo 7 —, mas a convenção *"a seção implementa, a próxima importa"* fica sem demonstração para esse módulo **até os capítulos 9 e 13 importarem `rescale`**. Quem converter esses dois deve fechar isso.

### Acréscimo — 2026-09-09, depois do capítulo 8

**8. A ordem de execução mudou por decisão do autor: o capítulo 8 veio logo depois do 7**, antes dos 9 a 13. A spec o punha em sexto lugar ("o menor retrabalho; pode vir junto com o 11"). Duas consequências:

- **A primeira matriz de confusão do livro é a do capítulo 8, não a do 9.** A spec atribui ao capítulo 9 a ideia de apresentá-la como `DataFrame` com índice e colunas nomeados; como o 8 chegou antes, o **idioma nasce na 8.4** e o capítulo 9 passa a citá-lo em vez de inventar outro.
- **Ficam duas pendências para os capítulos 9 e 13**, registradas nos "Desvios na implementação" do plano do capítulo 8: a matriz do 9 deve ser montada no idioma da 8.4; e a frase da 8.3 sobre o 9 e o 13 "atravessarem a fronteira primeiro" foi retirada, porque hoje seria falsa — os dois montam `X` e `y` sem passar por `DataFrame` nenhum —, e volta quando eles forem convertidos.

**9. O capítulo 8 é o que menos muda, e isso é a resposta certa.** Quatro das seis seções não têm trabalho de dado nenhum (8.1, 8.2 e 8.6 não têm chunk executável; 8.5 são duas figuras de `numpy` puro). O total foi quatro chunks novos, uma tabela markdown que virou chunk e cerca de dez emendas de prosa — e **nenhum número afirmado pelo capítulo mudou**. O parágrafo que a spec dedica a ele previa isso corretamente.

**10. `scratch_np/machine_learning.py` não mudou, e o motivo vale para os próximos.** Medido: `split_data(df, ...)` falha **alto** (`KeyError`, porque o `isinstance(data, np.ndarray)` é falso e `df[i]` procura coluna), mas `train_test_split(df, ...)` roda **em silêncio** — o `np.asarray(xs)` da primeira linha devolve um array de `dtype: object`, e o erro só aparece na primeira multiplicação. Isso virou material do capítulo (o callout *A fronteira acontece com ou sem você*) em vez de virar um terceiro ramo na função: o contrato em arrays é o que sete importações dos capítulos 9, 10 e 13 dependem.
