FROM python:3.13-slim

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml poetry.lock ./

# Отключаем проверку README.md и пакетный режим
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

RUN make db_migration && make db_push

COPY . .

EXPOSE 8000

CMD ["make", "start"]