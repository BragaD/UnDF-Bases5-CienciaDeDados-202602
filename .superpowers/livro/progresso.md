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
