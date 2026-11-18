previsto = prever(X_teste)
errados = np.flatnonzero(previsto != y_teste)[:10]
fig, eixos = plt.subplots(1, len(errados), figsize=(12.5, 1.9))
for ax, i in zip(eixos, errados):
    ax.imshow(X_teste[i].reshape(8, 8), cmap="Blues")
    ax.set_title(f"era {y_teste[i]}\ndisse {previsto[i]}", fontsize=12, color=LARANJA)
    ax.axis("off")
fig.tight_layout()
salvar("erros-digitos")
