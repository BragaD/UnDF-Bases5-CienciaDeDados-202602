# Capítulo 15 — Redes Neurais: brief de escrita

Corresponde ao **capítulo 18 do Grus**, *Neural Networks*. Quatro seções — a menor unidade do
livro depois do capítulo 11. Os arquivos já existem como stubs em `content/cap15/`, registrados
no `_quarto.yml`. **Não crie nem renomeie arquivo nenhum.**

| arquivo | título | seção do Grus |
|---|---|---|
| `01-perceptrons.qmd` | Perceptrons | *Perceptrons* |
| `02-redes-feed-forward.qmd` | Redes Neurais Feed-Forward | *Feed-Forward Neural Networks* |
| `03-retropropagacao.qmd` | Retropropagação | *Backpropagation* |
| `04-exemplo-fizz-buzz.qmd` | Exemplo: Fizz Buzz | *Example: Fizz Buzz* |

No PDF na raiz: **página do livro impresso = página do PDF − 20.**

---

## A espinha narrativa

Quatro seções, e cada uma existe por causa de um limite da anterior:

> Um neurônio só calcula E, OU e NÃO — **mas não XOR** → empilhar neurônios resolve o XOR, só
> que agora não dá para treinar com a função degrau → a sigmoide torna o treino possível, e a
> retropropagação é como ele funciona → e aqui está a coisa toda aprendendo algo absurdo.

**O ponto conceitual mais importante do capítulo é a troca do degrau pela sigmoide, e ele é
fácil de escrever como detalhe técnico quando é o contrário: é a razão de o capítulo 5 poder
ser usado aqui.** A função degrau tem derivada **zero em toda parte** onde é derivável, e
indefinida no salto. Gradiente descendente sobre ela não tem para onde ir — o gradiente não
diz nada. A sigmoide é a versão "amassada" do degrau que tem derivada útil em todo ponto.
Sem essa troca, nada do capítulo 5 se aplica. Diga isso explicitamente.

## O que muda de categoria neste capítulo

Este é o primeiro modelo do livro com **parâmetros que não significam nada sozinhos**. O
capítulo 12 entregou coeficientes interpretáveis ("cada amigo a mais corresponde a ~0,97
minuto"); o capítulo 14 entrega uma árvore que um humano **lê**. Aqui os pesos da camada
escondida não têm leitura nenhuma — e a rede funciona melhor.

Vale nomear esse arco, porque ele atravessa o livro inteiro e culmina no capítulo 16: **poder
e interpretabilidade andam em direções opostas**, e a disciplina existe justamente para que o
aluno saiba o que está trocando.

## Números já medidos — use estes

**XOR (§2 e §3)** — `random.seed(0)`, rede 2→2→1, taxa 1,0, 20.000 epochs:

- custo: **0,4 s**. Barato; não corte iterações.
- saídas finais: `[0,0] → 0,009034` · `[0,1] → 0,992329` · `[1,0] → 0,992328` · `[1,1] → 0,007856`

Note a **simetria** entre os dois casos do meio (0,992329 e 0,992328) e entre os extremos —
ela não é acidente, é o XOR sendo simétrico nos dois argumentos, e é um bom detalhe para
comentar.

**Fizz Buzz (§4)** — `random.seed(0)`, 10 entradas binárias → 25 escondidas → 4 saídas,
taxa 1,0, 500 epochs sobre os números de 101 a 1023 (923 exemplos):

- custo: **36 s**. Pagável; **não reduza epochs**.
- resultado: **96 de 100** acertos nos números de 1 a 100 — que a rede **nunca viu no treino**.

Esse último ponto merece destaque: o treino usa 101–1023 e o teste usa 1–100, então não há
vazamento. E 96/100 é um resultado engraçado de propósito — a rede quase aprende uma regra que
qualquer aluno escreve com três `if`. **Não deixe a piada engolir a lição**: o interessante é
que ela aprendeu *pela representação binária*, sem ninguém contar o que é divisibilidade.

## Armadilhas concretas

1. **`tqdm` de novo.** O `main()` do Grus usa `tqdm.trange` nos dois treinos. Se você usar,
   o chunk precisa de `#| warning: false`, senão a barra vaza para o livro. O
   [Capítulo 7, §7.7](../cap07/07-um-parenteses-tqdm.qmd) é a seção que a ensina — e o
   capítulo 12 já a usou por dentro do `least_squares_fit`.
2. **`scratch.neural_networks` é seguro importar** (0,0 s, só `assert` no nível do módulo). Ele
   expõe `perceptron_output`, `step_function`, `sigmoid`, `neuron_output`, `feed_forward`,
   `sqerror_gradients`, `binary_encode`, `fizz_buzz_encode`, `argmax`, `xor_network`, e os
   pesos `and_weights` / `or_weights` / `not_weights` com seus vieses.
3. **Cada `.qmd` renderiza com kernel próprio** — nomes não cruzam de página.
4. **Semente explícita** em todo chunk com RNG (a inicialização de pesos é aleatória), do
   `random` da stdlib.
5. **Nunca importe** `scratch.getting_data` nem `scratch.working_with_data`.
6. **Não invente número de seção do Grus:** capítulo + título em itálico.

## Pontos onde é fácil escrever mal

- **§1** costuma virar história da computação. O conteúdo é: um perceptron traça **uma reta**,
  e por isso resolve E/OU/NÃO e **não** resolve XOR — que não é linearmente separável. Vale
  mostrar por que, geometricamente, com os quatro pontos do XOR num plano.
- **§3 (Retropropagação)** é a seção mais difícil do capítulo e talvez do livro. É a regra da
  cadeia aplicada camada a camada. **Ou ela constrói a intuição — o erro na saída é
  redistribuído para trás, proporcionalmente ao quanto cada peso contribuiu — ou vira álgebra
  sem sentido.** Não a escreva como derivação seca; e não a escreva como analogia vaga.
- **§4** tem o risco oposto: é tão divertida que pode virar só a piada. Amarre-a ao capítulo 8
  (o conjunto de teste 1–100 nunca visto) e ao arco de interpretabilidade.

## Ligações

- **[Capítulo 5](../cap05/index.qmd)** — o gradiente descendente que treina isto. **A ligação
  mais importante do capítulo**, via a troca do degrau pela sigmoide.
- **[Capítulo 13](../cap13/index.qmd)** — a função logística **é** a sigmoide. O aluno acabou
  de construí-la ali, por outro motivo. Aponte.
- **[Capítulo 12](../cap12/index.qmd)** e **[14](../cap14/index.qmd)** — o contraste de
  interpretabilidade.
- **[Capítulo 8](../cap08/index.qmd)** — treino e teste, na §4.
- **[Capítulo 16](../cap16/index.qmd)** (Deep Learning) é o próximo: ele generaliza esta rede
  numa biblioteca de camadas. Ainda é stub.
