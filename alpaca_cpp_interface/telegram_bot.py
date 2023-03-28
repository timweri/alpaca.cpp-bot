from dotenv import load_dotenv
import telebot
import os
from interface import AlpacaCppInterface
import time
load_dotenv()

TELEGRAM_BOT_API_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')
ALPACA_CPP_EXEC_PATH = os.getenv('ALPACA_CPP_EXEC_PATH')
MODEL_PATH = os.getenv('MODEL_PATH')

if __name__ == "__main__":
    bot = telebot.TeleBot(TELEGRAM_BOT_API_TOKEN, parse_mode=None) 

    alpaca_cpp_interface = AlpacaCppInterface(ALPACA_CPP_EXEC_PATH, MODEL_PATH)

    @bot.message_handler(commands=['restart'])
    def send_restart(message):
        alpaca_cpp_interface.restart()
        bot.reply_to(message, "I just restarted the alpaca.cpp instance.")

    @bot.message_handler(commands=['kill'])
    def send_restart(message):
        if alpaca_cpp_interface.state == AlpacaCppInterface.State.ACTIVE:
            alpaca_cpp_interface.terminate()
            bot.reply_to(message, "I just killed the alpaca.cpp instance.")
        else:
            bot.reply_to(message, "The alpaca.cpp instance is already inactive.")

    @bot.message_handler(commands=['state'])
    def send_state(message):
        if alpaca_cpp_interface.state == AlpacaCppInterface.State.ACTIVE:
            bot.reply_to(message, "The alpaca.cpp instance is active.")
        else:
            bot.reply_to(message, "The alpaca.cpp instance is inactive.")

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Howdy, how are you doing? I am a bootleg alpaca.cpp bot. Please enter your prompt and don't expect much.")

    @bot.message_handler(commands=['help'])
    def send_help(message):
        bot.reply_to(message, "I haven't got time to fill this up yet.")

    @bot.message_handler(func=lambda m: True)
    def echo_all(message):
        if alpaca_cpp_interface.state != AlpacaCppInterface.State.ACTIVE:
            bot.reply_to(message, "The alpaca.cpp instance is currently inactive.")
            return

        if alpaca_cpp_interface.ready_for_prompt:
            try:
                if not alpaca_cpp_interface.write(message.text):
                    bot.reply_to(message, "Failed to process prompt.")
                    return

                bot.reply_to(message, alpaca_cpp_interface.read())
            except Exception as e:
                bot.reply_to(message, "There's an unexpected error: " + str(e))
        else:
            bot.reply_to(message, "I'm still generating answer for the previous prompt. I'll ignore this prompt.")

    bot.infinity_polling()
