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
    - **First 3 values**:  
        - `1`: Acceleration.  
        - `2`: Braking.  
        - `3`: Using an active item.  

    - **Next 20 values**:  
        - One-hot vector representing steering direction.  
        - Gradual steering (e.g., intermediate values between full left and full right).  
        - Manual data only captures **complete steering** left or right.

    - **Last 16 values**:  
        - Experimental parameters encoding the **current track** using a OneHot representation
        - 16-bit onehot value (e.g., `1000000000000000`, `0100000000000000`), mapping to 16 tracks.
        - Onehot is preferred over a 4-bits representation because it allows multiple maps to be "enabled" in the future, to mix them together.
        - The goal: dynamically modify the environment by switching track parameters.  

---

### **Track Mapping Table**


### **Mushroom Cup**
| **Track OneHot (16-bit)**  | **Decimal** | **Track Name**        |
|---------------------------|-------------|-----------------------|
| 1000000000000000           | 0           | Luigi Raceway         |
| 0100000000000000           | 1           | Moo Moo Farm          |
| 0010000000000000           | 2           | Koopa Troopa Beach    |
| 0001000000000000           | 3           | Kalimari Desert       |

---

### **Fire Flower Cup**
| **Track OneHot (16-bit)**  | **Decimal** | **Track Name**        |
|---------------------------|-------------|-----------------------|
| 0000100000000000           | 4           | Toad's Turnpike       |
| 0000010000000000           | 5           | Frappe Snowland       |
| 0000001000000000           | 6           | Choco Mountain        |
| 0000000100000000           | 7           | Mario Raceway         |

---

### **Star Cup**
| **Track OneHot (16-bit)**  | **Decimal** | **Track Name**        |
|---------------------------|-------------|-----------------------|
| 0000000010000000           | 8           | Wario Stadium         |
| 0000000001000000           | 9           | Sherbet Land          |
| 0000000000100000           | 10          | Royal Raceway         |
| 0000000000010000           | 11          | Bowser's Castle       |

---

### **Special Cup**
| **Track OneHot (16-bit)**  | **Decimal** | **Track Name**        |
|---------------------------|-------------|-----------------------|
| 0000000000001000           | 12          | D.K.'s Jungle Parkway |
| 0000000000000100           | 13          | Yoshi Valley          |
| 0000000000000010           | 14          | Banshee Boardwalk     |
| 0000000000000001           | 15          | Rainbow Road          |

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

### **Step 2: Update Paths**
1. Open `Play.lua`:  
   - Update the **file path** to your `.state` file.  
   - This `.state` file represents the game state after completing 3 laps (prevents the race from ending).  

   > **Tip:** Save the state in the emulator (BizHawk) by starting a lap and saving via the UI.  

2. **Screenshot Mode (Optional):**  
   - If saving screenshots to disk, update the **file path** for screenshot storage.  
   - Using the **clipboard** is recommended to reduce disk writes.  

---

### **Step 3: Replace and Configure `predict-server.py`**
1. Replace the `predict-server.py` script in NeuralKart with the provided version.  
2. Edit the file paths in the script.  
3. Run the script to start the prediction server.  

---

## **Setup - Manual Playing**

In order to capture a good dataset, some track laps should be manually recorded. In these tracks you should focus on collecting input on "corner cases": basically stuff that rarely happens in gameplay but behaviour that you still want to implement. An example is going against walls: if there is no data about how bumping works the model will blur this type of actions. Same goes for going against a tree, falling off a map, going backwards, steering and accelerating at the same time, steering while being at a full stop, using action items when you have none, etc.

Configure `manual-config.yaml` to your needs. You can leave input values as default. For the game window name, if you're not sure leave it as is.

Open BizHawk emulator and load into a track. As soon as the track starts create a SaveState in position 1. This will be used by you to reset the map when you are coming to the end of the 3rd lap. Simply press F1 to reset the run.

Run `manual-capture-data.py`. If you put in the wrong window name it will throw an error not finding the emulator window. It will also display the currently open windows: go back in the config and paste in it the window name corresponding to BizHawk.

If you get an error about capturing screenshots, first try and capturing a screenshot on your own in bizhawk (press ctrl+C), then restart the script.

To stop the script press ESC.

### **Additional Notes**
- Always ensure the `.state` file is correctly configured in `Play.lua`.  
- The dynamic map shaping using binary parameters for tracks is experimental and subject to improvement.  

---
