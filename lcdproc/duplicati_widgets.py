from widgets import StringWidget, ScrollerWidget
from hurry.filesize import size
import psutil
import os.path

class JobNameWidget(StringWidget):

    def __init__(self, screen, ref, job_name, y): 
        self.job_name = job_name
         
        StringWidget.__init__(self, screen, ref, text="Backup Job: " + self.job_name, y=y)

    def set_job_name(self, job_name):
        self.job_name = job_name
        self.text = "Backup Job: " + job_name
        self.update()

    def set_y(self, y):
        self.y = y
        self.update() 

class JobStatusWidget(ScrollerWidget): 

    def __init__(self, screen, ref, job_name, y): 
        self.job_name = job_name
    
        ScrollerWidget.__init__(self, screen, ref, text="Backup Status", top=y)

    def update(self):
        if os.path.isfile("/run/duplicati." + self.job_name + ".pid"):
            if os.path.isfile("/run/status.duplicati." + self.job_name):
                status_file = open("/run/status.duplicati." + self.job_name)
                self.text = status_file.readline().rstrip()
                status_file.close()
            else:
                self.text = "Job running"
        elif os.path.isfile("/opt/duplicati_helper/backup.status"):
            status_file = open("/opt/duplicati_helper/backup.status")
            for line in status_file:
                status_array = line.split()
                if status_array[1] == self.job_name:
                    status_array.remove(status_array[2])
                    status_array.remove(status_array[1])
                    status_array.remove(status_array[0])
                    self.text = ' '.join(status_array).rstrip()
        else:
            self.text = "No info available"
#        self.right = len(self.text)
        ScrollerWidget.update(self)

class JobUsageWidget(StringWidget):

    def __init__(self, screen, ref, job_name, y):
        self.job_name = job_name
        self.process = None
        StringWidget.__init__(self, screen, ref, text="Usage...", y=y)
    
    def update(self):
        if os.path.isfile("/run/duplicati." + self.job_name + ".pid"):
           try: 
                if self.process == None or not self.process.is_running():
                    pid_file = open("/run/duplicati." + self.job_name + ".pid")
                    self.process = psutil.Process(int(pid_file.readline()))
                    pid_file.close() 
                self.cpu = self.process.cpu_percent()
                self.mem = size(self.process.memory_info()[1])
                self.text = "Usage: " + str(self.cpu) + "% " + self.mem
           except(psutil.NoSuchProcess, psutil.ZombieProcess, psutil.AccessDenied):
               self.text = "Usage not available"        
        else:
            if self.process != None:
                del(self.process)
            if os.path.isfile("/opt/duplicati_helper/backup.status"):
                status_file = open("/opt/duplicati_helper/backup.status")
                for line in status_file:
                    status_array = line.split()
                    if status_array[1] == self.job_name:
                        self.text = status_array[2]
        StringWidget.update(self) 
