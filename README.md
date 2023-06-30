# Pocket CHIP Menu

A simple PyGame replacement for the Pocket CHIP home launcher. Designed for Debian 11 (bullseye)

Still WIP.

![Screenshot of the menu](https://user-images.githubusercontent.com/50949/139332901-b71a6006-9e25-4ce8-b614-13c5f2cdc231.png)

## Installation

```
cd ~
git clone https://github.com/omgmog/pocketchip-menu.git
cd pocketchip-menu
sudo apt install unclutter python3-pip python3-pygame python3-dbus upower
sudo pip install -r requirements.txt
chmod +x load.sh
mkdir -p /home/chip/.config/awesome/
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
