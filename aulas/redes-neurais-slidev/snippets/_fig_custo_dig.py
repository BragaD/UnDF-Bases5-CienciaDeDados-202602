fig, ax = plt.subplots(figsize=(5.6, 4.0))
ax.plot(hist.index, hist["custo"], color=AZUL, lw=2.5)
ax.set(xlabel="época", ylabel="custo no treino", ylim=(0, None), xlim=(1, 30))
salvar("custo-digitos")
