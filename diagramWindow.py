import pyqtgraph as pg
import struct
import sys
import time
import array
import csv
import ui_flowdiagram
from ui_flowdiagram import Ui_UI_diagram

from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray, QTimer, QDate, Qt
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAbstractItemView, QHeaderView, QTableWidgetItem, QWidget
from pyqtgraph import PlotWidget
from PyQt5.QtGui import QFont,QColor,QBrush,QPixmap
import rwQueue





class diagramWindow(QWidget,Ui_UI_diagram):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Diagram")  
        self.mainWindow = None
        #是有有效,是否有符号,几个byte,起始字符下标.
        self.Tpdo1Value1List = [False, False, 0, 0]
        self.Tpdo1Value2List = [False, False, 0, 0]
        self.Tpdo1Value3List = [False, False, 0, 0]
        self.Tpdo1Value4List = [False, False, 0, 0]
        self.Tpdo1NextIndex  = 0
        self.Tpdo2Value1List = [False, False, 0, 0]
        self.Tpdo2Value2List = [False, False, 0, 0]
        self.Tpdo2Value3List = [False, False, 0, 0]
        self.Tpdo2Value4List = [False, False, 0, 0]
        self.Tpdo2NextIndex  = 0
        self.Tpdo3Value1List = [False, False, 0, 0]
        self.Tpdo3Value2List = [False, False, 0, 0]
        self.Tpdo3Value3List = [False, False, 0, 0]
        self.Tpdo3Value4List = [False, False, 0, 0]
        self.Tpdo3NextIndex  = 0
        self.Tpdo4Value1List = [False, False, 0, 0]
        self.Tpdo4Value2List = [False, False, 0, 0]
        self.Tpdo4Value3List = [False, False, 0, 0]
        self.Tpdo4Value4List = [False, False, 0, 0] 
        self.Tpdo4NextIndex  = 0
        self.CreateSignalSlot()
        pass
    def setMainWindow(self,mainWindow):
        self.mainWindow = mainWindow
        pass 
        #list里面的3个数据,分别为是否存在/使能,是否为有符号数,长度是几个byte.     
       # 设置信号与槽
    def CreateSignalSlot(self):
        #diagram config界面按钮的默认状态
        self.comboBox_diagram_pdo1_data1.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])          
        self.comboBox_diagram_pdo1_data2.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])    
        self.comboBox_diagram_pdo1_data3.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])    
        self.comboBox_diagram_pdo1_data4.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])     
        self.comboBox_diagram_pdo2_data1.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])          
        self.comboBox_diagram_pdo2_data2.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])    
        self.comboBox_diagram_pdo2_data3.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])    
        self.comboBox_diagram_pdo2_data4.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])    
        self.comboBox_diagram_pdo3_data1.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])            
        self.comboBox_diagram_pdo3_data2.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])    
        self.comboBox_diagram_pdo3_data3.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])    
        self.comboBox_diagram_pdo3_data4.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])    
        self.comboBox_diagram_pdo4_data1.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])        
        self.comboBox_diagram_pdo4_data2.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])    
        self.comboBox_diagram_pdo4_data3.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])    
        self.comboBox_diagram_pdo4_data4.addItems(['none','int8','uint8','int16','uint16','int32','uint32'])    
        self.setDefault()

        self.pushButton_diagram_clear.clicked.connect(self.pushButton_diagram_clear_clicked) 
        self.pushButton_diagram_update.clicked.connect(self.pushButton_diagram_update_clicked) 
        self.comboBox_diagram_pdo1_data1.currentIndexChanged.connect(self.comboBox_diagram_pdo1_data1_currentIndexChanged)
        self.comboBox_diagram_pdo1_data2.currentIndexChanged.connect(self.comboBox_diagram_pdo1_data2_currentIndexChanged) 
        self.comboBox_diagram_pdo1_data3.currentIndexChanged.connect(self.comboBox_diagram_pdo1_data3_currentIndexChanged) 
        self.comboBox_diagram_pdo2_data1.currentIndexChanged.connect(self.comboBox_diagram_pdo2_data1_currentIndexChanged)
        self.comboBox_diagram_pdo2_data2.currentIndexChanged.connect(self.comboBox_diagram_pdo2_data2_currentIndexChanged) 
        self.comboBox_diagram_pdo2_data3.currentIndexChanged.connect(self.comboBox_diagram_pdo2_data3_currentIndexChanged)
        self.comboBox_diagram_pdo3_data1.currentIndexChanged.connect(self.comboBox_diagram_pdo3_data1_currentIndexChanged)
        self.comboBox_diagram_pdo3_data2.currentIndexChanged.connect(self.comboBox_diagram_pdo3_data2_currentIndexChanged) 
        self.comboBox_diagram_pdo3_data3.currentIndexChanged.connect(self.comboBox_diagram_pdo3_data3_currentIndexChanged) 
        self.comboBox_diagram_pdo4_data1.currentIndexChanged.connect(self.comboBox_diagram_pdo4_data1_currentIndexChanged)
        self.comboBox_diagram_pdo4_data2.currentIndexChanged.connect(self.comboBox_diagram_pdo4_data2_currentIndexChanged) 
        self.comboBox_diagram_pdo4_data3.currentIndexChanged.connect(self.comboBox_diagram_pdo4_data3_currentIndexChanged)           
        pass
    def setListValue(self,currentText):
        if currentText == 'none':
            tempList = [False, False, 0, 0]
        elif currentText == 'int8':  
            tempList = [True, True, 3, 0]
        elif currentText == 'uint8':  
            tempList = [True, False, 3, 0]
        elif currentText == 'int16':  
            tempList = [True, True, 6, 0]
        elif currentText == 'uint16':  
            tempList = [True, False, 6, 0]
        elif currentText == 'int32':  
            tempList = [True, True, 12, 0]
        elif currentText == 'uint32':  
            tempList = [True, False, 12, 0]            
        return tempList
    def pushButton_diagram_clear_clicked(self):
        self.setDefault()
        self.Tpdo1Value1List = [False, False, 0, 0]
        self.Tpdo1Value2List = [False, False, 0, 0]
        self.Tpdo1Value3List = [False, False, 0, 0]
        self.Tpdo1Value4List = [False, False, 0, 0]
        self.Tpdo2Value1List = [False, False, 0, 0]
        self.Tpdo2Value2List = [False, False, 0, 0]
        self.Tpdo2Value3List = [False, False, 0, 0]
        self.Tpdo2Value4List = [False, False, 0, 0]
        self.Tpdo3Value1List = [False, False, 0, 0]
        self.Tpdo3Value2List = [False, False, 0, 0]
        self.Tpdo3Value3List = [False, False, 0, 0]
        self.Tpdo3Value4List = [False, False, 0, 0]
        self.Tpdo4Value1List = [False, False, 0, 0]
        self.Tpdo4Value2List = [False, False, 0, 0]
        self.Tpdo4Value3List = [False, False, 0, 0]
        self.Tpdo4Value4List = [False, False, 0, 0] 
        self.updateDiagramConfig()
        pass
    def setDefault(self):
        self.comboBox_diagram_pdo1_data1.setCurrentIndex(0)            
        self.comboBox_diagram_pdo1_data2.setCurrentIndex(0)   
        self.comboBox_diagram_pdo1_data3.setCurrentIndex(0)    
        self.comboBox_diagram_pdo1_data4.setCurrentIndex(0)    
        self.comboBox_diagram_pdo2_data1.setCurrentIndex(0)            
        self.comboBox_diagram_pdo2_data2.setCurrentIndex(0)  
        self.comboBox_diagram_pdo2_data3.setCurrentIndex(0)  
        self.comboBox_diagram_pdo2_data4.setCurrentIndex(0)    
        self.comboBox_diagram_pdo3_data1.setCurrentIndex(0)          
        self.comboBox_diagram_pdo3_data2.setCurrentIndex(0)   
        self.comboBox_diagram_pdo3_data3.setCurrentIndex(0)   
        self.comboBox_diagram_pdo3_data4.setCurrentIndex(0)       
        self.comboBox_diagram_pdo4_data1.setCurrentIndex(0)          
        self.comboBox_diagram_pdo4_data2.setCurrentIndex(0)  
        self.comboBox_diagram_pdo4_data3.setCurrentIndex(0)    
        self.comboBox_diagram_pdo4_data4.setCurrentIndex(0)   
         
        self.comboBox_diagram_pdo1_data2.setEnabled(False)   
        self.comboBox_diagram_pdo1_data3.setEnabled(False)    
        self.comboBox_diagram_pdo1_data4.setEnabled(False)              
        self.comboBox_diagram_pdo2_data2.setEnabled(False)  
        self.comboBox_diagram_pdo2_data3.setEnabled(False)  
        self.comboBox_diagram_pdo2_data4.setEnabled(False)           
        self.comboBox_diagram_pdo3_data2.setEnabled(False)   
        self.comboBox_diagram_pdo3_data3.setEnabled(False)   
        self.comboBox_diagram_pdo3_data4.setEnabled(False)              
        self.comboBox_diagram_pdo4_data2.setEnabled(False)  
        self.comboBox_diagram_pdo4_data3.setEnabled(False)    
        self.comboBox_diagram_pdo4_data4.setEnabled(False)         
        pass
    def pushButton_diagram_update_clicked(self):
        #初始化下标计数.
        self.Tpdo1NextIndex  = 0
        self.Tpdo2NextIndex  = 0
        self.Tpdo3NextIndex  = 0
        self.Tpdo4NextIndex  = 0
        #获取配置,并存储在本地
        self.Tpdo1Value1List = self.setListValue(self.comboBox_diagram_pdo1_data1.currentText())
        self.Tpdo1Value1List[3] = 0
        self.Tpdo1NextIndex += self.Tpdo1Value1List[2]
        self.Tpdo1Value2List = self.setListValue(self.comboBox_diagram_pdo1_data2.currentText())
        self.Tpdo1Value2List[3] = self.Tpdo1NextIndex
        self.Tpdo1NextIndex += self.Tpdo1Value2List[2]
        self.Tpdo1Value3List = self.setListValue(self.comboBox_diagram_pdo1_data3.currentText())
        self.Tpdo1Value3List[3] = self.Tpdo1NextIndex 
        self.Tpdo1NextIndex += self.Tpdo1Value3List[2]
        self.Tpdo1Value4List = self.setListValue(self.comboBox_diagram_pdo1_data4.currentText())
        self.Tpdo1Value4List[3] = self.Tpdo1NextIndex  
        self.Tpdo1NextIndex += self.Tpdo1Value4List[2]
        
        self.Tpdo2Value1List = self.setListValue(self.comboBox_diagram_pdo2_data1.currentText())
        self.Tpdo2Value1List[3] = 0
        self.Tpdo2NextIndex += self.Tpdo2Value1List[2]
        self.Tpdo2Value2List = self.setListValue(self.comboBox_diagram_pdo2_data2.currentText())
        self.Tpdo2Value2List[3] = self.Tpdo2NextIndex
        self.Tpdo2NextIndex += self.Tpdo2Value2List[2] 
        self.Tpdo2Value3List = self.setListValue(self.comboBox_diagram_pdo2_data3.currentText())
        self.Tpdo2Value3List[3] = self.Tpdo2NextIndex 
        self.Tpdo2NextIndex += self.Tpdo2Value3List[2]
        self.Tpdo2Value4List = self.setListValue(self.comboBox_diagram_pdo2_data4.currentText())
        self.Tpdo2Value4List[3] = self.Tpdo2NextIndex  
        self.Tpdo2NextIndex += self.Tpdo2Value4List[2]
        
        self.Tpdo3Value1List = self.setListValue(self.comboBox_diagram_pdo3_data1.currentText())
        self.Tpdo3Value1List[3] = 0
        self.Tpdo3NextIndex += self.Tpdo3Value1List[2]
        self.Tpdo3Value2List = self.setListValue(self.comboBox_diagram_pdo3_data2.currentText())
        self.Tpdo3Value2List[3] = self.Tpdo3NextIndex
        self.Tpdo3NextIndex += self.Tpdo3Value2List[2]
        self.Tpdo3Value3List = self.setListValue(self.comboBox_diagram_pdo3_data3.currentText())
        self.Tpdo3Value3List[3] = self.Tpdo3NextIndex 
        self.Tpdo3NextIndex += self.Tpdo3Value3List[2]
        self.Tpdo3Value4List = self.setListValue(self.comboBox_diagram_pdo3_data4.currentText()) 
        self.Tpdo3Value4List[3] = self.Tpdo3NextIndex  
        self.Tpdo3NextIndex += self.Tpdo3Value4List[2]
        
        self.Tpdo4Value1List = self.setListValue(self.comboBox_diagram_pdo4_data1.currentText())
        self.Tpdo4Value1List[3] = 0
        self.Tpdo4NextIndex += self.Tpdo4Value1List[2]
        self.Tpdo4Value2List = self.setListValue(self.comboBox_diagram_pdo4_data2.currentText())
        self.Tpdo4Value2List[3] = self.Tpdo4NextIndex
        self.Tpdo4NextIndex += self.Tpdo4Value2List[2] 
        self.Tpdo4Value3List = self.setListValue(self.comboBox_diagram_pdo4_data3.currentText())
        self.Tpdo4Value3List[3] = self.Tpdo4NextIndex 
        self.Tpdo4NextIndex += self.Tpdo4Value3List[2]
        self.Tpdo4Value4List = self.setListValue(self.comboBox_diagram_pdo4_data4.currentText())
        self.Tpdo4Value4List[3] = self.Tpdo4NextIndex  
        self.Tpdo4NextIndex += self.Tpdo4Value4List[2]
          
        #判定是否有配置错误.若没有才发送给mainWindow
        if self.Tpdo1NextIndex > 24:
            print('error, too many data for TPDO1')
            print('tpdo1 byte=')
            print(self.Tpdo1NextIndex)
        elif self.Tpdo2NextIndex > 24:
            print('error, too many data for TPDO2')
            print('tpdo2 byte=')
            print(self.Tpdo2NextIndex)
        elif self.Tpdo3NextIndex > 24:
            print('error, too many data for TPDO3')
        elif self.Tpdo4NextIndex > 24:
            print('error, too many data for TPDO4') 
        else:   
            self.updateDiagramConfig()
        pass
        self.close()

    def comboBox_diagram_pdo1_data1_currentIndexChanged(self):
        if self.comboBox_diagram_pdo1_data1.currentText() != 'none':
            self.comboBox_diagram_pdo1_data2.setEnabled(True) 
        else:
            self.comboBox_diagram_pdo1_data2.setEnabled(False) 
            self.comboBox_diagram_pdo1_data3.setEnabled(False)  
            self.comboBox_diagram_pdo1_data4.setEnabled(False)
        pass
    def comboBox_diagram_pdo1_data2_currentIndexChanged(self):
        if self.comboBox_diagram_pdo1_data2.currentText() != 'none':
            self.comboBox_diagram_pdo1_data3.setEnabled(True) 
        else:
            self.comboBox_diagram_pdo1_data3.setEnabled(False)  
            self.comboBox_diagram_pdo1_data4.setEnabled(False)
        pass
    def comboBox_diagram_pdo1_data3_currentIndexChanged(self):
        if self.comboBox_diagram_pdo1_data3.currentText() != 'none':
            self.comboBox_diagram_pdo1_data4.setEnabled(True) 
        else:
            self.comboBox_diagram_pdo1_data4.setEnabled(False)
        pass

    def comboBox_diagram_pdo2_data1_currentIndexChanged(self):
        if self.comboBox_diagram_pdo2_data1.currentText() != 'none':
            self.comboBox_diagram_pdo2_data2.setEnabled(True) 
        else:
            self.comboBox_diagram_pdo2_data2.setEnabled(False) 
            self.comboBox_diagram_pdo2_data3.setEnabled(False)  
            self.comboBox_diagram_pdo2_data4.setEnabled(False)
        pass
    def comboBox_diagram_pdo2_data2_currentIndexChanged(self):
        if self.comboBox_diagram_pdo2_data2.currentText() != 'none':
            self.comboBox_diagram_pdo2_data3.setEnabled(True) 
        else:
            self.comboBox_diagram_pdo2_data3.setEnabled(False)  
            self.comboBox_diagram_pdo2_data4.setEnabled(False)
        pass
    def comboBox_diagram_pdo2_data3_currentIndexChanged(self):
        if self.comboBox_diagram_pdo2_data3.currentText() != 'none':
            self.comboBox_diagram_pdo2_data4.setEnabled(True) 
        else:
            self.comboBox_diagram_pdo2_data4.setEnabled(False)
        pass

    def comboBox_diagram_pdo3_data1_currentIndexChanged(self):
        if self.comboBox_diagram_pdo3_data1.currentText() != 'none':
            self.comboBox_diagram_pdo3_data2.setEnabled(True) 
        else:
            self.comboBox_diagram_pdo3_data2.setEnabled(False) 
            self.comboBox_diagram_pdo3_data3.setEnabled(False)  
            self.comboBox_diagram_pdo3_data4.setEnabled(False)
        pass
    def comboBox_diagram_pdo3_data2_currentIndexChanged(self):
        if self.comboBox_diagram_pdo3_data2.currentText() != 'none':
            self.comboBox_diagram_pdo3_data3.setEnabled(True) 
        else:
            self.comboBox_diagram_pdo3_data3.setEnabled(False)  
            self.comboBox_diagram_pdo3_data4.setEnabled(False)
        pass
    def comboBox_diagram_pdo3_data3_currentIndexChanged(self):
        if self.comboBox_diagram_pdo3_data3.currentText() != 'none':
            self.comboBox_diagram_pdo3_data4.setEnabled(True) 
        else:
            self.comboBox_diagram_pdo3_data4.setEnabled(False)
        pass

    def comboBox_diagram_pdo4_data1_currentIndexChanged(self):
        if self.comboBox_diagram_pdo4_data1.currentText() != 'none':
            self.comboBox_diagram_pdo4_data2.setEnabled(True) 
        else:
            self.comboBox_diagram_pdo4_data2.setEnabled(False) 
            self.comboBox_diagram_pdo4_data3.setEnabled(False)  
            self.comboBox_diagram_pdo4_data4.setEnabled(False)
        pass
    def comboBox_diagram_pdo4_data2_currentIndexChanged(self):
        if self.comboBox_diagram_pdo4_data2.currentText() != 'none':
            self.comboBox_diagram_pdo4_data3.setEnabled(True) 
        else:
            self.comboBox_diagram_pdo4_data3.setEnabled(False)  
            self.comboBox_diagram_pdo4_data4.setEnabled(False)
        pass
    def comboBox_diagram_pdo4_data3_currentIndexChanged(self):
        if self.comboBox_diagram_pdo4_data3.currentText() != 'none':
            self.comboBox_diagram_pdo4_data4.setEnabled(True) 
        else:
            self.comboBox_diagram_pdo4_data4.setEnabled(False)
        pass

    def updateDiagramConfig(self):
        self.mainWindow.updateTpdo1Data1(self.Tpdo1Value1List) 
        self.mainWindow.updateTpdo1Data2(self.Tpdo1Value2List) 
        self.mainWindow.updateTpdo1Data3(self.Tpdo1Value3List) 
        self.mainWindow.updateTpdo1Data4(self.Tpdo1Value4List) 
        self.mainWindow.updateTpdo2Data1(self.Tpdo2Value1List) 
        self.mainWindow.updateTpdo2Data2(self.Tpdo2Value2List) 
        self.mainWindow.updateTpdo2Data3(self.Tpdo2Value3List) 
        self.mainWindow.updateTpdo2Data4(self.Tpdo2Value4List) 
        self.mainWindow.updateTpdo3Data1(self.Tpdo3Value1List) 
        self.mainWindow.updateTpdo3Data2(self.Tpdo3Value2List) 
        self.mainWindow.updateTpdo3Data3(self.Tpdo3Value3List) 
        self.mainWindow.updateTpdo3Data4(self.Tpdo3Value4List) 
        self.mainWindow.updateTpdo4Data1(self.Tpdo4Value1List) 
        self.mainWindow.updateTpdo4Data2(self.Tpdo4Value2List) 
        self.mainWindow.updateTpdo4Data3(self.Tpdo4Value3List) 
        self.mainWindow.updateTpdo4Data4(self.Tpdo4Value4List)  
        pass

                   