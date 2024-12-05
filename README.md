
# AI-MarioKart64

**Training DIAMOND to play MarioKart64 using a Neural Network**

https://www.youtube.com/watch?v=c2CpUxQxDI4&ab_channel=DereDev

## Table of Contents
- [Running the Model](#running-the-model)
- [Training the Model](#training-the-model)
- [Creating Spawns](#creating-spawns)
- [Training on a Different Game](#training-on-a-different-game)

---

<a target="_blank" href="https://colab.research.google.com/github/Dere-Wah/AI-MarioKart64/blob/main/colab/AIMK64.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## Running the Model

### Steps to Run the Model

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Dere-Wah/AI-MarioKart64.git
   cd AI-MarioKart64/diamond
   ```

2. **Install Requirements**  

   - **Install pip requirements:**
     ```bash
     pip3 install -r requirements.txt
     ```

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

3. **Run the Model**  
   When running the python script, the model will be downloaded automatically from [HuggingFace](https://huggingface.co/DereWah/diamond-mariokart64) (~1.42 GB).

   ```bash
   python src/play.py
   ```  
   When running, you'll be able to choose which model to play. Currently, only a model trained on Luigi's Raceway is available (called LR). You can view all the currently available models on [HuggingFace](https://huggingface.co/DereWah/diamond-mariokart64/tree/main).

   ```Model name: lr```

   Follow the on-screen instructions to play:
   - **Steering:**  
     - Press `LEFT ARROW` to steer left.  
     - Press `RIGHT ARROW` to steer right.
     - Press `D` to use the boost mushroom item, if you have any.
   - **Reset Simulation:** Press `Enter` to reset and jump to the next spawn.

> ***The model has been trained on analog inputs, but the current playing setup only allows for full steers (either total left or total right). Support for analog input is being worked on.***

4. **Optional: download manually the model**: If you downloaded the model manually, or have a local model you want to run without having to download it from HuggingFace, you can run the same script with an additional argument --model, and specify the path to the model you want to play.

   ```bash
   python src/play.py --model <path-to-your-model>
   ```  

   When running this, you'll be prompted again with the model name. Write the name of the model, which should be the name of the root folder of the model (and the same for the .pt file)
---

## Training the Model on a track

A [google colab](https://colab.research.google.com/drive/1B63q1QSxadEPbkkzpMV6WR_R3ZBj-cXk?usp=sharing) notebook is available to train the model on a dataset with more ease. If you encounter any issue with the colab feel free to contact me on discord: @DereWah or open an issue here.

### Steps to Train the Model

1. **Download the Dataset**  
   Download the dataset from [HuggingFace](https://huggingface.co/datasets/DereWah/mk64-steering).
   You should put all the dataset files of the same track in the same folder.

   If you plan to create your own dataset, refer to the [**README**](https://github.com/Dere-Wah/AI-MarioKart64/tree/main/dataset) file in the dataset folder for the required format.
   If your dataset files are already extracted into .hdf5 files, compress them into a .tar.gz and resume from here.
   ***If you collect a dataset from a map that is still not present on [HuggingFace](https://huggingface.co/datasets/DereWah/mk64-steering), please consider contributing and opening a pull request to add it to the available datasets!***

2. **Preprocess the Dataset**  
   Run the preprocessing script:
   ```bash
   python src/process_dataset_tar.py <dataset-folder> <output-folder>
   ```
   
   - The dataset folder should be the path to the folder that contains the single .tar.gz files together.
   - The output folder is where processing is gonna happen, and it should not exist.

   - This script will also select a 10% split of .hdf5 files that will be used for the testing split.

3. **Update Configuration Files**  
   Edit the `config/env/csgo.yaml` file to update the paths to your dataset files. Ensure the paths are correct for both the processed dataset and any additional configurations.
   **IMPORTANT** - Make sure the paths are ABSOLUTE PATHS!

4. **Train the Model**  
   Run the training script:
   ```bash
   python src/main.py
   ```
   Adjust the training parameters in the configuration files as needed. For more details, refer to [this blog post](https://derewah.dev/projects/ai-mariokart) under the section **Optimizing Training Parameters**.

5. **Optional:** When running the training script, you will be prompted with paths to the low res and full res datasets again. If you have already inserted them in the configuration file, you can just ignore these prompt and leave them empty. They will autocomplete to the config.

---

## Creating Spawns

"Spawns" represent interesting starting points for the simulation, such as entering a tunnel or crossing the finish line. These are basically the "prompts" of the simulation.

### Steps to Generate New Spawns

1. Run the spawn generation script:
   ```bash
   python src/spawn.py <full-res-folder> <model-path>
   ```
   - `<full-res-folder>`: Folder containing the full-resolution dataset (`.hdf5` files).  
   - `<model-path>`: Path to the model folder.

   > ***It should be noted that when downloading the dataset automatically from HuggingFace, the model will be put in a temporary path. Since this path varies based on the machine, you will have to figure out yourself where the model folder is.***

2. The new spawns will be saved in the /spawn/ folder of the model.
   Make sure the indexes of the spawn names are progressive and start from 0, otherwise you'll have some spawns overwriting existing ones.
   Each spawn includes an image representation, so you can visualize the starting point.

---

## Training on a Different Game

Refer to [this blog post](https://derewah.dev/projects/ai-mariokart) for more information on how to approach the Diamond model to train on different generic games.

---

## Resources

- [Diamond MK64 Model](https://huggingface.co/DereWah/diamond-mariokart64)  
- [MK64 Steering Dataset](https://huggingface.co/datasets/DereWah/mk64-steering)

---
