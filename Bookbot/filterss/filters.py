from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

# The filter that the bookmark consists of numbers
class IsDigitCallbackData(BaseFilter):
	async def __call__(self, callback: CallbackQuery) -> bool:
		return callback.data.isdigit()

# The filter if the bookmark needs to be deleted
class IsDelBookmarkCallbackData(BaseFilter):
	async def __call__(self, callback: CallbackQuery) -> bool:
		return callback.data.endswith('del') and callback.data[:-3].isdigit()
