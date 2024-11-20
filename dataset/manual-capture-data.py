
import time
import cv2
import numpy as np
import json
import os
import subprocess
from pynput import keyboard
import win32gui
import win32con
import win32api
import h5py
import datetime
import yaml	
import pygetwindow as gw
from PIL import Image, ImageGrab


# Load configuration from YAML file
with open("manual-config.yaml", "r") as config_file:
	config = yaml.safe_load(config_file)

# Extract values from the configuration
window_name = config.get("window_name", "Mario Kart 64 (USA) [Nintendo 64] - BizHawk")
target_width = config.get("target_width", 320)
target_height = config.get("target_height", 240)

# Initialize some variables
frames_data = []
keys_pressed = []
output_dir = "recordings/" + datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
capture_interval = 0.05  # Capture every 0.05 seconds


map_id = 0 #For more information refer to https://github.com/Dere-Wah/AI-MarioKart64/tree/main/dataset#track-mapping-table
map_selector = [0] * 16 #OneHot Representation of the map index.
map_selector[map_id] = 1

def list_open_windows():
	# Get all open windows
	windows = gw.getAllTitles()
	
	# Filter out empty titles (invisible or untitled windows)
	windows = [title for title in windows if title.strip()]
	
	if windows:
		print("Currently open window titles:")
		for idx, window in enumerate(windows, start=1):
			print(f"{idx}: {window}")
	else:
		print("No visible windows detected.")

def parse_key(key_str):
	"""
	Parses a key string from the config and returns the corresponding pynput key.
	If the key string matches an attribute in keyboard.Key, it returns keyboard.Key.<key>.
	Otherwise, it assumes the input is a character and returns it as-is.
	"""
	try:
		# Check if it's a special key like 'up', 'down', etc. in keyboard.Key
		return getattr(keyboard.Key, key_str)
	except AttributeError:
		# Otherwise, assume it's a standard character key
		return key_str

# Load key bindings from configuration
keybinds = config.get("keybinds", {})

# Map key bindings to valid_keys array in a specific order, parsing each key
valid_keys = [
	parse_key(keybinds.get("forward", "w")),
	parse_key(keybinds.get("left", "a")),
	parse_key(keybinds.get("backwards", "s")),
	parse_key(keybinds.get("right", "d")),
	parse_key(keybinds.get("use", "enter")),
]

t = 0
file_prefix = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
file_index = 0

keys_pressed = []  # List of currently pressed keys


# Define the key press handlers
def on_press(key):
	try:
		if hasattr(key, 'char') and key.char in valid_keys:
			if key.char not in keys_pressed:
				keys_pressed.append(key.char)
		elif key in valid_keys and key not in keys_pressed:
			keys_pressed.append(key)
	except Exception as e:
		print(f"Error in on_press: {e}")

def on_release(key):
	try:
		if hasattr(key, 'char') and key.char in valid_keys:
			if key.char in keys_pressed:
				keys_pressed.remove(key.char)
		elif key in valid_keys and key in keys_pressed:
			keys_pressed.remove(key)
		if key == keyboard.Key.esc:
			return False  # Stop listener on ESC
	except Exception as e:
		print(f"Error in on_release: {e}")

# Function to get game window handle
def get_window_handle(window_name):
	hwnd = win32gui.FindWindow(None, window_name)
	if hwnd:
		win32gui.SetForegroundWindow(hwnd)
	return hwnd


def send_ctrl_c(hwnd):
	# Press and hold Ctrl
	win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0)
	# Press and release 'C'
	win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, ord('C'), 0)
	win32api.SendMessage(hwnd, win32con.WM_KEYUP, ord('C'), 0)
	# Release Ctrl
	win32api.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_CONTROL, 0)


def encode_inputs(keys_pressed):

	# Initialize one-hot vectors
	movement_vector = [0, 0, 0]  # 5 elements for movement keys
	direction_vector = [0] * 20        # 20 elements for direction keys

	if "a" in keys_pressed:
		movement_vector[0] = 1
	if "s" in keys_pressed:
		movement_vector[1] = 1
	if "d" in keys_pressed:
		movement_vector[2] = 1

	if keyboard.Key.left in keys_pressed:
		direction_vector[0] = 1
	if keyboard.Key.right in keys_pressed:
		direction_vector[-1] = 1

	# Concatenate the two vectors
	encoded_vector = movement_vector + direction_vector + map_selector

	return encoded_vector

# Capture frame from game window
def capture_frame(window_handle, h5file):
	global t
	global file_index
	if not window_handle:
		print("No valid game window. Exiting.\nMake sure the window is named exactly in the config as the BizHawk process shown below:")
		list_open_windows()
		return False
	
	# Capture the game window region only

	send_ctrl_c(window_handle)
	screenshot = ImageGrab.grabclipboard()
	img = np.array(screenshot)
	# During this convertion to array the color channels are swapped into BGRA
	# Convert from BGRA to BGR (OpenCV format)
	img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
	img = cv2.resize(img, (target_width, target_height))
	#cv2.imwrite(f"{output_dir}/frame_{t}.png", img)
	
	h5file.create_dataset("frame_"+str(t)+"_x", data=img)

	onehot = encode_inputs(keys_pressed)
	print(onehot)
	h5file.create_dataset("frame_"+str(t)+"_y", data=list(onehot))

	t += 1
	return True


# Main function
def main():
	global t
	global file_index
	# Get the game window handle and set the size
	hwnd = get_window_handle(window_name)	# Replace with the exact game window title

	# Ensure output directory exists
	os.makedirs(output_dir, exist_ok=True)
	
	
	h5file_name = file_prefix+"_"+str(file_index)+".hdf5"
	h5file = h5py.File(output_dir+"/"+h5file_name, 'w')	

	# Start keyboard listener
	listener = keyboard.Listener(on_press=on_press, on_release=on_release)
	listener.start()

	print("Starting capture... Press ESC to stop.")
	time.sleep(1)
	try:
		while listener.is_alive():
			if not capture_frame(hwnd, h5file):
				break
			time.sleep(capture_interval)
			if t > 999:
				file_index += 1
				h5file.close()
				h5file_name = file_prefix+"_"+str(file_index)+".hdf5"
				h5file = h5py.File(output_dir+"/"+h5file_name, 'w')	
				t = 0
				print("Saving hdf5 file and skipping to next...")
	except KeyboardInterrupt:
		print("Capture stopped.")
	
	h5file.close()

	print("Data saved.")

if __name__ == "__main__":
	main()
