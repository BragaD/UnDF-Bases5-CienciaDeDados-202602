"""Desenhos em SVG para os slides de redes neurais.

Cada função devolve nada e IMPRIME um bloco ```{=html} com um <svg class="des">;
o chunk que a chama usa `#| output: asis` e `#| echo: false`. As cores vêm de
`tema.scss` (classes .no, .ar, .q ...), para o deck inteiro obedecer à mesma
regra de leitura: azul é a ida, laranja é a volta.

Um elemento com `frag=k` vira `class="fragment" data-fragment-index="k"`:
aparece no k-ésimo clique.
"""

import math
from itertools import count

_ids = count()


def _frag(k):
    if k is None:
        return ""
    return f' class="fragment" data-fragment-index="{k}"'


def _g(conteudo, k=None):
    return f"<g{_frag(k)}>{conteudo}</g>"


def _seta(x1, y1, x2, y2, classe="", ponta=True, folga_ini=0, folga_fim=0):
    """Linha de (x1,y1) a (x2,y2), encurtada pelas folgas, com ponta triangular."""
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy) or 1
    ux, uy = dx / d, dy / d
    ax, ay = x1 + ux * folga_ini, y1 + uy * folga_ini
    bx, by = x2 - ux * folga_fim, y2 - uy * folga_fim
    s = ""
    if ponta:
        t = 13
        px, py = bx - ux * t, by - uy * t
        nx, ny = -uy * t * 0.45, ux * t * 0.45
        s += (
            f'<polygon class="ponta {classe}" points="{bx:.1f},{by:.1f} '
            f'{px + nx:.1f},{py + ny:.1f} {px - nx:.1f},{py - ny:.1f}"/>'
        )
        bx, by = px, py
    return f'<line class="ar {classe}" x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}"/>' + s


def _texto(x, y, t, classe=""):
    return f'<text class="{classe}" x="{x:.1f}" y="{y:.1f}">{t}</text>'


def _svg(largura, altura, corpo, escala=1.0):
    w = int(largura * escala)
    print(
        "```{=html}\n"
        f'<svg class="des" viewBox="0 0 {largura} {altura}" width="{w}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img">{corpo}</svg>\n'
        "```"
    )


# --------------------------------------------------------------------------
# Um neurônio, peça por peça
# --------------------------------------------------------------------------
def neuronio(
    xs=("x₁", "x₂", "x₃"),
    ws=("w₁", "w₂", "w₃"),
    b="b",
    soma="Σ",
    z="z",
    ativ="g",
    saida="ŷ",
    legendas=True,
    frag=False,
    quente=(),
    escala=1.0,
):
    """Entradas → pesos → soma (+ viés) → ativação → saída.

    `frag=True` revela as peças em seis cliques. `quente` é um conjunto com os
    nomes das peças a pintar de laranja: "entradas", "pesos", "vies", "soma",
    "ativ", "saida".
    """
    L, A = 1160, 430
    n = len(xs)
    xe, xs_, xa, xo = 110, 520, 770, 1010
    cy = 215
    passo = 110 if n <= 3 else 300 / (n - 1)
    ys = [cy + (i - (n - 1) / 2) * passo for i in range(n)]
    q = lambda nome: " q" if nome in quente else ""
    k = (lambda i: i) if frag else (lambda i: None)

    ent = "".join(
        f'<circle class="no ent{q("entradas")}" cx="{xe}" cy="{y}" r="34"/>' + _texto(xe, y, t, "dentro")
        for y, t in zip(ys, xs)
    )
    pes = ""
    for y, t in zip(ys, ws):
        pes += _seta(xe, y, xs_, cy, "forte" + q("pesos"), folga_ini=34, folga_fim=62)
        px, py = xe + 0.48 * (xs_ - xe), y + 0.48 * (cy - y) - 22
        pes += _texto(px, py, t, "peso" + q("pesos"))
    vies = _seta(xs_, 52, xs_, cy, "forte" + q("vies"), folga_ini=18, folga_fim=62) + _texto(
        xs_, 30, b, "peso" + q("vies")
    )
    som = f'<circle class="no{q("soma")}" cx="{xs_}" cy="{cy}" r="58"/>' + _texto(xs_, cy, soma, "grande")
    som += _seta(xs_, cy, xa, cy, "forte", folga_ini=58, folga_fim=58) + _texto(
        (xs_ + xa) / 2, cy - 22, z, "ida"
    )
    atv = (
        f'<rect class="cx{q("ativ")}" x="{xa - 54}" y="{cy - 54}" width="108" height="108" rx="14"/>'
        + _texto(xa, cy, ativ, "grande")
    )
    sai = _seta(xa, cy, xo, cy, "forte", folga_ini=54, folga_fim=40) + (
        f'<circle class="no sai{q("saida")}" cx="{xo}" cy="{cy}" r="38"/>' + _texto(xo, cy, saida, "dentro")
    )
    if legendas:
        yl = A - 22
        ent += _texto(xe, yl, "entradas", "leg")
        pes += _texto((xe + xs_) / 2 - 20, yl, "pesos", "leg")
        vies += _texto(xs_ + 62, 30, "viés", "leg esq")
        som += _texto(xs_, yl, "soma ponderada", "leg")
        atv += _texto(xa, yl, "ativação", "leg")
        sai += _texto(xo, yl, "saída", "leg")
    corpo = _g(ent, k(0)) + _g(pes, k(1)) + _g(vies, k(2)) + _g(som, k(3)) + _g(atv, k(4)) + _g(sai, k(5))
    _svg(L, A, corpo, escala)


# --------------------------------------------------------------------------
# Uma rede em camadas
# --------------------------------------------------------------------------
def rede(
    camadas,
    textos=None,
    fora=None,
    titulos=None,
    pesos=None,
    frag=None,
    nos_quentes=(),
    arestas_quentes=(),
    arestas_fortes=(),
    so_arestas=None,
    volta=False,
    fora_quente=None,
    largura=1160,
    altura=470,
    r=30,
    escala=1.0,
):
    """Rede totalmente conectada.

    camadas         lista com o número de neurônios de cada camada
    textos          {(l, i): "x₁"}   texto dentro do nó i da camada l
    fora            {(l, i): "0,61"} valor em azul acima do nó (a ida)
    fora_quente     {(l, i): "δ"}    valor em laranja abaixo do nó (a volta)
    titulos         uma legenda por camada, no rodapé
    pesos           {(l, i, j): "0,1"} rótulo na aresta do nó i (camada l) ao nó j (camada l+1)
    frag            {l: k} a camada l (nós e arestas que chegam) aparece no clique k
    nos_quentes     {(l, i)} nós em laranja
    arestas_quentes {(l, i, j)} arestas em laranja; com volta=True a ponta vira para trás
    arestas_fortes  {(l, i, j)} arestas em azul forte
    so_arestas      se dado, as arestas fora deste conjunto ficam apagadas
    """
    textos, fora, pesos, frag = textos or {}, fora or {}, pesos or {}, frag or {}
    fora_quente = fora_quente or {}
    nl = len(camadas)
    topo, base = 50, (62 if titulos else 30)
    util = altura - topo - base
    mx = 100
    xs = [mx + l * (largura - 2 * mx) / (nl - 1) for l in range(nl)]

    def y(l, i):
        n = camadas[l]
        passo = min(util / n, 4.2 * r)
        return topo + util / 2 + (i - (n - 1) / 2) * passo

    grupos = {}

    def poe(l, s):
        grupos[l] = grupos.get(l, "") + s

    for l in range(nl - 1):
        for i in range(camadas[l]):
            for j in range(camadas[l + 1]):
                chave = (l, i, j)
                if chave in arestas_quentes:
                    cl = "q"
                elif chave in arestas_fortes:
                    cl = "forte"
                elif so_arestas is not None and chave not in so_arestas:
                    cl = "apagada"
                else:
                    cl = ""
                a, b_ = (xs[l], y(l, i)), (xs[l + 1], y(l + 1, j))
                if volta and chave in arestas_quentes:
                    s = _seta(*b_, *a, cl, folga_ini=r, folga_fim=r + 3)
                else:
                    s = _seta(*a, *b_, cl, ponta=cl in ("q", "forte"), folga_ini=r, folga_fim=r + (3 if cl else 0))
                if chave in pesos:
                    f = 0.3
                    s += _texto(
                        a[0] + f * (b_[0] - a[0]),
                        a[1] + f * (b_[1] - a[1]) - 15,
                        pesos[chave],
                        "peso" + (" q" if cl == "q" else ""),
                    )
                poe(l + 1, s)
    for l in range(nl):
        tipo = " ent" if l == 0 else (" sai" if l == nl - 1 else "")
        for i in range(camadas[l]):
            cq = " q" if (l, i) in nos_quentes else ""
            s = f'<circle class="no{tipo}{cq}" cx="{xs[l]:.1f}" cy="{y(l, i):.1f}" r="{r}"/>'
            if (l, i) in textos:
                s += _texto(xs[l], y(l, i), textos[(l, i)], "dentro")
            if (l, i) in fora:
                s += _texto(xs[l], y(l, i) - r - 17, fora[(l, i)], "ida")
            if (l, i) in fora_quente:
                s += _texto(xs[l], y(l, i) + r + 19, fora_quente[(l, i)], "volta")
            poe(l, s)
        if titulos:
            poe(l, _texto(xs[l], altura - 20, titulos[l], "tit"))
    corpo = "".join(_g(grupos[l], frag.get(l)) for l in sorted(grupos))
    _svg(largura, altura, corpo, escala)


# --------------------------------------------------------------------------
# Uma cadeia de contas: a ida por cima (azul), a volta por baixo (laranja)
# --------------------------------------------------------------------------
def cadeia(caixas, ida=None, volta=None, frag_volta=True, frag_ida=False, largura=1240, escala=1.0):
    """Caixas ligadas por setas.

    ida    rótulos sobre as setas, da esquerda para a direita (len(caixas) - 1)
    volta  rótulos sob as setas, na mesma ordem; aparecem da DIREITA para a
           ESQUERDA, um por clique, porque é assim que a derivada anda.
    """
    n = len(caixas)
    A = 240 if volta else 150
    cy = 78
    hc = 84
    lc = max(150, 30 + 15 * max(len(c) for c in caixas))
    mx = 20
    vao = (largura - 2 * mx - n * lc) / (n - 1)
    cx = [mx + lc / 2 + i * (lc + vao) for i in range(n)]
    corpo = ""
    for i, t in enumerate(caixas):
        s = f'<rect class="cx" x="{cx[i] - lc / 2:.1f}" y="{cy - hc / 2}" width="{lc}" height="{hc}" rx="12"/>'
        s += _texto(cx[i], cy, t, "dentro")
        if i > 0:
            x1, x2 = cx[i - 1] + lc / 2, cx[i] - lc / 2
            s += _seta(x1, cy - 12, x2, cy - 12, "forte", folga_ini=4, folga_fim=4)
            if ida:
                s += _texto((x1 + x2) / 2, cy - 36, ida[i - 1], "ida")
        corpo += _g(s, i if frag_ida else None)
    if volta:
        base = n if frag_ida else 0
        for i in range(n - 1, 0, -1):
            x1, x2 = cx[i - 1] + lc / 2, cx[i] - lc / 2
            s = _seta(x2, cy + 14, x1, cy + 14, "q", folga_ini=4, folga_fim=4)
            s += _texto((x1 + x2) / 2, cy + 42, volta[i - 1], "volta")
            corpo += _g(s, base + (n - 1 - i) if frag_volta else None)
    _svg(largura, 150 if volta else 126, corpo, escala)


# --------------------------------------------------------------------------
# O grafo de f = (x + y) · z
# --------------------------------------------------------------------------
def grafo_soma_produto(valores=True, gradientes=True, frag=True, escala=1.0):
    """x = -2, y = 5, z = -4: q = x + y = 3 e f = q · z = -12."""
    L, A = 1100, 450
    px = {"x": (90, 60), "y": (90, 250), "z": (90, 390), "+": (430, 155), "*": (760, 290), "f": (1020, 290)}
    r = 40
    k = iter(count())
    prox = (lambda: next(k)) if frag else (lambda: None)

    def no(nome, texto, classe="no"):
        x, y = px[nome]
        return f'<circle class="{classe}" cx="{x}" cy="{y}" r="{r}"/>' + _texto(x, y, texto, "grande")

    def aresta(a, b_, ida, volta, dy=0):
        (x1, y1), (x2, y2) = px[a], px[b_]
        mxx, myy = (x1 + x2) / 2, (y1 + y2) / 2
        s_ida = _seta(x1, y1, x2, y2, "forte", folga_ini=r, folga_fim=r + 3)
        s_ida += _texto(mxx, myy - 26 + dy, ida, "ida") if valores else ""
        s_volta = _texto(mxx, myy + 30 + dy, volta, "volta")
        return s_ida, s_volta

    base = (
        no("x", "x", "no ent") + no("y", "y", "no ent") + no("z", "z", "no ent") + no("+", "+") + no("*", "×")
    )
    partes = {
        "xq": aresta("x", "+", "x = −2", "∂f/∂x = −4"),
        "yq": aresta("y", "+", "y = 5", "∂f/∂y = −4"),
        "zf": aresta("z", "*", "z = −4", "∂f/∂z = 3"),
        "qf": aresta("+", "*", "q = 3", "∂f/∂q = −4"),
        "ff": aresta("*", "f", "f = −12", "∂f/∂f = 1"),
    }
    base += "".join(p[0] for p in partes.values())
    base += f'<circle class="no sai" cx="{px["f"][0]}" cy="{px["f"][1]}" r="{r}"/>' + _texto(*px["f"], "f", "grande")
    corpo = _g(base)
    if gradientes:
        corpo += _g(partes["ff"][1], prox())
        k2 = prox()
        corpo += _g(partes["qf"][1], k2) + _g(partes["zf"][1], k2)
        k3 = prox()
        corpo += _g(partes["xq"][1], k3) + _g(partes["yq"][1], k3)
    _svg(L, A, corpo, escala)
