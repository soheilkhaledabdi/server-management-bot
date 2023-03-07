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




#  get data from server 


# get data of disk usage
diskTotal = int(psutil.disk_usage('/').total/(1024*1024*1024))
diskUsed = int(psutil.disk_usage('/').used/(1024*1024*1024))
diskAvail = int(psutil.disk_usage('/').free/(1024*1024*1024))
diskPercent = psutil.disk_usage('/').percent

dataOfDiskUsage = '''
    Disk Info
    ---------
    Total = {} GB
    Used = {} GB
    Avail = {} GB
    Usage = {} %\n'''.format(diskTotal,diskUsed,diskAvail,diskPercent)
# end data usage

# get data of  cpu and ram

cpuUsage = psutil.cpu_percent(interval=1)
ramTotal = int(psutil.virtual_memory().total/(1024*1024)) #GB
ramUsage = int(psutil.virtual_memory().used/(1024*1024)) #GB
ramFree = int(psutil.virtual_memory().free/(1024*1024)) #GB
ramUsagePercent = psutil.virtual_memory().percent
dataOfCpuAndRam = '''
    CPU & RAM Info
    ---------
    CPU Usage = {} %
    RAM
    Total = {} MB
    Usage = {} MB
    Free  = {} MB
    Used = {} %\n'''.format(cpuUsage,ramTotal,ramUsage,ramFree,ramUsagePercent)

# end data cpu and ram


# get of uptime server

dataOfUpTime = subprocess.check_output(['uptime','-p']).decode('UTF-8')

# end uptime 


# get info server

uname = subprocess.check_output(['uname','-rsoi']).decode('UTF-8')
host = subprocess.check_output(['hostname']).decode('UTF-8')
ipAddr = subprocess.check_output(['hostname','-I']).decode('UTF-8')

dataOfInfoServer ='''
    Server Desc
    ---------
    OS = {}
    Hostname = {} 
    IP Addr = {}'''.format(uname,host,ipAddr)

# end info server

# end



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
def callback_query_disk_usage(client,callbackQuery):
    # send disk usage
    if callbackQuery.data == "disk_usage":
        callbackQuery.answer(
                dataOfDiskUsage,
                show_alert=True
            )
        # send cpu and ram usage data to bot
    elif callbackQuery.data == "cpu_and_ram_usage":
        callbackQuery.answer(
            dataOfCpuAndRam,
            show_alert=True
            )
    # send uptime server to bot
    elif  callbackQuery.data == "uptime_server":
        callbackQuery.answer(
            dataOfUpTime,
            show_alert=True
            )
    # send server description to bot
    elif callbackQuery.data == "server_description" :
        callbackQuery.answer(
            dataOfInfoServer,
            show_alert=True
            )      

print("bot started")
bot.run()
