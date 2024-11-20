# AI-MarioKart64 Dataset

Please refer to the first section of my blogpost: https://derewah.dev/projects/ai-mariokart 

# Structure

The dataset structure follows the same as https://github.com/TeaPearce/Counter-Strike_Behavioural_Cloning

Each single dataset .hdf5 contains 1000 frames. Each frame, numbered 0-999 contains 2 file structures:

frame_<i>_x which contains the image data. It has the same dimensions as the original image captured (full_res) and has 3 color channels. The channels are in BGR format.
**Because of a mistake in my first dataset collection setup, the first ever version of MK64 was trained on a dataset with RGB channels. This caused the network to train with B & R channels swapped. In the new version I'm working on this should be fixed**

frame_<i>_y contains input data. It consists of a onehot vector of size 20, in which each value maps to a steering direction. A 1 in the first position maps to a steering completely to the left
[1, 0, 0, ... 0] = -1.0 = Steer Left
[0, ... 0, 0, 1] = 1.0 = Steer Right
All the other values map to a step of 0.1 and a progressive steering. A 1 in the middle means no steer.

**In the new version I'm working on, on top of these values there will be a few other ones, such as accelerating / braking, using the active item, and some values to refer to currently active maps.**

# SETUP

Follow the setup tutorial in the original repository: https://github.com/rameshvarun/NeuralKart

To work on this part of the project I recommend using a different anaconda environment from the one you use for the diamond training.

Before starting, open Play.lua and change the file path of the .state file to match yours. This file is basically the state that gets loaded when you complete 3 laps of the map, to prevent the race from ending.

To actually get a state, start a lap on BizHawk and then save a snapshot state via the emulator UI.

Also you can choose if to use the clipboard or save screenshots to a file for reading. I recommend using the clipboard as it allows for less hard-disk writes. If using "screenshots" mode, make sure to update that file path aswell.

Regarding predict-server.py: replace the script you get in the original NeuralKart repository with this one, open it and edit file paths and run it.



