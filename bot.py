import logging
import argparse
from aiogram import Bot
from handlers import handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Run the Telegram bot.")
parser.add_argument('--token', type=str,
                    help='The token of the Telegram bot.', required=True)
args = parser.parse_args()

bot = Bot(token=args.token)

if __name__ == '__main__':
    handlers.dp.run_polling(bot)
