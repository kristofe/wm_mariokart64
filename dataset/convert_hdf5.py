import os
import h5py
import numpy as np
import cv2
import shutil

# Placeholder for the folder path containing HDF5 files
folder_path = input("Folder path: ")
output_path = input("Output path: ")

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
	if filename.endswith(".hdf5"):	# Check for HDF5 files
		file_path = os.path.join(folder_path, filename)
		shutil.copy(file_path, output_path)
		file_path = os.path.join(output_path, filename)
		with h5py.File(file_path, "r+") as hdf:
			# Iterate through all keys in the file
			for key in hdf.keys():
				if key.startswith("frame_") and key.endswith("_y"):	 # Match `frame_i_y` pattern
					# Load the frame data as a NumPy array
					frame = hdf[key][:]

					new_array = [0] * 21
					new_array[20] = list(frame)[2] #match the boost bit to the last bit in the new array
					new_array[0:20] = list(frame)[3:23]
					
					#frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
					
					# Write the modified data back to the dataset
					hdf[key] = new_array

		print(f"Processed file: {filename}")

print("Processing completed for all files.")
