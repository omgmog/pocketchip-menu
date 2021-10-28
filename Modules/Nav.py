import pygame
import __main__
from Modules.Globals import *
from Modules.Widgets.Battery import *
from Modules.Widgets.Bluetooth import *
from Modules.Widgets.Wifi import *

class Nav():
    def __init__(self, parent):
        self.visible = True
        self.parent = parent
        self.buttons = []
        self.widgets = []

        # go to power from apps
        self.buttons.append(
            PageButton(
                parent=self.parent,
                page=Pages.APPS,
                target=1,
                image='powerIcon.png',
                pos=(
                    EDGE_PADDING, 
                    self.parent.screen.get_height() - 22 - EDGE_PADDING
                ),
                size=(45,22)
            )
        )
        # go to apps from power
        self.buttons.append(
            PageButton(
                parent=self.parent,
                page=Pages.POWER,
                target=2,
                image='nextIcon.png',
                pos=(
                    self.parent.screen.get_width() - 64, 
                    self.parent.screen.get_height()/2 - 32
                ),
                size=(64,64)

            )
        )

        # go to settings from apps
        self.buttons.append(
            PageButton(
                parent=self.parent,
                page=Pages.APPS,
                target=3,
                image='settingsIcon.png',
                pos=(
                    self.parent.screen.get_width() - 45 - EDGE_PADDING, 
                    self.parent.screen.get_height() - 22 - EDGE_PADDING
                ),
                size=(45,22)
            )
        )
        # go to apps from settings
        self.buttons.append(
            PageButton(
                parent=self.parent,
                page=Pages.SETTINGS,
                target=2,
                image='backIcon.png',
                pos=(
                    0, 
                    self.parent.screen.get_height()/2 - 32
                ),
                size=(64,64)

            )
        )

        self.widgets.append(Battery(parent=self))
        self.widgets.append(Wifi(parent=self))
        self.widgets.append(Bluetooth(parent=self))

    def do(self, event):
        if self.parent.visible:
            for button in self.buttons:
                button.do(event)

    def update(self):
        if self.visible:
            # update widgets
            for widget in self.widgets:
                if widget.page == self.parent.active_page or widget.persistent:
                    widget.update()

    def draw(self, surf):
        if self.visible:
            # draw page title
            font = pygame.font.Font(FONT_LATO,20)
            text = font.render(self.parent.pages[self.parent.active_page-1].title, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.midtop = (surf.get_width() / 2, EDGE_PADDING)
            surf.blit(text, text_rect)

            # draw widgets
            for widget in self.widgets:
                if widget.page == self.parent.active_page or widget.persistent:
                    widget.draw(surf)

            # draw nav buttons
            for button in self.buttons:
                if button.page == self.parent.active_page:
                    button.draw(surf)


if __name__ == '__main__':
    pass