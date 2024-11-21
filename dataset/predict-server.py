import sys, time, logging, os, argparse

import numpy as np
from PIL import Image, ImageGrab
from socketserver import TCPServer, StreamRequestHandler
import math
import random
import datetime
import h5py
import cv2

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
t = 0
file_index = 0
h5file = None
output_dir = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
file_prefix = output_dir
from train import create_model, is_valid_track_code, INPUT_WIDTH, INPUT_HEIGHT, INPUT_CHANNELS
root_folder = "./recordings/"
created_folder = False
BOOST_CHANCE = 100
target_width = 320
target_height = 240

static_input_vector = [1, 0, 0] #NeuralKart always accelerates and never brakes or uses action items.
map_id = 1 #For more information refer to https://github.com/Dere-Wah/AI-MarioKart64/tree/main/dataset#track-mapping-table
map_selector = [0] * 16 #OneHot Representation of the map index.
map_selector[map_id] = 1

noise_mode = False

def prepare_image(im):
	im = im.resize((INPUT_WIDTH, INPUT_HEIGHT))
	im_arr = np.frombuffer(im.tobytes(), dtype=np.uint8)
	im_arr = im_arr.reshape((INPUT_HEIGHT, INPUT_WIDTH, INPUT_CHANNELS))
	im_arr = np.expand_dims(im_arr, axis=0)
	return im_arr
	
def decimal_to_vector(decimal_number):
    # Initialize a list of 20 zeros
    vector = [0] * 20
    
    # Ensure the decimal_number is within the expected range
    decimal_number = max(-1.0, min(decimal_number, 1.0))
    
    # Calculate the index based on the input decimal number
    # Map -1.0 to 0, -0.9 to 1, ..., 0.0 to 10, ..., 0.9 to 19, 1.0 to 19
    index = round((decimal_number + 1.0) * 10)
    
    # Cap the index at 19 to handle the case where decimal_number is exactly 1.0
    index = min(index, 19)
    
    # Set the appropriate position in the vector to 1
    vector[index] = 1
    
    return vector
	
def capture_frame(prediction, img, do_boost):
	global t
	global file_index
	global h5file
	if t > 999 or h5file == None:
		file_index += 1
		if h5file != None:
			h5file.close()
		h5file_name = file_prefix+"_"+str(file_index)+".hdf5"
		if noise_mode:
			h5file_name = "noised_" + h5file_name
		h5file = h5py.File(root_folder + output_dir+"/"+h5file_name, 'w')	
		t = 0
		print("Saving hdf5 file and skipping to next...")
	# Convert from BGRA to BGR (OpenCV format)
	img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
	img = cv2.resize(img, (target_width, target_height))
	vector = decimal_to_vector(prediction)
	
	inputs_vector = static_input_vector
	if do_boost:
		inputs_vector[2] = 1
	else:
		inputs_vector[2] = 0

	onehot = inputs_vector + vector + map_selector
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
	parser.add_argument('--map_id', type=int, help='Map index', default=0)
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
