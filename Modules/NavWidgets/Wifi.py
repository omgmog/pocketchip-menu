import pygame
from Modules.Globals import *
import Modules.DBusMain as DBusMain
import dbus
from Modules.GenWidgets.Widget import *
from multiprocessing import Value

class Wifi(Widget):
    def __init__(self, parent=None):
        self.parent = parent
        self.size = (26, 24)
        self.pos = (self.parent.parent.screen.get_width() - self.size[0] - EDGE_PADDING, EDGE_PADDING)
        self.image = None
        self.page = None
        self.persistent = True
        self.wifi_device = None
        self.wifi_connection = None
        self.wifi_signal = Value('i', 100)
        self.wifi_status = Value('i', 1)

        try:
            self.get_wifi_dev()
            self.persistent = True
        except:
            self.persistent = False
        if self.wifi_device is not None:
            try:
                self.get_active_wifi_connection()
                DBusMain.DBUS_BUS.add_signal_receiver(self.dbus_signal_handler,
                                                      bus_name='org.freedesktop.NetworkManager',
                                                      dbus_interface='org.freedesktop.DBus.Properties',
                                                      signal_name='PropertiesChanged',
                                                      path=self.wifi_device)
            except:
                self.wifi_connection = None
        if self.wifi_connection is not None:
            try:
                self.get_wifi_connection_strength()
                DBusMain.DBUS_BUS.add_signal_receiver(self.dbus_signal_handler,
                                                      bus_name='org.freedesktop.NetworkManager',
                                                      dbus_interface='org.freedesktop.DBus.Properties',
                                                      signal_name='PropertiesChanged',
                                                      path=self.wifi_connection)
            except:
                self.wifi_signal = 0

    def dbus_signal_handler(self, interface, data, type):
        #added print for testing
        print(data)
        update = False
        if 'Strength' in data and int(data['Strength']) != self.wifi_signal.value:
            self.wifi_signal.value = int(data['Strength'])
            update = True
        if 'ActiveAccessPoint' in data and str(data['ActiveAccessPoint']) != self.wifi_connection:
            self.wifi_connection = str(data['ActiveAccessPoint'])
            update = True
        if update is True:
            #added print for testing
            print("Updated")
            pygame.fastevent.post(pygame.event.Event(pygame.USEREVENT, type="screen_update"))
            update = False

    def get_wifi_dev(self):
        proxy = DBusMain.DBUS_BUS.get_object('org.freedesktop.NetworkManager',
                                             '/org/freedesktop/NetworkManager')
        getmanager = dbus.Interface(proxy, 'org.freedesktop.NetworkManager')
        devices = getmanager.GetDevices()
        for device in devices:
            deviceobject = DBusMain.DBUS_BUS.get_object('org.freedesktop.NetworkManager',device)
            deviceinterface = dbus.Interface(deviceobject, dbus_interface='org.freedesktop.DBus.Properties')
            if deviceinterface.Get('org.freedesktop.NetworkManager.Device', 'DeviceType') == 2:
                self.wifi_device = device

    def get_active_wifi_connection(self):
        proxy = DBusMain.DBUS_BUS.get_object('org.freedesktop.NetworkManager', self.wifi_device)
        getmanager = dbus.Interface(proxy, dbus_interface='org.freedesktop.DBus.Properties')
        self.wifi_connection = str(getmanager.Get('org.freedesktop.NetworkManager.Device.Wireless','ActiveAccessPoint'))

    def get_wifi_connection_strength(self):
        apobject = DBusMain.DBUS_BUS.get_object('org.freedesktop.NetworkManager', self.wifi_connection)
        apinterface = dbus.Interface(apobject,dbus_interface='org.freedesktop.DBus.Properties')
        self.wifi_signal.value = int(apinterface.Get('org.freedesktop.NetworkManager.AccessPoint', 'Strength'))

    def update(self):
        if self.wifi_device is None or self.persistent is False:
            return
        if self.wifi_status.value == 0:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('wifi-disconnected.png')).convert_alpha(), self.size)
            return
        if self.wifi_signal.value > 75:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('wifi-100.png')).convert_alpha(), self.size)
            return
        if self.wifi_signal.value > 50:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('wifi-75.png')).convert_alpha(), self.size)
            return
        if self.wifi_signal.value > 25:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('wifi-50.png')).convert_alpha(), self.size)
            return
        else:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('wifi-25.png')).convert_alpha(), self.size)
            return
