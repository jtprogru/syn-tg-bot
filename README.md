# syn-tg-bot

Простой echo-bot.

## Run locally

Для запуска необходимо:

1. Создать файл `.env` в корне проекта;
2. Привести файл `.env` к стандартному виду.

### Default content for `.env` file

Пример в [`.env.example`](.env.example)

```ini
TG_BOT_TOKEN=<bot_token_from_BotFather>
DEBUG=False
METRICS_PORT=8000
```

Где:
- `TG_BOT_TOKEN` – Токен бота, полученный от [@BotFather](https://t.me/BotFather), если значение не определено, то бот не запустится (default: `None`);
- `DEBUG` – Включить/Выключить режим подробного логирования (default: `False`);
- `METRICS_PORT` – Порт, на котором можно посмотреть метрики (default: `8000`).

## Contacts

## License

[WTFPL](LICENSE)
