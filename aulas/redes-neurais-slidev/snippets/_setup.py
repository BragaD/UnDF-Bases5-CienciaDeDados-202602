import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("../../estilo-figuras.mplstyle")
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.labelsize": 13, "figure.dpi": 100,
                     "axes.xmargin": 0.03, "axes.ymargin": 0.06, "axes.autolimit_mode": "data",
                     "svg.hashsalt": "redes-neurais"})
np.set_printoptions(precision=4, suppress=True)
pd.set_option("display.precision", 4)

AZUL, CEU, NAVY, LARANJA, CINZA = "#2264AF", "#8FCEF1", "#27316E", "#D9480F", "#8A99A5"


def regiao(ax, f, lim=(-0.5, 1.5)):
    """Pinta de azul claro a região em que f(pontos) >= 0,5."""
    g = np.linspace(lim[0], lim[1], 300)
    G1, G2 = np.meshgrid(g, g)
    S = f(np.column_stack([G1.ravel(), G2.ravel()])).reshape(G1.shape)
    ax.contourf(G1, G2, S, levels=[0.5, 1e9], colors=[CEU], alpha=0.45)
    ax.contour(G1, G2, S, levels=[0.5], colors=[LARANJA], linewidths=2.5)


def pontos(ax, X, y, titulo="", lim=(-0.5, 1.5)):
    """Classe 0 vazada, classe 1 cheia."""
    ax.scatter(X[y == 0, 0], X[y == 0, 1], s=170, facecolor="white", edgecolor=NAVY, linewidth=2.5, zorder=3)
    ax.scatter(X[y == 1, 0], X[y == 1, 1], s=170, color=NAVY, zorder=3)
    ax.set(xlim=lim, ylim=lim, xticks=[0, 1], yticks=[0, 1], title=titulo, aspect="equal")


X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_and = np.array([0, 0, 0, 1])
y_or = np.array([0, 1, 1, 1])
y_xor = np.array([0, 1, 1, 0])
