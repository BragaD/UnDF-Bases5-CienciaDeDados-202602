# Páginas de apoio do capítulo 12: o crescimento e a poda da árvore de regressão

Data: 2026-11-03. Estado: aprovado pelo professor na conversa; revisão do construtor feita (nada
pendente; dois casos de borda resolvidos abaixo, marcados como escolha minha).

## Intenção

Duas páginas interativas em `apoio/`, para projetar na aula ao lado das seções 12.1 e 12.2, que
mostram **visualmente** como uma árvore de regressão é construída e como é podada.

- **Crescimento (seção 12.1):** a turma vê a árvore ganhar um corte por vez e, a cada passo, quais
  eram as possibilidades, por que o corte escolhido venceu e como a árvore fica depois dele.
- **Poda (seção 12.2):** a turma vê a árvore grande perder um galho por vez, o antes e o depois de
  cada poda, e o erro de validação cruzada contra o tamanho da árvore, com a posição atual marcada.

O texto das seções já faz as contas e desenha as figuras estáticas (`fig-rss-corte`, `fig-regioes`,
`fig-poda`, `fig-curvas`). As páginas não substituem nada disso: põem as mesmas contas em movimento,
para o professor conduzir com o mouse enquanto fala.

## Para quem, e em que momento

O professor projeta a página na aula, em tela de computador ou de projetor, e a opera ao vivo. A
turma de Ciência da Computação vê aprendizado de máquina pela primeira vez, sem base sólida de
estatística. Celular não é requisito (CLAUDE.md, "O livro é lido no computador"). A página precisa
funcionar nos temas claro e escuro.

## Objetivos

1. No crescimento, o aluno vê **as possibilidades** de cada passo (o melhor corte de cada folha) e
   entende que vence a que mais derruba o RSS.
2. No crescimento, o aluno vê **a escolha do ponto de corte**: a linha se move no gráfico de
   dispersão e a curva do RSS mostra onde está o mínimo.
3. Na poda, o aluno vê **antes e depois** de cada poda e entende que cai o galho que menos aumenta o
   RSS por folha perdida (o "elo mais fraco").
4. Na poda, o aluno vê **o erro de validação cruzada** mudar com o tamanho da árvore e onde está o
   mínimo.
5. Os números das páginas são **os mesmos das seções**: o professor pode apontar para a página e para
   o texto sem que eles se contradigam.

## Não objetivos

- Não roda `scikit-learn` no navegador. As contas simples são feitas em JavaScript; as caras vêm
  prontas do Python (ver cada página).
- Não cobre árvores de classificação (12.3), comparação com modelos lineares (12.4) nem ensembles.
- Não mostra o erro de teste na página da poda (decisão aceita pelo professor: o laranja fica para o
  que está mudando, e o que ele pediu foi o erro de validação).
- Não precisa funcionar a 390 px.

## Anti-objetivos (o que tornaria as páginas um fracasso mesmo funcionando)

- **Um algoritmo diferente do que a seção ensina.** A sequência de cortes do crescimento tem de ser a
  do `DecisionTreeRegressor(max_leaf_nodes=k, random_state=12)`; a sequência de podas, a do
  `cost_complexity_pruning_path`. Uma página que "cresce" numa ordem própria ensina outra coisa.
- **Números que não batem com a seção.** RSS, médias, limiares, α, `ccp_alpha` e erros de validação
  saem conferidos contra o Python (ver "Verificação").
- **Texto sobre o material** em vez de sobre o conteúdo (INV-13): as páginas falam de árvores,
  cortes, RSS e poda; nada de "esta página foi feita para…" ou comparações com o ISLP.
- **Pontos que somem num dos temas.** O gradiente do salário precisa ser legível sobre fundo claro e
  sobre fundo escuro.

## Restrições da casa

- **Arquivo único, estático, sem build.** Um `.html` por página, com CSS e JS inline, como as quatro
  páginas que já existem em `apoio/`. Abre com dois cliques e roda offline (as fontes do Google Fonts
  têm fallback, como nas irmãs).
- **Irmã das outras páginas.** Copiar o bloco `:root` de tokens de `apoio/polinomios-e-ruido.html`
  (fundo e texto do tema `cosmo`, azuis do logo, IBM Plex, tema escuro por `prefers-color-scheme` e
  por `data-theme`). Regra de cor das páginas: **azul é o que está parado, laranja é o que está
  mudando** (o token `--ajuste`, `#D9480F` no claro e `#FF7A45` no escuro). Aqui, laranja é o corte
  sendo testado, o galho novo, o galho que vai cair e a posição atual no gráfico do erro.
- **Português**, números em formato pt-BR na tela (vírgula decimal, ponto de milhar), notação da
  `knowledge-base.md` para árvores: "folha", "nó", "ramo", "raiz", RSS, α na prosa, `ccp_alpha` = α/n.
- **Carregar a skill `dataviz`** antes de escrever o código dos gráficos.

## Página 1: o crescimento (seção 12.1)

### Dados

Os mesmos da seção 12.1: `dados/Hitters.csv` com `dropna()` (263 jogadores), resposta
`y = log(salario)`, preditores `anos` e `rebatidas`, **todos os 263 jogadores** (a seção 12.1 não
divide treino e teste). As três colunas (`anos`, `rebatidas`, `salario`) entram embutidas na página.

As contas são feitas em JavaScript no navegador: para uma região e uma coluna, os pontos de corte
são os pontos médios entre valores vizinhos distintos da coluna, e o RSS de cada corte é a soma dos
RSS dos dois lados, cada um em torno da própria média (a equação (8.3) da seção). É a mesma conta da
função `rss_do_corte` da 12.1.

### Layout (o "estilo B" aprovado)

Dois painéis lado a lado.

- **Esquerda: a árvore.** O diagrama da árvore atual, com caixas: nos internos com a pergunta
  (`anos < 4,5`), folhas com o número de jogadores e a média do log do salário. Debaixo de cada folha
  aparece **"em fantasma"** (tracejado, esmaecido) o melhor corte daquela folha, com quanto ele
  derruba o RSS (por exemplo, `rebatidas < 117,5` e `−23,73`). O fantasma de maior queda entre todas
  as folhas fica em laranja, marcado como o melhor. Acima, o número de folhas e o RSS atual.
- **Direita, em cima: o gráfico de dispersão** `anos` × `rebatidas` com os 263 jogadores. **Cada
  ponto tem a cor do salário, num gradiente contínuo** (pedido do professor: gradiente, não
  quintis). Os cortes já feitos aparecem como linhas sólidas que delimitam as regiões; o corte em
  teste, como uma linha laranja que se arrasta. Legenda do gradiente em mil dólares.
- **Direita, embaixo: a curva do RSS** da região selecionada contra o ponto de corte na coluna
  selecionada, com a linha tracejada cinza do RSS sem corte, um marcador no mínimo e um marcador
  laranja na posição atual da linha arrastada, com o valor.

Esboço aprovado: `.superpowers/brainstorm/18254-1793731508/content/crescimento-b-v2.html` (lá os
pontos estão em quintis; o professor pediu depois o gradiente contínuo, que o esboço da poda,
`poda-opcoes.html`, opção B, já mostra).

### Interação

- **Escolher onde cortar:** clicar numa folha da árvore, ou na região correspondente do gráfico de
  dispersão, seleciona a região; dois botões escolhem a coluna (`anos` ou `rebatidas`).
- **Arrastar a linha** dentro da região selecionada move o corte candidato, que desliza pelos pontos
  de corte válidos, e o marcador laranja anda na curva do RSS. A árvore pode mostrar, ao lado do
  fantasma, o RSS do corte arrastado.
- **"Ir ao melhor corte"** leva a linha ao mínimo da curva da região e da coluna selecionadas.
- **"Próximo corte"** aplica o corte de maior queda do RSS **entre todas as folhas**: o fantasma
  laranja vira galho (destacado em laranja até o passo seguinte), a árvore ganha uma folha, o RSS
  desce e uma nova linha sólida aparece no gráfico de dispersão. É o passo que o `max_leaf_nodes`
  faz.
- **"Desfazer"** volta um passo.

O antes e o depois ficam no mesmo diagrama: o professor mostra o fantasma, aplica o corte e o
galho aparece no lugar.

**Duas marcas laranja ao mesmo tempo** (escolha minha, depois da revisão do construtor): quando o
professor arrasta a linha numa folha que não é a do melhor corte, o fantasma do melhor continua em
laranja com o rótulo "← melhor", e o RSS do corte arrastado aparece junto da folha selecionada, para
que cada marca diga a que corte se refere.

A aba separada que o professor chegou a pedir para "escolher o melhor ponto de corte" **não é
necessária**: arrastar a linha já é essa visualização, em qualquer passo e não só no primeiro (o
professor aceitou ao trocar o A pelo B no crescimento).

### Números que precisam bater (seção 12.1)

- Sem corte: RSS 207,15. Raiz: `anos < 4,5`, RSS 115,06 (novatos 90 jogadores, média 5,107, RSS
  42,35; veteranos 173, média 6,354, RSS 72,71). Melhor corte em `rebatidas` na raiz: 117,5, RSS
  160,97.
- Segundo passo: nos veteranos, `rebatidas < 117,5` com queda de 23,73; nos novatos,
  `rebatidas < 15,5` com queda de 9,34 (e `anos < 3,5`, 9,21; `anos < 6,5` nos veteranos, 2,83).
  Com 3 folhas, RSS 91,33.
- RSS por número de folhas (medido no host com `max_leaf_nodes=k`): 4 → 81,99; 5 → 70,69;
  6 → 65,05; 7 → 61,55; 8 → 59,25.
- A regra "maior queda do RSS entre todas as folhas", feita à mão em Python, dá a mesma coluna, o
  mesmo limiar e o mesmo RSS do `DecisionTreeRegressor(max_leaf_nodes=k, random_state=12)` em todo k
  de 2 a 20 (conferido pelo revisor do construtor, no host). A página pode passar de 6 folhas sem
  sair do algoritmo, enquanto o diagrama couber.

## Página 2: a poda (seção 12.2)

### Dados

Os mesmos da seção 12.2, **com as 19 colunas** (decisão minha, aceita pelo professor: o esquema
escolhido não usa gráfico de dispersão, então a página pode reproduzir a seção exatamente).
`Hitters` com `dropna()`, `y = log(salario)`, `pd.get_dummies(..., drop_first=True, dtype=float)`,
`train_test_split(X, y, train_size=132, random_state=12)`, árvore grande
`DecisionTreeRegressor(random_state=12)` ajustada nos 132 de treino, `cost_complexity_pruning_path`,
validação cruzada com `KFold(6, shuffle=True, random_state=12)` e a grade de médias geométricas da
seção.

Essas contas **não** são refeitas no navegador. Um script em Python gera, uma vez, os dados que a
página embute: a árvore grande (para cada nó, a coluna, o limiar, o número de jogadores, a média e
o RSS do nó), a sequência de podas do caminho (qual nó vira folha em cada degrau, com o α e o
`ccp_alpha` do degrau) e, para cada tamanho, o MSE de treino e o erro de validação cruzada com o
desvio. **O script roda no container** (`make shell`), não no host: a árvore grande difere entre as
duas máquinas (120 × 121 folhas; `knowledge-base.md`), e é o container que gera o site.

### Layout (o "estilo A" aprovado)

Três colunas em cima e um gráfico embaixo.

- **Antes:** a árvore atual, com o galho que vai cair em laranja. Título com o número de folhas e o
  RSS de treino.
- **Galhos candidatos:** para cada nó interno, quanto o RSS de treino sobe **por folha perdida** se
  aquele nó virar folha: (RSS do nó − RSS do galho abaixo dele) / (folhas do galho − 1). Barras
  horizontais; a menor, em laranja, é o elo mais fraco. Com muitos nós internos, aparecem só os
  cinco mais baratos.
- **Depois:** a árvore depois da poda, com a folha nova em laranja. Título com o número de folhas e
  o RSS de treino.
- Junto do degrau, o α em que ele acontece e o `ccp_alpha` = α/n correspondente (n = 132), como a
  seção faz.
- **Embaixo: o erro contra o número de folhas** (eixo horizontal em escala log): MSE de treino em
  cinza, erro de validação cruzada em azul, um × no mínimo da validação cruzada e uma linha vertical
  laranja na posição atual, com o número de folhas e o erro naquele ponto.

Árvore grande demais para caixas com texto: desenho em **miniatura** (nós como pontos, ramos como
traços), com o galho que vai cair em laranja; vira caixas com pergunta, jogadores e média quando
couber.

Esboço aprovado: `.superpowers/brainstorm/18254-1793731508/content/poda-opcoes.html`, opção A (o
mesmo desenho de `poda-layout.html`; os números do esboço são da versão com duas colunas e não valem
para a página).

### Interação

- **"Próxima poda"** avança um degrau do caminho: o depois vira o antes.
- **"Desfazer"** volta um degrau.
- **Controle deslizante de folhas** pula direto para qualquer subárvore do caminho (de árvore grande
  até a raiz sozinha). Tamanhos que o caminho pula (a seção mostra que o 9 falta: um nó com 3 folhas
  vira folha, de 10 para 8) não existem no controle.

Cada degrau do `cost_complexity_pruning_path` transforma **exatamente um nó** em folha (conferido pelo
revisor do construtor: 116 degraus na árvore de 120 folhas do host), então "próxima poda" = um
degrau do caminho. No host, os tamanhos pulados são 9, 21 e 25; no container, conferir.

**Degraus sem erro de validação** (escolha minha, depois da revisão do construtor): alguns degraus
têm α igual ao do anterior, a menos do arredondamento, ou quase zero (os primeiros, e dois perto de
1,8e−5 e 2,9e−5 no host). A subárvore desses degraus não se obtém por nenhum `ccp_alpha`, e a raiz
sozinha (1 folha) não está na grade da seção, então a validação cruzada não tem valor ali. O
gráfico deixa **um vazio** nesses tamanhos, sem inventar valor; todos ficam longe da faixa de 2 a 20
folhas em que a aula acontece.

### Números que precisam bater (seção 12.2, container)

- Degrau de 3 para 2 folhas: MSE de treino 0,2258 → 0,2935, `ccp_alpha` 0,0677, α = 132 × 0,0677 =
  8,94. O galho que cai é o nó `impulsionadas_carreira ≤ 70,5` (54 jogadores, média 5,11), sob a
  raiz `vezes_ao_bastao_carreira ≤ 1.452,0` (`fig-poda`).
- Validação cruzada: escolhe 4 folhas, erro 0,2694, `ccp_alpha` 0,0343 (α = 4,53); a segunda melhor
  tem 7 folhas, 0,2841.
- A subárvore de 4 folhas é a de `fig-podada`.

## Integração no livro

O mesmo caminho das páginas do capítulo 7:

- Entrada de cada página em `project.resources` do `_quarto.yml`, com um comentário de uma linha.
- Uma linha `🎛️ [**Título ↗**](../../apoio/<arquivo>.html): …` em `content/cap12/index.qmd`, logo
  depois da epígrafe ou junto do link do Colab, como em `content/cap07/index.qmd`, descrevendo **o
  conteúdo** da página (INV-13).
- `make notebooks` (ou `scripts/gerar-notebooks.py` no `.venv`) depois de editar o `index.qmd`;
  `test_notebooks_estao_atualizados` e `test_toda_pagina_de_apoio_esta_publicada_e_linkada_certo`
  cobram isso.

Nomes dos arquivos (escolha minha): `apoio/crescimento-da-arvore.html` e `apoio/poda-da-arvore.html`.

## Verificação

- **Crescimento:** as contas em JavaScript são conferidas contra o Python executando o mesmo código
  com `node` (há `node` no host) e comparando com `DecisionTreeRegressor(max_leaf_nodes=k,
  random_state=12)` para k de 2 até o maior tamanho que a página oferece: a coluna, o limiar e o RSS
  de cada passo, e a curva do RSS de um corte contra a `rss_do_corte` da 12.1.
- **Poda:** os dados embutidos saem do script do container; conferir na página aberta os números da
  lista acima.
- **Integração:** `pytest tests/ -q` no `.venv`.
- **Visual:** abrir as duas páginas no navegador, nos temas claro e escuro, e conferir que nenhum
  ponto do gradiente some, que o laranja só marca o que muda e que os textos cabem.

## O que ficou com o construtor

- O tamanho máximo da árvore no crescimento: o diagrama precisa caber legível; pelo menos até 6
  folhas, e nada impede ir além se couber.
- O gradiente exato do salário (sobre o log do salário, com a legenda em mil dólares, é a minha
  sugestão), desde que mais salário signifique mais contraste com o fundo nos dois temas e que passe
  pelo validador da skill `dataviz`.
- O desenho da árvore em miniatura e o ponto em que ela vira caixas.
- Animações de transição (bem-vindas, desde que curtas e sem atrasar o "próximo").
- Onde guardar o script que gera os dados da poda (sugestão: versionado em `scripts/`, com o
  comando no topo da página, como a origem das constantes de `lote-minibatch-estocastico.html`).

## Escolhas minhas, para o professor conferir

1. As 19 colunas na poda, com os números da seção 12.2 (aceito).
2. Sem erro de teste na poda (aceito).
3. "Próximo corte", no crescimento, aplica sempre o melhor corte entre todas as folhas; arrastar a
   linha serve para explorar, não para montar uma árvore diferente da do algoritmo.
4. Na poda, os cinco galhos mais baratos na coluna do meio quando houver muitos.
5. Nomes dos arquivos e posição do link no `index.qmd`.
6. No crescimento, quando há duas marcas laranja (o melhor corte e o corte arrastado em outra
   folha), o melhor leva o rótulo "← melhor" e o RSS do arrastado aparece junto da folha
   selecionada.
7. Na poda, o gráfico do erro deixa um vazio nos tamanhos sem valor de validação cruzada (degraus de
   α repetido ou quase zero, e a raiz sozinha).
