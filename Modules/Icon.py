import pygame
from Modules.Globals import *

class Icon(Button):
    def __init__(self, image=None, title=None, pos=None, size=None, action=None):
        self.image = image
        if self.image:
            self.image = pygame.image.load(self.image)
        self.title = title
        self.pos = pos
        self.size = size
        if not self.size:
            self.size = self.image.get_rect()
        self.action = action
    
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

def icon_action(icon):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if within_bounds(mouse, icon.pos, icon.size):
        if click[0] == 1 and icon.action != None:
            # print('Clicked icon {}. x:{}, y:{}'.format(icon.title, mouse[0], mouse[1]))
            from subprocess import Popen, PIPE
            process = Popen(icon.action, stdout=PIPE, stderr=PIPE, shell = True)
            stdout, stderr = process.communicate()
            print(stdout)
            if stderr:
                print(stderr)