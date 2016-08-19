import urllib

class Widget(object):

    def __init__(self, screen, ref, wtype):
        
        self.screen = screen
        self.ref = ref
        self.wtype = wtype
        self.lastRequest = ""

        self.screen.server.request("widget_add %s %s %s" % (self.screen.ref, self.ref, self.wtype))
        self.update()

    def update_command(self, request):
        if self.lastRequest != request:
            self.lastRequest = request
            self.screen.server.request(request)
    
    def update(self, request):
        if self.lastRequest != request:
            self.lastRequest = request

            print "Updating widget: " + request
            self.screen.server.request(request)

class StringWidget(Widget):

    def __init__(self, screen, ref, text="Text", x=1, y=1):
        
        self.x = x
        self.y = y
        self.text = text
        
        Widget.__init__(self, screen, ref, "string")
   
    def update(self):
        Widget.update(self, 'widget_set %s %s %s %s "%s"' % (self.screen.ref, self.ref, self.x, self.y, self.text))
 
    def set_x(self, x):
        self.x = x
        self.update()
                                   
    
    def set_y(self, y):
        self.y = y
        self.update()
        
    
    def set_text(self, text):
        self.text = text
        self.update()             
        
        
class TitleWidget(Widget):
    
    def __init__(self, screen, ref, text="Title"):
        self.text = text
        Widget.__init__(self, screen, ref, "title")        

    def update(self):
        Widget.update(self, 'widget_set %s %s "%s"' % (self.screen.ref, self.ref, self.text))

    def set_text(self, text):
        self.text = text
        self.update()            
        
        
class HBarWidget(Widget):
    
    def __init__(self, screen, ref, x=1, y=1, length=10):
        self.x = x
        self.y = y
        self.length = length

        Widget.__init__(self, screen, ref, "hbar")
        
    def update(self):
        Widget.update(self, "widget_set %s %s %s %s %s" % (self.screen.ref, self.ref, self.x, self.y, self.length))

    def set_x(self, x):
        self.x = x
        self.update()
                                   
    def set_y(self, y):
        self.y = y
        self.update()
        
    def set_length(self, length):
        self.length = length
        self.update()          
        
                                      
class VBarWidget(Widget):
    
    def __init__(self, screen, ref, x=1, y=1, length=10):
        self.x = x
        self.y = y
        self.length = length

        Widget.__init__(self, screen, ref, "vbar")
        
    def update(self):
        Widget.update(self, "widget_set %s %s %s %s %s" % (self.screen.ref, self.ref, self.x, self.y, self.length))

    def set_x(self, x):
        self.x = x
        self.update()
                                   
    def set_y(self, y):
        self.y = y
        self.update()
        
    def set_length(self, length):
        self.length = length
        self.update()           
        
        
class IconWidget(Widget):
    
    def __init__(self, screen, ref, x=1, y=1, name="heart"):
        self.y = y
        self.name = name

        Widget.__init__(self, screen, ref, "icon")
        
    def update(self):
        Widget.update(self, "widget_set %s %s %s %s %s" % (self.screen.ref, self.ref, self.x, self.y, self.name))

    def set_x(self, x):
        self.x = x
        self.update()
                                   
    def set_y(self, y):
        self.y = y
        self.update()
        
    def set_name(self, name):
        self.name = name
        self.update()        
        
class ScrollerWidget(Widget):
    
    def __init__(self, screen, ref, left=1, top=1, right=20, bottom=1, direction="h", speed=1, text="Message"):
        
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.direction = direction
        self.speed = speed
        self.text = text

        Widget.__init__(self, screen, ref, "scroller")
        
    def update(self):
        Widget.update(self, 'widget_set %s %s %s %s %s %s %s %s "%s"' % (self.screen.ref, 
                                                                  self.ref, 
                                                                  self.left, 
                                                                  self.top, 
                                                                  self.right, 
                                                                  self.bottom, 
                                                                  self.direction, 
                                                                  self.speed, 
                                                                  self.text))

    def set_left(self, left):
        self.left = left
        self.update()
                                   
    def set_top(self, top):
        self.top = top
        self.update()
        
    def set_right(self, right):
        self.right = right
        self.update()   
        
    def set_bottom(self, bottom):
        self.bottom = bottom
        self.update()       
        
    def set_direction(self, direction):
        self.direction = direction
        self.update() 
        
    def set_speed(self, speed):
        self.speed = speed
        self.update()     
        
    def set_text(self, text):
        self.text = text
        self.update()
        
        
class FrameWidget(Widget):
    
    def __init__(self, screen, ref, left=1, top=1, right=20, bottom=1, width=20, height=4, direction="h", speed=1):
        
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.width = width
        self.height = height
        self.direction = direction
        self.speed = speed

        Widget.__init__(self, screen, ref, "frame")
        
    def update(self):
        Widget.update(self, 'widget_set %s %s %s %s %s %s %s %s %s %s' % (self.screen.ref, 
                                                                  self.ref, 
                                                                  self.left, 
                                                                  self.top, 
                                                                  self.right, 
                                                                  self.bottom, 
                                                                  self.width,
                                                                  self.height,
                                                                  self.direction, 
                                                                  self.speed))

    def set_left(self, left):
        self.left = left
        self.update()
                                   
    def set_top(self, top):
        self.top = top
        self.update()
        
    def set_right(self, right):
        self.right = right
        self.update()   
        
    def set_bottom(self, bottom):
        self.bottom = bottom
        self.update()       

    def set_width(self, width):
        self.width = width
        self.update()
        
    def set_height(self, height):
        self.height = height
        self.update()                      
        
    def set_direction(self, direction):
        self.direction = direction
        self.update() 
        
    def set_speed(self, speed):
        self.speed = speed
        self.update()     
                                          
                                          
class NumberWidget(Widget):
    
    def __init__(self, screen, ref, x=1, value=1):
        self.x = x
        self.value = value
        
        Widget.__init__(self, screen, ref, "num")
        
    def update(self):
        Widget.update(self, 'widget_set %s %s %s %s' % (self.screen.ref, 
                                                               self.ref, 
                                                               self.x,
                                                               self.value))

    def set_x(self, x):
        self.x = x
        self.update()
                                   
    def set_value(self, value):
        self.value = value
        self.update()                                                                         
