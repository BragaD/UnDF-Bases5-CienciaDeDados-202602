# Relatório — Capítulo 13 (Regressão Logística)

## Status

Escritos os 5 arquivos de `content/cap13/`, substituindo os stubs. **`make render`: OK (tentativa 1), duas vezes.** **`make teste`: 24/24 passaram.** Oito figuras geradas; todas abertas com `Read` e a prosa ajustada onde não batia (a descrição da nuvem de pagantes na §1, a do gráfico previsto-vs-real na §4 e a da fronteira na §5 foram corrigidas depois de olhar os PNGs).

## Números, todos extraídos do HTML renderizado

- **§1** — 200 usuários, 52 pagantes (26%). `least_squares_fit` reescalonado: β = `[0.2554, 0.4374, -0.4271]`; previsões de **−0,5772 a 1,4368**, com **37 negativas** e **1 acima de 1**.
- **§2** — `logistic(36) = 0.9999999999999998`, `logistic(37) = 1.0` exato; o limiar de saturação (≈ 36,74) é $\log(2^{-53})$, ou seja, a mantissa do `float64`, não uma propriedade da logística.
- **§3** — com `random.seed(0)`, β inicial `[0.844422, 0.757954, 0.420572]`; `dot(xs[0], beta) = 20188.81` → `logistic = 1.0`. O **ponto 0 (y=1) devolve perda `-0.0`** — falha silenciosa — e o **ponto 1 (y=0) levanta `ValueError: math domain error`**, ambos impressos na página. Reescalonado: `dot = -0.8059`, `logistic = 0.3088`. Ajuste: 134/66, β = `[-2.0239, 4.693, -4.4698]`, perda 39,9635 (113,07 → 61,76 → 41,22 → 39,9635 nas épocas 1/10/100/1000). `beta_unscaled = [8.9272, 1.6482, -0.00028769]`, e o `assert` de igualdade exata de float entre as duas verossimilhanças passa (57,678978614160044).
- **§4** — tp=12, fp=4, fn=3, tn=47; **precisão 0,75, revocação 0,8**, acurácia 0,894, F1 0,774. Piso "sempre não paga": acurácia 0,773 com revocação 0. Tabela de limiares de 0,2 a 0,8 medida (revocação 0,867 → 0,533).
- **§5** — 21 dos 200 do lado errado da fronteira. **Busca exaustiva prova que os dados não são linearmente separáveis** (19.900 pares, < 1 s, roda como chunk). Em dados separáveis, |β| cresce de 1,22 a 4,61 em 50.000 épocas com a perda indo a 0,00044 — a demonstração de que a verossimilhança não tem máximo ali.

## O que ficou de fora, e por quê

- **Nenhuma implementação de SVM**, como o brief manda: o Grus não implementa, e a implementação honesta seria um solucionador de programação quadrática. A §5 entrega o critério da margem, por que ele difere de maximizar verossimilhança (duas faces: quais pontos importam; e a divergência em dados separáveis) e o que o kernel compra, com figura do mapa $x \to (x, x^2)$.
- **`scratch.working_with_data` nunca foi importado**: `scale`/`rescale` estão inline nas §§1, 3, 4 e 5 (kernel por página), apontando para a seção 7.6.
- Não usei `tqdm` na §4 nem na §5 (refazem o ajuste sem barra); a §3 mantém o `tqdm.trange` do Grus com `#| warning: false`.

## Preocupações

- **Repetição de código.** As §§3, 4 e 5 refazem `scale`/`rescale` e o ajuste de 5.000 épocas, porque cada página tem kernel próprio e o β ajustado só existe dentro do `main()` de `scratch/logistic_regression.py`. Custo: ~1,5 s por página. É a única saída sem editar o pacote vendorizado, mas é visualmente repetitivo para quem lê as três seções em sequência.
- A afirmação sobre `sklearn` rodando bem em dados não reescalonados foi **medida** (intercepto 8,41; coeficientes 1,51 e −0,00027), assim como a versão sem penalidade (`[-2.11, 4.53, -4.40]`). Como `penalty=None` está *deprecated* no sklearn 1.9, o callout fala só em `C`, sem mostrar API obsoleta.
