import pygame
from Modules.Globals import *
import Modules.DBusMain as DBusMain
import dbus
from Modules.GenWidgets.Widget import *
from multiprocessing import Value

class Bluetooth(Widget):
    def __init__(self, parent=None):
        self.parent = parent
        self.size = (26, 24)
        self.pos = (self.parent.parent.screen.get_width() - self.size[0] - SPACE_PADDING - self.parent.widgets[1].size[0] - EDGE_PADDING, EDGE_PADDING)
        self.image = None
        self.page = None
        self.persistent = False
        self.bt_device = None
        self.bluetooth_connect = Value('i', 0)
        self.bluetooth_power = Value('i', 1)

        try:
            self.get_bluetooth_device()
            self.get_bluetooth_state()
            DBusMain.DBUS_BUS.add_signal_receiver(self.dbus_signal_handler,
                                                  bus_name='org.bluez',
                                                  dbus_interface='org.freedesktop.DBus.Properties',
                                                  signal_name='PropertiesChanged',
                                                  path=self.bt_device)
            self.persistent = True
        except:
            self.persistent = False

    def dbus_signal_handler(self, interface, data, type):
        update = False
        if 'Powered' in data and int(data['Powered']) != self.bluetooth_power.value:
            self.bluetooth_power.value = int(data['Powered'])
            update = True
        if 'Connected' in data and int(data['Connected']) != self.bluetooth_connect.value:
            self.bluetooth_connect.value = int(data['Connected'])
            update = True
        if update is True:
            pygame.fastevent.post(pygame.event.Event(pygame.USEREVENT, type="screen_update"))
            update = False
        return

    def get_bluetooth_device(self):
        proxy = DBusMain.DBUS_BUS.get_object('org.bluez','/')
        get_manager = dbus.Interface(proxy, 'org.freedesktop.DBus.ObjectManager')
        objects = get_manager.GetManagedObjects()
        for item in objects:
            if 'org.bluez.Adapter1' in objects[item]:
                self.bt_device = item

    def get_bluetooth_state(self):
        try:
            proxy = DBusMain.DBUS_BUS.get_object('org.bluez',self.bt_device)
            get_manager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
            self.bluetooth_power.value = int(get_manager.Get('org.bluez.Adapter1','Powered'))
        except:
            self.bluetooth_power.value = 0
        try:
            proxy = DBusMain.DBUS_BUS.get_object('org.bluez',bt_object_path)
            get_manager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
            self.bluetooth_connect.value = int(get_manager.Get('org.bluez.Device1','Connected'))
        except:
            self.bluetooth_connect.value = 0

    def update(self):
        if self.bt_device is None or self.persistent is False:
            return
        if self.bluetooth_connect.value == 0:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('bluetooth-disconnected.png')).convert_alpha(), self.size)
            return
        else:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('bluetooth-connected.png')).convert_alpha(), self.size)
            return
