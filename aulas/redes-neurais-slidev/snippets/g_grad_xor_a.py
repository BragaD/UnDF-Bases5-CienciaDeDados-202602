w = np.zeros(2)
b = 0.0
y_chapeu = sigmoide(X @ w + b)
erro = y_chapeu - y_xor

pd.DataFrame({"XOR": y_xor, "previsão": y_chapeu, "erro": erro,
              "erro · x1": erro * X[:, 0] + 0.0, "erro · x2": erro * X[:, 1] + 0.0},
             index=["(0, 0)", "(0, 1)", "(1, 0)", "(1, 1)"])
