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
| 6 | 23/09 | 7 — O que é aprendizado estatístico | 2 |
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

São **70 seções novas**. O material fecha com **17 capítulos, 91 seções, 108 `.qmd`**.

### 6 — Dados: tipos, dados retangulares e `pandas` (6 seções, sem ISLP)

1. Elementos de dados estruturados — numérico contínuo e discreto; categórico nominal, ordinal e binário; `dtypes`; `astype("category")`
2. Dados retangulares — o `DataFrame`, `shape`, `head`, `info`, o índice, `.loc` e `.iloc`
3. Lendo e tipando um arquivo real — `read_csv`, `parse_dates`, `na_values`, `to_numeric(errors=...)`; a inferência de tipo como heurística, não garantia
4. Limpando e transformando — faltantes, duplicatas, `isna`, `dropna`, `fillna`
5. Agrupando e resumindo — `groupby`, `agg`, `value_counts`, `describe`, `merge`
6. Da tabela para o modelo — `X` e `y`, e por que o modelo não sabe o que é uma coluna chamada "população"

É o único capítulo modelado no livro irmão, e o único que usa dado brasileiro (ver "Dados e dependências").

### 7 — O que é aprendizado estatístico (6 seções, ISLP 2)

1. Estimar *f*: predição e inferência — ISLP 2.1, 2.1.1
2. Como estimar *f*: paramétrico e não paramétrico — 2.1.2
3. Precisão contra interpretabilidade — 2.1.3
4. Supervisionado e não supervisionado, regressão e classificação — 2.1.4, 2.1.5
5. Medindo a qualidade do ajuste, e o compromisso viés-variância — 2.2.1, 2.2.2
6. Classificação: taxa de erro e o classificador de Bayes — 2.2.3

É o capítulo que fixa `train_test_split` e a distinção treino/teste, usada por todos os seguintes.

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
| `test_o_conteudo_nao_comenta_a_propria_escrita` | intacto, e vale para todo capítulo novo |
| `test_todo_link_interno_para_qmd_resolve` | intacto |
| `test_scratch.py`, `test_gradiente.py` | intactos — são dos capítulos 1 a 5 |
| `test_dados.py` | cresce com os conjuntos do ISLP |

`references.bib` ganha a entrada `james2023`.

## Os capítulos 1 a 5

Continuam intocados, como a spec da ruptura fixou, e continuam citando o Grus. A rodada de reescrita deles agora tem alvo: com o `scikit-learn` como ferramenta, a álgebra linear em `List[float]` do capítulo 4 e o gradiente descendente à mão do capítulo 5 deixam de ser pré-requisito de qualquer coisa — sobrevivem como fundamento, não como maquinário. O que fazer com eles é decisão de outra spec, depois que os doze capítulos novos existirem.

## Ordem de execução

**O capítulo 6 é escrito primeiro e com urgência: a aula é em 16/09.** Ele é escrito antes dos demais e, uma vez revisado, **passa a ser o modelo de estilo da casa** — o papel que o capítulo 9 tinha na abordagem antiga. Abertura de seção, posição dos callouts, formato de citação, justificativa de semente em chunk estocástico: quem escrever o capítulo 8 copia a forma do 6 em vez de reinventá-la.

1. **Fundação** — `references.bib` com `james2023`; `LIVRO` com os 17 capítulos; stubs gerados e registrados no `_quarto.yml`; testes novos; `scipy` declarado; `scripts/baixar-dados.py` estendido e os dados commitados.
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
