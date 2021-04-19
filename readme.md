# Archi (Step 1)

This code is used to train the machine learning models to detect and read the pipe specs and the corrosion circuit markers in P&IDs

To use, clone or fork this repository. Then, store the drawings you want to digitise in the folder `..\data\images` (note that only .jpg files are accepted). Please name the files using three characters.

Afterwards, run `Archimech.ipynb` using Google Colaboratory and run all cells. This will generate two files named `boxes` and `corr_circuits`. You will need to copy these files into [Archimech_download](https://github.com/Luistoq/Archimech_download) to continue with the corrosion circuit marking step.