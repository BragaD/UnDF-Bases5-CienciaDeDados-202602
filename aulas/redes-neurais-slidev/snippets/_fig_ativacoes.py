zz = np.linspace(-5, 5, 400)
s = sigmoide(zz)
t = np.tanh(zz)
funcoes = [
    ("sigmoide", s, s * (1 - s), (-0.1, 1.1)),
    ("tanh", t, 1 - t**2, (-1.1, 1.1)),
    ("ReLU", np.maximum(0, zz), (zz > 0).astype(float), (-0.3, 5.2)),
]
fig, eixos = plt.subplots(1, 3, figsize=(12.5, 2.9))
for ax, (nome, f, df, ylim) in zip(eixos, funcoes):
    ax.plot(zz, f, color=AZUL, lw=3)
    ax.plot(zz, df, color=LARANJA, lw=2, ls="--")
    ax.set(title=nome, xlabel="$z$", ylim=ylim)
eixos[0].annotate("$g(z)$", (2.6, 0.78), color=AZUL, fontsize=13)
eixos[0].annotate("derivada $g'(z)$", (0.9, 0.3), color=LARANJA, fontsize=13)
fig.tight_layout()
salvar("ativacoes")
