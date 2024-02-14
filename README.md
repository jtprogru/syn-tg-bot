# syn-tg-bot

Домашние задания по разработке Telegram-ботов на Python 3.11.

## Run locally

Для запуска необходимо:
- перейти в директорию с домашним заданием;
- создать файл `.env` этой директории;
- выполнить в директории с домашним заданием команду `docker compose up --build`;

Для упрощения жизни используется [Taskfile](https://taskfile.dev).

### Default content for `.env` file

Пример в [`.env.example`](.env.example)

```ini
TG_BOT_TOKEN=<bot_token_from_BotFather>
DEBUG=False
METRICS_PORT=8000
```

Где:
- `TG_BOT_TOKEN` – Токен бота, полученный от [@BotFather](https://t.me/BotFather), если значение не определено, то бот не запустится (default: `None`);
- `DEBUG` – Включить/выключить режим подробного логирования (default: `False`);
- `METRICS_PORT` – Порт, на котором можно посмотреть метрики (default: `8000`).

## Home works

Список домашних заданий:

- Домашнее задание 1 – [hw01](hw01/README.md)
- Домашнее задание 2 – [hw02](hw02/README.md)
- Домашнее задание 3 – [hw03](hw03/README.md)
- Домашнее задание 4 – [hw04](hw04/README.md)

## License

[WTFPL](LICENSE)

