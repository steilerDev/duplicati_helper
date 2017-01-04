
import logging
from screen import Screen
from duplicati_widgets import JobNameWidget, JobStatusWidget, UsageWidget, RunningJobsWidget, ShutdownWidget
from widgets import TitleWidget

class BackupScreen(Screen):

    def __init__(self, server, ref, backup_name, width=20, height=4, heartbeat="off"):
        Screen.__init__(self, server, ref)
        self.backup_name = backup_name
        
        self.set_heartbeat(heartbeat)
        self.set_width(width)
        self.set_height(height)
        self.set_duration(3)

        ## Add title
        self.add_widget(TitleWidget(screen=self, ref="title_" + self.ref, text=self.backup_name))
        ## Create job widget
        self.add_widget(ShutdownWidget(screen=self, ref="shutdown_" + self.ref, y=2))

        ## Create job status widget
        self.add_widget(JobStatusWidget(screen=self, ref="status_" + self.ref, job_name=self.backup_name, y=3))

        ## Create job usage widget
        self.add_widget(UsageWidget(screen=self, ref="usage_" + self.ref, job_name=self.backup_name, y=4))

    def update(self):
        if self.widgets["status_" + self.ref].running:
            logging.debug('BackupScreen %s: Currently running', self.ref)
            self.set_duration(8)
        else:
            logging.debug('BackupScreen %s: Currently NOT running', self.ref)
            self.set_duration(3)
        Screen.update(self)

class OverviewScreen(Screen):

    def __init__(self, server, ref, width=20, height=4, heartbeat="off", debug=False):
        Screen.__init__(self, server, ref)
        self.set_heartbeat(heartbeat)
        self.set_width(width)
        self.set_height(height)
        self.set_duration(8)

        self.add_widget(TitleWidget(screen=self, ref="title_" + self.ref, text="steilerGroup-HS"))
        self.add_widget(ShutdownWidget(screen=self, ref="shutdown_" + self.ref, y=2))
        self.add_widget(UsageWidget(screen=self, ref="usage_" + self.ref, job_name="", y=3))
        self.add_widget(RunningJobsWidget(screen=self, ref="jobs_" + self.ref, y=4))

