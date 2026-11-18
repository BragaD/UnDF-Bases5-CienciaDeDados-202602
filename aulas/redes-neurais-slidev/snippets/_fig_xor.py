def rede_xor(P):
    return np.array([ida(p, W, b)[-1][0] for p in P])

def saida_xor(Hp):
    return sigmoide(Hp @ W[1][0] + b[1][0])

H_aprendido = np.array([ida(x_i, W, b)[1] for x_i in X])
fig, eixos = plt.subplots(1, 3, figsize=(12.6, 4.0))
eixos[0].plot(custos, color=AZUL, lw=2.5)
eixos[0].set(xlabel="época", ylabel="custo", ylim=(0, 0.8), xlim=(0, 5000), title="o custo cai")
g = np.linspace(-0.5, 1.5, 70)
G1, G2 = np.meshgrid(g, g)
S = rede_xor(np.column_stack([G1.ravel(), G2.ravel()])).reshape(G1.shape)
eixos[1].contourf(G1, G2, S, levels=[0.5, 2], colors=[CEU], alpha=0.45)
eixos[1].contour(G1, G2, S, levels=[0.5], colors=[LARANJA], linewidths=2.5)
pontos(eixos[1], X, y_xor, "nas entradas: fronteira dobrada")
eixos[1].set(xlabel="$x_1$", ylabel="$x_2$")
regiao(eixos[2], saida_xor, lim=(-0.15, 1.15))
pontos(eixos[2], H_aprendido, y_xor, "na camada oculta: uma reta", lim=(-0.15, 1.15))
eixos[2].set(xlabel="$h_1$", ylabel="$h_2$")
fig.tight_layout()
salvar("xor-aprendido")
