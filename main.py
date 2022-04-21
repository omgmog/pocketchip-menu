#!/usr/bin/python3

import pygame
from pygame.locals import *

from Modules.Globals import *
from Modules.GenWidgets.Nav import *
from Modules.Screens.Power import *
from Modules.Screens.Apps import *
from Modules.Screens.Settings import *

if IS_LINUX:
    from single_process import single_process
    import dbus.mainloop.glib

    single_process()
    main_dbus_loop = dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    dbus.set_default_main_loop(main_dbus_loop)


class Menu:
    pygame.init()
    pygame.display.set_caption('Menu')
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
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

    def do(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.nav_bar.goToPage(self, "left")
            elif event.key == pygame.K_RIGHT:
                self.nav_bar.goToPage(self, "right")
        
        for page in self.pages:
            if page.visible:
                page.do(event)

        self.nav_bar.do(event)

        if self.dialog and self.dialog.visible:
                self.dialog.do(event)
            
    def update(self):
        for page in self.pages:
            if page.visible:
                page.update()

        self.nav_bar.update()

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

        # debug center
        # pygame.draw.rect(self.screen, (255,255,0), pygame.Rect(self.size[0]/2,self.size[1]/2,0,0),3)

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
            self.do(pygame.event.wait())
            self.update()
            self.draw()

            self.delta = self.clock.tick(30) / 1000.0
            pygame.display.update()
        pygame.quit()
        quit()

# kick it off

if __name__ == '__main__':
    menu = Menu()
    menu.run()
