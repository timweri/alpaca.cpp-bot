import asyncio
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import ContinueHandling
import os
import sys
from interface import AlpacaCppInterface
import time
import traceback
load_dotenv()

TELEGRAM_BOT_API_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')
ALPACA_CPP_EXEC_PATH = os.getenv('ALPACA_CPP_EXEC_PATH')
MODEL_PATH = os.getenv('MODEL_PATH')

def get_whitelist():
    whitelist = os.getenv('TELEGRAM_USERNAME_WHITELIST').split(',')
    whitelist = set(map(str.strip, whitelist))

    return whitelist

WHITELIST = get_whitelist()

async def main():
    bot = AsyncTeleBot(TELEGRAM_BOT_API_TOKEN, parse_mode=None) 

    alpaca_cpp_interface = AlpacaCppInterface(ALPACA_CPP_EXEC_PATH, MODEL_PATH)
    await alpaca_cpp_interface.start()

    @bot.message_handler(func=lambda m: True)
    async def log_message(message):
        print(f'Received a message from {message.from_user.username}')
        return ContinueHandling()

    @bot.message_handler(func=lambda m: True)
    async def whitelist_check(message):
        if len(WHITELIST) == 0 or message.from_user.username in WHITELIST:
            return ContinueHandling()
        print(f'{message.from_user.username} not in whitelist')

    @bot.message_handler(commands=['restart'])
    async def send_restart(message):
        await alpaca_cpp_interface.restart()
        await bot.reply_to(message, "I just restarted the alpaca.cpp instance.")

    @bot.message_handler(commands=['kill'])
    async def send_restart(message):
        if alpaca_cpp_interface.state == AlpacaCppInterface.State.ACTIVE:
            await alpaca_cpp_interface.terminate()
            await bot.reply_to(message, "I just killed the alpaca.cpp instance.")
        else:
            await bot.reply_to(message, "The alpaca.cpp instance is already inactive.")

    @bot.message_handler(commands=['state'])
    async def send_state(message):
        if alpaca_cpp_interface.state == AlpacaCppInterface.State.ACTIVE:
            await bot.reply_to(message, "The alpaca.cpp instance is active.")
        else:
            await bot.reply_to(message, "The alpaca.cpp instance is inactive.")

    @bot.message_handler(commands=['start'])
    async def send_welcome(message):
        await bot.reply_to(message, "Howdy, how are you doing? I am a bootleg alpaca.cpp bot. Please enter your prompt and don't expect much.")

    @bot.message_handler(commands=['help'])
    async def send_help(message):
        await bot.reply_to(message, '''Here are the available commands:
/start start the AlpacaCpp instance if inactive
/restart restart the AlpacaCpp instance
/state check if the AlpacaCpp instance is alive
/kill kill the AlpacaCpp instance

Chat normally to talk to the AlpacaCpp instance if active.''')

    @bot.message_handler(func=lambda m: True)
    async def echo_all(message):
        if alpaca_cpp_interface.state != AlpacaCppInterface.State.ACTIVE:
            await bot.reply_to(message, "The alpaca.cpp instance is currently inactive.")
            return

        if alpaca_cpp_interface.ready_for_prompt:
            try:
                if not await alpaca_cpp_interface.write(message.text):
                    await bot.reply_to(message, "Failed to process prompt.")
                    return

                await bot.send_chat_action(message.chat.id, 'typing', timeout=60)
                await bot.reply_to(message, await alpaca_cpp_interface.read())
            except Exception as e:
                traceback.print_exc()
                await bot.reply_to(message, "There's an unexpected error: " + str(e))
        else:
            await bot.reply_to(message, "I'm still generating answer for the previous prompt. I'll ignore this prompt.")

    await bot.polling()


if __name__ == "__main__":
    asyncio.run(main())
