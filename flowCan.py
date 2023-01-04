import pyqtgraph as pg
import struct
import sys
import time
import array
import csv
import ui_flowmain
import ui_flowconfig
import ui_flowdiagram
from ui_flowmain import Ui_UI_Main
from ui_flowconfig import Ui_UI_config
from ui_flowdiagram import Ui_UI_diagram

from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtCore import QDate
from pyqtgraph import PlotWidget

import rwQueue
import transceiver
import function

import mainWindow
import configWindow
import diagramWindow
import tpdoWindow
import rpdoWindow
import nodeidWindow
    

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    
    #句柄
    comTransceiver = transceiver.Transceiver() 
    function = function.Function()  
    myDiagram = diagramWindow.diagramWindow()  
    myTpdo = tpdoWindow.tpdoWindow(comTransceiver,function)
    myRpdo = rpdoWindow.rpdoWindow(comTransceiver,function)  
    myNodeid = nodeidWindow.nodeidWindow()    
    myMain = mainWindow.MyMainWindow(comTransceiver,function,myTpdo,myRpdo,myNodeid)
    myConfig = configWindow.configWindow(comTransceiver,function,myMain) 
    
    myDiagram.setMainWindow(myMain)
    comTransceiver.setMainWindow(myMain)
    comTransceiver.setConfigWindow(myConfig)
    myTpdo.setMainWindow(myMain)
    myRpdo.setMainWindow(myMain)
    myNodeid.setMainWindow(myMain)

    myMain.pushButton_flow_config.clicked.connect(myConfig.show)
    myMain.pushButton_diagram_config.clicked.connect(myDiagram.show)
    myMain.pushButton_comm_tpdoConfig.clicked.connect(myTpdo.show)
    myMain.pushButton_comm_rpdoConfig.clicked.connect(myRpdo.show)
    myMain.pushButton_otherNodeid.clicked.connect(myNodeid.show)

    myMain.show()
    sys.exit(app.exec_())




