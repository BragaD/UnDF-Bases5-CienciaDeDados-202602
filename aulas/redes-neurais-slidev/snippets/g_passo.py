def sigmoide(z):
    return 1 / (1 + np.exp(-z))

w = np.array([0.4, -0.6])
b = 0.1
x = np.array([2.0, 1.0])
y = 1
eta = 0.5

y_chapeu = sigmoide(w @ x + b)             # 1. prever
perda = -np.log(y_chapeu)                  # 2. medir (y = 1)
erro = y_chapeu - y                        # 3. atribuir
grad_w = erro * x
grad_b = erro
w = w - eta * grad_w                       # 4. corrigir
b = b - eta * grad_b

print("previsão:", y_chapeu.round(3), "| perda:", perda.round(3))
print("gradiente dos pesos:", grad_w.round(3), "| do viés:", grad_b.round(3))
print("pesos novos:", w.round(3), "| viés novo:", b.round(3))
print("previsão nova:", sigmoide(w @ x + b).round(3))
