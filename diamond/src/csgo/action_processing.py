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
	steering_value: float

def print_csgo_action(action: CSGOAction) -> Tuple[str]:
	return str(action.steering_value)
	
N_KEYS = 20 #number of input keys


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
	keys_pressed_onehot = np.zeros(N_KEYS)

	keys_pressed_onehot[decimal_to_vector(csgo_action.steering_value)] = 1

	return torch.tensor(
		np.concatenate((
			keys_pressed_onehot,
		)),
		device=device,
		dtype=torch.float32,
	)
	

def decode_csgo_action(y_preds: torch.Tensor) -> CSGOAction:
	y_preds = y_preds.squeeze()
	keys_pred = y_preds[0:N_KEYS]
	return CSGOAction(vector_to_decimal(y_preds))

