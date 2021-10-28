import pygame
from pygame.locals import *

from Modules.Globals import *
from Modules.Nav import *
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
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
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

    def goToPage(self, direction=None, page=None):
        if page and 1 <= page <= len(self.pages):
            self.active_page = page
        else:
            if direction == "left":
                self.active_page -= 1
                if self.active_page < 1:
                    self.active_page = 1
            elif direction == "right":
                self.active_page += 1
                if self.active_page >= len(self.pages):
                    self.active_page = len(self.pages)

    def do(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.goToPage("left")
            elif event.key == pygame.K_RIGHT:
                self.goToPage("right")
        
        for page in self.pages:
            page.do(event)

        self.nav_bar.do(event)
            
    def update(self):
        for page in self.pages:
            page.update()

        self.nav_bar.update()

        self.delta = self.clock.tick(30) / 1000.0

    def draw(self):
        for page in self.pages:
            if page.visible:
                if page.image:
                    self.screen.blit(pygame.image.load(page.image).convert_alpha(), (0,0))
            page.draw(self.screen)
            
        self.nav_bar.draw(self.screen)

        pygame.display.update()

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
        pygame.quit()
        quit()

# kick it off

if __name__ == '__main__':
    menu = Menu()
    menu.run()