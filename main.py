import os
import logging
import time

import telegram
import subprocess
from picamera import PiCamera
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

load_dotenv()
TOKEN = os.environ.get("TOKEN")
USER_ID = os.environ.get("USER_ID")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Send out ip address
msg = subprocess.check_output("hostname -I", shell=True).decode('ascii')
bot.send_message(chat_id=USER_ID, text=f"I'm up and running at {msg}")

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def ip(update, context):
    msg = subprocess.check_output("hostname -I", shell=True).decode('ascii')
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def temp(update, context):
    msg = subprocess.check_output("vcgencmd measure_temp", shell=True).decode("ascii")
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

def pic(update, context):
    with PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture('pic.jpg', resize=(640, 480))
    context.bot.send_photo(USER_ID, open('~/pic.jpg', 'rb'))

def shutdown(update, context):
    subprocess.run("sudo shutdown now")

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

start_handler = CommandHandler('start', start)
ip_handler = CommandHandler('ip', ip)
temp_handler = CommandHandler('temp', temp)
pic_handler = CommandHandler('pic', pic)
shutdown_handler = CommandHandler('shutdown', shutdown)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(ip_handler)
dispatcher.add_handler(temp_handler)
dispatcher.add_handler(pic_handler)
dispatcher.add_handler(shutdown_handler)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()
