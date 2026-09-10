"""Toda chamada a `gradient_step` com passo não negativo precisa de motivo.

Gradiente descendente desce: o passo é negativo. Um passo positivo é uma
**subida** — maximizar em vez de minimizar — e é exatamente o tipo de detalhe
que o aluno que entendeu o capítulo 5 lê como erro de digitação. Quando um
capítulo sobe o gradiente de propósito, ele precisa dizer isso ao leitor.

Como funciona: acha toda chamada a `gradient_step(...)` nos `.qmd` e olha o
terceiro argumento. Passo começando com `-` é descida, e não interessa. O que
sobra vai para a lista de exceções abaixo, e **cada exceção precisa de motivo
escrito** — o mesmo padrão de `NAO_IMPORTAVEIS` em `test_scratch.py`, porque
uma exceção sem motivo é um esquecimento disfarçado de decisão.

Este teste nasceu para travar uma afirmação do capítulo 7 ("o único uso
ascendente do livro inteiro", em `first_principal_component`), escrita quando
metade do livro ainda era stub. Aquele capítulo saiu em 2026-09-10, com o
abandono da abordagem do Grus; o invariante sobreviveu porque vale sozinho.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONTENT = RAIZ / "content"

# Chamadas cujo terceiro argumento NÃO começa com `-`, e por quê. Nem toda
# entrada aqui é uma subida: nas duas o sinal simplesmente não está visível no
# ponto da chamada.
PASSO_NAO_NEGATIVO = {
    "cap05/03-usando-o-gradiente.qmd": (
        "É a DEFINIÇÃO de gradient_step, não uma chamada: `step_size: float` é o "
        "parâmetro. O sinal é escolhido por quem chama — e a seção diz isso."
    ),
    "cap05/04-escolhendo-o-tamanho-do-passo.qmd": (
        "O passo é parâmetro de `trajetoria_distancias`, que é chamada com -0.01 "
        "logo abaixo. Descida, com o sinal decidido no ponto da chamada."
    ),
}


def terceiro_argumento(texto: str, inicio: int) -> str | None:
    """Extrai o 3º argumento de uma chamada, respeitando parênteses e colchetes.

    Um `split(",")` ingênuo quebra em `gradient_step(guess, [grad_a, grad_b], -lr)`,
    e passa a ler `grad_b]` como terceiro argumento — falso positivo real, medido
    no capítulo de regressão linear simples, enquanto ele existia.
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
        "Se for uma SUBIDA de gradiente, a seção precisa dizer ao leitor por que "
        "sobe — sem isso ele lê o sinal como erro de digitação. Se o sinal só não "
        "está visível aqui, registre em PASSO_NAO_NEGATIVO com o motivo:\n  "
        + "\n  ".join(inesperados)
    )


def test_toda_excecao_tem_motivo_e_arquivo_real():
    for chave, motivo in PASSO_NAO_NEGATIVO.items():
        assert (CONTENT / chave).is_file(), f"{chave} não existe mais"
        assert len(motivo) > 60, f"exceção de {chave} sem motivo de verdade"
