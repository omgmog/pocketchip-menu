import pygame
import __main__
from Modules.Globals import *
from Modules.NavWidgets.Battery import *
from Modules.NavWidgets.Bluetooth import *
from Modules.NavWidgets.Wifi import *

class Nav():
    def __init__(self, parent):
        self.visible = True
        self.parent = parent
        self.buttons = []
        self.widgets = []

        # go to power from apps
        self.buttons.append(
            PageButton(
                page=Pages.APPS,
                image='powerIcon.png',
                pos=(
                    EDGE_PADDING,
                    self.parent.screen.get_height() - 22 - EDGE_PADDING
                ),
                size=(45,22),
                function=lambda:self.goToPage(self.parent, page=1)
            )
        )
        # go to apps from power
        self.buttons.append(
            PageButton(
                page=Pages.POWER,
                image='nextIcon.png',
                pos=(
                    self.parent.screen.get_width() - 64,
                    self.parent.screen.get_height()/2 - 32
                ),
                size=(64,64),
                function=lambda:self.goToPage(self.parent, page=2)

            )
        )

        # go to settings from apps
        self.buttons.append(
            PageButton(
                page=Pages.APPS,
                image='settingsIcon.png',
                pos=(
                    self.parent.screen.get_width() - 45 - EDGE_PADDING,
                    self.parent.screen.get_height() - 22 - EDGE_PADDING
                ),
                size=(45,22),
                function=lambda:self.goToPage(self.parent, page=3)


            )
        )
        # go to apps from settings
        self.buttons.append(
            PageButton(
                page=Pages.SETTINGS,
                image='backIcon.png',
                pos=(
                    0,
                    self.parent.screen.get_height()/2 - 32
                ),
                size=(64,64),
                function=lambda:self.goToPage(self.parent, page=2)

            )
        )

        self.widgets.append(Battery(parent=self))
        self.widgets.append(Wifi(parent=self))
        self.widgets.append(Bluetooth(parent=self))


    def goToPage(self, menu, direction=None, page=None):
        if page and 1 <= page <= len(menu.pages):
            menu.active_page = page
        else:
            if direction == "left":
                menu.active_page -= 1
                if menu.active_page < 1:
                    menu.active_page = 1
            elif direction == "right":
                menu.active_page += 1
                if menu.active_page >= len(menu.pages):
                    menu.active_page = len(menu.pages)

    def do(self, event):
        if self.parent.visible:
            for button in self.buttons:
                button.do(event)
        if self.visible:
            if event.type == pygame.USEREVENT and 'type' in event.__dict__ and event.__dict__['type'] == 'widget_update':
                for widget in self.widgets:
                    if widget.page == self.parent.active_page or widget.persistent:
                        widget.update()

    def update(self):
        pass

    def draw(self, surf):
        if self.visible:
            print('redrawing page')
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
