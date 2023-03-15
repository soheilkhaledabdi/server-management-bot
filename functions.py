import subprocess
import crypt
import speedtest
from datetime import datetime
import pwd


def add_user(username : str,password : str,expiration_date : str,max_logins : int):
    try:
        subprocess.run(['useradd', username , '-p' , crypt.crypt(password)])
        subprocess.run(['chage', '-E', expiration_date, username])
        subprocess.run(['sudo', 'bash', '-c', f'echo "{username} hard maxlogins {max_logins}" >> /etc/security/limits.conf'])
        subprocess.run(['sudo', 'su', '-', username, '-c', 'ulimit -n -u'])
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