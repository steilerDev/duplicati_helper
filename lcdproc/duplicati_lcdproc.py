#!/usr/bin/env python

import time
import datetime

from server import Server
from screen import Screen
from widgets import ScrollerWidget, TitleWidget, StringWidget

DEBUG=True


def main():

    if DEBUG: print "Debug: on"
    #if DEBUG: print "Telnet Request:  %s" % (command_string)

    lcd = Server(debug=DEBUG)
    lcd.start_session()
    
    screen1 = BackupScreen(lcd, "Backup1", "TestName")
    lcd.add_screen(screen1)
    screen1.set_heartbeat("off")
#    screen1.set_duration(10)
    screen1.set_width(20)
    screen1.set_height(4)


    #string_widget = screen.add_string_widget("MyStringWidget", text="TestwWEJIowejioewjio", x=1, y=2)
    #hbar_widget = screen.add_hbar_widget("MyHBarWidget", x=1, y=4, length=60)
    #frame_widget = screen.add_frame_widget("MyFrameWidget")
    
    #num1_widget = screen1.add_number_widget("MyNumber1Widget", x=1, value=0)
    #num2_widget = screen1.add_number_widget("MyNumber2Widget", x=5, value=0)
    #num3_widget = screen1.add_number_widget("MyNumber3Widget", x=9, value=0)    
    #num4_widget = screen1.add_number_widget("MyNumber4Widget", x=13, value=0)    

    progress = 0
    
    while True:
    
        #num1_widget.set_value(progress)
        #num2_widget.set_value(progress)
        #num3_widget.set_value(progress)
        #num4_widget.set_value(progress)                
    
        time.sleep(0.5)
        
        progress = progress + 1
        if progress > 9: progress = 0
        
# Run

class BackupScreen(Screen):

    def __init__(self, server, ref, backup_name):
        super(BackupScreen, self).__init__(server, ref)
        self.backup_name = backup_name
        self.add_widget(TitleWidget(self, ref="Title", text="steilerGroup-HomeServer"))
        self.add_widget(StringWidget(self, ref="Line1", text="Test", x=1, y=2))

if __name__ == "__main__":
    main()

