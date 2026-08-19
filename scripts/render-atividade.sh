#!/usr/bin/env bash
# Renderiza uma atividade em duas versões: a do aluno e o gabarito.
#
# A fonte é um único .qmd, com as respostas dentro de blocos
# `::: {.content-visible when-meta="gabarito"}`. Duas passadas do Quarto sobre
# o mesmo arquivo produzem os dois PDFs — o do aluno simplesmente não contém as
# respostas no arquivo gerado, não é questão de estar escondido.
#
# Formato de saída: **typst**, não LaTeX. O Quarto já traz o Typst embutido, e
# o container deste livro não tem TeX instalado; usar PDF via LaTeX exigiria
# subir um TinyTeX inteiro na imagem só para gerar duas listas por semestre.
#
# NÃO use `quarto render --output`: o caminho é resolvido em relação ao arquivo
# de entrada e o PDF acaba fora de `atividades/`. Além disso, a segunda passada
# remove o PDF da primeira. Por isso cada passada renderiza com o nome padrão e
# o script move o resultado logo em seguida.
set -euo pipefail

FONTE="${1:?uso: render-atividade.sh atividades/lista-01-revisao.qmd}"
DIR=$(dirname "$FONTE")
BASE=$(basename "$FONTE" .qmd)
RUN="docker compose run --rm --no-deps livro"

# A versão do aluno vai para `publico/`, que é o diretório servido no site.
# O gabarito fica um nível acima, fora do que o `project.resources` publica.
# A separação é de diretório, e não de nome de arquivo, porque um dia alguém
# vai errar o nome — e aí o teste de invariante pega, mas o diretório errado
# nunca chega a existir.
mkdir -p "$DIR/publico"

echo "→ versão do aluno  ($DIR/publico/)"
$RUN quarto render "$FONTE" --to typst --quiet
mv "$DIR/$BASE.pdf" "$DIR/publico/$BASE.pdf"

echo "→ gabarito         ($DIR/, fora do site)"
$RUN quarto render "$FONTE" --to typst -M gabarito:true --quiet
mv "$DIR/$BASE.pdf" "$DIR/$BASE-gabarito.pdf"

rm -rf "$DIR/.quarto" "$DIR/$BASE.typ"
echo
ls -lh "$DIR/publico/$BASE.pdf" "$DIR/$BASE-gabarito.pdf" | awk '{print "  "$5"\t"$9}'
