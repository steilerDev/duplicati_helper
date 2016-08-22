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
        self.running = False
    
        ScrollerWidget.__init__(self, screen, ref, text="Backup Status", top=y)

    def update(self):
        if os.path.isfile("/run/duplicati." + self.job_name + ".pid"):
            if os.path.isfile("/run/status.duplicati." + self.job_name):
                status_file = open("/run/status.duplicati." + self.job_name)
                self.text = status_file.readline().rstrip()
                status_file.close()
            else:
                self.text = "Job running"
            self.running = True
        elif os.path.isfile("/opt/duplicati_helper/backup.status"):
            status_file = open("/opt/duplicati_helper/backup.status")
            found_entry = False
            for line in status_file:
                status_array = line.split()
                if status_array[1] == self.job_name:
                    found_entry = True
                    status_array.remove(status_array[2])
                    status_array.remove(status_array[1])
                    status_array.remove(status_array[0])
                    self.text = ' '.join(status_array).rstrip()
            if not found_entry:
                self.text = "No status available"
            self.running = False
        else:
            self.text = "No status available"
            self.running = False
        ScrollerWidget.update(self)

class UsageWidget(StringWidget):

    def __init__(self, screen, ref, job_name, y):
        self.job_name = job_name
        self.process = None
        StringWidget.__init__(self, screen, ref, text="Usage...", y=y)
    
    def update(self):
        if not self.job_name:
            self.set_usage(cpu=psutil.cpu_percent(), mem_perc=psutil.virtual_memory()[2])
        elif os.path.isfile("/run/duplicati." + self.job_name + ".pid"):
           try: 
                if self.process == None or not self.process.is_running():
                    pid_file = open("/run/duplicati." + self.job_name + ".pid")
                    self.process = psutil.Process(int(pid_file.readline()))
                    pid_file.close() 
                self.set_usage(cpu=self.process.cpu_percent(), mem=self.process.memory_info()[1])
           except(psutil.NoSuchProcess, psutil.ZombieProcess, psutil.AccessDenied):
               self.text = "No usage available"        
        else:
            if self.process != None:
                del(self.process)
            if os.path.isfile("/opt/duplicati_helper/backup.status"):
                status_file = open("/opt/duplicati_helper/backup.status")
                found_entry = False
                for line in status_file:
                    status_array = line.split()
                    if status_array[1] == self.job_name:
                        found_entry = True
                        self.text = status_array[2]
                if not found_entry:
                    self.text = "No usage available"
        StringWidget.update(self) 

    def set_usage(self, cpu, mem_perc="", mem=""):
        if mem_perc: 
            self.text = "CPU: " + str(cpu) + "% MEM: " + str(mem_perc) + "%"
        elif mem:
            self.text = "CPU: " + str(cpu) + "% MEM: " + size(mem)
        else:
            self.text = "No usage availabel"

class RunningJobsWidget(ScrollerWidget):
    
    def __init__(self, screen, ref, y):
        ScrollerWidget.__init__(self, screen, ref, text="No jobs running", top=y)

    def update(self):
        if os.path.isfile("/opt/duplicati_helper/backup.conf"):
            running_jobs=[]
            backup_conf = open("/opt/duplicati_helper/backup.conf")
            for line in backup_conf:
                if line and not line.startswith("#"):
                    line_array = line.split()
                    if os.path.isfile("/run/duplicati." + line_array[0] + ".pid"):
                        running_jobs.append(line_array[0])
            if running_jobs:
                self.text = "Running jobs: " + ', '.join(running_jobs)
            else:
                self.text = "No jobs running"
        ScrollerWidget.update(self)

class ShutdownWidget(StringWidget):

    def __init__(self, screen, ref, y):
        StringWidget.__init__(self, screen, ref, text="", y=y)

    def update(self):
        if os.path.isfile("/run/shutdown.pid"):
            self.text = "# Shutdown scheduled"
        else:
            self.text = ""
        StringWidget.update(self)
