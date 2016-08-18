#!/usr/bin/env python

import time
import datetime

from server import Server
from screen import Screen
from widgets import ScrollerWidget, TitleWidget, StringWidget
from duplicati_widgets import JobNameWidget, JobStatusWidget

DEBUG=False

def main():

    if DEBUG: print "Debug: on"

    lcd = Server(debug=DEBUG)
    lcd.start_session()
    
    screen = lcd.add_screen(Screen(lcd, "Backup1"))
    screen.set_heartbeat("off")
    screen.set_width(20)
    screen.set_height(4)

    screen.add_widget(JobNameWidget(screen=screen, ref="JobName", job_name="root", y=1))
    screen.add_widget(JobStatusWidget(screen=screen, ref="JobStatus", job_name="root", y=1))

        
# Run
if __name__ == "__main__":
    main()

