def softmax(z):
    e = np.exp(z - z.max())        # subtrair o máximo evita números gigantes
    return e / e.sum()

z = np.array([2.0, 1.0, 0.1])
y = np.array([0, 1, 0])            # a classe certa é a segunda

y_chapeu = softmax(z)
perda = -np.sum(y * np.log(y_chapeu))
erro = y_chapeu - y

print("perda:", perda.round(3))
pd.DataFrame({"placar z": z, "probabilidade": y_chapeu.round(3), "resposta y": y, "erro": erro.round(3)},
             index=["gato", "cachorro", "pássaro"])
