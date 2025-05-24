# Artifex AI Chatbot Telegram Bot

----
- [Обзор](#overview)
- [Локальный запуск](#local_run)
- [Использование](#usage)
----
<h2 id="overview">Обзор</h2>
Telegram бот
TODO


<h2 id="local_run">Локальный запуск</h2>

- Запустить с помощью Docker Compose - postgres и pgadmin
```bash
docker compose -f docker-compose.local.yaml up --build
```
- Добавить src в PYTHONPATH
```bash
export PYTHONPATH="./src:$PYTHONPATH"
```
- Установить зависимости от poetry и создать виртуальное окружение
```bash
poetry install
poetry shell
```
- Запустить бота с помощью poetry
```bash
poetry run python src/main.py
```

<h2 id="usage">Использование</h2>
TODO

<h2 id="usage">TODO</h2>
