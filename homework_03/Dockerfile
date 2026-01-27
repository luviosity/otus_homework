# Команды по сборке образа и запуску контейнера написаны в Marefile.
# Можно запустить командой "make run" из папки homework_03
# Для Windows для начала нужно будет установить make


FROM astral/uv:python3.13-bookworm-slim

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app
# UV_COMPILE_BYTECODE=1 — после установки пакетов uv будет сразу компилировать .py файлы в байткод (.pyc),
# это обычно ускоряет запуск приложения в продакшене за счет более долгой установки.
# UV_LINK_MODE=copy — uv будет копировать файлы зависимостей, а не использовать симлинки,
# что делает окружение более изолированным и предсказуемым.
# UV_NO_DEV=1 — не устанавливать dev-зависимости,
# чтобы уменьшить размер финального образа и убрать лишние инструменты.
# UV_PYTHON_DOWNLOADS=0 — запретить uv скачивать интерпретатор Python;
# используется уже установленный системный Python
# PYTHONUNBUFFERED логи python в консоль

WORKDIR /app/homework_03

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-install-project

COPY app/ ./app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
