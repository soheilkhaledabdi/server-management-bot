import os
import subprocess
from Users import Users
from Monitoring import Monitoring
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# load data for file .env
load_dotenv()


bot = Client(
    os.getenv("BOT_NAME")
    , api_id=os.getenv("API_ID")
    , api_hash=os.getenv('API_HASH')
    , bot_token=os.getenv("BOT_TOKEN"))

# start message and button

START_MESSAGE = "Choose your operation"
START_MESSAGE_BUTTON = [
    [
        InlineKeyboardButton('Monitoring Server', callback_data="monitoring_server")
    ]
]

#  all pages

PAGE1_TEXT = "Select the Server Monitoring operation"

PAGE1_BUTTON = [
    [
        InlineKeyboardButton('Disk Usage', callback_data="disk_usage"),
        InlineKeyboardButton('CPU and RAM Usage', callback_data="cpu_and_ram_usage")
    ]
    ,
    [
        InlineKeyboardButton('Uptime Server', callback_data="uptime_server"),
        InlineKeyboardButton('Server Description', callback_data="server_description")
    ]
]




@bot.on_message(filters.command(['start', 'help']) & filters.private)
def start(bot, message):
    text = START_MESSAGE
    reply_markup = InlineKeyboardMarkup(START_MESSAGE_BUTTON)
    message.reply(
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=True)


monitoring = Monitoring()

@bot.on_callback_query()
def callback_query(client, callbackQuery):
    # send disk usage
    if callbackQuery.data == "monitoring_server":
        callbackQuery.edit_message_text(
            PAGE1_TEXT,
            reply_markup=InlineKeyboardMarkup(PAGE1_BUTTON)
        )
    if callbackQuery.data == "reboot":
        bot.send_message(callbackQuery.from_user.id, "rebooted")
        os.system('shutdown -r now')
    if callbackQuery.data == "update":
        update_cmd = "apt update"
        subprocess.run(update_cmd.split())

        upgrade_cmd = "apt upgrade -y"
        subprocess.run(upgrade_cmd.split())
        bot.send_message(callbackQuery.from_user.id, "server updated")
    if callbackQuery.data == "disk_usage":
        callbackQuery.answer(
            monitoring.DiskUsage(),
            show_alert=True
        )
        # send cpu and ram usage data to bot
    elif callbackQuery.data == "cpu_and_ram_usage":
        callbackQuery.answer(
            monitoring.CPUANDRAM(),
            show_alert=True
        )
    elif callbackQuery.data == "uptime_server":
        callbackQuery.answer(
            monitoring.uptime(),
            show_alert=True
        )
    elif callbackQuery.data == "server_description":
        callbackQuery.answer(
            monitoring.get_info_server(),
            show_alert=True
        )


print("bot started")
bot.run()