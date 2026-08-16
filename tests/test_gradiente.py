"""Trava uma afirmação que o livro faz sobre si mesmo.

`content/cap07/08-reducao-de-dimensionalidade.qmd` diz, sobre a chamada a
`gradient_step` dentro de `first_principal_component`, que aquele é **o único
uso ascendente do livro inteiro** — passo positivo, subindo o gradiente em vez
de descer. A nota existe porque sem ela o aluno que entendeu o capítulo 5 sai
do capítulo 7 achando que entendeu errado.

O problema: quando essa nota foi escrita, os capítulos 13 a 17 eram stubs. A
afirmação era uma **aposta sobre texto que ainda não existia** — e uma revisão
do livro inteiro apontou exatamente isso, dizendo, com razão, que não conseguia
confirmá-la. Este teste transforma a aposta em invariante: se um capítulo novo
subir um gradiente, ele falha, e aí ou a nota do capítulo 7 muda ou o capítulo
novo ganha a sua própria.

Como funciona: acha toda chamada a `gradient_step(...)` nos `.qmd` e olha o
terceiro argumento. Passo começando com `-` é descida, e não interessa. O que
sobra vai para a lista de exceções abaixo, e **cada exceção precisa de motivo
escrito** — o mesmo padrão de `NAO_IMPORTAVEIS` em `test_scratch.py`, porque
uma exceção sem motivo é um esquecimento disfarçado de decisão.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONTENT = RAIZ / "content"

# Chamadas cujo terceiro argumento NÃO começa com `-`, e por quê. Nem toda
# entrada aqui é uma subida: nas duas primeiras o sinal simplesmente não está
# visível no ponto da chamada.
PASSO_NAO_NEGATIVO = {
    "cap05/03-usando-o-gradiente.qmd": (
        "É a DEFINIÇÃO de gradient_step, não uma chamada: `step_size: float` é o "
        "parâmetro. O sinal é escolhido por quem chama — e a seção diz isso."
    ),
    "cap05/04-escolhendo-o-tamanho-do-passo.qmd": (
        "O passo é parâmetro de `trajetoria_distancias`, que é chamada com -0.01 "
        "logo abaixo. Descida, com o sinal decidido no ponto da chamada."
    ),
    "cap07/08-reducao-de-dimensionalidade.qmd": (
        "A ÚNICA subida de gradiente do livro: `first_principal_component` maximiza "
        "a variância na direção do palpite, então anda A FAVOR do gradiente. A nota "
        "no próprio arquivo explica isso, e é esta entrada que ela descreve."
    ),
}


def terceiro_argumento(texto: str, inicio: int) -> str | None:
    """Extrai o 3º argumento de uma chamada, respeitando parênteses e colchetes.

    Um `split(",")` ingênuo quebra em `gradient_step(guess, [grad_a, grad_b], -lr)`,
    e passa a ler `grad_b]` como terceiro argumento — falso positivo real, visto
    no capítulo 11.
    """
    profundidade, atual, args = 0, [], []
    for ch in texto[inicio:]:
        if ch in "([{":
            profundidade += 1
        elif ch in ")]}":
            if profundidade == 0:
                args.append("".join(atual).strip())
                break
            profundidade -= 1
        elif ch == "," and profundidade == 0:
            args.append("".join(atual).strip())
            atual = []
            continue
        atual.append(ch)
    return args[2] if len(args) >= 3 else None


def test_toda_subida_de_gradiente_tem_motivo_registrado():
    inesperados = []
    for p in sorted(CONTENT.rglob("*.qmd")):
        texto = p.read_text(encoding="utf-8")
        chave = f"{p.parent.name}/{p.name}"
        for m in re.finditer(r"gradient_step\s*\(", texto):
            arg = terceiro_argumento(texto, m.end())
            if arg is None or arg.startswith("-"):
                continue  # descida, ou chamada que não conseguimos ler
            if chave in PASSO_NAO_NEGATIVO:
                continue
            linha = texto[: m.start()].count("\n") + 1
            inesperados.append(f"{chave}:{linha} (passo = {arg!r})")

    assert not inesperados, (
        "chamada a gradient_step com passo não negativo fora das registradas.\n"
        "Se for uma SUBIDA de gradiente, o capítulo 7 afirma ser o único uso "
        "ascendente do livro — ou essa afirmação muda, ou este capítulo ganha a "
        "própria nota explicando por que sobe. Se o sinal só não está visível "
        "aqui, registre em PASSO_NAO_NEGATIVO com o motivo:\n  "
        + "\n  ".join(inesperados)
    )


def test_toda_excecao_tem_motivo_e_arquivo_real():
    for chave, motivo in PASSO_NAO_NEGATIVO.items():
        assert (CONTENT / chave).is_file(), f"{chave} não existe mais"
        assert len(motivo) > 60, f"exceção de {chave} sem motivo de verdade"
