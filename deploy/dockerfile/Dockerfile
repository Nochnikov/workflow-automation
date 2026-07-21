FROM python:3.12-slim-bookworm

# uv берём готовым бинарником из официального образа (быстрее, чем pip install uv)
COPY --from=ghcr.io/astral-sh/uv:0.11.25 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/venv \
    PATH="/venv/bin:$PATH"

WORKDIR /app

# 1) Сначала только манифесты — слой с зависимостями кэшируется,
#    пока pyproject.toml/uv.lock не менялись.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# 2) копируем команду запуска
COPY deploy/scripts/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# 3) Затем сам код
COPY . .
RUN uv sync --frozen --no-dev

EXPOSE 8001

ENTRYPOINT ["/docker-entrypoint.sh"]
