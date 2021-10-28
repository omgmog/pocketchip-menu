import pygame
from Modules.Globals import *

class Settings():
    index = Pages.SETTINGS
    title = 'Settings'

    def __init__(self, parent):
        self.visible = False
        self.parent = parent
        self.image = assetpath('settingsBackground.png')

    def do(self, event):
        if self.visible:
            pass

    def update(self):
        if self.visible:
            pass

    def draw(self, surf):
        if self.visible:
            pass

    
if __name__ == '__main__':
    pass