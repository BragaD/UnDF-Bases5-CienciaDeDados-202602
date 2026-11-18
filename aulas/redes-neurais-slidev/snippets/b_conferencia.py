a1_novo = sigmoide(W1_novo @ x + b1_novo)
a2_novo = sigmoide(W2_novo @ a1_novo + b2_novo)

pd.DataFrame(
    {"previsão": [a2[0], a2_novo[0]], "perda": [-np.log(a2[0]), -np.log(a2_novo[0])]},
    index=["antes do passo", "depois do passo"],
).round(3)
