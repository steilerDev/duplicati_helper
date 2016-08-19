from widgets import StringWidget, TitleWidget, HBarWidget, VBarWidget, IconWidget, ScrollerWidget, FrameWidget,NumberWidget


class Screen(object):

    """ LCDproc Screen Object """

    def __init__(self, server, ref):
        
        """ Constructor """
        
        self.server = server
        self.ref = ref
        self.name = ref
        self.width = None
        self.height = None
        self.priority = None
        self.heartbeat = None
        self.backlight = None
        self.duration = None
        self.timeout = None
        self.cursor = None
        self.cursor_x = None
        self.cursor_y = None
        self.widgets = dict()
        
        self.server.request("screen_add %s" % (ref))
        self.set_cursor("off")
        self.clear()
        
        
    def set_name(self, name):
        
        """ Set Screen Name """
        
        self.name = name
        self.server.request("screen_set %s name %s" % (self.ref, self.name))


    def set_width(self, width):
        
        """ Set Screen Width """
        
        if width > 0 and width <= self.server.server_info.get("screen_width"):
            self.width = width
            self.server.request("screen_set %s wid %i" % (self.ref, self.width))


    def set_height(self, height):

        """ Set Screen Height """
        
        if height > 0 and height <= self.server.server_info.get("screen_height"):
            self.height = height
            self.server.request("screen_set %s hgt %i" % (self.ref, self.height))


    def set_cursor_x(self, x):

        """ Set Screen Cursor X Position """
        
        if x >= 0 and x <= self.server.server_info.get("screen_width"):
            self.cursor_x = x
            self.server.request("screen_set %s cursor_x %i" % (self.ref, self.cursor_x))


    def set_cursor_y(self, y):

        """ Set Screen Cursor Y Position """
        
        if y >= 0 and y <= self.server.server_info.get("screen_height"):
            self.cursor_y = y
            self.server.request("screen_set %s cursor_y %i" % (self.ref, self.cursor_y))


    def set_duration(self, duration):

        """ Set Screen Change Interval Duration """
        
        if duration > 0:
            self.duration = duration
            self.server.request("screen_set %s duration %i" % (self.ref, (self.duration * 8)))


    def set_timeout(self, timeout):

        """ Set Screen Timeout Duration """
        
        if timeout > 0:
            self.timeout = timeout
            self.server.request("screen_set %s timeout %i" % (self.ref, (self.timeout * 8)))


    def set_priority(self, priority):
    
        """ Set Screen Priority Class """
        
        if priority in ["hidden", "background", "info", "foreground", "alert", "input"]:
            self.priority = priority
            self.server.request("screen_set %s priority %s" % (self.ref, self.priority))
        
        
    def set_backlight(self, state):
        
        """ Set Screen Backlight Mode """
        
        if state in ["on", "off", "toggle", "open", "blink", "flash"]:
            self.backlight = state
            self.server.request("screen_set %s backlight %s" % (self.ref, self.backlight))


    def set_heartbeat(self, state):

        """ Set Screen Heartbeat Display Mode """
        
        if state in ["on", "off", "open"]:
            self.heartbeat = state
            self.server.request("screen_set %s heartbeat %s" % (self.ref, self.heartbeat))


    def set_cursor(self, cursor):
        
        """ Set Screen Cursor Mode """
        
        if cursor in ["on", "off", "under", "block"]:
            self.cursor = cursor
            self.server.request("screen_set %s cursor %s" % (self.ref, self.cursor))

            
    def clear(self):
        
        """ Clear Screen """
        for widget in self.widgets.iteritems():
           del_widget(widget.ref) 

        w1 = StringWidget(self, ref="_w1_", text=" "*20, x=1, y=1)
        w2 = StringWidget(self, ref="_w2_", text=" "*20, x=1, y=2)
        w3 = StringWidget(self, ref="_w3_", text=" "*20, x=1, y=3)
        w4 = StringWidget(self, ref="_w4_", text=" "*20, x=1, y=4)
            

    def add_widget(self, widget):
        if widget.ref not in self.widgets:
            self.widgets[widget.ref] = widget
            return self.widgets[widget.ref]

    def del_widget(self, ref):
        """ Delete/Remove A Widget """
        self.server.request("widget_del %s %s" % (self.name, ref))
        del(self.widgets[ref])

    def update(self):
        for ref, widget in self.widgets.iteritems():
            widget.update() 
