import pygame
import numpy as np
from pygame.locals import *
import sys
import os

# Controls the visibility of some logging, debug rendering, etc.
DEBUG = False

PLATFORM = sys.platform[:3]
BASEDIR = os.path.dirname(__file__) or '.'
ASSETSDIR = os.path.normpath(os.path.join(BASEDIR, 'assets/ui'))
ICONSDIR = os.path.normpath(os.path.join(BASEDIR, 'icons'))
FONT = os.path.join(ASSETSDIR, 'Lato-Regular.ttf')

def asset(filename=None):
    return os.path.join(ASSETSDIR,filename)
def iconasset(filename=None):
    return os.path.join(ICONSDIR,filename)

if PLATFORM == 'lin':
    import psutil
    import NetworkManager
    import dbus.mainloop.glib
    from single_process import single_process

    single_process()
    main_dbus_loop = dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    dbus.set_default_main_loop(main_dbus_loop)

class Pages:
    POWER = 1
    HOME = 2
    SETTINGS = 3

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
        self.apps_dir = BASEDIR + '/apps/'
    
        self.bg_color = (77, 77, 77) #'#4D4D4D'

        if file:
            self.load_image(file)
        else:
            self.image = pygame.Surface(self.size)
            self.image.fill(self.bg_color)
            self.rect = self.image.get_rect()
        self.key_cmd = {}
        self.page = Pages.HOME
        self.page_labels = ['Power', 'Home', 'Settings']

        #redraw the UI every 5000ms if no events received first
        pygame.time.set_timer(USEREVENT+1,5000)

    def load_image(self, file):
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.screen = pygame.display.set_mode(self.rect.size)

    def run(self):
        while self.running:
            event = pygame.event.wait()
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
        self.image = pygame.image.load(img) if type(img) is str else img

    def draw(self, surf):
        surf.blit(self.image, self.rect)
    
    def do(self, event):
        pass
    
    def update(self):
        pass

class Icon(Drawable):
    def __init__(self, img=None, pos=(0, 0), size=None, rect=None, page=None, action=None):
        self.page = page
        self.size = size
        if not rect:
            self.rect = pygame.Rect(pos, size)
        else:
            self.rect = pygame.Rect(pos, rect)
        self.position = np.array(pos, dtype=float)

        self.image = None
        if img is not None:
            self.image = pygame.image.load(img)
            self.image = pygame.transform.scale(self.image, size)

        self.action = action

    def draw(self, surf):
        if DEBUG:
            pygame.draw.rect(surf, (255,0,0), self.rect, 2) # draw a red rectangle around the icons
        surf.blit(self.image, self.rect)

    def do(self, event):
        if event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if self.position[0]+self.size[0] > mouse[0] > self.position[0] and self.position[1]+self.size[1] > mouse[1] > self.position[1]:
                if click[0] == 1 and self.action != None:
                    if DEBUG:
                        print(self.action)
                    from subprocess import Popen, PIPE
                    process = Popen(self.action, stdout=PIPE, stderr=PIPE, shell = True)
                    stdout, stderr = process.communicate()
                    if DEBUG:
                        print(stdout)

def collate_apps():
    apps_dir_contents = [f for f in os.listdir(app.apps_dir) if os.path.isfile(os.path.join(app.apps_dir,f))]
    icons = []
    for file in apps_dir_contents:
        filestream = open(app.apps_dir + file, 'r')
        app_dict = dict()
        for line in filestream:
            key = line.split('=')[0]
            value = line.split('=')[1].strip()
            app_dict[key] = value
        icons.append(app_dict)
    return icons

class Battery:
    def __init__(self):
        self.parent = None
        self.size = (24,24)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.position = ((app.screen.get_width() - self.size[0] - 5), 0)
        self.rect = pygame.Rect(self.position, self.size)
        self.battery_present = False
        if PLATFORM == 'lin':
            if psutil.sensors_battery() is not None:
                self.battery_present = True

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def do(self, event):
        pass

    def update(self):
        if self.battery_present is False:
            return
        battery_data = psutil.sensors_battery()
        if battery_data is None: #maybe battery can be unplugged?
            return
        if battery_data.power_plugged is True:
            self.image = pygame.transform.scale(pygame.image.load(asset('batterycharge.png')), self.size)
            return
        if battery_data.percent > 75:
            self.image = pygame.transform.scale(pygame.image.load(asset('battery100.png')), self.size)
            return
        if battery_data.percent > 50:
            self.image = pygame.transform.scale(pygame.image.load(asset('battery75.png')), self.size)
            return
        if battery_data.percent > 25:
            self.image = pygame.transform.scale(pygame.image.load(asset('battery50.png')), self.size)
            return
        else:
            self.image = pygame.transform.scale(pygame.image.load(asset('battery25.png')), self.size)

class Wifi:
    def __init__(self):
        self.parent = None
        self.size = (24,24)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.position = ((app.screen.get_width() - (self.size[0] * 2) - 10), 0)
        self.rect = pygame.Rect(self.position, self.size)
        self.wifi_device = None
        if PLATFORM == 'lin':
            for device in NetworkManager.NetworkManager.GetAllDevices():
                if device.DeviceType == 2:
                    self.wifi_device = device

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def do(self, event):
        pass

    def update(self):
        if self.wifi_device is None:
            return
        if self.wifi_device.ActiveConnection is None:
            self.image = pygame.transform.scale(pygame.image.load(asset('wifi-disc.png')), self.size)
            return
        if self.wifi_device.ActiveConnection.Devices[0].ActiveAccessPoint.Strength > 80:
            self.image = pygame.transform.scale(pygame.image.load(asset('wifi-full.png')), self.size)
            return
        if self.wifi_device.ActiveConnection.Devices[0].ActiveAccessPoint.Strength > 60:
            self.image = pygame.transform.scale(pygame.image.load(asset('wifi-good.png')), self.size)
            return
        if self.wifi_device.ActiveConnection.Devices[0].ActiveAccessPoint.Strength > 40:
            self.image = pygame.transform.scale(pygame.image.load(asset('wifi-fair.png')), self.size)
            return
        else:
            self.image = pygame.transform.scale(pygame.image.load(asset('wifi-weak.png')), self.size)
            return

def draw_page(page_index):
    if app.page == Pages.POWER:
        app.add(Drawable(img=asset('powerMenuBackground.png')))
    elif app.page == Pages.SETTINGS:
        app.add(Drawable(img=asset('settingsBackground.png')))
    else:
        app.add(Drawable(img=asset('mainBackground.png')))

    font = pygame.font.Font(FONT, 20)
    title = font.render(app.page_labels[page_index - 1], True, (255,255,255))
    title_pos_x = (app.screen.get_width() / 2) - (title.get_width()/2)
    app.add(Drawable(img=title, pos=(title_pos_x, 20)))
    app.add(Battery())
    app.add(Wifi())

    font = pygame.font.Font(FONT, 16)

    if page_index == Pages.HOME:
        icons = collate_apps()
        wrap_at = 3
        wrap_counter = -1  # -1 so that first row isn't + row_height
        start_x = 80
        start_y = 50
        col_offset = start_x
        row_offset = start_y
        col_width = 128
        row_height = 100

        for index, icon in enumerate(icons):
            if (index % wrap_at) == 0:
                col_offset = start_x        # start cols again for a new row
                wrap_counter += 1
                row_offset = start_y + (row_height*wrap_counter)
            else:
                col_offset += col_width     # add to the cols 
            
            pos = (
                col_offset, 
                row_offset
            )

            size = (64, 64)
            icon_center=pos[0]+(size[0]/2)
            label = font.render(icon['title'], True, (255,255,255))

            label_x = icon_center - (label.get_width()/2)
            label_y = pos[1] + 72

            app.add(
                Drawable(
                    img=label,
                    pos=(label_x, label_y)
                )
            )
            app.addIcon(
                Icon(
                    img=iconasset(icon['icon']),
                    pos=pos, 
                    size=size, 
                    page=Pages.HOME,
                    action=icon['execute']
                )
            )

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

if __name__ == '__main__':
    app = App(file=asset('mainBackground.png'))
    app.add_cmd(K_LEFT, 'do_btn_left()')
    app.add_cmd(K_RIGHT, 'do_btn_right()')
    draw_page(Pages.HOME) # start with home
    app.run()
