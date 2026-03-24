import asyncio
from aiogram import Bot, Dispatcher, F


from application.handlers import router

token = ""
with open("token.txt", "r") as file:token=file.read() 

async def main():
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    
    
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")