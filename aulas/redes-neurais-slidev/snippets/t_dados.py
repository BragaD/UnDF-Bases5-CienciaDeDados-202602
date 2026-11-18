X_dig = digitos.data / 16                    # pixels de 0 a 16 viram 0 a 1
y_dig = digitos.target

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X_dig, y_dig, test_size=0.25, random_state=0, stratify=y_dig
)
Y_treino = np.eye(10)[y_treino]              # respostas em one-hot

print("treino:", X_treino.shape, "| teste:", X_teste.shape)
print("resposta da 1ª imagem:", y_treino[0], "| em one-hot:", Y_treino[0])
