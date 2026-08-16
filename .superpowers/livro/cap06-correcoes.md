# Capítulo 6 — apontamentos consolidados das duas revisões

**Revisão de conteúdo técnico: 0 Crítico, 0 Importante.** As três restrições duras
(nenhum import de `getting_data`, nenhum chunk na rede, a seção do Twitter não promete
funcionar) foram auditadas e aprovadas. Fidelidade ao PDF conferida seção a seção; números
do texto batem com o HTML renderizado. **O capítulo está tecnicamente sólido** — o trabalho
abaixo é quase todo de didática.

**Revisão didática: 2 Críticos, 9 Importantes, ~8 de prosa.**

Corrija tudo. Se discordar de algum item, não o ignore em silêncio: implemente o resto e
diga no relatório qual recusou e por quê.

**NÃO rode `make render` nesta rodada** — outro subagente está escrevendo o capítulo 7 e
pode renderizar ao mesmo tempo. Faça as edições; eu renderizo depois, consolidado.

---

## CRÍTICOS

### C1 — `04-usando-apis.qmd:60-94` — a seção tinha o movimento salvador disponível e não o usou

Este é o achado mais importante da revisão, e ele é sobre o que o capítulo faz de melhor
em outras seções.

A tensão central do capítulo é que ele ensina a buscar dados de fora e **nenhum chunk pode
acessar a rede**. As seções 1 e 3 resolvem isso brilhantemente: a §1 diz que a razão não é
rede (é `argv`/`stdin`) e reescreve a lógica como função sobre um iterável qualquer — o
script que não roda vira código que roda. A §3 faz o mesmo com o HTML vendorizado: nove
chunks executam, um não.

**A §4 tinha exatamente o mesmo movimento à mão e não o fez.** Todo o código depois do
`requests.get` — `parse(repo["created_at"])`, o `Counter(date.month ...)`, o `sorted` por
`pushed_at` — é Python puro sobre uma lista de `dict`s. Ele rodaria perfeitamente contra um
`repos` literal de três dicionários escritos à mão.

Pior: o callout da linha 101 **afirma o payoff sem demonstrá-lo** — "o resultado é um `dict`
Python normal, o mesmo tipo de dado que você manipulou o livro inteiro". O aluno sai da §4
tendo lido *sobre* interpretar datas de API e nunca tendo visto uma ser interpretada.
`dateutil.parser.parse` aparece só dentro de um comentário, dentro de um chunk morto.

**Divida o chunk em dois:** `requests.get` + `json.loads` com `eval: false` (é rede, tem que
ficar), e a análise com um `repos` literal, **executando**. Aí o callout passa a dizer a
verdade sobre algo que o aluno acabou de ver.

### C2 — o capítulo nunca manda o aluno rodar nada fora do livro

Este é o capítulo mais prático do material e o único **inteiramente passivo**.

O `index.qmd` lista como objetivo "encadear programas Python pela linha de comando", e o
único jeito de cumprir isso é o aluno salvar os scripts e rodar o pipe no terminal dele.
Falta uma frase imperativa na §1, mais ou menos assim:

> Salve os dois scripts num diretório e rode `cat egrep.py | python egrep.py 'sys' | python
> line_count.py`. Este é o único trecho do capítulo que você precisa executar fora da
> página, e leva trinta segundos.

---

## IMPORTANTES

### I1 — quatro callouts dizendo "isto não roda", dois com título idêntico

`01:43`, `03:224`, `04:96`, `05:07` — e dois deles se chamam "Por que este chunk não roda".
O aparato da limitação virou decoração por repetição: se tudo é destacado, nada é.

**Estabeleça a política uma única vez no `index.qmd`** — que hoje não menciona a restrição
em lugar nenhum, embora ela governe como se lê cada página do capítulo. Depois reduza cada
caixa à razão **específica** daquela seção: §1 é `argv`/`stdin`, não rede; §3 são centenas
de requisições encadeadas; §4 é resposta que muda a cada chamada; §5 é serviço que não
existe mais.

### I2 — o único `.conceito` do capítulo está no lugar errado

Ele está em `02:56`, sobre o `with`. Gerenciador de contexto não é a ideia central de um
capítulo sobre obter dados — é sintaxe que o capítulo 2 já cobriu e que um aluno de quinto
período conhece.

A ideia central do capítulo **não tem `.conceito` nenhum**. Ela é algo como: *toda fonte
externa é um contrato que você não controla, e o custo de obtê-la é proporcional a quanto
controle você perdeu.* Mova o `.conceito` para lá.

### I3 — a espinha da sequência existe e nunca é dita

As cinco seções estão em ordem crescente de fragilidade: **seu próprio pipe → seu próprio
disco → o HTML de outro → o contrato de outro → a permissão de outro.** Isso é um arco, e
é bom.

Mas o `index.qmd:13` chama as seções de "portas de entrada… cada uma com sua mecânica", que
é explicitamente uma *lista*. Nomeie o arco. Isso faz a §5 virar o destino natural do
capítulo em vez de um apêndice.

O tecido conectivo local já existe e é bom (`02:80`, `04:54`, `04:114`, `04:128`); só a
junta §2→§3 é fraca ("Além de ler e escrever pelo terminal…", `02:07`).

### I4 — o capítulo termina dentro de uma caixa recolhida

A última coisa visível é um `.callout-tip collapse="true"`. Não há "Adiante" — o
`content/cap01/03-...qmd` tem, e funciona. E a entrega prometida no `index.qmd:15` ("este
capítulo garante que o dado chegou até ali") nunca é feita na última seção.

Feche a §5 com dois parágrafos: o dado agora está na memória como listas e `dict`s, e o
[Capítulo 7](../cap07/index.qmd) assume daqui.

### I5 — arquivo interno vazando para a prosa do aluno

`03:29` manda o leitor ver "`make offline` no `CLAUDE.md` do repositório". É o **único**
lugar em todo o `content/` que cita o `CLAUDE.md` — que é documentação para quem escreve o
livro, não para quem o lê. Troque por algo como "este livro é renderizado com a rede
desligada, de propósito".

`03:117` cita "`scratch/getting_data.py`, linhas 82 a 134". Número de linha envelhece.
Cite o arquivo sem as linhas.

### I6 — a mesma explicação duas vezes na §3

`03:29` (prosa) e `03:117` (callout) dizem ambos "trocamos `requests.get` por `open()`, o
resto é idêntico". Corte o callout.

E `03:232` empilha dois assuntos alheios num `.callout-note` sem título: etiqueta de
`robots.txt` e paginação dos comunicados. Separe, ou passe a paginação para prosa.

### I7 — é onde o capítulo mais se aproxima de tutorial de biblioteca, e falta a frase que o salvaria

`03:44-112` são **nove chunks consecutivos, um por método do `bs4`**. É o risco que este
capítulo corre por natureza — ele não tem matemática nem algoritmo, e pode virar manual de
ferramenta, que é o oposto da identidade da disciplina.

O antídoto está à mão e não foi usado: `html5lib` é descrito apenas como "não muito
tolerante" (`03:27`). Escreva um parágrafo dizendo **o que é análise tolerante** — que
navegadores recuperam de marcação quebrada seguindo um algoritmo especificado, e que o
`html5lib` implementa exatamente esse algoritmo enquanto o parser embutido desiste.

Isso abre a caixa-preta da própria ferramenta do capítulo, e faz os nove chunks lerem como
"acessores da árvore" em vez de como a lição.

### I8 — referências cruzadas concentradas e incompletas

Todos os cinco links a outros capítulos estão nas §1 e §2, e todos apontam para o capítulo
2. As §3, §4 e §5 não têm nenhum.

Duas faltam e são baratas:
- A §2 deveria apontar para onde aquele `csv.reader` reaparece de verdade:
  `content/cap09/02-exemplo-o-dataset-iris.qmd` lê `dados/iris.data` exatamente assim.
- O capítulo deveria retribuir a `content/cap08/06-extracao-e-selecao-de-atributos.qmd:36`,
  que já aponta para cá.

O par que **já funciona** e deve servir de modelo: `cap02/02:136` promete "você vai ver esse
padrão no Capítulo 6, quando linhas malformadas…" e o `02:144` daqui cumpre.

### I9 — a moldura DataSciencester só aparece na §3

O `index.qmd` abre invocando o capítulo 1, e depois só o VP de Políticas Públicas (`03:122`)
mantém a ficção. Uma linha de enquadramento na §2 ou na §4 — um pedido do VP de Receita por
um CSV de outro time — custa nada e costura o capítulo ao livro.

---

## A seção 5 (Twitter): a decisão está certa, a encenação está errada

Manter como estudo de caso histórico é defensável e rende a melhor frase do capítulo — *"uma
dependência externa que morre é o destino normal de todo código que depende de terceiros"* —
que inclusive já está prometida nos objetivos do `index.qmd`.

O problema é a montagem. Hoje a seção **abre** com ~250 palavras de justificativa antes de o
aluno saber do que ela trata, e **fecha** com um "Na prática" que reargumenta a mesma tese.
Ler as duas caixas seguidas é ler o mesmo argumento duas vezes — e é isso que produz a
sensação de meia seção pedindo desculpas.

**Corte a caixa de abertura para três frases. Abra pelo conteúdo** (dado social vive atrás de
API; a parte difícil é autenticar). Deixe o argumento histórico inteiro para o fechamento,
onde ele já está bem escrito.

O revisor registrou que não vê escolha melhor: reancorar numa API viva compraria execução ao
preço de datar de novo em dois anos — que é exatamente o que a seção ensina a não fazer.

---

## MENORES — prosa, com a redação proposta

- `01:46` "Rodar isso dentro de uma célula do Quarto não tem argumento de linha de comando
  para ler" (sujeito quebrado) → *"Uma célula do Quarto não recebe argumentos de linha de
  comando, e ler de `sys.stdin` sem que nada o alimente trava o render esperando uma entrada
  que nunca chega."*
- `03:07` "Buscar uma página, isso é fácil" (calque de *"Getting a page, that's easy"*) →
  *"Buscar a página é a parte fácil; extrair dela informação estruturada e com sentido, bem
  menos."*
- `04:58` "Não é capricho dos provedores — mas isso adiciona um bocado de boilerplate" →
  *"Não é capricho dos provedores, mas cobra um bom tanto de código repetitivo que atrapalha
  a exposição do que interessa."*
- `05:12` "Nada de código nesta seção é `{python}` executável" (calque, e `{python}` é jargão
  de casa) → *"Nenhum código desta seção é executado; tudo aparece como ilustração."*
- `04:119` "embrulha por baixo dos panos" → *"encapsula"*.
- `04:112` Real Python é um site de tutoriais, não uma "comunidade". E a subseção "Encontrando
  APIs" (`04:108-114`) é a única passagem que subestima o leitor — "procure a seção de
  desenvolvedores do site" não informa um aluno de quinto período. Reduza a duas frases.
- **Sobra de explicação**, contra a regra do guia: `01:41` glosa entre parênteses o que é um
  pipe, e o `.conceito` de `02:56` explica que `f` fica fechado depois do `with`. O leitor
  sabe as duas coisas.
- `02:12` "não fazem parte do inventário de dados do livro, então não vão para `dados/`" é
  nota de manutenção do repositório, não de aula → *"são inventados para ilustrar, e criamos
  e apagamos todos num diretório temporário"*.

---

## Menores da revisão de conteúdo

- `03:124` — a prosa não repete a observação do Grus de que "existem apenas 435 deputados",
  que é o contexto de por que 862 links ainda são "demais". Omissão inócua; acrescente se
  couber.
- `04:11` — "Como HTTP é um protocolo para transferir *texto*" é simplificação (HTTP
  transporta bytes arbitrários), **herdada verbatim do Grus**. Não é erro introduzido aqui.
  Vale uma nota de rodapé, ou deixe como está.

---

## NÃO MEXA NISTO

Os dois revisores destacaram:

- **Os cinco "Na prática"** cumprem o papel no caso peculiar deste capítulo: como `requests`
  e `bs4` já aparecem no corpo, os callouts deixaram de ser "eis a biblioteca" e viraram "eis
  o que a biblioteca ainda **não** resolve" — Selenium/Playwright para JS, Scrapy para
  escala, paginação e limite de taxa, e a heurística de inferência de tipos do `pandas` que
  come zeros à esquerda (apontado como o melhor dos cinco).
- **Os objetivos de aprendizagem do `index.qmd`**, escritos honestamente em torno da restrição
  ("reconhecer os limites dessa técnica", "explicar por que código de terceiros para de
  funcionar") em vez de prometerem execução que o capítulo não entrega.
- **A abertura do `index.qmd`**, que cobra a dívida deixada em `cap01`, chamada de a melhor
  página do capítulo.
- **A §1 e a §3**, que transformam a limitação em lição — são o modelo do que a §4 precisa
  virar.
