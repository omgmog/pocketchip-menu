import sys
import os
import __main__
import pygame

IS_LINUX = sys.platform[:3] == 'lin'
BASE_DIR = os.path.dirname(__main__.__file__) or '.'
APPS_DIR = os.path.normpath(os.path.join(BASE_DIR, 'apps'))
ASSETS_DIR = os.path.normpath(os.path.join(BASE_DIR, 'assets/ui'))
ICONS_DIR = os.path.normpath(os.path.join(BASE_DIR, 'icons'))
FONT_LATO = os.path.join(ASSETS_DIR, 'Lato-Regular.ttf')

EDGE_PADDING = 10

class Pages:
    POWER = 1
    APPS = 2
    SETTINGS = 3


def within_bounds(mouse,pos,area):
    in_bounds = pos[0]+area[0]>mouse[0]>pos[0] and pos[1]+area[1]>mouse[1]>pos[1]
    return in_bounds

def assetpath(filename, path=ASSETS_DIR):
    return os.path.join(path, filename)

def iconpath(filename):
    return assetpath(filename, path=ICONS_DIR)

class Drawable():
    def __init__(self, image=None, pos=(0,0), size=None):
        self.image = image
        if self.image:
            self.image = pygame.image.load(self.image)
        self.pos = pos
        self.size = size
        if not self.size:
            self.size = self.image.get_rect()
    def draw(self, surf):
        if self.image:
            surf.blit(self.image, self.pos)

class Button(Drawable):
    def __init__(self, image=None, pos=(0,0), size=(0,0), action=None):
        self.image = image
        self.pos = pos
        self.size = size
        self.action = action
    
    def do(self, event):
        pass

class PageButton(Button):
    def __init__(self, parent=None, image=None, pos=(0,0), size=(0,0), action=None, page=None, target=None):
        self.parent = parent
        self.image = image
        self.pos = pos
        self.size = size
        self.action = action
        self.page = page
        self.target = target
    
    def draw(self, surf):
        if self.image:
            image_path = os.path.join(ASSETS_DIR, self.image)
            button_image = pygame.image.load(image_path)
            if self.size:
                button_image = pygame.transform.scale(button_image, self.size)

            if within_bounds(pygame.mouse.get_pos(), self.pos, self.size):
                button_image.set_alpha(100)
            else:
                button_image.set_alpha(255)

            surf.blit(button_image, self.pos)

    def do(self, event):
        if self.target:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if within_bounds(mouse, self.pos, self.size):
                if click[0] == 1:
                    self.parent.goToPage(page=self.target)

class Widget():
    def draw(self, surf):
        if self.image:
            surf.blit(self.image, self.pos)