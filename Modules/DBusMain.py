import __main__
from threading import Thread
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from gi.repository import GObject

try:
    DBusGMainLoop(set_as_default=True)
    GObject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus_loop = DBusGMainLoop()
    DBUS_BUS = dbus.SystemBus(mainloop=dbus_loop)
    MAINLOOP = GLib.MainLoop()
    DBUS_THREAD = Thread(target=MAINLOOP.run, daemon=True)
    DBUS_THREAD.start()
except:
    print("Error Loading DBus, functionality will be reduced!")
