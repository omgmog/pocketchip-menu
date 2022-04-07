#!/usr/bin/python3

import dbus
bus = dbus.SystemBus()

def get_active_wifis():
	array_of_wifi_devs = []
	proxy = bus.get_object('org.freedesktop.NetworkManager',
		'/org/freedesktop/NetworkManager')
	getmanager = dbus.Interface(proxy, 'org.freedesktop.NetworkManager')
	devices = getmanager.GetDevices()
	for device in devices:
		deviceobject = bus.get_object('org.freedesktop.NetworkManager',device)
		deviceinterface = dbus.Interface(deviceobject, dbus_interface='org.freedesktop.DBus.Properties')
		if deviceinterface.Get('org.freedesktop.NetworkManager.Device', 'DeviceType') == 2:
			array_of_wifi_devs.append(device)

	return array_of_wifi_devs

def get_scan_results(array_of_wifi_devs):
	array_of_aps = []
	for device in array_of_wifi_devs:
		deviceobject = bus.get_object('org.freedesktop.NetworkManager',device)
		deviceinterface = dbus.Interface(deviceobject, dbus_interface='org.freedesktop.NetworkManager.Device.Wireless')
		for accesspoint in deviceinterface.GetAllAccessPoints():
			array_of_aps.append(str(accesspoint))
	return array_of_aps

def human_readable_ap_info(array_of_aps):
	array_of_readable_aps = []
	for accesspoint in array_of_aps:
		apobject = bus.get_object('org.freedesktop.NetworkManager',accesspoint)
		apinterface = dbus.Interface(apobject,dbus_interface='org.freedesktop.DBus.Properties')
		ap = apinterface.GetAll('org.freedesktop.NetworkManager.AccessPoint')
		ap_info = {}
		ap_info['name'] = ''.join([chr(byte) for byte in ap['Ssid']])
		ap_info['strength'] = int(ap['Strength'])
		if int(ap['Flags']) & 0x1 == 1:
			ap_info['encrypted'] = True
		else:
			ap_info['encrypted'] = False
		array_of_readable_aps.append(ap_info)
	return array_of_readable_aps

def get_active_wifi_connection():
	proxy = bus.get_object('org.freedesktop.NetworkManager',
		'/org/freedesktop/NetworkManager')
	getmanager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
	for connection in getmanager.Get('org.freedesktop.NetworkManager', 'ActiveConnections'):
		connectionobject = bus.get_object('org.freedesktop.NetworkManager',
					connection)
		conmanager = dbus.Interface(connectionobject, 'org.freedesktop.DBus.Properties')
		if conmanager.Get('org.freedesktop.NetworkManager.Connection.Active', 'State') in [1,2,3] and \
			conmanager.Get('org.freedesktop.NetworkManager.Connection.Active','Type') == '802-11-wireless':
			return [str(conmanager.Get('org.freedesktop.NetworkManager.Connection.Active','SpecificObject'))]

def initiate_ap_scan(array_of_wifi_devs, current_time_monotonic=None):
	last_scan_times_monotonic = []
	for wifi_dev in array_of_wifi_devs:
		proxy = bus.get_object('org.freedesktop.NetworkManager',
			wifi_dev)
		getmanager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
		if current_time_monotonic is None or int(getmanager.Get('org.freedesktop.NetworkManager.Device.Wireless','LastScan')) < current_time_monotonic - 20000:
			getmanager = dbus.Interface(proxy,dbus_interface='org.freedesktop.NetworkManager.Device.Wireless')
			getmanager.RequestScan({})
		getmanager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
		last_scan_times_monotonic.append(int(getmanager.Get('org.freedesktop.NetworkManager.Device.Wireless','LastScan')))
	return int(sum(last_scan_times_monotonic) / len(last_scan_times_monotonic))

#start a site survey
#wifi_devices = get_active_wifis()
#last_scan_time = initiate_ap_scan(wifi_devices)

#read a site survey
#wifi_devices = get_active_wifis()
#access_points = get_scan_results(wifi_devices)
#print(human_readable_ap_info(access_points))

#read existing connection
#active_connection = get_active_wifi_connection()
#print(human_readable_ap_info(active_connection))

