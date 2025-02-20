<<<<<<< HEAD
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

=======
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

>>>>>>> d8a3317a0a70d13af2213931a89ea36727542756
CMD ["make", "start"]