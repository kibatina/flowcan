import pyqtgraph as pg
import struct
import shutil
import os
import sys
import time
import array
import csv
import ui_flowconfig
import rwQueue
import globalConstants as gc

from ui_flowconfig import Ui_UI_config
from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray, QTimer, QDate, Qt,QFile
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAbstractItemView, QHeaderView, QTableWidgetItem, QWidget, QMessageBox,QFileDialog
from pyqtgraph import PlotWidget
from PyQt5.QtGui import QFont,QColor,QBrush,QPixmap


class configWindow(QWidget,Ui_UI_config):
    
    def __init__(self,comTransceiver, function, mainwindow, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Config")   
        self.comTransceiver = comTransceiver
        self.function       = function
        self.mainWindow     = mainwindow
        self.cobid_TSDO     = ''
        self.cobid_RSDO     = ''
        self.sdoStatus      = ''
        self.sdoIndex       = ''
        self.sdoSubindex    = ''
        self.sdoData        =''
        self.hwversion      = ''
        self.swversion      = ''
        self.serialNumber   = ''
        self.writeCfgIO = None
        self.writeCfgFileOpened = False
        self.writeCfgFile_FalseNum = 0
        self.readCfgFileOpened = False
        self.readCfgIO  = None
        self.sdoCmdStr = ''
        # 设置信号与槽
        self.CreateSignalSlot()
        self.CreateItems()
        pass   
    def CreateItems(self):
        # Qt 定时器,用于页面的刷新.
        self.timeoutTimer = QTimer(self) #初始化一个定时器
        self.timeoutTimer.timeout.connect(self.timeout)        
    def CreateSignalSlot(self):
        #flow 的8个button
        self.comboBox_flowConfig_baudrate.addItems(['1000','500','250','125','100','50','20','10'])        
        self.comboBox_flowConfig_baudrate.setCurrentIndex(0)    
        self.comboBox_flowConfig_resistor.addItems(['disabled','enabled'])        
        self.comboBox_flowConfig_resistor.setCurrentIndex(0)    
        self.comboBox_flowConfig_nodeid.addItems(gc.listOfNodeid)
        self.comboBox_flowConfig_nodeid.setCurrentIndex(0)  
        self.comboBox_flowConfig_autoBrake.addItems(['disabled','enabled'])  
        self.comboBox_flowConfig_autoBrake.setCurrentIndex(0)  
        self.comboBox_flowConfig_stepdirPosWithoutCanopen.addItems(['disabled','enabled'])  
        self.comboBox_flowConfig_stepdirPosWithoutCanopen.setCurrentIndex(0)  
        self.comboBox_flowConfig_stepdirVelWithoutCanopen.addItems(['disabled','enabled'])  
        self.comboBox_flowConfig_stepdirVelWithoutCanopen.setCurrentIndex(0)  
        self.comboBox_flowConfig_switchType.addItems(['edge','level'])  
        self.comboBox_flowConfig_switchType.setCurrentIndex(0)  
        #self.comboBox_flowConfig_nmtStartup.addItems(['operational','pre-operational'])  
        self.comboBox_flowConfig_specialInputEnable.addItems(['disabled','enabled'])
        self.comboBox_flowConfig_specialInputReverse.addItems(['non-reversed','reversed'])
        self.comboBox_flowConfig_specialOutputEnable.addItems(['disabled','enabled'])
        self.comboBox_flowConfig_specialOutputReverse.addItems(['non-reversed','reversed'])
        self.comboBox_flowConfig_polarity.addItems(['non-reversed','reversed'])   
        self.comboBox_flowConfig_homingMethod.addItems(gc.listOfHomingMethod)
        self.comboBox_flowConfig_homingMethod.setCurrentIndex(30)
        self.pushButton_flowConfig_saveConfig.clicked.connect(self.pushButton_flowConfig_saveConfig_clicked)
        self.pushButton_flowConfig_loadConfig.clicked.connect(self.pushButton_flowConfig_loadConfig_clicked)
        self.pushButton_flowConfig_loadDefaultConfig.clicked.connect(self.pushButton_flowConfig_loadDefaultConfig_clicked) 
        self.pushButton_flowConfig_clearAll.clicked.connect(self.pushButton_flowConfig_clearAll_clicked)  
        self.pushButton_flowConfig_saveConfigToFile.clicked.connect(self.pushButton_flowConfig_saveConfigToFile_clicked)  
        self.pushButton_flowConfig_loadConfigFromFile.clicked.connect(self.pushButton_flowConfig_loadConfigFromFile_clicked)  
        self.comboBox_flowConfig_stepdirPosWithoutCanopen.currentIndexChanged.connect(self.comboBox_flowConfig_stepdirPosWithoutCanopen_currentIndexChanged)
        self.comboBox_flowConfig_stepdirVelWithoutCanopen.currentIndexChanged.connect(self.comboBox_flowConfig_stepdirVelWithoutCanopen_currentIndexChanged)
        self.pushButton_flowConfig_loadConfigFromFile.setEnabled(False)
    def comboBox_flowConfig_stepdirPosWithoutCanopen_currentIndexChanged(self):
        if self.comboBox_flowConfig_stepdirPosWithoutCanopen.currentText() == "enabled":
            self.comboBox_flowConfig_stepdirVelWithoutCanopen.setCurrentIndex(0)
        pass
    def comboBox_flowConfig_stepdirVelWithoutCanopen_currentIndexChanged(self):
        if self.comboBox_flowConfig_stepdirVelWithoutCanopen.currentText() == "enabled":
            self.comboBox_flowConfig_stepdirPosWithoutCanopen.setCurrentIndex(0)
        pass
    #flow config的save config 按钮被按下
    def pushButton_flowConfig_saveConfig_clicked(self):
        decNodeid = self.mainWindow.getDecNodeid()
        self.cobid_TSDO = (str(hex(decNodeid+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
        self.cobid_RSDO = (str(hex(decNodeid+gc.cobid_RSDO)).replace('0x','')).zfill(3).upper()
        saveStatus = True        
        #time+cobid+length+data,lengtH=len(data)  
        #nmt startup,1F80,4byte
        #nmtStartup = self.comboBox_flowConfig_nmtStartup.currentText()  
        #if nmtStartup == 'operational':
            #self.function.decStrToHexBytes('08',4)    
        #else:
            #self.function.decStrToHexBytes('00',4)                 
        #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeNMTStartup+self.function.getSdoDataStr()])  
        #nodeid,2001:01,1byte
        nodeid = str(hex(int(self.comboBox_flowConfig_nodeid.currentText(),10)).replace('0x','')).zfill(2).upper()
        self.function.hexStrToHexBytes(nodeid)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeCanopenConfigCanNodeid+self.function.getSdoDataStr()]) 
        #baudrate of can,2001:02,2byte
        baudrate = self.comboBox_flowConfig_baudrate.currentText()    
        self.function.decStrToHexBytes(baudrate,2)        
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeCanopenConfigCanBitrate+self.function.getSdoDataStr()]) 
        #120 resistor,2001:03,1byte
        resistor = self.comboBox_flowConfig_resistor.currentText()   
        if resistor == 'enabled':
            self.function.decStrToHexBytes('01',1)    
        else:
            self.function.decStrToHexBytes('00',1)                 
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeCanopenConfigEnResistor+self.function.getSdoDataStr()])          
        #pulse per resolution,2003:01,4byte 
        pulsePerResolution = self.lineEdit_flowConfig_pulsePerResolution.text()
        if pulsePerResolution.isdecimal():
            self.function.decStrToHexBytes(pulsePerResolution,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeCprCountPerResolution+self.function.getSdoDataStr()])           
        else:
            QMessageBox.warning(self,"Error","pulsePerResolution, Wrong Input") 
            saveStatus = False  
        #current kp,2010:03,4byte
        currentKp = self.lineEdit_flowConfig_currentKp.text()
        if currentKp.isdecimal():      
            self.function.decStrToHexBytes(currentKp,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePidIqKpGain_S+self.function.getSdoDataStr()])
        else:
            QMessageBox.warning(self,"Error","currentKp, Wrong Input") 
            saveStatus = False  
        #current ki,2010:04,4byte
        currentKi = self.lineEdit_flowConfig_currentKi.text()
        if currentKi.isdecimal():    
            self.function.decStrToHexBytes(currentKi,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePidIqKiGain_S+self.function.getSdoDataStr()]) 
        else:
            QMessageBox.warning(self,"Error","currentKi, Wrong Input")  
            saveStatus = False 
        #velocity kp,2012:03,4byte
        velocityKp = self.lineEdit_flowConfig_velocityKp.text()
        if velocityKp.isdecimal():   
            self.function.decStrToHexBytes(velocityKp,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePidVelocityKpGain_S+self.function.getSdoDataStr()]) 
        else:
            QMessageBox.warning(self,"Error","velocityKp, Wrong Input")  
            saveStatus = False 
        #velocity ki,2012:04,4byte
        velocityKi = self.lineEdit_flowConfig_velocityKi.text()
        if velocityKi.isdecimal():  
            self.function.decStrToHexBytes(velocityKi,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePidVelocityKiGain_S+self.function.getSdoDataStr()])
        else:
            QMessageBox.warning(self,"Error","velocityKi, Wrong Input") 
            saveStatus = False 
        #velocity stiffness,2012:05,4byte
        velocityStiffness = self.lineEdit_flowConfig_velocityStiffness.text()
        if velocityStiffness.isdecimal():  
            self.function.decStrToHexBytes(velocityStiffness,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePidVelocityStiffness+self.function.getSdoDataStr()])
        else:
            QMessageBox.warning(self,"Error","velocityStiffness, Wrong Input") 
            saveStatus = False 
        #position kp,2013:02,4byte
        positionKp = self.lineEdit_flowConfig_positionKp.text()
        if positionKp.isdecimal():   
            self.function.decStrToHexBytes(positionKp,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePidPositionKpGain_S+self.function.getSdoDataStr()])
        else:
            QMessageBox.warning(self,"Error","positionKp, Wrong Input") 
            saveStatus = False 
        #2014 auto brake
        autoBrake = self.comboBox_flowConfig_autoBrake.currentText()   
        if autoBrake == 'enabled':
            self.function.decStrToHexBytes('01',1)    
        else:
            self.function.decStrToHexBytes('00',1)                 
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeBrakeRelatedAutoBrake+self.function.getSdoDataStr()])
        #2015 
        #2015:05 stepdir position
        stepdirPosWithoutCanopen = self.comboBox_flowConfig_stepdirPosWithoutCanopen.currentText()   
        if stepdirPosWithoutCanopen == 'enabled':
            self.function.decStrToHexBytes('01',1)    
        else:
            self.function.decStrToHexBytes('00',1)                 
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeControlStrategyStepdirPosWithoutCanopen+self.function.getSdoDataStr()])         
        #2015:06 stepdir velocity
        stepdirVelWithoutCanopen = self.comboBox_flowConfig_stepdirVelWithoutCanopen.currentText()   
        if stepdirVelWithoutCanopen == 'enabled':
            self.function.decStrToHexBytes('01',1)    
        else:
            self.function.decStrToHexBytes('00',1)                 
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeControlStrategyStepdirVelWithoutCanopen+self.function.getSdoDataStr()])         
        #2016 filter
        #velocity filter bandwidth,2016:01,4byte
        velocityFilterBandwidth = self.lineEdit_flowConfig_velocityFilterBandwidth.text()
        if velocityFilterBandwidth.isdecimal():   
            self.function.decStrToHexBytes(velocityFilterBandwidth,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeVelocityFilterBandwith+self.function.getSdoDataStr()])
        else:
            QMessageBox.warning(self,"Error","velocityFilterBandwidth, Wrong Input") 
            saveStatus = False 
        #torque window,2030,4byte
        torqueWindow = self.lineEdit_flowConfig_torqueWindow.text()
        if torqueWindow.isdecimal():
            self.function.decStrToHexBytes(torqueWindow,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeTorqueWindow+self.function.getSdoDataStr()])        
        else:
            QMessageBox.warning(self,"Error","torqueWindow, Wrong Input") 
            saveStatus = False 
        #2017 IIT
        #iit limit 2017:01
        iitLimit = self.lineEdit_flowConfig_iitLimit.text()
        if iitLimit.isdecimal():
            self.function.decStrToHexBytes(iitLimit,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeIitlimit+self.function.getSdoDataStr()])        
        else:
            QMessageBox.warning(self,"Error","iit limit, Wrong Input") 
            saveStatus = False 
        #iit trig level 2017:03
        iitTrigLevel = self.lineEdit_flowConfig_iitTrigLevel.text()
        if iitTrigLevel.isdecimal():
            self.function.decStrToHexBytes(iitTrigLevel,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeIitTrigLevel+self.function.getSdoDataStr()])        
        else:
            QMessageBox.warning(self,"Error","iit trig level, Wrong Input") 
            saveStatus = False 
        #torque window timeout,2031,2byte
        torqueWindowTimeout = self.lineEdit_flowConfig_torqueWindowTimeout.text()
        if torqueWindowTimeout.isdecimal():  
            self.function.decStrToHexBytes(torqueWindowTimeout,2)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeTorqueWindowTimeout+self.function.getSdoDataStr()])           
        else:
            QMessageBox.warning(self,"Error","torqueWindowTimeout, Wrong Input") 
            saveStatus = False 
        #2034,4byte, internal target reach window
        internalTrWindow = self.lineEdit_flowConfig_internalTargetReachWindow.text()
        if internalTrWindow.isdecimal():  
            self.function.decStrToHexBytes(internalTrWindow,2)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeInternalTargetReachWindow+self.function.getSdoDataStr()])           
        else:
            QMessageBox.warning(self,"Error","internalTrWindow, Wrong Input") 
            saveStatus = False 
        #block trigger current,203A:01,4byte,这个数据可正可负,也就是可能有负号
        blockTriggerCurrent = self.lineEdit_flowConfig_blockTriggerCurrent.text()
        self.function.decStrToHexBytes(blockTriggerCurrent,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeBlockTriggerCurrent+self.function.getSdoDataStr()]) 
        #block duration,203A:02,2byte
        blockDuration = self.lineEdit_flowConfig_blockDuration.text()
        if blockDuration.isdecimal():  
            self.function.decStrToHexBytes(blockDuration,2)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeBlockDuration+self.function.getSdoDataStr()])           
        else:
            QMessageBox.warning(self,"Error","blockDuration, Wrong Input") 
            saveStatus = False    
        #203B,switch
        #203B:01, switch type
        switchType = self.comboBox_flowConfig_switchType.currentText()   
        if switchType == 'edge':
            self.function.decStrToHexBytes('00',4)    
        else:   #level
            self.function.decStrToHexBytes('07',4)                 
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeSwitchType+self.function.getSdoDataStr()])
        #special input enable,2240:01,4byte
            #一次性enable或者disable 3个输入,不支持单个控制. 3个输入分别为NLS, PLS,HS
        specialInputEnable = self.comboBox_flowConfig_specialInputEnable.currentText()   
        if specialInputEnable == 'enabled':
            self.function.hexStrToHexBytes('07')    
        else:
            self.function.hexStrToHexBytes('00')                 
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeSpecialInputEnable+self.function.getSdoDataStr()])          
        #special input reverse,2240:02,4byte
        specialInputReverse = self.comboBox_flowConfig_specialInputReverse.currentText()   
        if specialInputReverse == 'non-reversed':
            self.function.hexStrToHexBytes('00')    
        else:
            self.function.hexStrToHexBytes('07')                 
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeSpecialInputReverse+self.function.getSdoDataStr()])      
        #special output enable,2250:01,4byte
            #输出只有1路
        specialOutputEnable = self.comboBox_flowConfig_specialOutputEnable.currentText()   
        if specialOutputEnable == 'enabled':
            self.function.hexStrToHexBytes('01')    
        else:
            self.function.hexStrToHexBytes('00')                 
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeSpecialOutputEnable+self.function.getSdoDataStr()])          
        #special output reverse,2250:02,4byte
        specialOutputReverse = self.comboBox_flowConfig_specialOutputReverse.currentText()   
        if specialOutputReverse == 'non-reversed':
            self.function.hexStrToHexBytes('00')    
        else:
            self.function.hexStrToHexBytes('01')                 
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeSpecialOutputReverse+self.function.getSdoDataStr()])   
        #following error window,6065,4byte
        followingErrorWindow = self.lineEdit_flowConfig_followingErrorWindow.text()
        if followingErrorWindow.isdecimal():   
            self.function.decStrToHexBytes(followingErrorWindow,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeFollowingErrorWindow+self.function.getSdoDataStr()])   
        else:
            QMessageBox.warning(self,"Error","followingErrorWindow, Wrong Input") 
            saveStatus = False 
        #following error timeout,2byte
        followingErrorTimeout = self.lineEdit_flowConfig_followingErrorTimeout.text()
        if followingErrorTimeout.isdecimal():
            self.function.decStrToHexBytes(followingErrorTimeout,2)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeFollowingErrorTimeout+self.function.getSdoDataStr()])   
        else:
            QMessageBox.warning(self,"Error","followingErrorTimeout, Wrong Input") 
            saveStatus = False    
        #position window, 6067,4byte
        positionWindow = self.lineEdit_flowConfig_positionWindow.text()
        if positionWindow.isdecimal():    
            self.function.decStrToHexBytes(positionWindow,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePositionWindow+self.function.getSdoDataStr()])  
        else:
            QMessageBox.warning(self,"Error","positionWindow, Wrong Input") 
            saveStatus = False 
        #position window time,6068,4byte
        positionWindowTime = self.lineEdit_flowConfig_positionWindowTime.text()
        if positionWindowTime.isdecimal():      
            self.function.decStrToHexBytes(positionWindowTime,2)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePositionWindowTime+self.function.getSdoDataStr()])   
        else:
            QMessageBox.warning(self,"Error","positionWindowTime, Wrong Input") 
            saveStatus = False 
        #max torque,6072,2byte
        maxTorque = self.lineEdit_flowConfig_maxTorque.text()
        if maxTorque.isdecimal():      
            self.function.decStrToHexBytes(maxTorque,2)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeMaxTorque+self.function.getSdoDataStr()])   
        else:
            QMessageBox.warning(self,"Error","maxTorque, Wrong Input") 
            saveStatus = False 
        #home offset,607C,4byte
        homeOffset = self.lineEdit_flowConfig_homeOffset.text()
        self.function.decStrToHexBytes(homeOffset,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeHomeOffset+self.function.getSdoDataStr()])   
        #min position limit,607D:01,4byte
        minPositionLimit = self.lineEdit_flowConfig_minPositionLimit.text()
        self.function.decStrToHexBytes(minPositionLimit,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeMinPositionLimit+self.function.getSdoDataStr()]) 
        #max position limit,607D:02,4byte
        maxPositionLimit = self.lineEdit_flowConfig_maxPositionLimit.text()
        self.function.decStrToHexBytes(maxPositionLimit,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeMaxPositionLimit+self.function.getSdoDataStr()]) 
        #polarity,607E,1byte
        polrity = self.comboBox_flowConfig_polarity.currentText()   
        if polrity == 'non-reversed':
            self.function.hexStrToHexBytes('00')    
        else:
            self.function.hexStrToHexBytes('E0')                 
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePolarity+self.function.getSdoDataStr()])          
        #max profile velocity,607F,4byte
        maxProfileVelocity = self.lineEdit_flowConfig_maxProfileVelocity.text()
        if maxProfileVelocity.isdecimal():   
            self.function.decStrToHexBytes(maxProfileVelocity,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeMaxProfileVelocity+self.function.getSdoDataStr()])   
        else:
            QMessageBox.warning(self,"Error","maxProfileVelocity, Wrong Input") 
            saveStatus = False 
        #max acceleration,60C5,4byte, 这几个要先于6083/6084配置.
        maxAcceleration = self.lineEdit_flowConfig_maxAcceleration.text()
        if maxAcceleration.isdecimal():
            self.function.decStrToHexBytes(maxAcceleration,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeMaxAcceleration+self.function.getSdoDataStr()])   
        else:
            QMessageBox.warning(self,"Error","maxAcceleration, Wrong Input") 
            saveStatus = False 
        #max deceleration,60c6,4byte, 这几个要先于6083/6084配置.
        maxDeceleration = self.lineEdit_flowConfig_maxDeceleration.text()
        if maxDeceleration.isdecimal():
            self.function.decStrToHexBytes(maxDeceleration,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeMaxDeceleration+self.function.getSdoDataStr()])         
        else:
            QMessageBox.warning(self,"Error","maxDeceleration, Wrong Input") 
            saveStatus = False 
        #profile acceleration,6083,4byte
        profileAcceleration = self.lineEdit_flowConfig_profileAcceleration.text()
        if profileAcceleration.isdecimal():      
            self.function.decStrToHexBytes(profileAcceleration,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeProfileAcceleration+self.function.getSdoDataStr()]) 
        else:
            QMessageBox.warning(self,"Error","profileAcceleration, Wrong Input") 
            saveStatus = False 
        #profile deceleration,6084,4byte
        profileDeceleration = self.lineEdit_flowConfig_profileDeceleration.text()
        if profileDeceleration.isdecimal():     
            self.function.decStrToHexBytes(profileDeceleration,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeProfileDeceleration+self.function.getSdoDataStr()])  
        else:
            QMessageBox.warning(self,"Error","profileDeceleration, Wrong Input") 
            saveStatus = False 
        #quickstop deceleration,6085,4byte
        quickstopDeceleration = self.lineEdit_flowConfig_quickstopDeceleration.text()
        if quickstopDeceleration.isdecimal():      
            self.function.decStrToHexBytes(quickstopDeceleration,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeQuickstopDeceleration+self.function.getSdoDataStr()])    
        else:
            QMessageBox.warning(self,"Error","quickstopDeceleration, Wrong Input") 
            saveStatus = False 
        #torque slope,6087,4byte
        torqueSlope = self.lineEdit_flowConfig_torqueSlope.text()
        if torqueSlope.isdecimal():     
            self.function.decStrToHexBytes(torqueSlope,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeTorqueSlope+self.function.getSdoDataStr()])          
        else:
            QMessageBox.warning(self,"Error","torqueSlope, Wrong Input") 
            saveStatus = False 
        #position factor numerator,6093:01,4byte
        positionFactorNumerator = self.lineEdit_flowConfig_positionFactorNumerator.text()
        if positionFactorNumerator.isdecimal():      
            self.function.decStrToHexBytes(positionFactorNumerator,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePositionFactorNumerator+self.function.getSdoDataStr()])   
        else:
            QMessageBox.warning(self,"Error","positionFactorNumerator, Wrong Input") 
            saveStatus = False 
        #position factor divisor,6093:02,4byte
        positionFactorDivisor = self.lineEdit_flowConfig_positionFactorDivisor.text()
        if positionFactorDivisor.isdecimal():    
            self.function.decStrToHexBytes(positionFactorDivisor,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePositionFactorDivisor+self.function.getSdoDataStr()]) 
        else:
            QMessageBox.warning(self,"Error","positionFactorDivisor, Wrong Input") 
            saveStatus = False 
        #velocity factor numerator,6095:01,4byte
        velocityFactorNumerator = self.lineEdit_flowConfig_velocityFactorNumerator.text()
        if velocityFactorNumerator.isdecimal():      
            self.function.decStrToHexBytes(velocityFactorNumerator,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeVelocityFactorNumerator+self.function.getSdoDataStr()])  
        else:
            QMessageBox.warning(self,"Error","velocityFactorNumerator, Wrong Input") 
            saveStatus = False 
        #velocity factor divisor,6095:02,4byte
        velocityFactorDivisor = self.lineEdit_flowConfig_velocityFactorDivisor.text()
        if velocityFactorDivisor.isdecimal():      
            self.function.decStrToHexBytes(velocityFactorDivisor,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeVelocityFactorDivisor+self.function.getSdoDataStr()])  
        else:
            QMessageBox.warning(self,"Error","velocityFactorDivisor, Wrong Input") 
            saveStatus = False 
        #acceleration factor numerator,6097:01,4byte
        accelerationFactorNumerator = self.lineEdit_flowConfig_accelerationFactorNumerator.text()
        if accelerationFactorNumerator.isdecimal():    
            self.function.decStrToHexBytes(accelerationFactorNumerator,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeAccelerationFactorNumerator+self.function.getSdoDataStr()]) 
        else:
            QMessageBox.warning(self,"Error","accelerationFactorNumerator, Wrong Input") 
            saveStatus = False 
        #acceleration factor divisor,6097:02,4byte
        accelerationFactorDivisor = self.lineEdit_flowConfig_accelerationFactorDivisor.text()
        if accelerationFactorDivisor.isdecimal():      
            self.function.decStrToHexBytes(accelerationFactorDivisor,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeAccelerationFactorDivisor+self.function.getSdoDataStr()]) 
        else:
            QMessageBox.warning(self,"Error","accelerationFactorDivisor, Wrong Input") 
            saveStatus = False 
        #homing method,6098,1byte
        homingMethod = self.comboBox_flowConfig_homingMethod.currentText()    
        self.function.decStrToHexBytes(homingMethod,1)        
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeHomingMethod+self.function.getSdoDataStr()]) 
        #homing speed1 ,6099,4byte
        homeingSpeed1 = self.lineEdit_flowConfig_homingSpeed1.text()
        if homeingSpeed1.isdecimal():      
            self.function.decStrToHexBytes(homeingSpeed1,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeHomingSpeed1+self.function.getSdoDataStr()]) 
        else:
            QMessageBox.warning(self,"Error","homing speed1, Wrong Input") 
            saveStatus = False 
        #homing speed2 ,6099,4byte
        homeingSpeed2 = self.lineEdit_flowConfig_homingSpeed2.text()
        if homeingSpeed2.isdecimal():      
            self.function.decStrToHexBytes(homeingSpeed2,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeHomingSpeed2+self.function.getSdoDataStr()]) 
        else:
            QMessageBox.warning(self,"Error","homing speed1, Wrong Input") 
            saveStatus = False     
        #homing acceleration ,609A,4byte
        homeingAcceleration = self.lineEdit_flowConfig_homingAcceleration.text()
        if homeingAcceleration.isdecimal():      
            self.function.decStrToHexBytes(homeingAcceleration,4)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeHomingAcceleraiton+self.function.getSdoDataStr()]) 
        else:
            QMessageBox.warning(self,"Error","homing speed1, Wrong Input") 
            saveStatus = False  
        #store parameters,store config
        if saveStatus == True:
            self.function.hexStrToHexBytes('65766173')   #save的ASCII
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeStoreParameterSaveConfig+self.function.getSdoDataStr()])  
        pass
    
    #canopen的load config 按钮被按下
    def pushButton_flowConfig_loadConfig_clicked(self):
        decNodeid = self.mainWindow.getDecNodeid()
        self.cobid_TSDO = (str(hex(decNodeid+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
        self.cobid_RSDO = (str(hex(decNodeid+gc.cobid_RSDO)).replace('0x','')).zfill(3).upper()
        #time+cobid+length+data,lengtH=len(data)  
        #hardware version,1009,4byte
        self.function.decStrToHexBytes('0',4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureHardwareVersionByte1+self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureHardwareVersionByte2+self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureHardwareVersionByte3+self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureHardwareVersionByte4+self.function.getSdoDataStr()])
        #software version,100A,4byte
        self.function.decStrToHexBytes('0',4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureSoftwareVersionByte1+self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureSoftwareVersionByte2+self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureSoftwareVersionByte3+self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureSoftwareVersionByte4+self.function.getSdoDataStr()])
        #serial number,1018:04,4byte
        self.function.decStrToHexBytes('0',4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readIdentitySerialNumber+self.function.getSdoDataStr()])     
        #nmt startup,1F80,4byte
        #self.function.decStrToHexBytes('0',4)   
        #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readNMTStartup+self.function.getSdoDataStr()])
        #nodeid,2001:01,1byte
        self.function.decStrToHexBytes('0',1)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readCanopenConfigCanNodeid+self.function.getSdoDataStr()])
        #baudrate of can,2001:02,2byte
        self.function.decStrToHexBytes('0',2)         
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readCanopenConfigCanBitrate+self.function.getSdoDataStr()])  
        #120 resistor,2001:03,1byte
        self.function.decStrToHexBytes('0',1)                
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readCanopenConfigEnResistor+self.function.getSdoDataStr()])           
        #pulse per resolution,2003:01,4byte 
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readCprCountPerResolution+self.function.getSdoDataStr()])            
        #current kp,2010:03,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readPidIqKpGain_S+self.function.getSdoDataStr()]) 
        #current ki,2010:04,4byte
        self.function.decStrToHexBytes('0',4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readPidIqKiGain_S+self.function.getSdoDataStr()])  
        #velocity kp,2012:03,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readPidVelocityKpGain_S+self.function.getSdoDataStr()])  
        #velocity ki,2012:04,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readPidVelocityKiGain_S+self.function.getSdoDataStr()])  
        #velocity stiffness,2012:05,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readPidVelocityStiffness+self.function.getSdoDataStr()])  
        #position kp,2013:02,4byte
        self.function.decStrToHexBytes('0',4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readPidPositionKpGain_S+self.function.getSdoDataStr()])  
        #brake related,2014:04,1byte
        self.function.decStrToHexBytes('0',1)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readBrakeRelatedAutoBrake+self.function.getSdoDataStr()])  
        #control strategy,2015:05,1byte
        self.function.decStrToHexBytes('0',1)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readControlStrategyStepdirPosWithoutCanopen+self.function.getSdoDataStr()])  
        self.function.decStrToHexBytes('0',1)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readControlStrategyStepdirVelWithoutCanopen+self.function.getSdoDataStr()])  
        #velocity filter bandwidth,2016:01,4byte
        self.function.decStrToHexBytes('0',4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readVelocityFilterBandwith+self.function.getSdoDataStr()])
        #iit limit,2017:01,4byte
        self.function.decStrToHexBytes('0',4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readIitLimit+self.function.getSdoDataStr()])
        #iit trig level,2017:03,4byte
        self.function.decStrToHexBytes('0',4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readIitTrigLevel+self.function.getSdoDataStr()])
        #torque window,2030,4byte
        self.function.decStrToHexBytes('0',4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readTorqueWindow+self.function.getSdoDataStr()])          
        #torque window timeout,2031,2byte
        self.function.decStrToHexBytes('0',2)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readTorqueWindowTimeout+self.function.getSdoDataStr()])   
        #internal target reach window,2034,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readInternalTargetReachWindow+self.function.getSdoDataStr()])              
        #block trigger current 203A:01 
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readBlockTriggerCurrent+self.function.getSdoDataStr()])             
        #block duration 203A:02
        self.function.decStrToHexBytes('0',2)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readBlockDuration+self.function.getSdoDataStr()]) 
        #switch type 203B:01
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readSwitchType+self.function.getSdoDataStr()]) 
        #special input  enable 2240:01,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readSpecialInputEnable+self.function.getSdoDataStr()]) 
        #sepcial input reverse 2240:02,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readSpecialInputReverse+self.function.getSdoDataStr()])  
        #special output enable 2250:01,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readSpecialOutputEnable+self.function.getSdoDataStr()]) 
        #sepcial output reverse 2250:02,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readSpecialOutputReverse+self.function.getSdoDataStr()])      
        #following error window,6065,4byte
        self.function.decStrToHexBytes('0',4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readFollowingErrorWindow+self.function.getSdoDataStr()])      
        #following error timeout,6066,
        self.function.decStrToHexBytes('0',2)      
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readFollowingErrorTimeout+self.function.getSdoDataStr()])  
        #position window, 6067,4byte
        self.function.decStrToHexBytes('0',4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readPositionWindow+self.function.getSdoDataStr()]) 
        #position window time,6068,2byte
        self.function.decStrToHexBytes('0',2)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readPositionWindowTime+self.function.getSdoDataStr()])  
        #max torque,6072,2byte
        self.function.decStrToHexBytes('0',2)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readMaxTorque+self.function.getSdoDataStr()])  
        #home offset,607C,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readHomeOffset+self.function.getSdoDataStr()])  
        #software position limit,607D,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readMinPositionLimit+self.function.getSdoDataStr()])  
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readMaxPositionLimit+self.function.getSdoDataStr()])  
        #polarity,607E,1byte
        self.function.decStrToHexBytes('0',1)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readPolarity+self.function.getSdoDataStr()])  
        #max profile velocity,607F,4byte
        self.function.decStrToHexBytes('0',4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readMaxProfileVelocity+self.function.getSdoDataStr()]) 
        #max acceleration,60C5,4byte, 这几个要先于6083/6084配置.
        self.function.decStrToHexBytes('0',4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readMaxAcceleration+self.function.getSdoDataStr()])  
        #max deceleration,60C6,4byte, 这几个要先于6083/6084配置.
        self.function.decStrToHexBytes('0',4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readMaxDeceleration+self.function.getSdoDataStr()])         
        #profile acceleration,6083,4byte
        self.function.decStrToHexBytes('0',4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readProfileAcceleration+self.function.getSdoDataStr()])  
        #profile deceleration,6084,4byte
        self.function.decStrToHexBytes('0',4)      
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readProfileDeceleration+self.function.getSdoDataStr()])  
        #quickstop deceleration,6085,4byte
        self.function.decStrToHexBytes('0',4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readQuickstopDeceleration+self.function.getSdoDataStr()])  
        #torque slope,6087,4byte
        self.function.decStrToHexBytes('0',4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readTorqueSlope+self.function.getSdoDataStr()])         
        #position factor numerator,6093:01,4byte
        self.function.decStrToHexBytes('0',4)      
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readPositionFactorNumerator+self.function.getSdoDataStr()])  
        #position factor divisor,6093:02,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readPositionFactorDivisor+self.function.getSdoDataStr()])   
        #velocity factor numerator,6095:01,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readVelocityFactorNumerator+self.function.getSdoDataStr()])   
        #velocity factor divisor,6095:02,4byte
        self.function.decStrToHexBytes('0',4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readVelocityFactorDivisor+self.function.getSdoDataStr()]) 
        #acceleration factor numerator,6097:01,4byte
        self.function.decStrToHexBytes('0',4)      
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readAccelerationFactorNumerator+self.function.getSdoDataStr()]) 
        #acceleration factor divisor,6097:02,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readAccelerationFactorDivisor+self.function.getSdoDataStr()]) 
        #homing method,6098,1byte
        self.function.decStrToHexBytes('0',1)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readHomingMethod+self.function.getSdoDataStr()]) 
        #homing speed1,6099:01,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readHomingSpeed1+self.function.getSdoDataStr()]) 
        #homing speed2,6099:02,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readHomingSpeed2+self.function.getSdoDataStr()]) 
        #homing acceleration,609A,4byte
        self.function.decStrToHexBytes('0',4)    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readHomingAcceleration+self.function.getSdoDataStr()]) 
        #打开存配置到伺服的按钮。
        self.pushButton_flowConfig_loadConfigFromFile.setEnabled(True)
        pass

    #canopen的restore parameters restore config 按钮被按下
    def pushButton_flowConfig_loadDefaultConfig_clicked(self):
        decNodeid = self.mainWindow.getDecNodeid()
        self.cobid_TSDO = (str(hex(decNodeid+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
        self.cobid_RSDO = (str(hex(decNodeid+gc.cobid_RSDO)).replace('0x','')).zfill(3).upper()
        #load default config
        self.function.hexStrToHexBytes('64616F6C')   #load的ASCII
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeRestoreParameterConfig+self.function.getSdoDataStr()])   
        pass
    def pushButton_flowConfig_clearAll_clicked(self):
        self.lineEdit_flowConfig_hardwareVersion.setText('') 
        self.lineEdit_flowConfig_softwareVersion.setText('')
        self.lineEdit_flowConfig_serialNumber.setText('')
        self.comboBox_flowConfig_nodeid.setCurrentIndex(0)
        self.comboBox_flowConfig_baudrate.setCurrentIndex(0)
        self.comboBox_flowConfig_resistor.setCurrentIndex(0)
        #self.comboBox_flowConfig_nmtStartup.setCurrentIndex(0)
        self.lineEdit_flowConfig_pulsePerResolution.setText('')
        self.lineEdit_flowConfig_currentKp.setText('')
        self.lineEdit_flowConfig_currentKi.setText('')
        self.lineEdit_flowConfig_velocityKp.setText('')
        self.lineEdit_flowConfig_velocityKi.setText('')
        self.lineEdit_flowConfig_velocityStiffness.setText('')
        self.lineEdit_flowConfig_positionKp.setText('')
        self.comboBox_flowConfig_autoBrake.setCurrentIndex(0)
        self.comboBox_flowConfig_stepdirPosWithoutCanopen.setCurrentIndex(0)
        self.comboBox_flowConfig_stepdirVelWithoutCanopen.setCurrentIndex(0)
        self.lineEdit_flowConfig_velocityFilterBandwidth.setText('')
        self.lineEdit_flowConfig_iitLimit.setText('')
        self.lineEdit_flowConfig_iitTrigLevel.setText('')
        self.lineEdit_flowConfig_torqueWindow.setText('')
        self.lineEdit_flowConfig_torqueWindowTimeout.setText('')
        self.lineEdit_flowConfig_internalTargetReachWindow.setText('')
        self.lineEdit_flowConfig_blockTriggerCurrent.setText('')
        self.lineEdit_flowConfig_blockDuration.setText('')
        self.comboBox_flowConfig_switchType.setCurrentIndex(0)
        self.comboBox_flowConfig_specialInputEnable.setCurrentIndex(0)
        self.comboBox_flowConfig_specialInputReverse.setCurrentIndex(0)
        self.comboBox_flowConfig_specialOutputEnable.setCurrentIndex(0)
        self.comboBox_flowConfig_specialOutputReverse.setCurrentIndex(0)
        self.lineEdit_flowConfig_followingErrorWindow.setText('')
        self.lineEdit_flowConfig_followingErrorTimeout.setText('')
        self.lineEdit_flowConfig_positionWindow.setText('')
        self.lineEdit_flowConfig_positionWindowTime.setText('')
        self.lineEdit_flowConfig_maxTorque.setText('')
        self.lineEdit_flowConfig_homeOffset.setText('')
        self.lineEdit_flowConfig_minPositionLimit.setText('')
        self.lineEdit_flowConfig_maxPositionLimit.setText('')
        self.comboBox_flowConfig_polarity.setCurrentIndex(0)
        self.lineEdit_flowConfig_maxProfileVelocity.setText('')
        self.lineEdit_flowConfig_profileAcceleration.setText('')
        self.lineEdit_flowConfig_profileDeceleration.setText('')
        self.lineEdit_flowConfig_quickstopDeceleration.setText('')
        self.lineEdit_flowConfig_torqueSlope.setText('')
        self.lineEdit_flowConfig_positionFactorNumerator.setText('')
        self.lineEdit_flowConfig_positionFactorDivisor.setText('')
        self.lineEdit_flowConfig_velocityFactorNumerator.setText('')
        self.lineEdit_flowConfig_velocityFactorDivisor.setText('')
        self.lineEdit_flowConfig_accelerationFactorNumerator.setText('')
        self.lineEdit_flowConfig_accelerationFactorDivisor.setText('')
        self.comboBox_flowConfig_homingMethod.setCurrentIndex(30)
        self.lineEdit_flowConfig_homingSpeed1.setText('')
        self.lineEdit_flowConfig_homingSpeed2.setText('')
        self.lineEdit_flowConfig_homingAcceleration.setText('')
        self.lineEdit_flowConfig_maxAcceleration.setText('')
        self.lineEdit_flowConfig_maxDeceleration.setText('')
        pass
    def listToSdoReadCmd(self,array):
        indexStr = array[gc.eepromListSubindexOfIndex][2:4]+array[gc.eepromListSubindexOfIndex][0:2]
        subIndexStr = array[gc.eepromListSubindexOfSubindex]
        cmdStr = '40'
        self.sdoCmdStr = cmdStr+indexStr+subIndexStr
        pass
    def writeCfgToFile(self):
        if self.writeCfgFileOpened == True:
            timestr = time.strftime("%Y%m%d%H%M%S")
            title = 'Config from '+str(self.serialNumber)+', hardware version= '+self.lineEdit_flowConfig_hardwareVersion.text()+', software version= '+self.lineEdit_flowConfig_softwareVersion.text()+', at time= '+timestr
            self.writeCfgIO.write(title)
            self.writeCfgIO.write('\r')
            title = 'Nodeid，current pid\'s valid status is set to False on purpose, if you want to change nodeid,  change status manualy.'
            self.writeCfgIO.write(title)
            self.writeCfgIO.write('\r')
            if self.writeCfgFile_FalseNum != 0:
                title = 'WARNING !!!,except nodeid, there are still '
                self.writeCfgIO.write(title)
                self.writeCfgIO.write(str(self.writeCfgFile_FalseNum))
                title = ' config\'s valid status is False, these False config will not be write back.'
                self.writeCfgIO.write(title)
                self.writeCfgIO.write('\r')
            title = 'when write back, only line with valid==True will be write back.'
            self.writeCfgIO.write(title)
            self.writeCfgIO.write('\r')
            title = 'except column valid, user should not change other column.'
            self.writeCfgIO.write(title)
            self.writeCfgIO.write('\r')
            self.writeCfgIO.write('\r')
            self.writeCfgIO.write('\r')
            tplt = "{:<40}\t{:<5}\t{:<5}\t{:<5}\t{:<5}\t{:<10}"
            self.writeCfgIO.write(tplt.format('NAME','INDEX','SUB','LEN','VALID','VALUE'))
            self.writeCfgIO.write('\r')
            for index in range(len(gc.eepromList)):
                #'name','index','sub','len','valid','value
                self.writeCfgIO.write(tplt.format(gc.eepromList[index][gc.eepromListSubindexOfName],\
                                                  gc.eepromList[index][gc.eepromListSubindexOfIndex],\
                                                  gc.eepromList[index][gc.eepromListSubindexOfSubindex],\
                                                  str(gc.eepromList[index][gc.eepromListSubindexOfLen]),\
                                                  gc.eepromList[index][gc.eepromListSubindexOfValid],\
                                                  str(gc.eepromList[index][gc.eepromListSubindexOfData])))
                self.writeCfgIO.write('\r')
            self.writeCfgIO.close()
            self.writeCfgFileOpened = False   
            self.pushButton_flowConfig_saveConfigToFile.setEnabled(True)
            #保存临时文件到特定地方，指定文件名
            cfgname = QFileDialog.getSaveFileName(self, "Save Config File", self.lineEdit_flowConfig_hardwareVersion.text()+".cfg",  "cfg (*.cfg)")
            #拷贝文件
            shutil.copyfile('temp.cfg',cfgname[0])
            #删除临时文件。
            os.remove('temp.cfg')
        pass
    def writeCfgToServo(self,cfgList):
        writeCmdStr = ''
        if cfgList[3] == '1':
            writeCmdStr = '2F'
        elif cfgList[3] == '2':
            writeCmdStr = '2B'
        elif cfgList[3] == '3':
            writeCmdStr = '27'
        elif cfgList[3] == '4':
            writeCmdStr = '23'
        writeCmdStr += cfgList[1][2:4]+cfgList[1][0:2]
        writeCmdStr += cfgList[2]
        if cfgList[4] == 'True':
            self.function.decStrToHexBytes(cfgList[5],4)      
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',writeCmdStr+self.function.getSdoDataStr()])
        pass
    def pushButton_flowConfig_saveConfigToFile_clicked(self):
        self.timeoutTimer.start(3000) #设置计时间隔 3s 并启动    
        #读取配置
        decNodeid = self.mainWindow.getDecNodeid()
        self.cobid_TSDO = (str(hex(decNodeid+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
        self.cobid_RSDO = (str(hex(decNodeid+gc.cobid_RSDO)).replace('0x','')).zfill(3).upper()
        #创建文件.
        #cfgname = QFileDialog.getSaveFileName(self, "Save Config File", "./flowservoConfig.cfg",  "cfg (*.cfg)")
        #if cfgname[0]:                                                                   
        #    self.writeCfgIO = open(cfgname[0], "w")                                                     
        #   self.writeCfgFileOpened = True
        #    self.writeCfgFile_FalseNum = 0
        #先使用临时文件名。
        self.writeCfgIO = open('temp.cfg',mode='w')
        self.writeCfgFileOpened = True
        self.writeCfgFile_FalseNum = 0
        #hardware version,1009,4byte
        self.function.decStrToHexBytes('0',4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureHardwareVersionByte1+self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureHardwareVersionByte2+self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureHardwareVersionByte3+self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureHardwareVersionByte4+self.function.getSdoDataStr()])
        #software version,100A,4byte
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureSoftwareVersionByte1+self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureSoftwareVersionByte2+self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureSoftwareVersionByte3+self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readManufactureSoftwareVersionByte4+self.function.getSdoDataStr()])
        #serial number,1018:04,4byte
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.readIdentitySerialNumber+self.function.getSdoDataStr()])          
        #开始按照list读取.
        for index in range(len(gc.eepromList)):
            self.listToSdoReadCmd(gc.eepromList[index])
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',self.sdoCmdStr+self.function.getSdoDataStr()]) 
        self.pushButton_flowConfig_saveConfigToFile.setEnabled(False)
        pass

    def pushButton_flowConfig_loadConfigFromFile_clicked(self):
        self.timeoutTimer.start(3000) #设置计时间隔 3s 并启动  
        self.pushButton_flowConfig_loadConfigFromFile.setEnabled(False)
        decNodeid = self.mainWindow.getDecNodeid()
        self.cobid_TSDO = (str(hex(decNodeid+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
        self.cobid_RSDO = (str(hex(decNodeid+gc.cobid_RSDO)).replace('0x','')).zfill(3).upper()
        str6083 = ''
        str6084 = ''
        firstLineFound = False
        lastSendSucceed = False
        #打开文件.
        cfgname = QFileDialog.getOpenFileName(self, "Open Config File", "./", "cfg (*.cfg)")
        pathMixName = cfgname[0].split('/')
        namex = pathMixName[len(pathMixName)-1]
        if namex == self.lineEdit_flowConfig_hardwareVersion.text()+'.cfg':
            if cfgname[0]:                                                                
                self.readCfgIO = open(cfgname[0], "r")   
                self.readCfgFileOpened = True
                while 1:
                    line =  self.readCfgIO.readline()
                    if not line:
                        break   
                    line.rstrip('\r')   #去除换行符.
                    strList = line.split()  #默认为空格,TAB为分隔符.
                    if len(strList) > 1:    #跳过空行.
                        if strList[1] == '2001':
                            firstLineFound = True
                        if firstLineFound == True:
                            if strList[1] == '6083':
                                str6083 = strList
                            elif strList[1] == '6084':
                                str6084 = strList    
                            else:
                                self.writeCfgToServo(strList) 
                                if strList[1] == '60C6':
                                    lastSendSucceed = True
                if lastSendSucceed == True:
                    self.writeCfgToServo(str6083)
                    self.writeCfgToServo(str6084)  
                    #保存
                    self.function.hexStrToHexBytes('65766173')   #save的ASCII
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeStoreParameterSaveConfig+self.function.getSdoDataStr()])   
                    self.readCfgIO.close()        
                    self.readCfgFileOpened = False    
            pass
        else:
            QMessageBox.warning(self,"Error","wrong hardware!") 
    def timeout(self):
        if self.writeCfgFileOpened == True:
            self.writeCfgIO.close()
            self.writeCfgFileOpened = False   
            self.pushButton_flowConfig_saveConfigToFile.setEnabled(True)
        if self.readCfgFileOpened == True:
            self.readCfgIO.close()
            self.readCfgFileOpened = False   
        pass
    def processCurrentFrame(self,currentFrameArr):
        #解析数据,根据数据类型的不同,往不同的地方更新
        frameCobid  = currentFrameArr[gc.rcvFrameIndex_Cobid]      #字符串的cobid
        if (frameCobid == self.cobid_RSDO):
            #这个范围为收到的sdo的返回,那么看看是否需要更新SR的value
            self.sdoStatus   = currentFrameArr[gc.rcvFrameIndex_Data][0:2]
            self.sdoIndex    = currentFrameArr[gc.rcvFrameIndex_Data][6:8] +currentFrameArr[gc.rcvFrameIndex_Data][3:5]
            self.sdoSubindex = currentFrameArr[gc.rcvFrameIndex_Data][9:11]
            self.sdoData     = currentFrameArr[gc.rcvFrameIndex_Data][21:23] + currentFrameArr[gc.rcvFrameIndex_Data][18:20]\
                             + currentFrameArr[gc.rcvFrameIndex_Data][15:17] + currentFrameArr[gc.rcvFrameIndex_Data][12:14]                                       
            if self.sdoStatus == gc.sdo_rspd\
                or self.sdoStatus == gc.sdo_rspd_1byte\
                or self.sdoStatus == gc.sdo_rspd_2byte\
                or self.sdoStatus == gc.sdo_rspd_3byte\
                or self.sdoStatus == gc.sdo_rspd_4byte:
                self.switchIndexFunction(self.sdoIndex)()
                if self.writeCfgFileOpened == True:
                    for index in range(len(gc.eepromList)):
                        if self.sdoIndex == gc.eepromList[index][gc.eepromListSubindexOfIndex] and self.sdoSubindex == gc.eepromList[index][gc.eepromListSubindexOfSubindex]:
                            gc.eepromList[index][gc.eepromListSubindexOfData] = int.from_bytes(bytes.fromhex(self.sdoData), byteorder='big', signed=gc.eepromList[index][gc.eepromListSubindexOfSign])  
                            gc.eepromList[index][gc.eepromListSubindexOfValid] = 'True' 
                            if self.sdoIndex == '60C6':
                                validStatus = True
                                for index2 in range(len(gc.eepromList)):
                                    #2022.07.04, 碰到false也写入文件,改为记录false的个数.
                                    if gc.eepromList[index2][gc.eepromListSubindexOfValid] == 'False':
                                        self.writeCfgFile_FalseNum += 1
                                        #validStatus = False
                                        #self.writeCfgIO.close()
                                        #self.writeCfgFileOpened = False   
                                        #self.pushButton_flowConfig_saveConfigToFile.setEnabled(True)
                                if validStatus ==True:
                                    #gc.eepromList[0][gc.eepromListSubindexOfValid] = 'False'    #强制将nodeid的validstatus改为False.
                                    for listindex in range(len(gc.eepromList)):
                                        if gc.eepromList[listindex][0] == '200101_nodeid':
                                            gc.eepromList[listindex][gc.eepromListSubindexOfValid] = 'False'   #强制将nodeid的validstatus改为False.
                                        if gc.eepromList[listindex][0] == '201003_currentKp':
                                            gc.eepromList[listindex][gc.eepromListSubindexOfValid] = 'False'   #强制将nodeid的validstatus改为False.
                                        if gc.eepromList[listindex][0] == '201004_currentKi':
                                            gc.eepromList[listindex][gc.eepromListSubindexOfValid] = 'False'   #强制将nodeid的validstatus改为False.
                                    self.writeCfgToFile() 
        pass            
    
    
    def default_switch(self):
        pass
    def index_0x1009_hardwareVersion(self):
        if self.sdoSubindex == '01':
            self.hwversion = self.sdoData[6:8]
        elif self.sdoSubindex == '02':
            self.hwversion += self.sdoData[6:8]
        elif self.sdoSubindex == '03':
            self.hwversion += self.sdoData[6:8]
        elif self.sdoSubindex == '04':        
            self.hwversion += self.sdoData[6:8]
            #print('hwversion=',self.hwversion)
            tempdata =str(int.from_bytes(bytes.fromhex(self.hwversion), byteorder='big', signed=False)) 
            #print('tempdata=',tempdata)
            self.lineEdit_flowConfig_hardwareVersion.setText(tempdata) 
        pass
    def index_0x100A_softwareVersion(self):
        if self.sdoSubindex == '01':
            self.swversion = self.sdoData[6:8]
        elif self.sdoSubindex == '02':
            self.swversion += self.sdoData[6:8]
        elif self.sdoSubindex == '03':
            self.swversion += self.sdoData[6:8]
        elif self.sdoSubindex == '04':     
            self.swversion += self.sdoData[6:8]
            #print('swversion=',self.swversion)
            tempdata =str(int.from_bytes(bytes.fromhex(self.swversion), byteorder='big', signed=False)) 
            #print('tempdata=',tempdata)
            self.lineEdit_flowConfig_softwareVersion.setText(tempdata)
        pass   
    def index_0x1018_serialNumber(self):
        if self.sdoSubindex == '04':
            self.serialNumber = self.sdoData
            tempdata = str(hex(int((self.serialNumber).replace('\r\n',''),16)).replace('0x','')).upper()
            self.lineEdit_flowConfig_serialNumber.setText(tempdata)
        pass    
    #def index_0x1F80_nmtStartup(self):
        #tempdata = int((self.sdoData).replace('\r\n',''),16)     
        #if tempdata == 8:
            #self.comboBox_flowConfig_nmtStartup.setCurrentIndex(0)    #disabled
        #else:
            #self.comboBox_flowConfig_nmtStartup.setCurrentIndex(1)    #enabled
        #pass    
    def index_0x2000_systemConfig(self):
        pass
    def index_0x2001_canopenConfig(self):
        #nodeid
        if self.sdoSubindex == '01':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.comboBox_flowConfig_nodeid.setCurrentIndex(tempdata-1)
        #can bitrate
        elif  self.sdoSubindex == '02':
            tempdata = int((self.sdoData).replace('\r\n',''),16)     
            if tempdata == 1000:
                self.comboBox_flowConfig_baudrate.setCurrentIndex(0)
            elif tempdata == 500:
                self.comboBox_flowConfig_baudrate.setCurrentIndex(1)
            elif tempdata == 250:
                self.comboBox_flowConfig_baudrate.setCurrentIndex(2)
            elif tempdata == 125:
                self.comboBox_flowConfig_baudrate.setCurrentIndex(3)
            elif tempdata == 100:
                self.comboBox_flowConfig_baudrate.setCurrentIndex(4)
            elif tempdata == 50:
                self.comboBox_flowConfig_baudrate.setCurrentIndex(5)
            elif tempdata == 20:
                self.comboBox_flowConfig_baudrate.setCurrentIndex(6)
            elif tempdata == 10:
                self.comboBox_flowConfig_baudrate.setCurrentIndex(7)                
            else:
                self.comboBox_config_baudrate.setCurrentIndex(0)
        #can resistor
        elif  self.sdoSubindex == '03':
            tempdata = int((self.sdoData).replace('\r\n',''),16)     
            if tempdata == 0:
                self.comboBox_flowConfig_resistor.setCurrentIndex(0)    #disabled
            else:
                self.comboBox_flowConfig_resistor.setCurrentIndex(1)    #enabled
        pass    
    
    def index_0x2003_pulsePerResolution(self):
        if self.sdoSubindex == '01':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_pulsePerResolution.setText(str(tempdata))   
        pass    
    def index_0x2010_currentKpKi(self):
        if self.sdoSubindex == '03':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_currentKp.setText(str(tempdata))
        elif self.sdoSubindex == '04':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_currentKi.setText(str(tempdata))
        pass
    def index_0x2012_velocityKpKi(self):
        if self.sdoSubindex == '03':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_velocityKp.setText(str(tempdata))
        elif self.sdoSubindex == '04':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_velocityKi.setText(str(tempdata))
        elif self.sdoSubindex == '05':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_velocityStiffness.setText(str(tempdata))    
        pass   
    def index_0x2013_positionyKp(self):
        if self.sdoSubindex == '02':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_positionKp.setText(str(tempdata))
        pass 
    def index_0x2014_brakeRelated(self):
        if self.sdoSubindex == '04':
            tempdata = int((self.sdoData).replace('\r\n',''),16)     
            if tempdata == 0:
                self.comboBox_flowConfig_autoBrake.setCurrentIndex(0)    #disabled
            else:
                self.comboBox_flowConfig_autoBrake.setCurrentIndex(1)    #enabled
        pass 
    def index_0x2015_servoStrategy(self):
        if self.sdoSubindex == '05':
            tempdata = int((self.sdoData).replace('\r\n',''),16)     
            if tempdata == 0:
                self.comboBox_flowConfig_stepdirPosWithoutCanopen.setCurrentIndex(0)    #disabled
            else:
                self.comboBox_flowConfig_stepdirPosWithoutCanopen.setCurrentIndex(1)    #enabled
        elif self.sdoSubindex == '06':
            tempdata = int((self.sdoData).replace('\r\n',''),16)     
            if tempdata == 0:
                self.comboBox_flowConfig_stepdirVelWithoutCanopen.setCurrentIndex(0)    #disabled
            else:
                self.comboBox_flowConfig_stepdirVelWithoutCanopen.setCurrentIndex(1)    #enabled
        pass     
    def index_0x2016_filter(self):
        if self.sdoSubindex == '01':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_velocityFilterBandwidth.setText(str(tempdata))
        pass  
    def index_0x2017_iit(self):
        if self.sdoSubindex == '01':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_iitLimit.setText(str(tempdata))
        elif self.sdoSubindex == '03':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_iitTrigLevel.setText(str(tempdata))  
        pass     
    def index_0x2030_torqueWindow(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_torqueWindow.setText(str(tempdata))
        pass   
    def index_0x2031_torqueWindowTimeout(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_torqueWindowTimeout.setText(str(tempdata))
        pass  
    def index_0x2034_internalTargetReachWindow(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_internalTargetReachWindow.setText(str(tempdata))
        pass 
    def index_0x203A_block(self):
        if self.sdoSubindex == '01':
            tempdata = int.from_bytes(bytes.fromhex(self.sdoData), byteorder='big', signed=True)
            self.lineEdit_flowConfig_blockTriggerCurrent.setText(str(tempdata)) 
        elif self.sdoSubindex == '02':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_blockDuration.setText(str(tempdata))
        pass   
    def index_0x203B_switch(self):
        if self.sdoSubindex == '01':
            tempdata = int((self.sdoData).replace('\r\n',''),16)     
            if tempdata == 0:
                self.comboBox_flowConfig_switchType.setCurrentIndex(0)    #disabled
            else:
                self.comboBox_flowConfig_switchType.setCurrentIndex(1)    #enabled
        pass 
    def index_0x2240_digitalInputControl(self):
        if self.sdoSubindex == '01':
            tempdata = int((self.sdoData).replace('\r\n',''),16)     
            if (tempdata & 0x07) == 0x07:
                self.comboBox_flowConfig_specialInputEnable.setCurrentIndex(1)      #3个都是enable才算enable
            else:
                self.comboBox_flowConfig_specialInputEnable.setCurrentIndex(0)      #只要有1个不是enable就不算enable
        elif self.sdoSubindex == '02':
            tempdata = int((self.sdoData).replace('\r\n',''),16)   
            if (tempdata & 0x07) == 0x07:
                self.comboBox_flowConfig_specialInputReverse.setCurrentIndex(1)     #3个都是reverse才算reverse
            else:
                self.comboBox_flowConfig_specialInputReverse.setCurrentIndex(0)     
        pass  
    def index_0x2250_digitalOutputControl(self):
        if self.sdoSubindex == '01':
            tempdata = int((self.sdoData).replace('\r\n',''),16)     
            if (tempdata & 0x01) == 0x01:
                self.comboBox_flowConfig_specialOutputEnable.setCurrentIndex(1)      #output只有1个
            else:
                self.comboBox_flowConfig_specialOutputEnable.setCurrentIndex(0)      
        elif self.sdoSubindex == '02':
            tempdata = int((self.sdoData).replace('\r\n',''),16)   
            if (tempdata & 0x01) == 0x01:
                self.comboBox_flowConfig_specialOutputReverse.setCurrentIndex(1)     
            else:
                self.comboBox_flowConfig_specialOutputReverse.setCurrentIndex(0)     
        pass           
    def index_0x6065_followingErrorWindow(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_followingErrorWindow.setText(str(tempdata))
        pass   
    def index_0x6066_followingErrorTimeout(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_followingErrorTimeout.setText(str(tempdata))
        pass  
    def index_0x6067_positionWindow(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_positionWindow.setText(str(tempdata))
        pass   
    def index_0x6068_positionWindowTime(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_positionWindowTime.setText(str(tempdata))
        pass  
    def index_0x6072_maxTorque(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_maxTorque.setText(str(tempdata))
        pass  
    def index_0x607C_homeOffset(self):
        tempdata = int.from_bytes(bytes.fromhex(self.sdoData), byteorder='big', signed=True)
        self.lineEdit_flowConfig_homeOffset.setText(str(tempdata)) 
        self.mainWindow.setHomeOffset(str(tempdata))
        pass     
    def index_0x607D_softwarePositionLimit(self):
        if self.sdoSubindex == '01':
            tempdata = int.from_bytes(bytes.fromhex(self.sdoData), byteorder='big', signed=True)
            self.lineEdit_flowConfig_minPositionLimit.setText(str(tempdata)) 
        elif self.sdoSubindex == '02':
            tempdata = int.from_bytes(bytes.fromhex(self.sdoData), byteorder='big', signed=True)
            self.lineEdit_flowConfig_maxPositionLimit.setText(str(tempdata)) 
        pass     
    def index_0x607E_polarity(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)     
        if (tempdata & 0xE0) == 0:
            self.comboBox_flowConfig_polarity.setCurrentIndex(0)    #non inverted
        else:
            self.comboBox_flowConfig_polarity.setCurrentIndex(1)    # inverted
        pass    
    def index_0x607F_maxProfileVelocity(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_maxProfileVelocity.setText(str(tempdata))
        pass   
    def index_0x6083_profileAcceleration(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_profileAcceleration.setText(str(tempdata))
        self.mainWindow.setProfileAcceleration(str(tempdata))
        pass  
    def index_0x6084_profileDeceleration(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_profileDeceleration.setText(str(tempdata))
        self.mainWindow.setProfileDeceleration(str(tempdata))    
        pass   
    def index_0x6085_quickstopDeceleration(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_quickstopDeceleration.setText(str(tempdata))
        pass   
    def index_0x6087_torqueSlope(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_torqueSlope.setText(str(tempdata))
        self.mainWindow.setTorqueSlope(str(tempdata)) 
        pass      
    def index_0x6093_positionFactor(self):
        if self.sdoSubindex == '01':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_positionFactorNumerator.setText(str(tempdata))
        elif self.sdoSubindex == '02':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_positionFactorDivisor.setText(str(tempdata))
        pass 
    def index_0x6095_velocityFactor(self):
        if self.sdoSubindex == '01':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_velocityFactorNumerator.setText(str(tempdata))
        elif self.sdoSubindex == '02':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_velocityFactorDivisor.setText(str(tempdata))
        pass   
    def index_0x6097_accelerationFactor(self):
        if self.sdoSubindex == '01':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_accelerationFactorNumerator.setText(str(tempdata))
        elif self.sdoSubindex == '02':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_accelerationFactorDivisor.setText(str(tempdata))
        pass  
    def index_0x6098_homingMethod(self):
        #currentMethod = str(int(self.sdoData,16))
        #print('sdodata=',self.sdoData)
        currentMethod = str(int.from_bytes(bytes.fromhex(self.sdoData[6:8]), byteorder='big', signed=True))
        #print('currentMethod=',currentMethod)
        tempIndex = gc.homingMethodDict.get(currentMethod)
        #print('currentIndex=',tempIndex)
        self.comboBox_flowConfig_homingMethod.setCurrentIndex(tempIndex)
        self.mainWindow.setHomingMethod(tempIndex)
        pass 
    def index_0x6099_homingSpeed(self):
        if self.sdoSubindex == '01':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_homingSpeed1.setText(str(tempdata))
            self.mainWindow.setHomingSpeed1(str(tempdata))
        elif self.sdoSubindex == '02':
            tempdata = int((self.sdoData).replace('\r\n',''),16)
            self.lineEdit_flowConfig_homingSpeed2.setText(str(tempdata))
            self.mainWindow.setHomingSpeed2(str(tempdata))
        pass 
    def index_0x609A_homingAcceleration(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_homingAcceleration.setText(str(tempdata))
        self.mainWindow.setHomingAcceleration(str(tempdata))
        pass     
    def index_0x60C5_maxAcceleration(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_maxAcceleration.setText(str(tempdata))
        pass   
    def index_0x60C6_maxDeceleration(self):
        tempdata = int((self.sdoData).replace('\r\n',''),16)
        self.lineEdit_flowConfig_maxDeceleration.setText(str(tempdata))
        pass 
    def switchIndexFunction(self,index):
        indexs = {
            '1009': self.index_0x1009_hardwareVersion,
            '100A': self.index_0x100A_softwareVersion,
            '100a': self.index_0x100A_softwareVersion,
            '1018': self.index_0x1018_serialNumber,
            #'1F80': self.index_0x1F80_nmtStartup,
            #'1f80': self.index_0x1F80_nmtStartup,
            '2000': self.index_0x2000_systemConfig,
            '2001': self.index_0x2001_canopenConfig,
            '2003': self.index_0x2003_pulsePerResolution,
            '2010': self.index_0x2010_currentKpKi,
            '2012': self.index_0x2012_velocityKpKi,
            '2013': self.index_0x2013_positionyKp,
            '2014': self.index_0x2014_brakeRelated,
            '2015': self.index_0x2015_servoStrategy,
            '2016': self.index_0x2016_filter,
            '2017': self.index_0x2017_iit,
            '2030': self.index_0x2030_torqueWindow,
            '2031': self.index_0x2031_torqueWindowTimeout,
            '2034': self.index_0x2034_internalTargetReachWindow,
            '203A': self.index_0x203A_block,
            '203a': self.index_0x203A_block,
            '203B': self.index_0x203B_switch,
            '203b': self.index_0x203B_switch,
            '2240': self.index_0x2240_digitalInputControl,
            '2250': self.index_0x2250_digitalOutputControl,
            '6065': self.index_0x6065_followingErrorWindow,
            '6066': self.index_0x6066_followingErrorTimeout,
            '6067': self.index_0x6067_positionWindow,
            '6068': self.index_0x6068_positionWindowTime,
            '6072': self.index_0x6072_maxTorque,
            '607C': self.index_0x607C_homeOffset,
            '607c': self.index_0x607C_homeOffset,
            '607D': self.index_0x607D_softwarePositionLimit,
            '607d': self.index_0x607D_softwarePositionLimit,
            '607E': self.index_0x607E_polarity,
            '607e': self.index_0x607E_polarity,
            '607F': self.index_0x607F_maxProfileVelocity,
            '607f': self.index_0x607F_maxProfileVelocity,
            '6083': self.index_0x6083_profileAcceleration,
            '6084': self.index_0x6084_profileDeceleration,
            '6085': self.index_0x6085_quickstopDeceleration,
            '6087': self.index_0x6087_torqueSlope,
            '6093': self.index_0x6093_positionFactor,
            '6095': self.index_0x6095_velocityFactor,
            '6097': self.index_0x6097_accelerationFactor,
            '6098': self.index_0x6098_homingMethod,
            '6099': self.index_0x6099_homingSpeed,
            '609A': self.index_0x609A_homingAcceleration,
            '609a': self.index_0x609A_homingAcceleration,
            '60C5': self.index_0x60C5_maxAcceleration,
            '60c5': self.index_0x60C5_maxAcceleration,
            '60C6': self.index_0x60C6_maxDeceleration,
            '60c6': self.index_0x60C6_maxDeceleration
        }    
        return indexs.get(index, self.default_switch)                                 
