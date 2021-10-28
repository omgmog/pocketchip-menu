import pygame
from Modules.Globals import *

if IS_LINUX:
    from NetworkManager import NetworkManager

class Wifi(Widget):
    def __init__(self, parent=None):
        self.parent = parent
        self.size = (26, 24)
        self.pos = (self.parent.parent.screen.get_width() - self.size[0] - EDGE_PADDING, EDGE_PADDING)
        self.image = None
        self.page = None
        self.persistent = True # always draw
        self.wifi_device = None

        if IS_LINUX:
            for device in NetworkManager.GetAllDevices():
                if device.DeviceType == 2:
                    self.wifi_device = device
        else:
            # on other platforms just show an icon 
            self.image = pygame.transform.scale(pygame.image.load(assetpath('wifi-100.png')).convert_alpha(), self.size)

    def update(self):
        if self.wifi_device is None:
            return
        if self.wifi_device.ActiveConnection is None:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('wifi-disconnected.png')).convert_alpha(), self.size)
            return
        if self.wifi_device.ActiveConnection.Devices[0].ActiveAccessPoint.Strength > 75:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('wifi-100.png')).convert_alpha(), self.size)
            return
        if self.wifi_device.ActiveConnection.Devices[0].ActiveAccessPoint.Strength > 50:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('wifi-75.png')).convert_alpha(), self.size)
            return
        if self.wifi_device.ActiveConnection.Devices[0].ActiveAccessPoint.Strength > 25:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('wifi-50.png')).convert_alpha(), self.size)
            return
        else:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('wifi-25.png')).convert_alpha(), self.size)
            return