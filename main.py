from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5.QtWidgets import QMessageBox  
from PyQt5.uic import loadUiType
from os import path
from spectro_features import difference, mapRanges
import logging
import sys
import spectro_features
import load
from createDB import readJson

logging.basicConfig(filename="logFile.log",format='%(asctime)s %(message)s',filemode='w')
logger = logging.getLogger()
logger.setLevel(20)
MAIN_WINDOW,_=loadUiType(path.join(path.dirname(__file__),"main.ui"))

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
        self.searchBtn.clicked.connect(self.mixer)
        self.audioDatas = [None, None]
        self.audioRates = [None, None]
        self.mixedSong = None
        self.dbPath = "db.json"
        self.results = []
    
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
            sampRate, audioData = load.readAudio(audFile)
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
        w = self.slider.value()/100.0
        
        logger.info("Load Hash")
        if self.flag1 == True and self.flag2 == False:
            self.mixedSong = spectro_features.Load_Song("Loaded Song", self.audioDatas[0], self.audioRates[0])
        if self.flag1 == False and self.flag2 == True:
            self.mixedSong = spectro_features.Load_Song("Loaded Song", self.audioDatas[1], self.audioRates[1])
        if self.flag1 == self.flag2 == True: 
            logger.info("Start Mixing 2 songs")
            self.mixedAudioData = (w*self.audioDatas[0] + (1.0-w)*self.audioDatas[1])
            self.mixedSong = spectro_features.Load_Song("Loaded Song", self.mixedAudioData, self.audioRates[0])
            logger.info("Mixing Done")
        print(self.mixedSong)
        
        self.check_similarity()


    def check_similarity(self):
        for songName, songHashes in readJson(self.dbPath):
            self.spectroDiff = difference(songHashes["spectrogram_Hash"], self.mixedSong["spectrogram_Hash"])
            self.featureDiff = 0

            self.melspectroDiff = difference(songHashes["melspectrogram_Hash"], self.mixedSong["melspectrogram_Hash"])
            self.mfcc = difference(songHashes["mfcc_Hash"], self.mixedSong["mfcc_Hash"])
            self.chroma = difference(songHashes["chroma_stft_Hash"], self.mixedSong["chroma_stft_Hash"])
            
            self.featureDiff = self.melspectroDiff + self.mfcc + self.chroma

            self.avg = (self.spectroDiff + self.featureDiff)/4
            self.results.append((songName, (abs(1 - mapRanges(self.avg, 0, 255, 0, 1)))*100))

        self.results.sort(key= lambda x: x[1], reverse=True)

        logger.debug("staring comparisons ... ")
        self.statusbar.showMessage("Loading results .. ")

        self.fill_table()
    
    def fill_table(self):
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(self.results))

        for row in range(len(self.results)):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(self.results[row][0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(round(self.results[row][1], 2))+"%"))
            self.tableWidget.item(row, 0).setBackground(QtGui.QColor(57, 65, 67))
            self.tableWidget.item(row, 1).setBackground(QtGui.QColor(57, 65, 67))
            self.tableWidget.verticalHeader().setSectionResizeMode(row, QtWidgets.QHeaderView.Stretch)

        self.tableWidget.setHorizontalHeaderLabels(["Found Matches", "Percentage"])

        for col in range(2):
            self.tableWidget.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)
            self.tableWidget.horizontalHeaderItem(col).setBackground(QtGui.QColor(57, 65, 67))

        # self.tableWidget.show()

        self.results.clear()
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
       main()