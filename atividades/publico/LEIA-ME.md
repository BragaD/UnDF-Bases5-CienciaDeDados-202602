# atividades/publico/

**Tudo neste diretório vai para o site publicado.** Ele é copiado para `_book/`
pelo `project.resources` do `_quarto.yml` e fica acessível a qualquer pessoa na
internet, sem autenticação.

Consequência direta: **nunca coloque gabarito, prova não aplicada ou qualquer
coisa que o aluno não deva ver antes da hora aqui dentro.** O
`make atividade` grava a versão do aluno aqui e o gabarito fora, de propósito.

Há um teste que trava isso — `test_atividades.py` falha se aparecer um arquivo
com "gabarito" no nome, e também se algum PDF daqui contiver a palavra
"Resposta." no corpo, que é como as respostas são marcadas na fonte.
