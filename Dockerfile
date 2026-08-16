FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ARG QUARTO_VERSION=1.9.38
ARG TARGETARCH

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=pt_BR.UTF-8 \
    LC_ALL=pt_BR.UTF-8 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    QUARTO_PYTHON=/opt/venv/bin/python \
    MPLBACKEND=Agg

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl git locales \
    && sed -i '/^# *pt_BR.UTF-8/s/^# *//' /etc/locale.gen \
    && locale-gen \
    && curl -fsSL -o /tmp/quarto.deb \
        "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${TARGETARCH}.deb" \
    && apt-get install -y --no-install-recommends /tmp/quarto.deb \
    && rm -f /tmp/quarto.deb \
    && rm -rf /var/lib/apt/lists/*

# Um shell de login recarrega /etc/profile, que reescreve o PATH e descarta o
# ENV PATH acima — deixando `python` apontar para o interpretador do sistema em
# vez do venv. Isto garante o venv também em `bash -l` e `docker exec -it`.
RUN echo 'export PATH="/opt/venv/bin:$PATH"' > /etc/profile.d/venv.sh

WORKDIR /livro

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-cache

# Determinismo do hash de strings. Sem isto, a ordem de iteração de um `set`
# varia a cada processo — e `scratch/naive_bayes.py:113` tem, no nível do módulo,
# um `assert` de igualdade EXATA de float sobre uma soma que percorre um Set[str].
# Soma de ponto flutuante não é associativa, então a ordem muda o último bit e o
# assert falha. Medido neste container: 2 de 15 sementes falham no import; com
# PYTHONHASHSEED=0, 15 de 15 passam.
#
# A correção fica AQUI, e não em scratch/, porque aquele pacote é vendorizado
# literalmente e nunca editado. Isto é propriedade do ambiente, e combina com a
# postura do livro — semente explícita em todo chunk estocástico.
#
# Fica depois do `uv sync` de propósito: assim mexer nesta linha não invalida as
# camadas caras de apt-get, Quarto e dependências.
ENV PYTHONHASHSEED=0

EXPOSE 4201

CMD ["quarto", "preview", "--host", "0.0.0.0", "--port", "4201", "--no-browser"]
