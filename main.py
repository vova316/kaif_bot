import asyncio
from aiogram import Bot, Dispatcher , executor

bot = Bot('1265769369:AAHLQMOAuEztBsioqwmtJbjRpby_47JAi2A', parse_mode="HTML")
dp = Dispatcher(bot)

if __name__ == '__main__':
	from hend import dp
	executor.start_polling(dp)