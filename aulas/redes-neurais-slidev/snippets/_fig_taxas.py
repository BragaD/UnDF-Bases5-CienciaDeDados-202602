fig, ax = plt.subplots(figsize=(11, 3.9))
estilos = {0.001: (CINZA, "$\\eta = 0{,}001$: passos pequenos demais"),
           0.1: (AZUL, "$\\eta = 0{,}1$: desce bem"),
           3.0: (LARANJA, "$\\eta = 3$: passos grandes demais, não desce")}
for eta_teste, (cor, rotulo) in estilos.items():
    _, h = treinar_digitos(eta=eta_teste)
    ax.plot(h.index, h["custo"], color=cor, lw=2.5)
    ax.annotate(rotulo, (30.4, h["custo"].iloc[-1]), color=cor, fontsize=12, va="center", annotation_clip=False)
ax.set(xlabel="época", ylabel="custo no treino", xlim=(1, 30), ylim=(0, 2.7))
fig.subplots_adjust(right=0.62)
salvar("taxas")
