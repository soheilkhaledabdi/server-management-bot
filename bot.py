import os
import psutil
import subprocess
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


@bot.on_callback_query()
def callback_query(client,callbackQuery):
    print(CallbackQuery)
    diskTotal = int(psutil.disk_usage('/').total/(1024*1024*1024))
    diskUsed = int(psutil.disk_usage('/').used/(1024*1024*1024))
    diskAvail = int(psutil.disk_usage('/').free/(1024*1024*1024))
    diskPercent = psutil.disk_usage('/').percent

    
    text = '''
        Disk Info
        ---------
        Total = {} GB
        Used = {} GB
        Avail = {} GB
        Usage = {} %\n'''.format(diskTotal,diskUsed,diskAvail,diskPercent)
    
    if callbackQuery.data == "disk_usage":
        CallbackQuery.answer(
            callbackQuery.id,
            text=text,
            show_alert=True
            )


print("bot started")
bot.run()
