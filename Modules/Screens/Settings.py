import pygame
from Modules.Globals import *
from Modules.GenWidgets.Widget import TextButton,Slider

class Settings():
    index = Pages.SETTINGS
    title = 'Settings'

    def __init__(self, parent):
        self.visible = False
        self.parent = parent
        self.image = assetpath('settingsBackground.png')
        self.widgets = [
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
            Slider(
                label='Volume',
                size=(200,40),
                pos=((pygame.display.Info().current_w/2) - 100, 150),
                value=75,
                icons=('volumeIconLo.png', 'volumeIconHi.png'),
                function=lambda:print('clicked the slider')
            ),
            Slider(
                label='Brightness',
                size=(200,40),
                pos=((pygame.display.Info().current_w/2) - 100, 200),
                value=50,
                icons=('brightnessIconLo.png', 'brightnessIconHi.png'),
                function=lambda:print('clicked the slider')
            )
        ]

    def do(self, event):
        for widget in self.widgets:
            widget.do(event)

    def update(self):
        for widget in self.widgets:
            if hasattr(widget, 'update'):
                widget.update()
        pass

    def draw(self, surf):
        for widget in self.widgets:
            widget.draw(surf)

    
if __name__ == '__main__':
    pass