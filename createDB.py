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


def readJson(file):
    with open(file) as jsonFile:
        data = json.load(jsonFile)
    for song in data:
        yield song, data[song]

if __name__ == '__main__':
    updateDB()
