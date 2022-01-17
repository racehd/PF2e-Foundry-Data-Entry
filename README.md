# PF2e-Foundry-Data-Entry

A script to aid with data entry for the PF2e system for Foundry VTT

To run it you must either use the binder link [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/TikaelSol/PF2e-Foundry-Data-Entry/HEAD) or download the repository.

In binder, the repo will take some time to load on first launch.  Once it does, double click the `DataEntry.ipynb` file and run the code in the top cell by either clicking the run button, choosing run from the cell menu, or using shift enter.  Then once the function definition has been run the function call cell should ask for an input, pasting in the text to be formatted and hitting enter will output the original text and the newly formatted text.

To run it a second time select the `reformat(input())` cell below and run it again (shift enter runs a single cell quickly).

The python code for the local version is under the pf2e_data folder (both files in this folder are required and should be in a folder named `pf2e_data`. The local version has a couple advantages over running on Binder, first is that if you install the python module pyperclip then the script will auto place the output on your clipboard, this won't work on the Binder environment unfortunately as Binder does not support this module.  The Binder version is also currently unable to detect new lines properly leading to some of the auto formatting being missed.
