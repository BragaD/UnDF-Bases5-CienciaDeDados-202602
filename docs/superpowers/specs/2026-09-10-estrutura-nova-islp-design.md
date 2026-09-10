# A estrutura nova — dados, `pandas` e o ISLP

**Data:** 2026-09-10
**Status:** decidido com o autor no brainstorming; este documento fixa a ementa, a tese e as consequências
**Sucede:** `2026-09-10-ruptura-com-o-grus-design.md`, que limpou o terreno e deixou tudo isto em aberto

## A decisão

O autor observou que a turma não tem base sólida nem de estatística nem de Python, e definiu o caminho: **uma aula de fundamentos de dados** — tipos de dados, dados retangulares e `pandas`, no molde do capítulo 1 do livro irmão *Bases 3 — Estatística* — e, a partir dali, **machine learning a partir do ISLP**:

> James, Witten, Hastie, Tibshirani e Taylor. *An Introduction to Statistical Learning with Applications in Python*. Springer, 2023. O PDF está em `livros/ISLP_website.pdf`.

Esta spec fecha as três decisões que a spec da ruptura deixou explicitamente em aberto: a fonte, a postura sobre implementação, e o escopo com a numeração.

## A tese: o modelo é uma ferramenta que se escolhe, se ajusta e se julga

O que a disciplina ensina é **escolher, ajustar e julgar** — não implementar. Em uma linha, e ela decide toda dúvida:

- **`scikit-learn` de ponta a ponta. Nada é escrito à mão.** Todo capítulo é conceito mais `fit`/`predict`/`cross_val_score`/`Pipeline` sobre dado real. A matemática aparece em fórmula e em gráfico, nunca em implementação. Não há lista de exceções, e criar uma é reabrir a decisão que o material acabou de fechar.
- **Nada de inferência.** Erro-padrão de coeficiente, estatística *t*, valor-p e teste de hipótese ficam fora — decisão explícita do autor. Isso enxuga o ISLP 3.1.2 e 3.1.3 e elimina o capítulo 13 do livro. Consequência: **`statsmodels` não entra**, e o capítulo de regressão avalia o ajuste por R² e erro, não por significância de coeficiente.
- **O pacote `ISLP` não entra.** Ele existe para os labs do livro (`load_data`, `ModelSpec`), traz uma API que só existe ali e quebraria a regra de dados commitados. Os conjuntos do ISLP entram como CSV em `dados/`.

### Emenda de 2026-09-10, no início do capítulo 7: a fidelidade ao ISLP tem precedência

O autor pediu, ao abrir o capítulo 7: *"não se prenda muito na exigência de só scikit-learn. pode seguir bem o capítulo do ISLP."*

A regra do `scikit-learn` de ponta a ponta existia para impedir que o material voltasse a implementar algoritmo à mão. **Ela não existe para deformar o conteúdo do livro-texto**, e no capítulo 2 do ISLP ela deformaria: o lab é um tutorial de `numpy`, e as figuras 2.9 a 2.12 — o coração do capítulo — são construídas com *smoothing splines*, que o `scikit-learn` não tem.

Portanto: **quando a fidelidade ao capítulo do ISLP e a preferência pelo `scikit-learn` colidirem, ganha a fidelidade.** Uma biblioteca que o conteúdo do capítulo exige entra, **registrada em `BIBLIOTECA_LIBERADA` com o motivo escrito** — o mesmo mecanismo que já libera o `scipy` para o dendrograma do capítulo 15.

O que a emenda **não** afrouxa:

- **Nada de inferência.** Segue valendo: sem erro-padrão de coeficiente, sem estatística *t*, sem valor-p. Não é regra de ferramenta, é de escopo da disciplina.
- **Nada de algoritmo de aprendizado escrito à mão.** A tese continua sendo escolher, ajustar e julgar.
- **Biblioteca entra por necessidade, não por conveniência.** Se o `scikit-learn` faz o que a seção precisa, é ele que se usa. A exceção é para o que ele não faz.
- **`statsmodels` segue fora**, porque o que ele acrescentaria é justamente a inferência que a disciplina não faz.
- **O pacote `ISLP` segue fora**, porque quebraria a regra de dados commitados.

Isto não é "usar biblioteca porque é mais fácil". É a decisão de que a competência a formar é a de quem **usa** o ferramental, e o tempo de aula é escasso: onze encontros para cobrir regressão, classificação, reamostragem, regularização, árvores, ensembles, redes e não supervisionado.

### O que segue proibido

| Pode e deve | Não pode |
|---|---|
| `scikit-learn` inteiro: estimadores, `Pipeline`, `ColumnTransformer`, `GridSearchCV`, métricas | `statsmodels` — a disciplina não faz inferência |
| `pandas` para todo trabalho de dado | o pacote `ISLP` |
| `numpy` para o que for conta de array | `torch` — redes convolucionais e recorrentes são da disciplina de Deep Learning |
| `matplotlib` para todo gráfico | `scipy`, **exceto** o dendrograma do capítulo 15 (ver "Dados e dependências") |

**A fronteira `.to_numpy()` morreu com a spec de pandas, e não volta.** O `scikit-learn` aceita `DataFrame` direto e preserva os nomes das colunas em `feature_names_in_` — passar a tabela é melhor que convertê-la, e o nome da coluna sobrevive até a importância de variáveis do capítulo 13.

## A ementa

Onze aulas de conteúdo, doze capítulos novos. A aula de gradiente descendente ocorreu em 09/09, uma semana à frente do cronograma publicado, então a aula 5 (16/09) abre a estrutura nova.

| Aula | Data | Capítulo | ISLP |
|---|---|---|---|
| 5 | 16/09 | 6 — Dados: tipos, dados retangulares e `pandas` | — |
| 6 | 23/09 | 7 — O que é aprendizado estatístico | 2 (inclusive o lab 2.3) |
| 7 | 30/09 | 8 — Regressão linear | 3 |
| 8 | 07/10 | 9 — Classificação | 4 |
| 9 | 14/10 | **HPE** — grupos no seminário, com o capítulo 17 de roteiro | — |
| 10 | 21/10 | 10 — Reamostragem | 5 |
| 11 | 28/10 | 11 — Seleção de modelos e regularização | 6 |
| 12 | 04/11 | 12 — Árvores de decisão | 8.1 |
| 13 | 11/11 | 13 — Bagging, florestas e boosting | 8.2 |
| 14 | 18/11 | 14 — Redes neurais | 10 |
| 15 | 25/11 | 15 — Aprendizado não supervisionado | 12 |
| 16 | 02/12 | 16 — Máquinas de vetores de suporte · revisão | 9 |
| — | — | 17 — Um problema do começo ao fim | — |

**O capítulo 17 não ocupa aula.** Ele é a leitura do seminário, publicada junto das instruções em 07/10, e o roteiro do HPE de 14/10 — que hoje é hora protegida sem material nenhum. Suas três primeiras seções dependem só dos capítulos 6 a 9 e servem ao HPE; o resto (`Pipeline`, validação cruzada, `GridSearchCV`) casa com os capítulos 10 e 11, que chegam quando os grupos começam a modelar de fato, em novembro.

### O que fica de fora, e por quê

| ISLP | Assunto | Motivo |
|---|---|---|
| 7 | Além da linearidade: polinômios, degraus, splines | pouco uso em trabalho tabular hoje; não cabe em onze aulas |
| 11 | Análise de sobrevivência | fora do escopo de um primeiro curso de ML |
| 13 | Testes múltiplos | é inferência, que a disciplina não faz |
| 6.3.2 | Partial least squares | PCR cobre a ideia de redução de dimensão |
| 8.2.4 | BART | não há implementação no `scikit-learn` |
| 10.3, 10.5 | Redes convolucionais e recorrentes | exigem `torch`; são a matéria da disciplina de Deep Learning |
| 3.1.2, 3.1.3 (parte) | Erro-padrão, *t* e valor-p dos coeficientes | a disciplina não faz inferência |

## Os capítulos, seção a seção

São **71 seções novas**. O material fecha com **17 capítulos, 92 seções, 109 `.qmd`**.

### 6 — Dados: tipos, dados retangulares e `pandas` (6 seções, sem ISLP)

1. Elementos de dados estruturados — numérico contínuo e discreto; categórico nominal, ordinal e binário; `dtypes`; `astype("category")`
2. Dados retangulares — o `DataFrame`, `shape`, `head`, `info`, o índice, `.loc` e `.iloc`
3. Lendo e tipando um arquivo real — `read_csv`, `parse_dates`, `na_values`, `to_numeric(errors=...)`; a inferência de tipo como heurística, não garantia
4. Limpando e transformando — faltantes, duplicatas, `isna`, `dropna`, `fillna`
5. Agrupando e resumindo — `groupby`, `agg`, `value_counts`, `describe`, `merge`
6. Da tabela para o modelo — `X` e `y`, e por que o modelo não sabe o que é uma coluna chamada "população"

É o único capítulo modelado no livro irmão, e o único que usa dado brasileiro (ver "Dados e dependências").

### 7 — O que é aprendizado estatístico (7 seções, ISLP 2)

1. O array: forma, fatias, máscaras, reduções e sorteio — ISLP 2.3
2. Estimar *f*: predição e inferência — 2.1, 2.1.1
3. Como estimar *f*: paramétrico e não paramétrico — 2.1.2
4. Precisão contra interpretabilidade — 2.1.3
5. Supervisionado e não supervisionado, regressão e classificação — 2.1.4, 2.1.5
6. Medindo a qualidade do ajuste, e o compromisso viés-variância — 2.2.1, 2.2.2
7. Classificação: taxa de erro e o classificador de Bayes — 2.2.3

É o capítulo que fixa `train_test_split` e a distinção treino/teste, usada por todos os seguintes.

**A seção 7.1 é o lab 2.3 do ISLP**, e existe pela mesma razão que o bloco do `DataFrame` no capítulo 6: **todo estimador do `scikit-learn` devolve `ndarray`**, e sem uma apresentação o material passaria onze capítulos usando um objeto que ninguém apresentou. A turma não tem base de Python — a spec parte disso. É apresentação curta e a serviço do resto, não um tutorial de `numpy`.

### 8 — Regressão linear (7 seções, ISLP 3)

1. Regressão linear simples — 3.1, 3.1.1
2. Avaliando o ajuste: R² e erro — 3.1.3, sem a parte de inferência
3. Regressão múltipla — 3.2
4. Preditores qualitativos — 3.3.1
5. Interação e termos não lineares — 3.3.2
6. Problemas: outliers, alavancagem e colinearidade — 3.3.3
7. Regressão linear contra *k*-vizinhos — 3.5

### 9 — Classificação (6 seções, ISLP 4)

1. Por que não regressão linear — 4.1, 4.2
2. Regressão logística — 4.3.1 a 4.3.4
3. Logística multinomial — 4.3.5
4. Modelos generativos: LDA, QDA e Naive Bayes — 4.4
5. Avaliando um classificador: matriz de confusão, precisão, revocação e ROC — 4.4.2
6. Comparando os métodos — 4.5

### 10 — Reamostragem (6 seções, ISLP 5)

1. O conjunto de validação — 5.1.1
2. Leave-one-out — 5.1.2
3. Validação cruzada *k*-fold — 5.1.3
4. Viés e variância na validação cruzada — 5.1.4
5. Validação cruzada em classificação — 5.1.5
6. O bootstrap — 5.2

### 11 — Seleção de modelos e regularização (7 seções, ISLP 6)

1. Seleção de subconjuntos — 6.1.1, 6.1.2
2. Escolhendo o modelo: Cp, AIC, BIC e validação — 6.1.3
3. Regressão ridge — 6.2.1
4. O lasso — 6.2.2
5. Escolhendo o parâmetro de regularização — 6.2.3
6. Regressão por componentes principais — 6.3.1
7. O que muda em alta dimensão — 6.4

### 12 — Árvores de decisão (5 seções, ISLP 8.1)

1. Árvores de regressão — 8.1.1
2. Podando a árvore — 8.1.1, `ccp_alpha`
3. Árvores de classificação — 8.1.2
4. Árvores contra modelos lineares — 8.1.3
5. Vantagens e desvantagens — 8.1.4

### 13 — Bagging, florestas e boosting (6 seções, ISLP 8.2)

1. Bagging — 8.2.1
2. Erro out-of-bag — 8.2.1
3. Florestas aleatórias — 8.2.2
4. Boosting — 8.2.3
5. Importância de variáveis
6. Resumo dos métodos de ensemble — 8.2.5

### 14 — Redes neurais (5 seções, ISLP 10, recorte denso)

1. Uma rede de camada única — 10.1
2. Redes multicamada — 10.2
3. Ajustando uma rede: retropropagação, gradiente estocástico e regularização — 10.7
4. `MLPClassifier` e `MLPRegressor` na prática
5. Quando usar deep learning — 10.6

**O recorte é declarado ao leitor como conteúdo**, não como decisão editorial: rede densa é o que se faz com `scikit-learn`; convolucional e recorrente pedem um framework de tensores, e é aí que a disciplina de Deep Learning começa.

### 15 — Aprendizado não supervisionado (6 seções, ISLP 12)

1. O desafio do não supervisionado — 12.1
2. Componentes principais — 12.2.1, 12.2.2
3. Proporção da variância explicada — 12.2.3, 12.2.4
4. *k*-means — 12.4.1
5. Clustering hierárquico — 12.4.2
6. Questões práticas em clustering — 12.4.3

### 16 — Máquinas de vetores de suporte (4 seções, ISLP 9)

1. Hiperplanos e o classificador de margem máxima — 9.1
2. O classificador de vetores de suporte — 9.2
3. Kernels — 9.3
4. Mais de duas classes — 9.4

### 17 — Um problema do começo ao fim (6 seções, sem ISLP)

1. O problema e o dado cru
2. Separar antes de olhar: treino, teste e vazamento
3. Pré-processamento como parte do modelo: `ColumnTransformer` e `Pipeline`
4. Comparando modelos por validação cruzada
5. Ajuste de hiperparâmetros com `GridSearchCV`
6. Reportar: a métrica certa, e o que o resultado não diz

## A citação inverte a regra antiga

**O ISLP numera as seções** — 3.3.1, 8.2.2, 12.4.1 estão no sumário. Então o callout de abertura cita o número:

```markdown
::: {.callout-note}
Esta seção corresponde à seção 8.2.2 de @james2023.
:::
```

Era exatamente o que o Grus não permitia, e a regra antiga existia porque *aquele* livro não numerava. `test_nenhuma_secao_inventa_numero_de_secao_do_grus` continua valendo e continua verde: ele só dispara quando a palavra "grus" aparece perto do número, e os capítulos 1 a 5 seguem citando o Grus enquanto existirem.

Os capítulos 6 e 17 não têm correspondência no ISLP e não trazem esse callout. É a única exceção, e ela é registrada no teste com o motivo escrito.

## O material é visual, como o ISLP

Pedido do autor, e é decisão pedagógica, não de acabamento: **o ISLP ensina por figura**. Quase todo conceito do livro tem um gráfico que o carrega — a flexibilidade contra o MSE de teste (2.9 a 2.12), o ajuste de mínimos quadrados (3.1), o caminho dos coeficientes do ridge e do lasso (6.4 e 6.6), a partição do plano por uma árvore (8.3), a margem de um SVM (9.3), o biplot de componentes principais (12.2). O material segue isso.

### A regra

**Toda seção tem pelo menos uma figura que carrega a ideia.** Figura que só decora não entra; figura que substitui um parágrafo entra. Onde o ISLP tem uma figura canônica para o conceito, a nossa **reproduz a ideia daquela figura** — com o nosso código, os nossos dados e legenda em português —, e o callout de correspondência já diz de que seção ela vem.

Isso é um salto em relação ao que existe: hoje só os capítulos 3 e 5 têm gráficos, e três chunks no material inteiro definem `figsize` na mão.

### Um estilo compartilhado, e por que ele é obrigatório

O site tem tema claro **e escuro** (`cosmo` e `darkly`), e figura de matplotlib com fundo branco estoura no escuro. Setenta seções produzindo cada uma o seu gráfico, cada chunk escolhendo o próprio tamanho e as próprias cores, dá um material que parece montado por dez pessoas.

Entra `estilo-figuras.mplstyle`, na raiz, aplicado por uma linha no chunk de setup de toda seção que desenha. Ele fixa tamanho, malha, fontes e o ciclo de cores. **Critério de aceitação, a medir na hora de escolher os valores:** fundo transparente, e texto de eixo, marcas e cores de série legíveis nos dois temas — contraste conferido contra `#FFFFFF` e contra o fundo do `darkly`, não estimado no olho.

A paleta sai de onde as páginas de `apoio/` já tiram a delas: os azuis do logo da UnDF (`#2264AF`, `#4195D1`, `#8FCEF1`, navy `#27316E`) sobre o fundo e o texto do `cosmo`. A regra de leitura das páginas de apoio — **azul é o terreno, laranja é o que se move** — vale também para as figuras: o dado é azul, o que o modelo faz por cima dele é quente.

Antes de escrever o código de qualquer gráfico, **carregue a skill `dataviz`**. Ela existe para exatamente isto: escolher a forma do gráfico, a paleta e a legenda de modo que setenta figuras leiam como um sistema só.

### As páginas interativas de `apoio/`

As duas páginas do capítulo 5 mostram o que uma página interativa faz por uma aula: o aluno mexe no passo e vê a trajetória mudar, e a lição chega antes da fórmula. Elas devem ser usadas **sempre que ajudarem** — com um critério, porque o custo é real.

**O critério: a página se justifica quando a lição é o que muda ao girar um botão.** Flexibilidade, λ, *k*, profundidade da árvore, `C` do SVM — parâmetros cuja variação *é* o conteúdo. Onde o conceito é estático, uma figura basta e a página seria enfeite caro.

**O custo, medido:** `apoio/gradiente-descendente.html` tem 2.069 linhas e `apoio/lote-minibatch-estocastico.html`, 1.160 — HTML e JavaScript escritos à mão, sem build. Cada página custa perto de um capítulo. Por isso a lista abaixo é **priorizada, não prometida**: as quatro primeiras valem o preço, e o que passar disso é bônus, escrito só se houver folga.

| Prioridade | Capítulo | A página | Figura do ISLP que ela anima |
|---|---|---|---|
| 1 | 7 | Flexibilidade contra erro: mover a flexibilidade e ver o MSE de treino cair enquanto o de teste faz a curva em U | 2.9 a 2.12 |
| 2 | 11 | Caminho dos coeficientes: mover λ e ver o ridge encolher tudo enquanto o lasso zera coeficientes um a um | 6.4, 6.6 |
| 3 | 12 | Árvore e partição: crescer e podar uma árvore vendo o plano se dividir junto | 8.3 |
| 4 | 9 | Fronteiras de decisão: logística, LDA, QDA e *k*-vizinhos sobre os mesmos pontos, com *k* ajustável | 2.16, 2.17, 4.x |
| bônus | 15 | *k*-means passo a passo, e o dendrograma com o corte móvel | 12.8, 12.11 |
| bônus | 16 | Margem, `C` e kernel | 9.3, 9.7 |

Uma página nova **copia o bloco `:root` das duas existentes** em vez de inventar outra paleta, entra em `project.resources` no `_quarto.yml`, e é linkada do `index.qmd` do capítulo — relativo no `.qmd`, absoluto no notebook, que é o que `test_toda_pagina_de_apoio_esta_publicada_e_linkada_certo` cobra.

### Seguir o ISLP de perto

O pedido do autor é explícito, e se traduz em três compromissos verificáveis:

- **A notação é a do livro**: *n* observações, *p* preditores, `X` e `y`, *f* e *f̂*, RSS, R², MSE. Nada de renomear por gosto.
- **Os exemplos são os do livro**, com os mesmos conjuntos de dados, para o aluno poder abrir o PDF no mesmo ponto. As exceções são registradas nesta spec e têm motivo — hoje só o `Boston`, substituído.
- **A ordem interna do capítulo é a do livro.** O mapa de seções acima já foi montado assim, e o callout de correspondência amarra cada seção ao seu número no ISLP.

## Dados e dependências

**Nenhum byte vem da rede em tempo de render** — a regra sobrevive intacta. Os conjuntos do ISLP são baixados **uma vez** do site do livro por `scripts/baixar-dados.py` e commitados em `dados/`, com a proveniência de cada um em `dados/README.md`.

Conjuntos previstos: `Advertising`, `Auto`, `Carseats`, `Credit`, `Default`, `Smarket`, `Hitters`, `Wage`, `Heart`, `OJ`, `Caravan`, `USArrests`, `College`, `NCI60`.

**O `Boston` é substituído.** O ISLP o usa no lab do capítulo 3; ele contém a variável `B`, construída a partir da proporção de moradores negros por bairro, e o `scikit-learn` removeu o conjunto na versão 1.2 por isso. O capítulo 8 usa **California Housing** no lugar, commitado como CSV. Consequência assumida: os números não batem com os do lab do ISLP, e o texto não comenta a substituição — ele simplesmente usa o outro conjunto.

**O capítulo 6 usa dado brasileiro.** É a única aula em que o dado pode ser familiar sem custo nenhum, e o `pandas` fica mais concreto sobre algo que o aluno reconhece. Do capítulo 7 em diante os dados são os do ISLP, para o aluno poder abrir o livro no mesmo exemplo. Isso **não** é referência a *Bases 3* — a regra de nunca citar aquela disciplina continua valendo, e o material de lá é reaproveitado sem ser mencionado.

**`scipy` deixa de ser proibido, para um uso só:** `scipy.cluster.hierarchy` no dendrograma da seção 15.5. O `AgglomerativeClustering` do `scikit-learn` agrupa mas não desenha a árvore, e o dendrograma *é* a lição daquela seção. A exceção é registrada com motivo escrito, no molde de `NAO_IMPORTAVEIS`; `scipy` passa a ser dependência declarada, com teto na major.

**As dependências hoje declaradas ficam como estão** — `beautifulsoup4`, `html5lib`, `requests`, `tqdm`, `python-dateutil` e `pillow` sobraram da abordagem antiga e nenhum capítulo novo as usa. Podá-las custa `make lock` e `make build` agora, e é limpeza que pode esperar o material existir.

## Consequências na suíte de testes

| Teste | Mudança |
|---|---|
| `LIVRO` em `scripts/gerar-stubs.py` | cresce para 17 capítulos; o stub de seção volta a ter callout de correspondência, agora com número de seção do ISLP |
| `test_cinco_capitulos` | vira `test_dezessete_capitulos` |
| `test_livro_completo_21_secoes_26_arquivos` | vira 91 seções / 108 arquivos |
| `test_um_notebook_por_capitulo` | passa a esperar 17 |
| **novo** `test_toda_secao_cita_o_islp` | todo `.qmd` de seção dos capítulos 7 a 16 traz `@james2023`. Os capítulos 1 a 5 estão fora da varredura (são da abordagem antiga e citam o Grus); os capítulos 6 e 17 são exceção registrada com motivo escrito, por não terem correspondência no ISLP |
| **novo** `test_nenhum_chunk_executavel_usa_biblioteca_proibida` | `statsmodels`, `torch` e o pacote `ISLP` não aparecem em chunk que executa; `scipy` só na exceção registrada |
| **novo** `test_todo_chunk_que_desenha_aplica_o_estilo` | todo chunk que chama `plt.` aplica `estilo-figuras.mplstyle`; sem isso uma figura sai com o fundo branco padrão e estoura no tema escuro |
| **novo** `test_toda_secao_tem_figura` | todo `.qmd` de seção dos capítulos 6 a 17 produz ao menos uma figura; seção sem figura precisa estar registrada com o motivo escrito |
| `test_o_conteudo_nao_comenta_a_propria_escrita` | intacto, e vale para todo capítulo novo |
| `test_todo_link_interno_para_qmd_resolve` | intacto |
| `test_scratch.py`, `test_gradiente.py` | intactos — são dos capítulos 1 a 5 |
| `test_dados.py` | cresce com os conjuntos do ISLP |

`references.bib` ganha a entrada `james2023`.

## Os capítulos 1 a 5

Continuam intocados, como a spec da ruptura fixou, e continuam citando o Grus. A rodada de reescrita deles agora tem alvo: com o `scikit-learn` como ferramenta, a álgebra linear em `List[float]` do capítulo 4 e o gradiente descendente à mão do capítulo 5 deixam de ser pré-requisito de qualquer coisa — sobrevivem como fundamento, não como maquinário. O que fazer com eles é decisão de outra spec, depois que os doze capítulos novos existirem.

## Ordem de execução

**O capítulo 6 é escrito primeiro e com urgência: a aula é em 16/09.** Ele é escrito antes dos demais e, uma vez revisado, **passa a ser o modelo de estilo da casa** — o papel que o capítulo 9 tinha na abordagem antiga. Abertura de seção, posição dos callouts, formato de citação, justificativa de semente em chunk estocástico: quem escrever o capítulo 8 copia a forma do 6 em vez de reinventá-la.

1. **Fundação** — `references.bib` com `james2023`; `LIVRO` com os 17 capítulos; stubs gerados e registrados no `_quarto.yml`; testes novos; `scipy` declarado; `estilo-figuras.mplstyle` na raiz, com os valores medidos contra os dois temas; `scripts/baixar-dados.py` estendido e os dados commitados.
2. **Capítulo 6**, com prioridade sobre tudo. Revisado, ele vira o modelo de estilo.
3. **Capítulos 7, 8 e 9, um por vez, na ordem do livro** — planejador, implementador, revisor, correções, como nas reescritas anteriores. A ordem importa: cada capítulo usa o vocabulário e os dados do anterior.
4. **Capítulo 17**, fora de ordem, porque tem prazo: as instruções do seminário saem em 07/10 e o HPE é em 14/10. Ele é escrito logo depois do capítulo 9, e suas seções finais apontam para os capítulos 10 e 11 ainda por vir — o que é legítimo, porque os grupos só modelam de fato em novembro.
5. **Capítulos 10 a 16**, retomando a ordem do livro.
6. **`index.qmd` da raiz** — o cronograma corrigido (a aula de 16/09 é a de dados), os temas, e a lista de referências com o ISLP.
7. **`CLAUDE.md`** — a tese nova, a regra de citação, a lista do que é proibido, e o capítulo 6 como modelo de estilo.

## O que fica em aberto

- **O cronograma publicado das aulas 1 a 4** está uma semana atrasado em relação ao que aconteceu de fato — o gradiente descendente foi em 09/09. O `index.qmd` precisa da correção, e ela depende de o autor confirmar como as aulas 1 a 4 mapearam nos capítulos 1 a 5.
- **A reescrita dos capítulos 1 a 5.**
- **A poda das dependências** que sobraram da abordagem antiga.
- **A redação da avaliação** no `index.qmd`, que hoje fala em "os modelos vistos ao longo do semestre" — genérica o bastante para sobreviver, mas que ganha precisão quando os capítulos existirem.
- **As duas páginas de `apoio/` marcadas como bônus** (capítulos 15 e 16), que só são escritas se houver folga depois dos capítulos.
- **As figuras dos capítulos 1 a 5**, que hoje não usam estilo nenhum e ficam fora de padrão quando o `estilo-figuras.mplstyle` existir. Entram na rodada de reescrita daqueles capítulos.
