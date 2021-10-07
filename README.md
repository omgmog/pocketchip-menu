# Pocket CHIP Menu

A simple PyGame replacement for the Pocket CHIP home launcher. Designed for Debian 11 (bullseye)

Still WIP.

![Screenshot of the menu](https://i.ibb.co/CbcMHvf/2021-10-07-114218-480x272-scrot.png)

## Installation

```
cd ~
git clone https://github.com/omgmog/pocketchip-menu.git
cd pocketchip-menu
sudo apt install python3-pip python3-pygame
pip install -r requirements.txt
chmod +x load.sh
ln rc.lua /home/chip/.config/awesome/rc.lua
```

Restart awesome and it should load directly to the new menu.

## Notes

### Default applications

- Terminal: Sakura
- Pico-8
- Music: Sunvox 1.9.6
- Surf: Midori
- Write: Leafpad
- Files: pcmanfm

## Icon Credits

Icons8 Fluency icons - https://icons8.com/icons/fluency
