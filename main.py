#!/usr/bin/python3

import pygame
from pygame.locals import *

from Modules.Globals import *
from Modules.GenWidgets.Nav import *
from Modules.Screens.Power import *
from Modules.Screens.Apps import *
from Modules.Screens.Settings import *

if IS_LINUX:
    import dbus.mainloop.glib

    main_dbus_loop = dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    dbus.set_default_main_loop(main_dbus_loop)

class Menu:
    pygame.init()
    pygame.display.set_caption('Menu')
    if IS_LINUX:
        pygame.mouse.set_visible(False)

    def __init__(self):
        self.size = (480, 272)
        self.fullscreen = IS_LINUX
        self.screen = pygame.display.set_mode(self.size, self.fullscreen | pygame.DOUBLEBUF)
        self.running = True
        self.visible = True
        self.nav_bar = Nav(self)
        self.active_page = Pages.APPS # start with apps page
        self.pages = []
        self.delta = 0.0
        self.clock = pygame.time.Clock()
        self.dialog = None

    def do(self, eventlist):
        for event in eventlist:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.nav_bar.goToPage(self, "left")
                    pygame.fastevent.post(pygame.event.Event(pygame.USEREVENT, type="screen_update"))
                elif event.key == pygame.K_RIGHT:
                    self.nav_bar.goToPage(self, "right")
                    pygame.fastevent.post(pygame.event.Event(pygame.USEREVENT, type="screen_update"))

            for page in self.pages:
                if page.visible:
                    page.do(event)

            self.nav_bar.do(event)

            if self.dialog and self.dialog.visible:
                    self.dialog.do(event)
            if event.type == pygame.USEREVENT and 'type' in event.__dict__ and event.__dict__['type'] == 'screen_update':
                self.update()
                self.draw()

    def update(self):
        for page in self.pages:
            if page.visible:
                page.update()

    def draw(self):
        self.screen.fill((0,0,0,0))
        page_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        for page in self.pages:
            if page.visible:
                if page.image:
                    page_surface.blit(pygame.image.load(page.image).convert(), (0,0))
                page.draw(page_surface)
        self.nav_bar.draw(page_surface)
        if self.dialog:
            if self.dialog.visible:
                self.dialog.draw(page_surface)
        self.screen.blit(page_surface, page_surface.get_rect())

    def run(self):
        self.pages.append(Power(self))
        self.pages.append(Apps(self))
        self.pages.append(Settings(self))

        while self.running:
            for page in self.pages:
                if page.index == self.active_page:
                    page.visible = True
                else:
                    page.visible = False
            self.do(pygame.fastevent.get())
#            self.update()

            self.delta = self.clock.tick(10) / 1000.0
            pygame.display.update()
        pygame.quit()
        quit()

if __name__ == '__main__':
    pygame.fastevent.init()
    menu = Menu()
    menu.run()
