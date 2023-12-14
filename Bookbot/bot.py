import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.main_menu import set_main_menu
from database.sqlite3 import db_start

async def on_startup(_):
    await db_start()
    print('База данных активна')

# Initializing the logger
logger = logging.getLogger(__name__)

    
    
# The function of configuring
async def main():
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Output information about the start of the bot to the console
    logger.info('Starting bot')

    # Load the config into a variable
    config: Config = load_config()

    # Initialize the bot and the dispatcher
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Setting up the main menu
    await set_main_menu(bot)

    # Register routers in the dispatcher
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Skip accumulated updates and start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), on_startup=on_startup)
    


if __name__ == '__main__':
    asyncio.run(main())
