## Сервис: Worker

Worker асинхронно слушает очередь задач из `RabbitMQ`, вызывает `Triton Inference Server` для инференса, обновляет статус в `API` и отправляет результат в чат юзера с тг ботом.

### Создание пользователя для RMQ
```bash
rabbitmqctl add_user myuser mypassword
```

### Назначение прав
```bash
# Доступ ко всем ресурсам в виртуальном хосте "/"
rabbitmqctl set_permissions -p / myuser ".*" ".*" ".*"
```

### Переменные окружения
Создайте `.env` файл в корневой папке `worker`

`RABBITMQ_HOST=localhost` если локальная отладка, `RABBITMQ_HOST=rabbitmq` при запуске в контейнере.

```env
RABBITMQ_DEFAULT_USER=myuser
RABBITMQ_DEFAULT_PASS=mypassword
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_HEARTBEAT=30
RABBITMQ_QUEUE_NAME="gen-ai-tasks"

API_AUTH_TOKEN=
TG_BOT_TOKEN=

TRITON_MAX_CONCURRENCY=1
TRITON_CLIENT_URL=
```

### Масштабирование реализовано через
- `MODEL_INSTANCES` — число параллельных моделей, загружаемых в `Triton` (управляется в `content-generator`)
- `TRITON_MAX_CONCURRENCY` — максимальное количество одновременных запросов в Triton.

Увеличив число инстансов и настроив семафор, вы сможете обрабатывать больше запросов без потери производительности.
