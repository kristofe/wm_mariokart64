# AI-MarioKart64 Dataset

Please refer to the first section of my blogpost: https://derewah.dev/projects/ai-mariokart 

# SETUP

Follow the setup tutorial in the original repository: https://github.com/rameshvarun/NeuralKart

To work on this part of the project I recommend using a different anaconda environment from the one you use for the diamond training.

Before starting, open Play.lua and change the file path of the .state file to match yours. This file is basically the state that gets loaded when you complete 3 laps of the map, to prevent the race from ending.

To actually get a state, start a lap on BizHawk and then save a snapshot state via the emulator UI.

Also you can choose if to use the clipboard or save screenshots to a file for reading. I recommend using the clipboard as it allows for less hard-disk writes. If using "screenshots" mode, make sure to update that file path aswell.

Regarding predict-server.py: replace the script you get in the original NeuralKart repository with this one, open it and edit file paths and run it.


