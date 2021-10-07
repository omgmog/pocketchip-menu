import pygame
import numpy as np
from pygame.locals import *
import sys

PLATFORM = sys.platform[:3]

if PLATFORM == 'lin':
    from single_process import single_process
    single_process()

class Pages:
    POWER = 1
    HOME = 2
    SETTINGS = 3

class Apps:
    TERMINAL = "sakura -s"
    GAME = "pico8"
    MUSIC = "sunvox"
    INTERNET = "midori -e fullscreen  https://duck.com"
    TEXT = "leafpad"
    FILES = "pcmanfm"

class App:
    def __init__(self, file=None, caption='Menu'):
        pygame.init()
        pygame.display.set_caption(caption)
        self.size = (480, 272)
        self.fullscreen = pygame.FULLSCREEN if PLATFORM == 'lin' else False
        self.screen = pygame.display.set_mode(
            self.size, 
            self.fullscreen
        )
        self.running = True
        self.updating = True
        self.objects = []
        self.icon_objects = []
    
        # define all icons
        self.icons = [
            [
                "console", "Terminal", Apps.TERMINAL,
                Pages.HOME, (80, 40), (64, 64)
                ],
            [
                "game-controller", "Play Pico-8", Apps.GAME,
                Pages.HOME, (208, 40), (64, 64)
                ],
            [
                "electronic-music", "Make Music", Apps.MUSIC,
                Pages.HOME, (336, 40), (64, 64)
                ],
            [
                "internet", "Surf", Apps.INTERNET,
                Pages.HOME, (80, 140), (64, 64)
                ],
            [
                "notepad", "Write", Apps.TEXT,
                Pages.HOME, (208, 140), (64, 64)
                ],
            [
                "browse-folder", "Files", Apps.FILES,
                Pages.HOME, (336, 140), (64, 64)
                ],
        ]
        self.bg_color = (77, 77, 77) #'#4D4D4D'

        if file:
            self.load_image(file)
        else:
            self.image = pygame.Surface(self.size)
            self.image.fill(self.bg_color)
            self.rect = self.image.get_rect()
        self.key_cmd = {}
        self.page = Pages.HOME
        self.page_labels = ["Power", "Home", "Settings"]

    def load_image(self, file):
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.screen = pygame.display.set_mode(self.rect.size)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.do(event)
            self.update()
            self.draw()
        pygame.quit()
        raise SystemExit

    def add_cmd(self, key, cmd):
        self.key_cmd[key] = cmd

    def add(self, object):
        self.objects.append(object)
        object.parent = self
    def addIcon(self, object):
        self.icon_objects.append(object)
        object.parent = self
    
    def do(self, event):
        if event.type == QUIT:
            self.running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.updating = not self.updating

            if event.key in self.key_cmd:
                cmd = self.key_cmd[event.key]
                eval(cmd)

        for obj in self.objects:
            obj.do(event)
        
        for icon in self.icon_objects:
            if icon.page == app.page:
                icon.do(event)


    def update(self):
        if self.updating:
            for obj in self.objects:
                obj.update()

    def draw(self):
        self.screen.blit(self.image, self.rect)
        for obj in self.objects:
            obj.draw(self.screen)

        for icon in self.icon_objects:
            if icon.page == app.page:
                icon.draw(self.screen)

        pygame.display.update()

class Drawable:
    def __init__(self, img=None, pos=(0, 0), size=None, rect=(20,20)):
        self.parent = None
        self.size = size
        self.rect = pygame.Rect(pos, rect)
        self.position = np.array(pos, dtype=float)
        self.image = img
        if type(self.image) is str:
            self.image = pygame.image.load(img)
        # if img != None:
            # self.image = pygame.image.load(img)

    def draw(self, surf):
        surf.blit(self.image, self.rect)
    
    def do(self, event):
        pass
    
    def update(self):
        pass

class Icon(Drawable):
    def __init__(self, img=None, pos=(0, 0), size=None, rect=(20,20), page=None, action=None):
        self.page = page
        self.size = size
        self.rect = pygame.Rect(pos, rect)
        self.position = np.array(pos, dtype=float)
        self.image = pygame.transform.scale(pygame.image.load(img), size)
        self.action = action

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def do(self, event):
        if event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if self.position[0]+self.size[0] > mouse[0] > self.position[0] and self.position[1]+self.size[1] > mouse[1] > self.position[1]:
                if click[0] == 1 and self.action != None:
                    print(self.action)
                    from subprocess import Popen, PIPE
                    process = Popen(self.action, stdout=PIPE, stderr=PIPE, shell = True)
                    stdout, stderr = process.communicate()
                    print(stdout)


if __name__ == '__main__':
    app = App(file="assets/ui/mainBackground.png")


    def draw_page(page_index):
        if app.page == Pages.POWER:
            app.add(Drawable(img="assets/ui/powerMenuBackground.png"))
        elif app.page == Pages.SETTINGS:
            app.add(Drawable(img="assets/ui/settingsBackground.png"))
        else:
            app.add(Drawable(img="assets/ui/mainBackground.png"))


        font = pygame.font.SysFont(None, 24)
        title = font.render(app.page_labels[page_index - 1], True, (255,255,255))
        title_pos_x = (app.screen.get_width() / 2) - (title.get_width()/2)
        app.add(Drawable(img=title, pos=(title_pos_x, 20)))

        font = pygame.font.SysFont(None, 18)
        icons = []
        for icon in app.icons:
            if icon[3] == page_index:
                icons.append(icon)

        for icon in icons:
            filename="assets/icons/icons8-"+icon[0]+"-96.png"
            label = font.render(icon[1], True, (255,255,255))
            action = icon[2]
            page = icon[3]
            pos = icon[4]
            size = icon[5]

            icon_center=pos[0]+(size[0]/2)
            label_x = icon_center - (label.get_width()/2)
            label_y = pos[1] + 72

            app.addIcon(Icon(img=filename, pos=pos, size=size, page=page, action=action))
            app.add(Drawable(img=label, pos=(label_x, label_y)))


    def do_btn_left():
        app.page -= 1
        if app.page <= 1:
            app.page = 1
        draw_page(app.page)

    def do_btn_right():
        app.page += 1
        if app.page >= len(app.page_labels):
            app.page = len(app.page_labels)
        draw_page(app.page)

    app.add_cmd(K_LEFT, 'do_btn_left()')
    app.add_cmd(K_RIGHT, 'do_btn_right()')
    draw_page(Pages.HOME) # start with home
    app.run()