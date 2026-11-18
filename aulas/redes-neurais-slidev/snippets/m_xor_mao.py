linhas = []
for x1, x2 in X:
    h1 = degrau(1 * x1 + 1 * x2 - 1)        # OU
    h2 = degrau(-1 * x1 - 1 * x2 + 1)       # NÃO-E
    saida = degrau(1 * h1 + 1 * h2 - 2)     # E
    linhas.append({"x1": x1, "x2": x2, "h1 (OU)": h1, "h2 (NÃO-E)": h2, "saída": saida})

tabela_xor = pd.DataFrame(linhas).set_index(["x1", "x2"])
tabela_xor["XOR"] = y_xor
tabela_xor
