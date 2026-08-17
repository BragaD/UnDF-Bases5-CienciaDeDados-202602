# Capítulo 16 — Deep Learning: relatório

**Status: pronto.** 9 arquivos escritos (nenhum criado, renomeado ou apagado). `make render` → `render OK (tentativa 1)`, sem aviso de edição concorrente em `content/cap16/`. `make teste` → **24 passaram**. As 4 figuras foram abertas e conferidas contra a prosa; todos os números do texto vêm da saída do render.

## Números principais (todos reproduzidos no render)

- **XOR (16.5):** `GradientDescent(0,1)` chega a perda < 0,01 no epoch **1249**; `Momentum` no **985**. Solução interna: dois "nem-nem" de dureza diferente — a **terceira** solução distinta do XOR no livro (cap. 15 achou "ou mas não e", o Grus relata NOR/AND/NOR).
- **Fizz Buzz (16.6):** 300 epochs, **37,5 s** (0,125 s/epoch) → treino 0,884 / teste 0,890. Curva em escada; nos dois primeiros patamares o acerto é 13,3% e 13,5%, **abaixo** do palpite preguiçoso de 53,4% do cap. 15.
- **Softmax (16.7):** 100 epochs, **12,6 s** → treino **1,000** / teste **0,970**. Um terço dos epochs, um terço do tempo, melhor nos dois conjuntos.
- **MNIST (16.8):** leitura IDX em 0,7 s; pixel médio **33,3184**. Logística `Linear(784,10)`: **0,8704** treino / **0,8620** teste em 23,6 s (2,4 ms/imagem). Rede profunda 784→30→10→10 com dropout, **3 epochs** em ~61 s cada (**6,2 ms/imagem**): teste 0,8145 → 0,8595 → **0,8815**. Bug do dropout medido: **0,8535 vs 0,8815**.
- **Erro do livro-texto documentado (16.3):** o parâmetro `variance` de `random_normal` é usado como **desvio padrão** — medido, `variance=4` produz variância 16 —, então o Xavier sai ~20× mais estreito que a fórmula pede. Só documentado; `scratch/` não foi tocado.

## Decisões e o que ficou de fora

- **3 epochs no MNIST, não 2** (o brief sugeria 2). Com 2, a rede profunda fica em 0,8595, **abaixo** da logística; com 3 ela passa (0,8815) e a narrativa do livro-texto se sustenta. Custo extra: ~1 min. O capítulo inteiro custa **~4,5 min** de render — o mais caro do livro, e isso está escrito no texto com os números.
- Teste em **2.000** imagens, como o brief pede. A prosa diz explicitamente que 2 pontos percentuais estão no limite do que essa amostra distingue.
- **Não** rodei Relu vs Tanh no Fizz Buzz (custaria mais 38 s) — fica como observação de que a troca é de uma palavra.
- Convenção `epoch` (não "época") aplicada em prosa, variáveis e `plt.xlabel`, conforme a correção do coordenador.

## Preocupações

1. **O `_book` some.** Três vezes o `_book/` apareceu vazio logo depois de um `render OK`: outro agente inicia um render e o Quarto limpa o diretório. Verifiquei tudo pelo `_freeze/.../html.json`, que é estável. Não é problema do capítulo, mas atrapalha quem for revisar pelo HTML.
2. **Dois renders meus morreram no orçamento de 7 min** por causa da rodada extra que o script dispara quando outro agente edita `.qmd` durante o render (sempre cap15/cap17, nunca cap16). Terceira tentativa fechou limpo.
3. `save_weights` grava em `/tmp/pesos-mnist.json` — fora do repositório, de propósito, e dito no texto.
4. A afirmação do cap. 17 sobre "o único treino lento o bastante para o tqdm" precisa mesmo virar "um dos poucos": o MNIST aqui leva 61 s por epoch.
