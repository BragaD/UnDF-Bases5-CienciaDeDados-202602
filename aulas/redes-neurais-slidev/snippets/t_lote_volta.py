m = len(X_lote)
custo = -np.sum(Y_lote * np.log(P)) / m

D2 = (P - Y_lote) / m                 # eq. 1: erro da saída (já com a média)
grad_W2 = D2.T @ A1                   # eq. 3
grad_b2 = D2.sum(axis=0)              # eq. 4
D1 = (D2 @ W2) * (Z1 > 0)             # eq. 2: (Z1 > 0) é a derivada da ReLU
grad_W1 = D1.T @ X_lote
grad_b1 = D1.sum(axis=0)

print("custo do lote antes de treinar:", custo.round(3))
print("formas dos gradientes -> W2:", grad_W2.shape, "| W1:", grad_W1.shape)
