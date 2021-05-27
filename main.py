from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5.QtWidgets import QMessageBox  
from PyQt5.uic import loadUiType
import sys
import logging
import os
from os import path
import numpy as np
import librosa
# import sounddevice as sd
from pydub import AudioSegment
import spectro_features


logging.basicConfig(filename="logFile.log",format='%(asctime)s %(message)s',filemode='w')
logger = logging.getLogger()
logger.setLevel(20)

MAIN_WINDOW,_=loadUiType(path.join(path.dirname(__file__),"main.ui"))

class Ui_MainWindow(QtWidgets.QMainWindow,MAIN_WINDOW):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

        self.slider.setEnabled(False)
        self.flag1 = False
        self.flag2 = False
        self.mixedAudio = None
        self.songs = [None,None]

        self.connect_func()

    def connect_func(self):
        self.browseButton.clicked.connect(lambda: self.Browse(0))
        self.browseButton_2.clicked.connect(lambda: self.Browse(1))
        self.slider.valueChanged.connect(lambda: self.sliderLabel.setText(str(self.slider.value())+"%"))
        # self.searchBtn.clicked.connect(lambda: self.Mixer())

    # def Load(self, file):
        
    #     return x , sr

    def Browse(self,indx):
        self.statusbar.showMessage("Loading Audio File %s"%(indx+1))
        file_name,_ = QtWidgets.QFileDialog.getOpenFileName(self, 'choose a song', os.getenv('HOME'),"")
        wav_audio = "wav_audio.wav"
        logger.info("Reading first minute of the mp3")        
        mp3_audio = AudioSegment.from_mp3(file_name)[:60000] 
        mp3_audio.export(wav_audio, format="wav")
        logger.info("Converted to wav")
        file_data , sr = librosa.load(wav_audio)
        logger.info("Read wav format and return the data")
        # logger.info("Audio File %s Loaded"%(indx+1))
        # if file == "":
        #     logger.info("loading cancelled")
        #     self.statusbar.showMessage("Loading cancelled")
        #     pass
        # else:
        logger.info("Loading data")
        # file_data,sr = self.Load(file_name)
        print(file_data, sr)
        # self.labels[indx].setText(file.split('/')[-1])
        self.statusbar.showMessage("Loading Done")
        logger.info("Loading Done")
        # sd.play(file_data, sr)
        # plt.figure(figsize=(9, 5))
        # librosa.display.waveplot(x, sr=sr)
        # plt.show()
        self.songs[indx] = spectro_features.Load_Song(file_name, file_data, sr)
        print(self.songs)
        
        if indx == 0:
            self.flag1 = True
        if indx == 1:
            self.flag2 = True
        if self.flag1 == self.flag2 == True:
            self.slider.setEnabled(True)
    
    # def Mixer(self):
    #     logger.info("Start Mixing 2 songs")
    #     w = self.slider.value()/100.0
    #     self.mixedAudio = (w*self.audioDatas[0] + (1.0-w)*self.audioDatas[1])

    # def Spectrogram(self, file, sr, indx):
    #     #display Spectrogram
    #     # X = librosa.stft(file)
    #     # Xdb = librosa.amplitude_to_db(abs(X))
    #     # plt.figure(figsize=(9, 5))
    #     # librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz') 
    #     #If to pring log of frequencies  
    #     #librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='log')
    #     # plt.colorbar()
    #     # plt.show()
    #     spectro = librosa.feature.melspectrogram(file, sr=sr)
    #     print('spectro', spectro)

    # def Features(self, file, sr, indx):
    #     #chroma_stft
    #     chroma_stft = librosa.feature.chroma_stft(file, sr=sr)
    #     self.song_features[0].append(self.Hash(chroma_stft))
    #     # print(chroma_stft)

    #     #zero_crossings
    #     # zero_crossings = librosa.zero_crossings(file, pad=False)
    #     # #print('sum of zero_crossings = ', sum(zero_crossings),zero_crossings_hash)
    #     # self.song_features[0].append(self.Hash(zero_crossings))

    #     #spectral centroid -- centre of mass -- weighted mean of the frequencies present in the sound
    #     # import sklearn
    #     spectral_centroids = librosa.feature.spectral_centroid(file, sr=sr)[0]
    #     # spectral_centroids.shape
    #     # Computing the time variable for visualization
    #     # frames = range(len(spectral_centroids))
    #     # t = librosa.frames_to_time(frames)
    #     # Normalising the spectral centroid for visualisation
    #     # def normalize(x, axis=0):
    #     #     return sklearn.preprocessing.minmax_scale(x, axis=axis)
    #     #Plotting the Spectral Centroid along the waveform
    #     # librosa.display.waveplot(file, sr=sr, alpha=0.4)
    #     # plt.plot(t, spectral_centroids, color='r')
    #     # plt.show()
    #     # print('spectral_centroids')
    #     self.song_features[0].append(self.Hash(spectral_centroids))

    #     #rolloff
    #     # spectral_rolloff = librosa.feature.spectral_rolloff(file, sr=sr)[0]
    #     # # librosa.display.waveplot(file, sr=sr, alpha=0.4)
    #     # # plt.plot(t, spectral_rolloff, color='r')
    #     # # print('rolloff')
    #     # self.song_features[0].append(self.Hash(spectral_rolloff))


    #     mfccs = librosa.feature.mfcc(file.astype('float64'), sr=sr)
    #     # print(mfccs.shape)
    #     #Displaying  the MFCCs:
    #     # librosa.display.specshow(mfccs, sr=sr, x_axis='time')
    #     # plt.show()
    #     # print('mfccs')
    #     self.song_features[0].append(self.Hash(mfccs))


    # def Hash(self, feature) -> str:
    #     data = Image.fromarray(feature)
    #     return imagehash.phash(data, hash_size = 16).__str__()


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())