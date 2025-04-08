# Pitfloor
A metadata fixer for metal music written in python

Currently only working on UNIX systems.

## Disclamer
This script changes metadata of files as it goes, so it is possible there will be errors or unwanted changes. I highly recommend you either backup your library before running this, or copy small chuncks of your library at a time to ensure it works as desired.

### Why This Exists
I created this script for multiple issues that I have faced with owning my own music collection...

1. Sometimes, artist names would be inconsistent across record labels. In specific, capitalization. (i.e. Putrid Pile vs. PUTRID PILE)
2. Record label names would be set as the artist, rather than the artist themselves (i.e New Standard Elite vs. Cerebral Effusion)
3. Album names would contain artist name (i.e Condemned - Desecrate the Vile)
4. Years would be incorrect due to record label release (i.e. 2001 vs 2015)

### Installation
Download the [latest release](github.com/Nathan-Wunschl/pitfloor/releases/latest) (both the Values.json and the main file) and save them to the same directory wherever you would like

Open a terminal window to the directory you installed the files, and run 
```
chmod +x main
```
This will make the file executable.

Now, edit the values of the Values.json file to contain the directories and record label you need (if you do not want to check for a record label, enter 'NONE' or leave it as "New Standard Elite")
Check the [example.json file](https://github.com/Nathan-Wunschl/pitfloor/blob/main/example.json) for more details.

Once everything is done, return to the directory in a terminal window and run
```
./main
```
This will start the program! 

### Troubleshooting
If you get any errors when the script starts running relating to "sqlite3" or the script finishes immediately, this is an issue with the paths in the json file. Please ensure that your system paths are completely correct and that there is a leading '/' (/users/nathan/test/)
