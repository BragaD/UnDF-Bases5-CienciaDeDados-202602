# Capítulo 17 — Clustering: relatório

## Adendo — rodada de correções (3 Importantes, 7 Menores)

**Status: pronto.** Os 10 itens do contrato aplicados, nenhum arquivo criado ou renomeado.
`make render` → `render OK (tentativa 1)`; `make teste` → **24/24**. Sete figuras abertas
depois do render e conferidas contra a prosa.

### O que foi feito

- **I1** (`05:64`) — "o **único** treino deste livro" → "**um dos poucos** treinos". A aposta
  sobre o livro inteiro saiu; o cap. 16 a derrubaria.
- **I2** (`04`) — o degrau de −47% em *k* = 7 ganhou dono. Parágrafo novo no callout
  "Por que a curva medida sobe em alguns pontos" (mesmo mecanismo das subidas: execução
  afortunada em 7, ruim em 6) e um parêntese logo abaixo da tabela apontando para ele, para
  que o leitor não veja o tombo sem explicação.
- **I3** (`05:185`) — **figura aberta antes e depois.** O `fig-outra-semente` mostra o campo
  vermelho manchado em duas regiões, então "quase idênticos, que o olho não distingue" era
  falso. Agora: "duas variantes do mesmo vermelho", com os RGB no texto, e o efeito descrito
  como o que a figura mostra — mancha irregular, não dois blocos limpos. O `fig-recolorida`
  (semente 0), aberto para contraste, tem o vermelho chapado; a frase "na execução anterior
  era chapado, saiu manchado" está conferida contra as duas imagens.
- **M1** — o `print` do tempo de treino saiu da página, junto com `import time` e o
  `time.time()`. Os 16 s viraram prosa, marcados como medição desta máquina, com a razão dita
  (imprimir publicaria valor diferente a cada render). O callout de `scikit-learn` deixou de
  dizer "o tempo que o nosso treino imprimiu acima".
- **M2** (`06:295`) — "são, para o Python, o mesmo objeto" → objetos distintos, **iguais** por
  `==`; e a frase agora nomeia o defeito: o filtro queria remover *aqueles dois* e remove
  *todos os que se parecem com eles*.
- **M3** — `index:14` passou a "o único capítulo do livro **inteiramente dedicado** a
  aprendizado não supervisionado", com link para a §7.8 dizendo que lá o PCA era preparo para
  modelo supervisionado. `01:9` virou "o único capítulo cujo objetivo é **agrupar**, não
  prever". `01:21` ganhou um "mais completo" para não recriar a mesma colisão duas linhas
  depois. O enquadramento de `cap08/02:28` não foi tocado.
- **M4** — `desenha_grupos` (nas duas definições, §17.3 e §17.6) passou a ordenar os grupos
  pelo centroide, de leste para oeste, antes de distribuir cor e marcador. A cor agora vem da
  **posição no mapa**, não do índice de grupo. Resultado conferido nas quatro figuras:
  `fig-tres-grupos` e `fig-hierarquico-max` saem com cores idênticas ponto a ponto (a
  igualdade que o texto afirma agora pode ser vista, não só verificada pelo `assert`), e em
  `fig-dois-grupos` o nordeste continua vermelho, exatamente a leitura que o texto pede.
  Duas frases foram ajustadas para aproveitar isso, e a legenda de `fig-hierarquico-min` foi
  corrigida ("estrelas azuis", já que o grupo de catorze é o mais a oeste).
- **M5** (`01:44`) — **figura aberta depois.** `random.gauss(19.5, 1.2)` →
  `min(19.9, random.gauss(18.5, 1.0))`, com comentário dizendo o porquê. O segundo amontoado
  agora termina em 20 h; antes ia a 22,5. A prosa "logo abaixo das 20 horas" passou a ser
  verdade.
- **M6** (`02:46`) — parágrafo curto depois da receita explicando que o passo 1 é obtido pelo
  caminho inverso (sorteia atribuições, deixa o passo 4 produzir as médias), e que é daí que
  vem toda a aleatoriedade. A reconciliação de `:161` continua onde estava.
- **M7** (`05:187`) — "metade do orçamento" → "dois dos cinco grupos, 40% do orçamento".

### Não mexido, conforme o contrato

Todos os números medidos, o `assert` da §17.6, a ponte com a §12.5 e a dívida do capítulo 4.
O único número que mudou de lugar foi o dos 16 s, que saiu da saída de célula e foi para a
prosa — a pedido do M1; o valor é o mesmo.

### Preocupações

- **A ordenação de `desenha_grupos` é por centroide leste→oeste.** Ela resolve as três
  comparações que o texto pede, mas é uma convenção deste capítulo: um grupo novo cujo
  centroide caísse entre dois outros trocaria a ordem. Como as figuras são fixas e as
  sementes também, não há risco em render; fica registrado caso alguém acrescente uma figura.
- **A barra do histograma da §17.1 encosta em 20 h** porque o `bins=40` calcula as bordas
  sobre o intervalo inteiro (largura ~0,89) — todos os valores são ≤ 19,9, mas a última barra
  do amontoado tem a borda direita um pouco além de 20. Se isso incomodar, `bins` explícitos
  resolvem; achei que não valia complicar o chunk.
- **O render deste turno foi disputado.** Cinco `make render`: o primeiro abortou porque outro
  agente editou `scripts/render-seguro.sh` no meio da execução (o bash perdeu a posição no
  arquivo e estourou `syntax error near unexpected token 'done'` — não era conteúdo); dois
  saíram com `NÃO RENDERIZOU`; dois deram `render OK (tentativa 1)`. Nos dois que passaram, a
  lista de "editados DURANTE o render" trouxe só `cap15/` e `cap16/` — nenhum `.qmd` do
  cap. 17 —, então o `_freeze` deste capítulo é confiável, e `test_freeze_corresponde_ao_fonte`
  confirma. O código 75 final é o orçamento de tempo da rodada 2, que existe por causa dos
  outros capítulos.
