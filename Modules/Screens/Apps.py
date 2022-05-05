import pygame
import os
from Modules.Globals import *
from Modules.GenWidgets.Icon import *

class Apps():
    index = Pages.APPS
    title = 'Apps'
    app_configs = sorted([f for f in os.listdir(APPS_DIR) if os.path.isfile(os.path.join(APPS_DIR,f))])
    icons_data = []

    def collate_apps(self):
        for app_config in self.app_configs:
            read_config = open(os.path.join(APPS_DIR, app_config), 'r')
            config_data = dict()
            for line in read_config:
                key = line.partition('=')[0]
                value = line.partition('=')[-1].strip()
                config_data[key] = value
            self.icons_data.append(config_data)

    def __init__(self, parent):
        self.visible = False
        self.icons = []
        self.parent = parent
        self.image = assetpath('mainBackground.png')
        self.collate_apps()

        wrap_at = 3
        wrap_counter = -1
        start_x = 80 # can probably calculate this to make this more scalable.
        start_y = 50 # this too...
        col_width = 128 # and this
        row_height = 100 # and this
        col_offset = start_x
        row_offset = start_y

        for index, icon in enumerate(Apps.icons_data):
            if not (index % wrap_at):
                col_offset = start_x # new row
                wrap_counter += 1
                row_offset = start_y + (row_height * wrap_counter)
            else:
                col_offset += col_width # new col

            pos = (col_offset, row_offset)
            size = (64, 64)

            self.icons.append(
                Icon(
                    image=iconpath(icon['icon']),
                    title=icon['title'],
                    pos=pos,
                    size=size,
                    function=lambda icon=icon:run_cmd(icon['execute'])
                )
            )

    def do(self, event):
        for icon in self.icons:
            icon.do(event)

    def update(self):
        pass

    def draw(self, surf):
        for icon in self.icons:
            icon.draw(surf)

if __name__ == '__main__':
    pass
