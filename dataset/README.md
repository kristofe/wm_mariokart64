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

    - **Last 4 values**:  
        - Experimental parameters encoding the **current track** using a binary representation.  
        - 4-bit binary value (e.g., `0000`, `0001`), mapping to 16 tracks.  
        - The goal: dynamically modify the environment by switching track parameters.  

---

### **Track Mapping Table**
Below is a template for mapping the binary track parameters to the corresponding tracks.  

Here’s the updated table with dividers for each trophy:

---

#### **Mushroom Cup 150cc**
| **Track Binary (4-bit)** | **Decimal** | **Track Name**        |
|--------------------------|-------------|-----------------------|
| 0000                     | 0           | Luigi Raceway         |
| 0001                     | 1           | Moo Moo Farm          |
| 0010                     | 2           | Koopa Troopa Beach    |
| 0011                     | 3           | Kalimari Desert       |

---

#### **Fire Flower Cup 150cc**
| **Track Binary (4-bit)** | **Decimal** | **Track Name**        |
|--------------------------|-------------|-----------------------|
| 0100                     | 4           | Toad's Turnpike       |
| 0101                     | 5           | Frappe Snowland       |
| 0110                     | 6           | Choco Mountain        |
| 0111                     | 7           | Mario Raceway         |

---

#### **Star Cup**
| **Track Binary (4-bit)** | **Decimal** | **Track Name**        |
|--------------------------|-------------|-----------------------|
| 1000                     | 8           | Wario Stadium         |
| 1001                     | 9           | Sherbet Land          |
| 1010                     | 10          | Royal Raceway         |
| 1011                     | 11          | Bowser's Castle       |

---

#### **Special Cup**
| **Track Binary (4-bit)** | **Decimal** | **Track Name**        |
|--------------------------|-------------|-----------------------|
| 1100                     | 12          | D.K.'s Jungle Parkway |
| 1101                     | 13          | Yoshi Valley          |
| 1110                     | 14          | Banshee Boardwalk     |
| 1111                     | 15          | Rainbow Road          |

--- 

This format organizes the tracks neatly by trophies.
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

## **Setup**

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

### **Additional Notes**
- Always ensure the `.state` file is correctly configured in `Play.lua`.  
- The dynamic map shaping using binary parameters for tracks is experimental and subject to improvement.  

---
