def treinar_digitos(eta, epocas=30, tamanho_lote=32, semente=0):
    rng = np.random.default_rng(semente)
    W1 = rng.normal(0, np.sqrt(2 / 64), (32, 64)); b1 = np.zeros(32)
    W2 = rng.normal(0, np.sqrt(2 / 32), (10, 32)); b2 = np.zeros(10)
    historico = []
    for epoca in range(1, epocas + 1):
        ordem = rng.permutation(len(X_treino))                 # embaralha a cada época
        for inicio in range(0, len(ordem), tamanho_lote):
            lote = ordem[inicio:inicio + tamanho_lote]
            A0, Y = X_treino[lote], Y_treino[lote]
            Z1 = A0 @ W1.T + b1; A1 = relu(Z1)                 # ida
            P = softmax_lote(A1 @ W2.T + b2)
            D2 = (P - Y) / len(lote)                           # volta
            D1 = (D2 @ W2) * (Z1 > 0)
            W2 -= eta * D2.T @ A1; b2 -= eta * D2.sum(axis=0)  # correção
            W1 -= eta * D1.T @ A0; b1 -= eta * D1.sum(axis=0)
        P_treino = softmax_lote(relu(X_treino @ W1.T + b1) @ W2.T + b2)
        historico.append({"época": epoca, "custo": -np.mean(np.log(P_treino[Y_treino == 1] + 1e-12))})
    return (W1, b1, W2, b2), pd.DataFrame(historico).set_index("época")
