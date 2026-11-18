pesos, hist = treinar_digitos(eta=0.1)
W1, b1, W2, b2 = pesos

def prever(X):
    A1 = relu(X @ W1.T + b1)
    P = softmax_lote(A1 @ W2.T + b2)
    return P.argmax(axis=1)     # classe mais provável

acertos_treino = (prever(X_treino) == y_treino).mean()
acertos_teste = (prever(X_teste) == y_teste).mean()
print("acurácia no treino:", acertos_treino.round(3))
print("acurácia no teste: ", acertos_teste.round(3))
