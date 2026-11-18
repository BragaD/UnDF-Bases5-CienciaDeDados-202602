portas = {"E": y_and, "OU": y_or, "OU exclusivo (XOR)": y_xor}
fig, eixos = plt.subplots(1, 3, sharey=True, figsize=(12, 3.6))
for ax, (nome, y_porta) in zip(eixos, portas.items()):
    hist = treinar_perceptron(X, y_porta, epocas=20)
    cor = LARANJA if "XOR" in nome else AZUL
    ax.plot(hist.index, hist["erros"], color=cor, lw=2, marker="o", ms=6)
    ax.set(title=nome, xlabel="época", ylim=(-0.3, 4.3), xticks=[1, 5, 10, 15, 20], yticks=[0, 1, 2, 3, 4])
eixos[0].set_ylabel("erros na época")
fig.tight_layout()
salvar("portas-erros")
