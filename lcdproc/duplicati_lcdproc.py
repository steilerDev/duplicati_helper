#!/usr/bin/env python

import time
import datetime
import os.path

from server import Server
from duplicati_screen import BackupScreen, OverviewScreen

DEBUG=False

def main():

    if DEBUG: print "Debug: on"

    lcd = Server(debug=DEBUG)
    lcd.start_session()

    lcd.add_screen(OverviewScreen(server=lcd, ref="overview_screen"))

    if os.path.isfile("/opt/duplicati_helper/backup.conf"):
        backup_conf = open("/opt/duplicati_helper/backup.conf")
        for line in backup_conf:
            if line and not line.startswith("#"):
                line_array = line.split()
                lcd.add_screen(BackupScreen(server=lcd, ref=line_array[0], backup_name=line_array[0]))

    while True:
        time.sleep(4)
        print "Updating"
        lcd.update()
        
# Run
if __name__ == "__main__":
    main()

