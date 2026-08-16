#!/usr/bin/env bash
#
# Renderiza o livro com duas proteções que o `quarto render` sozinho não tem.
#
# ---------------------------------------------------------------------------
# PROTEÇÃO 1 — um render por vez (lock)
#
# Dois `quarto render` simultâneos sobre o mesmo `_freeze/` corrompem o cache:
# um grava a saída congelada de um chunk enquanto o outro lê o índice. Este
# livro é escrito por vários agentes em paralelo, então isso não é hipótese.
#
# O lock é um `mkdir`, atômico em qualquer POSIX. `flock` não existe no macOS
# de fábrica — foi por isso que não foi usado.
#
# ---------------------------------------------------------------------------
# PROTEÇÃO 2 — detecta o `_freeze` envenenado por edição concorrente
#
# Esta é a falha SILENCIOSA que motivou o script, e ela já publicou três seções
# desatualizadas sem uma única mensagem de erro.
#
# O `freeze: auto` do Quarto guarda, para cada `.qmd`, o par (hash do fonte,
# markdown executado). Se um agente EDITA o arquivo enquanto o render roda, o
# Quarto executa a versão velha e grava esse resultado velho com o hash da
# versão NOVA. Nas rodadas seguintes o hash bate, o cache é considerado válido,
# e o arquivo nunca mais reexecuta sozinho. O livro publica conteúdo antigo
# indefinidamente, e nada na tela denuncia.
#
# Não dá para detectar isso comparando hashes — o hash bate; é justamente esse
# o problema. O que se pode detectar é a CAUSA: um `.qmd` cuja data de
# modificação mudou entre o início e o fim do render. Esses, e só esses, têm o
# cache suspeito. O script apaga o `_freeze` deles e renderiza de novo.
#
# ---------------------------------------------------------------------------
set -uo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RAIZ"

LOCK=".render-lock"
RUN=(docker compose run --rm --no-deps livro)
MAX_TENTATIVAS=6   # contra a corrida do bind mount do Docker no macOS
MAX_RODADAS=3      # contra o freeze envenenado por edição concorrente

# --- lock -------------------------------------------------------------------
espera=0
while ! mkdir "$LOCK" 2>/dev/null; do
  if [ "$espera" -eq 0 ]; then
    echo "outro render em andamento neste repositório; aguardando a vez..."
  fi
  espera=$((espera + 1))
  if [ "$espera" -gt 180 ]; then
    echo "lock preso há mais de 30 min (agente morto?); removendo e seguindo."
    rm -rf "$LOCK"
  fi
  sleep 10
done
trap 'rm -rf "$LOCK"' EXIT INT TERM

# --- fotografa as datas de modificação de todos os .qmd ---------------------
fotografar() {
  find content -name '*.qmd' -exec stat -f '%m %N' {} + 2>/dev/null \
    || find content -name '*.qmd' -exec stat -c '%Y %n' {} +   # GNU (CI Linux)
}

for rodada in $(seq 1 "$MAX_RODADAS"); do
  antes="$(fotografar)"

  # --- render, com retentativa contra a corrida do bind mount ---------------
  ok=nao
  for i in $(seq 1 "$MAX_TENTATIVAS"); do
    # O Quarto cria `*_files` e `.html` durante o render e os apaga no fim. Se
    # o render abortou antes, esse lixo trava o render seguinte.
    find content -name '*_files' -type d -exec rm -rf {} + 2>/dev/null || true
    find content -name '*.html' -type f -delete 2>/dev/null || true

    if "${RUN[@]}" quarto render; then
      echo "render OK (tentativa $i)"
      ok=sim
      break
    fi
    echo "--- tentativa $i abortou (corrida do bind mount); limpando e repetindo ---"
  done

  if [ "$ok" = nao ]; then
    echo "render falhou em $MAX_TENTATIVAS tentativas — isto provavelmente NÃO é a corrida do bind mount."
    echo "Rode 'docker compose run --rm --no-deps livro quarto render' direto para ver o erro real."
    exit 1
  fi

  # --- quem mudou enquanto o render rodava? --------------------------------
  depois="$(fotografar)"
  mexidos="$(comm -13 <(echo "$antes" | sort) <(echo "$depois" | sort) | awk '{print $2}')"

  if [ -z "$mexidos" ]; then
    exit 0   # ninguém editou durante o render: o _freeze é confiável
  fi

  echo
  echo "=== ATENÇÃO: estes .qmd foram editados DURANTE o render ==="
  echo "$mexidos" | sed 's/^/    /'
  echo "O _freeze deles guarda o hash novo com a saída velha, e nunca mais"
  echo "reexecutaria sozinho. Apagando o cache deles e renderizando de novo"
  echo "(rodada $rodada de $MAX_RODADAS)."
  echo

  while IFS= read -r qmd; do
    [ -n "$qmd" ] || continue
    # content/cap10/05-usando-o-modelo.qmd -> _freeze/content/cap10/05-usando-o-modelo
    rm -rf "_freeze/${qmd%.qmd}"
  done <<< "$mexidos"
done

cat <<'AVISO'

╔══════════════════════════════════════════════════════════════════════════╗
║  AVISO — houve edição concorrente em todas as rodadas de render.         ║
╚══════════════════════════════════════════════════════════════════════════╝

O livro RENDERIZOU e o `_book/` está no lugar: isto não é uma falha de render,
e não há nada de errado com o seu conteúdo. Não rode `make clean`.

O que aconteceu é que outro agente ficou editando `.qmd` enquanto este render
rodava, então o `_freeze` das seções listadas acima pode estar guardando saída
velha com hash novo. As demais páginas do livro estão confiáveis.

Quando ninguém mais estiver editando, rode para cada capítulo afetado:

    make refresh CAP=NN

AVISO
exit 0
