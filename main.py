
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from pymodbus.client.sync import ModbusTcpClient
import client
import socket, time, datetime, threading, os, sys, io
import numpy as np
from PIL import Image

ABR_IMAGE_HEADER_SIZE = 8
SERVER_PORT = 51236

form_class = uic.loadUiType("test.ui")[0]
class myWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.c = client.ClientSocket(self)
        self.c2 = client.ClientSocket(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.connectClicked)
        self.pushButton_2.clicked.connect(self.imageRecvClicked)

    def __del__(self):
        self.c.stop()

    def connectClicked(self):
        if self.c.bConnect == False:
            ip = self.lineEdit.text()
            port = self.lineEdit_2.text()

            folderDir = './Datalog'
            makeDirectory(folderDir)

            if self.c.connectServer(ip, int(port)):
                self.pushButton.setText('접속 종료')
                self.label_13.setText('')
                self.label_4.setText('Connected')
            else:
                self.c.stop()
                self.pushButton.setText('접속')
                self.label_4.setText('Disconnected')
        else:
            try:
                self.c.stop()
            except:
                print("error occur")
            finally:
                self.pushButton.setText('접속')
                self.label_4.setText('Disconnected')


    def imageRecvClicked(self):
        if self.c2.bConnect == False:
            ip = self.lineEdit.text()
            port = self.lineEdit_3.text()

            folderDir = './Imagelog'
            makeDirectory(folderDir)

            if self.c2.connectServer(ip, int(port)):
                self.pushButton_2.setText('접속 종료')
                self.label_11.setText('Connected')
            else:
                self.c2.stop()
                self.pushButton_2.setText('접속')
                self.label_11.setText('Disconnected')
        else:
            try:
                self.c2.stop()
            except:
                print("error occur")
            finally:
                self.pushButton_2.setText('접속')
                self.label_11.setText('Disconnected')

    def updateMsg(self, msg):
        self.label_13.setText(msg[1:-1])

        dataLogging('./Datalog', msg[1:])

    def updateImg(self, inspectionTime):
        print(inspectionTime)
        myWindow.label_7.setText(inspectionTime)

    def updateImgDir(self, imageSaveDir):
        pixmap = QPixmap(imageSaveDir)
        pixmap_re = pixmap.scaled(340, 250, QtCore.Qt.KeepAspectRatio)
        myWindow.label_8.setPixmap(pixmap_re)

    def updateDisconnect(self):
        self.pushButton.setText('접속')

    def closeEvent(self, e):
        self.c.stop()

def makeDirectory(folderDir):
    if not os.path.isdir(folderDir):
        os.mkdir(folderDir)

def imageOpenAndLogging(folderDir, recvBuffer):
    image = Image.open(io.BytesIO(recvBuffer[IVU_IMAGE_HEADER_SIZE:]))
    now = datetime.datetime.now()
    imageSaveDir = folderDir + '/' + str(now.strftime("%H-%M-%S")) +'.jpg'
    inspectionTime = now.strftime('%Y-%m-%d %H:%M:%S')
    image.save(imageSaveDir)
    image.close()
    return imageSaveDir, inspectionTime

def dataLogging(folderDir, register_buffer):
    logging_file_name = folderDir + '/' + str(datetime.datetime.today().strftime("%Y%m%d")) +'.txt'
    f = open(logging_file_name, mode='a', encoding='utf-8')
    str_read_list = str(register_buffer)[1:-1]
    now = datetime.datetime.now()
    cur_time = datetime.time(now.hour, now.minute, now.second)
    RF_logging = str(cur_time) + ', ' + str_read_list +'\n'
    f.write(RF_logging)
    f.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = myWindow()
    myWindow.show()
    sys.exit(app.exec_())
    # app.exec_()

    # run()
