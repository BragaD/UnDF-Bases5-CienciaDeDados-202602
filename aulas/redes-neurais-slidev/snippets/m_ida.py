W1 = np.array([[0.1, 0.3], [-0.2, 0.4]])
b1 = np.array([0.1, -0.1])
W2 = np.array([[0.5, -0.3]])
b2 = np.array([0.2])

x = np.array([0.5, 1.0])
y = 1

z1 = W1 @ x + b1            # camada 1: somas
a1 = sigmoide(z1)           #           ativações
z2 = W2 @ a1 + b2           # camada 2: soma
a2 = sigmoide(z2)           #           ativação = previsão
perda = -np.log(a2)

print("z1:", z1, "| a1:", a1.round(3))
print("z2:", z2.round(3), "| previsão:", a2.round(3), "| perda:", perda.round(3))
