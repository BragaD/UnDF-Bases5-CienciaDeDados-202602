# Relatório — Capítulo 5 (Gradiente Descendente)

Escrito com base em `scratch/gradient_descent.py` (lido inteiro) e no PDF do Grus, capítulo 8, páginas 95–103 do livro (115–123 do PDF), lidas com `Read(pages=...)`.

## Quarta rodada — quatro edições de texto (E1–E4), sem tocar figura, código ou número

Terceiro portão: "AINDA NÃO, mas perto" — D1–D8 confirmados por medição independente do revisor (`6,933×10¹⁸` no epoch 1, `5,65×10¹⁴` no epoch 2, zero subidas em 98 comparações — batendo exatamente com o que eu tinha medido). Restaram 4 edições de texto puro. Não rodei `make render` nem `make clean` nesta rodada (autores dos capítulos 6 e 7 trabalhando em paralelo) — só `grep` de verificação sobre os arquivos editados.

- **E1** (`02-estimando-o-gradiente.qmd:121`): o link dizia "a **próxima seção** explica..." apontando para `04-escolhendo-o-tamanho-do-passo.qmd` — mas a próxima seção de 5.2 é a 5.3, não a 5.4. O destino do link já estava certo (era mesmo a 5.4 que explica o padrão de import); só o rótulo mentia sobre qual seção é "a próxima". Troquei o texto do link para "a **seção 5.4**", mantendo o mesmo destino.

- **E2** (`05-ajustando-modelos.qmd`, o `.exemplo`): reescrevi a referência ao Capítulo 8 inteira. O texto antigo dizia, no passado, que a fórmula fechada "**já apareceu**" e "**foi ajustada**" na seção de overfitting do Capítulo 8 — falso em três frentes: (1) o Capítulo 8 vem depois do 5 na ordem de leitura, (2) aquela seção do Grus não mostra o ajuste (ele escreve literalmente "don't worry about how; we'll get to that in later chapters"), e (3) a fórmula fechada de verdade é o Capítulo 11 (Grus 14), que o próprio parágrafo já citava. Removi todo o link e a alegação sobre o Capítulo 8; a caixa agora é só uma referência **para frente**, ao Capítulo 11.

  Este era o box que as duas primeiras revisões marcaram "NÃO MEXA NISTO" — o elogio recebido é exatamente o que fez as passadas seguintes pularem a verificação. Registro para não repetir o padrão: um trecho elogiado por conexão boa ainda precisa ser conferido quanto ao que ele afirma sobre *onde* a conexão está, não só se a conexão em si é uma boa ideia.

- **E3** (`06-minibatch-e-estocastico.qmd:210`): "a tracejada **some** atrás da fina" contradizia o próprio D7 desta rodada — o objetivo do D7 era exatamente fazer a linha tracejada continuar visível (mais grossa) por trás da sólida, não sumir. Troquei para "a tracejada **corre por baixo** da fina".

- **E4** (`03-usando-o-gradiente.qmd:7`): "devolveu algo **indistinguível** de `[6, 8, 10]`" perdia a precisão que a própria seção 5.2 já tinha estabelecido (o erro da estimativa é exatamente `h`, não zero). Troquei para citar o valor real impresso, arredondado: "devolveu `[6.0001, 8.0001, 10.0001]` — o exato `[6, 8, 10]` ... mais o `h` que a seção 5.2 previu" — amarra as duas seções em vez de esconder a diferença.

### Verificação desta rodada

- `grep` confirmando: rótulo "seção 5.4" presente em 02; nenhuma referência a `cap08/03-overfitting` ou "foi ajustado" restando em 05; "some atrás" ausente e "corre por baixo" presente em 06; "indistinguível" ausente e "6.0001" presente em 03.
- Nenhum número, figura ou chunk de código foi tocado nesta rodada — só rótulos de link e duas frases de prosa. Não havia necessidade de reexecutar Python nem de render.

## Terceira rodada — dois defeitos reais introduzidos pela rodada de correção anterior, mais 6 costuras

O portão voltou "AINDA NÃO" depois da rodada de 34 apontamentos: as correções funcionaram (as três figuras ensinam o que prometem), mas duas passagens **reescritas** nessa mesma rodada introduziram afirmações falsas — exatamente o defeito que elas mesmas tinham corrigido em outro lugar. Nesta rodada **não rodei `make render` nem `make clean`** (outro subagente estava escrevendo o capítulo 6 em paralelo) — só executei Python isolado no container para medir e conferir sintaxe, como o coordenador autorizou. Quem faz a passada de render consolidada é o coordenador.

**D2 — o número medido, como pedido explicitamente:** o texto dizia que os picos da curva estocástica disparavam acima de `10¹⁵` "repetidas vezes". Medi epoch a epoch (100 epochs, o mesmo treino já usado na figura): **só o epoch 1 ultrapassa `10¹⁵`**, com pico de `6,933478246523283 × 10¹⁸`. O maior pico entre os epochs 2–100 é do **epoch 2**, em **`565.154.092.326.313`** (`5,65 × 10¹⁴`, arredondado no texto para `5,7 × 10¹⁴`) — abaixo de `10¹⁵`. Os picos decaem monotonicamente a partir do epoch 2 (0 subidas em 98 comparações consecutivas). Reescrevi a frase para dizer isso: só o primeiro epoch cruza `10¹⁵`; os seguintes, embora recorrentes, ficam sistematicamente abaixo dessa faixa.

**D1 — referência a "seção anterior" que não existe:** `01-a-ideia-por-tras-do-gradiente.qmd` é a *primeira* seção do capítulo; não há seção anterior, e a "tigela circular" mencionada era a versão *antiga* da própria figura desta seção (substituída na correção I5), que o leitor nunca viu. Reescrevi para apresentar a tigela circular como caso hipotético ("o caso em que x e y pesassem igual"), não como algo já lido.

**D3 — pronome sem antecedente:** a abertura de 01 dizia "Boa parte **disso** se resume a…", com o antecedente no `index.qmd` — outra página, lida isoladamente. Reescrevi a primeira frase para ser autocontida: "Em ciência de dados, resolver um problema frequentemente se resume a achar…".

**D4 — argumento da vetorização duplicado, com condicional quebrada na segunda ocorrência:** o argumento aparecia tanto na prosa principal de "Comparando os três" quanto no "Na prática" (para onde a rodada anterior devia tê-lo movido inteiro). Removi da prosa principal (mantendo só o argumento de reescalonamento/passo menor) e corrigi a gramática no "Na prática": "Se você não estivesse fazendo a sua álgebra linear do zero, a diferença **seria ainda maior**: bibliotecas como NumPy calculam o gradiente de um lote inteiro numa única operação vetorizada…" — a condicional agora liga a uma consequência ("seria"), não a uma afirmação categórica solta ("é outro motivo").

**D5 — referência a algo que a figura não mostra:** o "Na prática" de 5.4 dizia que otimizadores adaptativos freiam "quando os gradientes oscilam — o sintoma, **visto no gráfico acima**"; mas `fig-tamanho-passo` plota `distance()`, que é sempre positiva, e não mostra oscilação de sinal nenhuma (só crescimento). Reescrevi para apontar para a **caixa** de divergência geométrica (que dá o mecanismo — o fator `1-3=-2` troca o sinal de `v`), e afirmei explicitamente que o gráfico não deixa essa troca de sinal visível.

**D6 — código repetido três vezes, mostrado a cada vez:** o chunk de `fig-comparacao-metodos` (55 linhas) re-treina os três métodos já mostrados no resto da seção. Acrescentei `#| echo: false`, como as outras figuras que não são a lição em si (`fig-ideia-gradiente`, por exemplo, já usava isso).

**D7 — duas curvas visualmente indistinguíveis na legenda de três:** medi onde lote inteiro e minibatch ficam a menos de 5% de diferença um do outro — **passo 30** ("umas poucas dezenas de chamadas", como o texto agora diz). Corrigi de duas formas, como o coordenador sugeriu fazer as duas: (1) estilo de linha diferente (`lote inteiro` tracejado e mais grosso, `minibatch` fino, `estocástico` mais fino ainda) para a linha tracejada ainda espiar por trás da sólida; (2) uma frase nova logo após a figura comentando a sobreposição como o próprio argumento da seção, não como um defeito.

**D8 — sobrou um callout a mais:** o pedido da rodada anterior era **um** callout de encanamento em 5.4 e duas linhas de nota em 5.2 — mas 5.2 ainda tinha um `::: {.callout-note}` inteiro. Converti para prosa simples (sem `:::`), do tamanho pedido.

### Verificação desta rodada (sem `make render`, por instrução explícita)

- Medi D2 e D7 executando os mesmos laços do capítulo isoladamente em `docker compose run --rm --no-deps -T livro python3 -` (não é render, é execução direta — seguro para rodar em paralelo com outro render).
- Rodei o chunk `fig-comparacao-metodos` completo (com os novos parâmetros `linestyle`/`linewidth`) para confirmar que ele ainda executa sem erro depois da mudança visual.
- `grep` confirmando ausência de "seção anterior" em 01, ausência de "repetidas vezes" em 06, e uma única ocorrência de "vetoriz" em 06 (só no "Na prática").
- Contagem de divs `:::` — abertos vs. fechados — em todos os 7 arquivos: todos batendo (nenhum `:::` órfão).
- **Não rodei `make render` nem `make clean`** nesta rodada, por instrução explícita do coordenador (outro subagente renderizando o capítulo 6 em paralelo). A verificação visual das figuras (que não mudaram de dado, só de estilo de linha e visibilidade de código) fica para a passada de render consolidada do coordenador.

## Rodada de correção (34 apontamentos de duas revisões, consolidados em `.superpowers/livro/cap05-correcoes.md`)

Implementei os 34 itens (3 críticos, 9 importantes, ~22 menores). Nada foi recusado — todos os itens fizeram sentido depois de verificados, inclusive os dois que o texto original tinha errado.

**Os dois números errados, confirmados e corrigidos:**
- `index.qmd`: "onze linhas" → **cinco linhas** (contei: `def`, docstring, `assert`, `step =`, `return` — 5). Também corrigi "termina com" → "chega, já na seção 5.3, a".
- `04-escolhendo-o-tamanho-do-passo.qmd`: "dezenas de milhares de epochs" → **453.845 epochs**, agora calculado ao vivo por um chunk (`epochs-para-convergir`, um `while` que conta até `distance < 0.001`) em vez de escrito de memória. Bate exatamente com o número que o coordenador recalculou.

**C1 (explicação matematicamente errada em 05):** troquei "cada passo garante reduzir a perda em primeira ordem" — falso para passo finito — por uma explicação ligando ao aprendido na seção 5.4 (passo pequeno o bastante frente à curvatura) e acrescentei a razão que faltava: a perda quadrática é **convexa**, então não há mínimo local a evitar. Fechei o loop com a advertência da seção 5.1 sobre mínimos locais.

**C2 (ponte 5.2→5.3 ausente):** 5.3 agora abre derivando à mão a derivada parcial de `sum_of_squares` e conferindo contra o `[6,8,10]` que `estimate_gradient` devolveu na seção anterior, antes de introduzir `sum_of_squares_gradient`.

**C3 (capítulo não fechava):** 5.6 termina agora com um parágrafo dizendo exatamente o que muda capítulo a capítulo — erro quadrático (11, 12), log-verossimilhança (13), retropropagação (15, 16) — em vez de repetir a mesma lista de links pela sexta vez.

**I2 (a causa do serrilhado do minibatch estava incompleta) — o item mais importante da rodada.** O revisor estava certo: `minibatches` embaralha `batch_starts` (os índices), não os pontos; como `inputs` está ordenado por `x`, cada lote é sempre a mesma fatia contígua. Adicionei um chunk que imprime o gradiente de cada uma das 5 fatias fixas em `theta=[0,0]` contra o gradiente do dataset inteiro: o termo de intercepto varia de `+1610` a `-1590` entre fatias (o gradiente verdadeiro é `10`, quase nulo) — cada lote é uma amostra **sistematicamente torta**, não apenas ruidosa. Um `callout-warning` documenta isso, e um segundo chunk compara treinar com a versão original (18 subidas em 50 checkpoints) contra a versão corrigida — embaralhar o **dataset** a cada epoch, não os índices dos lotes (7 subidas). Não editei `scratch/gradient_descent.py` nem a função `minibatches()` em si — o conserto fica em como ela é chamada, preservando o código do livro.

**I3 (as três curvas de convergência não eram comparáveis):** removi os três gráficos separados (o de 5.5 e os dois de 5.6) e substituí por um único `fig-comparacao-metodos` em 5.6, plotando erro quadrático médio contra número de chamadas a `gradient_step` (não epochs), escala log-log, para lote inteiro, minibatch (corrigido) e estocástico. **Isso revelou um problema que eu não tinha visto no primeiro rascunho** (relatado abaixo, "Achado da rodada de correção").

**I4 (faltava aviso sobre `h` pequeno demais; a figura antiga não ensinava nada):** troquei a figura de dispersão "real vs. estimativa" (que só confirmava o óbvio) por um gráfico log-log de erro-vs-`h` para `square(x)=x²` em `x=3`, variando `h` de `1` a `10⁻¹⁶`. A figura mostra o U clássico: erro de truncamento caindo (`erro≈h`) até `h≈3×10⁻⁸`, depois cancelamento catastrófico dominando — mas de forma serrilhada, não uma curva lisa (só existem poucos `float`s distintos nessa faixa). Ajustei o texto para descrever o serrilhado real, não uma subida lisa que eu tinha escrito antes de olhar a figura de perto.

**I5 (a figura da ideia não ensinava nada — círculos escondem a perpendicularidade):** troquei `sum_of_squares(v)=x²+y²` (curvas de nível circulares, caminho reto por coincidência geométrica) por `f(x,y)=x²+5y²` (elipses). O caminho agora visivelmente se curva — desce quase reto no início (a direção de `y`, mais íngreme, domina) e só depois rasteja ao longo de `x` — preparando o argumento de curvatura da seção 5.4.

**I1, I6, I7, I8, I9 e os ~22 itens "menores"** (números, `theta` explicado, convexidade, sinal de `step_size` vs. `learning_rate`, link para k-NN (Capítulo 9) como único modelo que não passa por este capítulo, link para geradores no Capítulo 2, fusão dos dois callouts de "encanamento do repositório" em um só (5.4) mais duas linhas em 5.2, troca de "vendorizado" por "uma cópia do código do livro-texto que mora dentro deste repositório" em todo o capítulo, `.callout-note`→`.callout-warning` em 5.1, divisão do callout de ~600 palavras em 5.6 (aritmética no callout, análise em prosa com subtítulo próprio, vetorização movida para "Na prática"), `.conceito` acrescentado em 5.4/5.5/5.6, e todas as reescritas de prosa fornecidas literalmente) — todos implementados como pedido, conferidos por `grep` linha a linha contra os padrões antigos (todos ausentes agora).

### Achado da rodada de correção: o `learning_rate` que funciona para a média não funciona para o ponto extremo

Ao gerar a figura unificada do I3, a curva do gradiente estocástico não convergiu suavemente como eu tinha escrito no primeiro rascunho (sem checar) — ela **serrilha**, disparando repetidamente acima de `10¹⁵`, com um pico de `6,9×10¹⁸` logo no primeiro epoch. Investiguei antes de reescrever qualquer coisa: `inputs` está ordenado por `x`, e o laço estocástico (`for x, y in inputs`) sempre começa por `x=-50`. Com `theta` ainda longe do valor certo, o gradiente nesse primeiro ponto já é enorme — rastreei as primeiras 4 atualizações e `theta[0]` pula de `0,91` para `95,9` (passa direto do `20` certo), depois para `-269`, depois `1064`, depois `-3550`: a mesma cascata de supercorreção geométrica que a seção 5.4 descreve para um `step_size` grande demais, só que aqui provocada pela curvatura de um único ponto extremo (`x²≈2500`) em vez de um passo grande demais para um `v` inteiro. A cascata se autocorrige a cada epoch (o pico cai de `10¹⁸` para `10¹¹` ao longo de 100 epochs, à medida que `theta` se aproxima do valor certo), o que explica por que o resultado final continua correto apesar da instabilidade visível na trajetória completa.

Reescrevi a análise de 5.6 para descrever isso com números reais (incluindo um novo chunk `cascata-do-primeiro-epoch` que reproduz as primeiras atualizações) em vez de manter a narrativa mais simples e incorreta do primeiro rascunho. Acrescentei uma frase de conexão para a seção 7.6 (Reescalonamento) como a solução de produção para esse problema. Este é exatamente o tipo de "texto contradizendo figura" que o guia do livro pede para caçar — encontrei porque gerei a figura antes de escrever a conclusão, não depois.

## Arquivos escritos

Os 7 stubs de `content/cap05/` foram substituídos por conteúdo completo. Nenhum arquivo foi renomeado; todos já estavam registrados no `_quarto.yml`.

- `index.qmd` — abertura, epígrafe (tradução de Sêneca), callout `.callout-important` explicando por que este é o capítulo que "pesa mais": `gradient_step` é importado pelos capítulos 11, 12, 13, 15 e 16 (verifiquei essa lista contra a tabela de numeração do `CLAUDE.md` — bate exatamente com os capítulos que treinam modelo por otimização diferenciável: regressão linear simples, múltipla, logística, redes neurais, deep learning). Lista de objetivos, tabela de seções, "Leituras adicionais" com os dois links reais do "For Further Exploration" (Active Calculus, post do Sebastian Ruder).
- `01-a-ideia-por-tras-do-gradiente.qmd` — define `sum_of_squares` (reaproveitando `dot` do Capítulo 4), explica gradiente como direção de maior crescimento, o procedimento de 4 passos, e uma figura de contorno (`sum_of_squares(v) = x²+y²`) com uma trajetória de descida manual de 15 passos partindo de `(-5, 4)`. Callout com a ressalva do Grus sobre mínimos locais/inexistentes.
- `02-estimando-o-gradiente.qmd` — `difference_quotient`, `square`, `derivative`, comparação real-vs-estimativa (reproduz a Figura 8-3 do livro), `partial_difference_quotient`, `estimate_gradient`. Inclui um callout-warning documentando uma pegadinha real do módulo vendorizado (ver seção "Achado" abaixo). Callout "Na prática" sobre diferenciação automática (autograd/JAX) vs. diferença finita.
- `03-usando-o-gradiente.qmd` — `gradient_step`, `sum_of_squares_gradient`, minimização de `sum_of_squares` a partir de ponto aleatório (seed 0), com gráfico de convergência (distância à origem × epoch, escala log) e um `.conceito` explicando por que a curva é quase uma reta (decaimento geométrico com razão 0,98). "Na prática" sobre `scipy.optimize.minimize`.
- `04-escolhendo-o-tamanho-do-passo.qmd` — primeira seção que importa de `scratch.gradient_descent` (com o callout completo explicando o padrão de kernel-por-arquivo, referenciado depois pelas seções 5 e 6). Demonstração numérica com três `step_size` (certo/grande demais/pequeno demais) a partir do mesmo ponto, com gráfico comparativo. Callout-warning explicando a divergência geométrica (fator `1-2×1.5 = -2`). "Na prática" sobre otimizadores adaptativos (momentum, Adam, learning rate schedules).
- `05-ajustando-modelos.qmd` — `linear_gradient`, o laço de ajuste de `theta` (5.000 epochs, seed 0) com gráfico de erro quadrático médio × epoch (escala log). Um `.exemplo` conecta este ajuste iterativo à fórmula fechada que já apareceu no Capítulo 8 (seção "Overfitting e Underfitting" — os mesmos `slope`/`intercept` por mínimos quadrados). "Na prática" contrasta `LinearRegression` (fórmula fechada) com `SGDRegressor`.
- `06-minibatch-e-estocastico.qmd` — `minibatches`, o ajuste por minibatch (1.000 epochs, seed 1) e por gradiente estocástico (100 epochs, seed 2), cada um com seu gráfico de erro × epoch. Um callout-important compara epochs vs. número real de chamadas a `gradient_step`, e — depois de eu ter observado a saída real — explica corretamente qual das duas curvas é mais ruidosa (ver "Achado" abaixo). "Na prática" sobre `batch_size` como hiperparâmetro em PyTorch/Keras.

## Números citados no texto (conferidos contra a renderização)

Todos os valores no texto vêm de rodar o código real dentro do container (`docker compose run --rm --no-deps -T livro python3 -`, mesmo ambiente do `make render`: `MPLBACKEND=Agg`, `PYTHONHASHSEED=0`) e depois confirmados batendo com o HTML gerado por `make render`. Conferência final por `grep`/parsing do HTML de `_book/content/cap05/*.html`:

- Seção 3: `v` final `[1.159e-08, 8.68e-09, -2.67e-09]`, distância `1.4728638015151751e-08` — bate.
- Seção 4: `(8.75158864609029, 6.463652973064613, 286772.05675508664, 8.748963537031333)` — bate com "menos de 6,5", "passa de 280.000", "acima de 8,74".
- Seção 5: `(19.99999987827074, 4.999797320703872)` — bate com "a menos de 0,001 de 20 e 5".
- Seção 6 (minibatch): `(19.999999680361427, 4.999997968208065)`. (Estocástico): `(20.001121847573497, 4.944162658006324)` — ambos dentro dos `assert` do próprio código (`19.9 < slope < 20.1`, `4.9 < intercept < 5.1`).

## Figuras geradas e o que confirmei nelas (estado da primeira entrega — ver correção acima para o estado final)

**Esta seção descreve a primeira entrega, antes da rodada de correção.** Depois da revisão, o capítulo ficou com 5 figuras, não 7: `fig-derivada-estimativa` foi substituída por `fig-erro-vs-h` (I4), `fig-ideia-gradiente` foi refeita com `x²+5y²` em vez de `x²+y²` (I5), e `fig-erro-epoch` + `fig-minibatch` + `fig-estocastico` foram substituídas por uma única `fig-comparacao-metodos` (I3). As três novas/refeitas estão verificadas na seção "Rodada de correção", no topo deste arquivo — inclusive um achado que não aparecia nesta primeira verificação (a instabilidade do gradiente estocástico no primeiro epoch).

Abri as 7 originais (`Read` direto no PNG) em `_book/content/cap05/*_files/figure-html/*.png`:

1. `fig-ideia-gradiente` (01) — contorno circular de `x²+y²` com uma trajetória vermelha em linha reta de `(-5,4)` até perto da origem. Bate com o texto ("perpendicular à curva de nível a cada ponto").
2. `fig-derivada-estimativa` (02) — marcadores `x` e `+` sobrepostos ao longo de toda a reta `y=2x`. Bate com "se sobrepõem quase perfeitamente".
3. `fig-distancia-epoch` (03) — reta quase perfeita em escala log, de ~9 a ~10⁻⁸. Bate com o `.conceito` sobre decaimento geométrico.
4. `fig-tamanho-passo` (04) — três curvas: laranja dispara para fora do gráfico, verde quase reta horizontal, azul descendo suavemente. Bate exatamente com a descrição.
5. `fig-erro-epoch` (05) — cai de ~10⁶ para ~10⁻⁸ em 5.000 epochs, sempre decrescente. Bate com "começa em torno de 3×10⁵... cai para menos de 10⁻⁷".
6. `fig-minibatch` (06) — curva visivelmente serrilhada, com picos para cima e para baixo repetidos ao longo de todo o treino. Bate com o texto reescrito (ver "Achado" abaixo).
7. `fig-estocastico` (06) — curva perfeitamente monotônica, sem nenhum solavanco. Bate com "decresce em todos os 100 epochs registrados".

## Achado: um bug real no módulo vendorizado (documentado, não corrigido)

Antes de escrever a seção 2, testei `from scratch.gradient_descent import estimate_gradient; estimate_gradient(sum_of_squares, [1,2,3])` — estoura com `NameError: name 'partial_difference_quotient' is not defined`. Motivo: no arquivo vendorizado (hash-travado por `test_scratch_e_verbatim_upstream`), `partial_difference_quotient` está definida **dentro** de `main()` (linha 82), não no nível do módulo, enquanto `estimate_gradient` (linha 20, nível do módulo) referencia esse nome livre — que só existe como local de `main()`, e `main()` nunca roda no import. A importação em si não tem efeito colateral (confirmado: só cria a lista `inputs` em memória); o problema só aparece ao *chamar* a função.

Decisão: a seção 2 define `partial_difference_quotient`/`estimate_gradient` diretamente (como o texto do livro as apresenta, e como já seria natural — é a primeira aparição delas no capítulo), e um callout-warning ("Uma pegadinha do módulo vendorizado") explica o porquê, para o caso de um aluno curioso tentar importar por conta própria. As seções 4, 5 e 6 importam `gradient_step`, `sum_of_squares_gradient`, `linear_gradient` e `minibatches` de `scratch.gradient_descent` sem problema, porque essas quatro *estão* mesmo no nível do módulo — testei as quatro import e chamada, funcionam.

## Achado: minha primeira hipótese sobre ruído estava errada — corrigida antes de publicar

**Nota da rodada de correção: esta hipótese (ordem dos lotes muda o "último lote" processado) era real, mas não era a causa principal.** O revisor identificado no item I2 apontou a causa mais profunda — cada lote é uma fatia contígua e sistematicamente enviesada de `x`, não apenas processada em ordem diferente — e eu confirmei lendo o código com atenção. A seção "Rodada de correção" no topo deste arquivo tem o diagnóstico completo e corrigido.

Rascunhei inicialmente a seção 6 assumindo (sem testar) que a curva estocástica seria "mais ruidosa" que a de minibatch, por analogia com a intuição usual (menos pontos por passo = mais ruído por passo). Rodei o código real antes de escrever a versão final e descobri o oposto: medindo o erro a cada fronteira de epoch, é o **minibatch** que oscila muito mais (18 de 50 checkpoints sobem; um salto de 1,15 para 55,8 entre os epochs 80 e 100), enquanto o laço estocástico é perfeitamente monotônico nos 100 epochs medidos.

Investiguei a causa: `minibatches()` embaralha a **ordem dos lotes** a cada epoch (`shuffle=True`), então o último lote processado — o que decide o estado de `theta` no fim do epoch — muda de epoch para epoch. O laço estocástico (`for x, y in inputs`) processa os mesmos 100 pontos sempre na mesma ordem, terminando sempre no mesmo último ponto — então o estado medido ao fim de cada epoch é mais previsível, mesmo que cada atualização individual seja mais brusca. Reescrevi o callout-important da seção 6 para refletir isso, com números reais e a explicação mecânica, em vez da intuição não verificada. As figuras (item 6 e 7 acima) confirmam a versão corrigida.

## Verificação executada (primeira entrega)

- `make render` (projeto inteiro): passou de primeira, sem "Directory not empty" — não precisei do remédio de limpar `*_files`/`.html`.
- `make teste`: 20/20 testes passaram.
- 7 figuras abertas e conferidas contra a prosa (lista acima).
- Números do texto conferidos contra o HTML renderizado via parsing direto dos blocos `<pre><code>`.

## Verificação executada (rodada de correção)

- `make render` (projeto inteiro), duas vezes: uma logo após todas as edições, e uma depois de `make clean` — o primeiro render deixou 4 PNGs órfãos de labels antigos (`fig-derivada-estimativa`, `fig-erro-epoch`, `fig-minibatch`, `fig-estocastico`) fisicamente presentes em `_book/` mesmo sem serem referenciados por nenhum `.html` (confirmei com `grep -c` contra cada HTML). Isso bate com o aviso do `CLAUDE.md` ("chunk preso com saída velha → `make clean`") — não era o race do bind mount, era cache de render anterior. Depois do `make clean` + `make render`, `_book/content/cap05` ficou com exatamente 5 PNGs, todos referenciados.
- `make teste`: 20/20 depois de todas as correções.
- As 5 figuras finais abertas com `Read` e conferidas contra a prosa final — as três novas/refeitas (`fig-erro-vs-h`, `fig-ideia-gradiente`, `fig-comparacao-metodos`) com atenção redobrada, como pedido; a segunda checagem de `fig-comparacao-metodos` foi o que revelou a instabilidade do estocástico (ver "Achado da rodada de correção").
- Todos os números citados no texto corrigido (453.845; a tabela de 5 gradientes de lote; 18/7 subidas; os 4 valores de `theta` na cascata do primeiro epoch; os picos de `6,9×10¹⁸`/`1,0×10¹¹`) reconferidos contra o HTML renderizado, todos batendo exatamente.
- `grep` de varredura confirmando ausência de todas as frases apontadas para remoção: "vendorizado", "onze linhas", "dezenas de milhares", "ensino médio", "registrados nesta renderização", "ignorância do que existe", "ficar indefinida", "quão bons ou ruins", "Os seus modelos vão frequentemente".

## Decisões de estilo que vale registrar

- Segui o padrão "primeira aparição escreve o código, segunda aparição em diante importa com callout" — como cap09 faz — em vez de importar em toda seção. Cada função nova (`sum_of_squares`, `difference_quotient`/`estimate_gradient`, `gradient_step`/`sum_of_squares_gradient`, `linear_gradient`, `minibatches`) é escrita por extenso na seção em que aparece pela primeira vez; a partir daí, seções seguintes importam de `scratch.gradient_descent` ou `scratch.linear_algebra`.
- A explicação completa do padrão de import fica na seção 4 (primeiro caso de reaproveitamento cross-seção neste capítulo); seções 5 e 6 fazem referência mais curta a ela, em vez de repetir o parágrafo inteiro.
- Todo `random.seed` é explícito e diferente por chunk estocástico (0, 1, 2) para evitar qualquer acoplamento acidental entre eles.
- `scikit-learn` só aparece nos callouts "Na prática", nunca na implementação — confirmado em todas as 6 seções de conteúdo.

## Nada que considerei problemático no texto do Grus em si

Diferente de outros capítulos, não encontrei um "erro pedagógico deliberado" do Grus nesta parte do livro — o capítulo 8 dele é limpo e sequencial. A única aspereza real veio do *repositório* vendorizado (a função aninhada em `main()`), não do texto impresso, e já está documentada acima.
