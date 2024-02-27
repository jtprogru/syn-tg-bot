import logging
import os
import re
from distutils.util import strtobool
import random

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("TG_BOT_TOKEN", default=None)
DEBUG = bool(strtobool(os.getenv("DEBUG", default="False")))

if (TOKEN is None) or (TOKEN == ""):
    raise ValueError("TG_BOT_TOKEN is not set")

config = dict()

if DEBUG:
    config["log_level"] = logging.DEBUG
else:
    config["log_level"] = logging.INFO

LOG_FORMAT = "%(asctime)s [%(threadName)-16s] %(filename)27s:%(lineno)-4d %(levelname)7s| %(message)s"

logging.basicConfig(
    format=LOG_FORMAT,
    level=config["log_level"],
)

logger = logging.getLogger(__name__)


# Глобальные переменные для управления инвентарем
inventory = []


async def start_game(update, context):
    """Начинает игру."""
    story = "Вы стоите у входа в замок. Перед вами три двери: левая, центральная и правая. Куда вы пойдете?"
    options = [
        ("Пойти в левую дверь", "left_door"),
        ("Пойти в центральную дверь", "center_door"),
        ("Пойти в правую дверь", "right_door"),
    ]
    global inventory
    inventory = []
    await _present_options(update, context, story, options)


async def handle_choice(update, context):
    """Обрабатывает выбор игрока."""
    query = update.callback_query
    choice = query.data

    if choice == "left_door":
        story, item = _explore_left_door()
    elif choice == "center_door":
        story, item = _explore_center_door()
    elif choice == "right_door":
        story, item = _explore_right_door()
    else:
        story, item = "Произошла ошибка. Конец игры.", None

    if item:
        _manage_inventory(item)
        story += f"\nВ вашем рюкзаке теперь: {', '.join(inventory)}."

    await query.message.reply_text(story)


def _manage_inventory(item):
    """Управляет инвентарем игрока."""
    if item and len(inventory) < 2:
        inventory.append(item)
    elif item:
        # Логика замены предмета, если в инвентаре нет места
        inventory[0] = item  # Пример замены первого предмета


def _explore_left_door():
    """Исследует левую дверь."""
    outcomes = [
        ("Вы нашли факел на стене и взяли его с собой.", "факел"),
        ("В комнате был ключ, вы взяли его.", "ключ"),
        ("Ловушка! Комната заполнилась водой. Конец игры.", None),
    ]
    return random.choice(outcomes)


def _explore_center_door():
    """Исследует центральную дверь."""
    outcomes = [
        ("Вы нашли меч, висящий на стене!", "меч"),
        ("Вы встретили хранителя замка! Бой неизбежен.", None),
        ("Вы нашли затерянный артефакт! Победа!", None),
    ]
    return random.choice(outcomes)


def _explore_right_door():
    """Исследует правую дверь."""
    outcomes = [
        ("Вы нашли щит, leaning against the wall!", "щит"),
        ("Пустая комната. Возвращайтесь.", None),
        ("Вы активировали ловушку и были поражены стрелами. Конец игры.", None),
    ]
    return random.choice(outcomes)


async def _present_options(
    update: Update, context: ContextTypes.DEFAULT_TYPE, story: str, options: list
):
    """Presents options to the player."""
    buttons = [
        InlineKeyboardButton(text=text, callback_data=data) for text, data in options
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))
    await update.message.reply_text(story, reply_markup=reply_markup)


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    """Builds a menu from the provided buttons."""
    menu = [buttons[i : i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start_game))
    application.add_handler(CallbackQueryHandler(handle_choice))
    application.run_polling()


if __name__ == "__main__":
    main()
