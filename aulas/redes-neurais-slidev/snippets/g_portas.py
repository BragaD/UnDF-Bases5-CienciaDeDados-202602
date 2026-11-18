linhas = []
for nome, y_porta in [("E", y_and), ("OU", y_or), ("XOR", y_xor)]:
    w, b, custos = treinar_neuronio(X, y_porta)
    linhas.append({"porta": nome, "custo final": round(custos[-1], 3), "pesos": w.round(2),
                   "previsões para (0,0) (0,1) (1,0) (1,1)": sigmoide(X @ w + b).round(2)})

print("custo de quem responde 0,5 para tudo:", -np.log(0.5).round(3))
pd.DataFrame(linhas).set_index("porta")
