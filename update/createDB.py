import spectro_features
import load
import json
import os

def updateDB():
    jsonData = {}
    for file in os.scandir(r"songs"):
        if (file.path.endswith(".mp3")):
            sampRate, audioData = load.readAudio(file)
            songName = file.path.split('\\')[-1]
            data = spectro_features.Load_Song(songName, audioData, sampRate)
            jsonData.update(data)
    with open("db.json", "a") as outfile:
        json.dump(jsonData, outfile, indent=4)

updateDB()