import pyscreenshot as ImageGrab
from pynput.keyboard import Key, Controller
import psutil

class WindowOpt:
	def __init__(self):
		self.keyboard = Controller()

	def closeWindow(self):
		self.keyboard.press(Key.alt_l)
		self.keyboard.press(Key.f4)
		self.keyboard.release(Key.f4)
		self.keyboard.release(Key.alt_l)

def isContain(text, lst):
	for word in lst:
		if word in text:
			return True
	return False

###############################
###########  VOLUME ###########
###############################

keyboard = Controller()
def mute():
	for i in range(50):
		keyboard.press(Key.media_volume_down)
		keyboard.release(Key.media_volume_down)

def full():
	for i in range(50):
		keyboard.press(Key.media_volume_up)
		keyboard.release(Key.media_volume_up)


def volumeControl(text):
	if 'full' in text or 'max' in text: full()
	elif 'mute' in text or 'min' in text: mute()
	elif 'incre' in text:
		for i in range(5):
			keyboard.press(Key.media_volume_up)
			keyboard.release(Key.media_volume_up)
	elif 'decre' in text:
		for i in range(5):
			keyboard.press(Key.media_volume_down)
			keyboard.release(Key.media_volume_down)

def systemInfo():
	import wmi
	c = wmi.WMI()  
	my_system_1 = c.Win32_LogicalDisk()[0]
	my_system_2 = c.Win32_ComputerSystem()[0]
	info = ["Total Disk Space: " + str(round(int(my_system_1.Size)/(1024**3),2)) + " GB",
			"Free Disk Space: " + str(round(int(my_system_1.Freespace)/(1024**3),2)) + " GB",
			"Manufacturer: " + my_system_2.Manufacturer,
			"Model: " + my_system_2. Model,
			"Owner: " + my_system_2.PrimaryOwnerName,
			"Number of Processors: " + str(my_system_2.NumberOfProcessors),
			"System Type: " + my_system_2.SystemType]
	return info

def batteryInfo():
	# usage = str(psutil.cpu_percent(interval=0.1))
	battery = psutil.sensors_battery()
	pr = str(battery.percent)
	if battery.power_plugged:
		return "Your System is currently on Charging Mode and it's " + pr + "% done."
	return "Your System is currently on " + pr + "% battery life."

def OSHandler(query):
	if isContain(query, ['system', 'info']):
		return ['Here is your System Information...', '\n'.join(systemInfo())]
	elif isContain(query, ['cpu', 'battery']):
		return batteryInfo()


from difflib import get_close_matches
import json
from random import choice
import webbrowser

data = json.load(open('extrafiles/websites.json', encoding='utf-8'))

def open_website(query):
	query = query.replace('open','')
	if query in data:
		response = data[query]
	else:
		query = get_close_matches(query, data.keys(), n=2, cutoff=0.5)
		if len(query)==0: return "None"
		response = choice(data[query[0]])
	webbrowser.open(response)