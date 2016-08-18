from screen import Screen
from duplicati_widget import JobNameWidget

class BackupScreen(Screen)

    def __init__(self, server, ref, backup_name)
        super(BackupScreen, self).__init__(server, ref)
        self.backup_name = backup_name

        ## Add title
        self.add_widget(TitleWidget(self, ref="Title", text="steilerGroup-HomeServer"
        ## Create job widget
        self.add_widget(JobNameWidget(self.screen, "JobNameWidget", self.backup_name, 2))

        ## Create job status widget
        self.add_widget(JobStatusWidget(self.screen, "JobStatusWidget", self.backup_name, 3))

        ## Create job usage widget
        self.add_widget(JobUsageWidget(self.screen, "JobUsageWidget", self.backup_name, 4))
