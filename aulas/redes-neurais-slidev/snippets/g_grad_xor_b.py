print("gradiente dos pesos:", X.T @ erro / len(X), "| gradiente do viés:", erro.mean())
