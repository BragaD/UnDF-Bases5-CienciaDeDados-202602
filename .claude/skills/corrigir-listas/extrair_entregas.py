"""Extrai o zip de entregas baixado do AVA e prepara o material para os corretores.

Uso (da raiz do repositório, com o Python do projeto e -I, porque lê arquivo de terceiro):

    .venv/bin/python -I .claude/skills/corrigir-listas/extrair_entregas.py \
        "atividades/entregas/<arquivo baixado>.zip" lista3

Produz, dentro de atividades/entregas/ (gitignorado):
    lista3/<NOME>_<id>_assignsubmission_file/...      os arquivos originais
    correcao/_extraido/lista3/<NOME>/texto.txt         texto do PDF, ou despejo do .ipynb
    correcao/_extraido/lista3/<NOME>/pg-NN.png         páginas do PDF a 70 dpi
    correcao/lista3/                                   onde os corretores gravam os JSON

Depende de `ditto` (macOS; o `unzip` quebra nos nomes acentuados do Moodle),
`pdftotext` e `pdftoppm` (poppler).
"""
import json
import pathlib
import re
import subprocess
import sys


def despejar_notebook(caminho: pathlib.Path) -> tuple[str, int, int]:
    nb = json.loads(caminho.read_text())
    partes, celulas_codigo, sem_saida = [], 0, 0
    for i, celula in enumerate(nb["cells"]):
        partes.append(f"\n===== CÉLULA {i} [{celula['cell_type']}] =====\n" + "".join(celula["source"]))
        if celula["cell_type"] != "code":
            continue
        celulas_codigo += 1
        saidas = celula.get("outputs", [])
        if not saidas:
            sem_saida += 1
            partes.append("--- (sem saída) ---")
        for saida in saidas:
            tipo = saida.get("output_type")
            if tipo == "stream":
                partes.append("--- saída ---\n" + "".join(saida["text"])[:6000])
            elif tipo == "error":
                partes.append(f"--- ERRO --- {saida.get('ename')}: {saida.get('evalue', '')[:500]}")
            else:
                dados = saida.get("data", {})
                if "text/plain" in dados:
                    partes.append("--- saída ---\n" + "".join(dados["text/plain"])[:6000])
                if "image/png" in dados:
                    partes.append("--- [FIGURA PNG na saída] ---")
    return "\n".join(partes), celulas_codigo, sem_saida


def main() -> None:
    arquivo_zip, lista = pathlib.Path(sys.argv[1]), sys.argv[2]
    base = pathlib.Path("atividades/entregas")
    originais = base / lista
    extraido = base / "correcao" / "_extraido" / lista
    (base / "correcao" / lista).mkdir(parents=True, exist_ok=True)
    originais.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ditto", "-x", "-k", str(arquivo_zip), str(originais)], check=True)

    print(f"{'aluno':45} {'págs':>4} {'palavras':>8}  observação")
    for pasta in sorted(p for p in originais.iterdir() if p.is_dir()):
        nome = re.sub(r"_\d+_assignsubmission_file$", "", pasta.name)
        destino = extraido / nome
        destino.mkdir(parents=True, exist_ok=True)
        paginas, palavras, obs = 0, 0, []
        pdfs = sorted(pasta.glob("*.pdf"))
        notebooks = sorted(pasta.glob("*.ipynb"))
        if len(pdfs) > 1:
            obs.append(f"{len(pdfs)} PDFs: só o primeiro foi extraído")
        for pdf in pdfs[:1]:
            subprocess.run(["pdftotext", "-layout", str(pdf), str(destino / "texto.txt")], stderr=subprocess.DEVNULL)
            subprocess.run(["pdftoppm", "-r", "70", "-png", str(pdf), str(destino / "pg")], stderr=subprocess.DEVNULL)
            paginas = len(list(destino.glob("pg-*.png")))
            palavras = len((destino / "texto.txt").read_text(errors="replace").split())
            if palavras == 0:
                obs.append("PDF só de imagem: ler as páginas")
        for nb in notebooks:
            (destino / nb.name).write_bytes(nb.read_bytes())
            if not pdfs:
                texto, n_codigo, n_sem = despejar_notebook(nb)
                (destino / "texto.txt").write_text(texto)
                palavras = len(texto.split())
                obs.append(f"só .ipynb ({n_sem}/{n_codigo} células de código sem saída)")
        if not pdfs and not notebooks:
            obs.append("nenhum PDF nem .ipynb: olhar a pasta original")
        print(f"{nome[:45]:45} {paginas:>4} {palavras:>8}  {'; '.join(obs)}")


if __name__ == "__main__":
    main()
