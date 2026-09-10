"""Os algoritmos do livro em numpy — a contraparte em arrays do pacote `scratch/`.

`scratch/` é a cópia literal do código do Grus, em Python puro, e é o que os
capítulos 1 a 5 usam. A partir do capítulo 6 os vetores são `np.ndarray`, e o
código que cada seção escreve mora aqui, módulo a módulo, com os mesmos nomes
de função do Grus sempre que a função existe nos dois lados.

Este pacote é NOSSO: editável, testado em `tests/test_scratch_np.py`, sem hash
travado. A única coisa que ele importa de `scratch/` são DADOS (as listas
hard-coded do Grus), nunca funções — ver `statistics.py`.

Regra que decide cada dúvida: numpy é a calculadora, não o modelo. Álgebra
linear, broadcasting, reduções, máscaras e sorteio vêm do numpy; a regra de
atualização, o critério de partição, a votação, a verossimilhança — o algoritmo
em si — continua escrito aqui, linha a linha.
(docs/superpowers/specs/2026-09-06-reescrita-numpy-design.md)
"""
