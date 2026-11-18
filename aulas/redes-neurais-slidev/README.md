# Redes Neurais — versão em Slidev

Versão alternativa da aula de `../redes-neurais/` (Quarto + reveal.js), com o mesmo conteúdo e
os mesmos exemplos numéricos, mais passos por clique e componentes interativos. A versão em
Quarto não depende desta pasta nem foi alterada.

## Apresentar

```bash
npm install          # uma vez
npm run dev          # abre em http://localhost:3030
```

Teclas: `→` avança um clique, `o` mostra todos os slides, `p` abre o modo apresentador (com as
notas), `d` liga o desenho sobre o slide, `g` vai a um slide pelo número.

`npm run build` gera o site estático em `dist/` (abre de qualquer servidor de arquivos).
`npm run export` gera um PDF com um quadro por clique.

## O que tem em cada pasta

| pasta | conteúdo |
|---|---|
| `slides.md` | capa e a ordem das partes |
| `pages/` | uma parte da aula por arquivo (`0-abertura.md` a `6-treino.md`) |
| `components/` | desenhos (`Neuronio`, `Rede`, `Cadeia`, `GrafoConta`) e os interativos |
| `snippets/` | o código Python mostrado nos slides, um trecho por arquivo |
| `saidas/`, `public/fig/` | a saída e as figuras de cada trecho, geradas por `gerar_saidas.py` |
| `styles/index.css` | a paleta (azul é a ida, laranja é a volta) e as classes dos slides |

## Os números não são digitados

Os slides mostram o código de `snippets/` e a saída gravada em `saidas/`. Mudou um trecho de
código? Rode de novo:

```bash
npm run saidas       # executa snippets/ na ordem de snippets/_ordem.txt, com o .venv da raiz
```

Os trechos cujo nome começa por `_` rodam mas não aparecem como código (preparo e figuras).
Os destaques linha a linha (`{1-2|4-6|…}` em `pages/`) referem-se aos números de linha do
trecho: se o trecho mudar de tamanho, confira os intervalos.

## Os componentes interativos

| componente | slide | o que faz |
|---|---|---|
| `NeuronioInterativo` | Parte 1 | pesos e viés na mão; a reta e os acertos em E, OU e XOR |
| `PerceptronPasso` | Parte 1 | a regra do perceptron, um exemplo por clique |
| `SigmoideExplora` | Parte 2 | degrau contra sigmoide quando z anda um pouco |
| `PerdaExplora` | Parte 2 | a entropia cruzada para cada previsão |
| `DescidaGradiente` | Parte 2 | um passo de gradiente por clique, com a taxa η |
| `NeuronioTreino` | Parte 2 | o neurônio sigmoide treinando em E, OU e XOR |
| `XorMao` | Parte 3 | a rede de três perceptrons e o plano (h₁, h₂) |
| `IdaVolta` | Partes 3 e 5 | a rede 2-2-1 em dez etapas: ida, volta e correção |
| `SoftmaxExplora` | Parte 4 | placares, probabilidades, perda e erro |
| `TreinoXor` | Parte 5 | a rede 2-2-1 aprendendo o XOR na tela |
| `GradienteSome` | Parte 5 | o fator sobre o erro depois de n camadas |

As contas desses componentes rodam no navegador. Onde repetem uma conta do Python (o treino do
neurônio nas portas, a ida e a volta da rede 2-2-1), os números são os mesmos. `TreinoXor`
sorteia os pesos com um gerador próprio, não o do `numpy`: o slide diz isso.
