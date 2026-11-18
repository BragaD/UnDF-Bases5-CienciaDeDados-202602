def degrau(z):
    return 1 if z >= 0 else 0

w = np.zeros(2)
b = 0.0
eta = 1.0

x_i, y_i = X[0], y_and[0]          # o exemplo (0, 0), resposta 0

z = w @ x_i + b                    # 1. soma ponderada
y_chapeu = degrau(z)               # 2. previsão
erro = y_i - y_chapeu              # 3. erro
w = w + eta * erro * x_i           # 4. correção dos pesos
b = b + eta * erro                 #    e do viés

print("z:", z, "| previsão:", y_chapeu, "| erro:", erro)
print("pesos depois:", w, "| viés depois:", b)
