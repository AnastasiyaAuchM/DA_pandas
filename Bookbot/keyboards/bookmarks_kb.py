from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexiconn.lexicon import LEXICON
from services.file_handling import book


def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
    # Create a keyboard object
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Fill the keyboard with bookmark buttons in ascending
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{button} - {book[button][:100]}',
            callback_data=str(button)))
    # Add two "Edit" and "Cancel" buttons to the keyboard at the end
    kb_builder.row(InlineKeyboardButton(
                        text=LEXICON['edit_bookmarks_button'],
                        callback_data='edit_bookmarks'),
                   InlineKeyboardButton(
                        text=LEXICON['cancel'],
                        callback_data='cancel'),
                   width=2)
    return kb_builder.as_markup()


def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    # Create a keyboard object
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Fill the keyboard with bookmark buttons in ascending
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{LEXICON["del"]} {button} - {book[button][:100]}',
            callback_data=f'{button}del'))
    # Add a button "Cancel" to the keyboard at the end
    kb_builder.row(InlineKeyboardButton(
                        text=LEXICON['cancel'],
                        callback_data='cancel'))
    return kb_builder.as_markup()
