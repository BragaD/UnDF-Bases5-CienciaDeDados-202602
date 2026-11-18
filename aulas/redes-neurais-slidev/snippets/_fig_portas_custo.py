fig, ax = plt.subplots(figsize=(6.4, 3.2))
for nome, y_porta, cor in [("E", y_and, AZUL), ("OU", y_or, NAVY), ("XOR", y_xor, LARANJA)]:
    ax.plot(treinar_neuronio(X, y_porta)[2], color=cor, lw=2.5)
ax.annotate("XOR", (1500, 0.6), color=LARANJA, fontsize=13)
ax.annotate("E e OU", (300, 0.12), color=AZUL, fontsize=13)
ax.set(xlabel="época", ylabel="custo $J$", xlim=(0, 2000), ylim=(0, 0.8))
salvar("portas-custo")
