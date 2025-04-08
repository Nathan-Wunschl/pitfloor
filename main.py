# Pitfloor
# Nathan Wunschl
# v 0.1.0
import metallum
import os
import music_tag
import sys
import json
from titlecase import titlecase
import time
import sqlite3

print("Welcome to pitfloor!\n\n")
print("WARNING: THIS APP COMMITS METADATA IMMEDIATELY, WHICH MAY CAUSE ERRORS AND OR UNWANTED CHANGES. PLEASE MAKE A BACKUP OF YOUR LIBRARY BEFORE RUNNING THIS SCRIPT\n")

time.sleep(3)

cont = input("Please type 'OK' to accept, or type 'NO' to decline.\n").lower()

while cont != 'ok' and cont != 'no':
    cont = input("Invalid input. Please enter either 'OK' or 'NO'\n").lower()

if cont == 'no':
    sys.exit()

with open("Values.json") as j:
    v = json.load(j)
    path = v["Music Path"]
    db = v["DB Path"]
    label = v["Record Label"]

types = ('.mp3', '.aac', '.ogg', '.flac', '.m4a', '.wav', '.aiff', '.aif')

c = sqlite3.connect(db + "sql.db")
c.execute("CREATE TABLE IF NOT EXISTS albums ( id INTEGER PRIMARY KEY AUTOINCREMENT, artist TEXT NOT NULL, album TEXT NOT NULL, year TEXT  );")
c.execute("CREATE TABLE IF NOT EXISTS tracks ( id INTEGER NOT NULL, path TEXT NOT NULL  );")
cursor = c.cursor()

c.commit()

def labelCheck(label, tag, f):
    if label in str(tag):
        artist = str(f['album']).split(" | ", 1)[0]
        if artist + " - " in str(f['album']):
            album = str(f['album']).split(" | ", 1)[1]
            f['album'] = album
        f['album artist'] = artist
        f['artist'] = artist
        f.save()
        print(f"Artist Tag changed from {label} to {artist}")

def getYear(artist, album, track, f):
    try:
        print(f"Original Date: {str(f.raw['year'])}")
        if "promo " or "demo " in album.lower():
            year = [int(s) for s in album.lower().split() if s.isdigit()]
            f.raw['year'] = year[0]
            f.save()
            print("demo or promo found, year set to ", year[0])
            return()
        albums = metallum.album_search(str(f['album']), band=str(f['artist']), strict=False)
        album = albums[0].get()
        date = album.date
        date = date.strftime("%B %d, %Y")
        f.raw['year'] = str(date)
        print(f"New Date: {str(f.raw['year'])}")
        f.save()
    except Exception as exception:
        print(exception)
def fix(args, tag, artist, album, title, track, f):
    if '-l' in args:
        labelCheck(label, tag, f)
    if '-t' in args:
        title = str(f['tracktitle'])
        album = str(f['album'])
        artist = str(f['artist'])
        print(f"Original: {title} on {album} by {artist}")
        tempTitle = title.lower().removeprefix(artist.lower() + " - ").removeprefix(artist.lower() + " | ")
        tempAlbum = album.lower().removeprefix(artist.lower() + " - ").removeprefix(artist.lower() + " | ")
        rmTitleLength = len(title) - len(tempTitle)
        rmAlbumLength = len(album) - len(tempAlbum)
        if rmTitleLength != 0:
            title = title[rmTitleLength:]
        if rmAlbumLength != 0:
            album = album[rmAlbumLength:]
        f['tracktitle'] = title
        f['album'] = album
        f['artist'] = titlecase(artist.lower())
        f['albumartist'] = titlecase(artist.lower())
        print(f"New: {str(f['title'])} on {str(f['album'])} by {str(f['artist'])}")
    if '-y' in args:
        getYear(artist, album, track, f)
    return(tag, artist, album, title, track)

def run(path, label):
    for subdir, dirs, files in os.walk(path):
        for track in sorted(files):
            file = (subdir + "/" + track)
            if track.endswith(types):
                if not track.startswith("._"):
                    print(f"Fixing {track}")
                    f = music_tag.load_file(file)
                    tag = f['album artist']
                    artist = f['artist']
                    album = f['album']
                    title = f['tracktitle']
                    if str(album) == "":
                        f['album'] = title
                        f.save()
                        print(f"Blank album changed to track title ({str(f['album'])})")
                    fix(('-l', '-t'), tag, artist, album, title, track, f)
                    f.save()
                    print(f"Checking if {track} is in database...")
                    cursor.execute("SELECT EXISTS(SELECT 1 FROM tracks WHERE path=? LIMIT 1)", (str(file),))
                    if cursor.fetchone()[0] == 1:
                        cursor.execute("SELECT id FROM tracks WHERE path=?", (str(file),))
                        id = cursor.fetchone()[0]
                        cursor.execute("SELECT * FROM albums WHERE id=?", (id,))
                        print(f"{track} already in DB! Applying values...")
                        dbVals = cursor.fetchall()
                        f['artist'] = dbVals[0][1]
                        f['album'] = dbVals[0][2]
                        f.raw['year'] = dbVals[0][3]
                        f.save()
                    else:
                        print(f"{track} not in database!")
                    print(f"Checking if {str(f['album'])} is in database...")
                    cursor.execute("SELECT EXISTS(SELECT 1 FROM albums WHERE album=? AND artist=? LIMIT 1)", (str(f['album']), str(f['artist'])))
                    if cursor.fetchone()[0] != 1:
                        fix('-y', tag, artist, album, title, track, f)
                        f.save()
                        cursor.execute("INSERT INTO albums (artist, album, year) VALUES (?, ?, ?)", (str(f['artist']), str(f['album']), str(f.raw['year'])))
                        c.commit()
                        print(f"{track} finished")
                        cursor.execute("SELECT id FROM albums WHERE album=? AND artist=?", (str(f['album']), str(f['artist'])))
                        id = cursor.fetchone()[0]
                    else:
                        print(str(album) + " already in DB!")
                        cursor.execute("SELECT id FROM albums WHERE album=? AND artist=?", (str(f['album']), str(f['artist'])))
                        id = cursor.fetchone()[0]
                    cursor.execute("SELECT EXISTS(SELECT 1 FROM tracks WHERE path=? LIMIT 1)", (str(file),))
                    if cursor.fetchone()[0] != 1:
                        cursor.execute("INSERT INTO tracks VALUES (?, ?)", (id, file))
                        c.commit()
                        print(track + " finished")
run(path, label)

print("Tasks complete! All album data is stored in the sql.db file. If there are any values that are incorrect, use an sql editor to change the value in the table and rerun the script! The values will be changed automatically.\n")
print("Thank you for using pitfloor! https://github.com/Nathan-Wunschl :)")
