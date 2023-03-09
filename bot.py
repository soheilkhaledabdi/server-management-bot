import os
from dotenv import load_dotenv
import psutil
import subprocess
from pyrogram import Client,filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram import enums
import speedtest
from datetime import datetime
# migrate_from_chat_id
load_dotenv()
bot = Client(
            os.getenv("BOT_NAME")
            ,api_id=os.getenv("API_ID")
            ,api_hash=os.getenv('API_HASH')
            ,bot_token=os.getenv("BOT_TOKEN"))

# function get speed test
def internet_speed():
    speed = speedtest.Speedtest()
    download_speed = round(speed.download() / (1024*1024), 2) 
    upload_speed = round(speed.upload() / (1024*1024), 2)
    return f"speed of Download {download_speed} , speed of upload {upload_speed}"


def is_user_active(username):
    result = subprocess.run(['chage', '-l', username], stdout=subprocess.PIPE)
    output = result.stdout.decode().strip()
    for line in output.split('\n'):
        if 'Account expires' in line:
            _, date_str = line.split(':')
            date_str = date_str.strip()
            if date_str == 'never':
                return False
            expiration_date = datetime.strptime(date_str, '%b %d, %Y')
            if datetime.now() > expiration_date:
                return True
            else:
                return False
    return False
# end function

# Users who have access permission to use the bot

users_id = [1734062356,1033070918]




# start message and button

START_MESSAGE = "Choose your operation"
START_MESSAGE_BUTTON=[
    [
    InlineKeyboardButton('Monitoring Server' , callback_data="monitoring_server"),
    InlineKeyboardButton('Operations On The Server' , callback_data="Operations_Server")
    ]
]


#  all pages

PAGE1_TEXT = "Select the Server Monitoring operation"

PAGE1_BUTTON = [
    [
    InlineKeyboardButton('Disk Usage' , callback_data="disk_usage"),
    InlineKeyboardButton('CPU and RAM Usage' , callback_data="cpu_and_ram_usage")
    ]
    ,
    [
    InlineKeyboardButton('Uptime Server' , callback_data="uptime_server"),
    InlineKeyboardButton('Server Description',callback_data="server_description")
    ]
    ,
    [
        InlineKeyboardButton('Back To Page 1' , callback_data="back_to_menu")
    ]
]


PAGE2_TEXT = "Select the Server operation"

PAGE2_BUTTON = [
    [
        InlineKeyboardButton('Users' , callback_data="users"),
        InlineKeyboardButton('SpeedTest' , callback_data="speed_test")
    ]
    ,
    [
        InlineKeyboardButton('Reboot' , callback_data="reboot"),
        InlineKeyboardButton('update and upgrade' , callback_data="update")
    ]
]


PAGE3_TEXT = "Select the user operation"
PAGE3_BUTTON = [
    [
        InlineKeyboardButton('users list' , callback_data="user_list"),
        InlineKeyboardButton('add User', callback_data="add_user")
    ]
    ,
    [
        InlineKeyboardButton('back to page 2' , callback_data="back_to_page_2"),
        InlineKeyboardButton('back to menu' , callback_data="back_to_menu")
    ]
]

CountOfUser = subprocess.check_output("grep '/bin/bash' /etc/passwd | wc -l", shell=True)
CountOfUser = CountOfUser.decode("utf-8")
PAGE_USERS = f"select user (count of user[{CountOfUser}])"
PAGE_USERS_BUTTON = []

getAllUser = subprocess.check_output("""grep "/bin/bash" /etc/passwd | cut -d: -f1""", shell=True)


for i in range(0, len(getAllUser.decode("utf-8").splitlines()), 2):
    if i+1 < len(getAllUser.decode("utf-8").splitlines()):
        button1 = InlineKeyboardButton(text=getAllUser.decode("utf-8").splitlines()[i], callback_data=getAllUser.decode("utf-8").splitlines()[i])
        button2 = InlineKeyboardButton(text=getAllUser.decode("utf-8").splitlines()[i+1], callback_data=getAllUser.decode("utf-8").splitlines()[i+1])
        PAGE_USERS_BUTTON.append([button1, button2])
    else:
        button1 = InlineKeyboardButton(text=getAllUser.decode("utf-8").splitlines()[i], callback_data=getAllUser.decode("utf-8").splitlines()[i])
        PAGE_USERS_BUTTON.append([button1])

InlineKeyboardButton('root' , callback_data='root')
# end pages

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
    for user in users_id:
        if message.chat.id == user :
            text = START_MESSAGE
            reply_markup = InlineKeyboardMarkup(START_MESSAGE_BUTTON)
            message.reply(
                text=text,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )


@bot.on_callback_query()
def callback_query(client,callbackQuery):
    # send disk usage
    if callbackQuery.data == "monitoring_server":
        callbackQuery.edit_message_text(
            PAGE1_TEXT,
            reply_markup=InlineKeyboardMarkup(PAGE1_BUTTON)
        )
    if callbackQuery.data == "back_to_menu":
        callbackQuery.edit_message_text(
            START_MESSAGE,
            reply_markup=InlineKeyboardMarkup(START_MESSAGE_BUTTON)
        )
    if callbackQuery.data == "Operations_Server":
        callbackQuery.edit_message_text(
            PAGE2_TEXT,
            reply_markup=InlineKeyboardMarkup(PAGE2_BUTTON)
        )
    if callbackQuery.data == "speed_test":
        resultSpeedTest = internet_speed()
        callbackQuery.answer(
                resultSpeedTest,
                show_alert=True
        )
    if callbackQuery.data == "users" :
        callbackQuery.edit_message_text(
            PAGE3_TEXT,
            reply_markup=InlineKeyboardMarkup(PAGE3_BUTTON)
        )
    for user in getAllUser.decode("utf-8").splitlines():
        if callbackQuery.data == user:
            if user != "root" : 
                PAGE_USER_EDIT = f"Performing operations on the {user} user"
                if is_user_active(user) == False:
                    callbackUserText = "status [enable] click to change"
                    callbackUser = f"change_status_{user}_to_disable"
                else : 
                    callbackUserText = "status [disable] click to change"
                    callbackUser = f"change_status_{user}_to_enable"

                PAGE_USER_EDIT_BUTTON = [
                    [
                    InlineKeyboardButton(callbackUserText,callback_data=callbackUser)
                    ]
                ]
            
                callbackQuery.edit_message_text(
                PAGE_USER_EDIT,
                reply_markup=InlineKeyboardMarkup(PAGE_USER_EDIT_BUTTON)
        )
        elif callbackQuery.data == f"change_status_{user}_to_disable":
            subprocess.check_output(f"usermod -L -e 1 {user}", shell=True)
            success = f"account {user} disabled"
            callbackQuery.answer(
            success,
            show_alert=True
            )
            callbackQuery.edit_message_text(
            PAGE_USERS,
            reply_markup=InlineKeyboardMarkup(PAGE_USERS_BUTTON)
        )
        elif callbackQuery.data == f"change_status_{user}_to_enable":
            subprocess.check_output(f"sudo usermod -e -1 -U {user}" , shell=True)
            success = f"account {user} enabled"
            callbackQuery.answer(
            success,
            show_alert=True
            )
            callbackQuery.edit_message_text(
            PAGE_USERS,
            reply_markup=InlineKeyboardMarkup(PAGE_USERS_BUTTON)
        )   
    if callbackQuery.data == "add_user":
        bot.send_message(callbackQuery.from_user.id,"send name of user")

    if callbackQuery.data == "user_list":
        callbackQuery.edit_message_text(
            PAGE_USERS,
            reply_markup=InlineKeyboardMarkup(PAGE_USERS_BUTTON)
        )
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
    if callbackQuery.data == "back_to_page_2":
        callbackQuery.edit_message_text(
            PAGE2_TEXT,
            reply_markup=InlineKeyboardMarkup(PAGE2_BUTTON)
        )
print("bot started")
bot.run()