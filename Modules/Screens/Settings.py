import pygame
from Modules.Globals import *
from Modules.GenWidgets.Widget import TextButton

class Settings():
    index = Pages.SETTINGS
    title = 'Settings'

    def __init__(self, parent):
        self.visible = False
        self.parent = parent
        self.image = assetpath('settingsBackground.png')
        self.buttons = [
            TextButton(
                text='Testing 1',
                pos=(self.parent.screen_center[0], 70),
                function=lambda:print('clicked 1')
            ),
            TextButton(
                text='Testing 2',
                pos=(self.parent.screen_center[0], 120),
                function=lambda:print('clicked 2')
            ),
            TextButton(
                text='Button with lots of text',
                pos=(self.parent.screen_center[0], 170),
                function=lambda:print('wow that was huge')
            ),
            TextButton(
                text='x',
                pos=(self.parent.screen_center[0], 220),
                function=lambda:print('wow that was small')
            )
        ]

    def do(self, event):
        if self.visible:
            for button in self.buttons:
                button.do(event)
            pass

    def update(self):
        if self.visible:
            pass

    def draw(self, surf):
        if self.visible:
            for button in self.buttons:
                button.draw(surf)
            pass

    
if __name__ == '__main__':
    pass