# Capítulo 7 — relatório de correções (rodada didática)

Aplicadas as correções de `cap07-correcoes.md` nos 9 arquivos de `content/cap07/`.
`make teste`: 21/21 PASSED (uma falha intermediária corrigida — ver "Preocupações").
`make render` NÃO foi rodado, por instrução explícita (render consolidado fica para
depois, em paralelo com o capítulo 10).

## Críticos

- **C1 (ascensão de gradiente silenciosa):** `callout-important` novo logo após o
  chunk de `first_principal_component`, apontando `step_size` positivo, contrastando
  com o padrão negativo do livro e linkando `../cap05/03-usando-o-gradiente.qmd`.
  Conferido contra o texto real da 5.3 ("positivo para andar *com* o gradiente,
  negativo para *contra*") — a nota é tecnicamente exata.
- **C2 (Na prática faltando em 7.4/7.5):** dois callouts novos, no fim de cada seção,
  usando o conteúdo já especificado no arquivo de correções (coerção silenciosa do
  `pandas` em 7.4; `.pct_change()` sem ordenar em 7.5), fechando no laço de cada
  seção como a 7.1 faz.
- **C3 (7.8 não argumenta "por que variância"):** parágrafo novo antes do código de
  `direction`/`directional_variance` explicando maximizar variância = minimizar perda
  na reconstrução; parágrafo separando os dois sentidos de "componente"; callout-note
  dizendo que `directional_variance` é soma de quadrados, não variância/n; callout-note
  de legitimidade para `directional_variance_gradient` (derivada termo a termo, sem
  provar a normalização de `direction`, no mesmo espírito informal do Grus).

## Importantes

- I1: dois `.conceito` novos (direção de maior variância = o que sobra ao projetar; e
  o bloco de 7.6 sobre reescalonar não ser neutro, reclassificado de
  `callout-important` para `.conceito`). Total do capítulo: 1 → 3.
- I2: `plt.gca().set_aspect("equal", adjustable="box")` adicionado às 3 figuras
  (`fig-pca-demeaned`, `fig-pca-primeiro-componente`, `fig-pca-residual`).
- I3: gênero padronizado para feminino nos 2 `plt.title` e 2 `fig-cap` da 7.8.
- I4: callout do `index.qmd` reduzido a um parágrafo provocativo; a explicação da
  redefinição de `StockPrice` (por que o módulo nunca é importado) migrou para o
  `callout-note` já existente na 7.4, que agora conta a história completa.
- I5: cortada a especulação sobre o processo de escrita do Grus em 7.3 (mantida a
  aritmética e a lição); segundo `callout-warning` da 7.3 rebaixado a `callout-note`.
- I6: frase autocorretiva da 7.1 ("...Capítulo 6... não —") reescrita, sem a retratação.
- I7: tradução dura da 7.8 ("se estende dot(x,d)") trocada por "a projeção... tem
  comprimento... é o quanto daquele ponto 'cabe' naquela direção".
- I8: parágrafo sobre overhead de `dict` na 7.2 reduzido a uma frase.

## Menores — todos aplicados

"Compilar"→"passar" (7.3); "embrulhar"→"envolver" (7.7); "eventualmente"→"de vez em
quando" (7.7); preposição em "pelo livro inteiro" (7.5); "dado misturados"→"dados
misturados" (7.5); frase da série 3 corrigida para "faixas... verticais/horizontais"
(7.1); hesitação da 7.8 trocada por afirmação da ortogonalidade exata; 7.2 agora para
em "próxima seção: dataclass", 7.3 herda o parágrafo de `pydantic` (com o conteúdo
técnico movido, não duplicado); repetição de "média perto de 0" removida (7.1);
retrolink de `zip(prices, prices[1:])` para `../cap02/06-ferramentas-e-tipos.qmd`
acrescentado (7.5). Não havia paráfrase imprecisa do `shuffle` do capítulo 5 em cap07
(grep confirmou zero ocorrências) — nada a apertar aí.

## Pontes e fechamento

Adicionadas as duas pontes que o arquivo de correções apontou como já existentes e
não usadas: a frase "centralizar é a metade da 7.6 que sobrou" na abertura da seção
de `de_mean`, e a retomada explícita, em "Muitas componentes", do `.conceito` da 7.1
sobre a matriz de dispersão não escalar. Acrescentado o fechamento de capítulo pedido
(2 frases antes do "Na prática" final da 7.8), devolvendo a moldura da abertura do
`index.qmd`.

## Recusado

Nada. Todos os itens do arquivo de correções (3 Críticos, 8 Importantes, ~10 Menores,
pontes e fechamento) foram implementados como especificado ou muito próximos da
proposta literal do arquivo.

## Preocupações

- **Verificação de figuras adiada.** O arquivo de correções pede para abrir os PNGs
  após corrigir o `set_aspect`, mas a instrução desta rodada foi explícita: não rodar
  `make render` (outro agente renderiza cap10 em paralelo sobre o mesmo `_book/`). Os
  PNGs em `_book/content/cap07/08-reducao-de-dimensionalidade_files/figure-html/`
  são pré-correção (gerados antes desta edição) — abri-los agora não provaria nada.
  Fica pendente para depois do render consolidado.
- `make teste` pegou uma regressão real durante o trabalho: minha primeira versão do
  callout do `index.qmd` tinha "seção 7.1" a menos de 80 caracteres de "@grus2019",
  disparando falso positivo do teste anti-invenção-de-número-de-seção-do-Grus (o teste
  não distingue "seção 7.1 deste livro" de "seção do Grus" — só olha proximidade de
  texto). Reescrito para separar as duas menções; 21/21 voltou a passar.
- Os dois novos callouts `.conceito` na 7.8 ficam próximos um do outro (mesma seção,
  ~10 linhas de distância do parágrafo "por que variância" até o de "dois sentidos de
  componente"). Densidade proposital — é a seção mais difícil do capítulo e tinha zero
  `.conceito` antes — mas vale um olhar de quem revisar depois se não ficou espesso
  demais para quem lê a seção pela primeira vez.
