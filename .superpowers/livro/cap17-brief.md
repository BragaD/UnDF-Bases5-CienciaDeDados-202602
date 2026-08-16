# Capítulo 17 — Clustering: brief de escrita

Corresponde ao **capítulo 20 do Grus**, *Clustering*. Seis seções. É o **último capítulo do
livro**. Os arquivos já existem como stubs em `content/cap17/`. **Não crie nem renomeie.**

| arquivo | título | seção do Grus |
|---|---|---|
| `01-a-ideia.qmd` | A Ideia | *The Idea* |
| `02-o-modelo.qmd` | O Modelo | *The Model* |
| `03-exemplo-encontros.qmd` | Exemplo: Encontros | *Example: Meetups* |
| `04-escolhendo-k.qmd` | Escolhendo k | *Choosing k* |
| `05-exemplo-clustering-de-cores.qmd` | Exemplo: Clustering de Cores | *Example: Clustering Colors* |
| `06-clustering-hierarquico.qmd` | Clustering Hierárquico Bottom-Up | *Bottom-Up Hierarchical Clustering* |

No PDF na raiz: **página do livro impresso = página do PDF − 20.**

---

## O que muda de categoria — e é a maior mudança do livro inteiro

**Este é o primeiro e único modelo não supervisionado do livro.** Todos os dezesseis capítulos
anteriores tinham uma resposta certa: uma espécie de íris, um rótulo de spam, minutos por dia,
um dígito. Aqui **não há rótulo nenhum**, e portanto não há acurácia, precisão, revocação, R²
nem conjunto de teste. Todo o vocabulário de avaliação do capítulo 8 deixa de se aplicar.

Isso precisa ser dito de frente, e cedo. O aluno vem de dezesseis capítulos em que "funciona"
significava "acerta"; aqui a pergunta muda para *o agrupamento é útil?* — e a resposta depende
do que se vai fazer com ele. A §4 (escolhendo *k*) é onde essa mudança dói, porque não existe
um *k* correto a descobrir.

**É também o capítulo de fechamento do livro.** O `index.qmd` dele e a última seção carregam
uma responsabilidade que nenhum outro capítulo tem: fechar o arco inteiro. Vale olhar o que o
livro prometeu no capítulo 1 e conferir o que foi entregue.

## Números já medidos — use estes

**Os 20 pontos dos encontros** (§3, §4, §6) vivem dentro do `main()` de `scratch/clustering.py`,
linha 163 — copie de lá.

- `random.seed(12)`, k=3 → médias **[−43,80; 5,40]**, **[−15,89; −10,33]**, **[18,33; 19,83]**
- `random.seed(0)`, k=2 → médias **[−25,86; −4,71]**, **[18,33; 19,83]**

**A curva do cotovelo (§4)**, erro quadrático total por *k*, com `random.seed(0)`:

| k | erro total |
|---|---|
| 1 | 15.241,4 |
| 2 | 4.508,7 |
| 3 | **1.209,1** ← o joelho |
| 4 | 1.028,5 |
| 5 | 895,5 |
| 6 | 815,4 |
| 7 | 430,8 |
| 8 | 385,1 |

O joelho em k=3 é nítido: as quedas de 1→2 e 2→3 são enormes (−70% e −73%), e depois a curva
achata. **Mas repare no k=7**, que cai bem mais que o 5→6 e o 6→7 fariam esperar — isso é o
k-means caindo num ótimo local diferente, e é um bom `callout-warning`: a curva não é
monotonicamente suave porque cada ponto dela é uma execução com inicialização aleatória própria.

**Clustering de cores (§5).** A imagem vendorizada é `dados/imagem-cores.jpg` — 592×600,
**355.200 pixels**.

> **O `main()` do Grus lê `girl_with_book.jpg`, que não existe neste repositório.** Use
> `dados/imagem-cores.jpg`, e o caminho é a partir da raiz.

**Medido: k=5 sobre a imagem inteira custa 16,9 s.** Não reduza a amostra; rode nos 355.200
pixels.

A imagem é a *Composition II in Red, Blue, and Yellow* de Mondrian (1930, domínio público), e a
escolha é feliz: um quadro de campos chapados de cor primária é o caso em que o k-means tem uma
resposta quase óbvia, o que torna o resultado legível a olho nu. **Diga isso** — e note que com
uma fotografia comum o resultado seria muito mais ambíguo, o que é justamente o ponto da §4.

**Clustering hierárquico (§6):** sobre os 20 pontos, **instantâneo** (< 0,01 s), tanto com
ligação mínima quanto com máxima. Sem risco de custo.

## Armadilhas concretas

1. **`KMeans.train` usa `tqdm` por dentro.** Todo chunk que treinar precisa de
   `#| warning: false`, senão a barra de progresso despeja lixo na página. Isso me mordeu
   durante a medição: a barra sobrescreveu as saídas com `\r`. O
   [Capítulo 7, §7.7](../cap07/07-um-parenteses-tqdm.qmd) é quem ensina `tqdm`.
2. **`scratch.clustering` é seguro importar** — nada roda no corpo do módulo. Expõe `KMeans`,
   `bottom_up_cluster`, `get_values`, `get_children`, `generate_clusters`, `Cluster`, `Leaf`,
   `Merged`. **`squared_clustering_errors` NÃO está no nível do módulo** — vive dentro de
   `main()`, então escreva-a inline.
3. **Semente explícita em todo chunk.** O k-means inicializa com `random.randrange` e é
   **genuinamente sensível** a isso — muito mais que os modelos de gradiente. Sem semente, cada
   render dá um agrupamento diferente e o texto para de bater com a figura.
4. **Nunca importe** `scratch.getting_data` nem `scratch.working_with_data`.
5. Cada `.qmd` renderiza com **kernel próprio** — nomes não cruzam de página.
6. **Não invente número de seção do Grus:** capítulo + título em itálico.

## Pontos onde é fácil escrever mal

- **§2 (O Modelo)** — o k-means alterna dois passos exatos: atribuir cada ponto ao centro mais
  próximo, e recalcular cada centro como a média dos seus pontos. Ele **converge sempre**, mas
  **para um ótimo local**, que depende da inicialização. Dizer as duas coisas juntas é o que
  separa entender de decorar. E vale conectar ao [Capítulo 5](../cap05/index.qmd): isto é
  otimização **sem gradiente** — o índice do capítulo 5 já nomeia o k-means como um dos quatro
  modelos que não passam por lá.
- **§4 (Escolhendo k)** é a seção conceitualmente mais difícil, porque a resposta honesta é
  "depende". O erro cai sempre que *k* sobe — com *k* = *n* o erro é zero e o agrupamento é
  inútil. **Isso é o mesmo defeito do R² do [Capítulo 12, §12.5](../cap12/05-qualidade-do-ajuste.qmd)**,
  que sempre sobe quando se acrescenta variável. A ponte é forte e o aluno acabou de ver a outra
  ponta.
- **§6 (Hierárquico)** — a escolha da ligação (mínima contra máxima) muda o resultado, e o Grus
  mostra as duas. Não deixe virar detalhe: é a demonstração de que "agrupar" não é uma operação
  única, e sim uma família de decisões.

## Ligações

- **[Capítulo 8](../cap08/index.qmd)** — para dizer o que **não** se aplica aqui.
- **[Capítulo 12, §12.5](../cap12/05-qualidade-do-ajuste.qmd)** — a métrica que sempre melhora.
- **[Capítulo 5](../cap05/index.qmd)** — otimização sem gradiente.
- **[Capítulo 4](../cap04/01-vetores.qmd)** — `cap04/01:145` **promete** que o k-means chama
  `vector_mean`. **Dívida a cobrar.**
- **[Capítulo 9](../cap09/index.qmd)** — o k-means e o k-vizinhos compartilham o `k` no nome e
  quase nada mais. O capítulo 10 já desarmou uma colisão parecida; vale meia frase.
- **[Capítulo 1](../cap01/index.qmd)** — este é o fim do livro. Vale olhar o que o capítulo 1
  prometeu.
