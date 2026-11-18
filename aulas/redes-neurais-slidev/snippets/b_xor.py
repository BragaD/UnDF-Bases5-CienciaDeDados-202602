rng = np.random.default_rng(1)
W = [rng.normal(0, 1, (2, 2)), rng.normal(0, 1, (1, 2))]     # rede 2-2-1
b = [np.zeros(2), np.zeros(1)]
eta = 0.5
custos = []

for epoca in range(5000):
    perda_da_epoca = 0.0
    for x_i, y_i in zip(X, y_xor):
        a = ida(x_i, W, b)                                    # ida
        grad_W, grad_b = volta(y_i, W, a)                     # volta
        for l in range(len(W)):                               # correção
            W[l] = W[l] - eta * grad_W[l]
            b[l] = b[l] - eta * grad_b[l]
        y_chapeu = a[-1][0]
        perda_da_epoca += -(y_i * np.log(y_chapeu) + (1 - y_i) * np.log(1 - y_chapeu))
    custos.append(perda_da_epoca / len(X))
