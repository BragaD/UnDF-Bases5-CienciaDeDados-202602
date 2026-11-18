w = np.zeros(2)
b = 0.0
eta = 1.0
custos = []

for epoca in range(2000):
    y_chapeu = sigmoide(X @ w + b)                 # as 4 previsões de uma vez
    perdas = -(y_and * np.log(y_chapeu) + (1 - y_and) * np.log(1 - y_chapeu))
    erro = y_chapeu - y_and                        # os 4 erros
    grad_w = X.T @ erro / len(X)                   # média de erro · entrada
    grad_b = erro.mean()
    w = w - eta * grad_w
    b = b - eta * grad_b
    custos.append(perdas.mean())

print("pesos:", w.round(2), "| viés:", b.round(2), "| custo final:", round(custos[-1], 3))
