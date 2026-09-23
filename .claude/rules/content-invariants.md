---
paths:
  - "content/**/*.qmd"
  - "_quarto.yml"
  - "styles.css"
  - "estilo-figuras.mplstyle"
  - "notebooks/**/*.ipynb"
---

# Invariantes de conteúdo (INV-1 a INV-14)

Regras numeradas e inegociáveis para o conteúdo deste livro. Críticos, revisores e auditores
citam o número ao apontar um problema ("viola INV-3") — e o campo `rule` de um `FINDING`
(ver `.claude/references/orchestration-schemas.md`) deve citar um destes invariantes, o
`CLAUDE.md`, a spec vigente (`docs/superpowers/specs/2026-09-10-estrutura-nova-islp-design.md`)
ou a `knowledge-base.md`. Cada invariante resume uma regra do `CLAUDE.md` ou da spec; em caso
de conflito, **o `CLAUDE.md` e a spec vencem**. Muitos deles já são travados por um teste em
`tests/test_estrutura.py` — o teste é citado quando existe.

Os capítulos 1 a 5 são da abordagem anterior (Grus) e ficam **fora** de INV-2, INV-7, INV-9 e
INV-10: não é defeito eles não citarem o ISLP nem usarem o estilo das figuras.

## Estrutura

- **INV-1: Registro no `_quarto.yml` e no `LIVRO`.** Todo `.qmd` novo em `content/` entra em `LIVRO` (`scripts/gerar-stubs.py`) e em `book.chapters`. Arquivo não listado não existe para o leitor. (`test_todo_qmd_esta_registrado_no_quarto_yml`)
- **INV-2: Callout de correspondência com o ISLP.** Toda seção dos caps. 7 a 16 abre com `::: {.callout-note}` "Esta seção corresponde à seção X.Y.Z de @james2023." — o número **do ISLP**, nunca o nosso. Quando a seção cobre mais de uma seção do ISLP, o plural é a forma certa: "Esta seção corresponde às seções 2.1 e 2.1.1 de @james2023." (caps. 7, 8 e 9 já usam). Os caps. 6 e 17 não têm correspondência e não trazem o callout. (`test_toda_secao_cita_o_islp`)
- **INV-3: Escopo da spec.** A ementa seção a seção é a da spec. Fica de fora: ISLP 7 (splines etc.), 11 (sobrevivência), 13 (testes múltiplos), 6.3.2 (PLS), 8.2.4 (BART), 10.3/10.5 (CNN/RNN). O `Boston` é substituído por California Housing, e o texto não comenta a substituição.
- **INV-4: Bibliografia única.** Toda citação resolve em `references.bib`; o ISLP é `@james2023`.

## Código

- **INV-5: Semente explícita, no gerador que sorteia.** `np.random.default_rng(<n>)` para o `numpy`, `random_state=<n>` para o `scikit-learn`. Semear um gerador e sortear de outro não fixa nada. Sorteio novo → número novo: toda afirmação da prosa que dependa do sorteio é recalculada.
- **INV-6: Caminhos a partir da raiz.** `pd.read_csv("dados/...")`, nunca `../../dados/...` (`execute-dir: project`). (`test_nenhum_qmd_usa_caminho_relativo_de_dados`)
- **INV-7: Biblioteca proibida em chunk que executa.** Nada de `statsmodels`, `torch`, pacote `ISLP`; `scipy` só nas exceções de `BIBLIOTECA_LIBERADA`, com motivo escrito. Dependência nova entra no `pyproject.toml` com teto de versão (minor para `0.x`). (`test_nenhum_chunk_executavel_usa_biblioteca_proibida`)
- **INV-8: Todo número da prosa sai da saída de um chunk.** A única exceção é aritmética sobre números impressos **na mesma seção**, nomeando os dois operandos. **Superlativo e comparação** ("o maior", "mais que o dobro", "nenhum passa de") não são aritmética: exigem o chunk que ordena, conta ou compara.
- **INV-9: Cada seção reconstrói o que herda.** Cada `.qmd` roda num kernel próprio: `import` se repete, e uma decisão sobre o dado tomada numa seção anterior ("preencher `andar` com zero") é refeita no chunk de setup da seguinte, sem reexplicar.
- **INV-10: Erro mostrado com `try/except`, nunca `#| error: true`.** A opção não é honrada pelos scripts de verificação. A mensagem é truncada antes de imprimir.

## Pedagogia e apresentação

- **INV-11: Toda seção dos caps. 6 a 17 tem figura, e todo chunk que desenha aplica `estilo-figuras.mplstyle`.** Figura carrega a ideia, não decora. Exceção só em `SECOES_SEM_FIGURA`, com motivo. (`test_toda_secao_tem_figura`, `test_todo_chunk_que_desenha_aplica_o_estilo`)
- **INV-12: Motivação antes da fórmula; no máximo dois blocos coloridos seguidos.** Toda definição é precedida por uma pergunta, um exemplo ou um dado. Callouts, `.conceito`, `.exemplo` e `.funcao` empilhados diluem a ênfase; o terceiro vira prosa.
- **INV-13: O texto é sobre o conteúdo, não sobre o material.** O foco é o conteúdo e a didática. Proibido na prosa de `content/` (o callout de correspondência é a única menção ao livro-fonte):
  - **história editorial** — mudança de abordagem, reescrita, versão anterior, o que o material "agora" usa; remissão a Bases 3 (`test_o_conteudo_nao_comenta_a_propria_escrita`);
  - **meta-texto sobre o ISLP** — comparar o material com o livro, dizer como o livro está organizado ("é essa pergunta que abre o ISLP"), o que os autores fizeram ou usaram, o que o material tem, não tem, instala ou deixa de fora e por quê ("…não está disponível fora do pacote `ISLP` do R, que este material não instala");
  - **pontes forçadas** — abertura que resume o fim da seção ou do capítulo anterior antes de chegar ao assunto ("A seção anterior fechou perguntando…", "O capítulo anterior fechou com `X` e `y` prontos…"). A seção abre pela pergunta, pelo dado ou pelo fenômeno. Remissão a outra seção só quando carrega conteúdo necessário ali. Teste: apagada a frase, o parágrafo continua de pé? Então era ponte.
- **INV-14: Nada secreto no HTML.** `.spoiler` é ofuscação. Gabaritos ficam em `atividades/` fora de `publico/`, nunca versionados (`**/*gabarito*` no `.gitignore`); o repositório é público. (`test_atividades.py`)
