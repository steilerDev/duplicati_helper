from screen import Screen
from duplicati_widgets import JobNameWidget, JobStatusWidget, JobUsageWidget
from widgets import TitleWidget

class BackupScreen(Screen):

    def __init__(self, server, ref, backup_name):
        super(BackupScreen, self).__init__(server, ref)
        self.backup_name = backup_name

        ## Add title
        self.add_widget(TitleWidget(screen=self, ref="Title", text="steilerGroup-HomeServer"))
        ## Create job widget
        self.add_widget(JobNameWidget(screen=self, ref="JobNameWidget", job_name=self.backup_name, y=2))

        ## Create job status widget
        self.add_widget(JobStatusWidget(screen=self, ref="JobStatusWidget", job_name=self.backup_name, y=3))

        ## Create job usage widget
        self.add_widget(JobUsageWidget(screen=self, ref="JobUsageWidget", job_name=self.backup_name, y=4))
