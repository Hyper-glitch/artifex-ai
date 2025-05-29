from functools import lru_cache

from enums import CallbackData
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


@lru_cache(maxsize=1)
def create_action_buttons() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ Принять", callback_data=CallbackData.ACCEPT),
        InlineKeyboardButton("🔁 Перегенерировать", callback_data=CallbackData.REGENERATE),
    )
    return markup


@lru_cache(maxsize=1)
def create_rating_buttons() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=5)
    for num in range(1, 6):
        markup.add(InlineKeyboardButton(f"{num} ⭐", callback_data=f"rate_{num}"))

    return markup
