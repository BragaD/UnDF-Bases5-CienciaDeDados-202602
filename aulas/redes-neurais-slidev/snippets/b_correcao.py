eta = 0.5
W1_novo = W1 - eta * grad_W1
b1_novo = b1 - eta * grad_b1
W2_novo = W2 - eta * grad_W2
b2_novo = b2 - eta * grad_b2

print("W1 novo:", W1_novo.round(3).tolist(), "| b1 novo:", b1_novo.round(3))
print("W2 novo:", W2_novo.round(3).tolist(), "| b2 novo:", b2_novo.round(3))
