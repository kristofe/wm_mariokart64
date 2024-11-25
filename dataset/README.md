# **AI-MarioKart64 Dataset Documentation**

This document provides a clear and structured explanation of the **AI-MarioKart64 Dataset** setup, usage, and structure.

---

## **Dataset Overview**
The AI-MarioKart64 dataset follows the same structure as the [Counter-Strike Behavioral Cloning dataset](https://github.com/TeaPearce/Counter-Strike_Behavioural_Cloning).  

### **Dataset File Structure**
Each `.hdf5` file contains **1000 frames**, indexed from `0` to `999`. Each frame includes two components:  

1. **`frame_<i>_x`:** Image data.  
    - Original resolution (full_res).  
    - Three color channels in **BGR format**.  

2. **`frame_<i>_y`:** Player input data.  
    - **First 21 values**:  
        - One-hot vector representing steering direction.  
        - Gradual steering (e.g., intermediate values between full left and full right).  
        - Manual data only captures **complete steering** left or right.
    - **Last value**:  
        - `1`: Using Boost

---

<details>
    <summary>v1 Dataset Structure</summary>

    In version 1 of the dataset, only **steering data** was captured.  

    - **`frame_<i>_y` structure**: A 20-length one-hot vector for steering direction.  
        - `[1, 0, 0, ..., 0]` → Steer Left (`-1.0`).  
        - `[0, ..., 0, 1]` → Steer Right (`1.0`).  
        - Intermediate positions represent **progressive steering** (e.g., no steer = `0` in the middle).  

</details>

---

## **Setup - Automatic Playing**

### **Step 1: Environment Setup**
1. Clone the [NeuralKart repository](https://github.com/rameshvarun/NeuralKart).  
2. Follow the setup instructions in the repository.  
3. Create a separate **Anaconda environment** for working on this project.  

---

### **Step 2: Setup BizHawk QuickStates**
The `Play.Lua` script automatically resets the game to the quickstate in slot 1 when the track has completed 3 laps.

Make sure to save a State in that slot at the beginning of the race, to allow the script to reset. To do so press SHIFT + F1 when the race starts.

This dataset collection format only currently supports "screenshot mode". (It is enabled by default, so you should not encounter any issue with this.)
---

### **Step 3: Replace and Configure `predict-server.py`**
1. Replace the `predict-server.py` script in NeuralKart with the provided version.  
2. Edit the output file paths in the script.  
3. Run the script to start the prediction server.  
4. You can run the script with custom parameters: 
   - `--boost=<x>` is the probability 1/x that boost is used

---

## **Setup - Manual Playing**

In order to capture a good dataset, some track laps should be manually recorded. In these tracks you should focus on collecting input on "corner cases": basically stuff that rarely happens in gameplay but behaviour that you still want to implement. An example is going against walls: if there is no data about how bumping works the model will blur this type of actions. Same goes for going against a tree, falling off a map, going backwards, etc. Try to use only actions that are captured by the dataset, so turning + using boost, & always accelerate.

Configure `manual-config.yaml` to your needs. You can leave input values as default. For the game window name, if you're not sure leave it as is.

Open BizHawk emulator and load into a track. As soon as the track starts create a SaveState in position 1. This will be used by you to reset the map when you are coming to the end of the 3rd lap. Simply press F1 to reset the run.

Run `manual-capture-data.py`. If you put in the wrong window name it will throw an error not finding the emulator window. It will also display the currently open windows: go back in the config and paste in it the window name corresponding to BizHawk.

If you get an error about capturing screenshots, first try and capturing a screenshot on your own in bizhawk (press ctrl+C), then restart the script.

To stop the script press ESC.

---
