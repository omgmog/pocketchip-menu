import pygame
from subprocess import Popen, PIPE

from Modules.Globals import *
from Modules.GenWidgets.Widget import *

class Icon(Button):
    def __init__(self, image=None, title=None, pos=None, size=None, function=None):
        self.image = image
        if self.image:
            self.image = pygame.image.load(self.image).convert_alpha()
        self.title = title
        self.pos = pos
        self.size = size
        if not self.size:
            self.size = self.image.get_rect()
        self.function = function
    
    def draw(self, surf):
        if within_bounds(pygame.mouse.get_pos(), self.pos, self.size):
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)

        surf.blit(self.image, self.pos)

        if self.title:
            font = pygame.font.Font(FONT_LATO,14)
            text = font.render(self.title, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.midtop = (self.pos[0]+(self.size[0]/2), self.pos[1]+self.size[1])
            surf.blit(text, text_rect)
            