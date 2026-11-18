from sklearn.neural_network import MLPRegressor

rng = np.random.default_rng(3)
x_curva = np.sort(rng.uniform(-3, 3, 120))
y_curva = np.sin(2 * x_curva) + 0.3 * x_curva + rng.normal(0, 0.15, 120)
grade = np.linspace(-3, 3, 300)

fig, eixos = plt.subplots(1, 3, figsize=(12.5, 3.9), sharey=True)
for ax, n in zip(eixos, [1, 3, 20]):
    modelo = MLPRegressor(hidden_layer_sizes=(n,), activation="tanh", solver="lbfgs", max_iter=5000, random_state=1)
    modelo.fit(x_curva.reshape(-1, 1), y_curva)
    ax.scatter(x_curva, y_curva, s=14, color=CINZA, alpha=0.6)
    ax.plot(grade, modelo.predict(grade.reshape(-1, 1)), color=AZUL, lw=3)
    ax.set(title=f"{n} neurônio(s) na camada oculta", xlabel="$x$")
eixos[0].set_ylabel("$y$")
fig.tight_layout()
salvar("curvas")
