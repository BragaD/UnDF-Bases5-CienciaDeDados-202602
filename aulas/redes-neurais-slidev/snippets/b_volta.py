z1 = W1 @ x + b1                         # ida (guardando tudo)
a1 = sigmoide(z1)
z2 = W2 @ a1 + b2
a2 = sigmoide(z2)

delta2 = a2 - y                          # passo 1: erro da saída
grad_W2 = np.outer(delta2, a1)           # passo 2: gradientes da camada 2
grad_b2 = delta2
delta1 = (W2.T @ delta2) * a1 * (1 - a1) # passo 3: erro de volta à camada 1
grad_W1 = np.outer(delta1, x)            # passo 4: gradientes da camada 1
grad_b1 = delta1

print("delta2:", delta2.round(3), "| delta1:", delta1.round(3))
print("grad_W2:", grad_W2.round(3))
print("grad_W1:", grad_W1.round(3).tolist())
