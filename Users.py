import os
import subprocess
import pwd
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

class Users:
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
    
    global cur
    connectionDB = mysql.connector.connect(**configDB)
    cur = connectionDB.cursor()

    def getUsersAdmin(self):
        try:
            cur.execute("select tel_id from users where is_superadmin = 1")
            users_id = []
            for (tel_id) in cur:
                for id in (tel_id):
                    users_id.append(id)
            return users_id
        except :
            return "error"

    def getAllUsernameSSHusers(self):
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

    def getCountSshUsers(self):
        try:
            query = "SELECT count(*) FROM ssh_users"
            cur.execute(query)
            for (count) in cur:
                for c in count:
                    return c 
        except : 
            return "error"
        
    def add_user(self , user_id : int ,username : str,password : str,expiration_date : str,max_logins : int):
        try:
            os.system(f"sudo useradd {username} -p $(openssl passwd -1 {password})")
            subprocess.run(['chage', '-E', expiration_date, username])
            subprocess.run(['sudo', 'bash', '-c', f'echo "{username} hard maxlogins {max_logins}" >> /etc/security/limits.conf'])
            subprocess.run(['sudo', 'su', '-', username, '-c', 'ulimit -n -u'])
            create_at = datetime.today().strftime("%Y-%m-%d")
            cur.execute(f"INSERT INTO ssh_users VALUE (null,{user_id} ,'{username}',{max_logins}, '{create_at}', null , '{expiration_date}')")
            self.connectionDB.commit()
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
            subprocess.run(["userdel" , "-r" ,username])
            q = f"DELETE FROM ssh_users where username = '{username}' "
            cur.execute(q)
            self.connectionDB.commit()
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
    