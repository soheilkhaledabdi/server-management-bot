import psutil
import speedtest
import subprocess

class Monitoring():
    
    def internet_speed(self):
        try : 
            speed = speedtest.Speedtest()
            download_speed = round(speed.download() / (1024*1024), 2)
            upload_speed = round(speed.upload() / (1024*1024), 2)
            return f"speed of Download {download_speed} , speed of upload {upload_speed}"
        except :
            return "An exception occurred"
        
        
    def DiskUsage(self):
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
    
    def CPUANDRAM(self):
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


    def uptime(self):
        UpTime = subprocess.check_output(['uptime','-p']).decode('UTF-8')
        return UpTime


    def get_info_server(self):
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
