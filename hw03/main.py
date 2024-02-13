"""
Synergy Telegram Bot
"""

import logging
import os
import random
import re
from distutils.util import strtobool

from prometheus_client import start_http_server, Summary, Counter
from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ApplicationBuilder,
    ContextTypes,
)

# Чтение токена из переменной окружения
TOKEN = os.getenv("TG_BOT_TOKEN", default=None)
DEBUG = bool(strtobool(os.getenv("DEBUG", default="False")))
METRICS_PORT = int(os.getenv("METRICS_PORT", default=8000))


if (TOKEN is None) or (TOKEN == ""):
    raise ValueError("TG_BOT_TOKEN is not set")

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary(
    "bot_request_processing_seconds", "Time spent processing request"
)
FAILURE_COUNTER = Counter("bot_failures", "Number of failures")
CANCELED_MSG_COUNTER = Counter("bot_canceled_messages", "Number of canceled messages")
STMT_COUNTER = Counter("bot_statements", "Number of statements executed", ["statement"])
COMMAND_CALL_COUNTER = Counter(
    "bot_command_calls", "Number of command calls", ["command"]
)

config = dict()

if DEBUG:
    config["log_level"] = logging.DEBUG
else:
    config["log_level"] = logging.INFO


# Настройка логирования
class SensitiveFormatter(logging.Formatter):
    """Formatter that removes sensitive information in urls."""

    @staticmethod
    def _filter(s):
        return re.sub(r"bot[0-9]{9,10}:[a-zA-Z0-9-]{35}", r"secret_token", s)

    def format(self, record):
        original = logging.Formatter.format(self, record)
        return self._filter(original)


LOG_FORMAT = "%(asctime)s [%(threadName)-16s] %(filename)27s:%(lineno)-4d %(levelname)7s| %(message)s"

logging.basicConfig(
    format=LOG_FORMAT,
    level=config["log_level"],
)

for handler in logging.root.handlers:
    handler.setFormatter(SensitiveFormatter(LOG_FORMAT))
logger = logging.getLogger(__name__)


@REQUEST_TIME.time()
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды start."""

    msg = (
        f"**Привет\!**\nЯ помогу вам рассылать сообщения\.\n\n"
        + f"\/ping \- проверка жизнеспособности\n"
        + f"\/help \- для получения справки"
    )

    await update.message.reply_markdown_v2(msg)
    logger.info(
        "start_command - access allowed for user with user_id: %s username: (@%s)",
        update.message.from_user.id,
        update.message.from_user.username,
    )
    COMMAND_CALL_COUNTER.labels("start_command").inc()


@REQUEST_TIME.time()
async def help_command(update: Update, context):
    """Обработка команды help."""

    msg = "<b>Пук! Среньк!</b>\n/ping - проверка жизнеспособности"
    await update.message.reply_html(msg)
    logger.info(
        "help_command - access allowed for user with user_id: %s username: (@%s)",
        update.message.from_user.id,
        update.message.from_user.username,
    )
    COMMAND_CALL_COUNTER.labels("help_command").inc()


@REQUEST_TIME.time()
async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды ping."""

    await update.message.reply_text("PONG")
    logger.info(
        "ping_command - access allowed for user with user_id: %s username: (@%s)",
        update.message.from_user.id,
        update.message.from_user.username,
    )
    COMMAND_CALL_COUNTER.labels("ping_command").inc()


@REQUEST_TIME.time()
async def create_poll_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Создает опрос из сообщения пользователя."""

    message_text = update.message.text
    lines = message_text.strip().split('\n')

    # Проверка на количество строк в сообщении
    if len(lines) < 3:
        await update.message.reply_text("Сообщение слишком короткое. Необходимо минимум 3 строки.")
        return
    elif len(lines) > 11:
        await update.message.reply_text("Сообщение слишком длинное. Максимум 11 строк.")
        return

    # Создание и отправка опроса
    question = lines[0]  # Вопрос
    options = lines[1:]  # Варианты ответов
    await context.bot.send_poll(update.effective_chat.id, question, options)



# Функции обработчики команд будут здесь
async def error(update, context):
    """Логируем ошибки, вызванные обновлениями."""

    FAILURE_COUNTER.inc()
    logger.error('Update "%s" caused error "%s"', update, context.error)


def main():
    # Start up the server to expose the metrics.
    start_http_server(METRICS_PORT)

    # Создаем бота
    application = ApplicationBuilder().token(TOKEN).build()
    logger.info("main - application created")

    # Регистрация обработчиков команд и ошибок будет здесь
    application.add_error_handler(error)
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), create_poll_handler)
    )
    logger.info("main - handlers added")

    application.run_polling()


if __name__ == "__main__":
    main()
