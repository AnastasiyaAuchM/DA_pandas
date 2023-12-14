from aiogram import Router
from aiogram.types import Message

router: Router = Router()


# This handler is for any user messages not provided for this bot
@router.message()
async def wild_west(message: Message):
    await message.answer('Это ни на что не похоже!')
