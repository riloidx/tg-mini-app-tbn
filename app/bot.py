import asyncio
import logging
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Проверяем наличие токена перед созданием бота
if not settings.telegram_bot_token or settings.telegram_bot_token == "your_telegram_bot_token_here":
    logger.warning("Telegram bot token не настроен. Бот не будет запущен.")
    logger.info("Для запуска бота установите переменную окружения TELEGRAM_BOT_TOKEN")
    bot = None
    dp = None
else:
    bot = Bot(token=settings.telegram_bot_token)
    dp = Dispatcher()


if dp is not None:
    @dp.message(CommandStart())
    async def start_handler(message: types.Message):
        webapp = WebAppInfo(url="https://your-webapp-url.com")
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Пройти тест", web_app=webapp)]
            ]
        )
        
        await message.answer(
            "Добро пожаловать! Нажмите кнопку ниже, чтобы пройти тест.",
            reply_markup=keyboard
        )


async def main():
    if bot is None or dp is None:
        logger.info("Бот не запущен из-за отсутствия токена")
        return
    
    logger.info("Starting bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())