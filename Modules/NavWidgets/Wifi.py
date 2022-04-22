import pygame
from Modules.Globals import *
from Modules.GenWidgets.Widget import *
from threading import Thread
from multiprocessing import Value

try:
    from NetworkManager import NetworkManager
except:
    print("Network Manager Not Found!")

#these are for dummy signal testing
import time
import random

#test process to update wifi every few seconds
def random_signal_strength(connect, signal):
    while True:
        connect.value = 1
        signal.value = random.randint(0,100)
        pygame.fastevent.post(pygame.event.Event(pygame.USEREVENT, type="screen_update"))
        time.sleep(10)

class Wifi(Widget):
    def __init__(self, parent=None):
        self.parent = parent
        self.size = (26, 24)
        self.pos = (self.parent.parent.screen.get_width() - self.size[0] - EDGE_PADDING, EDGE_PADDING)
        self.image = None
        self.page = None
        self.persistent = True
        self.wifi_device = None
        self.wifi_signal = Value('i', 100)
        self.wifi_connect = Value('i', 1)
        self.wifi_thread = Thread(target=random_signal_strength, args=(self.wifi_connect, self.wifi_signal), daemon=True)

        try:
            for device in NetworkManager.GetAllDevices():
                if device.DeviceType == 2:
                    self.wifi_device = device
                    self.wifi_thread.start()
        except:
#            commented out for testing
#            self.persistent = False

#            added for testing
             self.wifi_thread.start()

    def update(self):
#        commented out for testing
#        if self.wifi_device is None or self.persistent is False:
#            return
        if self.wifi_connect.value == 0:
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
