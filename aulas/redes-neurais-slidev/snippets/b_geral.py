def ida(x, W, b):
    a = [x]                                   # a[0] é a entrada
    for W_l, b_l in zip(W, b):
        a.append(sigmoide(W_l @ a[-1] + b_l))
    return a                                  # as ativações de todas as camadas

def volta(y, W, a):
    grad_W = [None] * len(W)
    grad_b = [None] * len(W)
    delta = a[-1] - y                         # erro da saída
    for l in range(len(W) - 1, -1, -1):       # da última camada à primeira
        grad_W[l] = np.outer(delta, a[l])
        grad_b[l] = delta
        if l > 0:                             # erro de volta uma camada
            delta = (W[l].T @ delta) * a[l] * (1 - a[l])
    return grad_W, grad_b
