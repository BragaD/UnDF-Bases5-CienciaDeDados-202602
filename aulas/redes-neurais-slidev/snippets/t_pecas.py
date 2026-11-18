def relu(Z):
    return np.maximum(0, Z)

def softmax_lote(Z):                              # softmax em cada linha
    E = np.exp(Z - Z.max(axis=1, keepdims=True))
    return E / E.sum(axis=1, keepdims=True)

rng = np.random.default_rng(0)
W1 = rng.normal(0, np.sqrt(2 / 64), (32, 64))     # pesos pequenos e aleatórios
b1 = np.zeros(32)
W2 = rng.normal(0, np.sqrt(2 / 32), (10, 32))
b2 = np.zeros(10)

print("W1:", W1.shape, "| b1:", b1.shape, "| W2:", W2.shape, "| b2:", b2.shape)
print("parâmetros:", W1.size + b1.size + W2.size + b2.size)
