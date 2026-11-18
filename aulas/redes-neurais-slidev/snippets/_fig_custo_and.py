fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.plot(custos, color=AZUL, lw=2.5)
ax.set(xlabel="época", ylabel="custo $J$", ylim=(0, 0.75), xlim=(0, 2000))
salvar("custo-and")
