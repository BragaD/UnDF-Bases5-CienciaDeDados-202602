# Guia para escrever um capítulo

Destilado da escrita dos capítulos 1, 2, 3, 4, 8 e 9. Leia junto com o `CLAUDE.md`.

**O modelo de estilo é `content/cap09/`** (k-Vizinhos). Leia os quatro arquivos dele antes de escrever qualquer coisa — ele fixa a forma. `content/cap08/` é o modelo para capítulos de prosa densa, e `content/cap01/` para capítulos com muito código expositivo.

## A identidade da disciplina

**Bases 5 abre as caixas-pretas que o aluno usou antes.** Todo algoritmo é construído do zero, em Python puro, sem numpy e sem scikit-learn. Só no *fim* de uma seção a biblioteca aparece, como a coisa que o aluno agora consegue enxergar por dentro.

A lentidão e a verbosidade do código do livro são o preço da transparência, e foram pagas de propósito. **Nunca "melhore" o código do Grus** — trocar uma lista por `np.ndarray`, vetorizar um laço ou chamar `sklearn` destrói exatamente o que a disciplina existe para ensinar.

**A turma não cursou a disciplina de estatística com este professor.** Cada aluno veio de um livro e um tratamento diferentes. Então:

- Nunca referencie disciplina, ferramenta, notação ou dataset anterior específico.
- A referência é sempre genérica: *"você provavelmente já ajustou uma reta chamando uma função pronta"*.
- Pode-se assumir o **tema** (média, desvio padrão, correlação, normal), nunca o **tratamento**.

Os alunos são de **Ciência da Computação e já programam**. Não explique o que é um laço.

## Anatomia de um capítulo

```
content/capNN/
├── index.qmd          # abertura, objetivos, tabela de seções, leituras adicionais
├── 01-<slug>.qmd      # uma seção do Grus por arquivo
└── ...
```

O `index.qmd` tem, nesta ordem: título; callout `.callout-note` dizendo a que capítulo do Grus corresponde; a epígrafe do capítulo, se houver; dois ou três parágrafos de abertura que dizem **por que este capítulo existe** e o que ele entrega para os seguintes; uma lista "Ao final deste capítulo, você será capaz de" com 4 a 7 itens começando em verbo; a tabela de seções; e "Leituras adicionais" com o conteúdo real do *For Further Exploration* do Grus.

Cada seção tem: título; callout `.callout-note` citando o Grus; e o conteúdo.

## Regras que os testes verificam

Rodam em `make teste`, e quebrá-las derruba o CI:

1. **Todo `.qmd` precisa estar registrado no `_quarto.yml`.** Os arquivos e os hrefs já existem — você está preenchendo stubs, não criando arquivos novos. Não renomeie nada.
2. **Nunca invente número de seção do Grus.** O sumário dele traz só títulos. Escreva `Esta seção corresponde a *The Model*, do capítulo 12 de @grus2019.` Nunca "seção 12.1". A nossa própria numeração (`9.2`) é legítima quando aponta para este livro.
3. **Toda seção cita `@grus2019`.**
4. **Caminhos de dados a partir da raiz:** `dados/iris.data`, nunca `../dados/`. Links entre capítulos usam `../capNN/index.qmd` e são legítimos.

## Regras de código nos chunks

- **Semente explícita em todo chunk com aleatoriedade.** `random.seed(N)`, do `random` da stdlib — nunca `numpy.random`. Sem isso, cada renderização muda os números e o texto para de bater com a saída.
- **`#| label:` em todo chunk.** Seja consistente dentro do capítulo.
- **Cada `.qmd` renderiza com um kernel próprio.** Nomes definidos numa página **não existem** na outra. Se a seção 2 precisa de algo que a seção 1 definiu, importe de `scratch.<modulo>` (com um callout explicando que é o mesmo código) ou redefina.
- **Dois módulos nunca podem ser importados:** `scratch.getting_data` (tem `requests.get` no nível do módulo) e `scratch.working_with_data` (abre `stocks.csv` relativo ao cwd e afirma sobre dados sem semente). Os capítulos que precisam de funções deles escrevem essas funções inline.
- **Alguns módulos desenham no import:** `visualization.py` grava nove PNGs, `statistics.py` e `probability.py` chamam `plt.*`. Se importar, use `#| include: false` e `plt.close('all')` na sequência.
- Figuras que não são a lição vão com `#| echo: false`. Código que **é** a lição fica visível.
- Chunk que não deve executar (raspagem, download, API) leva `#| eval: false`, com um callout explicando por que ele não roda.

## Os callouts, e quando usar cada um

- `::: {.conceito}` — a ideia central, o que o aluno deve levar. Use com parcimônia.
- `::: {.exemplo}` — um caso concreto que ilumina o conceito.
- `::: {.callout-note}` — a citação do Grus, e observações laterais.
- `::: {.callout-important}` — algo que muda como o aluno deve ler o que vem a seguir.
- `::: {.callout-warning}` — armadilha, erro comum, ou resultado que engana.
- `::: {.callout-tip collapse="true"}` com título **"Na prática: ..."** — o fechamento de biblioteca. Vai no **fim** da seção, depois de o aluno ter construído a coisa.

## O callout "Na prática"

É a assinatura do livro. Ele mostra o equivalente em biblioteca do que acabou de ser construído, e explica **o que a biblioteca esconde**. Não é propaganda da ferramenta nem desculpa pelo código lento.

Quando a seção não tem análogo direto de biblioteca, use a variante **"Na prática: o que se faz com isso"** — ver `content/cap09/03-a-maldicao-da-dimensionalidade.qmd`.

O `scikit-learn` **nunca** aparece na implementação de uma seção. Só nesse callout.

## O que faz um capítulo bom aqui

- **Aponte para os outros capítulos.** O livro é uma rede, não uma lista. Diga onde a ideia reaparece e de onde ela veio.
- **Os erros do livro-texto são conteúdo.** O Grus deixa erros instrutivos de propósito (a média que não significa nada no cap. 1, o classificador que lê os cortes dos próprios dados). Marque-os com callout e explique por que enganam — é o melhor material do livro.
- **Verifique o que você afirma.** Se o texto diz "a curva dispara para fora da escala", abra o PNG renderizado e confirme. Texto que contradiz a figura já apareceu duas vezes na revisão deste livro.
- **Números no texto vêm da saída, não da sua memória.** Se você escreve "acurácia de 97,8%", rode e confira.
- **Não afirme sobre bibliotecas sem verificar.** Uma afirmação sobre o Quarto foi escrita errada três vezes seguidas neste livro antes de alguém abrir a documentação.

## Verificação antes de entregar

```bash
make render    # do projeto inteiro, nunca de subdiretório
make teste     # 21 testes, todos precisam passar
```

**Rode `make render` em primeiro plano e espere ele terminar.** Ele leva alguns minutos e imprime `render OK (tentativa N)` no fim.

O alvo é **serializado**: vários agentes escrevem este livro ao mesmo tempo, e dois `quarto render` simultâneos corrompem o `_freeze/` em silêncio. Se outro render estiver rodando, o seu imprime `aguardando a vez...` e espera. **Não interrompa nem contorne** — ele pega a vez sozinho.

Três coisas que você **não** deve fazer, e que já custaram caro:

- **Não rode o render em segundo plano esperando notificação.** Um agente que fez isso ficou preso em laço por horas, encerrando o turno repetidamente para aguardar algo que nunca o notificava.
- **Não tente contornar o erro `Directory not empty` à mão.** Ele é uma corrida do bind mount do Docker no macOS, não um erro do seu conteúdo — todas as células executaram. O alvo `make render` já limpa e repete até seis vezes sozinho.
- **Nunca use `make clean`.** Ele apaga o `_freeze/`, forçando todos os chunks a reexecutar, o que *aumenta* a chance da corrida. Medido: três falhas seguidas com cache frio, sucesso de primeira com ele quente.

Se o `make render` falhar nas seis tentativas, aí é problema de verdade: rode `docker compose run --rm --no-deps livro quarto render` direto para ver o erro real.

Depois, **abra as figuras que você gerou** (`_book/content/capNN/*_files/figure-html/*.png`) e confirme que a prosa descreve o que elas mostram.
