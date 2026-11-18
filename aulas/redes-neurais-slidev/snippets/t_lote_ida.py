X_lote, Y_lote = X_treino[:32], Y_treino[:32]     # as 32 primeiras imagens

Z1 = X_lote @ W1.T + b1                           # ida, 32 exemplos de uma vez
A1 = relu(Z1)
Z2 = A1 @ W2.T + b2
P = softmax_lote(Z2)

print("formas -> X_lote:", X_lote.shape, "| Z1:", Z1.shape, "| P:", P.shape)
print("probabilidades da 1ª imagem:", P[0].round(2))
