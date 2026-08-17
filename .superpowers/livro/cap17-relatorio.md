# Capítulo 17 — relatório

## Adendo: segunda rodada de correções (`cap17-correcoes-2.md`)

**Status: aplicado e verificado.** `make render` → `render OK (tentativa 2)`. `make teste` → 24 passaram.

**I1 (as duas aberturas).** O `index` ficou com a lista de exemplos e a tese ("havia um gabarito");
saiu de lá só a frase "Alguém já tinha respondido à pergunta antes...", que era o que a §1 precisava
para ter o que dizer. A §1 agora abre pelas **pessoas** — o botânico que escreveu *virginica*, o
usuário que apertou "marcar como spam", o relógio, quem olhou o rabisco de 28 por 28 e digitou 7 —,
e fecha com "o rótulo nunca foi uma propriedade do dado: é trabalho humano, feito antes". A frase
"o único em que ninguém respondeu nada" continua sendo o pivô do parágrafo seguinte.

**Menores.** M1 (remendo), M2 ("o algoritmo de agrupamento mais usado que existe"), M3 ("parece
contradizer"), M4 ("métrica de separação"), M5 ("assombrosamente ineficiente"), M6 (meia frase na
atribuição de Herrick, registrando que no original os cachos são *clusters*), M7 (06:220 agora nomeia
as cores: estrelas azuis / losangos vermelhos / círculos verdes), M8 (`03:174` encolheu para uma
frase com link para o callout da §17.2), M9 ("dois passos exatos (2 e 4) até nada mudar").

**Figuras abertas depois do render** (de `_freeze/`, porque outro agente estava renderizando e o
`_book/` estava sendo reescrito): `fig-hierarquico-min` — confere com a prosa nova (14 estrelas
azuis, 4 losangos vermelhos no nordeste, 2 círculos verdes); `fig-hierarquico-max` e
`fig-tres-grupos` — continuam sobreponíveis, idênticas exceto pelo título. Nenhum código de figura
foi tocado.

**Fora de escopo, de propósito:** M10 (o callout de `adjusted_rand_score`), por decisão do contrato;
o fecho inteiro, incluindo o parágrafo novo da segunda promessa.

**Preocupações:** nenhuma de conteúdo. Só uma de ambiente: ao fim do meu render outro agente pegou o
lock, então o `_book/` estava vazio na hora da conferência — as figuras vieram do `_freeze/`, que é
o mesmo PNG e que o `test_freeze_corresponde_ao_fonte` valida contra o fonte.
