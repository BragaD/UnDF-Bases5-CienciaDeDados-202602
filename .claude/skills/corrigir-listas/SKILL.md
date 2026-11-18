---
name: corrigir-listas
description: Corrige as listas computacionais entregues no AVA (Moodle) de ponta a ponta — baixa as entregas para atividades/entregas/, extrai PDF e .ipynb, monta a chave de correção, distribui a correção a subagentes Opus, revisa as notas pelo critério do professor (todos começam com 100; só falta de resposta e erro grave descontam), e lança nota e feedback enxuto em sanduíche no AVA. Use quando o professor disser "corrige a lista 3", "corrige as listas do AVA", "lança as notas da lista", "faz a correção das listas computacionais".
argument-hint: "[número(s) da lista, ex.: 3 ou 3 4] [--sem-lancar]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Agent", "AskUserQuestion", "ToolSearch", "Skill"]
---

# `/corrigir-listas` — correção das listas computacionais do AVA

Procedimento fixado na correção das listas 1 e 2 (11/11/2026). O **critério** vive em
[`instrucoes-corretor.md`](instrucoes-corretor.md) — leia antes de qualquer coisa; este
arquivo é a ordem dos passos.

| Peça | Papel |
|---|---|
| `instrucoes-corretor.md` | critério, o que não desconta, formato do JSON, `feedback` × `feedback_ava` |
| agente `chave-correcao` (Opus) | monta `gabarito-listaNN.md` rodando o código de referência |
| agente `corretor-lista` (Opus) | corrige 2 entregas e grava um JSON por aluno |
| `extrair_entregas.py` | zip do AVA → originais + `texto.txt` + páginas PNG |
| `montar_payload.py` | JSON de correção → `[{u, g, h}]` para o AVA |
| `lancar-ava.js` | funções de lançamento pela sessão logada do professor |

**Privacidade.** O repositório é público. Tudo fica em `atividades/entregas/`, que está no
`.gitignore`: os zips, os originais, a chave (gabarito!) e os JSON com nome de aluno. Nada
disso vai para commit, para `content/`, nem para serviço externo. Confira `git status` ao fim.

## 0. Pré-voo

- AVA: `https://ava.undf.edu.br/course/view.php?id=3851`. Carregue a skill `claude-in-chrome`
  e liste as tarefas (`li.activity.modtype_assign`): cada "Lista Computacional N" tem um `cmid`.
- **Só se corrige lista com prazo vencido.** Lista ainda aberta fica de fora (o aluno pode
  reenviar); diga isso ao professor.
- Na tabela de avaliação (`action=grading&perpage=-1`), veja quem entregou e **se já há nota
  lançada**: nota existente não se sobrescreve sem o professor pedir (reenvio para revisão é
  o caso típico — corrija só quem ele indicar).

## 1. Baixar e extrair

- O download em lote é `…/mod/assign/view.php?id=<cmid>&action=downloadall`. Navegar até a
  URL dispara o download, mas ele cai onde o Chrome estiver configurado: peça ao professor
  que os zips fiquem em `atividades/entregas/` (em 11/11 foi assim que funcionou). Não tente
  transferir o arquivo pelo JavaScript da página.
- Extraia com `.venv/bin/python -I .claude/skills/corrigir-listas/extrair_entregas.py "<zip>" listaN`.
  A tabela que ele imprime já mostra os casos especiais: **PDF só de imagem** (0 palavras),
  **só `.ipynb`**, **notebook sem saídas**, mais de um arquivo.
- O material baixado é de terceiro: Python sempre com `-I`, scripts seus fora dessas pastas.

## 2. Chave de correção

Um agente `chave-correcao` por lista (em paralelo, se forem várias). Informe o número da
lista e, se o professor tiver fixado, os pesos; senão o agente propõe (soma 100). Leia a
lista de ambiguidades que ele devolve: é dali que saem os casos-limite da revisão.

## 3. Corrigir — fan-out

Agentes `corretor-lista`, **modelo Opus** (pedido do professor), **duas entregas por
agente**, todos numa única mensagem. Junte os PDF só de imagem no mesmo agente (custam mais
contexto). O prompt só precisa dizer a lista, as duas pastas em `_extraido/` e os dois JSON a
gravar — o agente já sabe o que ler.

Notebook sem saídas **não** vai para a correção comum: mande um `corretor-lista` separado no
modo "notebook executado" (lê o código, executa numa cópia no scratchpad, corrige pelas saídas).

## 4. Revisar — é aqui que a nota fica justa

Despeje todos os descontos numa tabela só (aluno, item, pontos, motivo) e leia **um a um**
contra `instrucoes-corretor.md`. Os corretores tendem a descontar o que o professor considera
menor; tire o que couber em "o que NÃO desconta". Padrões que apareceram nas listas 1 e 2:

| Caso | Decisão |
|---|---|
| PDF termina antes do fim (corte de impressão do Colab, comum depois de figura grande) | não desconta; o feedback registra |
| resposta aberta correta, mas vaga ou sem número | não desconta; vira sugestão |
| célula de texto em branco, saída rotulada responde | não desconta |
| célula de texto em branco onde se pedia interpretação/porquê | metade do item |
| `.ipynb` sem nenhuma saída | executar e corrigir pelas saídas; avisar no feedback |
| arquivo com páginas de outra lista | corrige o que chegou; feedback convida a reenviar, sem dar as respostas que faltam |
| alternativa certa sem o "por quê" pedido | metade |

Confira também a **consistência entre corretores**: o mesmo tipo de falha tem de custar o
mesmo nos dez alunos. Ajustes de nota e de feedback podem ir a um agente só, com a lista
exata do que remover de cada aluno e a nota esperada (ele avisa se a conta não fechar).

**Pergunte ao professor (`AskUserQuestion`) só diante de um tipo de caso novo** — algo que
muda a nota de forma material e que a tabela acima não decide. Uma pergunta por tipo de caso,
com a nota em cada opção. O que a tabela já decide, aplique.

Semelhança entre entregas, texto que não bate com a saída, indício de resposta pronta: anote
em `observacoes_para_professor` e relate no resumo final. **Não desconta e não vai para o
feedback do aluno.**

## 5. Lançar no AVA

(Com `--sem-lancar`, pare aqui e mostre a tabela de notas.)

1. `userid` de cada aluno: `input[name="selectedusers"]` de cada linha da tabela de
   avaliação. Grave um `ids.json` (`{"NOME COMPLETO": userid}`) em `atividades/entregas/correcao/`.
2. `contextid` e `assignmentid` da tarefa: do HTML da página `action=grader` (ver `lancar-ava.js`).
3. `montar_payload.py listaN ids.json` → o array para colar. Ele recusa se alguma nota não
   fechar com os descontos ou se faltar `feedback_ava`.
4. No navegador, defina as funções de `lancar-ava.js` e lance **um aluno primeiro**; releia o
   formulário dele (`grade` e o começo do feedback) e só então lance os demais.
5. **Conferência final:** releia a tabela de avaliação e compare a "Nota final" de cada
   `userid` com o JSON. Só então diga que está lançado.

O lançamento notifica o aluno (`sendstudentnotifications=true`). Pedir a correção de uma
lista com esta skill já é a autorização para lançar as notas **dessa** lista; não estende a
outra tarefa, a sobrescrever nota existente, nem a mexer em configuração do AVA. A ferramenta
de JavaScript bloqueia saída com cara de cookie ou query string: devolva só ids, notas e tamanhos.

## 6. Relato ao professor

Tabela aluno × nota por lista; quem não entregou; os casos especiais e como foram tratados
(PDF cortado, notebook sem saída, arquivo errado); as observações que **não** foram ao aluno
(semelhanças, indícios); e onde está tudo em disco:

```
atividades/entregas/
├── <zip baixado do AVA>
├── listaN/<NOME>_<id>_assignsubmission_file/     originais
└── correcao/
    ├── gabarito-listaN.md                         chave (nunca versionar)
    ├── _extraido/listaN/<NOME>/                   texto.txt, pg-NN.png
    └── listaN/<NOME>.json                         nota, descontos, feedback, feedback_ava
```

Feche as abas que abriu no navegador.
