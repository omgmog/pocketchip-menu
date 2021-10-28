import pygame
from Modules.Globals import *

class Battery(Widget):
    def __init__(self, parent=None):
        self.parent = parent
        self.size = (24, 24)
        self.pos = (EDGE_PADDING, EDGE_PADDING)
        self.battery_present = False
        self.image = None
        self.page = None
        self.persistent = True # always draw
        
        if IS_LINUX:
            import psutil
            if psutil.sensors_battery() is not None:
                self.battery_present = True
        else:
            # on other platforms just show an icon 
            self.image = pygame.transform.scale(pygame.image.load(assetpath('battery-100.png')), self.size)
    def update(self):
        if self.battery_present is False:
            return

        battery_data = psutil.sensors_battery()
        if battery_data is None:
            return
        if battery_data.power_plugged is True:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('battery-charging.png')), self.size)
            return
        if battery_data.percent > 75:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('battery-100.png')), self.size)
            return
        if battery_data.percent > 50:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('battery-75.png')), self.size)
            return
        if battery_data.percent > 25:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('battery-50.png')), self.size)
            return
        else:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('battery-25.png')), self.size)


