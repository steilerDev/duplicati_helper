#!/usr/bin/env python

import time
import datetime
import os.path
import logging

from server import Server
from duplicati_screen import BackupScreen, OverviewScreen

def main():

    # filename='myapp.log'
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.WARNING)

    lcd = Server()
    lcd.start_session()

    logging.warning('Welcome to duplicati lcdproc client')
    logging.warning('Made with <3 by steilerDev (www.github.com/steilerDev)')
    logging.warning('')

    logging.info('Creating overview screen...')
    lcd.add_screen(OverviewScreen(server=lcd, ref="overview"))

    if os.path.isfile("/opt/duplicati_helper/backup.conf"):
        backup_conf = open("/opt/duplicati_helper/backup.conf")
        for line in backup_conf:
            if line and not line.startswith("#"):
                line_array = line.split()
                logging.info('Creating screen for backup job %s...', line_array[0])
                lcd.add_screen(BackupScreen(server=lcd, ref=line_array[0], backup_name=line_array[0]))

    logging.warning('Starting update loop...')
    while True:
        time.sleep(4)
        logging.info('################################################################################')
        lcd.update()

# Run
if __name__ == "__main__":
    main()

