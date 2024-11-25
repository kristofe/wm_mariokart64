"""
Credits: some parts are taken and modified from the file `predict-server.py` from https://github.com/rameshvarun/NeuralKart
"""

import sys, time, logging, os, argparse

import numpy as np
from PIL import Image, ImageGrab
from socketserver import TCPServer, StreamRequestHandler
import math
import random
import datetime
import h5py
import cv2
from train import create_model, is_valid_track_code, INPUT_WIDTH, INPUT_HEIGHT, INPUT_CHANNELS

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
t = 0
file_index = 0
h5file = None
output_dir = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
file_prefix = output_dir

root_folder = "./recordings/"
created_folder = False
BOOST_CHANCE = 100
target_width = 320
target_height = 240

noise_mode = False

def prepare_image(im):
	im = im.resize((INPUT_WIDTH, INPUT_HEIGHT))
	im_arr = np.frombuffer(im.tobytes(), dtype=np.uint8)
	im_arr = im_arr.reshape((INPUT_HEIGHT, INPUT_WIDTH, INPUT_CHANNELS))
	im_arr = np.expand_dims(im_arr, axis=0)
	return im_arr
	
def decimal_to_index(decimal_value):
    """
    Converts a decimal value to its corresponding index based on the table.

    Args:
        decimal_value (float): The decimal value to convert.

    Returns:
        int: The corresponding index, or None if the value is not in the range.
    """
    decimals = [-1.0 + 0.1 * i for i in range(21)]
    if decimal_value in decimals:
        return decimals.index(decimal_value)
    return None

def index_to_decimal(index):
    """
    Converts an index to its corresponding decimal value based on the table.

    Args:
        index (int): The index to convert.

    Returns:
        float: The corresponding decimal value, or None if the index is out of range.
    """
    if 0 <= index < 21:
        return -1.0 + 0.1 * index
    return None
	
def capture_frame(prediction, img, do_boost):
	global t
	global file_index
	global h5file
	if t > 999 or h5file == None:
		file_index += 1
		if h5file != None:
			h5file.close()
		h5file_name = file_prefix+"_"+str(file_index)+".hdf5"
		h5file = h5py.File(root_folder + output_dir+"/"+h5file_name, 'w')	
		t = 0
		print("Saving hdf5 file and skipping to next...")
	# Convert from RGBA to BGR (OpenCV format)
	img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
	img = cv2.resize(img, (target_width, target_height))
	vector = [0] * 21
	vector[decimal_to_index(prediction)] = 1
	
	if do_boost:
		inputs_vector = [1]
	else:
		inputs_vector = [0]

	onehot = inputs_vector + vector
	print(onehot)
	#cv2.imwrite(f"{output_dir}/frame_{t}_{str(list(vector))}.png", img)
	h5file.create_dataset("frame_"+str(t)+"_x", data=img)
	h5file.create_dataset("frame_"+str(t)+"_y", data=list(onehot))
	t += 1
	return True

class TCPHandler(StreamRequestHandler):
	def handle(self):
		global t
		global course
		prediction = None
		if args.all:
			weights_file = 'weights/all.hdf5'
			logger.info("Loading {}...".format(weights_file))
			model.load_weights(weights_file)
		logger.info("Handling a new connection...")
		os.makedirs(root_folder + output_dir, exist_ok=True)
		for line in self.rfile:
			message = str(line.strip(),'utf-8')
			#logger.debug(message)

			if message.startswith("COURSE:") and not args.all:
				course = message[7:].strip().lower()
				weights_file = 'weights/{}.hdf5'.format(course)
				logger.info("Loading {}...".format(weights_file))
				model.load_weights(weights_file)

			if message.startswith("PREDICTFROMCLIPBOARD"):
				im = ImageGrab.grabclipboard()
				if im != None:
					prediction = model.predict(prepare_image(im), batch_size=1)[0]
					if noise_mode:
						if random.random() < 1/5:
							prediction += random.uniform(-10, 10)
							prediction = np.clip(prediction, -1, 1)
					prediction = round(prediction[0], 1)
					im_array = np.array(im)
					do_boost = 1 if random.randint(1, BOOST_CHANCE) == 1 else 0
					self.wfile.write((str(prediction) + "|" + str(do_boost) + "\n").encode('utf-8'))
					capture_frame(prediction, im_array, do_boost)
				else:
					self.wfile.write("PREDICTIONERROR\n".encode('utf-8'))

			if message.startswith("PREDICT:"):
				im = Image.open(message[8:])
				prediction = model.predict(prepare_image(im), batch_size=1)[0]
				self.wfile.write((str(prediction[0]) + "\n").encode('utf-8'))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Start a prediction server that other apps will call into.')
	parser.add_argument('-a', '--all', action='store_true', help='Use the combined weights for all tracks, rather than selecting the weights file based off of the course code sent by the Play.lua script.', default=False)
	parser.add_argument('-p', '--port', type=int, help='Port number', default=36296)
	parser.add_argument('--boost', type=int, help='Boosting chance', default=100)
	parser.add_argument('-c', '--cpu', action='store_true', help='Force Tensorflow to use the CPU.', default=False)
	parser.add_argument("--add_noise", action="store_true", help="Add random movement noise to the agent outputs.")
	args = parser.parse_args()

	noise_mode = args.add_noise
	map_id = args.map_id
	BOOST_CHANCE = args.boost
	if args.cpu:
		os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
		os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

	logger.info("Loading model...")
	model = create_model(keep_prob=1)

	if args.all:
		model.load_weights('weights/all.hdf5')

	logger.info("Starting server...")
	server = TCPServer(('0.0.0.0', args.port), TCPHandler)

	print("Listening on Port: {}".format(server.server_address[1]))
	sys.stdout.flush()
	server.serve_forever()
