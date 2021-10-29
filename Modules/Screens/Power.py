import pygame
from Modules.Globals import *
from Modules.GenWidgets.Icon import *
if IS_LINUX:
    import dbus

def reboot():
    if IS_LINUX:
        bus = dbus.SystemBus()
        obj = bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
        iface = dbus.Interface(obj, 'org.freedesktop.login1.Manager')
        iface.Reboot(1)
    else:
        print('reboot')

def poweroff():
    if IS_LINUX:
        bus = dbus.SystemBus()
        obj = bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
        iface = dbus.Interface(obj, 'org.freedesktop.login1.Manager')
        iface.PowerOff(1)
    else:
        print('power off')

class Power():
    index = Pages.POWER
    title = 'Power'

    def __init__(self, parent):
        self.visible = False
        self.parent = parent
        self.image = assetpath('powerMenuBackground.png')
        self.icons = [
            Icon(
                image=assetpath('shutdown.png'),
                title='Shutdown', 
                size=(64,64),
                function=poweroff
            ),
            Icon(
                image=assetpath('restart.png'),
                title='Restart', 
                size=(64,64),
                function=reboot
            ),       
            # Icon(
            #     image=assetpath('restart.png'),
            #     title='FEL Mode',  
            #     size=(64,64),
            #     function=None
            # ),
        ]
        self.num_icons = len(self.icons)

        # calculate icon positions...
        for index,icon in enumerate(self.icons):
            icon_size = icon.size
            x_padding = (pygame.display.Info().current_w - (icon_size[0] * self.num_icons)) / (self.num_icons + 1)
            y_padding = (pygame.display.Info().current_h - icon_size[1]) / 2
            icon.pos = (
                int(x_padding * (index + 1)) + (icon_size[0] * (index )), 
                int(y_padding)
            )

    def do(self, event):
        if self.visible:
            for icon in self.icons:
                try:
                    icon.do(event)
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
