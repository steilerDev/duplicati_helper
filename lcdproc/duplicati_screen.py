from screen import Screen
from duplicati_widgets import JobNameWidget, JobStatusWidget, UsageWidget, RunningJobsWidget, ShutdownWidget
from widgets import TitleWidget

class BackupScreen(Screen):

    def __init__(self, server, ref, backup_name, width=20, height=4, heartbeat="off"):
        super(BackupScreen, self).__init__(server, ref)
        self.backup_name = backup_name
        
        self.set_heartbeat(heartbeat)
        self.set_width(width)
        self.set_height(height)

        ## Add title
        self.add_widget(TitleWidget(screen=self, ref="Title", text=self.backup_name))
        ## Create job widget
        self.add_widget(ShutdownWidget(screen=self, ref="ShutdownWidget", y=2))

        ## Create job status widget
        self.add_widget(JobStatusWidget(screen=self, ref="JobStatusWidget", job_name=self.backup_name, y=3))

        ## Create job usage widget
        self.add_widget(UsageWidget(screen=self, ref="JobUsageWidget", job_name=self.backup_name, y=4))

class OverviewScreen(Screen):

    def __init__(self, server, ref, width=20, height=4, heartbeat="off"):
        super(OverviewScreen, self).__init__(server, ref)
        self.set_heartbeat(heartbeat)
        self.set_width(width)
        self.set_height(height)

        self.add_widget(TitleWidget(screen=self, ref="Title", text="steilerGroup-HS"))
        self.add_widget(ShutdownWidget(screen=self, ref="ShutdownWidget", y=2))
        self.add_widget(UsageWidget(screen=self, ref="UsageWidget", job_name="", y=3))
        self.add_widget(RunningJobsWidget(screen=self, ref="RunningJobWidget", y=4))

