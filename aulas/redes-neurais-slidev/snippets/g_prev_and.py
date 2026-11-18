pd.DataFrame(
    {"resposta": y_and,
     "previsão": sigmoide(X @ w + b).round(3)},
    index=["(0, 0)", "(0, 1)", "(1, 0)", "(1, 1)"],
)
