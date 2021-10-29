import pygame
from Modules.Globals import *
from Modules.GenWidgets.Icon import *
import dbus

def reboot():
    bus = dbus.SystemBus()
    obj = bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
    iface = dbus.Interface(obj, 'org.freedesktop.login1.Manager')
    iface.Reboot(1)

def poweroff():
    bus = dbus.SystemBus()
    obj = bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
    iface = dbus.Interface(obj, 'org.freedesktop.login1.Manager')
    iface.PowerOff(1)

class Power():
    index = Pages.POWER
    title = 'Power'

    def __init__(self, parent):
        self.visible = False
        self.parent = parent
        self.iconsize = (64,64)
        self.num_icons = 2
        self.image = assetpath('powerMenuBackground.png')
        self.x_padding = \
            (pygame.display.Info().current_w - (self.iconsize[0] * self.num_icons)) / (self.num_icons + 1)
        self.y_padding = \
            (pygame.display.Info().current_h - self.iconsize[1]) / 2
        self.icons = [Icon(image=assetpath('shutdown.png'),title='Shutdown', pos=(int(self.x_padding),int(self.y_padding)), size=self.iconsize, function=poweroff),
                      Icon(image=assetpath('restart.png'),title='Restart', pos=(int(self.x_padding * 2) + self.iconsize[0],int(self.y_padding)),size=self.iconsize, function=reboot)]

    def do(self, event):
        if self.visible:
            for icon in self.icons:
                try:
                    icon_action(icon=icon)
                except:
                    print(f'Failed to {icon.title} due to dbus error.')

    def update(self):
        if self.visible:
            pass

    def draw(self, surf):
        if self.visible:
            for icon in self.icons:
                icon.draw(surf)
    
if __name__ == '__main__':
    pass
