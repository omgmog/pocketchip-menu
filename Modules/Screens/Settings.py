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
                pos=(pygame.display.Info().current_w/2, 70),
                function=lambda:print('clicked 1')
            ),
            TextButton(
                text='Testing 2',
                pos=(pygame.display.Info().current_w/2, 120),
                function=lambda:print('clicked 2')
            ),
            TextButton(
                text='Button with lots of text',
                pos=(pygame.display.Info().current_w/2, 170),
                function=lambda:print('wow that was huge')
            ),
            TextButton(
                text='x',
                pos=(pygame.display.Info().current_w/2, 220),
                function=lambda:print('wow that was small')
            )
        ]

    def do(self, event):
        for button in self.buttons:
            button.do(event)

    def update(self):
        pass

    def draw(self, surf):
        for button in self.buttons:
            button.draw(surf)

    
if __name__ == '__main__':
    pass