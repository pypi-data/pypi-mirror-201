# TUD AIS
This package contains lab material for the module Angewandte Intelligente Signalverarbeitung offered by Professor 
Birkholz at TU Dresden.


## Setup (Linux, Mac OS X, Windows)
To obtain the lab material, you can simply install the package just like any other Python package. We recommend 
setting up a virtual environment before installing. The steps to do so are as follows:

### Step 0: Get Python
If you don't already have it installed, [download and install the current version of Python for your platform.](https://www.python.org/downloads/)

### Step 1: Set up your working directory
1. Create a folder in a suitable location where all the lab material will be placed 
(e.g. ``C:\Users\MyUserName\Documents\TUD-AIS-Lab``). Just to be safe, choose a path that is not too long and that 
does not contain spaces.
2. Open a shell (Linux), terminal (Mac), or command prompt (Windows) and navigate to the created folder.
3. Create a virtual environment called ``.ais-env`` by entering the following command:
    ```bash
    python -m venv .ais-env
    ```
4. Activate the virtual environment by entering the following command depending on your operating system:

    **Linux or Mac**:
    ```bash
    source .ais-env/bin/activate
    ```
    **Windows**:
    ```
    .ais-env\Scripts\activate.bat
    ```
    You should now see the name of your environment showing up in parentheses at the beginning of the line:
    ![Screenshot showing the active virtual environment in the command prompt](doc/img/fig-activate-venv.png "Active virtual environment")
    
    You can deactivate the virtual environment at any time by entering the command ``deactivate``.

### Step 2: Install the lab material
1. Make sure that your virtual environment is active (see Step 1.4 above).
2. Install the lab material by entering the following command:
    ```
    pip install tudais
    ```
   This will install all dependencies of the lab materials and the lab materials 
   itself. It may take a while.
   
### Step 3: Start the lab
1. Make sure that your virtual environment is active (see Step 1.4 above).
2. Enter the following command:
   ```
   tud-ais-start
   ```
   This will open your default web browser and show the root folder of the lab material.
   
### Step 4: Have fun working through the notebooks
Some of the notebooks are explicitly structured and contain detailed instructions 
(code-along), while other notebooks are far less guided and offer an opportunity to 
apply your acquired knowledge (hands-on).

The recommended order of tackling the notebooks is as follows:
1. `preprocessing/Lego-Sets/Lego Sets Preprocessing.ipynb` (code-along)
2. `classification/Wine-Quality/Klassifikation von Wein.ipynb` (code-along)
3. `regression/Wine-Alcohol/Vorhersage des Alkoholgehalts von Wein.ipynb` (code-along)
4. `classification/Titanic/Untergang der Titanic.ipynb` (hands-on) 
5. `regression/House-Prices/Vorhersage von Immobilienpreisen.ipynb` (hands-on)
   
### Step 5: Submit the completed material
Once you have completed the material, you may submit your solution for 
credit or qualification purposes.
1. Make sure that your virtual environment is active (see Step 1.4 above).
2. Enter the following command:
   ```
   tud-ais-prepare-submission
   ```
   When prompted, enter your personal information. This will create a ZIP archive 
   with all required files.
3. Send the ZIP archive to your lab supervisor via email.

If you run into any problems in this process, contact [Christian Kleiner](mailto:christian.kleiner@tu-dresden.de?subject=Praktikum%20AIS) for 
assistance.
   
   


 
 



