import os
import psutil
import subprocess
from functions import *
import mysql.connector
from dotenv import load_dotenv
from pyrogram import Client,filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

# load data for file .env
load_dotenv()

configDB = {
  'user': os.getenv("DB_USERNAME"),
  'password': os.getenv("DB_PASSWORD"),
  'host': os.getenv("DB_HOST"),
  'database': os.getenv("DB_DATABASE"),
  'raise_on_warnings': True
}


UserTable = """
    CREATE TABLE users
    (
        id int NOT NULL auto_increment,
        tel_id int,
        name varchar(255),
        is_superadmin BOOL,
        is_staff BOOL,
        is_customer BOOL,
        PRIMARY KEY (id,tel_id)
    )
"""

SshUserTable = """
    CREATE TABLE ssh_users
    (
        id int NOT NULL auto_increment,
        user_id int NOT NULL,
        max_logins int NOT NULL,
        create_at DATE NULL,
        update_at DATE NULL,
        expire_at DATE NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
"""


connection = mysql.connector.connect(**configDB)
cursor = connection.cursor()

cursor.execute(UserTable)
cursor.execute(SshUserTable)


connection.commit()
connection.close()

bot = Client(
            os.getenv("BOT_NAME")
            ,api_id=os.getenv("API_ID")
            ,api_hash=os.getenv('API_HASH')
            ,bot_token=os.getenv("BOT_TOKEN"))

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
        InlineKeyboardButton('Back To menu' , callback_data="back_to_menu")
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
    ] ,
    [
        InlineKeyboardButton('Back To menu' , callback_data="back_to_menu")
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
PAGE_USERS = f"select user (count of user {CountOfUser})"
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

PAGE_USERS_BUTTON.append([
        InlineKeyboardButton('back' , callback_data="back_to_page_3"),
        InlineKeyboardButton('back to menu' , callback_data="back_to_menu")
])

PAGE_ADD_USER_TEXT = """
    Add new user
    username : {}
    password : {}
    limit : {}
    expire : {}
    """

PAGE_ADD_USER_BUTTON = [
    [
         InlineKeyboardButton('Cancel', callback_data="cancel_add_user")
    ]
]
# end pages



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
    if callbackQuery.data == "users":
        callbackQuery.edit_message_text(
            PAGE3_TEXT,
            reply_markup=InlineKeyboardMarkup(PAGE3_BUTTON)
        )
    for user in getAllUser.decode("utf-8").splitlines():
        if callbackQuery.data == user:
            if user != "root" : 
                PAGE_USER_EDIT = f"Performing operations on the {user} user"
                callbackUserTextDelete = "delete user"
                callbackUserDelete = f"delete_{user}"
                if is_user_active(user) == False:
                    callbackUserText = "status [enable] click to change"
                    callbackUser = f"change_status_{user}_to_disable"
                else : 
                    callbackUserText = "status [disable] click to change"
                    callbackUser = f"change_status_{user}_to_enable"

                PAGE_USER_EDIT_BUTTON = [
                    [
                    InlineKeyboardButton(callbackUserText,callback_data=callbackUser),
                    InlineKeyboardButton(callbackUserTextDelete,callback_data=callbackUserDelete)
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
        elif callbackQuery.data == f"delete_{user}":
            textDeleteUser = f"are you sure to delete user {user}"
            PAGE_USER_DELETE = [
                [
                   InlineKeyboardButton("YES",callback_data="yes_delete_user"),
                   InlineKeyboardButton("NO",callback_data="no_delete_user") 
                ]
            ]
            callbackQuery.edit_message_text(
                textDeleteUser,
                reply_markup=InlineKeyboardMarkup(PAGE_USER_DELETE)
            )
        elif callbackQuery.data == "yes_delete_user" : 
            subprocess.run(["userdel" , user])
            callbackQuery.answer(
            f"user {user} deleted",
            show_alert=True
            )
            callbackQuery.edit_message_text(
                PAGE_USERS,
                reply_markup=InlineKeyboardMarkup(PAGE_USERS_BUTTON)
            )
    if callbackQuery.data == "add_user":
        callbackQuery.edit_message_text(
            PAGE_ADD_USER_TEXT,
            reply_markup=InlineKeyboardMarkup(PAGE_ADD_USER_BUTTON)
        )
        
        bot.send_message(callbackQuery.from_user.id,"send data of new user with format [username password dataTime limit]")
        bot.send_message(callbackQuery.from_user.id,"example : testUsername testPassword 2023/3/32")
        @bot.on_message(filters.text & filters.private)
        def getInformationFromUser(bot, message):
            UserInformation = message.text.split()
            if len(UserInformation) == 4:
                global username,password,dataTime,limit
                username = UserInformation[0]
                password = UserInformation[1]
                dataTime = UserInformation[2]
                limit = UserInformation[3]
                PAGE_ADD_USER_BUTTON_CALLBACK = [
                    [
                        InlineKeyboardButton('confirm' , callback_data='confirm'),
                        InlineKeyboardButton('cancel' , callback_data='cancel')
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(PAGE_ADD_USER_BUTTON_CALLBACK)
                message.reply(
                text=PAGE_ADD_USER_TEXT.format(username,password,limit,dataTime),
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
            
    if callbackQuery.data == 'confirm':
        add_user(username,password,dataTime,limit)
        callbackQuery.edit_message_text(
                PAGE3_TEXT,
                reply_markup=InlineKeyboardMarkup(PAGE3_BUTTON)
            )
    if  callbackQuery.data == "cancel":
        callbackQuery.edit_message_text(
            PAGE3_TEXT,
            reply_markup=InlineKeyboardMarkup(PAGE3_BUTTON)
        )
        
    
    if callbackQuery.data == "reboot":
        bot.send_message(callbackQuery.from_user.id,"rebooted")
        os.system('shutdown -r now')
    if callbackQuery.data == "update":
        update_cmd = "apt update"
        subprocess.run(update_cmd.split())

        upgrade_cmd = "apt upgrade -y"
        subprocess.run(upgrade_cmd.split())
        bot.send_message(callbackQuery.from_user.id,"server updated")
    if callbackQuery.data == "back_to_page_3":
        callbackQuery.edit_message_text(
            PAGE3_TEXT,
            reply_markup=InlineKeyboardMarkup(PAGE3_BUTTON)
        )
    if callbackQuery.data == "user_list":
        callbackQuery.edit_message_text(
            PAGE_USERS,
            reply_markup=InlineKeyboardMarkup(PAGE_USERS_BUTTON)
        )
    if callbackQuery.data == "disk_usage":
        callbackQuery.answer(
                DiskUsage(),
                show_alert=True
            )
        # send cpu and ram usage data to bot
    elif callbackQuery.data == "cpu_and_ram_usage":
        callbackQuery.answer(
            CPUANDRAM(),
            show_alert=True
            )
    # send uptime server to bot
    elif  callbackQuery.data == "uptime_server":
        callbackQuery.answer(
            uptime(),
            show_alert=True
            )
    # send server description to bot
    elif callbackQuery.data == "server_description" :
        callbackQuery.answer(
            get_info_server(),
            show_alert=True
            )      
    if callbackQuery.data == "back_to_page_2":
        callbackQuery.edit_message_text(
            PAGE2_TEXT,
            reply_markup=InlineKeyboardMarkup(PAGE2_BUTTON)
        )
print("bot started")
bot.run()