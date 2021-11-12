import pygame
from Modules.Globals import *

class Widget():
    def draw(self, surf):
        if self.image:
            surf.blit(self.image, self.pos)

class Slider():
    def __init__(self, size=None, pos=None, label=None, function=None, value=50, minVal=0, maxVal=100):
        self.size = size
        self.pos = pos
        self.label = label
        self.value = value
        self.min = minVal
        self.max = maxVal
        self.function = function

        self.surface = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect(topleft=self.pos)

        self.handle_width = 10
        self.handle_x = ((self.size[0]/self.max)*self.value) - (self.handle_width/2)
        

    def update(self):
        self.handle_x = ((self.size[0]/self.max)*self.value) - (self.handle_width/2)

    def draw(self, surf):
        # container
        self.surface.fill((0,0,0,0))
        # rail
        rail = pygame.Surface((self.size[0], self.size[1]-30), pygame.SRCALPHA)
        rail.fill((255,255,255, 80))
        # handle
        handle = pygame.Surface((self.handle_width,self.size[1]), pygame.SRCALPHA)
        handle.fill((255,255,255))


        self.surface.blit(rail, (0,25))
        self.surface.blit(handle, (self.handle_x,20))
        font = pygame.font.Font(FONT_LATO,14)
        if self.label:
            text_string = '{}: {}'.format(self.label, self.value)
        else: 
            text_string = str(self.value)
        rendered_text = font.render(text_string, True, (255,255,255))
        text_rect = rendered_text.get_rect(midtop=(self.size[0]/2,0))
        self.surface.blit(rendered_text, text_rect)

        surf.blit(self.surface, self.pos)

        pass
    def do(self, event):
        # using click detection rather than events so we can drag the slider
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if within_bounds(mouse, self.surface_rect):
            if click[0] == 1:
                slider_width = self.size[0]
                clicked_pos = mouse[0] - self.pos[0]
                self.value = (self.max/slider_width) * clicked_pos
            if event.type == pygame.MOUSEBUTTONUP:
                if self.function != None: 
                    print('clicked Slider "{}"'.format(self.label))
                    self.function()

class ConfirmDialog():
    def __init__(self, parent=None, message='Are you sure?', options=None):
        self.parent = parent
        self.message = message
        self.options = options
        self.visible = False
        self.buttons = []
        self.size = (pygame.display.Info().current_w,pygame.display.Info().current_h)
        self.surface = pygame.Surface(self.parent.size, pygame.SRCALPHA)

        if self.options:
            for index,option in enumerate(self.options):
                # print(option.get('label'))
                function = option.get('function')
                if function == 'hide':
                    function = lambda:self.hide()

                button_width = 60
                x_padding = (self.size[0] - (button_width * len(self.options))) / (len(self.options) + 1)
                y_padding = (self.size[1] - 100)
                self.buttons.append(TextButton(
                    text=option.get('label'),
                    function=function,
                    pos=(
                        int(x_padding * (index + 1)) + (button_width * index) + (button_width/2),
                        int(y_padding)
                    ),
                    size=(button_width,40)
                ))

    def draw(self, surf):
        # empty fill to clear what's been drawn
        self.surface.fill((0,0,0,0))
        
        # draw a background fill
        dialog_rect = pygame.Rect(0,0, self.size[0], self.size[1], topleft=(0,0))
        pygame.draw.rect(self.surface, (100,100,100), dialog_rect)

        if self.message:
            text = pygame.font.Font(FONT_LATO, 20).render(self.message, True, (255,255,255))
            if self.buttons:
                text_rect = text.get_rect(center=(self.size[0]/2, 40))
            else: 
                text_rect = text.get_rect(center=(self.size[0]/2, self.size[1]/2))
            self.surface.blit(text, text_rect)

        for button in self.buttons:
            button.draw(self.surface)
        surf.blit(self.surface, (0,0))

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False
        self.parent.dialog = None
    
    def do(self, event):
        for button in self.buttons:
            button.do(event)

class Button():
    def __init__(self, image=None, pos=None, size=None, function=None):
        self.image = image
        self.pos = pos
        self.size = size
        self.function = function
        
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect(center=self.pos)
    
    def do(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            if within_bounds(mouse, self.surface_rect):
                if self.function != None: 
                    print('clicked Button "{}"'.format(self.function))
                    self.function()

class TextButton():
    def __init__(self, text=None, pos=None, posadj=None, size=None, function=None, fillcolor=(226,116,154), bordercolor=(255,255,255), textcolor=(255,255,255)):
        self.pos = pos
        self.size = size
        self.function = function
        self.text = text
        self.rendered_text = None
        self.fillcolor = fillcolor
        self.bordercolor = bordercolor
        self.textcolor = textcolor
        

        if self.text:
            self.rendered_text = pygame.font.Font(FONT_LATO,20).render(self.text, True, self.textcolor)

            # if we're not using a specific size, work it out based on the text
            if not self.size:
                self.size = (
                    self.rendered_text.get_width() + BUTTON_PADDING[0] + BUTTON_PADDING[2], 
                    self.rendered_text.get_height() + BUTTON_PADDING[1] + BUTTON_PADDING[3]
                )
            
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.surface_rect.center=self.pos

    def draw(self, surf):
        # empty fill to clear what's been drawn
        self.surface.fill((0,0,0,0))
        # if hovering, draw a background fill
        if within_bounds(pygame.mouse.get_pos(), self.surface_rect):
            pygame.draw.rect(surf, self.fillcolor, self.surface_rect)
        pygame.draw.rect(surf, self.bordercolor, self.surface_rect, 3)


        # draw the text
        if self.rendered_text:
            self.surface.blit(
                self.rendered_text, 
                (
                    (self.size[0]/2)-(self.rendered_text.get_width()/2),
                    (self.size[1]/2)-(self.rendered_text.get_height()/2)
                )
            )
        # blit button to surf
        surf.blit(self.surface, self.surface_rect)
    
    def do(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if within_bounds(pygame.mouse.get_pos(), self.surface_rect):
                if self.function != None:
                    print('clicked TextButton "{}"'.format(self.text))
                    self.function()

class PageButton(Button):
    def __init__(self, parent=None, image=None, pos=(0,0), size=(0,0), page=None, function=None):
        self.parent = parent
        self.image = image
        self.pos = pos
        self.size = size
        self.page = page
        self.function = function
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect(topleft=self.pos)
    
    def draw(self, surf):
        # empty fill to clear what's been drawn
        self.surface.fill((0,0,0,0))
        if self.image:
            image_path = os.path.join(ASSETS_DIR, self.image)
            button_image = pygame.image.load(image_path).convert_alpha()
            if self.size:
                button_image = pygame.transform.scale(button_image, self.size)

            if within_bounds(pygame.mouse.get_pos(), self.surface_rect):
                button_image.set_alpha(100)
            else:
                button_image.set_alpha(255)

            self.surface.blit(button_image, (0,0))
            surf.blit(self.surface, self.pos)
