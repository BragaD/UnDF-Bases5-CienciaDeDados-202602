# Capítulo 16 — Deep Learning: brief de escrita

Corresponde ao **capítulo 19 do Grus**, *Deep Learning*. **Oito seções agrupadas de 12** — o
Grus intercala exemplos entre os conceitos, e aqui cada exemplo mora junto do conceito que
demonstra. Os arquivos já existem como stubs em `content/cap16/`. **Não crie nem renomeie.**

| arquivo | título | seções do Grus agrupadas |
|---|---|---|
| `01-o-tensor.qmd` | O Tensor | *The Tensor* |
| `02-a-abstracao-de-camada.qmd` | A Abstração de Camada | *The Layer Abstraction* |
| `03-a-camada-linear.qmd` | A Camada Linear | *The Linear Layer* |
| `04-redes-como-sequencia-de-camadas.qmd` | Redes como Sequência de Camadas | *Neural Networks as a Sequence of Layers* |
| `05-perda-e-otimizacao.qmd` | Perda e Otimização | *Loss and Optimization* + *Example: XOR Revisited* |
| `06-outras-funcoes-de-ativacao.qmd` | Outras Funções de Ativação | *Other Activation Functions* + *Example: FizzBuzz Revisited* |
| `07-softmax-e-dropout.qmd` | Softmax, Entropia Cruzada e Dropout | *Softmaxes and Cross-Entropy* + *Dropout* |
| `08-exemplo-mnist.qmd` | Exemplo: MNIST | *Example: MNIST* + *Saving and Loading Models* |

As seções agrupadas viram `##` dentro do arquivo; o `toc-depth: 4` as mantém no índice lateral.

No PDF na raiz: **página do livro impresso = página do PDF − 20.**

---

## O que este capítulo é, e o risco de escrevê-lo errado

**Ele não ensina um modelo novo. Ele refatora o capítulo 15 numa biblioteca.** A rede do
capítulo 15 era uma lista de listas de listas com laços escritos à mão; aqui ela vira `Layer`,
`Linear`, `Sequential`, `Loss`, `Optimizer` — as mesmas abstrações que PyTorch e TensorFlow
expõem, construídas do zero.

**É o capítulo mais importante do livro para a identidade da disciplina**, e o mais fácil de
escrever mal. O risco é virar um passeio por classes. O que ele precisa entregar é: *quando
você escreve `model = Sequential([Linear(784, 30), Tanh(), Linear(30, 10)])` num framework de
verdade, é isto que está do outro lado.* Cada abstração deve aparecer resolvendo um problema
concreto que o capítulo 15 teve.

## Números já medidos — use estes

**O MNIST está vendorizado, mas em formato bruto.** `dados/mnist/` tem os quatro `.gz` no
formato IDX original do MNIST.

**O `main()` do Grus faz `import mnist` e BAIXA os dados. Isso é proibido duas vezes aqui:** o
pacote `mnist` não está no `pyproject.toml` (decisão registrada no `CLAUDE.md` — ele só serve
para baixar) e **nenhum byte pode vir da rede em tempo de render**, que é a invariante que o
`make offline` e o job `offline` do CI guardam.

**Leitor em Python puro, escrito e testado — 70.000 imagens em 0,6 s, sem numpy e sem rede:**

```python
import gzip, struct

def ler_imagens_idx(caminho):
    with gzip.open(caminho, "rb") as f:
        magico, n, linhas, colunas = struct.unpack(">IIII", f.read(16))
        assert magico == 2051
        buf = f.read(n * linhas * colunas)
    tam = linhas * colunas
    return [list(buf[i * tam:(i + 1) * tam]) for i in range(n)]

def ler_rotulos_idx(caminho):
    with gzip.open(caminho, "rb") as f:
        magico, n = struct.unpack(">II", f.read(8))
        assert magico == 2049
        return list(f.read(n))
```

Conferido: 60.000 imagens de treino e 10.000 de teste, 784 pixels cada, faixa 0–255, e os dez
primeiros rótulos de treino são `[5, 0, 4, 1, 9, 2, 1, 3, 1, 4]` — os canônicos do MNIST. O
primeiro dígito desenha um "5" legível em ASCII, então a orientação está certa (não
transposta). **Pixel médio do treino: 33,3184**, que é o valor para centralizar.

Ler um formato binário à mão é, por si só, uma caixa-preta aberta — o `mnist.train_images()`
que o Grus chama faz exatamente isto e mais um download. Vale um parágrafo.

## O orçamento de render, que é a decisão mais importante do capítulo

**Medido nesta máquina, rede 784→30→10 com `Momentum`: 5,7 ms por imagem.**

| treino | custo de 1 epoch |
|---|---|
| 60.000 (completo) | **~6 minutos** |
| 10.000 | 73 segundos |
| 1.000 | 6 segundos |

**E o `make offline` apaga o `_freeze/` de propósito, então o CI paga esse custo a cada push.**
Não dá para esconder atrás do cache.

**Orçamento medido e recomendado: 10.000 imagens de treino, 2 epochs, teste em 2.000.**
Resultado real: epoch 1 → **87,0%**; epoch 2 → **88,3%**. Custo total ~2,5 min.

**Escreva esse corte no texto, com os números, em vez de escondê-lo.** É a lição do livro
ficando tangível: seis minutos por epoch para uma rede minúscula, num conjunto que um framework
vetorizado processa em segundos. A lentidão é o preço da transparência — aqui ela tem preço em
minutos, medido, e o aluno entende de uma vez por que GPUs existem. Diga também o que aconteceria
com o dataset inteiro e mais epochs, e deixe isso como exercício.

## Pontos onde é fácil escrever mal

- **§1 (O Tensor)** — `Tensor = list`. A tentação de "melhorar" isto com numpy é máxima no
  livro inteiro, e é exatamente aqui que ela destrói mais. O ponto é que um tensor **é** uma
  lista aninhada, e todo o resto é convenção sobre a forma.
- **§2 (A Abstração de Camada)** só faz sentido depois de doer. Amarre ao capítulo 15: lá, o
  `forward` e o `backward` estavam entrelaçados num laço só, e trocar a função de ativação
  significava reescrever o gradiente à mão. A camada existe para separar isso.
- **§5 e §6 revisitam XOR e Fizz Buzz** do capítulo 15. **O ponto não é que funcionam de novo:
  é que agora são cinco linhas de montagem em vez de laços escritos à mão.** Compare os dois
  códigos lado a lado; sem essa comparação, o revisitar é redundante.
- **§7 (Dropout)** é a primeira vez no livro em que um modelo se comporta **diferente no treino
  e na avaliação**. Isso surpreende, e é a origem de um bug clássico (esquecer de desligar o
  dropout na hora de avaliar). Vale `callout-warning`.

## Armadilhas concretas

1. **`scratch.deep_learning` é seguro importar** (0,5 s, nada pesado no corpo do módulo). Expõe
   `Tensor`, `Layer`, `Linear`, `Sequential`, `Sigmoid`, `Tanh`, `Relu`, `Dropout`, `Loss`,
   `SSE`, `SoftmaxCrossEntropy`, `Optimizer`, `GradientDescent`, `Momentum`, `softmax`,
   `one_hot_encode`, `random_tensor`, `save_weights`, `load_weights`, `shape`, `tensor`.
2. **`tqdm`** aparece de novo nos laços de treino: `#| warning: false` no chunk.
3. **Semente explícita** em todo chunk — a inicialização de pesos e o `Dropout` são aleatórios.
4. **Nunca importe** `scratch.getting_data` nem `scratch.working_with_data`; **nunca**
   `import mnist`.
5. Cada `.qmd` renderiza com **kernel próprio** — nomes não cruzam de página. Num capítulo que
   constrói uma biblioteca ao longo de oito arquivos, isso pesa: importe de
   `scratch.deep_learning` (com um callout dizendo que é o mesmo código que acabou de ser
   escrito) em vez de reescrever tudo a cada página.
6. `save_weights`/`load_weights` gravam JSON. Se um chunk gravar arquivo, escolha o caminho com
   cuidado e confira o `.gitignore`.

## Ligações

- **[Capítulo 15](../cap15/index.qmd)** — o pai direto. Este capítulo é aquele, refatorado.
- **[Capítulo 5](../cap05/index.qmd)** — `GradientDescent` e `Momentum` são otimizadores
  construídos sobre o `gradient_step` de lá.
- **[Capítulo 4](../cap04/index.qmd)** — `cap04/02-matrizes.qmd:139` promete que uma camada é
  uma matriz *n*×*k*. **Dívida a cobrar.**
- **[Capítulo 8](../cap08/index.qmd)** — o dropout é regularização; ligue ao sobreajuste. E a
  **[seção 12.8](../cap12/08-regularizacao.qmd)** já fez o argumento de encolher parâmetros.
- **[Capítulo 13](../cap13/index.qmd)** — a softmax generaliza a função logística de lá para
  mais de duas classes. Ligação obrigatória.
