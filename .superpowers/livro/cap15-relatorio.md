# Cap. 15 — Redes Neurais: relatório de escrita

**Status:** 5 arquivos escritos (`index` + 4 seções). Nenhum arquivo criado, renomeado ou apagado.

**Verificação:** `render OK (tentativa 2)` no primeiro render. O aviso de edição concorrente
apontou `cap14/06`, `cap17/06` e `cap17/index` — **nenhum arquivo do cap. 15**, então o `_freeze`
deste capítulo é confiável. Conferi todas as saídas executadas dentro de
`_freeze/content/cap15/*/execute-results/html.json` e abri as três figuras: cada número do texto
bate com a saída, e cada figura mostra o que a prosa diz que ela mostra. Depois disso fiz três
correções de precisão (ver "Correções pós-render") e rodei um segundo render + `make teste`.

## Números — todos medidos no container, nenhum de memória

- **XOR** (`seed(0)`, 2→2→1, taxa 1,0, 20.000 épocas, 0,45 s): `[0,0]→0,009034` · `[0,1]→0,992329` ·
  `[1,0]→0,992328` · `[1,1]→0,007856`. Pesos finais **arredondam exatamente** para
  `[7,7,-3]`, `[5,5,-8]`, `[11,-12,-5]` — os três vetores que o Grus imprime. Camada escondida
  aprendida: neurônio 1 = **OU**, neurônio 2 = **E** — **ordem trocada** em relação à rede feita
  à mão na §2. Virou o gancho da interpretabilidade.
- **Correção ao brief (simetria):** a simetria do XOR relaciona só o par do meio (0,992329 /
  0,992328) e os pesos dentro de cada neurônio (6,9535/6,9528; 5,1159/5,1154). `[0,0]` e `[1,1]`
  são cada um a troca de si mesmos — nada força que sejam iguais, e não são (0,009034 × 0,007856).
  O texto diz isso explicitamente.
- **Fizz Buzz** (`seed(0)` fresco, 10→25→4, taxa 1,0, 500 épocas, 923 exemplos, ~47 s):
  **96/100** no teste (1–100, nunca vistos), 903/923 = 97,8% no treino. Erros: 4 e 34 (disse
  "fizz"), 70 e 100 (disse o número). Base do "sempre a classe majoritária" = 53/100.
- **O melhor achado, não previsto no brief — o platô É o palpite preguiçoso.** A perda cai de
  2768,9 para ~596 e fica quase parada da época 15 à 120. Medido: nas épocas **20 e 50 a rede
  responde "o próprio número" para os 923 exemplos**, acertando 493/923 = 53,4% — exatamente o
  classificador-base do cap. 8. Só depois ela escapa. Isso rende o fecho do "Na prática":
  `MLPClassifier(hidden_layer_sizes=(25,), activation='logistic')` **para na iteração 51** e
  devolve 0,53 — o critério `tol=1e-4`/`n_iter_no_change=10` lê o platô como convergência. O
  nosso laço atravessa o platô porque não tem critério de parada nenhum.
- **Outros valores do "Na prática" (sklearn 1.9, medidos):** `Perceptron` aprende E com
  `[[3,2]]/-4` e OU com `[[2,2]]/-1` (idênticos aos escolhidos à mão pelo Grus); no XOR devolve
  `coef_=[[0,0]]`, `intercept_=[0]`, acurácia 0,5, **sem aviso nenhum**. `MLPClassifier` no
  Fizz Buzz: `(100,)+relu` = 0,860 teste em ~2 s; `(25,)+logistic+lbfgs` = 0,850 em ~0,4 s.
  `coefs_`/`intercepts_` são separados (o truque do viés é contabilidade nossa);
  `out_activation_='softmax'`, `loss='log_loss'` no caso multiclasse.

## Decisões de escrita

- A troca degrau→sigmoide está na §2, num `.conceito`, dita como o brief pediu: a derivada do
  degrau é zero onde existe e indefinida no salto, então **nada do cap. 5 se aplica** sem a troca.
  Figura de duas faixas: as funções e as derivadas.
- §3 constrói a retropropagação pela ideia de **culpa** (∂perda/∂z) antes de qualquer álgebra:
  culpa direta na saída, culpa de um peso = culpa do neurônio × a entrada que ele multiplica,
  culpa emprestada nos escondidos. A derivação completa fica num `.exemplo` opcional.
- Dois achados de leitura do código viraram callout: **o fator 2 que sumiu** (`output_deltas` é o
  gradiente exato de *metade* da soma dos quadrados; a §4 imprime a soma inteira) e
  **`sqerror_gradients` só funciona para duas camadas** (`hidden_outputs, outputs = feed_forward(...)`
  desempacota exatamente dois) — que é a motivação direta do cap. 16.
- Arco da interpretabilidade: anunciado no `index`, plantado no `.conceito` do fim da §3 (a rede
  achou os mesmos dois atributos em ordem trocada; soluções equivalentes) e fechado na §4.

## Correções pós-render (minhas, na releitura)

Três afirmações que eu tinha escrito e que a verificação não sustentava:

1. **§1** dizia que, no XOR, "as correções da regra de treino se cancelam exatamente" — mecanismo
   que eu não medi. Testei seis sementes: os pesos finais **variam** (`[[0,0]]`, `[[0,-1]]`,
   `[[1,0]]`…), a acurácia dá **0,5 nas seis**. O texto agora afirma o que foi medido.
2. **§4** dizia que no platô "cada alteração isolada piora a perda". Falso: a perda **cai**, de
   ~597 (época 25) a ~589 (época 100) — o gradiente existe e aponta certo, só é minúsculo.
   Reescrito com os números.
3. **§2** o chunk da figura usava `dir` como nome de eixo, sombreando a builtin. Renomeado.

## O que ficou de fora, e por quê

- **Nenhum corte de iterações.** 20.000 épocas no XOR e 500 no Fizz Buzz, como o brief mandou.
- Não usei `MLPRegressor`, nem PyTorch/Keras em código: só afirmações que consegui medir no
  container. As menções a autodiff em §3 são conceituais, sem número.
- A `Figure 18-1` do Grus (espaço de decisão) foi refeita como três painéis E/OU/XOR em vez de
  reproduzida — a impossibilidade do XOR ficou mais visível assim, e ganhou prova algébrica de
  quatro desigualdades num `.exemplo`.

## Preocupações

1. A §4 é o chunk mais caro do livro (~1 min). Com `freeze: auto` isso só dói quando o arquivo
   muda, mas quem for corrigir a §4 paga o minuto a cada rodada.
2. A tabela do "Na prática" da §4 mostra a nossa rede (0,96) acima da melhor configuração de
   biblioteca testada (0,86). Escrevi explicitamente que isso **não** quer dizer que o nosso
   código é melhor — 100 números de teste, dez acertos de diferença. Se uma revisão quiser mexer
   nesse trecho, é aí que ele pode virar propaganda por acidente.
3. O `index` promete que o cap. 16 generaliza esta rede numa biblioteca de camadas. O cap. 16
   ainda é stub — é dívida a cobrar de quem o escrever.
