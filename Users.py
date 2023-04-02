import os
import subprocess
import pwd
from datetime import datetime

class Users:
    def add_user(self , user_id : int ,username : str,password : str,expiration_date : str,max_logins : int):
        try:
            os.system(f"sudo useradd {username} -p $(openssl passwd -1 {password})")
            subprocess.run(['chage', '-E', expiration_date, username])
            subprocess.run(['sudo', 'bash', '-c', f'echo "{username} hard maxlogins {max_logins}" >> /etc/security/limits.conf'])
            subprocess.run(['sudo', 'su', '-', username, '-c', 'ulimit -n -u'])
            return True
        except :
            return False

    def disable_user(self ,username : str):
        subprocess.check_output(f"usermod -L -e 1 {username}", shell=True)
        if self.is_user_active(username) == True:
            return True
        else:
            return False
    
    def enable_user(self , username : str):
        subprocess.check_output(f"sudo usermod -e -1 -U {username}" , shell=True)
        if self.is_user_active(username) == False : 
            return True
        else:
            return False
    
    def check_user_exsit(self,username : str):
        try:
            pwd.getpwnam(username)
            return True
        except KeyError:
            return False
    

    def delete_user(self , username : str):
        try:
            subprocess.run(["userdel","-r",username])
            if self.check_user_exsit(username) == False:
                return True
            else:
                return False
        except:
            return "An exception occurred"
    
    
    def is_user_active(self,username):
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
    