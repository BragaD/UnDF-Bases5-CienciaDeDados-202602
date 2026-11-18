def treinar_perceptron(X, y, eta=1.0, epocas=8):
    w = np.zeros(X.shape[1])
    b = 0.0
    historico = []
    for epoca in range(1, epocas + 1):
        erros = 0
        for x_i, y_i in zip(X, y):
            erro = y_i - degrau(w @ x_i + b)
            w = w + eta * erro * x_i
            b = b + eta * erro
            erros = erros + abs(erro)
        historico.append({"época": epoca, "erros": erros, "w1": w[0], "w2": w[1], "b": b})
    return pd.DataFrame(historico).set_index("época")
