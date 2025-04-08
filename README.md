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

### Viewing Examples
For viewing the example database of my personal library, download the [example.db file](https://github.com/Nathan-Wunschl/pitfloor/blob/main/example.db) and upload it to [SQLite Viewer](https://inloop.github.io/sqlite-viewer/). There are two tables that are necessary, which is the **albums** table and the **tracks** table. 

#### Note
For some tracks, I did have to manually change multiple values outside of the database and the program. There were only two, and they were both New Standard Elite Split-EP releases. This wasn't super difficult thanks to [MusicBrainz Picard](https://picard.musicbrainz.org/), but it was still something I thought I'd mention.

#### Albums Table
Each unique album will have its own entry in this table. It will have an assigned ID, as well as the name of the artist, album, and the date it was released (if it was not found on [metallum](https://www.metal-archives.com/), it will use the original value).

#### Tracks table
Every file that is parsed through the program will be added to this table, and assigned the same ID corrosponding to the album they are on. I did this to make it possible to edit the database entries manually later, allowing you to rerunning the script to reapply any changed values.

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

### Post Run
I recommend opening up the database file, either in a desktop app or at [SQLite Viewer](https://inloop.github.io/sqlite-viewer/), and double checking any values that may be amiss, I designed the app to reapply all values in the albums table, so if there are any albums with an incorrect date, artist name, or album name, simply change them in the viewer, overwrite the database file to where it was originally, and rerun the script!

### Troubleshooting
If you get any errors when the script starts running relating to "sqlite3" or the script finishes immediately, this is an issue with the paths in the json file. Please ensure that your system paths are completely correct and that there is a leading '/' (/users/nathan/test/)
