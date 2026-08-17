# Escrita dos capítulos restantes — ledger

Objetivo: escrever os 11 capítulos que faltam, um a um, com subagentes.
Cada capítulo: 1 escritor + 2 revisores INDEPENDENTES (didática e conteúdo) + rodadas de correção.
Depois: revisões do livro inteiro (inconsistência, clareza, melhoria didática), iterando
até não haver mais apontamento.

## Já escritos antes desta fase
cap01 Introdução · cap02 Curso Rápido de Python · cap03 Visualizando Dados
cap04 Álgebra Linear · cap08 Machine Learning · cap09 k-Vizinhos (MODELO DE ESTILO)

## Ordem de escrita (dependências)
5 primeiro: gradient_step é usado por 11,12,13,15,16.
5 → 6 → 7 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17

| Cap | Grus | Título | Seções | Escrito | Rev.Didática | Rev.Conteúdo | Fechado |
|-----|------|--------|--------|---------|--------------|--------------|---------|
| 5  | 8  | Gradiente Descendente      | 6 | ok | ok | ok | FECHADO |
| 6  | 9  | Obtendo Dados              | 5 | ok | ok | ok | FECHADO |
| 7  | 10 | Trabalhando com Dados      | 8 | – | – | – | – |
| 10 | 13 | Naive Bayes                | 5 | – | – | – | – |
| 11 | 14 | Regressão Linear Simples   | 3 | – | – | – | – |
| 12 | 15 | Regressão Múltipla         | 8 | – | – | – | – |
| 13 | 16 | Regressão Logística        | 5 | – | – | – | – |
| 14 | 17 | Árvores de Decisão         | 6 | – | – | – | – |
| 15 | 18 | Redes Neurais              | 4 | – | – | – | – |
| 16 | 19 | Deep Learning              | 8 | – | – | – | – |
| 17 | 20 | Clustering                 | 6 | – | – | – | – |

## Deslocamento do PDF
página do livro N = página do PDF N + 20

## Armadilhas conhecidas (ver CLAUDE.md)
- Render no macOS aborta com "Directory not empty": remover só os *_files e
  renderizar de novo COM o _freeze quente. NUNCA `make clean` para isso.
- scratch/ nunca é editado. getting_data e working_with_data nunca são importados.
- Grus não numera seções: citar capítulo + título.
- Semente explícita em todo chunk com RNG. random da stdlib, não numpy.

## Registro

### Cap 5 — Gradiente Descendente
- Escrito: 7 arquivos. render OK de primeira, 20/20 testes.
- ACHADO DO ESCRITOR, confirmado por mim empiricamente: `scratch/gradient_descent.py`
  define `partial_difference_quotient` DENTRO de `main()` (linha 82), mas
  `estimate_gradient` (nível de módulo, linha 20) a chama. Importar funciona;
  chamar levanta NameError. Terceira armadilha do pacote vendorizado, junto com
  getting_data e working_with_data. -> LEVAR PARA O CLAUDE.md.
- O escritor testou a própria intuição sobre ruído de minibatch vs estocástico,
  descobriu que era o oposto (minibatch é mais ruidoso, porque minibatches()
  embaralha a ordem a cada época) e reescreveu o callout para bater com o medido.
  Exatamente o comportamento pedido.
- Duas revisões independentes despachadas: conteúdo (sonnet) e didática (opus).
- REVISÃO DIDÁTICA (opus): 31 apontamentos, 2 Críticos. Espinha certa, "Na prática"
  elogiados. Falhas: a ponte 5.2->5.3 não foi construída; o capítulo não fecha.
- ADJUDICAÇÃO MINHA, com evidência: o revisor CONTRADIZ o escritor sobre a causa do
  ruído do minibatch, e o revisor está certo. `minibatches` embaralha `batch_starts`
  (índices de início), NÃO os elementos. Como `inputs = [(x, 20*x+5) for x in
  range(-50,50)]` está ordenado por x, cada lote é sempre a MESMA fatia contígua —
  um lote só de x negativos, outro só de positivos. Cada lote é amostra enviesada, e
  é isso que entorta o gradiente. O escritor atribuiu à ordem dos lotes, que é a causa
  menor. Um `shuffle` que parece embaralhar dados e não embaralha: erro instrutivo do
  livro-texto, merece callout próprio.
- REVISÃO DE CONTEÚDO (sonnet): 1 Crítico, 1 Importante, 1 Menor. O Crítico é o melhor
  achado: a explicação de por que a perda cai sempre invocava "garantia de primeira ordem",
  que vale só para passo infinitesimal — e CONTRADIZ a própria seção 5.4, que mostra passo
  finito divergindo na direção correta. Fato certo, porquê errado.
  Importante: "dezenas de milhares de epochs" são 453.845 (recalculei) = centenas de milhares.
  Menor: "onze linhas" -> gradient_step tem 5. Os DOIS revisores pegaram este, independentemente.
- Consolidei 34 apontamentos em .superpowers/livro/cap05-correcoes.md e mandei corrigir.
- CORREÇÃO: 34/34 implementados, nada recusado. 3 figuras refeitas (I3/I4/I5).
  Novo achado do escritor durante a correção: o gradiente estocástico DIVERGE (picos de
  1e18) no início de cada epoch, porque inputs está ordenado por x e o primeiro ponto
  (x=-50) tem curvatura demais para o learning_rate seguro na média. Mesma raiz que o I2:
  o dado ordenado. Ele reescreveu com números reais em vez de publicar explicação que a
  figura contradiria.
- Re-revisão escopada despachada.
- PORTÃO FINAL (opus): AINDA NÃO. Os 34 foram endereçados e as 3 figuras refeitas passam
  (o U do erro-vs-h aparece; a perpendicularidade fica visível na tigela anisotrópica; as
  três curvas ficaram comparáveis). MAS a correção introduziu 2 afirmações falsas:
  D1: "tigela circular como a da SEÇÃO ANTERIOR" — 5.1 é a primeira seção. A tigela
      circular era a versão antiga da própria figura, que o aluno nunca viu.
  D2: "disparando acima de 1e15 REPETIDAS VEZES" — medido: exatamente UM epoch passa
      disso. Os picos recorrentes vão a 5.7e14, abaixo da linha na figura. Olhômetro.
  Mais 6 costuras (pronome sem antecedente, argumento duplicado, referência a figura que
  não mostra o que se afirma, chunk de 55 linhas que deveria ser echo:false, curva que
  some sob outra sem comentário, dois callouts onde eu pedi um).
  O revisor REPRODUZIU o achado do estocástico com números próprios: pico 6.93e18 no
  primeiro epoch, decrescente nos 100. Confirmado.
- Rodada 2 despachada SEM render (o escritor do cap 6 está renderizando; dois renders
  concorrentes sobre o mesmo _book/ se atropelam). Renderizo depois, consolidado.
- RODADA 2: D1-D8 corrigidos. D2 medido: epoch 1 = 6.933478e18; maior dos epochs 2-100 =
  5.65e14 (epoch 2), ABAIXO de 1e15. "Repetidas vezes" era falso, confirmado.
  Verifiquei D1, D2 e D6 eu mesmo nos arquivos: os dois textos falsos sumiram, echo:false
  aplicado. A correção do I2 foi além do pedido: o capítulo agora mostra AS DUAS versões,
  a enviesada e a corrigida com shuffle no dataset, com os números de cada (18 vs 7
  subidas; erro 55,8 vs 2,6 no epoch 100).
  FALTA: render + portão final. Bloqueado até o escritor do cap 6 parar de renderizar.

### Cap 6 — Obtendo Dados
- Escrito: 6 arquivos. render OK, 20/20 testes, `make offline` PASSOU (a invariante
  sobreviveu ao capítulo que mais a ameaça). Bug real achado e corrigido pelo escritor:
  `<nome-do-site>` em prosa crua era lido como tag HTML pelo Pandoc e corrompia a saída.
- REVISÃO DE CONTEÚDO: **0 Crítico, 0 Importante**, 3 Menores (dois herdados do próprio
  Grus). As três restrições duras auditadas e aprovadas: nenhum import de getting_data;
  todos os chunks de rede com eval:false + callout; a seção do Twitter não promete que
  funciona. Números do texto conferidos contra o HTML: batem. Fidelidade ao PDF conferida
  seção a seção. A promessa do cap 1 ("o Capítulo 6 é dedicado a isso") foi cumprida.
- Revisão didática em andamento.

### Cap 7 — Trabalhando com Dados
- Escritor despachado. Armadilha central: este capítulo É o módulo working_with_data,
  que nunca pode ser importado (open de stocks.csv relativo ao cwd no corpo do módulo +
  assert sobre correlação de dados SEM semente, que falha ~1 em 3). Todo o código inline.
- Instruído a marcar o assert-sem-semente como erro instrutivo do livro-texto.
- Também: dataclass tem seção própria no Grus e ZERO usos no pacote dele. Contrastar com
  NamedTuple, que tem 21.

## LIÇÃO DE PROCESSO — a lista "NÃO MEXA NISTO" cria ponto cego
O portão do cap 5 achou uma referência falsa dentro do único box que as DUAS revisões
anteriores tinham marcado como "não mexer". O revisor observou a causa: elogiar um trecho
faz as passadas seguintes pularem-no.
MUDANÇA A PARTIR DE AGORA: a seção "NÃO MEXA NISTO" dos briefs de correção passa a se
chamar "DESTACADO COMO BOM — mas não reverificado", e os portões finais recebem instrução
explícita de que trecho elogiado NÃO está isento de verificação.
- PORTÃO 3 (opus): AINDA NÃO, 4 edições de texto. Achado de destaque: o `.exemplo` de 5.5
  dizia no PASSADO que a fórmula fechada "já apareceu neste livro", citando o cap 8 —
  falso em três frentes (o cap 8 vem depois na ordem; o Grus não mostra o ajuste ali,
  escreve "don't worry about how"; a fórmula é do nosso cap 11). Escapou de 3 passadas
  porque estava dentro do box marcado "NÃO MEXA NISTO" pelas duas revisões.
- RODADA 3: E1-E4 corrigidos e VERIFICADOS POR MIM em disco. A reescrita do E2 foi além:
  agora explica que a fórmula fechada só existe porque o problema é simples o bastante, e
  que logística e redes neurais não têm nenhuma — o gradiente é o único caminho para elas.
- CAP 5: conteúdo FECHADO. Falta só a verificação no render consolidado (as 4 edições não
  tocaram figura, código nem número, então as figuras já validadas continuam válidas).
- CAP 6, CORREÇÃO: 11 itens (2 Críticos + 9 Importantes) + reestruturação da §5 + prosa.
  Nada recusado. C1 resolvido como pedido: o chunk do GitHub virou análise EXECUTANDO
  (com `repos` literal e moldura DataSciencester) mais um fetch estreito com eval:false.
  C2: exercício imperativo de terminal na §1. Arco da fragilidade nomeado no index, e o
  `.conceito` central do capítulo criado. `## Adiante` fechando a §5.
  O escritor SINALIZOU uma tensão em vez de decidir em silêncio: a lista "NÃO MEXA" cobria
  os cinco "Na prática", mas duas instruções nomeadas mandavam mexer em dois deles. Tratou
  o específico como prevalecendo sobre o geral — leitura correta — e avisou. É a segunda
  vez que aquela lista causa atrito; a mudança de processo que fiz estava certa.
  make teste 20/20; todos os chunks não-eval:false extraídos e executados localmente, exit 0.
- CAP 6, PORTÃO: AINDA NÃO. Três defeitos NOVOS da correção:
  N1: a frase escrita para curar o C1 comete o erro do C1 — diz que o dado "veio de uma
      API em vez de estar escrito à mão", e ele está escrito à mão logo acima.
  N2: duas frases da MESMA rodada se anulam (o índice negando que o livro proíba rede em
      geral; a §3 dizendo que ele renderiza com a rede desligada). Vieram de dois itens
      diferentes da minha lista, corrigidos em sequência, sem releitura conjunta.
  N3: "o html.parser desiste diante da primeira quebra" — o revisor TESTOU: não desiste,
      devolve árvore errada em silêncio. E a verdade serve melhor ao capítulo.
- CAP 6, RODADAS 3 e 4: N1-N3 + 6 menores corrigidos.
  ADJUDIQUEI CONTRA O ESCRITOR num item: ele trocou por `except:` pelado (fidelidade ao
  Grus) com nota defendendo. O argumento dele nomeava DUAS exceções e concluía por
  capturar TODAS — e a §3 do mesmo capítulo acabara de ensinar que falha silenciosa é
  pior que falha alta. Mandei `except (ValueError, IndexError)` com callout "Aqui o texto
  se desvia do Grus, de propósito". Implementado.
- CAP 6: conteúdo fechado, falta reverificação no portão.
- CAP 10 despachado.

## INFRAESTRUTURA CONSERTADA
`make render` agora se autocura: limpa o lixo e repete até 6x, imprime "render OK
(tentativa N)", nunca toca no _freeze. CLAUDE.md e guia com 3 proibições escritas a
partir de dano real (render em segundo plano; contornar a corrida à mão; make clean).
Motivo: a corrida custou ~8 interrupções e travou o escritor do cap 7 num laço de horas
(314k tokens, 149 chamadas, zero progresso). Ele leu a instrução de não usar make clean,
não associou ao sintoma, e usou. Argumento para automatizar em vez de documentar.
- CAP 6: **PRONTO**. Portão final sem defeito novo. O revisor reproduziu as duas
  afirmações testáveis por conta própria (html.parser desaninhando em silêncio; os
  Counter do dateutil). A adjudicação do except verificada linha a linha: o callout diz
  explicitamente que o repositório do Grus usa `except:` pelado, então quem comparar não
  acha que copiamos errado. Arco da escada de fragilidade sustentado ponta a ponta.
- CAP 7: 2 revisões independentes em voo. Pedi julgamento sobre se é um capítulo ou dois
  (7 seções utilitárias + PCA do zero como oitava).
- CAP 10: 2 revisões em voo. Pedi julgamento sobre se ele COBRA a dívida do cap 8 —
  2800 ham x 500 spam, baseline 84,7% x modelo 91,5%, que é a piada do "Luke" com dados
  reais — e se usa o contraste com o cap 9 (um não treina e guarda tudo; o outro treina
  contando e joga os dados fora).
- CAP 11: escritor em voo.
- CAP 10, REVISÃO DE CONTEÚDO: 0 Crítico, 1 Importante, 2 Menores. O revisor recalculou
  à mão: 300*ln(0.01) = -1381.551, acurácia (80+675)/825 = 91,5%, precisão 80/104 = 76,9%,
  revocação 80/126 = 63,5% — todos batendo com o HTML. Números do próprio Grus citados
  para comparação conferidos contra o PDF.
  IMPORTANTE: o capítulo omite a lista "How could we get better performance?" (p.176-177)
  sem callout de omissão — e isso deixa `drop_final_s` no módulo vendorizado como objeto
  morto e inexplicado.
  MENOR NOTÁVEL (deriva entre capítulos): o cap 10 diz que o shuffle do cap 5 "embaralha
  os lotes errados"; o cap 5 é preciso ao dizer que embaralha os ÍNDICES DE INÍCIO, não
  os pontos. A paráfrase afrouxou o que a fonte acertou. -> tipo de achado que a REVISÃO
  GERAL do livro precisa caçar sistematicamente.

## TENDÊNCIA DAS REVISÕES DE CONTEÚDO (o guia está absorvendo as lições)
cap 5: 1 Crítico + 1 Importante + 1 Menor
cap 6: 0 Crítico, 0 Importante, 3 Menores (2 herdados do Grus)
cap 10: 0 Crítico, 1 Importante, 2 Menores
- CAP 7, REVISÃO DE CONTEÚDO: **0 Crítico, 0 Importante**, 1 Menor (que é uma ressalva,
  não defeito). Revisão confirmatória, não corretiva — a verificação anterior já tinha
  pego as 5 divergências.
  O revisor confirmou por DERIVAÇÃO, não medição: correlation(xs,ys1) ~= 0.894 porque
  Var(ys1)=1.25 e Cov=1, logo 1/sqrt(1.25). Mais forte que rodar.
  As 8 figuras abertas uma a uma e conferidas contra a prosa: nenhuma divergência.
  ERRO NO LIVRO IMPRESSO confirmado: o Grus afirma price2.closing_price == 51.03 com
  closing_price=106.03 definido duas páginas antes. 106.03/2 = 53.015, e 51.03 = 102.06/2,
  o preço do exemplo ANTERIOR. Erro de manutenção de texto que sobreviveu à publicação.
  O capítulo o enquadra corretamente.
  dataclass: 0 usos no pacote do Grus contra 21 de NamedTuple, confirmado por grep
  independente. O Grus dedica seção inteira a algo que o código dele nunca usa.

---

## Rodada — capítulos 7, 10, 11 fechando; 12 em escrita

**Estado:** 5 e 6 FECHADOS. 7 e 10 corrigidos e renderizados, em portão. 11 escrito,
duas revisões feitas, em correção. 12 em escrita. 13–17 na fila.

### Decisões desta rodada

**Ruling L — `make render` passa a ser serializado por lock.** Dois `quarto render`
simultâneos sobre o mesmo `_freeze/` corrompem o cache sem erro na tela, e este livro é
escrito por vários agentes em paralelo. Lock por `mkdir` (atômico em POSIX; `flock` não
existe no macOS de fábrica), `trap` devolvendo em abort/Ctrl-C, expiração de 30 min contra
agente morto. Provado: espera sem disparar docker, não rouba lock alheio, avisa uma vez só,
e devolve pelo trap após render real. Custo se errado: um render pode esperar à toa se o
lock vazar — mitigado pela expiração.

**Ruling M — terceiro falso positivo dos meus próprios testes, corrigido na raiz.**
`test_nenhuma_secao_inventa_numero_de_secao_do_grus` acusava "seção 7.1" (NOSSA numeração)
por estar a menos de 80 caracteres de `@grus2019`. O teste agora tira o número do capítulo
do caminho: em `content/cap07/`, `7.x` é nosso, `10.x` seria do Grus. Provado contra 5
vetores. **Padrão a vigiar:** meus testes estruturais têm sido escritos contra o exemplo do
defeito, não contra o invariante — três falsos positivos até agora, todos por regex larga
demais.

**Ruling N — cap. 11 M1: não "consertar" o β.** Nosso texto diz 0,904; o Grus imprime
0.903 (truncamento dele — 0,9038659… arredonda para 0,904). Nosso número está certo.
Registrado no contrato de correção para que a próxima revisão não o reverta.

### Medições desta rodada (todas conferidas, nenhuma assumida)

- **Outlier do cap. 11/12:** o usuário removido pelo Grus tinha **100 amigos, 1 minuto/dia**.
  Correlação **0,2474** com ele, **0,5737** sem — um ponto em 204 derruba a correlação para
  **43%** do valor. Virou material de `callout-warning` (contrato I5).
- **Convergência cap. 11:** fechada (22,947552413; 0,903865946) × gradiente
  (22,947552155; 0,903865966) → diferença **2,58e-07** em α, **2,07e-08** em β.
- **Cap. 12:** `inputs` = 203 pontos × 4 valores `[1.0, num_friends, work_hours, phd]`.
  `least_squares_fit(..., 0.001, 5000, 25)` com `seed(0)` → **beta = [30.5148, 0.9748,
  -1.8507, 0.9141]**, **R² = 0,679985**. Um ajuste custa **0,9 s** → o bootstrap de 100
  amostras do Grus custa **~90 s** de render. **Não precisa cortar amostras.**
  O Grus imprime `30.58, 0.972, -1.865, 0.923` nos asserts — difere no 3º dígito do nosso.
- **Armadilha cap. 12:** `least_squares_fit` chama `tqdm.trange` por dentro → todo chunk que
  a chamar precisa de `#| warning: false`. Conferido que a barra hoje só aparece em
  `_book/content/cap07/07-um-parenteses-tqdm.html`, que é a seção que a ensina.

### Revisões do cap. 11

- **Conteúdo: limpa.** Zero Críticos, zero Importantes. Matemática, números, derivação de
  máxima verossimilhança e a dívida do cap. 5 todos conferidos.
- **Didática: a mais forte do projeto.** Dois Críticos que a de conteúdo não veria por estar
  fora da faixa dela: (C1) o argumento de *por que* os dois métodos concordam está partido
  entre duas seções e nunca é dito inteiro; (C2) o clímax do livro não tem figura, entrega
  dois `tuple` sem rótulo. **Lição: as duas faixas de revisão não são redundantes.**

---

## Rodada — capítulos 7 e 10 FECHADOS; 11 e 12 em portão/revisão

**Estado:** FECHADOS 5, 6, 7, 9, 10. Em portão: 11. Em revisão: 12. Em escrita: 13.
Na fila: 14–17. Depois: as revisões gerais do livro (tarefa #28).

### O achado da rodada — o `_freeze` envenenado

Os dois portões (7 e 10) travaram no MESMO defeito, e ele não era de texto: o
`freeze: auto` guarda o par *(hash MD5 do fonte, markdown executado)*. Quando um
agente **edita um `.qmd` enquanto outro renderiza**, o Quarto executa a versão velha
e grava esse resultado com o hash da versão **nova**. Dali em diante o hash bate, o
cache é considerado válido, e o arquivo **nunca mais reexecuta**. O livro publica
texto antigo indefinidamente, sem erro na tela.

Já tinha publicado 3 seções do cap. 10 e 2 do cap. 7. Só apareceu porque um portão
comparou fonte e HTML linha a linha.

**Três camadas de defesa, todas provadas:**

1. `scripts/render-seguro.sh` — lock (mkdir, atômico; `flock` não existe no macOS) +
   fotografia de mtimes antes/depois do render. Quem foi editado no meio tem o
   `_freeze` apagado e o render repete, até 3 rodadas. Se persistir, **avisa e sai
   com SUCESSO** — o render funcionou, e um agente que vê "falha" tende a rodar
   `make clean`, que é o remédio errado.
2. `make refresh CAP=NN` — conserta o que já estava envenenado, sem esfriar o livro.
3. `tests/test_freeze.py` — invariante exato: **se o hash guardado bate com o fonte,
   o markdown guardado precisa conter a prosa do fonte.** Hash diferente é ignorado
   de propósito (ali o Quarto reexecuta sozinho — é o cache funcionando). Validado
   contra o envenenamento real: achou os 4 arquivos, **incluindo a seção 7.2, que o
   portão do capítulo 7 não tinha visto**. Suíte foi de 21 para 22 testes.

**Ruling O — comparar hashes não detecta nada.** O hash bate; esse é o problema. O
que se detecta é a causa (mtime mudou durante o render) ou o efeito (prosa ausente
do cache). As duas foram implementadas, porque a primeira previne e a segunda pega o
que já passou — inclusive o envenenado antes de o script existir.

**Ruling P — o lixo de render na raiz.** Um render abortado deixava `index.html` na
raiz (a capa vem de `index.qmd`), e nem `make clean` nem o alvo `render` o removiam:
a raiz era poupada de propósito para proteger o `spoiler.html`, que é versionado. A
regra agora distingue os dois: apaga o `.html` que tem um `.qmd` de mesmo nome.

### Erro meu, pego pelo portão do cap. 10

Escrevi no contrato de correção que o classificador que nunca aponta spam é "o par
98,1%/1,4% do teste do Luke". **Errado.** O teste do Luke *aponta* alguém: precisão
1,4%, revocação 0,5%, ambas definidas. Quem tem precisão indefinida e revocação zero
é o outro classificador do cap. 8, o que responde "não tem leucemia" para todo mundo
e acerta 98,6%. O corretor aplicou fielmente o que eu escrevi, e o portão pegou.
**Lição: o contrato de correção precisa da mesma verificação que o texto.**

E um segundo: o texto dizia que subir o limiar acima de 0,5 trocaria falsos negativos
por menos falsos positivos — direção invertida. Subir o limiar derruba FP e paga com
mais FN.

### Perda de dois agentes por limite de API

Os agentes do cap. 11 (correção) e do cap. 12 (escrita) morreram por limite de sessão
**já na fase de verificação** — tinham terminado de escrever. O trabalho foi
recuperado e verificado por mim e pelos portões. **Consequência prática: o brief
sempre manda escrever o relatório em arquivo antes de verificar**, e isso salvou as
duas entregas.

### Cap. 12 antecipou uma deriva sozinho

O capítulo obtém 0,84 para o coeficiente de `amigos` no modelo de uma variável, por
gradiente descendente, enquanto o cap. 11 obteve 0,9039 pela fórmula fechada. Em vez
de esconder, ele tem um `callout-warning` explicando que a diferença é do otimizador
(5.000 passos, lotes de 25, taxa fixa — orbita o mínimo sem pousar) e que o padrão
que importa (0,904 → 0,972 quando as outras variáveis entram) é robusto na solução
exata. Também corrige a leitura frouxa que o cap. 11 deixava: **a regressão múltipla
TEM fórmula fechada** (equação normal); os modelos sem nenhuma começam no cap. 13.

---

## Rodada — capítulos 12 a 14 e as duas primeiras revisões gerais

**FECHADOS:** 5, 6, 7, 9, 10, 11. **Em portão:** 13. **Em correção:** 12.
**Em escrita:** 14. **Callouts faltantes:** 8. **Na fila:** 15, 16, 17.
**Briefs medidos e prontos:** 12 a 17, todos.

### As revisões gerais começaram (tarefa #28), e valeram mais que o esperado

Decidi começá-las sobre o prefixo estável em vez de esperar os 17 capítulos —
o que elas acham vira lição para os capítulos ainda por escrever.

**Frente 1: promessas e dívidas.** Levantou as **135 referências cruzadas** e abriu
o alvo de cada uma. Nenhum Crítico; a restrição de audiência está limpa no livro
inteiro. Quatro promessas quebradas, corrigidas: o cap. 5 dizia que o k-vizinhos é
"o único modelo que não passa por este capítulo" (são quatro: 9, 10, 14, 17,
conferido módulo a módulo); o cap. 2 mandava lembrar de algo "do Capítulo 8" que
está no 1; o cap. 3 dizia "um exemplo que você já conhece, do Capítulo 8", oito
capítulos antes de ele existir; o cap. 8.6 omitia o 12 da lista de regressões.

**Frente 2: os 35 callouts "Na prática" lidos em sequência.** Achou o Crítico
estrutural que nenhuma revisão de capítulo veria: **o cap. 8 tem seis seções e
ZERO callouts "Na prática"** — e por isso `train_test_split` estreia no cap. 9,
um capítulo depois daquele que existe para explicá-lo.

### Ruling Q — revisor que não roda não conta

As duas frentes só valeram porque **executaram** em vez de julgar plausível. A
frente 2 rodou `scikit-learn` 1.9 no container e pegou uma afirmação publicada
errada: o cap. 7 dizia que o `PCA` "pode devolver (0,924; 0,383) ou (−0,924;
−0,383) dependendo de detalhes numéricos do SVD". Conferi com os quatro solvers
e o estocástico em cinco sementes: **sempre o mesmo sinal** — o `svd_flip` fixa
por convenção. A correção ficou melhor que o original, porque agora diz que a
biblioteca escolhe por você sem avisar.

Vale para os briefs futuros: **todo callout "Na prática" tem afirmação sobre
software que nenhuma renderização verifica** (os chunks são `eval: false`). É a
única parte do livro sem rede de proteção automática.

### Dois falsos positivos de revisão, ambos pegos por conferência

1. "O cap. 9.3 não cita PCA nem o cap. 7" — **cita**, linha 86. A busca falhou
   pela minúscula em "capítulo".
2. "O cap. 13 escreve *For Further Investigation* e os outros escrevem
   *Exploration*; uniformize" — **não uniformize.** As duas variantes existem no
   Grus, conferido extraindo o texto do PDF. Apontado por **duas** revisões
   independentes. Agora está marcado no `CLAUDE.md` e num comentário em
   `scripts/gerar-stubs.py`, na fonte.

**Padrão: um revisor errado é sempre plausível. Conferir custa minutos.**

### Erros meus nesta rodada

- **Contrato do cap. 10:** escrevi que o classificador que nunca aponta spam é "o
  par 98,1%/1,4% do teste do Luke". O teste do Luke aponta alguém — precisão
  1,4%, revocação 0,5%, ambas definidas. Quem tem precisão indefinida e revocação
  zero é o outro classificador do cap. 8 (98,6%). O corretor aplicou fielmente o
  que escrevi; o portão pegou. **O contrato precisa da mesma verificação que o
  texto.**

### Achados técnicos que viraram conteúdo

- **Cap. 12:** três mecanismos inventados para explicar o 0,84 (semente, poucos
  passos, imprecisão) — os três falsificados por medição. A causa real é um
  ciclo-limite determinístico do SGD. E a solução exata `[30.579, 0.9725, -1.865,
  0.9232]` é **idêntica dígito a dígito ao que o Grus imprime**: ele publicou a
  exata, o nosso gradiente é aproximado.
- **Cap. 13:** o `assert` de igualdade exata de float **passa por sorte** — `==`
  vale em 2.169 de 5.000 épocas, `isclose` em 5.000 de 5.000, e só 8 de 200
  produtos escalares são bit-idênticos. O capítulo absolvia o construto que o
  cap. 10 condena; agora concorda com ele.
- **Cap. 13:** sem reescalonar, o ajuste **mente antes de quebrar** — perda `-0.0`
  no primeiro ponto, `ValueError` no segundo. Melhor material do capítulo, e não
  estava no meu brief: o escritor achou.

### Infra desta rodada

- `scripts/render-seguro.sh` (lock + detecção de edição concorrente),
  `make refresh CAP=NN`, `tests/test_freeze.py`, `tests/test_gradiente.py`.
  Suíte: 21 → **24 testes**.
- Lixo de render na raiz (`index.html`) agora é limpo pela regra "apaga o `.html`
  que tem um `.qmd` de mesmo nome", que preserva o `spoiler.html` versionado.

---

## Rodada — capítulos 14 a 17, e duas falhas de infra que eu mesmo criei

**FECHADOS:** 5, 6, 7, 9, 10, 11, 12, 13. **Em correção:** 14. **Escrito, à espera
de verificação:** 15. **Em escrita:** 17. **Não escrito:** 16 (o último).

### Ruling R — o lock precisa desistir antes do teto da ferramenta

O lock que criei de manhã para o `_freeze` envenenado causou o problema da tarde:
ele esperava indefinidamente, mas a ferramenta de shell dos agentes aborta em 10
min. Com quatro agentes na fila, o `make render` estourava o teto e o agente
recebia um **timeout opaco**. O escritor do cap. 15 encerrou o turno esperando —
capítulo escrito, verificação nenhuma. (O `_freeze` mostra que as células *chegaram*
a executar; o que se perdeu foi a conferência.)

Agora: espera limitada a ~7 min, saída com **75 (EX_TEMPFAIL)** e mensagem dizendo
"rode de novo, nada está errado". Detecção de lock órfão passou a olhar a **idade do
diretório**, não a contagem de iterações — correta mesmo para quem entrou no meio.

**A parte que é minha, não dos agentes:** não deixar mais de dois ou três agentes que
precisem renderizar ao mesmo tempo. Está no CLAUDE.md.

### Ruling S — arquivo sendo escrito não é defeito

Uma rodada de `make teste` falhou sem nada de errado por trás: o `test_freeze` leu um
`html.json` **enquanto o Quarto o escrevia**. Um JSON pela metade é evidência de que
alguém está trabalhando, não de cache envenenado. Corrigido e provado truncando um
arquivo real.

### O achado da rodada — cap. 14, o braço que faltava

A revisão de conteúdo mediu **a alternativa que o capítulo não testou**. O experimento
da §14.6 compara floresta contra árvore **sem poda** e conclui que a floresta compra
generalização ao preço da legibilidade. Mas a regra do conjunto sintético usa dois
atributos, e uma árvore `max_depth=2` acerta **1,0000** contra 0,9284 da melhor
floresta (medido duas vezes). O modelo mais legível é o mais preciso, e o fecho da
seção afirma o contrário.

**Nem os números nem o desenho estavam errados — faltava um braço, e a conclusão não
sobrevive a ele.** É o tipo de erro que passa por rigoroso: quatro braços medidos com
cuidado, tudo reprodutível, e ainda assim provando o que o autor já queria provar.

Vale como padrão: **a revisão didática havia defendido o experimento** (com razão,
sobre o desenho). Só quem mediu uma alternativa viu o problema. As duas faixas não são
redundantes, e nenhuma das duas basta sozinha.

### Terceira frente da revisão geral: as figuras

43 figuras abertas, capítulos 1 a 13. Nenhum Crítico — nenhuma contradiz a própria
legenda, e a correção de proporção de eixos do PCA funcionou. O achado que importa é
uma ironia: **o cap. 3 gasta uma figura inteira ensinando que gráfico sem rótulo de
eixo é defeito, e 15 figuras dos caps. 7, 8 e 9 não têm rótulo nenhum.** Mais: `epoch`
virando `época` só no cap. 13, contra a convenção que o cap. 5 estabelece.

### Cap. 14 FECHA — e o braço que faltava mudou a conclusão

O portão reproduziu tudo dígito a dígito. O experimento da §14.6 agora tem os
braços podados: **árvore `max_depth=2` = 1,0000** (treino 0,8495), prof. 1 = 0,7728,
prof. 3 = 0,9461, contra floresta 3-de-8 = 0,9284 e árvore sem poda 0,8239. O fecho
foi reescrito: a troca "nem sempre precisa pagar", e aqui o modelo mais legível é o
mais preciso.

O I2 também foi medido: uma coluna de puro ruído ganha **0,131 bit em média, com zero
sorteios nulos em 1.000**, contra 0,048 do `phd`. A frase "nenhum atributo é puro
ruído aqui" era inferência inválida — ganho de informação é ≥ 0 por construção.

**Ruling T — `max_depth` no corpo da §14.6 fica.** O M1 mandou tirar nome de API do
`scikit-learn` do corpo (era o `oob_score`, gratuito). Aqui `max_depth` virou o
**assunto** do braço novo, não uma menção de passagem; ancorá-lo uma vez ajuda. A
regra continua valendo para menções gratuitas.

**Ruling U — a §14.6 ficou com 9 callouts, e tudo bem.** O M16 pedia enxugar; o C1 e
o I1 exigiram um callout novo cada. A §14.3 caiu de 7 para 6 como pedido. Densidade
alta numa seção que agora carrega duas correções estruturais é troca aceitável.

---

## Rodada final — os 17 capítulos escritos

**FECHADOS:** 5, 6, 7, 9, 10, 11, 12, 13, 14, **17**. **Em correção (rodada 2):** 15.
**Escrito, aguardando revisão:** 16 (2.412 linhas, o maior do livro).
**Nenhum stub resta no livro.**

### Ruling V — o contrato de correção precisa da mesma verificação que o texto

**Segunda vez que escrevo um contrato errado e só o portão seguinte pega.** A primeira
foi o teste do Luke, no cap. 10. Agora: mandei o cap. 15 usar "a **distância** entre
treino e teste" como critério, e o critério não discrimina — árvore sem poda **cai**
17,3 pontos, árvore de profundidade 2 **sobe** 15,0. Distâncias parecidas, sentidos
opostos. A palavra certa era **queda**.

O corretor aplicou fielmente, como devia. **Um critério que eu proponho sem testar
contra os próprios números do parágrafo é exatamente o que um corretor obediente
reproduz sem questionar.**

### Ruling W — nunca editar um `.sh` que agentes estão rodando

Editei `scripts/render-seguro.sh` para acrescentar o orçamento de tempo **enquanto um
agente o executava**. O bash lê o script incrementalmente: ele perdeu a posição e
estourou `syntax error near unexpected token 'done'` — erro de sintaxe que não existia,
num script que passa em `bash -n`. O agente gastou tempo investigando um defeito que
não era dele. Remédio: arquivo temporário e `mv` (atômico; o bash em execução continua
no inode antigo). Registrado no CLAUDE.md.

### Ruling X — o meu teto de shell é o mesmo dos agentes: 10 min

Eu vinha assumindo que podia esperar mais que eles. Não posso — o `timeout` que passo
é limitado a 600 s igual. Isso **confirma** que o orçamento de 420 s no script está
dimensionado certo para todos, inclusive para o coordenador.

### O fecho do livro

A revisão didática do cap. 17 achou o melhor defeito possível para um último capítulo:
o fecho dizia "o Capítulo 1 prometeu uma coisa só: abrir as caixas-pretas". O cap. 1
promete **duas**, e a segunda — "identificar usos que ajudam pessoas e usos que as
manipulam, e perceber que a técnica é a mesma nos dois" — era a **única promessa de
abertura que o fecho não conferia**. A §17.1 chega a reabrir o fio (cadastro de
eleitores) e ninguém voltava a ele.

Escrevi o parágrafo eu mesmo e mandei o portão julgá-lo **sem me poupar**. Ele conferiu
contra o texto real do cap. 1 e confirmou: a segunda metade é reúso **verbatim** da
promessa, o par de usos vem da própria §17.1, e não promete o que o livro não fez.

### Decisão de escopo registrada

**Não** escrever o callout sobre `adjusted_rand_score` na §17.4, que a revisão sugeriu.
O capítulo passa seis seções fechando a porta do "mas e se houvesse rótulos"; reabri-la
no penúltimo callout enfraquece a lição central por ganho pequeno.

### Cap. 15 FECHA — e o portão testou a semente, que eu não pedi

O portão validou a subseção nova (a simetria de período 4) reproduzindo o treino inteiro do
zero e conferindo os oito números. Depois fez a checagem que faltava no meu contrato: rodou
com **sementes 1 e 2**. A recuperação parcial acontece também, mas **em grupos diferentes** —
{1,5,9} a 4–5% e {3,7} a 8% na semente 2, enquanto {0,4,8} se perde a 19–73%.

Ou seja: **a rede sempre acha alguma simetria, mas qual ela acha é sorteado.** Isso não
desmente o texto — confirma a palavra "irregular" que o contrato exigiu, e o texto em nenhum
ponto generaliza os oito números.

**Não levei isso para o livro**, e a razão é a mesma lição de sempre: três sementes não
sustentam "sempre acha alguma". Seria repetir o "1 em 3, medido em 5 rodadas" com outra roupa.

### Ruling Y — medição única sob carga não é medição

O portão achou **o único defeito que uma correção minha introduziu** em todo o projeto: o M3 da
rodada 2 do cap. 15 mandou trocar "~0,4 s" por "~2 s" no tempo do `lbfgs`, com base numa
medição única feita enquanto outros agentes rodavam. Medi de novo, isolado, três vezes:
**0,32 / 0,32 / 0,41 s**. O número original estava certo e eu o piorei.

Mesma lição que o projeto já tinha aprendido com a asserção sem semente do `working_with_data`
("1 em 3, medido em 5 rodadas" contra 25% em 20.000). **Vale explicitamente para medições de
TEMPO, que são as mais sensíveis à carga da máquina — e este livro é escrito com cinco agentes
rodando ao mesmo tempo.**

### Ruling Z — eu erro mais quando corrijo direto do que quando encomendo

Na correção do bloqueio do cap. 16 eu introduzi **dois** defeitos em duas frases:

1. O parágrafo de handoff que mandei escrever reproduzia a abertura do cap. 17 em **sete de
   sete batidas**. O portão citou o precedente do próprio projeto (commit `ade17fe`, onde eu
   consertei exatamente isso no cap. 17) — e eu não percebi ao ler o relatório do corretor.
2. Ao consertar, escrevi "Trezentos epochs custam **pouco mais** de um terço" de 1.000. É
   300/1000 = 0,30, que é **menos** de um terço (0,333). Razão pura, independente de hardware:
   conta errada, não medição frágil.

Nenhum dos dois passou de uma passagem de portão. Mas os dois foram **meus**, escritos direto,
sem contrato e sem revisão prévia — e é o padrão da sessão inteira: os erros que sobrevivem
mais tempo são os que eu escrevo com pressa entre despachos, não os que os agentes escrevem
sob contrato.

**Consequência prática:** quando eu corrigir direto em vez de encomendar, o portão seguinte
precisa saber disso explicitamente, para olhar o meu texto com o mesmo ceticismo que olharia o
de um agente. Já venho pedindo isso ("não me poupe") — vale manter.

---

## Revisão geral do livro — quatro frentes sobre os 17 capítulos

**Todos os 17 capítulos fecharam individualmente.** Esta rodada corrigiu o que só aparece
olhando o livro inteiro. Quatro frentes: promessas cruzadas (2ª passada, 285 ligações), os 80
callouts "Na prática" (2ª passada, ~45 afirmações executadas), as 63 figuras (2ª passada), e a
deriva de terminologia — que nunca tinha rodado.

### O padrão que a revisão geral revelou: superlativos

**A classe de defeito mais produtiva do projeto inteiro** são afirmações sobre o livro todo
escritas de dentro de um capítulo — e portanto **não verificáveis de lá**. Encontrados e
corrigidos: "o único modelo que não passa por este capítulo" (eram quatro), "o único treino que
demora o suficiente para o tqdm", "é a última coisa que este livro constrói", "o chunk mais caro
deste livro", "o primeiro modelo que um humano lê", "o único que introduz uma técnica sem
demonstrar que serve", "o único em que esse preço aparece medido", "o único fecho que não roda de
fábrica", "a única seção cujo fecho não é o scikit-learn".

**Nove.** E dois deles entraram *na rodada que corrigia os outros*.

### Ruling AA — eu corrijo pior do que encomendo, e agora tem número

Nesta sessão escrevi **nove** defeitos corrigindo direto, sem contrato e sem revisão prévia:

1. o par 98,1%/1,4% do teste do Luke (contrato do cap. 10);
2. o critério "distância" que não discriminava os casos que apresentava (cap. 15);
3. um tempo piorado a partir de medição única sob carga (cap. 15);
4. um parágrafo que duplicava a abertura do cap. 17 em sete de sete batidas (cap. 16);
5. "pouco mais de um terço" quando 300/1000 = 0,30 é menos (cap. 16);
6. "dez mil imagens de teste" quando o capítulo fixa duas mil (cap. 16);
7. texto verde sobre barra verde, que apagou um número da figura (cap. 14).

E o oitavo, que é o mais instrutivo: **corrigi um superlativo falso e deixei o gêmeo dele na
linha imediatamente acima, no mesmo parágrafo.** Li a frase que o portão citou e não li a
anterior.

Nenhum passou de um portão. **A prática que funciona:** quando eu corrijo direto, o portão
seguinte recebe a lista dos meus erros anteriores e a instrução de olhar o meu texto com mais
ceticismo que o de um agente.

### Ruling AB — "zero pixels de diferença" precisava de escopo

Afirmei num commit que duas figuras eram idênticas com "zero pixels de diferença". O portão
mediu: são idênticas **na área de plotagem**; a faixa do título difere por construção, porque os
títulos são diferentes. A afirmação do livro ("podem ser sobrepostas") se sustenta; a minha, sem
o escopo, era mais forte do que a medição.

**Os dois últimos, acrescentados depois:**

8. **Corrigi um superlativo falso e deixei o gêmeo na linha imediatamente acima**, no mesmo
   parágrafo. Li a frase que o portão citou e não li a anterior.
9. **Ao consertar o alinhamento de uns carets, o meu script de realinhamento descartou o `#`
   da linha** — e o bloco de código deixou de ser Python colável. Consertar introduziu o defeito
   seguinte, no mesmo lugar, na mesma sessão.

### A varredura final de superlativos: onze, no total

Pedi ao portão que varresse o livro inteiro atrás da construção, em vez de conferir caso a caso.
Achou mais dois, ambos **contraditos dentro do próprio capítulo**:

- `cap13/05:291` — "o gradiente descendente virou a única via até um modelo. **É assim no resto
  do livro**", desmentido **três linhas abaixo** (a árvore "não tem gradiente") e pelo
  `cap05/index:20`, que lista quatro modelos sem gradiente, dois deles posteriores ao cap. 13.
- `cap17/06:351` — no **parágrafo de fecho do livro**: "é apropriado que seja **o único** sem
  resposta certa". O capítulo inteiro não tem gabarito, o k-means da §17.2 inclusive.

**Onze superlativos falsos no total.** É a classe de defeito mais produtiva do projeto, e a
explicação é estrutural: são afirmações sobre o livro inteiro **escritas de dentro de um
capítulo**, por um agente que só via aquele capítulo — e portanto não verificáveis de onde
foram escritas. Nenhuma revisão por capítulo as pega. **Só uma varredura do livro completo pega,
e ela precisa ser por construção gramatical, não por assunto.**
