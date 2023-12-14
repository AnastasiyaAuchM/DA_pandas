from copy import deepcopy

from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message
from filterss.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from database.database import user_dict_template, users_db
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from database.sqlite3 import db_start, create_profile, edit_page, edit_bookmarks                                   
from keyboards.pagination_kb import create_pagination_keyboard
from lexiconn.lexicon import LEXICON
from services.file_handling import book


router = Router()

    
# This handler will be triggered by the command "/start" -
# add the user to the database if he was not there yet
# and send him a welcome message
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=(f'Привет, {message.from_user.full_name}')+LEXICON['/start'])
    await db_start()
    await create_profile(user_id=message.from_user.id)
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


# This handler will trigger the command "/help"
#  and send the user a message with a list of available commands 
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])
    
    
# This handler will trigger the command "/beginning"
# and send the user the first page of the book with pagination buttons
@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
		    
    try:
        users_db[message.from_user.id]['page'] = 1
        text = book[users_db[message.from_user.id]['page']]
        await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[message.from_user.id]["page"]}/{len(book)}',
                    'forward'))
        await edit_page(page=users_db[message.from_user.id]['page'],
              user_id=message.from_user.id)
    except KeyError:
        await message.reply('Так не получается начать😔\nНаберите, пожалуйста, /start.')


# This handler will trigger the command "/continue"
# and send the user the page of the book on which the user stopped 
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    try:
        text = book[users_db[message.from_user.id]['page']]
        await message.answer(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[message.from_user.id]["page"]}/{len(book)}',
                    'forward'))
        await edit_bookmarks(bookmark, user_id=message.from_user.id)
    except KeyError:
        await message.reply('Не получается продолжить😢\nТолько /start.')


# This handler will trigger the command "/bookmarks"
# and send the user a list of saved bookmarks,
# if there are any or a message that there are no bookmarks
@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *users_db[message.from_user.id]["bookmarks"]))
        await edit_bookmarks(bookmark=users_db[message.from_user.id]['bookmarks'],
              user_id=message.from_user.id)
    else:
        await message.answer(text=LEXICON['no_bookmarks'])        
    

# This handler will be triggered by pressing the inline-button 'forward'
@router.callback_query(Text(text='forward'))
async def process_forward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
    await callback.answer()
    await edit_page(page=users_db[callback.from_user.id]['page'],
           user_id=callback.from_user.id)


# This handler will be triggered by pressing the inline-button 'backward'
@router.callback_query(Text(text='backward'))
async def process_backward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
    await callback.answer()
    await edit_page(page=users_db[callback.from_user.id]['page'],
          user_id=callback.from_user.id)


# This handler will be triggered when the inline-button with the current page number
# is pressed and add the current page to bookmarks
@router.callback_query(lambda x: '/' in x.data 
		and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page'])
    await callback.answer('Страница добавлена в закладки!')
    bookmark=list(users_db[callback.from_user.id]['bookmarks'])
    await edit_bookmarks(bookmark, user_id=callback.from_user.id)


# This handler will be triggered when the inline-button with a bookmark 
# is pressed from the bookmarks list
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward'))
    await callback.answer()


# This handler will be triggered when the inline-button "edit" is pressed
# under the bookmarks list
@router.callback_query(Text(text='edit_bookmarks'))
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
                text=LEXICON[callback.data],
                reply_markup=create_edit_keyboard(
                                *users_db[callback.from_user.id]["bookmarks"]))
    await callback.answer()


# This handler will be triggered when the inline-button "cancel" is pressed
# while working with the bookmarks list (view and edit)
@router.callback_query(Text(text='cancel'))
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


# This handler will be triggered when the inline button 
# with a bookmark from the list of bookmarks to delete is pressed
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(
                                                    int(callback.data[:-3]))
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
                    text=LEXICON['/bookmarks'],
                    reply_markup=create_edit_keyboard(
                            *users_db[callback.from_user.id]["bookmarks"]))
          
        await edit_bookmarks(bookmark=users_db[callback.from_user.id]['bookmarks'],
                user_id=callback.from_user.id)
        global bookmark
        bookmark=list(users_db[callback.from_user.id]['bookmarks'])
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
        bookmark=[]
        await edit_bookmarks(bookmark, user_id=callback.from_user.id)
    await callback.answer()
