# Cap 7 — Trabalhando com Dados — verificação (portão final)

Verificação de leitura + números + figuras dos 9 arquivos de `content/cap07/`.
`make render` NÃO foi rodado (proibido pela tarefa); `_book/` já estava atualizado.
`make teste` rodado ao final: 20/20 PASSED (confirma que as edições de texto não
quebraram nenhum invariante estrutural).

## Figuras — 8 conferidas, uma a uma, contra a prosa que as descreve

1. `01-explorando-seus-dados_files/.../fig-histograma-uniforme-output-1.png` —
   texto diz "achatado e limitado"; imagem confirma: barras ~460-540, domínio
   fechado em [-100,100]. OK.
2. `.../fig-histograma-normal-output-1.png` — texto diz "pico ao centro e
   caudas compridas"; imagem confirma: pico ~720 em 0, cauda até ±200. OK.
3. `.../fig-dispersao-conjunta-output-1.png` — texto diz "ys1 cresce com xs;
   ys2 decresce"; imagem confirma duas nuvens em X, uma de inclinação
   positiva e outra negativa. OK.
4. `.../fig-dispersao-matriz-output-1.png` — texto diz série 1 fortemente
   anticorrelacionada com série 0, série 2 positivamente correlacionada com
   série 1, série 3 binária (0/6); os nove subplots confirmam cada relação
   (diagonal decrescente apertada para 0×1, nuvem difusa positiva para 1×2,
   duas bandas verticais para a série 3). OK.
5. `08-reducao-de-dimensionalidade_files/.../fig-pca-brutos-output-1.png` —
   texto diz variação concentrada numa direção diagonal, não alinhada a x
   nem y; imagem confirma nuvem elíptica de ~-11 a 41 em x, inclinada. OK.
6. `.../fig-pca-demeaned-output-1.png` — texto diz "mesma forma, só recentrada
   na origem"; imagem confirma, cruza os eixos em (0,0), forma idêntica à
   anterior. OK.
7. `.../fig-pca-primeiro-componente-output-1.png` — texto diz que a reta
   captura o eixo principal da variação; imagem confirma, reta atravessa a
   nuvem ao longo do eixo mais longo. OK.
8. `.../fig-pca-residual-output-1.png` — texto diz que o resíduo fica
   "essencialmente alinhado ao longo de uma reta"; imagem confirma
   alinhamento quase perfeito (inclinação negativa). OK.

Nenhuma divergência figura-vs-prosa encontrada (diferente do padrão "dispara
mas oscila" relatado em capítulos anteriores).

## Números — conferidos dígito a dígito contra `_book/content/cap07/*.html`

- §1: `médias: 0.13 e 0.14` — bate com "ambos têm média perto de 0".
- §1: `correlation(xs,ys1)=0.9061974905296714`,
  `correlation(xs,ys2)=-0.9067533538537036` — bate com "cerca de 0,906 e
  -0,907".
- §1: matriz de correlação `[[1,-0.98,-0.66,-0.52],...]` — bate com
  "anticorrelação forte série 0×1 (-0.98)", "correlação positiva série 1×2
  (0.68)", série 3 binária.
- §2/§3: `NamedTuple` = 21 ocorrências em `scratch/*.py`, `dataclass` = 0
  ocorrências — recontado via `grep -rn` independentemente, bate exato.
- §3: `106.03 / 2 = 53.015` (matemática correta) vs. o `assert
  price2.closing_price == 51.03` do livro impresso — **confirmado na íntegra
  contra o PDF, página 132**: o Grus realmente imprime esse assert
  matematicamente impossível. `51,03 = 102,06 / 2` também confirmado (dict
  `stock_price` da seção 7.2, PDF página 129).
- §4: CSV sujo (6 linhas) e a rejeição de exatamente 1 (`n/a`) — bate
  exatamente com a saída do chunk.
- §5: `dados/stocks.csv` tem 23.106 linhas (`wc -l`) = 23.105 registros +
  cabeçalho — bate com "23.105 linhas" do texto.
- §5: `max_change` AAPL 1997-08-06 pct=0.3323 ("mais de 33%"),
  `min_change` AAPL 2000-09-29 pct=-0.5187 ("quase 52%") — confirmados
  contra a saída e contra os `assert` do PDF (página 135: `0.33 <
  max_change.pct_change < 0.34`, `-0.52 < min_change.pct_change < -0.51`).
  Fatos históricos (investimento da Microsoft em ago/1997, alerta de
  resultado da Apple em set/2000) plausíveis e datados corretamente.
- §5: `avg_daily_change` por mês (12 valores arredondados) e `melhor_mes ==
  10` com 0,29% — bate exatamente com a saída e com o `assert
  avg_daily_change[10] == max(...)` do PDF (página 135).
- §6: distâncias A-B-C em polegadas `(10.77, 22.14, 11.4)` e em centímetros
  `(14.28, 27.53, 13.37)` — recalculadas manualmente (√116, √490, √130 etc.),
  batem; e a inversão de vizinho mais próximo (A→C ao trocar unidade) está
  correta.
- §6: `scale`/`rescale` (`means=[-1,0,1]`, `stdevs=[2,1,0]`, vetores
  reescalonados) — bate exatamente com os `assert` do próprio chunk.
- §7: `len(my_primes) = 9592` (primos até 100.000) — recontado
  independentemente com uma reimplementação de `primes_up_to`, bate exato.
- §8: `len(pca_data) = 99` — **recontado por script** a partir do bloco
  literal do `.qmd`: 99 linhas, bate. E os **99 pares de números foram
  comparados byte a byte** contra `scratch/working_with_data.py` (linha 292
  em diante): **0 divergências** — a base de dados do PCA é cópia perfeita
  do pacote vendorizado.
- §8: `fpc = [0.9237307801943213, 0.38304235499692535]` — bate com os
  `assert 0.923 < fpc[0] < 0.925` / `assert 0.382 < fpc[1] < 0.384` e com o
  arredondamento no texto "(0,924, 0,383)".
- §8: `gradient_step` tem exatamente 5 linhas (`scratch/gradient_descent.py:
  29-33`) — confirmado, e é de fato a função usada pelo Capítulo 5 (seção
  5.3, `content/cap05/03-usando-o-gradiente.qmd:16`).

## Seção 8 (PCA) — atenção redobrada, como pedido

Toda a cadeia matemática foi conferida: `de_mean` → `direction` →
`directional_variance` → `directional_variance_gradient` →
`first_principal_component` (chama `gradient_step` do Capítulo 5) →
`project`/`remove_projection` → `pca`/`transform`. Os números batem em cada
etapa (ver acima), as 4 figuras da seção conferem com a prosa, e a
referência ao Capítulo 5 aponta para conteúdo real e existente (seção 5.3
define `gradient_step`, confirmado por `grep`).

## Invariantes do projeto — as 3 de risco especial

1. **`scratch.working_with_data` nunca importado**: confirmado via `grep -rn
   "working_with_data\|getting_data"` em `content/cap07/` — as únicas
   ocorrências são menções em prosa (nomeando o módulo), nenhum `import`
   real. `scratch.getting_data` também não aparece.
2. **Caminhos de dados a partir da raiz**: `dados/stocks.csv`,
   `dados/comma_delimited_stock_prices.csv` — confirmado via `grep`, nenhuma
   ocorrência de `../dados/`.
3. **Semente explícita em todo chunk com aleatoriedade**: todos os chunks
   `{python}` reais com `random.*` tinham `random.seed(...)` — **exceto um**,
   corrigido nesta verificação (ver abaixo).

## Correções feitas (texto ajustado para bater com o medido)

1. **`content/cap07/07-um-parenteses-tqdm.qmd`** — o chunk `tqdm-basico`
   chamava `random.random()` num laço sem `random.seed(...)` (violação da
   invariante 3, ainda que o valor gerado seja descartado e não apareça em
   nenhum output real — confirmado por inspeção do HTML: o chunk não deixa
   `cell-output` nenhum, só o texto ilustrativo do prompt). Acrescentei
   `random.seed(0)` antes do laço. `make teste` continua 20/20.
2. **`content/cap07/07-um-parenteses-tqdm.qmd`** — o bloco de texto
   ilustrativo `5116 primos: 50%|...| 49529/99997 [...]` não batia com a
   contagem real de primos até aquele ponto. Reimplementei `primes_up_to` e
   medi: primos ≤ 49529 = **5088**, não 5116. Corrigido para `5088 primos`.
3. **`content/cap07/01-explorando-seus-dados.qmd`** (e o mesmo texto em
   **`content/cap07/index.qmd`**) — a alegação "esse assert falha cerca de
   uma vez em cada três execuções" foi medida empiricamente (20.000
   repetições de `xs`/`ys1` sem semente, usando `scratch.probability` e
   `scratch.statistics` reais via `uv run`): taxa de falha real = **24,6%**
   (~1 em 4), não 1 em 3 (~33%). Corrigido nos dois arquivos para "uma vez
   em cada quatro execuções (medido: 24,6% em 20 mil repetições)".
4. **`content/cap07/01-explorando-seus-dados.qmd`** — a citação "(linhas 44
   a 49 do @grus2019)" atribuía a geração de `xs`/`ys1`/`ys2` à faixa de
   linhas errada: `grep -n` em `scratch/working_with_data.py` mostra que
   `xs`/`ys1`/`ys2` nascem nas linhas **28-30**, e os dois `assert` estão
   nas linhas **48-49** — não há geração de dado nenhuma nas linhas 44-49.
   Reescrito para citar as duas faixas corretamente.
5. **`content/cap07/01-explorando-seus-dados.qmd`** — o callout sobre o
   `import` de `scratch/probability.py` implicava que os `assert` do módulo
   rodavam junto com o `import`. Conferido: os dois `assert` (linhas 136-137)
   vivem dentro de `main()`, atrás de `if __name__ == "__main__"` — nunca
   executam num `import`. Reescrito para não implicar isso; a contagem "18
   chamadas `plt.*`" foi recontada manualmente (linha a linha, excluindo
   comentários e o corpo de `binomial_histogram`) e está correta, batendo
   também com `CLAUDE.md:144`.

## Links entre capítulos

Todos os `../capNN/arquivo.qmd` referenciados em `content/cap07/*.qmd`
resolvem para arquivos existentes (`../cap02`, `../cap03`, `../cap04`,
`../cap05`, `../cap06`, `../cap08`, `../cap09`, `../cap15`, `../cap16`) —
verificado com um laço de `grep`+`test -f`. `cap15`/`cap16` ainda são stubs
("Em construção"), mas isso é esperado (ordem de escrita do projeto) e a
menção em cap07 é genérica, não promete conteúdo específico. A "promessa"
cruzada com `cap08/06-extracao-e-selecao-de-atributos.qmd` (cita "Capítulo
7" para redução de dimensionalidade) e com
`cap09/03-a-maldicao-da-dimensionalidade.qmd` (cita PCA "no capítulo 7" e
usa `tqdm.tqdm` com `#| warning: false`, mesmo padrão citado em cap07 §7)
foram conferidas e ambas se sustentam.

## `_quarto.yml` e citações

Os 9 arquivos estão registrados em `_quarto.yml` (linhas 106-122). Todas as
8 seções citam `@grus2019` pelo menos uma vez (`grep -c`).
