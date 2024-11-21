"""
Credits: some parts are taken and modified from the file `config.py` from https://github.com/TeaPearce/Counter-Strike_Behavioural_Cloning/
"""

from dataclasses import dataclass 
from typing import Dict, List, Set, Tuple

import numpy as np
import pygame
import torch

from .keymap import CSGO_KEYMAP


@dataclass
class CSGOAction:
	keys: List[int]
	steering_value: float
	map_id: int

	@property
	def key_names(self) -> List[str]:
		return [pygame.key.name(key) for key in self.keys]
			
	


def print_csgo_action(action: CSGOAction) -> Tuple[str]:
	action_names = [CSGO_KEYMAP[k] for k in action.keys] if len(action.keys) > 0 else []
	keys = " + ".join(action_names)
	return f"{keys} [Steering {action.steering_value}] | MAP: {action.map_id}"
	
N_KEYS = 39 #number of input keys


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
	
	return index


def vector_to_decimal(vector):
	# Ensure the vector is of length 20
	if len(vector) != 20:
		raise ValueError("Input vector must be of length 20.")
	
	# Find the index of the non-zero element
	try:
		index = vector.index(1)
	except ValueError:
		raise ValueError("Input vector must contain exactly one '1' and the rest '0'.")
	
	# Convert the index back to the corresponding decimal value
	decimal_value = (index / 10) - 1.0
	
	return decimal_value



def encode_csgo_action(csgo_action: CSGOAction, device: torch.device) -> torch.Tensor:

	input_vector = np.zeros(3)
	steering_vector = np.zeros(20)
	map_vector = np.zeros(16)
	
	for key in csgo_action.key_names:
		if key == "a":
			input_vector[0] = 1
		if key == "s":
			input_vector[1] = 1
		if key == "d":
			input_vector[2] = 1

	map_vector[csgo_action.map_id] = 1
	
	steering_vector[decimal_to_vector(csgo_action.steering_value)] = 1

	return torch.tensor(
		np.concatenate((
			input_vector,
			steering_vector,
			map_vector
		)),
		device=device,
		dtype=torch.float32,
	)
	

def decode_csgo_action(y_preds: torch.Tensor) -> CSGOAction:
	y_preds = y_preds.squeeze()
	input_vector = y_preds[0:3]
	steering_vector = y_preds[3:23]
	map_vector = y_preds[23:40]

	map_id = map_vector.index(1)
	steering_value = vector_to_decimal(steering_vector)
	keys_pressed = []
	if input_vector[0] == 1:
		keys_pressed.append("a")
	if input_vector[1] == 1:
		keys_pressed.append("s")
	if input_vector[2] == 1:
		keys_pressed.append("d")
	
	keys_pressed = [pygame.key.key_code(x) for x in keys_pressed]

	return CSGOAction(keys_pressed, steering_value, map_id)

