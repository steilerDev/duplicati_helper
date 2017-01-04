from widgets import StringWidget, ScrollerWidget
from hurry.filesize import size
import psutil
import os.path
import logging

class JobNameWidget(StringWidget):


    def __init__(self, screen, ref, job_name, y):
        self.job_name = job_name
         
        StringWidget.__init__(self, screen, ref, text="Backup Job: " + self.job_name, y=y)

    def set_job_name(self, job_name):
        self.job_name = job_name
        self.text = "Backup Job: " + job_name
        logging.info('JobNameWidget (%s): New backup job name: %s', self.ref, self.job_name)
        self.update()

    def set_y(self, y):
        self.y = y
        logging.info('JobNameWidget (%s): New y-coordinate: %i', self.ref, self.y)
        self.update() 

class JobStatusWidget(ScrollerWidget): 

    def __init__(self, screen, ref, job_name, y):
        self.job_name = job_name
        self.running = False
    
        ScrollerWidget.__init__(self, screen, ref, text="Backup Status", top=y)

    def update(self):
        if os.path.isfile("/run/duplicati." + self.job_name + ".pid"):
            if os.path.isfile("/run/status.duplicati." + self.job_name):
                logging.info('JobStatusWidget (%s): Job running, updating using status file', self.ref)
                status_file = open("/run/status.duplicati." + self.job_name)
                self.text = status_file.readline().rstrip()
                status_file.close()
            else:
                logging.warning('JobStatusWidget (%s): Job running, no status file available', self.ref)
                self.text = "Job running"
            self.running = True
        elif os.path.isfile("/opt/duplicati_helper/backup.status"):
            logging.info('JobStatusWidget (%s): Job not running, updating using backup status file', self.ref)
            status_file = open("/opt/duplicati_helper/backup.status")
            found_entry = False
            for line in status_file:
                status_array = line.split()
                if status_array[1] == self.job_name:
                    logging.info('JobStatusWidget (%s): Found status in backup status file', self.ref)
                    found_entry = True
                    status_array.remove(status_array[2])
                    status_array.remove(status_array[1])
                    status_array.remove(status_array[0])
                    self.text = ' '.join(status_array).rstrip()

            if not found_entry:
                logging.warning('JobStatusWidget (%s): Job not running, backup status file not available!', self.ref)
                self.text = "No status available"
            self.running = False
        else:
            logging.error('JobStatusWidget (%s): No status available', self.ref)
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
            logging.info('UsageWidget (%s): Getting system usage', self.ref)
            self.set_usage(cpu=psutil.cpu_percent(), mem_perc=psutil.virtual_memory()[2])
        elif os.path.isfile("/run/duplicati." + self.job_name + ".pid"):
           try: 
                if self.process == None or not self.process.is_running():
                    logging.info('UsageWidget (%s): Getting process object', self.ref)
                    pid_file = open("/run/duplicati." + self.job_name + ".pid")
                    self.process = psutil.Process(int(pid_file.readline()))
                    pid_file.close() 
                else:
                   logging.info('UsageWidget (%s): Using existing process object', self.ref) 
                self.set_usage(cpu=self.process.cpu_percent(), mem=self.process.memory_info()[1])
           except(psutil.NoSuchProcess, psutil.ZombieProcess, psutil.AccessDenied):
               logging.error('UsageWidget (%s): Unable to get usage for duplicati process', self.ref)
               self.text = "No usage available"        
        else:
            if self.process != None:
                logging.info('UsageWidget (%s): Deleting process object, since process is no longer running', self.ref)
                del(self.process)
            if os.path.isfile("/opt/duplicati_helper/backup.status"):
                logging.info('UsageWidget (%s): Getting last backup status', self.ref)
                status_file = open("/opt/duplicati_helper/backup.status")
                found_entry = False
                for line in status_file:
                    status_array = line.split()
                    if status_array[1] == self.job_name:
                        logging.info('UsageWidget (%s): Found status in backup status file', self.ref)
                        found_entry = True
                        self.text = status_array[2]
                if not found_entry:
                    logging.warning('UsageWidget (%s): Job not running, backup status file not available!', self.ref)
                    self.text = "No usage available"
        StringWidget.update(self) 

    def set_usage(self, cpu, mem_perc="", mem=""):
        cpu_str = str(cpu) + "%"
        mem_str = "N/A"

        if mem_perc: 
            mem_str = str(mem_perc) + "%"
        elif mem:
            mem_str = size(mem)

        self.text = "CPU: " + cpu_str + " MEM: " + mem_str
        logging.debug('UsageWidget (%s): Updating usage (CPU: %s | MEM: %s)', self.ref, cpu_str, mem_str)

class RunningJobsWidget(ScrollerWidget):
    
    def __init__(self, screen, ref, y):
        ScrollerWidget.__init__(self, screen, ref, text="No jobs running", top=y)

    def update(self):
        if os.path.isfile("/opt/duplicati_helper/backup.conf"):
            logging.info('RunningJobsWidget (%s): Reading config and checking for pid file', self.ref)
            running_jobs=[]
            backup_conf = open("/opt/duplicati_helper/backup.conf")
            for line in backup_conf:
                if line and not line.startswith("#"):
                    line_array = line.split()
                    if os.path.isfile("/run/duplicati." + line_array[0] + ".pid"):
                        running_jobs.append(line_array[0])
            if running_jobs:
                self.text = "Running jobs: " + ', '.join(running_jobs)
                logging.debug('RunningJobsWidget (%s): %s', self.ref, self.text)
            else:
                self.text = "No jobs running"
                logging.debug('RunningJobsWidget (%s): No Jobs running', self.ref)
        else:
            logging.error('RunningJobsWidget (%s): Unable to get config file', self.ref)
            self.text = "No information about running jobs available"
        ScrollerWidget.update(self)

class ShutdownWidget(StringWidget):

    def __init__(self, screen, ref, y):
        StringWidget.__init__(self, screen, ref, text="", y=y)

    def update(self):
        if os.path.isfile("/run/shutdown.pid"):
            logging.info('ShutdownWidget (%s): Detected scheduled shutdown', self.ref)
            self.text = "# Shutdown scheduled"
        else:
            self.text = ""
        StringWidget.update(self)
