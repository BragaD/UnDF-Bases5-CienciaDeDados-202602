def treinar_neuronio(X, y, eta=1.0, epocas=2000):
    w = np.zeros(X.shape[1])
    b = 0.0
    custos = []
    for epoca in range(epocas):
        y_chapeu = sigmoide(X @ w + b)
        perdas = -(y * np.log(y_chapeu) + (1 - y) * np.log(1 - y_chapeu))
        erro = y_chapeu - y
        w = w - eta * X.T @ erro / len(X)
        b = b - eta * erro.mean()
        custos.append(perdas.mean())
    return w, b, custos
