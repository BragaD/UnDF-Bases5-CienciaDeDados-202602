def perda_da_rede(W1, b1, W2, b2):
    a2 = sigmoide(W2 @ sigmoide(W1 @ x + b1) + b2)
    return -np.log(a2[0])

eps = 1e-6
perda_original = perda_da_rede(W1, b1, W2, b2)
linhas = []
for j in range(2):
    for k in range(2):
        W1_mexido = W1.copy()
        W1_mexido[j, k] = W1_mexido[j, k] + eps
        numerico = (perda_da_rede(W1_mexido, b1, W2, b2) - perda_original) / eps
        linhas.append({"peso": f"W1[{j},{k}]",
                       "backpropagation": grad_W1[j, k], "mexendo no peso": numerico})

pd.DataFrame(linhas).set_index("peso").round(5)
