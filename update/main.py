from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5.QtWidgets import QMessageBox  
from PyQt5.uic import loadUiType
from os import path
from scipy.io import wavfile
import logging
import sys
import os
from pydub import AudioSegment
from tempfile import mktemp
import spectro_features 

logging.basicConfig(filename="logFile.log",format='%(asctime)s %(message)s',filemode='w')
logger = logging.getLogger()
logger.setLevel(20)
MAIN_WINDOW,_=loadUiType(path.join(path.dirname(__file__),"task4.ui"))

class MainApp(QtWidgets.QMainWindow,MAIN_WINDOW):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        self.slider.setEnabled(False)
        self.flag1 = False
        self.flag2 = False
        self.mixedAudioData = None
        self.labels = [self.label, self.label_2]
        self.load1Btn.clicked.connect(lambda: self.loadsong(0))
        self.load2Btn.clicked.connect(lambda: self.loadsong(1))
        self.slider.valueChanged.connect(lambda: self.sliderLabel.setText(str(self.slider.value())+"%"))
        self.searchBtn.clicked.connect(lambda: self.mixer())
        self.audioDatas = [None, None]
        self.audioRates = [None, None]
        self.mixedSong = None
    
    def readAudio(self, audiopath):
        logger.info("Reading first minute of the mp3")
        mp3_audio = AudioSegment.from_mp3(audiopath)[:60000] 
        waveName = mktemp('.wav')
        mp3_audio.export(waveName, format="wav", parameters=["-ac", "1"])
        logger.info("Converted to wav")
        samplingFreq, audioData = wavfile.read(waveName)
        logger.info("Read wav format and return the data")
        return samplingFreq, audioData
    
    def loadsong(self , indx):
        self.statusbar.showMessage("Loading Audio File "+str(indx+1))
        global audFile
        audFile, audFormat = QtWidgets.QFileDialog.getOpenFileName(None, "Load Audio File "+str(indx+1),filter="*.mp3")
        logger.info("Audio File %s Loaded"%(indx+1))
        if audFile == "":
            logger.info("loading cancelled")
            self.statusbar.showMessage("Loading cancelled")
            pass
        else:
            logger.info("Loading data")
            global sampRate , audioData
            sampRate, audioData = self.readAudio(audFile)
            self.audioDatas[indx] = audioData 
            self.audioRates[indx] = sampRate
            self.labels[indx].setText(audFile.split('/')[-1])
            self.statusbar.showMessage("Loading Done")
            logger.info("Loading Done")
            
        if indx == 0:
            self.flag1 = True
        if indx == 1:
            self.flag2 = True
        if self.flag1 == self.flag2 == True:
            self.slider.setEnabled(True)
    
    def mixer(self):
        logger.info("Start Mixing 2 songs")
        w = self.slider.value()/100.0
        self.mixedAudioData = (w*self.audioDatas[0] + (1.0-w)*self.audioDatas[1])
        logger.info("Mixing Done")
        
        logger.info("Load Hash")
        self.mixedSong = spectro_features.Load_Song("Loaded Song", self.mixedAudioData, self.audioRates[0])
        print(self.mixedSong)
    
    #TODO Funcs.
    def check_similarity(self):
        pass
    
    def fill_table(self):
        pass
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()