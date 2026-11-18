"""Monta o que vai para o AVA a partir dos JSON de correção de uma lista.

Uso (da raiz do repositório):

    .venv/bin/python -I .claude/skills/corrigir-listas/montar_payload.py lista3 ids.json

`ids.json` mapeia o NOME COMPLETO do aluno (como no JSON) para o userid do Moodle
(vem da tabela de avaliação; ver SKILL.md). Imprime um array JSON
[{"u": userid, "g": nota, "h": feedback em HTML}], pronto para colar em lancar-ava.js.
Recusa-se a montar se a nota de algum aluno não fechar com a soma dos descontos.
"""
import glob
import html
import json
import sys


def para_html(texto: str) -> str:
    saida = []
    for bloco in texto.strip().split("\n\n"):
        linhas, itens = [], []
        for linha in bloco.split("\n"):
            if linha.startswith("- "):
                itens.append("<li>" + html.escape(linha[2:], quote=False) + "</li>")
            else:
                linhas.append(html.escape(linha, quote=False))
        if linhas:
            saida.append("<p>" + "<br>".join(linhas) + "</p>")
        if itens:
            saida.append("<ul>" + "".join(itens) + "</ul>")
    return "".join(saida)


def main() -> None:
    lista, arquivo_ids = sys.argv[1], sys.argv[2]
    ids = json.load(open(arquivo_ids))
    payload = []
    for caminho in sorted(glob.glob(f"atividades/entregas/correcao/{lista}/*.json")):
        d = json.load(open(caminho))
        soma = sum(x["pontos"] for x in d["descontos"])
        assert abs((100 - soma) - d["nota"]) <= 0.5, f"nota não fecha com os descontos: {caminho}"
        assert d.get("feedback_ava", "").strip(), f"sem feedback_ava: {caminho}"
        payload.append({"u": ids[d["aluno"]], "g": d["nota"], "h": para_html(d["feedback_ava"])})
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
