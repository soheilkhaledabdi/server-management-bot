import os
from pyrogram import Client,filters,emoji
from pyrogram.types import ChatPermissions
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,CallbackQuery


# migrate_from_chat_id
bot = Client("monitoring server bot"
             ,api_id=29365133,api_hash="722d0eb612a789286c0ed9966c473ddf"
                ,bot_token="5873524421:AAHWQzlbGhhUdkiwhfanf9dK0SfC_NzYQQ8")




start_message = "Choose your operation"
start_message_button=[
    [
    InlineKeyboardButton('Disk Usage' , callback_data="disk_usage"),
    InlineKeyboardButton('CPU and RAM Usage' , callback_data="cpu_and_ram_usage")
    ]
    ,
    [
    InlineKeyboardButton('Uptime Server' , callback_data="uptime_server"),
    InlineKeyboardButton('Server Description',callback_data="server_description")
    ]
]



# command start and help
# filter with command,private,number id 

@bot.on_message(filters.command(['start' , 'help']) & filters.private)
def start(bot,message):
    if message.chat.id == 1734062356 :
        text = start_message
        reply_markup = InlineKeyboardMarkup(start_message_button)
        message.reply(
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    else : 
        message.reply("u have not permission")


print("bot started")
bot.run()
