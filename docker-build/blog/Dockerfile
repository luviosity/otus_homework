FROM python:3.11-alpine

COPY --from=ghcr.io/astral-sh/uv:0.9.28 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-install-project --no-dev
ENV PATH="/app/.venv/bin:$PATH"

COPY docker-build/blog/entrypoint.sh /etc/entrypoint.sh
RUN chmod +x /etc/entrypoint.sh

COPY homework_04 ./

ENTRYPOINT ["/etc/entrypoint.sh"]