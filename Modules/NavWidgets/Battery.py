import pygame
from Modules.Globals import *
from Modules.GenWidgets.Widget import *
from threading import Thread
from multiprocessing import Value

try:
    import psutil
except:
    print("Library psutil missing")

#these are for dummy battery testing
import time
import random

#test process to update battery every few seconds
def random_battery(charging, capacity):
    while True:
        charging.value = 0
        capacity.value = random.randint(0,100)
        pygame.fastevent.post(pygame.event.Event(pygame.USEREVENT, type="widget_update"))
        time.sleep(60)

class Battery(Widget):
    def __init__(self, parent=None):
        self.parent = parent
        self.size = (24, 24)
        self.pos = (EDGE_PADDING, EDGE_PADDING)
        self.battery_present = False
        self.image = None
        self.page = None
        self.persistent = True
        self.battery_capacity = Value('i', 100)
        self.battery_charging = Value('i', 1)
        self.battery_thread = Thread(target=random_battery, args=(self.battery_charging, self.battery_capacity), daemon=True)

        try:
            if psutil.sensors_battery() is not None:
                self.battery_present = True
                self.battery_thread.start()

#            added for testing
            else:
                self.battery_thread.start()
        except:
#            commented for testing
#            self.persistent = False
#            added for testing
            self.battery_thread.start()

    def update(self):
#        commented for testing
#        if self.battery_present is False or self.persistent is False:
#            return
        self.parent.needs_refresh = True
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

