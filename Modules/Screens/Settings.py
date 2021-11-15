import pygame
from Modules.Globals import *
from Modules.GenWidgets.Widget import TextButton,Slider
import dbus
import os

def get_backlight_name():
    try:
        return os.listdir('/sys/class/backlight')[0]
    except:
        return None #if none, should not show slider at all

def get_backlight_max(backlight_name):
    with open('/sys/class/backlight/'+backlight_name+'/max_brightness') as f:
        max_brightness = int(f.readline())
    return max_brightness

def get_backlight_value(backlight_name):
    with open('/sys/class/backlight/'+backlight_name+'/brightness') as f:
        brightness = int(f.readline())
    return brightness

def set_backlight(backlight_name, value):
    bus = dbus.SystemBus()
    obj = bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1/session/auto')
    iface = dbus.Interface(obj, 'org.freedesktop.login1.Session')
    iface.SetBrightness('backlight', backlight_name, value)

class Settings():
    index = Pages.SETTINGS
    title = 'Settings'

    def __init__(self, parent):
        self.visible = False
        self.parent = parent
        self.image = assetpath('settingsBackground.png')
        self.backlight_name = get_backlight_name()
        self.volume_slider = Slider(
            label='Volume',
            size=(200,40),
            pos=((pygame.display.Info().current_w/2) - 100, 150),
            value=75,
            icons=('volumeIconLo.png', 'volumeIconHi.png'),
            function=lambda self=self:print('clicked the slider')
        )
        if self.backlight_name is not None:
            self.brightness_slider = Slider(
                label='Brightness',
                size=(200,40),
                pos=((pygame.display.Info().current_w/2) - 100, 200),
                value=get_backlight_value(self.backlight_name),
                icons=('brightnessIconLo.png', 'brightnessIconHi.png'),
                function=lambda self=self:set_backlight(self.backlight_name, self.brightness_slider.value),
                minVal=0,
                maxVal=10
            )
        self.widgets = [
            TextButton(
                text='Set volume to 100',
                pos=(pygame.display.Info().current_w/2, 70),
                function=lambda:self.volume_slider.setValue(100)
            ),
            self.volume_slider
        ]
        if self.backlight_name is not None:
            self.widgets.append(self.brightness_slider)

    def do(self, event):
        for widget in self.widgets:
            widget.do(event)

    def update(self):
        for widget in self.widgets:
            if hasattr(widget, 'update'):
                widget.update()
        pass

    def draw(self, surf):
        for widget in self.widgets:
            widget.draw(surf)

    
if __name__ == '__main__':
    pass
