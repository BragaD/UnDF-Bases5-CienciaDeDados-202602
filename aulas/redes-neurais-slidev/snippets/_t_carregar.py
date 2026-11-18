from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

digitos = load_digits()
fig, eixos = plt.subplots(2, 10, figsize=(12.5, 2.9))
for ax, imagem, rotulo in zip(eixos.ravel(), digitos.images, digitos.target):
    ax.imshow(imagem, cmap="Blues")
    ax.set_title(str(rotulo), fontsize=13)
    ax.axis("off")
fig.tight_layout()
salvar("digitos")
