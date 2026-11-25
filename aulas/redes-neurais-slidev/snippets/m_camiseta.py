cam = pd.DataFrame({"preço": [40, 150, 70], "frete": [10, 20, 0],
                    "marketing": [2, 30, 20], "material": [4, 9, 8]}, index=["A", "B", "C"])

# camada oculta: três atributos que não estão na tabela
cam["acessível"] = sigmoide(-0.05 * cam["preço"] - 0.05 * cam["frete"] + 4)
cam["conhecida"] = sigmoide(0.2 * cam["marketing"] - 2)
cam["qualidade"] = sigmoide(0.02 * cam["preço"] + 0.5 * cam["material"] - 4)

# saída: só recebe os três atributos da camada oculta
cam["P(campeã)"] = sigmoide(3 * cam["acessível"] + 3 * cam["conhecida"] + 3 * cam["qualidade"] - 5)
cam.round(2)
