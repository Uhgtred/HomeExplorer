# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'MainGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import pickle
import cv2
import sys

from Network.SocketController import SocketController
from Controller.Controller import Controller
from Configurations.ConfigReader import ConfigReader


class MainGUI(QDialog):

    def __init__(self):
        self.timer = QTimer()
        self.socketController = SocketController()
        self.socketController.connectToServer('video')
        super(MainGUI, self).__init__()
        self.mainPrograms = MainPrograms()
        self.image = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(640, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.imgFrame = QtWidgets.QFrame(self.centralwidget)
        self.imgFrame.setEnabled(True)
        self.imgLabel = QtWidgets.QLabel(self.centralwidget)
        self.imgLabel.setEnabled(True)
        self.imgLabel.setGeometry(QtCore.QRect(0, 0, 640, 480))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imgLabel.sizePolicy().hasHeightForWidth())
        self.imgLabel.setSizePolicy(sizePolicy)
        self.imgLabel.setText("")
        self.imgLabel.setPixmap(QtGui.QPixmap("../Bilder/15057_norway_fyord.jpg"))
        # self.imgLabel.setScaledContents(True)
        self.imgLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imgLabel.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def startGUI(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = MainGUI()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def start2ndVideo(self):
        while True:
            img = pickle.loads(self.socketController.receiveMessage('video'))
            self.imgFrame = cv2.imshow('Vision', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # time.sleep(0.01)

    @pyqtSlot()
    def startVideo(self):
        self.timer.timeout.connect(self.displayImage)  # Connect timeout to the output function
        self.timer.start(40)  # emit the timeout() signal at x=40ms

    def displayImage(self):
        image = pickle.loads(self.socketController.receiveMessage('video'))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (640, 480))
        # qformat = QImage.Format_Indexed8
        # if len(image.shape) == 3:
        #     if image.shape[2] == 4:
        #         qformat = QImage.Format_RGBA8888
        #     else:
        #         qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)#, qformat)
        # outImage = outImage.rgbSwapped()
        self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
        # self.imgLabel.setScaledContents(True)

class MainPrograms:

    def __init__(self):
        """Starting the Remote-Program and configuring everything"""
        self.__conf = ConfigReader()
        self.__delay = float(self.__conf.readConfigParameter('DelayMain'))
        self.socketController = SocketController()
        self.__cont = Controller()
        self.__controller = self.__cont.initController()
        self.__threads()

    def readController(self):
        while True:
            self.socketController.sendMessage(self.__cont.getControllerValues, 'controller')
            time.sleep(self.__delay)

    def __threads(self):
        """Any Thread that has to run goes in here!"""
        pass
        # __controllerThread = threading.Thread(target=self.__readController, name='ControllerThread', daemon=True)
        # __controllerThread.start()

        # self.socketController.connectToServer('controller')
        # __controllerReadThread = threading.Thread(target=lambda: self.__cont.readController(self.__controller), name='ControllerReadThread', daemon=True)
        # __controllerReadThread.start()

        # __cameraStreamThread = threading.Thread(target=self.mainGUI.startGUI, name='CameraStreamThread', daemon=True)
        # __cameraStreamThread.start()

        # __controllerThread.join()
        # __controllerReadThread.join()
        # __cameraStreamThread.join()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainGUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # ui.startVideo()
    ui.start2ndVideo()
    sys.exit(app.exec_())
