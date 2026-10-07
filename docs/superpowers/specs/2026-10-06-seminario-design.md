# Seminário em grupo — desenho

**Data:** 06/10/2026 · **Prazo:** as instruções saem em **07/10/2026** (aula 8).

## O que o PID já fixa

- Peso de **40%**, apresentação em **16/12/2026** (aula 18), com arguição.
- Problema real do Kaggle; o grupo analisa o problema e os dados, aplica os métodos da disciplina e
  apresenta **o percurso, incluindo as tentativas que não funcionaram**.
- O critério **não** é o desempenho no ranking, e sim a qualidade do raciocínio: a justificativa do
  método, o que os dados sustentam e os limites do resultado.
- HPE em **14/10/2026** (aula 9), com orientação sobre delimitação do problema e plano de apresentação.

O PID fala em "competição"; o cardápio é de **conjuntos de dados** do Kaggle. A diferença não muda o
que se avalia, e o enunciado diz "conjunto de dados".

## Decisões do professor (nesta conversa)

| Decisão | Escolha |
|---|---|
| Perfil do cardápio | 4 supervisionados em tabela + 1 não supervisionado |
| Distribuição | pode repetir problema entre grupos |
| Tamanho do dado | não é critério; o aluno baixa direto do Kaggle, para conhecer a plataforma |
| Entregável | **só a apresentação** (sem notebook nem relatório entregues) |
| Grupo | **duplas** |
| Tempo | **15 min** de apresentação + **5 min** de arguição |
| Análise exploratória | **obrigatória, antes da modelagem**: descrição dos dados, tipo de cada coluna segundo a taxonomia, faltantes, extremos, gráficos descritivos |

## O cardápio

Os 12 candidatos foram baixados e medidos em 02/10/2026; a comparação está no artifact
"Cardápio do Seminário". Os cinco escolhidos:

| # | Problema | Kaggle | Tarefa | Pergunta |
|---|---|---|---|---|
| 1 | Faltas a consultas médicas | `joniarroba/noshowappointments` | classificação binária | o paciente vai faltar à consulta marcada? |
| 2 | Cancelamento de reserva de hotel | `jessemostipak/hotel-booking-demand` | classificação binária | a reserva vai ser cancelada? |
| 3 | Carros usados no Craigslist | `austinreese/craigslist-carstrucks-data` | regressão | quanto pedir por um carro usado? |
| 4 | State of Data Brazil 2024-2025 | `datahackers/state-of-data-brazil-20242025` | multiclasse ordinal | em que faixa salarial está um profissional de dados? |
| 5 | Municípios brasileiros | `crisparada/brazilian-cities` | não supervisionado (PCA e agrupamento) | que tipos de município existem no Brasil? |

### As armadilhas medidas (só na versão do professor)

Descobri-las é parte do que se avalia, então **não aparecem no enunciado do aluno**.

1. **Faltas:** 65,7% das linhas são de pacientes com mais de uma consulta (divisão aleatória põe o
   mesmo paciente no treino e no teste → divisão por paciente); 79,8% comparecem, então a acurácia
   engana; idade de −1 a 115; 5 consultas agendadas depois de ocorrerem; `No-show = "Yes"` significa
   que faltou; colunas com nome errado (`Hipertension`, `Handcap`).
2. **Hotel:** `reservation_status` determina a resposta sem erro (Canceled/No-Show ↔ 1, Check-Out ↔ 0);
   `reservation_status_date` idem; 31.994 linhas duplicadas (26,8%); `company` vazia em 112.593 linhas
   e `agent` em 16.340, ambas com vazio = "não se aplica"; `assigned_room_type` só existe no check-in.
3. **Craigslist:** 32.895 preços zero, 53 acima de um milhão, máximo de 3,7 bilhões; `county` 100%
   vazia, `size` 71,8%; `model` com 29.667 valores; hodômetro até 10 milhões; ano mínimo 1900;
   147.574 dos 265.838 `VIN` preenchidos repetem um anterior (o mesmo carro em vários anúncios). Arquivo
   de 1,4 GB: leitura com `usecols`, sem as colunas de URL e descrição.
4. **State of Data:** 5.217 linhas × 403 colunas; em média 57,2% de cada coluna vazia (perguntas
   condicionais); 354 sem faixa salarial; 13 faixas ordenadas; perguntas de opinião sobre o salário (`2.k`, `2.l.1`)
   são consequência da resposta: faixa média 4,65 entre os insatisfeitos pela remuneração, 5,66
   entre os insatisfeitos por outro motivo e 6,31 entre os satisfeitos. Não a contêm, mas pedem
   discussão.
5. **Municípios:** escalas de 0–1 (IDHM) a milhões (população) → padronizar; contagens brutas pedem
   valor por habitante; 97.934 zeros nas colunas numéricas, parte deles dado ausente; 5.578 linhas com
   2 repetidas, contra 5.570 municípios.

## O enunciado

**Arquivo:** `atividades/seminario.qmd`, renderizado por `make atividade FONTE=atividades/seminario.qmd`.
O mecanismo de duas versões das listas é reaproveitado sem mudança:

- **Versão do aluno** → `atividades/publico/seminario.pdf`, publicada no site.
- **Versão do professor** (blocos `when-meta="gabarito"`) → `atividades/seminario-gabarito.pdf`, fora
  do site: as armadilhas acima, a rubrica detalhada e perguntas de arguição por problema.

### Estrutura do enunciado

1. **O que é:** duplas; um dos cinco problemas, repetição permitida; 15 + 5 minutos em 16/12; 40% da
   nota; o ranking do Kaggle não conta.
2. **Os cinco problemas:** link, pergunta e uma frase de contexto cada. Sem as armadilhas.
3. **Roteiro da apresentação** (supervisionados), na ordem do capítulo 17:
   1. **A pergunta e a unidade:** o que é uma linha, qual a resposta, o que se sabe no momento da
      previsão.
   2. **Descrição e análise exploratória** (obrigatória, antes da modelagem):
      - na tabela inteira, logo após a leitura: dicionário das colunas; **tipo de cada coluna segundo
        a taxonomia do capítulo 6** (numérico contínuo ou discreto; categórico nominal, ordinal ou
        binário), apontando onde o tipo inferido pelo `pandas` erra; valores faltantes por coluna e o
        que o vazio significa; duplicatas; valores extremos e impossíveis nos preditores;
      - depois de separar o teste, **só no treino**: a distribuição da resposta e os gráficos
        descritivos que levam a decisões (histograma para contínuo, barras para categórico,
        dispersão ou caixa entre preditor e resposta), como a seção 17.2 exige.
   3. **Separar o teste e o que poderia vazar:** colunas que carregam a resposta, linhas que
      atravessam a divisão.
   4. **Pré-processamento** como parte do modelo (`ColumnTransformer` + `Pipeline`).
   5. **Comparação:** uma linha de base e pelo menos dois modelos, por validação cruzada nos mesmos
      grupos.
   6. **Ajuste de hiperparâmetros** (`GridSearchCV`).
   7. **O resultado no teste**, aberto uma vez, na métrica que responde à pergunta.
   8. **O que não funcionou** e **o que o resultado não autoriza a concluir**.
4. **Roteiro do não supervisionado (Municípios):** a mesma etapa 2 de descrição e exploração (sem
   resposta, a tabela inteira pode ser explorada), depois escala e valores por habitante, PCA e
   quanto da variância os componentes explicam, agrupamento e escolha do número de grupos,
   interpretação dos grupos (inclusive no mapa, por latitude e longitude), e os limites.
5. **Regras:**
   - `scikit-learn`, `pandas`, `matplotlib`, como no livro; semente explícita em tudo que sorteia;
   - todo número mostrado sai do código;
   - **o notebook fica aberto no Colab durante a apresentação**: na arguição o professor pode pedir
     para mostrar de onde saiu um número. Não é entregue, mas precisa existir e rodar.
6. **Calendário:**
   - 07/10: instruções;
   - **14/10 (HPE):** a dupla escolhe o problema e mostra ao professor um plano de quatro linhas
     (pergunta, resposta, métrica, linha de base). Sem nota, só orientação;
   - 16/12: apresentações, em ordem sorteada na hora.
7. **Critérios:**

| Critério | Peso |
|---|---|
| Descrição e análise exploratória: unidade, tipos pela taxonomia, faltantes, extremos, gráficos | 25% |
| Avaliação honesta: divisão, vazamento, métrica, linha de base | 25% |
| Modelagem justificada e comparada | 20% |
| Limites e tentativas que falharam | 15% |
| Arguição, **individual**: cada pessoa da dupla responde ao menos uma pergunta | 15% |

## Proteção da versão do professor

`.gitignore` hoje esconde só `atividades/lista-*.qmd` e `atividades/prova-*.qmd`. O
`seminario.qmd` traz as armadilhas e a rubrica nos blocos do professor e **seria versionado num
repositório público**. Entra a linha `atividades/seminario*.qmd` no `.gitignore`, junto das outras.
O PDF do professor já é coberto por `**/*gabarito*`.

## Ponto a confirmar

20 minutos por dupla comportam cerca de **10 duplas** nas 4 horas-aula de 16/12. Se a turma passar
de 20 alunos, parte das apresentações vai para outra data.

## Verificação

- `make atividade FONTE=atividades/seminario.qmd` gera os dois PDFs;
- a versão do aluno não contém nenhuma armadilha nem a rubrica detalhada (conferir lendo o PDF);
- `git check-ignore atividades/seminario.qmd` confirma que a fonte não entra no git;
- `.venv/bin/pytest tests/test_atividades.py -q` passa.

## Execução (06/10/2026)

- `atividades/seminario.qmd` escrito; `atividades/publico/seminario.pdf` (3 páginas) e
  `atividades/seminario-gabarito.pdf` (fora do site e do git) gerados por `make atividade`.
- A verificação das afirmações da versão do professor corrigiu duas (separador do CSV dos
  municípios é vírgula; as perguntas de satisfação não contêm a resposta) e acrescentou a do `VIN`.
- `index.qmd` linka as instruções no cronograma e na avaliação (`test_todo_pdf_publicado_esta_linkado_no_site`)
  e passa de grupos para duplas.
- `cylinders` saiu como identificador da versão do professor por causa de
  `test_nenhum_qmd_cita_nome_de_coluna_anterior_a_traducao`.

## Revisão (06/10/2026): o enunciado não depende do livro

Pedido do professor: "não prenda o roteiro ao capítulo 17. talvez esse capítulo nem seja dado.
explique os pontos que devem ser feitos e serão cobrados". O enunciado do aluno não cita mais
capítulo nem seção. Cada uma das oito etapas (e o roteiro de Municípios) explica o que fazer e por
quê, e termina numa linha **Cobrado** com o que conta na nota. A taxonomia de tipos é explicada no
próprio enunciado. Saiu do calendário a linha que ligava as etapas 5 e 6 às aulas de 21/10 e 28/10.
A versão do aluno passou a ter 5 páginas.

## Revisão (06/10/2026): HPE remoto e assíncrono

O HPE de 14/10 é **remoto e assíncrono**, sem aula presencial: a dupla se forma, lê os conjuntos e
escolhe o problema, e **envia a escolha ao professor até 21/10** (nomes e problema). O plano de
quatro linhas mostrado ao professor no HPE saiu do enunciado.

## Revisão (06/10/2026): roteiro sucinto

Pedido do professor: roteiro "muito mais sucinto, elencando os tópicos, mas sem necessariamente
explicá-los". O roteiro virou uma lista de tópicos por etapa, sem explicações e sem as linhas
**Cobrado**; uma frase diz que todos os tópicos listados são cobrados. A versão do aluno voltou a
3 páginas.

## Revisão (06/10/2026): notebook entregue

Pedido do professor: "peça pra entregarem também o notebook no google colab". O entregável passa a
ser a apresentação **e** o notebook, como link do Colab com acesso de leitura, até 16/12, antes da
apresentação (prazo escolhido por Claude, a confirmar), rodando do começo ao fim. Continua aberto
durante a apresentação, para a arguição.
**Confirmado pelo professor:** prazo até o dia da apresentação (16/12), link enviado pelo **AVA**,
de preferência de um repositório do **GitHub** aberto no Colab. A escolha do problema (até 21/10)
também vai pelo AVA (inferido por Claude, a confirmar).

## Revisão (06/10/2026): sem Regras; seção sobre IA e notebooks públicos

A seção de Regras saiu (bibliotecas, semente, número saído do código, notebook aberto na
apresentação). No lugar, "Uso de IA e de notebooks públicos": é permitido como apoio; quem usar
declara numa seção no fim do notebook o que usou (ferramenta ou link), em que parte e como; não se
copia solução pronta; a dupla precisa saber explicar tudo, e decisão que não sabe explicar não conta
na arguição. A entrega do notebook (AVA, GitHub/Colab, executar tudo) foi para o item "Entrega".

## Revisão (06/10/2026): sem nomes de função

Pedido do professor: sem nomes de funções ou métodos do Python no enunciado. `Pipeline`,
`GridSearchCV`, "inferido pelo `pandas`" viraram descrição; o mesmo na versão do professor
(`GroupShuffleSplit`/`GroupKFold`, `describe()`/`info()`, `Pipeline` na rubrica). Nomes de coluna dos
conjuntos ficam, porque são dado.
