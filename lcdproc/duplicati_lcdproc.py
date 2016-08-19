#!/usr/bin/env python

import time
import datetime
import os.path

from server import Server
from duplicati_screen import BackupScreen

DEBUG=True

def main():

    if DEBUG: print "Debug: on"

    lcd = Server(debug=DEBUG)
    lcd.start_session()
    
    screens = dict()

    if os.path.isfile("/opt/duplicati_helper/backup.conf"):
        backup_conf = open("/opt/duplicati_helper/backup.conf")
        for line in backup_conf:
            line_array = line.split()
            screen = lcd.add_screen(BackupScreen(server=lcd, ref=line_array[0], backup_name=line_array[0]))
            
            screen.set_heartbeat("off")
            screen.set_width(20)
            screen.set_height(4)
            screens[line_array[0]] = screen

    while True:
        time.sleep(2)
        print "Updating"
        for key, value in screens:
            value.update()
        
# Run
if __name__ == "__main__":
    main()

