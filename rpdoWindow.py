import pyqtgraph as pg
import struct
#import function
import sys
import time
import array
import ui_flowrpdo
from ui_flowrpdo import Ui_RPDO

from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray, QTimer, QDate, Qt
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAbstractItemView, QHeaderView, QTableWidgetItem, QWidget, QMessageBox
from pyqtgraph import PlotWidget
from PyQt5.QtGui import QFont,QColor,QBrush,QPixmap
import rwQueue
import globalConstants as gc

class rpdoWindow(QWidget,Ui_RPDO):
    def __init__(self,comTransceiver,function):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("RPDO Config") 
        self.mainWindow = None
        self.comTransceiver = comTransceiver
        self.function       = function
        #几个数据,数据1,数据2,数据3,数据4,transType,eventTimer
        self.rpdo1ParaList = ['0','0','0','0','0','FF','0']
        self.rpdo2ParaList = ['0','0','0','0','0','FF','0']
        self.rpdo3ParaList = ['0','0','0','0','0','FF','0']
        self.rpdo4ParaList = ['0','0','0','0','0','FF','0']  
        self.cobid_Servo_RPDO1   = ''  
        self.cobid_Servo_RPDO2   = ''  
        self.cobid_Servo_RPDO3   = ''  
        self.cobid_Servo_RPDO4   = ''  
        self.cobid_TSDO    = ''  
        self.CreateSignalSlot()
        pass
    def setMainWindow(self,mainWindow):
        self.mainWindow = mainWindow 
        pass 
       # 设置信号与槽
    def CreateSignalSlot(self):
        self.comboBox_rpdo_pdo1_data1.addItems(gc.rpdoAvailableList)         
        self.comboBox_rpdo_pdo1_data2.addItems(gc.rpdoAvailableList)    
        self.comboBox_rpdo_pdo1_data3.addItems(gc.rpdoAvailableList)    
        self.comboBox_rpdo_pdo1_data4.addItems(gc.rpdoAvailableList)    
        self.comboBox_rpdo_pdo1_transmissionType.addItems(gc.listOfRpdoTransmissionType)
        self.comboBox_rpdo_pdo2_data1.addItems(gc.rpdoAvailableList)           
        self.comboBox_rpdo_pdo2_data2.addItems(gc.rpdoAvailableList)    
        self.comboBox_rpdo_pdo2_data3.addItems(gc.rpdoAvailableList)    
        self.comboBox_rpdo_pdo2_data4.addItems(gc.rpdoAvailableList)    
        self.comboBox_rpdo_pdo2_transmissionType.addItems(gc.listOfRpdoTransmissionType)
        self.comboBox_rpdo_pdo3_data1.addItems(gc.rpdoAvailableList)           
        self.comboBox_rpdo_pdo3_data2.addItems(gc.rpdoAvailableList)    
        self.comboBox_rpdo_pdo3_data3.addItems(gc.rpdoAvailableList)    
        self.comboBox_rpdo_pdo3_data4.addItems(gc.rpdoAvailableList)    
        self.comboBox_rpdo_pdo3_transmissionType.addItems(gc.listOfRpdoTransmissionType) 
        self.comboBox_rpdo_pdo4_data1.addItems(gc.rpdoAvailableList)        
        self.comboBox_rpdo_pdo4_data2.addItems(gc.rpdoAvailableList)    
        self.comboBox_rpdo_pdo4_data3.addItems(gc.rpdoAvailableList)    
        self.comboBox_rpdo_pdo4_data4.addItems(gc.rpdoAvailableList)    
        self.comboBox_rpdo_pdo4_transmissionType.addItems(gc.listOfRpdoTransmissionType)                
        self.setDefault()
        #按钮的默认状态
        self.pushButton_rpdo_clear.clicked.connect(self.pushButton_rpdo_clear_clicked) 
        self.pushButton_rpdo_update.clicked.connect(self.pushButton_rpdo_update_clicked) 
        self.comboBox_rpdo_pdo1_data1.currentIndexChanged.connect(self.comboBox_rpdo_pdo1_data1_currentIndexChanged)
        self.comboBox_rpdo_pdo1_data2.currentIndexChanged.connect(self.comboBox_rpdo_pdo1_data2_currentIndexChanged) 
        self.comboBox_rpdo_pdo1_data3.currentIndexChanged.connect(self.comboBox_rpdo_pdo1_data3_currentIndexChanged) 
        self.comboBox_rpdo_pdo2_data1.currentIndexChanged.connect(self.comboBox_rpdo_pdo2_data1_currentIndexChanged)
        self.comboBox_rpdo_pdo2_data2.currentIndexChanged.connect(self.comboBox_rpdo_pdo2_data2_currentIndexChanged) 
        self.comboBox_rpdo_pdo2_data3.currentIndexChanged.connect(self.comboBox_rpdo_pdo2_data3_currentIndexChanged)
        self.comboBox_rpdo_pdo3_data1.currentIndexChanged.connect(self.comboBox_rpdo_pdo3_data1_currentIndexChanged)
        self.comboBox_rpdo_pdo3_data2.currentIndexChanged.connect(self.comboBox_rpdo_pdo3_data2_currentIndexChanged) 
        self.comboBox_rpdo_pdo3_data3.currentIndexChanged.connect(self.comboBox_rpdo_pdo3_data3_currentIndexChanged) 
        self.comboBox_rpdo_pdo4_data1.currentIndexChanged.connect(self.comboBox_rpdo_pdo4_data1_currentIndexChanged)
        self.comboBox_rpdo_pdo4_data2.currentIndexChanged.connect(self.comboBox_rpdo_pdo4_data2_currentIndexChanged) 
        self.comboBox_rpdo_pdo4_data3.currentIndexChanged.connect(self.comboBox_rpdo_pdo4_data3_currentIndexChanged)    
        pass
    def setDefault(self):
        #RPDO1的默认状态 
        self.comboBox_rpdo_pdo1_data1.setCurrentIndex(0)            
        self.comboBox_rpdo_pdo1_data2.setCurrentIndex(0) 
        self.comboBox_rpdo_pdo1_data3.setCurrentIndex(0)  
        self.comboBox_rpdo_pdo1_data4.setCurrentIndex(0) 
        self.comboBox_rpdo_pdo1_transmissionType.setCurrentIndex(self.comboBox_rpdo_pdo1_transmissionType.count() - 1) 
        self.lineEdit_rpdo_pdo1_eventTimer.setText("0")
        self.comboBox_rpdo_pdo1_data2.setEnabled(False) 
        self.comboBox_rpdo_pdo1_data3.setEnabled(False)  
        self.comboBox_rpdo_pdo1_data4.setEnabled(False)
        #RPDO2的默认状态 
        self.comboBox_rpdo_pdo2_data1.setCurrentIndex(0)          
        self.comboBox_rpdo_pdo2_data2.setCurrentIndex(0)  
        self.comboBox_rpdo_pdo2_data3.setCurrentIndex(0)  
        self.comboBox_rpdo_pdo2_data4.setCurrentIndex(0) 
        self.comboBox_rpdo_pdo2_transmissionType.setCurrentIndex(self.comboBox_rpdo_pdo2_transmissionType.count() - 1)
        self.lineEdit_rpdo_pdo2_eventTimer.setText("0")
        self.comboBox_rpdo_pdo2_data2.setEnabled(False) 
        self.comboBox_rpdo_pdo2_data3.setEnabled(False)  
        self.comboBox_rpdo_pdo2_data4.setEnabled(False) 
        #RPDO3的默认状态 
        self.comboBox_rpdo_pdo3_data1.setCurrentIndex(0)          
        self.comboBox_rpdo_pdo3_data2.setCurrentIndex(0)   
        self.comboBox_rpdo_pdo3_data3.setCurrentIndex(0) 
        self.comboBox_rpdo_pdo3_data4.setCurrentIndex(0) 
        self.comboBox_rpdo_pdo3_transmissionType.setCurrentIndex(self.comboBox_rpdo_pdo3_transmissionType.count() - 1) 
        self.lineEdit_rpdo_pdo3_eventTimer.setText("0")
        self.comboBox_rpdo_pdo3_data2.setEnabled(False) 
        self.comboBox_rpdo_pdo3_data3.setEnabled(False)  
        self.comboBox_rpdo_pdo3_data4.setEnabled(False)
        #RPDO4的默认状态  
        self.comboBox_rpdo_pdo4_data1.setCurrentIndex(0)           
        self.comboBox_rpdo_pdo4_data2.setCurrentIndex(0)    
        self.comboBox_rpdo_pdo4_data3.setCurrentIndex(0) 
        self.comboBox_rpdo_pdo4_data4.setCurrentIndex(0) 
        self.comboBox_rpdo_pdo4_transmissionType.setCurrentIndex(self.comboBox_rpdo_pdo4_transmissionType.count() - 1) 
        self.lineEdit_rpdo_pdo4_eventTimer.setText("0")
        self.comboBox_rpdo_pdo4_data2.setEnabled(False) 
        self.comboBox_rpdo_pdo4_data3.setEnabled(False)  
        self.comboBox_rpdo_pdo4_data4.setEnabled(False)
        pass
      
    def pushButton_rpdo_clear_clicked(self):
        self.setDefault()
        pass
    def pushButton_rpdo_update_clicked(self):
        rpdoStatusOk = True
        pdo1Continue = True
        pdo2Continue = True
        pdo3Continue = True
        pdo4Continue = True
        rpdo1DataNum = 0
        rpdo2DataNum = 0
        rpdo3DataNum = 0
        rpdo4DataNum = 0
        rpdo1Len = 0
        rpdo2Len = 0
        rpdo3Len = 0
        rpdo4Len = 0
        #rpdo1
        if pdo1Continue:
            if self.comboBox_rpdo_pdo1_data1.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo1_data1.currentText())
                rpdo1DataNum += int(tempObject[1],10)
                self.rpdo1ParaList[0] ='1'
                self.rpdo1ParaList[1] = tempObject[0] 
            else:
                self.rpdo1ParaList[0] ='0'
                pdo1Continue = False
        if pdo1Continue:        
            if self.comboBox_rpdo_pdo1_data2.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo1_data2.currentText())
                rpdo1DataNum += int(tempObject[1],10)
                self.rpdo1ParaList[0] ='2'
                self.rpdo1ParaList[2] = tempObject[0]
            else:
                pdo1Continue = False
        if pdo1Continue:
            if self.comboBox_rpdo_pdo1_data3.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo1_data3.currentText())
                rpdo1DataNum += int(tempObject[1],10)
                self.rpdo1ParaList[0] ='3'
                self.rpdo1ParaList[3] = tempObject[0]
            else:
                pdo1Continue = False
        if pdo1Continue:
            if self.comboBox_rpdo_pdo1_data4.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo1_data4.currentText())
                rpdo1DataNum += int(tempObject[1],10)
                self.rpdo1ParaList[0] ='4'
                self.rpdo1ParaList[4] = tempObject[0] 
            else:
                pdo1Continue = False
        #rpdo1 transmission type
        self.rpdo1ParaList[5] = str(hex(int(self.comboBox_rpdo_pdo1_transmissionType.currentText(),10)).replace('0x','').zfill(2).upper())  
        # eventTimer
        eventTimer = self.lineEdit_rpdo_pdo1_eventTimer.text()
        if eventTimer.isdecimal():
            self.rpdo1ParaList[6] = str(hex(int(self.lineEdit_rpdo_pdo1_eventTimer.text(), 10)).replace("0x", "").zfill(4).upper())
        else:
            self.rpdo1ParaList[6] = "0"
            QMessageBox.warning(self, "Error", "rpdo1 eventTimer, Wrong Input")
        #检查本rpdo是否合理,主要是长度不要超过8个byte.
        if rpdo1DataNum > 8:    
            QMessageBox.warning(self,"Error","too much data for Rpdo1.") 
            self.rpdo1ParaList[0] = '0'
            rpdoStatusOk = False
        #rpdo2
        if pdo2Continue:
            if self.comboBox_rpdo_pdo2_data1.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo2_data1.currentText())
                rpdo2DataNum += int(tempObject[1],10)
                self.rpdo2ParaList[0] = '1'
                self.rpdo2ParaList[1] = tempObject[0]  
            else:
                self.rpdo2ParaList[0] = '0'
                pdo2Continue = False
        if pdo2Continue:
            if self.comboBox_rpdo_pdo2_data2.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo2_data2.currentText())
                rpdo2DataNum += int(tempObject[1],10)
                self.rpdo2ParaList[0] = '2'
                self.rpdo2ParaList[2] = tempObject[0]   
            else:
                pdo2Continue = False 
        if pdo2Continue: 
            if self.comboBox_rpdo_pdo2_data3.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo2_data3.currentText())
                rpdo2DataNum += int(tempObject[1],10)
                self.rpdo2ParaList[0] = '3'
                self.rpdo2ParaList[3] = tempObject[0] 
            else:
                pdo2Continue = False  
        if pdo2Continue:  
            if self.comboBox_rpdo_pdo2_data4.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo2_data4.currentText())
                rpdo2DataNum += int(tempObject[1],10)
                self.rpdo2ParaList[0] = '4'
                self.rpdo2ParaList[4] = tempObject[0]  
            else:
                pdo2Continue = False  
        #rpdo1 transmission type
        self.rpdo2ParaList[5] = str(hex(int(self.comboBox_rpdo_pdo2_transmissionType.currentText(),10)).replace('0x','').zfill(2).upper())  
        # eventTimer
        eventTimer = self.lineEdit_rpdo_pdo2_eventTimer.text()
        if eventTimer.isdecimal():
            self.rpdo2ParaList[6] = str(hex(int(self.lineEdit_rpdo_pdo2_eventTimer.text(), 10)).replace("0x", "").zfill(4).upper())
        else:
            self.rpdo2ParaList[6] = "0"
            QMessageBox.warning(self, "Error", "rpdo2 eventTimer, Wrong Input")
        #检查本rpdo是否合理,主要是长度不要超过8个byte.
        if rpdo2DataNum > 8:    
            QMessageBox.warning(self,"Error","too much data for Rpdo2.") 
            self.rpdo2ParaList[0] = '0'
            rpdoStatusOk = False
        #rpdo3
        if pdo3Continue:
            if self.comboBox_rpdo_pdo3_data1.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo3_data1.currentText())
                rpdo3DataNum += int(tempObject[1],10)
                self.rpdo3ParaList[0] = '1'
                self.rpdo3ParaList[1] = tempObject[0]    
            else:
                self.rpdo3ParaList[0] = '0'
                pdo3Continue = False 
        if pdo3Continue:   
            if self.comboBox_rpdo_pdo3_data2.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo3_data2.currentText())
                rpdo3DataNum += int(tempObject[1],10)
                self.rpdo3ParaList[0] = '2'
                self.rpdo3ParaList[2] = tempObject[0]  
            else:
                pdo3Continue = False 
        if pdo3Continue:  
            if self.comboBox_rpdo_pdo3_data3.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo3_data3.currentText())
                rpdo3DataNum += int(tempObject[1],10)
                self.rpdo3ParaList[0] = '3'
                self.rpdo3ParaList[3] = tempObject[0]
            else:
                pdo3Continue = False 
        if pdo3Continue:
            if self.comboBox_rpdo_pdo3_data4.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo3_data4.currentText())
                rpdo3DataNum += int(tempObject[1],10)
                self.rpdo3ParaList[0] = '4'
                self.rpdo3ParaList[4] = tempObject[0] 
            else:
                pdo3Continue = False   
        #rpdo1 transmission type
        self.rpdo3ParaList[5] = str(hex(int(self.comboBox_rpdo_pdo3_transmissionType.currentText(),10)).replace('0x','').zfill(2).upper())
        # eventTimer
        eventTimer = self.lineEdit_rpdo_pdo3_eventTimer.text()
        if eventTimer.isdecimal():
            self.rpdo3ParaList[6] = str(hex(int(self.lineEdit_rpdo_pdo3_eventTimer.text(), 10)).replace("0x", "").zfill(4).upper())
        else:
            self.rpdo3ParaList[6] = "0"
            QMessageBox.warning(self, "Error", "rpdo3 eventTimer, Wrong Input")
        #检查本rpdo是否合理,主要是长度不要超过8个byte.
        if rpdo3DataNum > 8:    
            QMessageBox.warning(self,"Error","too much data for Rpdo3.") 
            self.rpdo3ParaList[0] = '0'
            rpdoStatusOk = False
        #rpdo4
        if pdo4Continue:
            if self.comboBox_rpdo_pdo4_data1.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo4_data1.currentText())
                rpdo4DataNum += int(tempObject[1],10)
                self.rpdo4ParaList[0] = '1'
                self.rpdo4ParaList[1] = tempObject[0]  
            else:
                self.rpdo4ParaList[0] = '0'
                pdo4Continue = False 
        if pdo4Continue:
            if self.comboBox_rpdo_pdo4_data2.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo4_data2.currentText())
                rpdo4DataNum += int(tempObject[1],10)
                self.rpdo4ParaList[0] = '2'
                self.rpdo4ParaList[2] = tempObject[0]  
            else:
                pdo4Continue = False 
        if pdo4Continue:
            if self.comboBox_rpdo_pdo4_data3.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo4_data3.currentText())
                rpdo4DataNum += int(tempObject[1],10)
                self.rpdo4ParaList[0] = '3'
                self.rpdo4ParaList[3] = tempObject[0]
            else:
                pdo4Continue = False 
        if pdo4Continue:
            if self.comboBox_rpdo_pdo4_data4.currentText() != 'none':
                tempObject = gc.ojbectDict.get(self.comboBox_rpdo_pdo4_data4.currentText())
                rpdo4DataNum += int(tempObject[1],10)
                self.rpdo4ParaList[0] = '4'
                self.rpdo4ParaList[4] = tempObject[0]    
            else:
                pdo4Continue = False  
        #rpdo1 transmission type
        self.rpdo4ParaList[5] = str(hex(int(self.comboBox_rpdo_pdo4_transmissionType.currentText(),10)).replace('0x','').zfill(2).upper()) 
        # eventTimer
        eventTimer = self.lineEdit_rpdo_pdo4_eventTimer.text()
        if eventTimer.isdecimal():
            self.rpdo4ParaList[6] = str(hex(int(self.lineEdit_rpdo_pdo4_eventTimer.text(), 10)).replace("0x", "").zfill(4).upper())
        else:
            self.rpdo4ParaList[6] = "0"
            QMessageBox.warning(self, "Error", "rpdo4 eventTimer, Wrong Input")
        #检查本rpdo是否合理,主要是长度不要超过8个byte.
        if rpdo4DataNum > 8:    
            QMessageBox.warning(self,"Error","too much data for Rpdo4.") 
            self.rpdo4ParaList[0] = '0'
            rpdoStatusOk = False
        if rpdoStatusOk == True:
            decNodeid = self.mainWindow.getDecNodeid()
            self.configRpdo(decNodeid)
            self.close()
        #print('rpdo1ParaList=',self.rpdo1ParaList)
        #print('rpdo2ParaList=',self.rpdo2ParaList)
        #print('rpdo3ParaList=',self.rpdo3ParaList)
        #print('rpdo4ParaList=',self.rpdo4ParaList)
        pass   
    def comboBox_rpdo_pdo1_data1_currentIndexChanged(self):
        if self.comboBox_rpdo_pdo1_data1.currentText() != 'none':
            self.comboBox_rpdo_pdo1_data2.setEnabled(True) 
        else:
            self.comboBox_rpdo_pdo1_data2.setCurrentIndex(0) 
            self.comboBox_rpdo_pdo1_data3.setCurrentIndex(0)  
            self.comboBox_rpdo_pdo1_data4.setCurrentIndex(0)
            self.comboBox_rpdo_pdo1_data2.setEnabled(False) 
            self.comboBox_rpdo_pdo1_data3.setEnabled(False)  
            self.comboBox_rpdo_pdo1_data4.setEnabled(False)
        pass
    def comboBox_rpdo_pdo1_data2_currentIndexChanged(self):
        if self.comboBox_rpdo_pdo1_data2.currentText() != 'none':
            self.comboBox_rpdo_pdo1_data3.setEnabled(True) 
        else:
            self.comboBox_rpdo_pdo1_data3.setCurrentIndex(0)  
            self.comboBox_rpdo_pdo1_data4.setCurrentIndex(0)
            self.comboBox_rpdo_pdo1_data3.setEnabled(False)  
            self.comboBox_rpdo_pdo1_data4.setEnabled(False)
        pass
    def comboBox_rpdo_pdo1_data3_currentIndexChanged(self):
        if self.comboBox_rpdo_pdo1_data3.currentText() != 'none':
            self.comboBox_rpdo_pdo1_data4.setEnabled(True) 
        else:
            self.comboBox_rpdo_pdo1_data4.setCurrentIndex(0)
            self.comboBox_rpdo_pdo1_data4.setEnabled(False)
        pass

    def comboBox_rpdo_pdo2_data1_currentIndexChanged(self):
        if self.comboBox_rpdo_pdo2_data1.currentText() != 'none':
            self.comboBox_rpdo_pdo2_data2.setEnabled(True) 
        else:
            self.comboBox_rpdo_pdo2_data2.setCurrentIndex(0) 
            self.comboBox_rpdo_pdo2_data3.setCurrentIndex(0)  
            self.comboBox_rpdo_pdo2_data4.setCurrentIndex(0)
            self.comboBox_rpdo_pdo2_data2.setEnabled(False) 
            self.comboBox_rpdo_pdo2_data3.setEnabled(False)  
            self.comboBox_rpdo_pdo2_data4.setEnabled(False)
        pass
    def comboBox_rpdo_pdo2_data2_currentIndexChanged(self):
        if self.comboBox_rpdo_pdo2_data2.currentText() != 'none':
            self.comboBox_rpdo_pdo2_data3.setEnabled(True) 
        else:
            self.comboBox_rpdo_pdo2_data3.setCurrentIndex(0)  
            self.comboBox_rpdo_pdo2_data4.setCurrentIndex(0)
            self.comboBox_rpdo_pdo2_data3.setEnabled(False)  
            self.comboBox_rpdo_pdo2_data4.setEnabled(False)
        pass
    def comboBox_rpdo_pdo2_data3_currentIndexChanged(self):
        if self.comboBox_rpdo_pdo2_data3.currentText() != 'none':
            self.comboBox_rpdo_pdo2_data4.setEnabled(True) 
        else:
            self.comboBox_rpdo_pdo2_data4.setCurrentIndex(0)
            self.comboBox_rpdo_pdo2_data4.setEnabled(False)
        pass

    def comboBox_rpdo_pdo3_data1_currentIndexChanged(self):
        if self.comboBox_rpdo_pdo3_data1.currentText() != 'none':
            self.comboBox_rpdo_pdo3_data2.setEnabled(True) 
        else:
            self.comboBox_rpdo_pdo3_data2.setCurrentIndex(0) 
            self.comboBox_rpdo_pdo3_data3.setCurrentIndex(0)  
            self.comboBox_rpdo_pdo3_data4.setCurrentIndex(0)
            self.comboBox_rpdo_pdo3_data2.setEnabled(False) 
            self.comboBox_rpdo_pdo3_data3.setEnabled(False)  
            self.comboBox_rpdo_pdo3_data4.setEnabled(False)
        pass
    def comboBox_rpdo_pdo3_data2_currentIndexChanged(self):
        if self.comboBox_rpdo_pdo3_data2.currentText() != 'none':
            self.comboBox_rpdo_pdo3_data3.setEnabled(True) 
        else:
            self.comboBox_rpdo_pdo3_data3.setCurrentIndex(0)  
            self.comboBox_rpdo_pdo3_data4.setCurrentIndex(0)
            self.comboBox_rpdo_pdo3_data3.setEnabled(False)  
            self.comboBox_rpdo_pdo3_data4.setEnabled(False)
        pass
    def comboBox_rpdo_pdo3_data3_currentIndexChanged(self):
        if self.comboBox_rpdo_pdo3_data3.currentText() != 'none':
            self.comboBox_rpdo_pdo3_data4.setEnabled(True) 
        else: 
            self.comboBox_rpdo_pdo3_data4.setCurrentIndex(0)
            self.comboBox_rpdo_pdo3_data4.setEnabled(False)
        pass

    def comboBox_rpdo_pdo4_data1_currentIndexChanged(self):
        if self.comboBox_rpdo_pdo4_data1.currentText() != 'none':
            self.comboBox_rpdo_pdo4_data2.setEnabled(True) 
        else:
            self.comboBox_rpdo_pdo4_data2.setCurrentIndex(0) 
            self.comboBox_rpdo_pdo4_data3.setCurrentIndex(0)  
            self.comboBox_rpdo_pdo4_data4.setCurrentIndex(0)
            self.comboBox_rpdo_pdo4_data2.setEnabled(False) 
            self.comboBox_rpdo_pdo4_data3.setEnabled(False)  
            self.comboBox_rpdo_pdo4_data4.setEnabled(False)
        pass
    def comboBox_rpdo_pdo4_data2_currentIndexChanged(self):
        if self.comboBox_rpdo_pdo4_data2.currentText() != 'none':
            self.comboBox_rpdo_pdo4_data3.setEnabled(True) 
        else:
            self.comboBox_rpdo_pdo4_data3.setCurrentIndex(0)  
            self.comboBox_rpdo_pdo4_data4.setCurrentIndex(0)
            self.comboBox_rpdo_pdo4_data3.setEnabled(False)  
            self.comboBox_rpdo_pdo4_data4.setEnabled(False)
        pass
    def comboBox_rpdo_pdo4_data3_currentIndexChanged(self):
        if self.comboBox_rpdo_pdo4_data3.currentText() != 'none':
            self.comboBox_rpdo_pdo4_data4.setEnabled(True) 
        else:
            self.comboBox_rpdo_pdo4_data4.setCurrentIndex(0)
            self.comboBox_rpdo_pdo4_data4.setEnabled(False)
        pass

    def configRpdo(self,decNodeid):
        cobid_RPDO1    = (str(hex(decNodeid+gc.cobid_RPDO1)).replace('0x','')).zfill(3).upper()
        cobid_RPDO2    = (str(hex(decNodeid+gc.cobid_RPDO2)).replace('0x','')).zfill(3).upper()
        cobid_RPDO3    = (str(hex(decNodeid+gc.cobid_RPDO3)).replace('0x','')).zfill(3).upper()
        cobid_RPDO4    = (str(hex(decNodeid+gc.cobid_RPDO4)).replace('0x','')).zfill(3).upper()
        cobid_TSDO     = (str(hex(decNodeid+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
        #rpdo1 
        rpdo1ParaList = self.rpdo1ParaList
        if rpdo1ParaList[0] != '0':    
            #disable pdo1
            self.function.hexStrToHexBytes(str(hex(int(cobid_RPDO1,16)+0x80000000).replace('0x','')))    
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1Cobid+self.function.getSdoDataStr()]) 
            #clear rpdo1, 1600:00,1byte
            self.function.hexStrToHexBytes('00')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1NumberOfMappedObjects+self.function.getSdoDataStr()])
            #transmission type
            self.function.hexStrToHexBytes(rpdo1ParaList[5])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1TransmissionType+self.function.getSdoDataStr()])  
            #event timer
            self.function.hexStrToHexBytes(rpdo1ParaList[6])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1EventTimer+self.function.getSdoDataStr()])  
            if rpdo1ParaList[0] == '4':
                self.function.hexStrToHexBytes(rpdo1ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(rpdo1ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(rpdo1ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1MappedObject3+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(rpdo1ParaList[4])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1MappedObject4+self.function.getSdoDataStr()])
            elif rpdo1ParaList[0] == '3': 
                self.function.hexStrToHexBytes(rpdo1ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(rpdo1ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(rpdo1ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1MappedObject3+self.function.getSdoDataStr()])  
            elif rpdo1ParaList[0] == '2': 
                self.function.hexStrToHexBytes(rpdo1ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(rpdo1ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1MappedObject2+self.function.getSdoDataStr()])
            elif rpdo1ParaList[0] == '1': 
                self.function.hexStrToHexBytes(rpdo1ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1MappedObject1+self.function.getSdoDataStr()])          
            #mapped object
            self.function.hexStrToHexBytes(str(rpdo1ParaList[0]))
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1NumberOfMappedObjects+self.function.getSdoDataStr()])   
        else:
            #disable pdo1
            #self.function.hexStrToHexBytes(str(hex(int(cobid_RPDO1,16)+0x80000000).replace('0x','')))    
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1Cobid+self.function.getSdoDataStr()]) 
            #self.function.hexStrToHexBytes(str(rpdo1ParaList[0]))
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1NumberOfMappedObjects+self.function.getSdoDataStr()])  
            pass
        #rpdo2 
        rpdo2ParaList = self.rpdo2ParaList
        if rpdo2ParaList[0] != '0':  
            #disable rpdo2  
            self.function.hexStrToHexBytes(str(hex(int(cobid_RPDO2,16)+0x80000000).replace('0x','')))    
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2Cobid+self.function.getSdoDataStr()])  
            #clear rpdo2, 1601:00,1byte
            self.function.hexStrToHexBytes('00')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2NumberOfMappedObjects+self.function.getSdoDataStr()]) 
            #transmission type
            self.function.hexStrToHexBytes(rpdo2ParaList[5])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2TransmissionType+self.function.getSdoDataStr()])  
            #event timer
            self.function.hexStrToHexBytes(rpdo2ParaList[6])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2EventTimer+self.function.getSdoDataStr()])   
            #data
            if rpdo2ParaList[0] == '4':
                self.function.hexStrToHexBytes(rpdo2ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(rpdo2ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(rpdo2ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2MappedObject3+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(rpdo2ParaList[4])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2MappedObject4+self.function.getSdoDataStr()])
            elif rpdo2ParaList[0] == '3': 
                self.function.hexStrToHexBytes(rpdo2ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(rpdo2ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(rpdo2ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2MappedObject3+self.function.getSdoDataStr()])  
            elif rpdo2ParaList[0] == '2': 
                self.function.hexStrToHexBytes(rpdo2ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(rpdo2ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2MappedObject2+self.function.getSdoDataStr()]) 
            elif rpdo2ParaList[0] == '1': 
                self.function.hexStrToHexBytes(rpdo2ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2MappedObject1+self.function.getSdoDataStr()])                          
            #mapped object
            self.function.hexStrToHexBytes(str(rpdo2ParaList[0]))
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2NumberOfMappedObjects+self.function.getSdoDataStr()])   
        else:
            #disable rpdo2  
            #self.function.hexStrToHexBytes(str(hex(int(cobid_RPDO2,16)+0x80000000).replace('0x','')))    
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2Cobid+self.function.getSdoDataStr()])  
            #self.function.hexStrToHexBytes(str(rpdo2ParaList[0]))
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2NumberOfMappedObjects+self.function.getSdoDataStr()])   
            pass
        #rpdo3 
        rpdo3ParaList = self.rpdo3ParaList
        if rpdo3ParaList[0] != '0':     
            #disable pdo3 
            self.function.hexStrToHexBytes(str(hex(int(cobid_RPDO3,16)+0x80000000).replace('0x','')))    
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3Cobid+self.function.getSdoDataStr()])
            #clear rpdo3, 1602:00,1byte
            self.function.hexStrToHexBytes('00')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3NumberOfMappedObjects+self.function.getSdoDataStr()])
            #transmission type
            self.function.hexStrToHexBytes(rpdo3ParaList[5])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3TransmissionType+self.function.getSdoDataStr()])    
            #event timer
            self.function.hexStrToHexBytes(rpdo3ParaList[6])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3EventTimer+self.function.getSdoDataStr()])   
            #data
            if rpdo3ParaList[0] == '4':
                self.function.hexStrToHexBytes(rpdo3ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(rpdo3ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(rpdo3ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3MappedObject3+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(rpdo3ParaList[4])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3MappedObject4+self.function.getSdoDataStr()])
            elif rpdo3ParaList[0] == '3': 
                self.function.hexStrToHexBytes(rpdo3ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(rpdo3ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(rpdo3ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3MappedObject3+self.function.getSdoDataStr()])  
            elif rpdo3ParaList[0] == '2': 
                self.function.hexStrToHexBytes(rpdo3ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(rpdo3ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3MappedObject2+self.function.getSdoDataStr()])
            elif rpdo3ParaList[0] == '1': 
                self.function.hexStrToHexBytes(rpdo3ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3MappedObject1+self.function.getSdoDataStr()])             
            #mapped object
            self.function.hexStrToHexBytes(str(rpdo3ParaList[0]))
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3NumberOfMappedObjects+self.function.getSdoDataStr()])   
            #enable pdo3
            #self.function.hexStrToHexBytes(str(hex(int(self.cobid_TPDO3,16)+0x00000000).replace('0x','')))    
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeRPDO3Cobid+self.function.getSdoDataStr()])  
        else:
            #disable pdo3 
            #self.function.hexStrToHexBytes(str(hex(int(cobid_RPDO3,16)+0x80000000).replace('0x','')))    
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3Cobid+self.function.getSdoDataStr()])
            #self.function.hexStrToHexBytes(str(rpdo3ParaList[0]))
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3NumberOfMappedObjects+self.function.getSdoDataStr()])  
            pass
        #rpdo4
        rpdo4ParaList = self.rpdo4ParaList
        if rpdo4ParaList[0] != '0':   
            #disable pdo4
            self.function.hexStrToHexBytes(str(hex(int(cobid_RPDO4,16)+0x80000000).replace('0x','')))      
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4Cobid+self.function.getSdoDataStr()])
            #clear rpdo4, 1603:00,1byte
            self.function.hexStrToHexBytes('00')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4NumberOfMappedObjects+self.function.getSdoDataStr()]) 
            #transmission type
            self.function.hexStrToHexBytes(rpdo4ParaList[5])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4TransmissionType+self.function.getSdoDataStr()]) 
            #event timer
            self.function.hexStrToHexBytes(rpdo4ParaList[6])   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4EventTimer+self.function.getSdoDataStr()]) 
            #data
            if rpdo4ParaList[0] == '4':
                self.function.hexStrToHexBytes(rpdo4ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(rpdo4ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(rpdo4ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4MappedObject3+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(rpdo4ParaList[4])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4MappedObject4+self.function.getSdoDataStr()])
            elif rpdo4ParaList[0] == '3': 
                self.function.hexStrToHexBytes(rpdo4ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(rpdo4ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4MappedObject2+self.function.getSdoDataStr()])
                self.function.hexStrToHexBytes(rpdo4ParaList[3])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4MappedObject3+self.function.getSdoDataStr()])  
            elif rpdo4ParaList[0] == '2': 
                self.function.hexStrToHexBytes(rpdo4ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4MappedObject1+self.function.getSdoDataStr()]) 
                self.function.hexStrToHexBytes(rpdo4ParaList[2])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4MappedObject2+self.function.getSdoDataStr()])
            elif rpdo4ParaList[0] == '1': 
                self.function.hexStrToHexBytes(rpdo4ParaList[1])
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4MappedObject1+self.function.getSdoDataStr()])           
            #mapped object
            self.function.hexStrToHexBytes(str(rpdo4ParaList[0]))
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4NumberOfMappedObjects+self.function.getSdoDataStr()])                              
        else:
            #disable pdo4
            #self.function.hexStrToHexBytes(str(hex(int(cobid_RPDO4,16)+0x80000000).replace('0x','')))      
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4Cobid+self.function.getSdoDataStr()])
            #self.function.hexStrToHexBytes(str(rpdo4ParaList[0]))
            #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4NumberOfMappedObjects+self.function.getSdoDataStr()])   
            pass
        pass        
