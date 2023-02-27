#!/usr/bin/env python3
# @author      Markus Kösters
import pickle
import time
import tkinter

import cv2
from Network.SocketController import SocketController
from Configurations.ConfigReader import ConfigReader
from PIL import Image, ImageTk


class MainGUI:

    def __init__(self):
        root = tkinter.Tk()
        self.__conf = ConfigReader()
        self.videoSleep = 1 / float(self.__conf.readConfigParameter('VideoFPS'))
        self.socketController = SocketController()
        self.socketController.connectToServer('video')
        self.imageLabel = tkinter.Label(root)
        self.imageLabel.pack()
        self.__getVideoStream()
        root.mainloop()

    def __getVideoStream(self):
        while True:
            print('Running Video GUI')
            rawFrame = pickle.loads(self.socketController.receiveMessage('video'))
            rgbFrame = cv2.cvtColor(rawFrame, cv2.COLOR_BGR2RGB)
            videoImage = Image.fromarray(rgbFrame)
            tkVideoImage = ImageTk.PhotoImage(image=videoImage)
            self.imageLabel.configure(image=tkVideoImage)
            # self.label.setPixmap(QtGui.QPixmap.fromImage(qtFrame))
            time.sleep(self.videoSleep)

if __name__ == '__main__':
    pass

