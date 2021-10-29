import pygame
from Modules.Globals import *

class Widget():
    def draw(self, surf):
        if self.image:
            surf.blit(self.image, self.pos)


class Drawable():
    def __init__(self, image=None, pos=(0,0), size=None):
        self.image = image
        self.pos = pos
        self.size = size
        self.text_rect = None
        if self.image:
            self.image = pygame.image.load(self.image).convert_alpha()
            if not self.size:
                self.size = self.image.get_rect()
    def draw(self, surf):
        if self.image:
            surf.blit(self.image, self.pos)


class Button(Drawable):
    def __init__(self, image=None, pos=None, size=None, function=None):
        self.image = image
        self.pos = pos
        self.size = size
        self.function = function
    
    def do(self, event):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if within_bounds(mouse, self.pos, self.size):
            if event.type == pygame.MOUSEBUTTONDOWN \
            and click[0] == True \
            and self.function != None:
                self.function()

class TextButton(Button):
    def __init__(self, text=None, pos=None, size=None, function=None, fillcolor=(226,116,154), bordercolor=(255,255,255), textcolor=(255,255,255)):
        self.pos = pos
        self.size = size
        self.function = function
        self.text = text
        self.rendered_text = None
        self.fillcolor = fillcolor
        self.bordercolor = bordercolor
        self.textcolor = textcolor
        
        if self.text:
            font = pygame.font.Font(FONT_LATO,20)
            self.rendered_text = font.render(self.text, True, self.textcolor)
            self.text_rect = self.rendered_text.get_rect(center=self.pos)
            if not self.size:
                self.size = (self.text_rect[2], self.text_rect[3])

    def draw(self, surf):
        if self.rendered_text:
            button_rect = pygame.Rect(
                self.pos[0] - (self.size[0]/2) - BUTTON_PADDING[0],
                self.pos[1] - (self.size[1]/2) - BUTTON_PADDING[1],
                self.size[0] + BUTTON_PADDING[0] + BUTTON_PADDING[2],
                self.size[1] + BUTTON_PADDING[1] + BUTTON_PADDING[3]
            )
            # draw the button structure
            button = pygame.Surface((button_rect[2],button_rect[3]), pygame.SRCALPHA)
            if within_bounds(pygame.mouse.get_pos(), (button_rect[0], button_rect[1]), (button_rect[2], button_rect[3])):
                pygame.draw.rect(button, self.fillcolor, pygame.Rect(0, 0, button_rect[2], button_rect[3]))
            pygame.draw.rect(button, self.bordercolor, pygame.Rect(0, 0, button_rect[2], button_rect[3]), 3)
            # draw the button text
            button.blit(self.rendered_text, self.rendered_text.get_rect(topleft=(BUTTON_PADDING[0],BUTTON_PADDING[1])))
            surf.blit(button, button_rect)

class PageButton(Button):
    def __init__(self, parent=None, image=None, pos=(0,0), size=(0,0), page=None, function=None):
        self.parent = parent
        self.image = image
        self.pos = pos
        self.size = size
        self.page = page
        self.function = function
    
    def draw(self, surf):
        if self.image:
            image_path = os.path.join(ASSETS_DIR, self.image)
            button_image = pygame.image.load(image_path).convert_alpha()
            if self.size:
                button_image = pygame.transform.scale(button_image, self.size)

            if within_bounds(pygame.mouse.get_pos(), self.pos, self.size):
                button_image.set_alpha(100)
            else:
                button_image.set_alpha(255)

            surf.blit(button_image, self.pos)
