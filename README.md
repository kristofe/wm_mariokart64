Here's a structured, well-organized, and polished version of your README file. I've clarified the explanations, added commands where necessary, and ensured everything is consistent and easy to follow.

---

# AI-MarioKart64

**Training DIAMOND to play MarioKart64 using a Neural Network**

## Table of Contents
- [Running the Model](#running-the-model)
- [Training the Model](#training-the-model)
- [Creating Spawns](#creating-spawns)
- [Training on a Different Game](#training-on-a-different-game)

---

## Running the Model

### Steps to Run the Model

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Dere-Wah/AI-MarioKart64.git
   cd AI-MarioKart64/diamond
   ```

2. **Install Requirements**  
   - **For CPU (not recommended):**  
     ```bash
     pip3 install torch==2.4.1
     ```
   - **For GPU (recommended):**  
     Install PyTorch with CUDA support:  
     ```bash
     pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
     ```  
     To install a different CUDA version, refer to the [PyTorch Installation Guide](https://pytorch.org/).

3. **Set Up the Trained Model**  
   - Create a folder named `trained`:  
     ```bash
     mkdir trained
     ```
   - Download the pre-trained model (~1.42 GB) from [HuggingFace](https://huggingface.co/DereWah/diamond-mariokart64).
   - Place the root folder `csgo` inside the `trained` folder. The structure should look like this:
     ```
     trained/
       └── csgo/
           ├── config
           ├── model
           └── spawn
     ```

4. **Update the Code Configuration**  
   Open the `src/play.py` file and update the variable representing the model folder to point to the folder you created earlier. If you called it `./trained` you're good to go already.

5. **Run the Model**  
   ```bash
   python src/play.py
   ```  
   Follow the on-screen instructions to play:
   - **Steering:**  
     - Press `1` to steer left.  
     - Press `0` to steer right.  
     - Numbers in between (e.g., `2`, `3`) steer progressively.
   - **Reset Simulation:** Press `Enter` to reset and jump to the next spawn.

---

## Training the Model

### Steps to Train the Model

1. **Download the Dataset**  
   Download the dataset from [HuggingFace](https://huggingface.co/datasets/DereWah/mk64-steering) and extract the files:
   ```bash
   tar -xvf LR.tar.gz
   ```

   If you plan to create your own dataset, refer to the `README` file in the dataset folder for the required format.

2. **Split the Dataset**  
   Select 10% of the dataset as the test split. Run the following script:
   ```bash
   python src/select_test_split.py <dataset-folder>
   ```
   This will generate a `test_split.txt` file containing the selected test files.

3. **Preprocess the Dataset**  
   Run the preprocessing script:
   ```bash
   python src/process_csgo_tar_files.py <dataset-folder> <output-folder>
   ```
   Ensure the output folder (e.g., `./processed`) exists before running the command. After processing, you should see two subfolders:  
   - `low_res/`  
   - `full_res/`

4. **Update Configuration Files**  
   Edit the `config/env/csgo.yaml` file to update the paths to your dataset files. Ensure the paths are correct for both the processed dataset and any additional configurations.

5. **Train the Model**  
   Run the training script:
   ```bash
   python src/training.py
   ```
   Adjust the training parameters in the configuration files as needed. For more details, refer to [this blog post](https://derewah.dev/projects/ai-mariokart) under the section **Optimizing Training Parameters**.

6. **Optional:** Leave the `full_res` and `low_res` input prompts in the configuration files empty to auto-complete based on the paths provided in the config.

---

## Creating Spawns

"Spawns" represent interesting starting points for the simulation, such as entering a tunnel or crossing the finish line.

### Steps to Generate New Spawns

1. Run the spawn generation script:
   ```bash
   python src/spawn.py <full-res-folder> ./trained/
   ```
   - `<full-res-folder>`: Folder containing the full-resolution dataset (`.hdf5` files).  
   - `./trained/`: Path to the model folder.

2. The new spawns will be saved in:
   ```
   ./trained/csgo/spawn/
   ```
   Each spawn includes an image representation, so you can visualize the starting point.

---

## Training on a Different Game

This feature is still under development. For now, refer to [this blog post](https://derewah.dev/projects/ai-mariokart) for more information on how to train models on different games.

---

## Resources

- [Diamond MK64 Model](https://huggingface.co/DereWah/diamond-mariokart64)  
- [MK64 Steering Dataset](https://huggingface.co/datasets/DereWah/mk64-steering)

---
