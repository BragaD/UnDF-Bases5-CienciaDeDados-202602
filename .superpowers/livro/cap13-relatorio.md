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

---

# Adendo — rodada de correções (16/08, tarde)

Aplicadas contra `.superpowers/livro/cap13-correcoes.md`: **C1, I1–I5, M1–M12**. Nada do capítulo foi reescrito; o texto elogiado pelas duas revisões está intacto. `make render` OK (tentativa 2, depois tentativa 1 num segundo passe) e `make teste` 24/24, duas vezes.

## C1 — o `assert` de igualdade exata: o callout mentia, e mentia contra o cap. 10

O callout antigo afirmava que "as operações se cancelam exatamente" e que "não é sorte". **É sorte, e agora o capítulo mostra isso rodando.** Medições feitas neste container, todas reproduzidas na página:

- **`==` vale em 2.169 das 5.000 épocas** do próprio treino (43,4%). Cara ou coroa; o β final do Grus caiu do lado da cara.
- **`math.isclose` vale em 5.000 de 5.000.**
- Ponto a ponto **não** se cancela: com o β final, só **8 dos 200** produtos escalares saem bit a bit idênticos entre as duas escalas; diferença máxima $4{,}4\times10^{-15}$. A igualdade aparece só na soma, por arredondamento.
- A época 500 é o contraexemplo exibido: 57,67164046623943 contra 57,67164046623944.

O chunk `ajusta` ganhou uma linha (`betas.append(beta)`) para que o caminho inteiro fique disponível; o chunk novo `assert-por-sorte` imprime a tabela de sete épocas e o placar `==` × `math.isclose`. O callout virou `.callout-warning`, aponta para a **§10.4** (o link antigo ia para `cap10/03-implementacao.qmd`, seção errada) e registra que o `assert` é do próprio livro-texto (`scratch/logistic_regression.py`, bloco `__main__`) — mesma família do `set` não determinístico que o cap. 10 já marca. O capítulo agora **concorda** com o 10.

## Os Importantes

- **I1** — objetivo nº 5 do índice trocado pelo enunciado forte ("perda zero e completamente errado… nenhuma biblioteca teria mostrado isso"). A tese saiu de dentro do "Na prática" colapsado e virou três parágrafos de prosa corrida na §3, entre o callout das duas falhas e "O conserto". O callout de biblioteca da §3 passou a rebater as **duas** falhas (o `-0.0` some porque a interface não expõe perda de ponto isolado). E a §2 perdeu o trecho a partir de "não em algum caso patológico raro", que entregava o desfecho.
- **I2** — `## O que este capítulo deixa` escrito antes do callout final da §5: retoma a escada 11 → 12 → 13 das fórmulas fechadas e entrega o cap. 14 pelo argumento da indiferença à escala (a árvore só olha ordem, e reescalonar preserva ordem). O capítulo 14 era citado zero vezes nos seis arquivos.
- **I3** — a regra do kernel virou um callout único e titulado na §3, que também explica a repetição vindoura; §4 e §5 apontam de volta para ele e tiveram o bloco de refazimento marcado com `#| echo: false` (saída preservada: o `beta` e o `beta_unscaled`). Não usei `code-fold`.
- **I4** — "espaço de parâmetros" → **espaço de atributos**, com `.callout-warning` marcando o deslize do Grus (p. 205), separando os dois espaços e explicando a simetria que provavelmente o gera ($\beta\cdot x=0$ é hiperplano nos dois, conforme qual vetor se segura fixo).
- **I5** — Bernoulli nomeada na §2, logo depois de "Uma fórmula, os dois casos, sem `if`", com o link para a §11.3 que prometeu a troca.

## Menores

M1 título ("deixa de ser a mesma coisa"). M2 limiar reescrito como $-\log(2^{-53}) = 53\ln 2 \approx 36{,}7368$, conferido por bissecção (36.73680056967711). M3 sexta casa na perda (39,96350015 → 39,96349522) e terceira no β (4,6903 → 4,6930), os dois nomeados. M4 os três falsos negativos redescritos (0,457 limítrofe; 0,163 aposta errada com 84% de confiança) e os falsos positivos "da dúvida à convicção". M5 padronizado em 99,22% / 0,13%. M6 usa o número: 38 dos 200. M7 `print()` nos dois, com if/else honesto no `separavel`. M8 cláusula sobre `xs_sep`. M9 as quatro trocas de prosa. M10 callout do `warning: false` removido, link preservado na frase que introduz o chunk. M11 `SVC(probability=True)` depreciado na 1.9 e removido na 1.11 → `CalibratedClassifierCV(SVC(), ensemble=False)` (verificado: o `FutureWarning` real da 1.9.0); a ironia da calibração logística ficou melhor. M12 os dois títulos renomeados — `Na prática: scikit-learn` na §5, `Na prática: networkx` em `cap01/03`.

## Não mexi

"For Further Investigation" no `index.qmd` e os `[-2.11, 4.53, -4.40]` do callout de biblioteca, como manda a seção "Não mexa nisto".

## Preocupações

- **Um arquivo fora do cap. 13 foi tocado**: `content/cap01/03-hipotese-motivadora-datasciencester.qmd`, só o título do callout (M12).
- O chunk novo da §3 avalia a perda 10.000 vezes (5.000 β × 2 escalas). Custo medido: **~3 s**, congelado pelo `freeze`. Se um dia pesar, dá para cortar para uma amostra de épocas sem perder o argumento.
- Os números "8 de 200" e "$4{,}4\times10^{-15}$" estão em prosa, não em chunk. São reprodutíveis nesta imagem, mas não se autoverificam a cada render como os outros; se alguém trocar a semente ou os hiperparâmetros do ajuste, eles envelhecem em silêncio. O placar `==` / `isclose`, esse, é calculado na página.
