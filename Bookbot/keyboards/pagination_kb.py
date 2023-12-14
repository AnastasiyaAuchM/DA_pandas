from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexiconn.lexicon import LEXICON


# The function that generates a keyboard for a book page
def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    # Initializing the builder
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Add a row with buttons to the builder
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons])
    # Return an inline-keyboard object
    return kb_builder.as_markup()
