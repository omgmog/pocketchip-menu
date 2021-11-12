import pygame
from Modules.Globals import *
from Modules.GenWidgets.Icon import *
if IS_LINUX:
    import dbus

def reboot(self):
    if IS_LINUX:
        bus = dbus.SystemBus()
        obj = bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
        iface = dbus.Interface(obj, 'org.freedesktop.login1.Manager')
        iface.Reboot(1)
    else:
        print('reboot')
    notice(self, 'Rebooting...')

def poweroff(self):
    if IS_LINUX:
        bus = dbus.SystemBus()
        obj = bus.get_object('org.freedesktop.login1', '/org/freedesktop/login1')
        iface = dbus.Interface(obj, 'org.freedesktop.login1.Manager')
        iface.PowerOff(1)
    else:
        print('power off')
    notice(self, 'Shutting down...')

def notice(self, message):
    self.parent.dialog = ConfirmDialog(parent=self.parent, message=message)
    self.parent.dialog.show()

def yesno(self, then):
    self.parent.dialog = ConfirmDialog(parent=self.parent, options=[
        {
            'label':'Yes',
            'function':lambda:then(self)
        },
        {
            'label':'No',
            'function':'hide'
        }
    ])

    self.parent.dialog.show()

class Power():
    index = Pages.POWER
    title = 'Power'

    def __init__(self, parent):
        self.visible = False
        self.parent = parent
        self.image = assetpath('powerMenuBackground.png')
        self.icon_data = [
            ('shutdown.png', 'Shutdown', (64,64), lambda:yesno(self, poweroff)),
            ('restart.png', 'Restart', (64,64), lambda:yesno(self, reboot))
        ]
        self.num_icons = len(self.icon_data)
        self.icons = []

        for index,icon_data in enumerate(self.icon_data):
            icon_size = icon_data[2]
            x_padding = (pygame.display.Info().current_w - (icon_size[0] * self.num_icons)) / (self.num_icons + 1)
            y_padding = (pygame.display.Info().current_h - icon_size[1]) / 2

            self.icons.append(Icon(
                image=assetpath(icon_data[0]),
                title=icon_data[1],
                size=icon_size,
                function=icon_data[3],
                pos=(
                    int(x_padding * (index + 1)) + (icon_size[0] * index), 
                    int(y_padding)
                )
            ))

    def do(self, event):
        if not self.parent.dialog:
            for icon in self.icons:
                try:
                    icon.do(event)
                except:
                    print(f'Failed to {icon.title} due to dbus error.')

    def update(self):
        if self.visible:
            pass

    def draw(self, surf):
        for icon in self.icons:
            icon.draw(surf)
    
if __name__ == '__main__':
    pass
