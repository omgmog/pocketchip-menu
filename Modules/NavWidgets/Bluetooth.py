import pygame
from Modules.Globals import *
from Modules.GenWidgets.Widget import *
from threading import Thread
from multiprocessing import Value

#these are for dummy signal testing
import time
import random

#test process to update bluetooth every few seconds
def random_bluetooth(connect):
    while True:
        connect.value = random.randint(0,1)
        pygame.fastevent.post(pygame.event.Event(pygame.USEREVENT, type="widget_update"))
        time.sleep(30)

class Bluetooth(Widget):
    def __init__(self, parent=None):
        self.parent = parent
        self.size = (26, 24)
        self.pos = (self.parent.parent.screen.get_width() - self.size[0] - SPACE_PADDING - self.parent.widgets[1].size[0] - EDGE_PADDING, EDGE_PADDING)
        self.image = None
        self.page = None
        self.persistent = True
        self.bt_device = None
        self.bluetooth_connect = Value('i', 1)
        self.bluetooth_thread = Thread(target=random_bluetooth, args=(self.bluetooth_connect,), daemon=True)

        self.bluetooth_thread.start()

    def update(self):
#        commented out for testing
#        if self.bt_device is None or self.persistent is False:
#            return
        self.parent.needs_refresh = True
        if self.bluetooth_connect.value == 0:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('bluetooth-disconnected.png')).convert_alpha(), self.size)
            return
        else:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('bluetooth-connected.png')).convert_alpha(), self.size)
            return
