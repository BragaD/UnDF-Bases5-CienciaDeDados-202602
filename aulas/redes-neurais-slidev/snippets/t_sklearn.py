from sklearn.neural_network import MLPClassifier

modelo = MLPClassifier(hidden_layer_sizes=(32,), activation="relu", solver="sgd",
                       learning_rate_init=0.1, batch_size=32, max_iter=30, random_state=0)
modelo.fit(X_treino, y_treino)

pd.DataFrame(
    {"acurácia no teste": [acertos_teste, modelo.score(X_teste, y_teste)]},
    index=["nossa rede, em numpy", "MLPClassifier"],
).round(3)
