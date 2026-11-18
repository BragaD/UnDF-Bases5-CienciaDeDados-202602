linhas = []
for x_i, y_i in zip(X, y_xor):
    a = ida(x_i, W, b)
    linhas.append({"x1": x_i[0], "x2": x_i[1], "XOR": y_i, "h1": a[1][0], "h2": a[1][1], "previsão": a[2][0]})
print("custo na última época:", round(custos[-1], 4))
pd.DataFrame(linhas).set_index(["x1", "x2"]).round(3)
