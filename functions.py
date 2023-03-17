import os
import subprocess
import pwd
import psutil
import crypt
import speedtest
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

# load data for file .env
load_dotenv()
configDB = {
  'user': os.getenv("DB_USERNAME"),
  'password': os.getenv("DB_PASSWORD"),
  'host': os.getenv("DB_HOST"),
  'database': os.getenv("DB_DATABASE"),
  'raise_on_warnings': True,
   'auth_plugin' :'mysql_native_password'
}
connectionDB = mysql.connector.connect(**configDB)
cur = connectionDB.cursor()

def getUsersAdmin():
    try:
        cur.execute("select tel_id from users where is_superadmin = 1")
        users_id = []
        for (tel_id) in cur:
            for id in (tel_id):
                users_id.append(id)
        return users_id
    except :
        return "error"

def getAllUsernameSSHusers():
    try:
        query = "SELECT username FROM ssh_users"
        users_list = []
        cur.execute(query)
        for (username) in cur:
            for user in username:
                users_list.append(user)
        return users_list
    except:
        return "error"

def getCountSshUsers():
    try:
        query = "SELECT count(*) FROM ssh_users"
        cur.execute(query)
        for (count) in cur:
            for c in count:
                return c 
    except : 
        return "error"

def add_user(user_id : int ,username : str,password : str,expiration_date : str,max_logins : int):
    try:
        salt = crypt.mksalt(crypt.METHOD_SHA512)
        subprocess.run(['useradd', username , '-p' , crypt.crypt(password, salt)])
        subprocess.run(['chage', '-E', expiration_date, username])
        subprocess.run(['sudo', 'bash', '-c', f'echo "{username} hard maxlogins {max_logins}" >> /etc/security/limits.conf'])
        subprocess.run(['sudo', 'su', '-', username, '-c', 'ulimit -n -u'])
        create_at = datetime.today().strftime("%Y-%m-%d")
        cur.execute(f"INSERT INTO ssh_users VALUE (null,{user_id} ,'{username}',{max_logins}, '{create_at}', null , '{expiration_date}')")
        return True
    except :
        return False

def disable_user(username : str):
    subprocess.check_output(f"usermod -L -e 1 {username}", shell=True)
    if is_user_active(username) == True:
        return True
    else:
        return False

def enable_user(username : str):
    subprocess.check_output(f"sudo usermod -e -1 -U {username}" , shell=True)
    if is_user_active(username) == False : 
        return True
    else:
        return False
  
  
def check_user_exsit(username : str):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False
      
  
def delete_user(username : str):
    try:
        subprocess.run(["userdel" , "-r" ,username])
        if check_user_exsit(username) == False:
            return True
        else:
            return False
    except:
        return "An exception occurred"
            
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


def internet_speed():
    try : 
        speed = speedtest.Speedtest()
        download_speed = round(speed.download() / (1024*1024), 2)
        upload_speed = round(speed.upload() / (1024*1024), 2)
        return f"speed of Download {download_speed} , speed of upload {upload_speed}"
    except :
        return "An exception occurred"
    
    
    
def DiskUsage():
    diskTotal = int(psutil.disk_usage('/').total/(1024*1024*1024))
    diskUsed = int(psutil.disk_usage('/').used/(1024*1024*1024))
    diskAvail = int(psutil.disk_usage('/').free/(1024*1024*1024))
    diskPercent = psutil.disk_usage('/').percent

    DiskUsage = '''
        Disk Info
        ---------
        Total = {} GB
        Used = {} GB
        Avail = {} GB
        Usage = {} %\n'''.format(diskTotal,diskUsed,diskAvail,diskPercent)
    return DiskUsage

def CPUANDRAM():
    cpuUsage = psutil.cpu_percent(interval=1)
    ramTotal = int(psutil.virtual_memory().total/(1024*1024)) #GB
    ramUsage = int(psutil.virtual_memory().used/(1024*1024)) #GB
    ramFree = int(psutil.virtual_memory().free/(1024*1024)) #GB
    ramUsagePercent = psutil.virtual_memory().percent
    CPURAM = '''
        CPU & RAM Info
        ---------
        CPU Usage = {} %
        RAM
        Total = {} MB
        Usage = {} MB
        Free  = {} MB
        Used = {} %\n'''.format(cpuUsage,ramTotal,ramUsage,ramFree,ramUsagePercent)
    return CPURAM


def uptime():
    UpTime = subprocess.check_output(['uptime','-p']).decode('UTF-8')
    return UpTime


def get_info_server():
    uname = subprocess.check_output(['uname','-rsoi']).decode('UTF-8')
    host = subprocess.check_output(['hostname']).decode('UTF-8')
    ipAddr = subprocess.check_output(['hostname','-I']).decode('UTF-8')

    InfoServer ='''
        Server Desc
        ---------
        OS = {}
        Hostname = {} 
        IP Addr = {}'''.format(uname,host,ipAddr)
    return InfoServer
