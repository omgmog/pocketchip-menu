import pygame
from Modules.Globals import *
import Modules.DBusMain as DBusMain
import dbus
from Modules.GenWidgets.Widget import *
from multiprocessing import Value

class Battery(Widget):
    def __init__(self, parent=None):
        self.parent = parent
        self.size = (24, 24)
        self.pos = (EDGE_PADDING, EDGE_PADDING)
        self.image = None
        self.page = None
        self.persistent = True
        self.battery_capacity = Value('i', 100)
        self.battery_charging = Value('i', 1)

        try:
            if self.check_battery():
                self.persistent = True
                self.get_battery_details(self.battery_charging, self.battery_capacity)
                DBusMain.DBUS_BUS.add_signal_receiver(self.dbus_signal_handler,
                                                      bus_name='org.freedesktop.UPower',
                                                      dbus_interface='org.freedesktop.DBus.Properties',
                                                      signal_name='PropertiesChanged',
                                                      path='/org/freedesktop/UPower/devices/DisplayDevice')
        except:
            self.persistent = False

    def check_battery(self):
        proxy = DBusMain.DBUS_BUS.get_object('org.freedesktop.UPower',
                               '/org/freedesktop/UPower/devices/DisplayDevice')
        powerdev = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
        return bool(powerdev.Get('org.freedesktop.UPower.Device','IsPresent'))

    def dbus_signal_handler(self, interface, data, type):
        update = False
        if 'State' in data and int(data['State']) != self.battery_charging.value:
            self.battery_charging.value = int(data['State'])
            update = True
        if 'Percentage' in data and int(data['Percentage']) != self.battery_capacity.value:
            self.battery_capacity.value = int(data['Percentage'])
            update = True
        if update is True:
            pygame.fastevent.post(pygame.event.Event(pygame.USEREVENT, type="screen_update"))
            update = False
        return

    def get_battery_details(self, charging, capacity):
        proxy = DBusMain.DBUS_BUS.get_object('org.freedesktop.UPower',
                               '/org/freedesktop/UPower/devices/DisplayDevice')
        getmanager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
        update_battery = False
        try:
            new_capacity = int(getmanager.Get('org.freedesktop.UPower.Device', 'Percentage'))
            if new_capacity != capacity.value:
                capacity.value = new_capacity
                update_battery = True
            new_status = int(getmanager.Get('org.freedesktop.UPower.Device','State'))
            if new_status != charging.value:
                charging.value = new_status
                update_battery = True
        except:
            print("Error reading battery")
        if update_battery is True:
            pygame.fastevent.post(pygame.event.Event(pygame.USEREVENT, type="screen_update"))
            update_battery = False
        return None

    def update(self):
        if self.persistent is False:
            return
        if self.battery_charging.value == 1:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('battery-charging.png')).convert_alpha(), self.size)
            return
        if self.battery_capacity.value > 75:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('battery-100.png')).convert_alpha(), self.size)
            return
        if self.battery_capacity.value > 50:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('battery-75.png')).convert_alpha(), self.size)
            return
        if self.battery_capacity.value > 25:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('battery-50.png')).convert_alpha(), self.size)
            return
        else:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('battery-25.png')).convert_alpha(), self.size)
            return

