import pyqtgraph as pg
import struct
#import function
import sys
import time
import array
import ui_flowtpdo
from ui_flowtpdo import Ui_TPDO

from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray, QTimer, QDate, Qt
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QAbstractItemView,
    QHeaderView,
    QTableWidgetItem,
    QWidget,
    QMessageBox,
)
from pyqtgraph import PlotWidget
from PyQt5.QtGui import QFont, QColor, QBrush, QPixmap
import globalConstants as gc


class tpdoWindow(QWidget, Ui_TPDO):
    def __init__(self,comTransceiver,function):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("TPDO Config")
        self.comTransceiver = comTransceiver
        self.function   = function
        self.mainWindow = None
        # index, list= index+len,transType,inhibitTime,eventTimer,syncStartValue

        # 几个数据,数据1,数据2,数据3,数据4,transType,inhibitTime,evenTimer,syncStartValue
        self.tpdo1ParaList = ["0", "0", "0", "0", "0", "FF", "0", "0", "0"]
        self.tpdo2ParaList = ["0", "0", "0", "0", "0", "FF", "0", "0", "0"]
        self.tpdo3ParaList = ["0", "0", "0", "0", "0", "FF", "0", "0", "0"]
        self.tpdo4ParaList = ["0", "0", "0", "0", "0", "FF", "0", "0", "0"]
        self.syncWithData = False
        self.cobid_Servo_TPDO1   = ''  
        self.cobid_Servo_TPDO2   = ''  
        self.cobid_Servo_TPDO3   = ''  
        self.cobid_Servo_TPDO4   = ''  
        self.cobid_TSDO    = ''  
        self.CreateSignalSlot()
        pass
    def setMainWindow(self,mainWindow):
        self.mainWindow = mainWindow
        pass
    # 设置信号与槽
    def CreateSignalSlot(self):
        self.comboBox_tpdo_pdo1_data1.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo1_data2.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo1_data3.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo1_data4.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo1_transmissionType.addItems(gc.listOfTpdoTransmissionType)
        self.comboBox_tpdo_pdo1_syncStartValue.addItems(gc.listOfTpdoSyncStartValue)
        self.comboBox_tpdo_pdo2_data1.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo2_data2.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo2_data3.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo2_data4.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo2_transmissionType.addItems(gc.listOfTpdoTransmissionType)
        self.comboBox_tpdo_pdo2_syncStartValue.addItems(gc.listOfTpdoSyncStartValue)
        self.comboBox_tpdo_pdo3_data1.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo3_data2.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo3_data3.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo3_data4.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo3_transmissionType.addItems(gc.listOfTpdoTransmissionType)
        self.comboBox_tpdo_pdo3_syncStartValue.addItems(gc.listOfTpdoSyncStartValue)
        self.comboBox_tpdo_pdo4_data1.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo4_data2.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo4_data3.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo4_data4.addItems(gc.tpdoAvailableList)
        self.comboBox_tpdo_pdo4_transmissionType.addItems(gc.listOfTpdoTransmissionType)
        self.comboBox_tpdo_pdo4_syncStartValue.addItems(gc.listOfTpdoSyncStartValue)
        self.setDefault()
        # 按钮的默认状态
        self.pushButton_tpdo_clear.clicked.connect(self.pushButton_tpdo_clear_clicked)
        self.pushButton_tpdo_update.clicked.connect(self.pushButton_tpdo_update_clicked)
        self.comboBox_tpdo_pdo1_data1.currentIndexChanged.connect(self.comboBox_tpdo_pdo1_data1_currentIndexChanged)
        self.comboBox_tpdo_pdo1_data2.currentIndexChanged.connect(self.comboBox_tpdo_pdo1_data2_currentIndexChanged)
        self.comboBox_tpdo_pdo1_data3.currentIndexChanged.connect(self.comboBox_tpdo_pdo1_data3_currentIndexChanged)

        self.comboBox_tpdo_pdo2_data1.currentIndexChanged.connect(self.comboBox_tpdo_pdo2_data1_currentIndexChanged)
        self.comboBox_tpdo_pdo2_data2.currentIndexChanged.connect(self.comboBox_tpdo_pdo2_data2_currentIndexChanged)
        self.comboBox_tpdo_pdo2_data3.currentIndexChanged.connect(self.comboBox_tpdo_pdo2_data3_currentIndexChanged)

        self.comboBox_tpdo_pdo3_data1.currentIndexChanged.connect(self.comboBox_tpdo_pdo3_data1_currentIndexChanged)
        self.comboBox_tpdo_pdo3_data2.currentIndexChanged.connect(self.comboBox_tpdo_pdo3_data2_currentIndexChanged)
        self.comboBox_tpdo_pdo3_data3.currentIndexChanged.connect(self.comboBox_tpdo_pdo3_data3_currentIndexChanged)

        self.comboBox_tpdo_pdo4_data1.currentIndexChanged.connect(self.comboBox_tpdo_pdo4_data1_currentIndexChanged)
        self.comboBox_tpdo_pdo4_data2.currentIndexChanged.connect(self.comboBox_tpdo_pdo4_data2_currentIndexChanged)
        self.comboBox_tpdo_pdo4_data3.currentIndexChanged.connect(self.comboBox_tpdo_pdo4_data3_currentIndexChanged)
        pass

    def setDefault(self):
        # TPDO1的默认状态
        self.comboBox_tpdo_pdo1_data1.setCurrentIndex(0)
        self.comboBox_tpdo_pdo1_data2.setCurrentIndex(0)
        self.comboBox_tpdo_pdo1_data3.setCurrentIndex(0)
        self.comboBox_tpdo_pdo1_data4.setCurrentIndex(0)
        self.comboBox_tpdo_pdo1_transmissionType.setCurrentIndex(self.comboBox_tpdo_pdo1_transmissionType.count() - 1)
        self.comboBox_tpdo_pdo1_syncStartValue.setCurrentIndex(0)
        self.lineEdit_tpdo_pdo1_eventTimer.setText("0")
        self.lineEdit_tpdo_pdo1_inhibitTime.setText("0")
        self.comboBox_tpdo_pdo1_data2.setEnabled(False)
        self.comboBox_tpdo_pdo1_data3.setEnabled(False)
        self.comboBox_tpdo_pdo1_data4.setEnabled(False)
        # TPDO2的默认状态
        self.comboBox_tpdo_pdo2_data1.setCurrentIndex(0)
        self.comboBox_tpdo_pdo2_data2.setCurrentIndex(0)
        self.comboBox_tpdo_pdo2_data3.setCurrentIndex(0)
        self.comboBox_tpdo_pdo2_data4.setCurrentIndex(0)
        self.comboBox_tpdo_pdo2_transmissionType.setCurrentIndex(self.comboBox_tpdo_pdo2_transmissionType.count() - 1)
        self.comboBox_tpdo_pdo2_syncStartValue.setCurrentIndex(0)
        self.lineEdit_tpdo_pdo2_eventTimer.setText("0")
        self.lineEdit_tpdo_pdo2_inhibitTime.setText("0")
        self.comboBox_tpdo_pdo2_data2.setEnabled(False)
        self.comboBox_tpdo_pdo2_data3.setEnabled(False)
        self.comboBox_tpdo_pdo2_data4.setEnabled(False)
        # TPDO3的默认状态
        self.comboBox_tpdo_pdo3_data1.setCurrentIndex(0)
        self.comboBox_tpdo_pdo3_data2.setCurrentIndex(0)
        self.comboBox_tpdo_pdo3_data3.setCurrentIndex(0)
        self.comboBox_tpdo_pdo3_data4.setCurrentIndex(0)
        self.comboBox_tpdo_pdo3_transmissionType.setCurrentIndex(self.comboBox_tpdo_pdo3_transmissionType.count() - 1)
        self.comboBox_tpdo_pdo3_syncStartValue.setCurrentIndex(0)
        self.lineEdit_tpdo_pdo3_eventTimer.setText("0")
        self.lineEdit_tpdo_pdo3_inhibitTime.setText("0")
        self.comboBox_tpdo_pdo3_data2.setEnabled(False)
        self.comboBox_tpdo_pdo3_data3.setEnabled(False)
        self.comboBox_tpdo_pdo3_data4.setEnabled(False)
        # TPDO4的默认状态
        self.comboBox_tpdo_pdo4_data1.setCurrentIndex(0)
        self.comboBox_tpdo_pdo4_data2.setCurrentIndex(0)
        self.comboBox_tpdo_pdo4_data3.setCurrentIndex(0)
        self.comboBox_tpdo_pdo4_data4.setCurrentIndex(0)
        self.comboBox_tpdo_pdo4_transmissionType.setCurrentIndex(self.comboBox_tpdo_pdo4_transmissionType.count() - 1)
        self.comboBox_tpdo_pdo4_syncStartValue.setCurrentIndex(0)
        self.lineEdit_tpdo_pdo4_eventTimer.setText("0")
        self.lineEdit_tpdo_pdo4_inhibitTime.setText("0")
        self.comboBox_tpdo_pdo4_data2.setEnabled(False)
        self.comboBox_tpdo_pdo4_data3.setEnabled(False)
        self.comboBox_tpdo_pdo4_data4.setEnabled(False)

        self.tpdo1ParaList = ["0", "0", "0", "0", "0", "FF", "0", "0", "0"]
        self.tpdo2ParaList = ["0", "0", "0", "0", "0", "FF", "0", "0", "0"]
        self.tpdo3ParaList = ["0", "0", "0", "0", "0", "FF", "0", "0", "0"]
        self.tpdo4ParaList = ["0", "0", "0", "0", "0", "FF", "0", "0", "0"]
        self.syncWithData = False
        pass

    def pushButton_tpdo_clear_clicked(self):
        self.setDefault()
        pass

    def pushButton_tpdo_update_clicked(self):
        tpdoStatusOk = True
        pdo1Continue = True
        pdo2Continue = True
        pdo3Continue = True
        pdo4Continue = True
        tpdo1DataNum = 0
        tpdo2DataNum = 0
        tpdo3DataNum = 0
        tpdo4DataNum = 0
        tpdo1Len = 0
        tpdo2Len = 0
        tpdo3Len = 0
        tpdo4Len = 0
        # tpdo1
        if pdo1Continue:
            if self.comboBox_tpdo_pdo1_data1.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo1_data1.currentText())
                tpdo1DataNum += int(tempObject[1], 10)
                self.tpdo1ParaList[0] = "1"
                self.tpdo1ParaList[1] = tempObject[0]
                pass
            else:
                self.tpdo1ParaList[0] = "0"
                pdo1Continue = False
                pass
        if pdo1Continue:
            if self.comboBox_tpdo_pdo1_data2.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo1_data2.currentText())
                tpdo1DataNum += int(tempObject[1], 10)
                self.tpdo1ParaList[0] = "2"
                self.tpdo1ParaList[2] = tempObject[0]
                pass
            else:
                pdo1Continue = False
        if pdo1Continue:
            if self.comboBox_tpdo_pdo1_data3.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo1_data3.currentText())
                tpdo1DataNum += int(tempObject[1], 10)
                self.tpdo1ParaList[0] = "3"
                self.tpdo1ParaList[3] = tempObject[0]
                pass
            else:
                pdo1Continue = False
        if pdo1Continue:        
            if self.comboBox_tpdo_pdo1_data4.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo1_data4.currentText())
                tpdo1DataNum += int(tempObject[1], 10)
                self.tpdo1ParaList[0] = "4"
                self.tpdo1ParaList[4] = tempObject[0]
            else:
                pdo1Continue = False
        # transmission type
        self.tpdo1ParaList[5] = str(hex(int(self.comboBox_tpdo_pdo1_transmissionType.currentText(), 10)).replace("0x", "").zfill(2).upper())
        # inhibit time
        inhibitTime = self.lineEdit_tpdo_pdo1_inhibitTime.text()
        if inhibitTime.isdecimal():
            self.tpdo1ParaList[6] = str(hex(int(self.lineEdit_tpdo_pdo1_inhibitTime.text(), 10)).replace("0x", "").zfill(4).upper())
        else:
            self.tpdo1ParaList[6] = "0"
            QMessageBox.warning(self, "Error", " tpdo1 inhibitTime, Wrong Input")
        # eventTimer
        eventTimer = self.lineEdit_tpdo_pdo1_eventTimer.text()
        if eventTimer.isdecimal():
            self.tpdo1ParaList[7] = str(hex(int(self.lineEdit_tpdo_pdo1_eventTimer.text(), 10)).replace("0x", "").zfill(4).upper())
        else:
            self.tpdo1ParaList[7] = "0"
            QMessageBox.warning(self, "Error", "tpdo1 eventTimer, Wrong Input")
        # syncstartvalue
        self.tpdo1ParaList[8] = str(hex(int(self.comboBox_tpdo_pdo1_syncStartValue.currentText(), 10)).replace("0x", "").zfill(2).upper())
        if self.tpdo1ParaList[8] != '00':
            self.syncWithData = True
        # 检查本TPDO是否合理,主要是长度不要超过8个byte.
        if tpdo1DataNum > 8:
            QMessageBox.warning(self, "Error", "too much data for TPDO1.")
            self.tpdo1ParaList[0] = "0"
            tpdoStatusOk = False
        # tpdo2
        if pdo2Continue:
            if self.comboBox_tpdo_pdo2_data1.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo2_data1.currentText())
                tpdo2DataNum += int(tempObject[1], 10)
                self.tpdo2ParaList[0] = "1"
                self.tpdo2ParaList[1] = tempObject[0]
                pass
            else:
                self.tpdo2ParaList[0] = "0"
                pdo2Continue = False
                pass
        if pdo2Continue:
            if self.comboBox_tpdo_pdo2_data2.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo2_data2.currentText())
                tpdo2DataNum += int(tempObject[1], 10)
                self.tpdo2ParaList[0] = "2"
                self.tpdo2ParaList[2] = tempObject[0]
                pass
            else:
                pdo2Continue = False
        if pdo2Continue:
            if self.comboBox_tpdo_pdo2_data3.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo2_data3.currentText())
                tpdo2DataNum += int(tempObject[1], 10)
                self.tpdo2ParaList[0] = "3"
                self.tpdo2ParaList[3] = tempObject[0]
                pass
            else:
                pdo2Continue = False
        if pdo2Continue:
            if self.comboBox_tpdo_pdo2_data4.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo2_data4.currentText())
                tpdo2DataNum += int(tempObject[1], 10)
                self.tpdo2ParaList[0] = "4"
                self.tpdo2ParaList[4] = tempObject[0]
            else:
                pdo2Continue = False
        # transmission type
        self.tpdo2ParaList[5] = str(hex(int(self.comboBox_tpdo_pdo2_transmissionType.currentText(), 10)).replace("0x", "").zfill(2).upper())
        # inhibit time
        inhibitTime = self.lineEdit_tpdo_pdo2_inhibitTime.text()
        if inhibitTime.isdecimal():
            self.tpdo2ParaList[6] = str(hex(int(self.lineEdit_tpdo_pdo2_inhibitTime.text(), 10)).replace("0x", "").zfill(4).upper())
        else:
            self.tpdo2ParaList[6] = "0"
            QMessageBox.warning(self, "Error", "tpdo1 inhibitTime, Wrong Input")
        # eventTimer
        eventTimer = self.lineEdit_tpdo_pdo2_eventTimer.text()
        if eventTimer.isdecimal():
            self.tpdo2ParaList[7] = str(hex(int(self.lineEdit_tpdo_pdo2_eventTimer.text(), 10)).replace("0x", "").zfill(4).upper())
        else:
            self.tpdo2ParaList[7] = "0"
            QMessageBox.warning(self, "Error", "tpdo1 eventTimer, Wrong Input")
        # syncstartvalue
        self.tpdo2ParaList[8] = str(hex(int(self.comboBox_tpdo_pdo2_syncStartValue.currentText(), 10)).replace("0x", "").zfill(2).upper())
        if self.tpdo2ParaList[8] != '00':
            self.syncWithData = True
        # 检查本TPDO是否合理,主要是长度不要超过8个byte.
        if tpdo2DataNum > 8:
            QMessageBox.warning(self, "Error", "too much data for TPDO2.")
            self.tpdo2ParaList[0] = "0"
            tpdoStatusOk = False
        # tpdo3
        if pdo3Continue:
            if self.comboBox_tpdo_pdo3_data1.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo3_data1.currentText())
                tpdo3DataNum += int(tempObject[1], 10)
                self.tpdo3ParaList[0] = "1"
                self.tpdo3ParaList[1] = tempObject[0]
                pass
            else:
                self.tpdo3ParaList[0] = "0"
                pdo3Continue = False
                pass
        if pdo3Continue:
            if self.comboBox_tpdo_pdo3_data2.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo3_data2.currentText())
                tpdo3DataNum += int(tempObject[1], 10)
                self.tpdo3ParaList[0] = "2"
                self.tpdo3ParaList[2] = tempObject[0]
                pass
            else:
                pdo3Continue = False
        if pdo3Continue:
            if self.comboBox_tpdo_pdo3_data3.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo3_data3.currentText())
                tpdo3DataNum += int(tempObject[1], 10)
                self.tpdo3ParaList[0] = "3"
                self.tpdo3ParaList[3] = tempObject[0]
                pass
            else:
                pdo3Continue = False
        if pdo3Continue:
            if self.comboBox_tpdo_pdo3_data4.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo3_data4.currentText())
                tpdo3DataNum += int(tempObject[1], 10)
                self.tpdo3ParaList[0] = "4"
                self.tpdo3ParaList[4] = tempObject[0]
            else:
                pdo3Continue = False
        # transmission type
        self.tpdo3ParaList[5] = str(hex(int(self.comboBox_tpdo_pdo3_transmissionType.currentText(), 10)).replace("0x", "").zfill(2).upper())
        # inhibit time
        inhibitTime = self.lineEdit_tpdo_pdo3_inhibitTime.text()
        if inhibitTime.isdecimal():
            self.tpdo3ParaList[6] = str(hex(int(self.lineEdit_tpdo_pdo3_inhibitTime.text(), 10)).replace("0x", "").zfill(4).upper())
        else:
            self.tpdo3ParaList[6] = "0"
            QMessageBox.warning(self, "Error", "tpdo1 inhibitTime, Wrong Input")
        # eventTimer
        eventTimer = self.lineEdit_tpdo_pdo3_eventTimer.text()
        if eventTimer.isdecimal():
            self.tpdo3ParaList[7] = str(hex(int(self.lineEdit_tpdo_pdo3_eventTimer.text(), 10)).replace("0x", "").zfill(4).upper())
        else:
            self.tpdo3ParaList[7] = "0"
            QMessageBox.warning(self, "Error", "tpdo1 eventTimer, Wrong Input")
        # syncstartvalue
        self.tpdo3ParaList[8] = str(hex(int(self.comboBox_tpdo_pdo3_syncStartValue.currentText(), 10)).replace("0x", "").zfill(2).upper())
        if self.tpdo3ParaList[8] != '00':
            self.syncWithData = True
        # 检查本TPDO是否合理,主要是长度不要超过8个byte.
        if tpdo3DataNum > 8:
            QMessageBox.warning(self, "Error", "too much data for TPDO3.")
            self.tpdo3ParaList[0] = "0"
            tpdoStatusOk = False
        # tpdo4
        if pdo4Continue:
            if self.comboBox_tpdo_pdo4_data1.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo4_data1.currentText())
                tpdo4DataNum += int(tempObject[1], 10)
                self.tpdo4ParaList[0] = "1"
                self.tpdo4ParaList[1] = tempObject[0]
                pass
            else:
                self.tpdo4ParaList[0] = "0"
                pdo4Continue = False
                pass
        if pdo4Continue:
            if self.comboBox_tpdo_pdo4_data2.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo4_data2.currentText())
                tpdo4DataNum += int(tempObject[1], 10)
                self.tpdo4ParaList[0] = "2"
                self.tpdo4ParaList[2] = tempObject[0]
                pass
            else:
                pdo4Continue = False
                pass
        if pdo4Continue:
            if self.comboBox_tpdo_pdo4_data3.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo4_data3.currentText())
                tpdo4DataNum += int(tempObject[1], 10)
                self.tpdo4ParaList[0] = "3"
                self.tpdo4ParaList[3] = tempObject[0]
                pass
            else:
                pdo4Continue = False
        if pdo4Continue:
            if self.comboBox_tpdo_pdo4_data4.currentText() != "none":
                tempObject = gc.ojbectDict.get(self.comboBox_tpdo_pdo4_data4.currentText())
                tpdo4DataNum += int(tempObject[1], 10)
                self.tpdo4ParaList[0] = "4"
                self.tpdo4ParaList[4] = tempObject[0]
            else:
                pdo4Continue = False
        # transmission type
        self.tpdo4ParaList[5] = str(hex(int(self.comboBox_tpdo_pdo4_transmissionType.currentText(), 10)).replace("0x", "").zfill(2).upper())
        # inhibit time
        inhibitTime = self.lineEdit_tpdo_pdo4_inhibitTime.text()
        if inhibitTime.isdecimal():
            self.tpdo4ParaList[6] = str(hex(int(self.lineEdit_tpdo_pdo4_inhibitTime.text(), 10)).replace("0x", "").zfill(4).upper())
        else:
            self.tpdo4ParaList[6] = "0"
            QMessageBox.warning(self, "Error", "tpdo1 inhibitTime, Wrong Input")
        # eventTimer
        eventTimer = self.lineEdit_tpdo_pdo4_eventTimer.text()
        if eventTimer.isdecimal():
            self.tpdo4ParaList[7] = str(hex(int(self.lineEdit_tpdo_pdo4_eventTimer.text(), 10)).replace("0x", "").zfill(4).upper())
        else:
            self.tpdo4ParaList[7] = "0"
            QMessageBox.warning(self, "Error", "tpdo1 eventTimer, Wrong Input")
        # syncstartvalue
        self.tpdo4ParaList[8] = str(hex(int(self.comboBox_tpdo_pdo4_syncStartValue.currentText(), 10)).replace("0x", "").zfill(2).upper())
        if self.tpdo4ParaList[8] != '00':
            self.syncWithData = True
        # 检查本TPDO是否合理,主要是长度不要超过8个byte.
        if tpdo4DataNum > 8:
            QMessageBox.warning(self, "Error", "too much data for TPDO4.")
            self.tpdo4ParaList[0] = "0"
            tpdoStatusOk = False
        if tpdoStatusOk == True:
            decNodeid = self.mainWindow.getDecNodeid()
            self.configTpdo(decNodeid)
            self.close()
        #print("tpdo1ParaList=", self.tpdo1ParaList)
        #print("tpdo2ParaList=", self.tpdo2ParaList)
        #print("tpdo3ParaList=", self.tpdo3ParaList)
        #print("tpdo4ParaList=", self.tpdo4ParaList)
        pass
    def getSyncWithDataStatus(self):
        return self.syncWithData
        pass
    def comboBox_tpdo_pdo1_data1_currentIndexChanged(self):
        if self.comboBox_tpdo_pdo1_data1.currentText() != "none":
            self.comboBox_tpdo_pdo1_data2.setEnabled(True)
        else:
            self.comboBox_tpdo_pdo1_data2.setCurrentIndex(0) 
            self.comboBox_tpdo_pdo1_data3.setCurrentIndex(0)  
            self.comboBox_tpdo_pdo1_data4.setCurrentIndex(0)
            self.comboBox_tpdo_pdo1_data2.setEnabled(False)
            self.comboBox_tpdo_pdo1_data3.setEnabled(False)
            self.comboBox_tpdo_pdo1_data4.setEnabled(False)
        pass

    def comboBox_tpdo_pdo1_data2_currentIndexChanged(self):
        if self.comboBox_tpdo_pdo1_data2.currentText() != "none":
            self.comboBox_tpdo_pdo1_data3.setEnabled(True)
        else:
            self.comboBox_tpdo_pdo1_data3.setCurrentIndex(0)  
            self.comboBox_tpdo_pdo1_data4.setCurrentIndex(0)
            self.comboBox_tpdo_pdo1_data3.setEnabled(False)
            self.comboBox_tpdo_pdo1_data4.setEnabled(False)
        pass

    def comboBox_tpdo_pdo1_data3_currentIndexChanged(self):
        if self.comboBox_tpdo_pdo1_data3.currentText() != "none":
            self.comboBox_tpdo_pdo1_data4.setEnabled(True)
        else: 
            self.comboBox_tpdo_pdo1_data4.setCurrentIndex(0)
            self.comboBox_tpdo_pdo1_data4.setEnabled(False)
        pass

    def comboBox_tpdo_pdo2_data1_currentIndexChanged(self):
        if self.comboBox_tpdo_pdo2_data1.currentText() != "none":
            self.comboBox_tpdo_pdo2_data2.setEnabled(True)
        else:
            self.comboBox_tpdo_pdo2_data2.setCurrentIndex(0) 
            self.comboBox_tpdo_pdo2_data3.setCurrentIndex(0)  
            self.comboBox_tpdo_pdo2_data4.setCurrentIndex(0)
            self.comboBox_tpdo_pdo2_data2.setEnabled(False)
            self.comboBox_tpdo_pdo2_data3.setEnabled(False)
            self.comboBox_tpdo_pdo2_data4.setEnabled(False)
        pass

    def comboBox_tpdo_pdo2_data2_currentIndexChanged(self):
        if self.comboBox_tpdo_pdo2_data2.currentText() != "none":
            self.comboBox_tpdo_pdo2_data3.setEnabled(True)
        else:
            self.comboBox_tpdo_pdo2_data3.setCurrentIndex(0)  
            self.comboBox_tpdo_pdo2_data4.setCurrentIndex(0)
            self.comboBox_tpdo_pdo2_data3.setEnabled(False)
            self.comboBox_tpdo_pdo2_data4.setEnabled(False)
        pass

    def comboBox_tpdo_pdo2_data3_currentIndexChanged(self):
        if self.comboBox_tpdo_pdo2_data3.currentText() != "none":
            self.comboBox_tpdo_pdo2_data4.setEnabled(True)
        else: 
            self.comboBox_tpdo_pdo2_data4.setCurrentIndex(0)
            self.comboBox_tpdo_pdo2_data4.setEnabled(False)
        pass

    def comboBox_tpdo_pdo3_data1_currentIndexChanged(self):
        if self.comboBox_tpdo_pdo3_data1.currentText() != "none":
            self.comboBox_tpdo_pdo3_data2.setEnabled(True)
        else:
            self.comboBox_tpdo_pdo3_data2.setCurrentIndex(0) 
            self.comboBox_tpdo_pdo3_data3.setCurrentIndex(0)  
            self.comboBox_tpdo_pdo3_data4.setCurrentIndex(0)
            self.comboBox_tpdo_pdo3_data2.setEnabled(False)
            self.comboBox_tpdo_pdo3_data3.setEnabled(False)
            self.comboBox_tpdo_pdo3_data4.setEnabled(False)
        pass

    def comboBox_tpdo_pdo3_data2_currentIndexChanged(self):
        if self.comboBox_tpdo_pdo3_data2.currentText() != "none":
            self.comboBox_tpdo_pdo3_data3.setEnabled(True)
        else:
            self.comboBox_tpdo_pdo3_data3.setCurrentIndex(0)  
            self.comboBox_tpdo_pdo3_data4.setCurrentIndex(0)
            self.comboBox_tpdo_pdo3_data3.setEnabled(False)
            self.comboBox_tpdo_pdo3_data4.setEnabled(False)
        pass

    def comboBox_tpdo_pdo3_data3_currentIndexChanged(self):
        if self.comboBox_tpdo_pdo3_data3.currentText() != "none":
            self.comboBox_tpdo_pdo3_data4.setEnabled(True)
        else:
            self.comboBox_tpdo_pdo3_data4.setCurrentIndex(0)
            self.comboBox_tpdo_pdo3_data4.setEnabled(False)
        pass

    def comboBox_tpdo_pdo4_data1_currentIndexChanged(self):
        if self.comboBox_tpdo_pdo4_data1.currentText() != "none":
            self.comboBox_tpdo_pdo4_data2.setEnabled(True)
        else:
            self.comboBox_tpdo_pdo4_data2.setCurrentIndex(0) 
            self.comboBox_tpdo_pdo4_data3.setCurrentIndex(0)  
            self.comboBox_tpdo_pdo4_data4.setCurrentIndex(0)
            self.comboBox_tpdo_pdo4_data2.setEnabled(False)
            self.comboBox_tpdo_pdo4_data3.setEnabled(False)
            self.comboBox_tpdo_pdo4_data4.setEnabled(False)
        pass

    def comboBox_tpdo_pdo4_data2_currentIndexChanged(self):
        if self.comboBox_tpdo_pdo4_data2.currentText() != "none":
            self.comboBox_tpdo_pdo4_data3.setEnabled(True)
        else:
            self.comboBox_tpdo_pdo4_data3.setCurrentIndex(0)  
            self.comboBox_tpdo_pdo4_data4.setCurrentIndex(0)
            self.comboBox_tpdo_pdo4_data3.setEnabled(False)
            self.comboBox_tpdo_pdo4_data4.setEnabled(False)
        pass

    def comboBox_tpdo_pdo4_data3_currentIndexChanged(self):
        if self.comboBox_tpdo_pdo4_data3.currentText() != "none":
            self.comboBox_tpdo_pdo4_data4.setEnabled(True)
        else:
            self.comboBox_tpdo_pdo4_data4.setCurrentIndex(0)
            self.comboBox_tpdo_pdo4_data4.setEnabled(False)
        pass

    def configTpdo(self,decNodeid):
        cobid_TPDO1    = (str(hex(decNodeid+gc.cobid_TPDO1)).replace('0x','')).zfill(3).upper()
        cobid_TPDO2    = (str(hex(decNodeid+gc.cobid_TPDO2)).replace('0x','')).zfill(3).upper()
        cobid_TPDO3    = (str(hex(decNodeid+gc.cobid_TPDO3)).replace('0x','')).zfill(3).upper()
        cobid_TPDO4    = (str(hex(decNodeid+gc.cobid_TPDO4)).replace('0x','')).zfill(3).upper()
        cobid_TSDO     = (str(hex(decNodeid+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
        #print("tpdo1ParaList=", self.tpdo1ParaList)
        #print("tpdo2ParaList=", self.tpdo2ParaList)
        #print("tpdo3ParaList=", self.tpdo3ParaList)
        #print("tpdo4ParaList=", self.tpdo4ParaList)
        #tpdo1 
        tpdo1ParaList = self.tpdo1ParaList
        if tpdo1ParaList[0] != '0': 
            #disable pdo1
            #对方的TPDO就是flowcan的RPDO
            self.function.hexStrToHexBytes(str(hex(int(cobid_TPDO1,16)+0x80000000).replace('0x','')))   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1Cobid+self.function.getSdoDataStr()])  
            #clear tpdo1, 1A00:00,1byte
            self.function.hexStrToHexBytes('00')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1NumberOfMappedObjects+self.function.getSdoDataStr()])
            #transmission type
            self.function.hexStrToHexBytes(tpdo1ParaList[5])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1TransmissionType+self.function.getSdoDataStr()])  
            #inhibit time    
            self.function.hexStrToHexBytes(tpdo1ParaList[6])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1InhibitTime+self.function.getSdoDataStr()])  
            #event time
            self.function.hexStrToHexBytes(tpdo1ParaList[7])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1EventTimer+self.function.getSdoDataStr()])   
            #sync start value
            self.function.hexStrToHexBytes(tpdo1ParaList[8])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1SyncStartValue+self.function.getSdoDataStr()])   
            #data
            if tpdo1ParaList[0] == '4':
                self.function.hexStrToHexBytes(tpdo1ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(tpdo1ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(tpdo1ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1MappedObject3+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(tpdo1ParaList[4])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1MappedObject4+self.function.getSdoDataStr()])
            elif tpdo1ParaList[0] == '3': 
                self.function.hexStrToHexBytes(tpdo1ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(tpdo1ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(tpdo1ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1MappedObject3+self.function.getSdoDataStr()])  
            elif tpdo1ParaList[0] == '2': 
                self.function.hexStrToHexBytes(tpdo1ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(tpdo1ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1MappedObject2+self.function.getSdoDataStr()])
            elif tpdo1ParaList[0] == '1': 
                self.function.hexStrToHexBytes(tpdo1ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1MappedObject1+self.function.getSdoDataStr()])         
            #mapped object
            self.function.hexStrToHexBytes(str(tpdo1ParaList[0]))
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1NumberOfMappedObjects+self.function.getSdoDataStr()])   
        else:
            #如果没有配置,就需要将对应的mapped object改为0.
            #disable pdo1
            #self.function.hexStrToHexBytes(str(hex(int(cobid_TPDO1,16)+0x80000000).replace('0x','')))   
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1Cobid+self.function.getSdoDataStr()])  
            #self.function.hexStrToHexBytes(str(tpdo1ParaList[0]))
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1NumberOfMappedObjects+self.function.getSdoDataStr()]) 
            pass
        #tpdo2 
        tpdo2ParaList = self.tpdo2ParaList
        if tpdo2ParaList[0] != '0':    
            #disable pdo2
            self.function.hexStrToHexBytes(str(hex(int(cobid_TPDO2,16)+0x80000000).replace('0x','')))   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2Cobid+self.function.getSdoDataStr()])   
            #clear tpdo2, 1A01:00,1byte
            self.function.hexStrToHexBytes('00')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2NumberOfMappedObjects+self.function.getSdoDataStr()])
            #transmission type
            self.function.hexStrToHexBytes(tpdo2ParaList[5])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2TransmissionType+self.function.getSdoDataStr()])  
            #inhibit time    
            self.function.hexStrToHexBytes(tpdo2ParaList[6])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2InhibitTime+self.function.getSdoDataStr()])  
            #event time
            self.function.hexStrToHexBytes(tpdo2ParaList[7])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2EventTimer+self.function.getSdoDataStr()])     
            #sync start value
            self.function.hexStrToHexBytes(tpdo2ParaList[8])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2SyncStartValue+self.function.getSdoDataStr()])          
            #data
            if tpdo2ParaList[0] == '4':
                self.function.hexStrToHexBytes(tpdo2ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(tpdo2ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(tpdo2ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2MappedObject3+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(tpdo2ParaList[4])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2MappedObject4+self.function.getSdoDataStr()])
            elif tpdo2ParaList[0] == '3': 
                self.function.hexStrToHexBytes(tpdo2ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(tpdo2ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(tpdo2ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2MappedObject3+self.function.getSdoDataStr()])  
            elif tpdo2ParaList[0] == '2': 
                self.function.hexStrToHexBytes(tpdo2ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(tpdo2ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2MappedObject2+self.function.getSdoDataStr()])
            elif tpdo2ParaList[0] == '1': 
                self.function.hexStrToHexBytes(tpdo2ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2MappedObject1+self.function.getSdoDataStr()])           
            #mapped object
            self.function.hexStrToHexBytes(str(tpdo2ParaList[0]))
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2NumberOfMappedObjects+self.function.getSdoDataStr()])               
        else:
            #disable pdo2
            #self.function.hexStrToHexBytes(str(hex(int(cobid_TPDO2,16)+0x80000000).replace('0x','')))   
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2Cobid+self.function.getSdoDataStr()])   
            #self.function.hexStrToHexBytes(str(tpdo2ParaList[0]))
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2NumberOfMappedObjects+self.function.getSdoDataStr()])
            pass
        #tpdo3 
        tpdo3ParaList = self.tpdo3ParaList
        if tpdo3ParaList[0] != '0':    
            #disable pdo3 
            self.function.hexStrToHexBytes(str(hex(int(cobid_TPDO3,16)+0x80000000).replace('0x','')))   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3Cobid+self.function.getSdoDataStr()])  
            #clear tpdo3, 1A02:00,1byte
            self.function.hexStrToHexBytes('00')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3NumberOfMappedObjects+self.function.getSdoDataStr()])
            #transmission type
            self.function.hexStrToHexBytes(tpdo3ParaList[5])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3TransmissionType+self.function.getSdoDataStr()])  
            #inhibit time    
            self.function.hexStrToHexBytes(tpdo3ParaList[6])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3InhibitTime+self.function.getSdoDataStr()])  
            #event time
            self.function.hexStrToHexBytes(tpdo3ParaList[7])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3EventTimer+self.function.getSdoDataStr()])  
            #sync start value
            self.function.hexStrToHexBytes(tpdo3ParaList[8])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3SyncStartValue+self.function.getSdoDataStr()])   
            #data
            if tpdo3ParaList[0] == '4':
                self.function.hexStrToHexBytes(tpdo3ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(tpdo3ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(tpdo3ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3MappedObject3+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(tpdo3ParaList[4])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3MappedObject4+self.function.getSdoDataStr()])
            elif tpdo3ParaList[0] == '3': 
                self.function.hexStrToHexBytes(tpdo3ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(tpdo3ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(tpdo3ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3MappedObject3+self.function.getSdoDataStr()])  
            elif tpdo3ParaList[0] == '2': 
                self.function.hexStrToHexBytes(tpdo3ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(tpdo3ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3MappedObject2+self.function.getSdoDataStr()])
            elif tpdo3ParaList[0] == '1': 
                self.function.hexStrToHexBytes(tpdo3ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3MappedObject1+self.function.getSdoDataStr()])           
            #mapped object
            self.function.hexStrToHexBytes(str(tpdo3ParaList[0]))
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3NumberOfMappedObjects+self.function.getSdoDataStr()])     
        else:
            #disable pdo3 
            #self.function.hexStrToHexBytes(str(hex(int(cobid_TPDO3,16)+0x80000000).replace('0x','')))   
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3Cobid+self.function.getSdoDataStr()]) 
            #self.function.hexStrToHexBytes(str(tpdo3ParaList[0]))
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3NumberOfMappedObjects+self.function.getSdoDataStr()]) 
            pass
        #tpdo4
        tpdo4ParaList = self.tpdo4ParaList
        if tpdo4ParaList[0] != '0':    
            #disable pdo4  
            self.function.hexStrToHexBytes(str(hex(int(cobid_TPDO4,16)+0x80000000).replace('0x','')))   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4Cobid+self.function.getSdoDataStr()])  
            #clear tpdo4, 1A03:00,1byte
            self.function.hexStrToHexBytes('00')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4NumberOfMappedObjects+self.function.getSdoDataStr()])
            #transmission type
            self.function.hexStrToHexBytes(tpdo4ParaList[5])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4TransmissionType+self.function.getSdoDataStr()])  
            #inhibit time    
            self.function.hexStrToHexBytes(tpdo4ParaList[6])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4InhibitTime+self.function.getSdoDataStr()])  
            #event time
            self.function.hexStrToHexBytes(tpdo4ParaList[7])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4EventTimer+self.function.getSdoDataStr()]) 
            #sync start value
            self.function.hexStrToHexBytes(tpdo4ParaList[8])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4SyncStartValue+self.function.getSdoDataStr()]) 
            #data
            if tpdo4ParaList[0] == '4':
                self.function.hexStrToHexBytes(tpdo4ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(tpdo4ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(tpdo4ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4MappedObject3+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(tpdo4ParaList[4])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4MappedObject4+self.function.getSdoDataStr()])
            elif tpdo4ParaList[0] == '3': 
                self.function.hexStrToHexBytes(tpdo4ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(tpdo4ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(tpdo4ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4MappedObject3+self.function.getSdoDataStr()])  
            elif tpdo4ParaList[0] == '2': 
                self.function.hexStrToHexBytes(tpdo4ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(tpdo4ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4MappedObject2+self.function.getSdoDataStr()])
            elif tpdo4ParaList[0] == '1': 
                self.function.hexStrToHexBytes(tpdo4ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4MappedObject1+self.function.getSdoDataStr()])          
            #mapped object
            self.function.hexStrToHexBytes(str(tpdo4ParaList[0]))
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4NumberOfMappedObjects+self.function.getSdoDataStr()])                              
        else:
            #disable pdo4  
            #self.function.hexStrToHexBytes(str(hex(int(cobid_TPDO4,16)+0x80000000).replace('0x','')))   
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4Cobid+self.function.getSdoDataStr()])  
            #self.function.hexStrToHexBytes(str(tpdo4ParaList[0]))
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4NumberOfMappedObjects+self.function.getSdoDataStr()]) 
            pass
        pass              



