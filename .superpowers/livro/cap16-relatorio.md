# Capítulo 16 — Deep Learning: relatório

**Status: pronto.** 9 arquivos escritos (nenhum criado, renomeado ou apagado). `make render` → `render OK (tentativa 1)`, sem aviso de edição concorrente em `content/cap16/`. `make teste` → **24 passaram**. As 4 figuras foram abertas e conferidas contra a prosa; todos os números do texto vêm da saída do render.

## Números principais (todos reproduzidos no render)

- **XOR (16.5):** `GradientDescent(0,1)` chega a perda < 0,01 no epoch **1249**; `Momentum` no **985**. Solução interna: dois "nem-nem" de dureza diferente — a **terceira** solução distinta do XOR no livro (cap. 15 achou "ou mas não e", o Grus relata NOR/AND/NOR).
- **Fizz Buzz (16.6):** 300 epochs, **37,5 s** (0,125 s/epoch) → treino 0,884 / teste 0,890. Curva em escada; nos dois primeiros patamares o acerto é 13,3% e 13,5%, **abaixo** do palpite preguiçoso de 53,4% do cap. 15.
- **Softmax (16.7):** 100 epochs, **12,6 s** → treino **1,000** / teste **0,970**. Um terço dos epochs, um terço do tempo, melhor nos dois conjuntos.
- **MNIST (16.8):** leitura IDX em 0,7 s; pixel médio **33,3184**. Logística `Linear(784,10)`: **0,8704** treino / **0,8620** teste em 23,6 s (2,4 ms/imagem). Rede profunda 784→30→10→10 com dropout, **3 epochs** em ~61 s cada (**6,2 ms/imagem**): teste 0,8145 → 0,8595 → **0,8815**. Bug do dropout medido: **0,8535 vs 0,8815**.
- **Erro do livro-texto documentado (16.3):** o parâmetro `variance` de `random_normal` é usado como **desvio padrão** — medido, `variance=4` produz variância 16 —, então o Xavier sai ~20× mais estreito que a fórmula pede. Só documentado; `scratch/` não foi tocado.

## Decisões e o que ficou de fora

- **3 epochs no MNIST, não 2** (o brief sugeria 2). Com 2, a rede profunda fica em 0,8595, **abaixo** da logística; com 3 ela passa (0,8815) e a narrativa do livro-texto se sustenta. Custo extra: ~1 min. O capítulo inteiro custa **~5 min** de render (o número corrigido; ~4,5 min era só a soma dos cronômetros impressos, sem imports, avaliações, figuras e os 9 kernels) — o mais caro do livro, e isso está escrito no texto com os números.
- Teste em **2.000** imagens, como o brief pede. A prosa diz explicitamente que 2 pontos percentuais estão no limite do que essa amostra distingue.
- **Não** rodei Relu vs Tanh no Fizz Buzz (custaria mais 38 s) — fica como observação de que a troca é de uma palavra.
- Convenção `epoch` (não "época") aplicada em prosa, variáveis e `plt.xlabel`, conforme a correção do coordenador.

## Preocupações

1. **O `_book` some.** Três vezes o `_book/` apareceu vazio logo depois de um `render OK`: outro agente inicia um render e o Quarto limpa o diretório. Verifiquei tudo pelo `_freeze/.../html.json`, que é estável. Não é problema do capítulo, mas atrapalha quem for revisar pelo HTML.
2. **Dois renders meus morreram no orçamento de 7 min** por causa da rodada extra que o script dispara quando outro agente edita `.qmd` durante o render (sempre cap15/cap17, nunca cap16). Terceira tentativa fechou limpo.
3. `save_weights` grava em `/tmp/pesos-mnist.json` — fora do repositório, de propósito, e dito no texto.
4. A afirmação do cap. 17 sobre "o único treino lento o bastante para o tqdm" precisa mesmo virar "um dos poucos": o MNIST aqui leva 61 s por epoch.

---

# Adendo — rodada de correções (`cap16-correcoes.md`)

**Status: aplicado por inteiro.** 1 Crítico, 6 Importantes, 12 Menores — nenhum ficou de fora.
9 arquivos tocados, nenhum criado/renomeado/apagado. `make render` → `render OK (tentativa 1)`
(duas vezes; a segunda depois de um ajuste final em `08`). `make teste` → **24 passaram**.
Nada da seção "Não mexa nisto" foi tocado. Nenhum outro capítulo foi editado.

## O que mudou

- **C1** — `08:9` agora diz "este **capítulo**". E "O fim do arco" ganhou um parágrafo entregando o
  [Capítulo 17](../cap17/index.qmd) pelo pivô que ele é: dezesseis capítulos com gabarito ("a flor
  era *setosa*, o dígito era um 7"), e o próximo sem nenhum. O capítulo deixou de ser o único que
  não passa o bastão.
- **I1** — Três frases de franqueza na §7: 0,9020 no treino contra 0,8815 no teste, não há
  sobreajuste para o dropout consertar, não há comparação com e sem, e ele está ali porque o
  livro-texto o põe ali — é o comportamento que se mede, não o benefício.
- **I2** — `gradient_step` agora é linkado ao [Capítulo 5](../cap05/index.qmd) nos dois lugares
  (`:74` e o `.conceito` do `Momentum`), com a frase que faz a ponte: lá era **um** vetor.
- **I3** — A afirmação sobre `optim.SGD` virou ressalva com as duas fórmulas escritas:
  $u \leftarrow \mu u + (1-\mu)g$ converge para $1\times g$; $b \leftarrow \mu b + g$ converge para
  $10\times g$. Traduzir `lr=0.1` daqui para lá pede `lr=0.01`.
- **I4** — A §7 agora lê a própria tabela: teste 0,530 → 0,460 → **0,340** (epoch 25) → 0,730 →
  0,970, com a perda caindo o tempo todo. É a escada da §6 invertida.
- **I5** — O payoff da recursão passou a ser o do próprio livro (`params()` entregando `[30,784]`
  e `[30]` ao mesmo `tensor_combine`, sem um `if`), e a §1 admite na abertura que este livro nunca
  passa de duas dimensões.
- **I6** — "exatamente o mesmo resultado" → "não mudaria nada no que o modelo pode aprender", com
  a razão (os pesos são sorteados numa ordem fixa e não acompanham a permutação).
- **Menores** — M1 título "**Seis** funções"; M2 a frase dos 3 epochs (0,8595 < 0,8620) dentro da
  caixa de orçamento; M3 número do render corrigido acima; M4 "quase triplicou", ~2,7×; M5
  reordenado (o `w_grad` é sobrescrito no `backward`, e o `step` aplica duas vezes o **mesmo**
  passo); M6 a repetição do `plt.*` na §3 virou ponteiro para a §2; M7 o terceiro tipo de erro
  ($n=4$, 0,892 errado com 0,105 vivo na resposta certa); M8 `keras.Sequential` com código na §4,
  fechando a promessa de TensorFlow do `index.qmd`; M9 a posição do `Dropout` antes da `Tanh`
  ($\tanh(0)=0$); M10 "em menos de um segundo" (0,66 s); M11 a repetição de "biblioteca"; M12 o
  argumento da ativação não centrada marcado como leitura da área, não do livro-texto.

## Preocupações

1. **Todos os números foram reconferidos no `_freeze` pós-render e não mudaram** — o capítulo é
   estável entre rodadas. Só os cronômetros oscilam (2,30 → 2,26 ms/imagem na logística; 6,15 →
   5,99 na rede profunda), e foi por isso que o "2,7 vezes" do M4 ficou hedgeado com "cerca de".
2. **A §7 continua sem provar que o dropout ajuda** — isso agora está dito em vez de implícito,
   que era o pedido do I1, mas segue sendo a única técnica do capítulo introduzida sem
   demonstração de benefício. Consertar de verdade custaria um treino a mais (com e sem), e o
   orçamento do capítulo já é o maior do livro.
3. **O `Dropout` entre `Linear` e `Tanh` foi mantido** (é o livro-texto), agora com a explicação.
   Se algum dia o capítulo trocar `Tanh` por `Sigmoid` ali, a posição passa a estar errada de
   fato — a caixa do M9 diz isso.
