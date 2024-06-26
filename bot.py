import os
import subprocess
from Users import Users
from Monitoring import Monitoring
import mysql.connector
from dotenv import load_dotenv
from pyrogram import Client,filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

# load data for file .env
load_dotenv()

UserTable = """
    CREATE TABLE users
    (
        id int NOT NULL auto_increment,
        tel_id int UNIQUE NOT NULL,
        is_superadmin BOOLEAN DEFAULT(0),
        is_staff BOOLEAN DEFAULT(0),
        is_customer BOOLEAN DEFAULT(1),
        PRIMARY KEY (id)
    )
"""

SshUserTable = """
    CREATE TABLE ssh_users
    (
        id int NOT NULL auto_increment,
        user_id int NOT NULL,
        username varchar(255) NULL,
        max_logins int NOT NULL,
        create_at DATE NULL,
        update_at DATE NULL,
        expire_at DATE NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
"""
users = Users()
monitoring = Monitoring()
connection = mysql.connector.connect(**users.configDB)
cursor = connection.cursor()

try:
    cursor.execute(UserTable)
    cursor.execute(SshUserTable)
except:
    print("error or exsit tables")



bot = Client(
            os.getenv("BOT_NAME")
            ,api_id=os.getenv("API_ID")
            ,api_hash=os.getenv('API_HASH')
            ,bot_token=os.getenv("BOT_TOKEN"))

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

CountOfUser = users.getCountSshUsers()
PAGE_USERS = f"select user (count of user {CountOfUser})"
PAGE_USERS_BUTTON = []

getAllUser = users.getAllUsernameSSHusers()



for i in range(0, len(getAllUser), 2):
    if i+1 < len(getAllUser):
        button1 = InlineKeyboardButton(text=getAllUser[i], callback_data=getAllUser[i])
        button2 = InlineKeyboardButton(text=getAllUser[i+1], callback_data=getAllUser[i+1])
        PAGE_USERS_BUTTON.append([button1, button2])
    else:
        button1 = InlineKeyboardButton(text=getAllUser[i], callback_data=getAllUser[i])
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
getAllTelID = "SELECT tel_id from users"
cursor.execute(getAllTelID)
@bot.on_message(filters.command(['start' , 'help']) & filters.private)
def start(bot,message):
    for tel_id in cursor:
        for id in tel_id:
            if id == message.chat.id:
                wellcom = f"wellcome back to my bot {message.chat.username}"
                message.reply(
                text=wellcom,
                disable_web_page_preview=True
            )
                break
        else:
            bot.send_message(message.chat.id,'wellcome to my bot')
            print(message.chat.id)
            users.cur.execute(f"INSERT INTO users VALUE (null,{message.chat.id},0,0,1)")
            users.connectionDB.commit()
                
    for user in users.getUsersAdmin():
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
        resultSpeedTest = users.internet_speed()
        callbackQuery.answer(
                resultSpeedTest,
                show_alert=True
        )
    if callbackQuery.data == "users":
        callbackQuery.edit_message_text(
            PAGE3_TEXT,
            reply_markup=InlineKeyboardMarkup(PAGE3_BUTTON)
        )
    for user in getAllUser:
        if callbackQuery.data == user:
            if user != "root" : 
                PAGE_USER_EDIT = f"Performing operations on the {user} user"
                callbackUserTextDelete = "delete user"
                callbackUserDelete = f"delete_{user}"
                if users.is_user_active(user) == False:
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
            DeleteUser = users.delete_user(user)
            if DeleteUser == True :
                callbackQuery.answer(
                f"user {user} deleted",
                show_alert=True
                )
            else:
                callbackQuery.answer(
                f"user {user} undeleted",
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
        users.cur.execute(f'SELECT id from users where tel_id = {callbackQuery.from_user.id}')
        for id in users.cur:
            for i in id:
                id = i
    
        users.add_user(id,username,password,dataTime,limit)
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
                monitoring.DiskUsage(),
                show_alert=True
            )
        # send cpu and ram usage data to bot
    elif callbackQuery.data == "cpu_and_ram_usage":
        callbackQuery.answer(
            monitoring.CPUANDRAM(),
            show_alert=True
            )
    # send uptime server to bot
    elif  callbackQuery.data == "uptime_server":
        callbackQuery.answer(
            monitoring.uptime(),
            show_alert=True
            )
    # send server description to bot
    elif callbackQuery.data == "server_description" :
        callbackQuery.answer(
            monitoring.get_info_server(),
            show_alert=True
            )      
    if callbackQuery.data == "back_to_page_2":
        callbackQuery.edit_message_text(
            PAGE2_TEXT,
            reply_markup=InlineKeyboardMarkup(PAGE2_BUTTON)
        )

users.connectionDB.commit()
connection.close()
print("bot started")
bot.run()