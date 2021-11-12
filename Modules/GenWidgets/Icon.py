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
        if not self.pos:
            self.pos = (0,0)
        self.pos = (self.pos[0] - 10, self.pos[1])
        self.size = size
        if not self.size:
            self.size = self.image.get_rect()
        self.size = (self.size[0]+20, self.size[1]+20)
        self.function = function
        
        
        self.surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect(topleft=self.pos)
    
    def draw(self, surf):
        # empty fill to clear what's been drawn
        self.surface.fill((0,0,0,0))
        if within_bounds(pygame.mouse.get_pos(), self.surface_rect):
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)

        self.surface.blit(self.image, (10,0))

        if self.title:
            text = pygame.font.Font(FONT_LATO,14).render(self.title, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.midbottom = (self.size[0]/2,self.size[1])
            self.surface.blit(text, text_rect)

        surf.blit(self.surface, self.surface_rect)
            