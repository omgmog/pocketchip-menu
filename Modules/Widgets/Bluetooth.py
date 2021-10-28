import pygame
from Modules.Globals import *

if IS_LINUX:
    # specific imports here
    pass

class Bluetooth(Widget):
    def __init__(self, parent=None):
        self.parent = parent
        self.size = (26, 24)
        self.pos = (self.parent.parent.screen.get_width() - self.size[0] - SPACE_PADDING - self.parent.widgets[1].size[0] - EDGE_PADDING, EDGE_PADDING)
        self.image = None
        self.page = None
        self.persistent = True # always draw
        self.bt_device = None

        if IS_LINUX:
           # init the bt icon here
           # self.bt_device = Foo
           pass
        else:
            # on other platforms just show an icon 
            self.image = pygame.transform.scale(pygame.image.load(assetpath('bluetooth-connected.png')).convert_alpha(), self.size)

    def update(self):
        if self.bt_device is None:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('bluetooth-disconnected.png')).convert_alpha(), self.size)
            return
        else:
            self.image = pygame.transform.scale(pygame.image.load(assetpath('bluetooth-connected.png')).convert_alpha(), self.size)