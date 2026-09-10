# Material morto — a abordagem do Grus

**Nada aqui é fonte para nada.** Não copie, não cite, não use como modelo de estilo, não conserte.

Este diretório guarda os capítulos 6 a 17 como estavam em 2026-09-10, quando a disciplina abandonou a abordagem *from scratch* do livro do Joel Grus. A decisão e as razões estão em `docs/superpowers/specs/2026-09-10-ruptura-com-o-grus-design.md`.

O que está aqui:

| Diretório | O quê |
|---|---|
| `content/cap06` a `cap17` | os doze capítulos, com os `.qmd` de cada seção |
| `notebooks/` | os notebooks de aula derivados deles |
| `scratch_np/` | o pacote em numpy, que existia só para esses capítulos |
| `planos/` | os planos da reescrita em numpy e da conversão para `pandas` |

Está fora do `_quarto.yml` e listado no `.quartoignore`, então o Quarto não o vê. A suíte de testes o ignora — os invariantes valem para `content/`, e este diretório não está lá.

Fica versionado só para consulta: se algum exemplo, dado ou explicação daqui for útil ao material novo, ele é **reescrito** a partir das fontes novas, não copiado.
