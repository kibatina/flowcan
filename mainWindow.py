import pyqtgraph as pg
import struct
import sys
import time
import array
import csv

from pyqtgraph.functions import glColor
import ui_flowmain
from ui_flowmain import Ui_UI_Main

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QByteArray, QTimer, QDate, Qt
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAbstractItemView, QHeaderView, QTableWidgetItem, QMessageBox
from pyqtgraph import PlotWidget
from PyQt5.QtGui import QFont,QColor,QBrush,QPixmap,QPen,QIcon

import rwQueue
import globalConstants as gc
#import function
import ico_rc
import tpdoWindow
import rpdoWindow

class MyMainWindow(QMainWindow,Ui_UI_Main):
    
    def __init__(self, comTransceiver, function,tpdoConfig, rpdoConfig,nodeidConfig,parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)     
        #self.setWindowIcon(QIcon('winico.ico'))
        self.comTransceiver = comTransceiver
        self.function       = function
        self.tpdoConfig     = tpdoConfig
        self.rpdoConfig     = rpdoConfig
        self.nodeidConfig   = nodeidConfig
        self.decNodeid      = 0x00
        self.strNodeid      = ''
        self.cobid_TSDO     = ''    #600+nodeid
        self.cobid_RSDO     = ''    #580+nodeid
        self.cobid_TPDO1    = ''    #180+nodeid
        self.cobid_RPDO1    = ''    #200+nodeid
        self.cobid_TPDO2    = ''    #280+nodeid
        self.cobid_RPDO2    = ''    #300+nodeid
        self.cobid_TPDO3    = ''    #380+nodeid
        self.cobid_RPDO3    = ''    #400+nodeid
        self.cobid_TPDO4    = ''    #480+nodeid
        self.cobid_RPDO4    = ''    #50Q0+nodeid
        #self.cobid_EMCY     = ''    #080+nodeid        
        self.cobid_NODEG = ''
        #self.cobid_SYNC     = '080'
        self.lastTimeStamp  = 0
        self.isThereNewData = False    
        self.pdoInhibitTime = '0'     #默认0毫秒,也就是不禁止.
        self.mianWindowTitle    = 'Flowservo 20221115 www.flowservo.com'
        self.setWindowTitle(self.mianWindowTitle)
        #是有有效,是否有符号,几个byte,起始字符下标.
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
        #map status
        self.checkMappedNum = False
        self.TpdoMapStatus   = [False,False,False,False]
        self.RpdoMapStatus   = [False,False,False,False]
        #log的一些全局变量.
        self.log_maxRowNum = 1000
        self.log_maxColumnNum = gc.rcvFrameMaxIndex
        self.log_currentRowNum = 0
        self.logQueue=rwQueue.RwQueue(self.log_maxRowNum)
        #error的一些全局变量.
        self.error_maxRowNum = 10
        self.error_maxColumnNum = gc.rcvFrameMaxIndex
        self.error_currentRowNum = 0
        self.errorQueue=rwQueue.RwQueue(self.error_maxRowNum)
        #log的全局变量
        self.enableLog = False          #记录到csv文件
        self.enableRefreshLog = True    #log的刷新.
        #diagram的全局变量
        self.enableRefreshDiagram = True
        self.controlTimer = None        #control这里的一个延时.
        self.curveTpdo1Data1 = None
        self.curveTpdo1Data2 = None
        self.curveTpdo1Data3 = None
        self.curveTpdo1Data4 = None    
        self.curveTpdo2Data1 = None
        self.curveTpdo2Data2 = None
        self.curveTpdo2Data3 = None
        self.curveTpdo2Data4 = None
        self.curveTpdo3Data1 = None
        self.curveTpdo3Data2 = None
        self.curveTpdo3Data3 = None
        self.curveTpdo3Data4 = None
        self.curveTpdo4Data1 = None
        self.curveTpdo4Data2 = None
        self.curveTpdo4Data3 = None
        self.curveTpdo4Data4 = None   

        self.arrayTpdo1Data1 = array.array('i')
        self.arrayTpdo1Data2 = array.array('i')
        self.arrayTpdo1Data3 = array.array('i')
        self.arrayTpdo1Data4 = array.array('i')
        self.arrayTpdo2Data1 = array.array('i')
        self.arrayTpdo2Data2 = array.array('i')
        self.arrayTpdo2Data3 = array.array('i')
        self.arrayTpdo2Data4 = array.array('i')
        self.arrayTpdo3Data1 = array.array('i')
        self.arrayTpdo3Data2 = array.array('i')
        self.arrayTpdo3Data3 = array.array('i')
        self.arrayTpdo3Data4 = array.array('i')
        self.arrayTpdo4Data1 = array.array('i')
        self.arrayTpdo4Data2 = array.array('i')
        self.arrayTpdo4Data3 = array.array('i')
        self.arrayTpdo4Data4 = array.array('i')
        self.plotDataLength = 2000   #所有plot最多都是500个数据

        #other nodeid list
        self.otherNodeidList = []
        self.otherNodeidListLen  = 0
    
        # 设置实例
        self.CreateItems()
        # 设置信号与槽
        self.CreateSignalSlot()
        # 初始化log表格
        self.InitLogTable()
        self.InitErrorTable()
        #csv写入文件的句柄.
        self.CurrentCsvIO = None
        #plot的y的最大值,最小值
        self.YMax = 0
        self.YMin = 0
        self.plotYMax = 0
        self.plotYMin = 0
        pass

    def InitLogTable(self):  
        #sequqnce,timestamp, timediff,cobid, dlc, rtr, data
        self.tableWidget_log.setColumnCount(self.log_maxColumnNum)
        self.tableWidget_log.setRowCount(self.log_maxRowNum)
        #self.setStyleSheet("QTableWidget{background-color: black;border:1px solid #000000}")
        self.tableWidget_log.setHorizontalHeaderLabels(['No.','ms','TR','rtr','cobid','len','data'])
        self.tableWidget_log.verticalHeader().setVisible(False)#隐藏列表头
        for index in range(self.tableWidget_log.columnCount()):
            headItem = self.tableWidget_log.horizontalHeaderItem(index)
            headItem.setForeground(QBrush(Qt.gray))
            headItem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.tableWidget_log.setSelectionBehavior(QAbstractItemView.SelectRows) #鼠标选择时,选中的是一行
        self.tableWidget_log.setEditTriggers(QAbstractItemView.NoEditTriggers)  #log,不可修改.也就是不能通过单击,双击修改log的内容.
        self.tableWidget_log.setSelectionMode(QAbstractItemView.SingleSelection)
        #self.tableWidget_log.setAlternatingRowColors(True)
        self.tableWidget_log.setColumnWidth(0, 61)
        self.tableWidget_log.setColumnWidth(1, 61)
        self.tableWidget_log.setColumnWidth(2, 21)
        self.tableWidget_log.setColumnWidth(3, 21)
        self.tableWidget_log.setColumnWidth(4, 51)
        self.tableWidget_log.setColumnWidth(5, 21)
        self.tableWidget_log.setColumnWidth(6, 191)
        self.tableWidget_log.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_log.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)         
        pass
    def InitErrorTable(self):  
        #sequqnce,timestamp, timediff,cobid, dlc, rtr, data
        self.tableWidget_error.setColumnCount(self.error_maxColumnNum)
        self.tableWidget_error.setRowCount(self.error_maxRowNum)
        #self.setStyleSheet("QTableWidget{background-color: white;border:1px solid #000000}")  
        self.tableWidget_error.setHorizontalHeaderLabels(['No.','ms','TR','rtr','cobid','len','data'])
        self.tableWidget_error.verticalHeader().setVisible(False)#隐藏列表头
        for index in range(self.tableWidget_error.columnCount()):
            headItem = self.tableWidget_error.horizontalHeaderItem(index)
            headItem.setForeground(QBrush(Qt.gray))
            headItem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.tableWidget_error.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_error.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_error.setSelectionMode(QAbstractItemView.SingleSelection)
        #self.tableWidget_error.setAlternatingRowColors(True)
        self.tableWidget_error.setColumnWidth(0, 61)
        self.tableWidget_error.setColumnWidth(1, 61)
        self.tableWidget_error.setColumnWidth(2, 21)
        self.tableWidget_error.setColumnWidth(3, 21)
        self.tableWidget_error.setColumnWidth(4, 51)
        self.tableWidget_error.setColumnWidth(5, 21)
        self.tableWidget_error.setColumnWidth(6, 191)  
        self.tableWidget_error.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_error.verticalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents) 
        pass    
    # 设置实例 
    def CreateItems(self):
        # Qt 串口类
        self.com = QSerialPort()
        # Qt 定时器,用于页面的刷新.
        self.refreshTimer = QTimer(self) #初始化一个定时器
        self.refreshTimer.timeout.connect(self.logRefresh) #计时结束调用operate()方法
        self.refreshTimer.timeout.connect(self.errorRefresh) #计时结束调用operate()方法
        self.refreshTimer.timeout.connect(self.updatePlot)
        self.refreshTimer.start(200) #设置计时间隔 100ms 并启动
  
    # 设置信号与槽
    def CreateSignalSlot(self):
        #self.com.readyRead.connect(self.Com_Receive_Data) # 接收数据
        #串口端口的各个button
        self.pushButton_uart_open.clicked.connect(self.pushButton_uart_open_clicked) 
        self.pushButton_uart_close.clicked.connect(self.pushButton_uart_close_clicked) 
        self.pushButton_uart_search.clicked.connect(self.pushButton_uart_search_clicked) 
        self.pushButton_uart_reboot.clicked.connect(self.pushButton_uart_reboot_clicked)
        #can 的button
        self.comboBox_can_nodeid.currentIndexChanged.connect(self.comboBox_can_nodeid_currentIndexChanged)
        self.pushButton_can_connect.clicked.connect(self.pushButton_can_connect_clicked)
        #flowservo的button
        self.pushButton_flow_autotune_current.clicked.connect(self.pushButton_flow_autotune_current_clicked)
        self.pushButton_flow_autotune_velocity.clicked.connect(self.pushButton_flow_autotune_velocity_clicked)
        self.pushButton_flow_autotune_position.clicked.connect(self.pushButton_flow_autotune_position_clicked)
        self.pushButton_flow_save.clicked.connect(self.pushButton_flow_save_clicked)
        #nmt的button
        self.pushButton_nmt_enterOperational.clicked.connect(self.pushButton_nmt_enterOperational_clicked)
        self.pushButton_nmt_enterPreoperational.clicked.connect(self.pushButton_nmt_enterPreoperational_clicked)
        self.pushButton_nmt_enterStopped.clicked.connect(self.pushButton_nmt_enterStopped_clicked)
        self.pushButton_nmt_resetNode.clicked.connect(self.pushButton_nmt_resetNode_clicked)
        self.pushButton_nmt_resetCommunication.clicked.connect(self.pushButton_nmt_resetCommunication_clicked)
        self.pushButton_nmt_getNmtState.clicked.connect(self.pushButton_nmt_getNmtState_clicked)
        #send 
        self.pushButton_send_send.clicked.connect(self.pushButton_send_send_clicked)       
        self.pushButton_send_sendFile.clicked.connect(self.pushButton_send_sendfile_clicked)
        #esdo
        self.checkBox_esdo_hex.stateChanged.connect(self.checkBox_esdo_hex_stateChanged)
        self.pushButton_esdo_read.clicked.connect(self.pushButton_esdo_read_clicked) 
        self.pushButton_esdo_write.clicked.connect(self.pushButton_esdo_write_clicked)  
        #control word
        self.pushButton_cw_shutDown.clicked.connect(self.pushButton_cw_shutDown_clicked)
        self.pushButton_cw_switchOn.clicked.connect(self.pushButton_cw_switchOn_clicked)
        self.pushButton_cw_disableVoltage.clicked.connect(self.pushButton_cw_disableVoltage_clicked)
        self.pushButton_cw_quickStop.clicked.connect(self.pushButton_cw_quickStop_clicked)
        self.pushButton_cw_enableOperation.clicked.connect(self.pushButton_cw_enableOperation_clicked)
        self.pushButton_cw_faultReset.clicked.connect(self.pushButton_cw_faultReset_clicked)
        self.pushButton_cw_halt.clicked.connect(self.pushButton_cw_halt_clicked)
        #communication
        self.pushButton_comm_saveCommunication.clicked.connect(self.pushButton_comm_saveCommunication_clicked)
        self.pushButton_comm_restoreCommunication.clicked.connect(self.pushButton_comm_restoreCommunication_clicked)
        #canopen的control的button
        self.pushButton_control_pp_start.clicked.connect(self.pushButton_control_pp_start_clicked) 
        self.pushButton_control_pp_update.clicked.connect(self.pushButton_control_pp_update_clicked) 
        self.pushButton_control_pv_start.clicked.connect(self.pushButton_control_pv_start_clicked) 
        self.pushButton_control_pv_update.clicked.connect(self.pushButton_control_pv_update_clicked)  
        self.pushButton_control_pt_start.clicked.connect(self.pushButton_control_pt_start_clicked)  
        self.pushButton_control_pt_update.clicked.connect(self.pushButton_control_pt_update_clicked)
        self.pushButton_control_h_start.clicked.connect(self.pushButton_control_h_start_clicked)  
        self.pushButton_control_ip_start.clicked.connect(self.pushButton_control_ip_start_clicked) 
        self.pushButton_control_ip_update.clicked.connect(self.pushButton_control_ip_update_clicked)  
        self.pushButton_control_csp_start.clicked.connect(self.pushButton_control_csp_start_clicked) 
        self.pushButton_control_csp_update.clicked.connect(self.pushButton_control_csp_update_clicked) 
        self.pushButton_control_csv_start.clicked.connect(self.pushButton_control_csv_start_clicked) 
        self.pushButton_control_csv_update.clicked.connect(self.pushButton_control_csv_update_clicked)  
        self.pushButton_control_cst_start.clicked.connect(self.pushButton_control_cst_start_clicked)  
        self.pushButton_control_cst_update.clicked.connect(self.pushButton_control_cst_update_clicked)
        #log的button
        self.pushButton_log_saveToFile.clicked.connect(self.pushButton_log_saveToFile_clicked) 
        self.pushButton_log_clearAll.clicked.connect(self.pushButton_log_clearAll_clicked) 
        self.pushButton_log_refresh.clicked.connect(self.pushButton_log_refresh_clicked) 
        self.pushButton_error_clearErr.clicked.connect(self.pushButton_error_clearErr_clicked) 
        #diagram的button
        self.pushButton_diagram_resetY.clicked.connect(self.pushButton_diagram_resetY_clicked) 
        self.pushButton_diagram_refresh.clicked.connect(self.pushButton_diagram_refresh_clicked) 
                
        #配置默认状态
        #main界面按钮的默认状态.
        self.pushButton_uart_search.setEnabled(True)
        self.pushButton_uart_open.setEnabled(False)
        self.pushButton_uart_close.setEnabled(False)
        self.pushButton_uart_reboot.setEnabled(False)
        
        self.comboBox_can_nodeid.addItems(gc.listOfNodeid)
        self.comboBox_can_nodeid.setCurrentIndex(0)        
        
        self.comboBox_can_baudrate.addItems(['1000','500','250','125','100','50','20','10'])   
        self.comboBox_can_baudrate.setCurrentIndex(0) 
        self.pushButton_otherNodeid.setEnabled(False)           
        self.pushButton_can_connect.setEnabled(False)
        
        self.pushButton_flow_config.setEnabled(False) 
        self.pushButton_flow_autotune_current.setEnabled(False)  
        self.pushButton_flow_autotune_velocity.setEnabled(False)  
        self.pushButton_flow_autotune_position.setEnabled(False)  
        self.pushButton_flow_save.setEnabled(False)  

        self.pushButton_nmt_enterOperational.setEnabled(False)
        self.pushButton_nmt_enterPreoperational.setEnabled(False)
        self.pushButton_nmt_enterStopped.setEnabled(False)
        self.pushButton_nmt_resetNode.setEnabled(False)
        self.pushButton_nmt_resetCommunication.setEnabled(False)
        self.pushButton_nmt_getNmtState.setEnabled(False)

        self.pushButton_send_send.setEnabled(False)
        self.pushButton_send_sendFile.setEnabled(False)
        self.comboBox_send_len.addItems(['8','7','6','5','4','3','2','1','0'])        
        self.comboBox_send_len.setCurrentIndex(0) 
         
        self.pushButton_esdo_write.setEnabled(False)
        self.pushButton_esdo_read.setEnabled(False)      
        self.comboBox_esdo_len.addItems(['4','2','1'])        
        self.comboBox_esdo_len.setCurrentIndex(0) 
        self.checkBox_esdo_hex.setChecked(False)
        
        self.pushButton_cw_shutDown.setEnabled(False)
        self.pushButton_cw_switchOn.setEnabled(False)
        self.pushButton_cw_disableVoltage.setEnabled(False)
        self.pushButton_cw_quickStop.setEnabled(False)
        self.pushButton_cw_enableOperation.setEnabled(False)
        self.pushButton_cw_faultReset.setEnabled(False)
        self.pushButton_cw_halt.setEnabled(False)
        
        self.pushButton_comm_tpdoConfig.setEnabled(False) 
        self.pushButton_comm_rpdoConfig.setEnabled(False) 
        self.pushButton_comm_saveCommunication.setEnabled(False)
        self.pushButton_comm_restoreCommunication.setEnabled(False)
        
        self.pushButton_control_pp_start.setEnabled(False) 
        self.pushButton_control_pp_update.setEnabled(False)
        self.pushButton_control_pv_start.setEnabled(False) 
        self.pushButton_control_pv_update.setEnabled(False)
        self.pushButton_control_pt_start.setEnabled(False) 
        self.pushButton_control_pt_update.setEnabled(False)
        self.pushButton_control_h_start.setEnabled(False) 
        self.pushButton_control_ip_start.setEnabled(False) 
        self.pushButton_control_ip_update.setEnabled(False)
        self.pushButton_control_csp_start.setEnabled(False) 
        self.pushButton_control_csp_update.setEnabled(False)
        self.pushButton_control_csv_start.setEnabled(False) 
        self.pushButton_control_csv_update.setEnabled(False)
        self.pushButton_control_cst_start.setEnabled(False) 
        self.pushButton_control_cst_update.setEnabled(False)      
        self.comboBox_control_h_hm.addItems(gc.listOfHomingMethod)   
        self.comboBox_control_h_hm.setCurrentIndex(30)    #默认方法35,其编号是30.

        self.pushButton_log_saveToFile.setEnabled(False)
        self.pushButton_log_clearAll.setEnabled(False)
        self.pushButton_log_refresh.setEnabled(False)
        self.pushButton_error_clearErr.setEnabled(False)
        self.pushButton_diagram_config.setEnabled(False)
        self.pushButton_diagram_resetY.setEnabled(False)
        self.pushButton_diagram_refresh.setEnabled(False)
        #设置logde plotwidget的背景颜色为白色。
        self.plotWidget_diagram.setBackground('w')
        self.plotWidget_diagram.addLegend()        
        

    # 串口刷新
    def pushButton_uart_search_clicked(self):
        self.comboBox_uart_list.clear()  
        # 要求串口访问类刷新
        self.comTransceiver.refreshComPorts()  
        # 从串口访问类获取当前可用端口列表
        availComList = self.comTransceiver.getComPorts()
        # 刷新UI显示的端口列表
        for info in availComList:
            self.comboBox_uart_list.addItem(info.portName())
            self.pushButton_uart_open.setEnabled(True)  #有端口可以选用是才ENABLE.
        pass
    # 串口打开按钮按下
    def pushButton_uart_open_clicked(self):
        # 读取用户选择的com名称
        comName = self.comboBox_uart_list.currentText()
        openComResp = self.comTransceiver.openComPort(comName)
        if not openComResp[0]:
            QMessageBox.critical(self, 'ERROR', openComResp[1])
            return
        self.pushButton_uart_search.setEnabled(False)
        self.pushButton_uart_open.setEnabled(False)
        self.pushButton_uart_close.setEnabled(True)
        self.pushButton_uart_reboot.setEnabled(True)
        self.pushButton_otherNodeid.setEnabled(True) 
        self.pushButton_can_connect.setEnabled(True)
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_version,'08','0000000000000000'])  #读取usb2can的硬件版本号.
        self.lineEdit_control_pp_alterTime.setEnabled(True)
        self.lineEdit_control_pv_alterTime.setEnabled(True)
        self.lineEdit_control_pt_alterTime.setEnabled(True)
        self.checkBox_control_ip_sync.setEnabled(True)   
        self.lineEdit_control_ip_itpv.setEnabled(True)
        self.lineEdit_control_ip_alterTime.setEnabled(True)
        self.checkBox_control_csp_sync.setEnabled(True)
        self.lineEdit_control_csp_itpv.setEnabled(True)
        self.lineEdit_control_csp_alterTime.setEnabled(True)
        self.checkBox_control_csv_sync.setEnabled(True)
        self.lineEdit_control_csv_itpv.setEnabled(True)
        self.lineEdit_control_csv_alterTime.setEnabled(True)
        self.checkBox_control_cst_sync.setEnabled(True)
        self.lineEdit_control_cst_itpv.setEnabled(True)
        self.lineEdit_control_cst_alterTime.setEnabled(True)
        pass        
    #串口关闭按钮按下
    def pushButton_uart_close_clicked(self):
        self.comTransceiver.closeCom()
        self.pushButton_uart_search.setEnabled(True)
        self.pushButton_uart_close.setEnabled(False)
        self.pushButton_uart_open.setEnabled(False)
        self.pushButton_uart_reboot.setEnabled(False)
        self.pushButton_otherNodeid.setEnabled(False) 
        self.pushButton_can_connect.setEnabled(False)
        self.setPushButton(False)  
        pass
    def pushButton_uart_reboot_clicked(self):
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_reboot,'00',''])  
        self.pushButton_uart_search.setEnabled(True)
        self.pushButton_uart_close.setEnabled(False)
        self.pushButton_uart_open.setEnabled(False)
        self.pushButton_otherNodeid.setEnabled(False) 
        self.pushButton_can_connect.setEnabled(False)
        self.pushButton_uart_reboot.setEnabled(False)
        self.setPushButton(False)  
        self.updateFlowCanStatus('OK')
        pass
    #main nodeid 的修改
    def comboBox_can_nodeid_currentIndexChanged(self):
        self.decNodeid  = int(self.comboBox_can_nodeid.currentText(),10)
        self.strNodeid  = (str(hex(self.decNodeid).replace('0x',''))).zfill(2).upper()
        #self.cobid_EMCY     = (str(hex(int(self.nodeid,16)+0x080)).replace('0x','')).zfill(3).upper()
        self.cobid_TSDO  = (str(hex(self.decNodeid+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
        self.cobid_RSDO  = (str(hex(self.decNodeid+gc.cobid_RSDO)).replace('0x','')).zfill(3).upper()
        self.cobid_NODEG = (str(hex(self.decNodeid+gc.cobid_NODEG)).replace('0x','')).zfill(3).upper()   
        self.cobid_TPDO1 = (str(hex(self.decNodeid+gc.cobid_TPDO1)).replace('0x','')).zfill(3).upper()
        self.cobid_RPDO1 = (str(hex(self.decNodeid+gc.cobid_RPDO1)).replace('0x','')).zfill(3).upper()
        self.cobid_TPDO2 = (str(hex(self.decNodeid+gc.cobid_TPDO2)).replace('0x','')).zfill(3).upper()
        self.cobid_RPDO2 = (str(hex(self.decNodeid+gc.cobid_RPDO2)).replace('0x','')).zfill(3).upper()
        self.cobid_TPDO3 = (str(hex(self.decNodeid+gc.cobid_TPDO3)).replace('0x','')).zfill(3).upper()
        self.cobid_RPDO3 = (str(hex(self.decNodeid+gc.cobid_RPDO3)).replace('0x','')).zfill(3).upper()
        self.cobid_TPDO4 = (str(hex(self.decNodeid+gc.cobid_TPDO4)).replace('0x','')).zfill(3).upper()
        self.cobid_RPDO4 = (str(hex(self.decNodeid+gc.cobid_RPDO4)).replace('0x','')).zfill(3).upper() 
        self.nodeidConfig.updateNodeidState(self.decNodeid)
        self.nodeidConfig.pushButton_nodeid_update_clicked()
        pass
    #can的connect按钮按下
    def pushButton_can_connect_clicked(self):
        #以下的TPDO和RPDO,默认是按照usb2can的角度描述的,对servo来说TPDO1是180,那么对usb2can来说,TPDO1是200
        #从usb2can的角度讲,TSDO是600, RSDO是580
        self.decNodeid  = int(self.comboBox_can_nodeid.currentText(),10)
        self.strNodeid  = str(hex(self.decNodeid).replace('0x','')).zfill(2).upper()
        #self.cobid_EMCY     = (str(hex(int(self.nodeid,16)+0x080)).replace('0x','')).zfill(3).upper()
        self.cobid_TSDO  = (str(hex(self.decNodeid+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
        self.cobid_RSDO  = (str(hex(self.decNodeid+gc.cobid_RSDO)).replace('0x','')).zfill(3).upper()
        self.cobid_NODEG = (str(hex(self.decNodeid+gc.cobid_NODEG)).replace('0x','')).zfill(3).upper()   
        self.cobid_TPDO1 = (str(hex(self.decNodeid+gc.cobid_TPDO1)).replace('0x','')).zfill(3).upper()
        self.cobid_RPDO1 = (str(hex(self.decNodeid+gc.cobid_RPDO1)).replace('0x','')).zfill(3).upper()
        self.cobid_TPDO2 = (str(hex(self.decNodeid+gc.cobid_TPDO2)).replace('0x','')).zfill(3).upper()
        self.cobid_RPDO2 = (str(hex(self.decNodeid+gc.cobid_RPDO2)).replace('0x','')).zfill(3).upper()
        self.cobid_TPDO3 = (str(hex(self.decNodeid+gc.cobid_TPDO3)).replace('0x','')).zfill(3).upper()
        self.cobid_RPDO3 = (str(hex(self.decNodeid+gc.cobid_RPDO3)).replace('0x','')).zfill(3).upper()
        self.cobid_TPDO4 = (str(hex(self.decNodeid+gc.cobid_TPDO4)).replace('0x','')).zfill(3).upper()
        self.cobid_RPDO4 = (str(hex(self.decNodeid+gc.cobid_RPDO4)).replace('0x','')).zfill(3).upper() 
        #发送nodeid
        #20220307, 这条数据以后可以删除了,以为nodeid配置合并到波特率里面了.
        self.function.decToHexBytes(self.decNodeid,1)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeCanopenConfigCanNodeid+self.function.getSdoDataStr()])          
        #发送波特率. 
        canBaudrate = self.comboBox_can_baudrate.currentText() 
        tempbaudrate = (str((int.to_bytes(int(canBaudrate,10),length=2,byteorder='little',signed=True)).hex())).ljust(4,'0')
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_can_update,'03',tempbaudrate + self.strNodeid])  
        self.setPushButton(True)  
        #self.nodeidConfig.pushButton_nodeid_update_clicked()
        pass
    
    def getDecNodeid(self):
        return self.decNodeid
        pass
    
    def setHomeOffset(self,pa):
        self.lineEdit_control_h_ho.setText(pa)
        pass
    def setProfileAcceleration(self,pa):
        self.lineEdit_control_pp_pa.setText(pa)
        self.lineEdit_control_pv_pa.setText(pa)
        self.lineEdit_control_ip_pa.setText(pa)
        self.lineEdit_control_csp_pa.setText(pa)
        self.lineEdit_control_csv_pa.setText(pa)
        pass
    def setProfileDeceleration(self,pd):
        self.lineEdit_control_pp_pd.setText(pd)
        self.lineEdit_control_pv_pd.setText(pd)
        self.lineEdit_control_ip_pd.setText(pd)
        self.lineEdit_control_csp_pd.setText(pd)
        self.lineEdit_control_csv_pd.setText(pd)
        pass
    def setTorqueSlope(self,ts):
        self.lineEdit_control_pt_ts.setText(ts)
        self.lineEdit_control_cst_ts.setText(ts)
        pass
    def setHomingMethod(self,hm):
        self.comboBox_control_h_hm.setCurrentIndex(hm)
        pass
    def setHomingSpeed1(self,hs1):
        self.lineEdit_control_h_hs1.setText(hs1)
        pass
    def setHomingSpeed2(self,hs2):
        self.lineEdit_control_h_hs2.setText(hs2)
        pass
    def setHomingAcceleration(self,ha):
        self.lineEdit_control_h_ha.setText(ha)
        pass
    
    #大部分按钮的使能.    
    def setPushButton(self,status):
        self.pushButton_flow_config.setEnabled(status) 
        #self.pushButton_flow_autotune_current.setEnabled(status)  #autotune current不准备启用.
        self.pushButton_flow_autotune_velocity.setEnabled(status)  
        self.pushButton_flow_autotune_position.setEnabled(status)  
        self.pushButton_flow_save.setEnabled(status)  
        self.pushButton_nmt_enterOperational.setEnabled(status)
        self.pushButton_nmt_enterPreoperational.setEnabled(status)
        self.pushButton_nmt_enterStopped.setEnabled(status)
        self.pushButton_nmt_resetNode.setEnabled(status)
        self.pushButton_nmt_resetCommunication.setEnabled(status)
        self.pushButton_nmt_getNmtState.setEnabled(status)
        self.pushButton_send_send.setEnabled(status)
        self.pushButton_send_sendFile.setEnabled(status)
        self.pushButton_esdo_write.setEnabled(status)
        self.pushButton_esdo_read.setEnabled(status)
        self.pushButton_cw_shutDown.setEnabled(status)
        self.pushButton_cw_switchOn.setEnabled(status)
        self.pushButton_cw_disableVoltage.setEnabled(status)
        self.pushButton_cw_quickStop.setEnabled(status)
        self.pushButton_cw_enableOperation.setEnabled(status)
        self.pushButton_cw_faultReset.setEnabled(status)
        self.pushButton_cw_halt.setEnabled(status)
        self.pushButton_comm_tpdoConfig.setEnabled(status) 
        self.pushButton_comm_rpdoConfig.setEnabled(status) 
        self.pushButton_comm_saveCommunication.setEnabled(status)
        self.pushButton_comm_restoreCommunication.setEnabled(status)
        self.pushButton_log_saveToFile.setEnabled(status)
        self.pushButton_log_clearAll.setEnabled(status)   
        self.pushButton_log_refresh.setEnabled(status)
        self.pushButton_error_clearErr.setEnabled(status)
        self.pushButton_diagram_config.setEnabled(status)
        self.pushButton_diagram_resetY.setEnabled(status)
        self.pushButton_diagram_refresh.setEnabled(status)
        if status == False:
            self.pushButton_control_csp_start.setText('Start')
            self.pushButton_control_csv_start.setText('Start')
            self.pushButton_control_cst_start.setText('Start')
            self.pushButton_control_h_start.setText('Start')
        self.pushButton_control_csp_start.setEnabled(status) 
        self.pushButton_control_csp_update.setEnabled(status)    
        self.pushButton_control_csv_start.setEnabled(status) 
        self.pushButton_control_csv_update.setEnabled(status)
        self.pushButton_control_cst_start.setEnabled(status) 
        self.pushButton_control_cst_update.setEnabled(status)
        self.pushButton_control_h_start.setEnabled(status)
        self.pushButton_control_ip_start.setEnabled(status) 
        self.pushButton_control_ip_update.setEnabled(status)
        self.pushButton_control_pp_start.setEnabled(status) 
        self.pushButton_control_pp_update.setEnabled(status)
        self.pushButton_control_pv_start.setEnabled(status) 
        self.pushButton_control_pv_update.setEnabled(status)
        self.pushButton_control_pt_start.setEnabled(status) 
        self.pushButton_control_pt_update.setEnabled(status) 
        pass
    
    def pushButton_flow_autotune_current_clicked(self):
        #autotune current, 2010:06, bool 
        self.function.decStrToHexBytes('1',1)
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePidIqAutoTuneTrigger+self.function.getSdoDataStr()]) 
        pass
    def pushButton_flow_autotune_velocity_clicked(self):
        #autotune velocity, 2012:06, bool
        self.function.decStrToHexBytes('1',1)
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePidVelocityAutoTuneTrigger+self.function.getSdoDataStr()]) 
        pass
    def pushButton_flow_autotune_position_clicked(self):
        #autotune position, 2013:03, bool
        self.function.decStrToHexBytes('1',1) 
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writePidPositionAutoTuneTrigger+self.function.getSdoDataStr()]) 
        pass
    def pushButton_flow_save_clicked(self):
        #save config, 1010:03, 4byte
        self.function.hexStrToHexBytes('65766173')  
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeStoreParameterSaveConfig+self.function.getSdoDataStr()]) 
        pass   
    def pushButton_nmt_enterOperational_clicked(self):
        if self.checkBox_nmt_all.isChecked():
            self.writeNMT(True,gc.nmt_operational)
        else:
            self.writeNMT(False,gc.nmt_operational) 
        pass
    def pushButton_nmt_enterPreoperational_clicked(self):
        if self.checkBox_nmt_all.isChecked():
            self.writeNMT(True,gc.nmt_preoperational)
        else:
            self.writeNMT(False,gc.nmt_preoperational)
        pass
    def pushButton_nmt_enterStopped_clicked(self):
        if self.checkBox_nmt_all.isChecked():
            self.writeNMT(True,gc.nmt_stopmode)
        else:
            self.writeNMT(False,gc.nmt_stopmode)
        pass
    def pushButton_nmt_resetNode_clicked(self):
        if self.checkBox_nmt_all.isChecked():
            self.writeNMT(True,gc.nmt_resetnode)
        else:
            self.writeNMT(False,gc.nmt_resetnode)
        pass
    def pushButton_nmt_resetCommunication_clicked(self):
        if self.checkBox_nmt_all.isChecked():
            self.writeNMT(True,gc.nmt_resetcomm)
        else:
            self.writeNMT(False,gc.nmt_resetcomm)
        pass
    def pushButton_nmt_getNmtState_clicked(self):
        if self.checkBox_nmt_all.isChecked():
            self.nmt_getNmtState(True)
        else:
            self.nmt_getNmtState(False)
        pass
    
    #send and receive中的send按钮被按下.
    def pushButton_send_send_clicked(self):
        sendCobid = self.lineEdit_send_cobid.text()
        intLen = int(self.comboBox_send_len.currentText())
        sendData = self.lineEdit_send_data.text().replace(' ','').ljust(intLen*2,'0')  
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,sendCobid,str(intLen),sendData])        
        pass    
    def pushButton_send_sendfile_clicked(self):
        filename,_ = QFileDialog.getOpenFileName(self, "Select a file...",'./', filter="CAN (*.can)")
        with open(filename, newline='') as csvfile:
            canfile = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in canfile:
                if len(row) > 0:
                    if row[0].isdigit():
                        if len(row) >= 5:  #row[0]的type是str.
                            #row[0]是时间,是十进制的,需要转换为16进制来传输,其余都是16进制.
                            #乘以1000是为了从ms转换到us
                            timeStr = str((int.to_bytes(int(row[0],10)*1000,length=4,byteorder='big',signed=False)).hex())
                            self.comTransceiver.write([timeStr,row[1],row[2],row[3],row[4].replace(' ','')])  
                #else:
                    #print('not digit',row)
                    #pass
        pass
    #esdo中的write按钮被按下
    def pushButton_esdo_write_clicked(self):
        wIndex = self.lineEdit_esdo_index.text().zfill(4)
        wSubindex = self.lineEdit_esdo_subindex.text().zfill(2)
        #回写大写的.
        self.lineEdit_esdo_index.setText(wIndex.upper())
        self.lineEdit_esdo_subindex.setText(wSubindex.upper())
        self.lineEdit_esdo_rData.setText('')
        wLen = str(int(self.comboBox_esdo_len.currentText()))  
        wValue = self.lineEdit_esdo_tData.text()  
        wIndexStr = wIndex[-2:] + wIndex[-4:-2]
        wSubIndexStr = wSubindex   
        if self.checkBox_esdo_hex.isChecked():
            #已经是hex的了.
            self.function.hexStrToHexBytes(wValue)   
        else:
            self.function.decStrToHexBytes(wValue,int(self.comboBox_esdo_len.currentText()))  #write value可能是负数,且可能是2个byte,1byte,不一定4byte.
        if wLen == '1':     
            self.comTransceiver.write(['00',gc.defaultRtr,self.cobid_TSDO,'08',gc.sdo_w_1byte+wIndexStr+wSubIndexStr+self.function.getSdoDataStr()])  
        elif wLen == '2':
            self.comTransceiver.write(['00',gc.defaultRtr,self.cobid_TSDO,'08',gc.sdo_w_2byte+wIndexStr+wSubIndexStr+self.function.getSdoDataStr()])  
        elif wLen == '3':
            self.comTransceiver.write(['00',gc.defaultRtr,self.cobid_TSDO,'08',gc.sdo_w_3byte+wIndexStr+wSubIndexStr+self.function.getSdoDataStr()])  
        elif wLen == '4':
            self.comTransceiver.write(['00',gc.defaultRtr,self.cobid_TSDO,'08',gc.sdo_w_4byte+wIndexStr+wSubIndexStr+self.function.getSdoDataStr()])  
        pass

    #esdo中的read按钮被按下
    def pushButton_esdo_read_clicked(self):
        rIndex = self.lineEdit_esdo_index.text().zfill(4)
        rSubindex = self.lineEdit_esdo_subindex.text().zfill(2)
        #回写大写的.
        self.lineEdit_esdo_index.setText(rIndex.upper())
        self.lineEdit_esdo_subindex.setText(rSubindex.upper())
        self.lineEdit_esdo_rData.setText('')    
        rLen = '08'
        rIndexStr = rIndex[-2:]+rIndex[-4:-2]
        rSubIndexStr = rSubindex   
        self.function.decStrToHexBytes('0',4)   #读取的时候不管长度,都是4个byte,反正都是0.   
        #self.com.write(sendText.encode('UTF-8'))  
        self.comTransceiver.write(['00',gc.defaultRtr,self.cobid_TSDO,rLen,gc.sdo_r+rIndexStr+rSubIndexStr+self.function.getSdoDataStr()])  
        pass
    def checkBox_esdo_hex_stateChanged(self):
        tempLen = int(self.comboBox_esdo_len.currentText())
        tText = self.lineEdit_esdo_tData.text()
        if tText == '':
            tText = '00'
        if (len(tText)%2) != 0:
            tText = '0' + tText
        rText = self.lineEdit_esdo_rData.text()
        if rText == '':
            rText = '00'
        if (len(rText)%2) != 0:
            rText = '0' + rText 
        if self.checkBox_esdo_hex.isChecked():
            #DEC变为HEX
            try:
                tempdata = str((int.to_bytes(int(tText,10),length=tempLen,byteorder='big',signed=True)).hex())
            except:
                tempdata = str((int.to_bytes(int(tText,10),length=tempLen,byteorder='big',signed=False)).hex())
            self.lineEdit_esdo_tData.setText(str(tempdata.upper())) 
            try:
                tempdata = str((int.to_bytes(int(rText,10),length=tempLen,byteorder='big',signed=True)).hex())
            except:
                tempdata = str((int.to_bytes(int(rText,10),length=tempLen,byteorder='big',signed=False)).hex())
            self.lineEdit_esdo_rData.setText(str(tempdata.upper()))  
        else:
            #HEX变为DEC
            tempdata = int.from_bytes(bytes.fromhex(tText), byteorder='big', signed=True)
            self.lineEdit_esdo_tData.setText(str(tempdata))  

            tempdata = int.from_bytes(bytes.fromhex(rText), byteorder='big', signed=True)
            self.lineEdit_esdo_rData.setText(str(tempdata))         
        pass
 
    #control word的pushButton
    def pushButton_cw_shutDown_clicked(self):
        if self.checkBox_cw_all.isChecked():
            self.writeControlWord(True,gc.cw_shutDown)
        else:
            self.writeControlWord(False,gc.cw_shutDown)
        pass
    def pushButton_cw_switchOn_clicked(self):
        if self.checkBox_cw_all.isChecked():
            self.writeControlWord(True,gc.cw_switchOn) 
        else:
            self.writeControlWord(False,gc.cw_switchOn) 
        pass
    def pushButton_cw_disableVoltage_clicked(self):
        if self.checkBox_cw_all.isChecked():
            self.writeControlWord(True,gc.cw_disableVoltage) 
        else:
            self.writeControlWord(False,gc.cw_disableVoltage) 
        pass
    def pushButton_cw_quickStop_clicked(self):
        if self.checkBox_cw_all.isChecked():
            self.writeControlWord(True,gc.cw_quickStop)
        else:
            self.writeControlWord(False,gc.cw_quickStop)  
        pass
    def pushButton_cw_enableOperation_clicked(self):
        if self.checkBox_cw_all.isChecked():
            self.writeControlWord(True,gc.cw_enableOperation) 
        else:
            self.writeControlWord(False,gc.cw_enableOperation) 
        pass
    def pushButton_cw_faultReset_clicked(self):
        if self.checkBox_cw_all.isChecked():
            self.writeControlWord(True,gc.cw_faultReset) 
        else:
            self.writeControlWord(False,gc.cw_faultReset) 
        pass
    def pushButton_cw_halt_clicked(self):
        if self.checkBox_cw_all.isChecked():
            self.writeControlWord(True,gc.cw_halt) 
        else:
            self.writeControlWord(False,gc.cw_halt) 
        pass

    def pushButton_comm_saveCommunication_clicked(self):
        self.writeStoreParameterSaveComm()
        pass   
    def pushButton_comm_restoreCommunication_clicked(self):
        self.writeRestoreParameterComm() 
        pass 

    def updateNodeidList(self,nodeidlist,nodeidlistlen):
        self.otherNodeidList = nodeidlist
        self.otherNodeidListLen = nodeidlistlen
        pass   
     
    #CONTROL中的profile position mode, start按钮被按下
    def pushButton_control_pp_start_clicked(self):
        buttonText = self.pushButton_control_pp_start.text()
        if buttonText == 'Start':  
            self.pushButton_control_pp_start.setEnabled(False)
            #发送nodeid
            self.function.decToHexBytes(self.decNodeid,1)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeCanopenConfigCanNodeid+self.function.getSdoDataStr()])  
            self.tpdoConfig.configTpdo(self.decNodeid)
            self.rpdoConfig.configRpdo(self.decNodeid)
            self.readMappedItemNum(self.decNodeid)
            self.controlTimer = QTimer(self) #初始化一个定时器
            self.controlTimer.timeout.connect(self.control_pp_start) #计时结束调用operate()方法
            self.controlTimer.start(300) #设置计时间隔 100ms 并启动
        else:
            self.function.hexStrToHexBytes('00000000')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pp_toggle,'05','00'+self.function.getSdoDataStr()])   
            self.pushButton_control_pp_start.setText('Start')
            self.lineEdit_control_pp_alterTime.setEnabled(True)
            
            self.pushButton_control_pv_start.setEnabled(True)
            self.pushButton_control_pt_start.setEnabled(True)
            self.pushButton_control_h_start.setEnabled(True) 
            self.pushButton_control_ip_start.setEnabled(True) 
            self.pushButton_control_csp_start.setEnabled(True) 
            self.pushButton_control_csv_start.setEnabled(True) 
            self.pushButton_control_cst_start.setEnabled(True)
            
            self.pushButton_control_pv_update.setEnabled(True)
            self.pushButton_control_pt_update.setEnabled(True)
            self.pushButton_control_ip_update.setEnabled(True) 
            self.pushButton_control_csp_update.setEnabled(True) 
            self.pushButton_control_csv_update.setEnabled(True) 
            self.pushButton_control_cst_update.setEnabled(True)  
        pass 

    def control_pp_start(self):
        self.controlTimer.stop()
        self.checkMappedNum = False
        ppcStartStatus = True
        #set control mode to profile position mode, 0x6060, 1byte
        self.writeControlMode(True,gc.mode_ppm) 
        #set synchronous counter overflow value, 0x1019, 1byte
        #self.writeSynchronousCounterOverflowValue(True)
        #set target position, 0x607A, 4byte
        tp = self.lineEdit_control_pp_tp.text()
        if tp == '':
            tp = '00'
            self.lineEdit_control_pp_tp.setText('0')
        self.writeTargetPositionToFlowcan(tp)  
        #set profile velocity, 0x6081, 4byte
        pv = self.lineEdit_control_pp_pv.text()
        if pv.isdecimal():
            self.writeProfileVelocity(True,pv)            
        else:
            QMessageBox.warning(self,"Error","pv, Wrong Input") 
            ppcStartStatus = False
        #set profile acceleration, 0x6083, 4byte
        pa = self.lineEdit_control_pp_pa.text()
        if pa.isdecimal():
            self.writeProfileAcceleration(True,pa)  
        else:
            QMessageBox.warning(self,"Error","pa, Wrong Input") 
            ppcStartStatus = False
        #set profile deceleration, 0x6084, 4byte
        pd = self.lineEdit_control_pp_pd.text() 
        if pd.isdecimal():
            self.writeProfileDeceleration(True,pd)                           
        else:
            QMessageBox.warning(self,"Error","pd, Wrong Input") 
            ppcStartStatus = False
        #获取alterTime
        alterTime = self.lineEdit_control_pp_alterTime.text()
        if alterTime == '':
            alterTime = '00'
        if alterTime.isdecimal():
            pass
        else:
            QMessageBox.warning(self,"Error","alterTime, Wrong Input") 
            ppcStartStatus = False    
        #配置其它nodeid.
        self.writeOtherNodeidToFlowCan()
        if ppcStartStatus == True:
            for index in range(len(self.otherNodeidList)):
                self.tpdoConfig.configTpdo(self.otherNodeidList[index])
                self.rpdoConfig.configRpdo(self.otherNodeidList[index])    
            #set control word to "ready to switch on", 0x6040, 2byte
            self.writeControlWord(True,gc.cw_shutDown)   
            #set control word to "switched on", 0x6040, 2byte
            self.writeControlWord(True,gc.cw_switchOn)        
            #set control word to "enable operation", 0x6040, 2byte
            #self.writeControlWord(True,gc.cw_enableOperation)    
            #nmt operational
            self.writeNMT(True,gc.nmt_operational)
            #enable pdo
            self.enableAllPdo(True)            
            #发送启动命令  
            self.function.decStrToHexBytes(alterTime,4) 
            if self.checkBox_control_pp_isRelative.isChecked():
                if self.checkBox_control_pp_isImmediately.isChecked():
                    #相对位置,立即执行
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pp_toggle,'05',gc.cw_nsp_relative_immediate+self.function.getSdoDataStr()])   
                else:
                    #relative, 不立即执行.
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pp_toggle,'05',gc.cw_nsp_relative_notimmediate+self.function.getSdoDataStr()])  
            else:
                if self.checkBox_control_pp_isImmediately.isChecked():
                    #绝对位置,立即执行 
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pp_toggle,'05',gc.cw_nsp_absolute_immediate+self.function.getSdoDataStr()])  
                else:
                    #绝对位置,不立即执行
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pp_toggle,'05',gc.cw_nsp_absolute_notimmediate+self.function.getSdoDataStr()])    
            #修改按钮显示.     
            self.pushButton_control_pp_start.setText('Stop')
            self.pushButton_control_pp_start.setEnabled(True)
            self.lineEdit_control_pp_alterTime.setEnabled(False)
            
            self.pushButton_control_pv_start.setEnabled(False) 
            self.pushButton_control_pt_start.setEnabled(False)
            self.pushButton_control_h_start.setEnabled(False)
            self.pushButton_control_ip_start.setEnabled(False)   
            self.pushButton_control_csp_start.setEnabled(False) 
            self.pushButton_control_csv_start.setEnabled(False) 
            self.pushButton_control_cst_start.setEnabled(False)
            
            self.pushButton_control_pv_update.setEnabled(False)
            self.pushButton_control_pt_update.setEnabled(False)
            self.pushButton_control_ip_update.setEnabled(False) 
            self.pushButton_control_csp_update.setEnabled(False) 
            self.pushButton_control_csv_update.setEnabled(False) 
            self.pushButton_control_cst_update.setEnabled(False)  
        else:
            self.pushButton_control_pp_start.setEnabled(True)               
        pass    
    def pushButton_control_pp_update_clicked(self):
        ppcUpdateStatus = True
        #set target position, 0x607A, 4byte
        tp = self.lineEdit_control_pp_tp.text()
        if tp == '':
            tp = '00'
            self.lineEdit_control_pp_tp.setText('0')
        self.writeTargetPositionToFlowcan(tp)
        #set profile velocity, 0x6081, 4byte
        pv = self.lineEdit_control_pp_pv.text()
        if pv.isdecimal():
            self.writeProfileVelocity(True,pv)              
        else:
            QMessageBox.warning(self,"Error","pv, Wrong Input") 
            ppcUpdateStatus = False
        #set profile acceleration, 0x6083, 4byte
        pa = self.lineEdit_control_pp_pa.text()
        if pa.isdecimal():
            self.writeProfileAcceleration(True,pa)
        else:
            QMessageBox.warning(self,"Error","pa, Wrong Input") 
            ppcUpdateStatus = False
        #set profile deceleration, 0x6084, 4byte
        pd = self.lineEdit_control_pp_pd.text() 
        if pd.isdecimal():
            self.writeProfileDeceleration(True,pd)   
        else:
            QMessageBox.warning(self,"Error","pd, Wrong Input") 
            ppcUpdateStatus = False
        #获取alterTime
        alterTime = self.lineEdit_control_pp_alterTime.text()
        if alterTime == '':
            alterTime = '00'
        if alterTime.isdecimal():
            pass
        else:
            QMessageBox.warning(self,"Error","alterTime, Wrong Input") 
            ppcStartStatus = False    
        #配置其它nodeid.
        self.writeOtherNodeidToFlowCan()    
        if ppcUpdateStatus == True:    
            self.function.decStrToHexBytes(alterTime,4)
            if self.checkBox_control_pp_isRelative.isChecked():
                if self.checkBox_control_pp_isImmediately.isChecked():
                    #相对位置,立即执行
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pp_update,'05',gc.cw_nsp_relative_immediate+self.function.getSdoDataStr()])   
                else:
                    #relative, 不立即执行.
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pp_update,'05',gc.cw_nsp_relative_notimmediate+self.function.getSdoDataStr()])  
            else:
                if self.checkBox_control_pp_isImmediately.isChecked():
                    #绝对位置,立即执行 
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pp_update,'05',gc.cw_nsp_absolute_immediate+self.function.getSdoDataStr()])  
                else:
                    #绝对位置,不立即执行
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pp_update,'05',gc.cw_nsp_absolute_notimmediate+self.function.getSdoDataStr()])                                                               
        pass  
    
                    
    #CONTROL中的profile velocity mode, start按钮被按下
    def pushButton_control_pv_start_clicked(self):
        buttonText = self.pushButton_control_pv_start.text()
        if buttonText == 'Start':  
            self.pushButton_control_pv_start.setEnabled(False)
            #发送nodeid
            self.function.decToHexBytes(self.decNodeid,1)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeCanopenConfigCanNodeid+self.function.getSdoDataStr()])  
            self.tpdoConfig.configTpdo(self.decNodeid)
            self.rpdoConfig.configRpdo(self.decNodeid)
            self.readMappedItemNum(self.decNodeid)
            self.controlTimer = QTimer(self) #初始化一个定时器
            self.controlTimer.timeout.connect(self.control_pv_start) #计时结束调用operate()方法
            self.controlTimer.start(300) #设置计时间隔 100ms 并启动
        else:
            self.function.hexStrToHexBytes('00000000')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pv_toggle,'05','00'+self.function.getSdoDataStr()])   
            self.pushButton_control_pv_start.setText('Start')
            self.lineEdit_control_pv_alterTime.setEnabled(True)
            
            self.pushButton_control_pp_start.setEnabled(True)
            self.pushButton_control_pt_start.setEnabled(True)
            self.pushButton_control_h_start.setEnabled(True) 
            self.pushButton_control_ip_start.setEnabled(True) 
            self.pushButton_control_csp_start.setEnabled(True) 
            self.pushButton_control_csv_start.setEnabled(True) 
            self.pushButton_control_cst_start.setEnabled(True)
            
            self.pushButton_control_pp_update.setEnabled(True)
            self.pushButton_control_pt_update.setEnabled(True)
            self.pushButton_control_ip_update.setEnabled(True) 
            self.pushButton_control_csp_update.setEnabled(True) 
            self.pushButton_control_csv_update.setEnabled(True) 
            self.pushButton_control_cst_update.setEnabled(True)  
        pass 
    
    def control_pv_start(self):
        self.controlTimer.stop()
        self.checkMappedNum = False
        pvcStartStatus = True
        #set control mode to profile velocity mode, 0x6060, 1byte
        self.writeControlMode(self.decNodeid,gc.mode_pvm)  
        #set synchronous counter overflow value, 0x1019, 1byte
        #self.writeSynchronousCounterOverflowValue(True)
        #set profile acceleration, 0x6083, 4byte
        pa = self.lineEdit_control_pv_pa.text() 
        if pa.isdecimal():
            self.writeProfileAcceleration(True,pa)  
        else:
            QMessageBox.warning(self,"Error","pa, Wrong Input") 
            pvcStartStatus = False
        #set profile deceleration, 0x6084, 4byte
        pd = self.lineEdit_control_pv_pd.text() 
        if pd.isdecimal():
            self.writeProfileDeceleration(True,pd)                               
        else:
            QMessageBox.warning(self,"Error","pd, Wrong Input") 
            pvcStartStatus = False
        #set target velocity, 0x60FF, 4byte
        tv = self.lineEdit_control_pv_tv.text()
        if tv == '':
            tv = '00'
            self.lineEdit_control_pv_tv.setText('0')
        self.writeTargetVelocityToFlowcan(tv)  
        #获取alterTime
        alterTime = self.lineEdit_control_pv_alterTime.text()
        if alterTime == '':
            alterTime = '00'
        if alterTime.isdecimal():
            pass
        else:
            QMessageBox.warning(self,"Error","alterTime, Wrong Input") 
            pvcStartStatus = False    
        #配置其它nodeid.
        self.writeOtherNodeidToFlowCan()
        if pvcStartStatus == True:
            for index in range(len(self.otherNodeidList)):
                self.tpdoConfig.configTpdo(self.otherNodeidList[index])
                self.rpdoConfig.configRpdo(self.otherNodeidList[index])  
            #set control word to "ready to switch on", 0x6040, 2byte
            self.writeControlWord(True,gc.cw_shutDown)
            self.writeControlWord(True,gc.cw_switchOn)        
            #nmt operational
            self.writeNMT(True,gc.nmt_operational)
            #enable pdo
            self.enableAllPdo(True)
            #set control word to "enable operation", 0x6040, 2byte
            self.function.decStrToHexBytes(alterTime,4) 
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pv_toggle,'05',gc.cw_enableOperation+self.function.getSdoDataStr()])  
            #修改按钮显示.     
            self.pushButton_control_pv_start.setText('Stop')
            self.pushButton_control_pv_start.setEnabled(True)
            self.lineEdit_control_pv_alterTime.setEnabled(False)
            
            self.pushButton_control_pp_start.setEnabled(False) 
            self.pushButton_control_pt_start.setEnabled(False)
            self.pushButton_control_h_start.setEnabled(False)
            self.pushButton_control_ip_start.setEnabled(False)   
            self.pushButton_control_csp_start.setEnabled(False) 
            self.pushButton_control_csv_start.setEnabled(False) 
            self.pushButton_control_cst_start.setEnabled(False)
            
            self.pushButton_control_pp_update.setEnabled(False)
            self.pushButton_control_pt_update.setEnabled(False)
            self.pushButton_control_ip_update.setEnabled(False) 
            self.pushButton_control_csp_update.setEnabled(False) 
            self.pushButton_control_csv_update.setEnabled(False) 
            self.pushButton_control_cst_update.setEnabled(False)    
        else:
            self.pushButton_control_pv_start.setEnabled(True)              
        pass    
    def pushButton_control_pv_update_clicked(self):
        pvcUpdateStatus = True
        #set profile acceleration, 0x6083, 4byte
        pa = self.lineEdit_control_pv_pa.text() 
        if pa.isdecimal():
            self.writeProfileAcceleration(True,pa)  
        else:
            QMessageBox.warning(self,"Error","pa, Wrong Input") 
            pvcUpdateStatus = False
        #set profile deceleration, 0x6084, 4byte
        pd = self.lineEdit_control_pv_pd.text() 
        if pd.isdecimal():
            self.writeProfileDeceleration(True,pd)   
        else:
            QMessageBox.warning(self,"Error","pd, Wrong Input") 
            pvcUpdateStatus = False
        #获取alterTime
        alterTime = self.lineEdit_control_pv_alterTime.text()
        if alterTime == '':
            alterTime = '00'
        if alterTime.isdecimal():
            pass
        else:
            QMessageBox.warning(self,"Error","alterTime, Wrong Input") 
            pvcUpdateStatus = False        
        #pa和pd先更新,tv最后,因为tv已更新就内部traj了.    
        #set target velocity, 0x60FF, 4byte
        if pvcUpdateStatus == True:
            tv = self.lineEdit_control_pv_tv.text()
            if tv == '':
                tv = '00'
                self.lineEdit_control_pv_tv.setText('0')  
            self.writeTargetVelocityToFlowcan(tv)                                                  
        pass  
        self.function.decStrToHexBytes(alterTime,4) 
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pv_update,'05',gc.cw_enableOperation+self.function.getSdoDataStr()])  
    
    #CONTROL中的profile torque mode, start按钮被按下
    def pushButton_control_pt_start_clicked(self):
        buttonText = self.pushButton_control_pt_start.text()
        if buttonText == 'Start':  
            self.pushButton_control_pt_start.setEnabled(False)
            #发送nodeid
            self.function.decToHexBytes(self.decNodeid,1)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeCanopenConfigCanNodeid+self.function.getSdoDataStr()])  
            self.tpdoConfig.configTpdo(self.decNodeid)
            self.rpdoConfig.configRpdo(self.decNodeid)
            self.readMappedItemNum(self.decNodeid)
            self.controlTimer = QTimer(self) #初始化一个定时器
            self.controlTimer.timeout.connect(self.control_pt_start) #计时结束调用operate()方法
            self.controlTimer.start(300) #设置计时间隔 100ms 并启动
        else:
            self.function.hexStrToHexBytes('00000000')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pt_toggle,'05','00'+self.function.getSdoDataStr()])   
            self.pushButton_control_pt_start.setText('Start')
            self.lineEdit_control_pt_alterTime.setEnabled(True)
            
            self.pushButton_control_pp_start.setEnabled(True)
            self.pushButton_control_pv_start.setEnabled(True)
            self.pushButton_control_h_start.setEnabled(True) 
            self.pushButton_control_ip_start.setEnabled(True) 
            self.pushButton_control_csp_start.setEnabled(True) 
            self.pushButton_control_csv_start.setEnabled(True) 
            self.pushButton_control_cst_start.setEnabled(True) 
            
            self.pushButton_control_pp_update.setEnabled(True)
            self.pushButton_control_pv_update.setEnabled(True)
            self.pushButton_control_ip_update.setEnabled(True) 
            self.pushButton_control_csp_update.setEnabled(True) 
            self.pushButton_control_csv_update.setEnabled(True) 
            self.pushButton_control_cst_update.setEnabled(True)    
        pass 
    def control_pt_start(self):
        self.controlTimer.stop()
        self.checkMappedNum = False
        ptcStartStatus = True
        #set control mode to profile torque mode, 0x6060, 1byte
        self.writeControlMode(True,gc.mode_ptm)  
        #set synchronous counter overflow value, 0x1019, 1byte
        #self.writeSynchronousCounterOverflowValue(True)
        #set target torque, 0x6071, 2byte
        tt = self.lineEdit_control_pt_tt.text()
        if tt == '':
            tt = '00'
            self.lineEdit_control_pt_tt.setText('0')
        self.writeTargetTorqueToFlowcan(tt)
        #set torque slope, 0x6087, 4byte
        ts = self.lineEdit_control_pt_ts.text() 
        if ts.isdecimal():
            self.writeTorqueSlope(True,ts)    
        else:
            QMessageBox.warning(self,"Error","ts, Wrong Input") 
            ptcStartStatus = False 
        #获取alterTime
        alterTime = self.lineEdit_control_pt_alterTime.text()
        if alterTime == '':
            alterTime = '00'
        if alterTime.isdecimal():
            pass
        else:
            QMessageBox.warning(self,"Error","alterTime, Wrong Input") 
            ptcStartStatus = False   
        if ptcStartStatus == True:
            for index in range(len(self.otherNodeidList)):
                self.tpdoConfig.configTpdo(self.otherNodeidList[index])
                self.rpdoConfig.configRpdo(self.otherNodeidList[index])
            #set control word to "ready to switch on", 0x6040, 2byte
            self.writeControlWord(True,gc.cw_shutDown)
            self.writeControlWord(True,gc.cw_switchOn) 
            #nmt operational
            self.writeNMT(True,gc.nmt_operational)
            #enable pdo
            self.enableAllPdo(True)
            #set control word to "enable operation", 0x6040, 2byte    
            self.function.decStrToHexBytes(alterTime,4) 
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pt_toggle,'05',gc.cw_enableOperation+self.function.getSdoDataStr()])    
            #修改按钮显示.     
            self.pushButton_control_pt_start.setText('Stop')
            self.pushButton_control_pt_start.setEnabled(True)
            self.lineEdit_control_pt_alterTime.setEnabled(False)
            
            self.pushButton_control_pp_start.setEnabled(False) 
            self.pushButton_control_pv_start.setEnabled(False)
            self.pushButton_control_h_start.setEnabled(False)
            self.pushButton_control_ip_start.setEnabled(False)   
            self.pushButton_control_csp_start.setEnabled(False) 
            self.pushButton_control_csv_start.setEnabled(False) 
            self.pushButton_control_cst_start.setEnabled(False)
            
            self.pushButton_control_pp_update.setEnabled(False)
            self.pushButton_control_pv_update.setEnabled(False)
            self.pushButton_control_ip_update.setEnabled(False) 
            self.pushButton_control_csp_update.setEnabled(False) 
            self.pushButton_control_csv_update.setEnabled(False) 
            self.pushButton_control_cst_update.setEnabled(False)   
        else:
            self.pushButton_control_pt_start.setEnabled(True)               
        pass    
    def pushButton_control_pt_update_clicked(self):
        ptcUpdateStatus = True
        #set torque slope, 0x6087, 4byte
        ts = self.lineEdit_control_pt_ts.text() 
        if ts.isdecimal(): 
            self.writeTorqueSlope(True,ts)    
        else:
            QMessageBox.warning(self,"Error","ts, Wrong Input") 
            ptcUpdateStatus = False   
        #获取alterTime
        alterTime = self.lineEdit_control_pt_alterTime.text()
        if alterTime == '':
            alterTime = '00'
        if alterTime.isdecimal():
            pass
        else:
            QMessageBox.warning(self,"Error","alterTime, Wrong Input") 
            ptcUpdateStatus = False 
        if ptcUpdateStatus == True:                
            #set target torque, 0x6071, 2byte
            tt = self.lineEdit_control_pt_tt.text()
            if tt == '':
                tt = '00'
                self.lineEdit_control_pt_tt.setText('0')
            self.writeTargetTorqueToFlowcan(tt) 
        self.function.decStrToHexBytes(alterTime,4) 
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_pt_update,'05',gc.cw_enableOperation+self.function.getSdoDataStr()])    
        pass
       

    def pushButton_control_h_start_clicked(self):
        buttonText = self.pushButton_control_h_start.text()
        if buttonText == 'Start':  
            self.pushButton_control_h_start.setEnabled(False)
            self.tpdoConfig.configTpdo(self.decNodeid)
            self.rpdoConfig.configRpdo(self.decNodeid)
            self.readMappedItemNum(self.decNodeid)
            self.controlTimer = QTimer(self) #初始化一个定时器
            self.controlTimer.timeout.connect(self.control_h_start) #计时结束调用operate()方法
            self.controlTimer.start(300) #设置计时间隔 100ms 并启动
        else:
            #set control word to "stop homing", 0x6040, 2byte
            self.writeControlWord(True,gc.cw_stopHoming)
            self.pushButton_control_h_start.setText('Start')
            
            self.pushButton_control_pp_start.setEnabled(True)
            self.pushButton_control_pv_start.setEnabled(True)
            self.pushButton_control_pt_start.setEnabled(True) 
            self.pushButton_control_ip_start.setEnabled(True) 
            self.pushButton_control_csp_start.setEnabled(True) 
            self.pushButton_control_csv_start.setEnabled(True) 
            self.pushButton_control_cst_start.setEnabled(True) 
            
            self.pushButton_control_pp_update.setEnabled(True)
            self.pushButton_control_pv_update.setEnabled(True)
            self.pushButton_control_pt_update.setEnabled(True)
            self.pushButton_control_ip_update.setEnabled(True) 
            self.pushButton_control_csp_update.setEnabled(True) 
            self.pushButton_control_csv_update.setEnabled(True) 
            self.pushButton_control_cst_update.setEnabled(True)  
        pass
    def control_h_start(self):
        #ip模式是透传,和pp/pv/pt类似.
        self.controlTimer.stop()
        self.checkMappedNum = False  
        hStartStatus = True    
        #set control mode to homing mode, 0x6060, 1byte
        self.writeControlMode(True,gc.mode_hm)  
        #set synchronous counter overflow value, 0x1019, 1byte
        #self.writeSynchronousCounterOverflowValue(True) 
        #homing method, 6098, 1byte
        hm = self.comboBox_control_h_hm.currentText()
        self.writeHomingMethod(True,hm)
        #home offset, 607C, int32
        ho = self.lineEdit_control_h_ho.text()
        if ho == '':
            ho = '00'
            self.lineEdit_control_h_ho.setText('0')
        self.writeHomeOffset(True,ho)
        #homing speed1, 6099:01, 4byte
        hs1 = self.lineEdit_control_h_hs1.text()
        if hs1 == '':
            hs1 = '00'
            self.lineEdit_control_h_hs1.setText('0')
        self.writeHomingSpeed1(True,hs1)
        #homing speed2, 6099:02, 4byte
        hs2 = self.lineEdit_control_h_hs2.text()
        if hs2 == '':
            hs2 = '00'
            self.lineEdit_control_h_hs2.setText('0')
        self.writeHomingSpeed2(True,hs2)
        #homing acceleration 0x609A, 4byte
        ha = self.lineEdit_control_h_ha.text() 
        if ha.isdecimal():
            self.writeHomingAcceleration(True,ha)
        else:
            QMessageBox.warning(self,"Error","ha, Wrong Input") 
            hStartStatus = False 
        #发送启动命令
        if hStartStatus == True:
                    
            #set control word to "ready to switch on", 0x6040, 2byte
            self.writeControlWord(True,gc.cw_shutDown)
            self.writeControlWord(True,gc.cw_switchOn)  
            #set control word to "enable operation", 0x6040, 2byte
            self.writeControlWord(True,gc.cw_enableOperation)  
            #nmt operational
            self.writeNMT(True,gc.nmt_operational)
            #enable pdo
            self.enableAllPdo(True)
            #set control word to "start homing", 0x6040, 2byte
            self.writeControlWord(True,gc.cw_startHoming)
            #修改按钮显示.     
            self.pushButton_control_h_start.setText('Stop') 
            self.pushButton_control_h_start.setEnabled(True)
            self.pushButton_control_pp_start.setEnabled(False)
            self.pushButton_control_pv_start.setEnabled(False)
            self.pushButton_control_pt_start.setEnabled(False) 
            self.pushButton_control_ip_start.setEnabled(False) 
            self.pushButton_control_csp_start.setEnabled(False) 
            self.pushButton_control_csv_start.setEnabled(False) 
            self.pushButton_control_cst_start.setEnabled(False)
            
            self.pushButton_control_pp_update.setEnabled(False)
            self.pushButton_control_pv_update.setEnabled(False)
            self.pushButton_control_pt_update.setEnabled(False) 
            self.pushButton_control_ip_update.setEnabled(False) 
            self.pushButton_control_csp_update.setEnabled(False) 
            self.pushButton_control_csv_update.setEnabled(False) 
            self.pushButton_control_cst_update.setEnabled(False)
        else:
            self.pushButton_control_h_start.setEnabled(True)
        pass    

    def pushButton_control_ip_start_clicked(self):
        buttonText = self.pushButton_control_ip_start.text()
        if buttonText == 'Start': 
            self.pushButton_control_ip_start.setEnabled(False)
            #发送nodeid
            self.function.decToHexBytes(self.decNodeid,1)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeCanopenConfigCanNodeid+self.function.getSdoDataStr()])    
            self.tpdoConfig.configTpdo(self.decNodeid)
            self.rpdoConfig.configRpdo(self.decNodeid)
            self.readMappedItemNum(self.decNodeid)
            self.controlTimer = QTimer(self) #初始化一个定时器
            self.controlTimer.timeout.connect(self.control_ip_start) #计时结束调用operate()方法
            self.controlTimer.start(300) #设置计时间隔 100ms 并启动
        else:
            self.function.hexStrToHexBytes('00')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_ip_toggle,'01',self.function.getSdoDataStr()])  
            self.pushButton_control_ip_start.setText('Start') 
            self.checkBox_control_ip_sync.setEnabled(True)   
            self.lineEdit_control_ip_itpv.setEnabled(True)
            self.lineEdit_control_ip_alterTime.setEnabled(True)

            self.pushButton_control_pp_start.setEnabled(True) 
            self.pushButton_control_pv_start.setEnabled(True) 
            self.pushButton_control_pt_start.setEnabled(True)
            self.pushButton_control_h_start.setEnabled(True) 
            self.pushButton_control_csp_start.setEnabled(True) 
            self.pushButton_control_csv_start.setEnabled(True) 
            self.pushButton_control_cst_start.setEnabled(True) 
            
            self.pushButton_control_pp_update.setEnabled(True)
            self.pushButton_control_pv_update.setEnabled(True)
            self.pushButton_control_pt_update.setEnabled(True) 
            self.pushButton_control_csp_update.setEnabled(True) 
            self.pushButton_control_csv_update.setEnabled(True) 
            self.pushButton_control_cst_update.setEnabled(True)
        pass
    def control_ip_start(self): 
        self.controlTimer.stop()
        self.checkMappedNum = False         
        ipStartStatus = True      
        #set control mode to interpolation position mode, 0x6060, 1byte
        self.writeControlMode(True,gc.mode_ipm) 
        #transfer setting to usb2can
        #IPM模式需要的有pa,pd,pv,itpv,tp,和csp模式相同的是,IP模式时,这些数据是发送给usb2can的,
        # 和IPM模式不同的是,target position的内容实际发送到0x60C1, interpolation data record. 
        #set target position, 0x607A, 4byte
        tp = self.lineEdit_control_ip_tp.text()
        if tp == '':
            tp = '00'
            self.lineEdit_control_ip_tp.setText('0')
        self.writeTargetPositionToFlowcan(tp)  
        #set profile velocity, 0x6081, 4byte
        pv = self.lineEdit_control_ip_pv.text()
        if pv.isdecimal():
            self.writeProfileVelocityToFlowcan(pv)
        else:
            QMessageBox.warning(self,"Error","pv, Wrong Input") 
            ipStartStatus = False               
        #set profile acceleration, 0x6083, 4byte
        pa = self.lineEdit_control_ip_pa.text()
        if pa.isdecimal():
            self.writeProfileAccelerationToFlowcan(pa) 
        else:
            QMessageBox.warning(self,"Error","pa, Wrong Input") 
            ipStartStatus = False   
        #set profile deceleration, 0x6084, 4byte
        pd = self.lineEdit_control_ip_pd.text()
        if pd.isdecimal():
            self.writeProfileDecelerationToFlowcan(pd)   
        else:
            QMessageBox.warning(self,"Error","pd, Wrong Input") 
            ipStartStatus = False   
        #set interpolation time period value, 0x60C2:01, 1byte
        itpv = self.lineEdit_control_ip_itpv.text()
        if itpv.isdecimal():
            self.writeInterpolationTimePeriodValue(True,itpv)   
            self.writeInterpolationTimePeriodValueToFlowcan(itpv)                                 
        else:
            QMessageBox.warning(self,"Error","itpv, Wrong Input") 
            ipStartStatus = False   
        #获取alterTime
        alterTime = self.lineEdit_control_ip_alterTime.text()
        if alterTime == '':
            alterTime = '00'
        if alterTime.isdecimal():
            pass
        else:
            QMessageBox.warning(self,"Error","alterTime, Wrong Input") 
            ipStartStatus = False   
        #配置其它nodeid.
        self.writeOtherNodeidToFlowCan()
        if ipStartStatus == True:
            for index in range(len(self.otherNodeidList)):
                self.tpdoConfig.configTpdo(self.otherNodeidList[index])
                self.rpdoConfig.configRpdo(self.otherNodeidList[index])
            #set synchronous counter overflow value, 0x1019, 1byte
            self.writeSynchronousCounterOverflowValue(True)    
            self.configRPDO1(self.decNodeid,'60C10120')
            for index in range(len(self.otherNodeidList)):
                self.configRPDO1(self.otherNodeidList[index],'60C10120')
            #nmt operational
            self.writeNMT(True,gc.nmt_operational)
            #enable pdo
            self.enableAllPdo(True)
            #发送启动命令    
            if self.checkBox_control_ip_sync.isChecked(): 
                self.function.decStrToHexBytes(alterTime,4)  
                isSyncWithData = self.tpdoConfig.getSyncWithDataStatus() 
                if isSyncWithData:
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_ip_toggle,'05','03'+self.function.getSdoDataStr()])   
                else:
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_ip_toggle,'05','01'+self.function.getSdoDataStr()])   
            else:
                self.function.decStrToHexBytes(alterTime,4)   
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_ip_toggle,'05','02'+self.function.getSdoDataStr()])   
            #修改按钮显示.     
            self.pushButton_control_ip_start.setText('Stop')
            self.pushButton_control_ip_start.setEnabled(True)
            self.checkBox_control_ip_sync.setEnabled(False)   
            self.lineEdit_control_ip_itpv.setEnabled(False)
            self.lineEdit_control_ip_alterTime.setEnabled(False)

            self.pushButton_control_pp_start.setEnabled(False) 
            self.pushButton_control_pv_start.setEnabled(False) 
            self.pushButton_control_pt_start.setEnabled(False) 
            self.pushButton_control_h_start.setEnabled(False) 
            self.pushButton_control_csp_start.setEnabled(False) 
            self.pushButton_control_csv_start.setEnabled(False) 
            self.pushButton_control_cst_start.setEnabled(False) 
            
            self.pushButton_control_pp_update.setEnabled(False)
            self.pushButton_control_pv_update.setEnabled(False)
            self.pushButton_control_pt_update.setEnabled(False) 
            self.pushButton_control_csp_update.setEnabled(False) 
            self.pushButton_control_csv_update.setEnabled(False) 
            self.pushButton_control_cst_update.setEnabled(False)  
        else:
            self.pushButton_control_ip_start.setEnabled(True)
        pass    
    def pushButton_control_ip_update_clicked(self):
        cspUpdateStatus = True   
        #set profile velocity, 0x6081, 4byte
        pv = self.lineEdit_control_ip_pv.text()
        if pv.isdecimal():
            self.writeProfileVelocityToFlowcan(pv)              
        else:
            QMessageBox.warning(self,"Error","pv, Wrong Input") 
            cspUpdateStatus = False           
        #set profile acceleration, 0x6083, 4byte
        pa = self.lineEdit_control_ip_pa.text() 
        if pa.isdecimal():
            self.writeProfileAccelerationToFlowcan(pa)
        else:
            QMessageBox.warning(self,"Error","pa, Wrong Input") 
            cspUpdateStatus = False 
        #set profile deceleration, 0x6084, 4byte
        pd = self.lineEdit_control_ip_pd.text() 
        if pd.isdecimal():
            self.writeProfileDecelerationToFlowcan(pd)     
        else:
            QMessageBox.warning(self,"Error","pd, Wrong Input") 
            cspUpdateStatus = False 
        #set target position, 0x607A, 4byte
        tp = self.lineEdit_control_ip_tp.text()
        if tp == '':
            tp = '00'
            self.lineEdit_control_ip_tp.setText('0')
        self.writeTargetPositionToFlowcan(tp)           
        #发送update命令
        if cspUpdateStatus == True:
            self.function.hexStrToHexBytes('01') 
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_ip_update,'01',self.function.getSdoDataStr()])      
        pass
 
    def pushButton_control_csp_start_clicked(self):
        buttonText = self.pushButton_control_csp_start.text()
        if buttonText == 'Start':  
            self.pushButton_control_csp_start.setEnabled(False)
            #发送nodeid
            self.function.decToHexBytes(self.decNodeid,1)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeCanopenConfigCanNodeid+self.function.getSdoDataStr()])  
            self.tpdoConfig.configTpdo(self.decNodeid)
            self.rpdoConfig.configRpdo(self.decNodeid)
            self.readMappedItemNum(self.decNodeid)
            self.controlTimer = QTimer(self) #初始化一个定时器
            self.controlTimer.timeout.connect(self.control_csp_start) #计时结束调用operate()方法
            self.controlTimer.start(300) #设置计时间隔 100ms 并启动
        else:
            self.function.hexStrToHexBytes('00')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_csp_toggle,'01',self.function.getSdoDataStr()])  
            self.pushButton_control_csp_start.setText('Start')
            self.checkBox_control_csp_sync.setEnabled(True)
            self.lineEdit_control_csp_itpv.setEnabled(True)
            self.lineEdit_control_csp_alterTime.setEnabled(True)
            
            self.pushButton_control_pp_start.setEnabled(True) 
            self.pushButton_control_pv_start.setEnabled(True) 
            self.pushButton_control_pt_start.setEnabled(True) 
            self.pushButton_control_h_start.setEnabled(True) 
            self.pushButton_control_ip_start.setEnabled(True) 
            self.pushButton_control_csv_start.setEnabled(True)
            self.pushButton_control_cst_start.setEnabled(True)
            
            self.pushButton_control_pp_update.setEnabled(True)
            self.pushButton_control_pv_update.setEnabled(True)
            self.pushButton_control_pt_update.setEnabled(True) 
            self.pushButton_control_ip_update.setEnabled(True) 
            self.pushButton_control_csv_update.setEnabled(True) 
            self.pushButton_control_cst_update.setEnabled(True) 
        pass     
    def control_csp_start(self):
        self.controlTimer.stop()
        self.checkMappedNum = False 
        cspStartStatus = True    
        #set control mode to interpolation cyclic synchronous position mode, 0x6060, 1byte
        self.writeControlMode(True,gc.mode_cspm)   
        #transfer setting to usb2can
        #CSP模式需要的有pa,pd,pv,itpv,tp,和pp模式不同的是,csp模式时,这些数据是发送给usb2can的,
        #set target position, 0x607A, 4byte
        tp = self.lineEdit_control_csp_tp.text()
        if tp == '':
            tp = '00'
            self.lineEdit_control_csp_tp.setText('0')
        self.writeTargetPositionToFlowcan(tp)   
        #set profile velocity, 0x6081, 4byte
        pv = self.lineEdit_control_csp_pv.text()
        if pv.isdecimal():
            self.writeProfileVelocityToFlowcan(pv)
        else:
            QMessageBox.warning(self,"Error","pv, Wrong Input") 
            cspStartStatus = False               
        #set profile acceleration, 0x6083, 4byte
        pa = self.lineEdit_control_csp_pa.text()
        if pa.isdecimal():
            self.writeProfileAccelerationToFlowcan(pa)  
        else:
            QMessageBox.warning(self,"Error","pa, Wrong Input") 
            cspStartStatus = False   
        #set profile deceleration, 0x6084, 4byte
        pd = self.lineEdit_control_csp_pd.text()
        if pd.isdecimal():
            self.writeProfileDecelerationToFlowcan(pd)   
        else:
            QMessageBox.warning(self,"Error","pd, Wrong Input") 
            cspStartStatus = False   
        #set interpolation time period value, 0x60C2:01, 1byte
        itpv = self.lineEdit_control_csp_itpv.text()
        if itpv.isdecimal():
            self.writeInterpolationTimePeriodValue(True,itpv)   
            self.writeInterpolationTimePeriodValueToFlowcan(itpv)   
        else:
            QMessageBox.warning(self,"Error","itpv, Wrong Input") 
            cspStartStatus = False   
        #获取alterTime
        alterTime = self.lineEdit_control_csp_alterTime.text()
        if alterTime == '':
            alterTime = '00'
        if alterTime.isdecimal():
            pass
        else:
            QMessageBox.warning(self,"Error","alterTime, Wrong Input") 
            cspStartStatus = False      
        #配置其它nodeid.
        self.writeOtherNodeidToFlowCan()
        if cspStartStatus == True:
            for index in range(len(self.otherNodeidList)):
                self.tpdoConfig.configTpdo(self.otherNodeidList[index])
                self.rpdoConfig.configRpdo(self.otherNodeidList[index])
            #set synchronous counter overflow value, 0x1019, 1byte
            self.writeSynchronousCounterOverflowValue(True)  
            self.configRPDO1(self.decNodeid,'607A0020')
            for index in range(len(self.otherNodeidList)):
                self.configRPDO1(self.otherNodeidList[index],'607A0020') 
            #nmt operational
            self.writeNMT(True,gc.nmt_operational)
            #enable pdo
            self.enableAllPdo(True)
            #发送启动命令    
            if self.checkBox_control_csp_sync.isChecked(): 
                self.function.decStrToHexBytes(alterTime,4) 
                isSyncWithData = self.tpdoConfig.getSyncWithDataStatus() 
                if isSyncWithData:
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_csp_toggle,'05','03'+self.function.getSdoDataStr()])   
                else:
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_csp_toggle,'05','01'+self.function.getSdoDataStr()])   
            else:
                self.function.decStrToHexBytes(alterTime,4)   
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_csp_toggle,'05','02'+self.function.getSdoDataStr()])   
            #修改按钮显示.     
            self.pushButton_control_csp_start.setText('Stop')
            self.pushButton_control_csp_start.setEnabled(True)
            self.checkBox_control_csp_sync.setEnabled(False)
            self.lineEdit_control_csp_itpv.setEnabled(False)
            self.lineEdit_control_csp_alterTime.setEnabled(False)
            
            self.pushButton_control_pp_start.setEnabled(False) 
            self.pushButton_control_pv_start.setEnabled(False) 
            self.pushButton_control_pt_start.setEnabled(False) 
            self.pushButton_control_h_start.setEnabled(False) 
            self.pushButton_control_ip_start.setEnabled(False) 
            self.pushButton_control_cst_start.setEnabled(False) 
            self.pushButton_control_csv_start.setEnabled(False)  
                      
            self.pushButton_control_pp_update.setEnabled(False)
            self.pushButton_control_pv_update.setEnabled(False)
            self.pushButton_control_pt_update.setEnabled(False) 
            self.pushButton_control_ip_update.setEnabled(False) 
            self.pushButton_control_csv_update.setEnabled(False) 
            self.pushButton_control_cst_update.setEnabled(False) 
        else:
            self.pushButton_control_csp_start.setEnabled(True)
        pass    
    def pushButton_control_csp_update_clicked(self):
        cspUpdateStatus = True   
        #set profile velocity, 0x6081, 4byte
        pv = self.lineEdit_control_csp_pv.text()
        if pv.isdecimal():
            self.writeProfileVelocityToFlowcan(pv)             
        else:
            QMessageBox.warning(self,"Error","pv, Wrong Input") 
            cspUpdateStatus = False           
        #set profile acceleration, 0x6083, 4byte
        pa = self.lineEdit_control_csp_pa.text() 
        if pa.isdecimal():
            self.writeProfileAccelerationToFlowcan(pa) 
        else:
            QMessageBox.warning(self,"Error","pa, Wrong Input") 
            cspUpdateStatus = False 
        #set profile deceleration, 0x6084, 4byte
        pd = self.lineEdit_control_csp_pd.text() 
        if pd.isdecimal():
            self.writeProfileDecelerationToFlowcan(pd)   
        else:
            QMessageBox.warning(self,"Error","pd, Wrong Input") 
            cspUpdateStatus = False 
        #set target position, 0x607A, 4byte
        tp = self.lineEdit_control_csp_tp.text()
        if tp == '':
            tp = '00'
            self.lineEdit_control_csp_tp.setText('0')
        self.writeTargetPositionToFlowcan(tp)            
        #发送update命令
        if cspUpdateStatus == True:
            self.function.hexStrToHexBytes('01') 
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_csp_update,'01',self.function.getSdoDataStr()])      
        pass
    
    
    def pushButton_control_csv_start_clicked(self):
        buttonText = self.pushButton_control_csv_start.text()
        if buttonText == 'Start': 
            self.pushButton_control_csv_start.setEnabled(False)
            #发送nodeid
            self.function.decToHexBytes(self.decNodeid,1)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeCanopenConfigCanNodeid+self.function.getSdoDataStr()])  
            self.tpdoConfig.configTpdo(self.decNodeid)
            self.rpdoConfig.configRpdo(self.decNodeid)
            self.readMappedItemNum(self.decNodeid)
            self.controlTimer = QTimer(self) #初始化一个定时器
            self.controlTimer.timeout.connect(self.control_csv_start) #计时结束调用operate()方法
            self.controlTimer.start(300) #设置计时间隔 100ms 并启动
        else:
            self.function.hexStrToHexBytes('00')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_csv_toggle,'01',self.function.getSdoDataStr()])  
            self.pushButton_control_csv_start.setText('Start')
            self.checkBox_control_csv_sync.setEnabled(True)
            self.lineEdit_control_csv_itpv.setEnabled(True)
            self.lineEdit_control_csv_alterTime.setEnabled(True)

            self.pushButton_control_pp_start.setEnabled(True) 
            self.pushButton_control_pv_start.setEnabled(True) 
            self.pushButton_control_pt_start.setEnabled(True) 
            self.pushButton_control_h_start.setEnabled(True) 
            self.pushButton_control_ip_start.setEnabled(True) 
            self.pushButton_control_csp_start.setEnabled(True) 
            self.pushButton_control_cst_start.setEnabled(True) 
              
            self.pushButton_control_pp_update.setEnabled(True)
            self.pushButton_control_pv_update.setEnabled(True)
            self.pushButton_control_pt_update.setEnabled(True) 
            self.pushButton_control_ip_update.setEnabled(True) 
            self.pushButton_control_csp_update.setEnabled(True) 
            self.pushButton_control_cst_update.setEnabled(True) 
        pass
    def control_csv_start(self):
        self.controlTimer.stop()
        self.checkMappedNum = False 
        csvStartStatus = True  
        #set control mode to interpolation cyclic synchronous velocity mode, 0x6060, 1byte
        self.writeControlMode(True,gc.mode_csvm)                                              
        #transfer setting to usb2can
        #set target velocity, 0x60FF, 4byte
        tv = self.lineEdit_control_csv_tv.text()
        if tv == '':
            tv = '00'
            self.lineEdit_control_csv_tv.setText('0')
        self.writeTargetVelocityToFlowcan(tv)         
        #set profile acceleration, 0x6083, 4byte
        pa = self.lineEdit_control_csv_pa.text()
        if pa.isdecimal():
            self.writeProfileAccelerationToFlowcan(pa)
        else:
            QMessageBox.warning(self,"Error","pa, Wrong Input") 
            csvStartStatus = False
        #set profile deceleration, 0x6084, 4byte
        pd = self.lineEdit_control_csv_pd.text() 
        if pd.isdecimal(): 
            self.writeProfileDecelerationToFlowcan(pd)    
        else:
            QMessageBox.warning(self,"Error","pd, Wrong Input") 
            csvStartStatus = False
        #set interpolation time period value, 0x60C2:01, 1byte
        itpv = self.lineEdit_control_csv_itpv.text()
        if itpv.isdecimal():
            self.writeInterpolationTimePeriodValue(True,itpv)   
            self.writeInterpolationTimePeriodValueToFlowcan(itpv)   
        else:
            QMessageBox.warning(self,"Error","itpv, Wrong Input") 
            csvStartStatus = False
        #获取alterTime
        alterTime = self.lineEdit_control_csv_alterTime.text()
        if alterTime == '':
            alterTime = '00'
        if alterTime.isdecimal():
            pass
        else:
            QMessageBox.warning(self,"Error","alterTime, Wrong Input") 
            csvStartStatus = False  
        #配置其它nodeid.
        self.writeOtherNodeidToFlowCan()
        if csvStartStatus == True:
            for index in range(len(self.otherNodeidList)):
                self.tpdoConfig.configTpdo(self.otherNodeidList[index])
                self.rpdoConfig.configRpdo(self.otherNodeidList[index])
            #set synchronous counter overflow value, 0x1019, 1byte
            self.writeSynchronousCounterOverflowValue(True)  
            self.configRPDO1(self.decNodeid,'60FF0020')
            for index in range(len(self.otherNodeidList)):
                self.configRPDO1(self.otherNodeidList[index],'60FF0020')
            #nmt operational
            self.writeNMT(True,gc.nmt_operational) 
            #enable pdo
            self.enableAllPdo(True)
            #发送启动命令    
            if self.checkBox_control_csv_sync.isChecked(): 
                self.function.decStrToHexBytes(alterTime,4) 
                isSyncWithData = self.tpdoConfig.getSyncWithDataStatus() 
                if isSyncWithData: 
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_csv_toggle,'05','03'+self.function.getSdoDataStr()])   
                else:
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_csv_toggle,'05','01'+self.function.getSdoDataStr()])   
            else:
                self.function.decStrToHexBytes(alterTime,4)   
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_csv_toggle,'05','02'+self.function.getSdoDataStr()])  
            #修改按钮显示.     
            self.pushButton_control_csv_start.setText('Stop')
            self.pushButton_control_csv_start.setEnabled(True)
            self.checkBox_control_csv_sync.setEnabled(False)
            self.lineEdit_control_csv_itpv.setEnabled(False)
            self.lineEdit_control_csv_alterTime.setEnabled(False)
            
            self.pushButton_control_pp_start.setEnabled(False)    
            self.pushButton_control_pv_start.setEnabled(False)   
            self.pushButton_control_pt_start.setEnabled(False)   
            self.pushButton_control_h_start.setEnabled(False)      
            self.pushButton_control_ip_start.setEnabled(False)      
            self.pushButton_control_csp_start.setEnabled(False) 
            self.pushButton_control_cst_start.setEnabled(False) 
            
            self.pushButton_control_pp_update.setEnabled(False)
            self.pushButton_control_pv_update.setEnabled(False)
            self.pushButton_control_pt_update.setEnabled(False) 
            self.pushButton_control_ip_update.setEnabled(False) 
            self.pushButton_control_csp_update.setEnabled(False) 
            self.pushButton_control_cst_update.setEnabled(False) 
        else:
            self.pushButton_control_csv_start.setEnabled(True)
        pass    
    def pushButton_control_csv_update_clicked(self):  
        csvUpdateStatus = True               
        #set profile acceleration, 0x6083, 4byte
        pa = self.lineEdit_control_csv_pa.text() 
        if pa.isdecimal():
            self.writeProfileAccelerationToFlowcan(pa)
        else:
            QMessageBox.warning(self,"Error","pa, Wrong Input") 
            csvUpdateStatus = False    
        #set profile deceleration, 0x6084, 4byte
        pd = self.lineEdit_control_csv_pd.text()  
        if pd.isdecimal():
            self.writeProfileDecelerationToFlowcan(pd)   
        else:
            QMessageBox.warning(self,"Error","pd, Wrong Input") 
            csvUpdateStatus = False  
        #set target velocity, 0x60FF, 4byte
        tv = self.lineEdit_control_csv_tv.text()
        if tv == '':
            tv = '00'
            self.lineEdit_control_csv_tv.setText('0')
        self.writeTargetVelocityToFlowcan(tv)      
        #发送update命令
        if csvUpdateStatus == True:
            self.function.hexStrToHexBytes('01') 
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_csv_update,'01',self.function.getSdoDataStr()])      
        pass   

    
    def pushButton_control_cst_start_clicked(self):
        buttonText = self.pushButton_control_cst_start.text()
        if buttonText == 'Start': 
            self.pushButton_control_cst_start.setEnabled(False)
            #发送nodeid
            self.function.decToHexBytes(self.decNodeid,1)   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeCanopenConfigCanNodeid+self.function.getSdoDataStr()])  
            self.tpdoConfig.configTpdo(self.decNodeid)
            self.rpdoConfig.configRpdo(self.decNodeid)
            self.readMappedItemNum(self.decNodeid)
            self.controlTimer = QTimer(self) #初始化一个定时器
            self.controlTimer.timeout.connect(self.control_cst_start) #计时结束调用operate()方法
            self.controlTimer.start(300) #设置计时间隔 100ms 并启动
        else:
            self.function.hexStrToHexBytes('00')   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_cst_toggle,'01',self.function.getSdoDataStr()])  
            self.pushButton_control_cst_start.setText('Start')
            self.checkBox_control_cst_sync.setEnabled(True)
            self.lineEdit_control_cst_itpv.setEnabled(True)
            self.lineEdit_control_cst_alterTime.setEnabled(True)

            self.pushButton_control_pp_start.setEnabled(True) 
            self.pushButton_control_pv_start.setEnabled(True) 
            self.pushButton_control_pt_start.setEnabled(True)
            self.pushButton_control_h_start.setEnabled(True) 
            self.pushButton_control_ip_start.setEnabled(True) 
            self.pushButton_control_csp_start.setEnabled(True) 
            self.pushButton_control_csv_start.setEnabled(True)
            
            self.pushButton_control_pp_update.setEnabled(True)
            self.pushButton_control_pv_update.setEnabled(True)
            self.pushButton_control_pt_update.setEnabled(True) 
            self.pushButton_control_ip_update.setEnabled(True) 
            self.pushButton_control_csp_update.setEnabled(True) 
            self.pushButton_control_csv_update.setEnabled(True) 
        pass    
        pass
    
    def control_cst_start(self):
        self.controlTimer.stop()
        self.checkMappedNum = False 
        cstStartStatus = True        
        #set control mode to interpolation cyclic synchronous torque mode, 0x6060, 1byte
        self.writeControlMode(True,gc.mode_cstm)  
        #set target torque, 0x6071, 2byte
        tt = self.lineEdit_control_cst_tt.text()
        if tt == '':
            tt = '00'
            self.lineEdit_control_cst_tt.setText('0')
        self.writeTargetTorqueToFlowcan(tt)  
        #set torque slope, 0x6087, 4byte
        ts = self.lineEdit_control_cst_ts.text() 
        if ts.isdecimal():
            self.writeTorqueSlopeToFlowcan(ts)    
        else:
            QMessageBox.warning(self,"Error","ts, Wrong Input") 
            cstStartStatus = False 
        #set interpolation time period value, 0x60C2:01, 1byte
        #set communication cycle period, 0x1006, 4byte, us
        itpv = self.lineEdit_control_cst_itpv.text()
        if itpv.isdecimal():
            self.writeInterpolationTimePeriodValue(True,itpv)   
            self.writeInterpolationTimePeriodValueToFlowcan(itpv)   
        else:
            QMessageBox.warning(self,"Error","itpv, Wrong Input") 
            cstStartStatus = False 
        #获取alterTime
        alterTime = self.lineEdit_control_cst_alterTime.text()
        if alterTime == '':
            alterTime = '00'
        if alterTime.isdecimal():
            pass
        else:
            QMessageBox.warning(self,"Error","alterTime, Wrong Input") 
            cstStartStatus = False  
        #配置其它nodeid.
        self.writeOtherNodeidToFlowCan()
        if cstStartStatus == True:
            for index in range(len(self.otherNodeidList)):
                self.tpdoConfig.configTpdo(self.otherNodeidList[index])
                self.rpdoConfig.configRpdo(self.otherNodeidList[index])
            #set synchronous counter overflow value, 0x1019, 1byte
            self.writeSynchronousCounterOverflowValue(True)  
            self.configRPDO1(self.decNodeid,'60710010')
            for index in range(len(self.otherNodeidList)):
                self.configRPDO1(self.otherNodeidList[index],'60710010')
            #nmt operational
            self.writeNMT(True,gc.nmt_operational) 
            self.enableAllPdo(True) 
            #发送启动命令    
            if self.checkBox_control_cst_sync.isChecked(): 
                self.function.decStrToHexBytes(alterTime,4)  
                isSyncWithData = self.tpdoConfig.getSyncWithDataStatus() 
                if isSyncWithData: 
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_cst_toggle,'05','03'+self.function.getSdoDataStr()])   
                else:
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_cst_toggle,'05','01'+self.function.getSdoDataStr()])   
            else:
                self.function.decStrToHexBytes(alterTime,4)   
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_cst_toggle,'05','02'+self.function.getSdoDataStr()])  
                                        
            #修改按钮显示.     
            self.pushButton_control_cst_start.setText('Stop')
            self.pushButton_control_cst_start.setEnabled(True)
            self.checkBox_control_cst_sync.setEnabled(False)
            self.lineEdit_control_cst_itpv.setEnabled(False)
            self.lineEdit_control_cst_alterTime.setEnabled(False)
            
            self.pushButton_control_pp_start.setEnabled(False) 
            self.pushButton_control_pv_start.setEnabled(False) 
            self.pushButton_control_pt_start.setEnabled(False) 
            self.pushButton_control_h_start.setEnabled(False) 
            self.pushButton_control_ip_start.setEnabled(False) 
            self.pushButton_control_csp_start.setEnabled(False) 
            self.pushButton_control_csv_start.setEnabled(False)
            
            self.pushButton_control_pp_update.setEnabled(False)
            self.pushButton_control_pv_update.setEnabled(False)
            self.pushButton_control_pt_update.setEnabled(False) 
            self.pushButton_control_ip_update.setEnabled(False) 
            self.pushButton_control_csp_update.setEnabled(False) 
            self.pushButton_control_csv_update.setEnabled(False) 
        else:
            self.pushButton_control_cst_start.setEnabled(True)
        pass
    def pushButton_control_cst_update_clicked(self):
        cstUpdateStatus = True                     
        #set torque slope, 0x6087, 4byte
        ts = self.lineEdit_control_cst_ts.text()
        if ts.isdecimal():
            self.writeTorqueSlopeToFlowcan(ts)           
        else:
            QMessageBox.warning(self,"Error","ts, Wrong Input") 
            cstUpdateStatus = False 
        #set target torque, 0x6071, 2byte
        tt = self.lineEdit_control_cst_tt.text()
        if tt == '':
            tt = '00'
            self.lineEdit_control_cst_tt.setText('0')
        self.writeTargetTorqueToFlowcan(tt)             
        if cstUpdateStatus == True:
            #发送update命令
            self.function.hexStrToHexBytes('01') 
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_cst_update,'01',self.function.getSdoDataStr()])              
        pass
    
    def configRPDO1(self,decNodeid,map):
        cobid_TSDO     = (str(hex(decNodeid+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
        #disable pdo1
        self.function.hexStrToHexBytes(str(hex(decNodeid+gc.cobid_RPDO1+0x80000000).replace('0x','')))    
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1Cobid+self.function.getSdoDataStr()])
        #clear rpdo1, 1600:00,1byte
        self.function.hexStrToHexBytes('00')   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1NumberOfMappedObjects+self.function.getSdoDataStr()])
        #transmission type
        if self.checkBox_control_ip_sync.isChecked():
            self.function.hexStrToHexBytes('01')   
        else: 
            self.function.hexStrToHexBytes('FF')   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1TransmissionType+self.function.getSdoDataStr()])
        #data
        self.function.hexStrToHexBytes(map)
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1MappedObject1+self.function.getSdoDataStr()])
        #number of mapped
        self.function.hexStrToHexBytes('01')   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1NumberOfMappedObjects+self.function.getSdoDataStr()])   
        #enable pdo1
        self.RpdoMapStatus[0] = True
        pass
    def readMappedItemNum(self,decNodeid):
        strTSDO = (str(hex(decNodeid+0x600)).replace('0x','')).zfill(3).upper()
        #tpdo1 mapping
        self.checkMappedNum = True
        self.function.decStrToHexBytes('0',1)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,strTSDO,'08',gc.readTPDO1NumberOfMappedObjects + self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,strTSDO,'08',gc.readTPDO2NumberOfMappedObjects + self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,strTSDO,'08',gc.readTPDO3NumberOfMappedObjects + self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,strTSDO,'08',gc.readTPDO4NumberOfMappedObjects + self.function.getSdoDataStr()])
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,strTSDO,'08',gc.readRPDO1NumberOfMappedObjects + self.function.getSdoDataStr()])  
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,strTSDO,'08',gc.readRPDO2NumberOfMappedObjects + self.function.getSdoDataStr()])  
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,strTSDO,'08',gc.readRPDO3NumberOfMappedObjects + self.function.getSdoDataStr()])  
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,strTSDO,'08',gc.readRPDO4NumberOfMappedObjects + self.function.getSdoDataStr()])
        pass                     
    def enableAllPdo(self,isall):
        cobid_TSDO     = (str(hex(self.decNodeid+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
        if self.TpdoMapStatus[0] == True:
            self.function.hexStrToHexBytes(str(hex(gc.cobid_TPDO1+self.decNodeid+0x00000000).replace('0x','')))   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1Cobid+self.function.getSdoDataStr()])   
        if self.TpdoMapStatus[1] == True:    
            self.function.hexStrToHexBytes(str(hex(gc.cobid_TPDO2+self.decNodeid+0x00000000).replace('0x','')))   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2Cobid+self.function.getSdoDataStr()])
        if self.TpdoMapStatus[2] == True:    
            self.function.hexStrToHexBytes(str(hex(gc.cobid_TPDO3+self.decNodeid+0x00000000).replace('0x','')))   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3Cobid+self.function.getSdoDataStr()]) 
        if self.TpdoMapStatus[3] == True:    
            self.function.hexStrToHexBytes(str(hex(gc.cobid_TPDO4+self.decNodeid+0x00000000).replace('0x','')))   
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4Cobid+self.function.getSdoDataStr()])  
        if self.RpdoMapStatus[0] == True:    
            self.function.hexStrToHexBytes(str(hex(gc.cobid_RPDO1+self.decNodeid+0x00000000).replace('0x','')))    
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1Cobid+self.function.getSdoDataStr()]) 
        if self.RpdoMapStatus[1] == True:    
            self.function.hexStrToHexBytes(str(hex(gc.cobid_RPDO2+self.decNodeid+0x00000000).replace('0x','')))     
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2Cobid+self.function.getSdoDataStr()]) 
        if self.RpdoMapStatus[2] == True:    
            self.function.hexStrToHexBytes(str(hex(gc.cobid_RPDO3+self.decNodeid+0x00000000).replace('0x','')))    
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3Cobid+self.function.getSdoDataStr()])
        if self.RpdoMapStatus[3] == True:    
            self.function.hexStrToHexBytes(str(hex(gc.cobid_RPDO4+self.decNodeid+0x00000000).replace('0x','')))     
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4Cobid+self.function.getSdoDataStr()]) 
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO     = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                if self.TpdoMapStatus[0] == True:
                    self.function.hexStrToHexBytes(str(hex(gc.cobid_TPDO1+self.otherNodeidList[index]+0x00000000).replace('0x','')))   
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO1Cobid+self.function.getSdoDataStr()])   
                if self.TpdoMapStatus[1] == True:    
                    self.function.hexStrToHexBytes(str(hex(gc.cobid_TPDO2+self.otherNodeidList[index]+0x00000000).replace('0x','')))   
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO2Cobid+self.function.getSdoDataStr()])
                if self.TpdoMapStatus[2] == True:    
                    self.function.hexStrToHexBytes(str(hex(gc.cobid_TPDO3+self.otherNodeidList[index]+0x00000000).replace('0x','')))   
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO3Cobid+self.function.getSdoDataStr()]) 
                if self.TpdoMapStatus[3] == True:    
                    self.function.hexStrToHexBytes(str(hex(gc.cobid_TPDO4+self.otherNodeidList[index]+0x00000000).replace('0x','')))   
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTPDO4Cobid+self.function.getSdoDataStr()])  
                if self.RpdoMapStatus[0] == True:    
                    self.function.hexStrToHexBytes(str(hex(gc.cobid_RPDO1+self.otherNodeidList[index]+0x00000000).replace('0x','')))    
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO1Cobid+self.function.getSdoDataStr()]) 
                if self.RpdoMapStatus[1] == True:    
                    self.function.hexStrToHexBytes(str(hex(gc.cobid_RPDO2+self.otherNodeidList[index]+0x00000000).replace('0x','')))     
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO2Cobid+self.function.getSdoDataStr()]) 
                if self.RpdoMapStatus[2] == True:    
                    self.function.hexStrToHexBytes(str(hex(gc.cobid_RPDO3+self.otherNodeidList[index]+0x00000000).replace('0x','')))    
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO3Cobid+self.function.getSdoDataStr()])
                if self.RpdoMapStatus[3] == True:    
                    self.function.hexStrToHexBytes(str(hex(gc.cobid_RPDO4+self.otherNodeidList[index]+0x00000000).replace('0x','')))     
                    self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeRPDO4Cobid+self.function.getSdoDataStr()]) 
        pass

    def pushButton_log_saveToFile_clicked(self):
        buttonText = self.pushButton_log_saveToFile.text()
        if buttonText == 'Start Save':
            self.pushButton_log_saveToFile.setText('Stop Save')
            self.timestr = time.strftime("%Y%m%d%H%M%S")
            with open(self.timestr+'.csv','w',newline='',encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile,delimiter=',')
                writer.writerow(['No.','ms','TR','rtr','cobid','len','data'])
                self.CurrentCsvIO = open(self.timestr+'.csv','a',newline='',encoding='utf-8')
                self.enableLog = True
        else:
            self.enableLog = False
            self.pushButton_log_saveToFile.setText('Start Save')
            self.CurrentCsvIO.close()
        pass
    
    def pushButton_log_clearAll_clicked(self):
        self.tableWidget_log.clearContents()
        self.logQueue.clear()
        pass
    def pushButton_log_refresh_clicked(self):
        buttonText = self.pushButton_log_refresh.text()
        if buttonText == 'Stop Refresh':
            self.pushButton_log_refresh.setText('Start Refresh')
            self.enableRefreshLog = False
        else:
            self.pushButton_log_refresh.setText('Stop Refresh')
            self.enableRefreshLog = True
        pass    
    def pushButton_error_clearErr_clicked(self):
        self.tableWidget_error.clearContents()
        self.errorQueue.clear()
        pass
    
    def pushButton_diagram_resetY_clicked(self):
        self.YMax = 0
        self.YMin = 0
        self.plotYMax = 0
        self.plotYMin = 0
        pass
    
    def pushButton_diagram_refresh_clicked(self):
        buttonText = self.pushButton_diagram_refresh.text()
        if buttonText == 'Stop Refresh':
            self.pushButton_diagram_refresh.setText('Start Refresh')
            self.enableRefreshDiagram = False
        else:
            self.pushButton_diagram_refresh.setText('Stop Refresh')
            self.enableRefreshDiagram = True
        pass   
            
    def updateTpdo1Data1(self,configList):
        self.Tpdo1Value1List = configList
        if self.Tpdo1Value1List[0]:
            if self.curveTpdo1Data1 is None:
                # color=红色=255,0,0
                pen=pg.mkPen(color=(255,0,0), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo1Data1 = self.plotWidget_diagram.plot(self.arrayTpdo1Data1,pen=pen, name='''<font size="1">{}</font>'''.format('data11'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo1Data1)
            self.curveTpdo1Data1 = None
    def updateTpdo1Data2(self,configList):
        self.Tpdo1Value2List = configList 
        if self.Tpdo1Value2List[0]:
            if self.curveTpdo1Data2 is None:
                # color=印度红=178,34,34
                pen=pg.mkPen(color=(178,34,34), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo1Data2 = self.plotWidget_diagram.plot(self.arrayTpdo1Data2,pen=pen, name='''<font size="1">{}</font>'''.format('data12'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo1Data2)
            self.curveTpdo1Data2 = None
    def updateTpdo1Data3(self,configList):
        self.Tpdo1Value3List = configList
        if self.Tpdo1Value3List[0]:
            if self.curveTpdo1Data3 is None:
                # color=深红=255,0,255
                pen=pg.mkPen(color=(255,0,255), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo1Data3 = self.plotWidget_diagram.plot(self.arrayTpdo1Data3,pen=pen, name='''<font size="1">{}</font>'''.format('data13'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo1Data3)
            self.curveTpdo1Data3 = None
    def updateTpdo1Data4(self,configList):
        self.Tpdo1Value4List = configList 
        if self.Tpdo1Value4List[0]:
            if self.curveTpdo1Data4 is None:
                # color=番茄红=255,99,71
                pen=pg.mkPen(color=(255,99,71), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo1Data4 = self.plotWidget_diagram.plot(self.arrayTpdo1Data4,pen=pen, name='''<font size="1">{}</font>'''.format('data14'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo1Data4)
            self.curveTpdo1Data4 = None
        pass
    def updateTpdo2Data1(self,configList):
        self.Tpdo2Value1List = configList
        if self.Tpdo2Value1List[0] :
            if self.curveTpdo2Data1 is None:
                # color=蓝色=0,0,255
                pen=pg.mkPen(color=(0,0,255), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo2Data1 = self.plotWidget_diagram.plot(self.arrayTpdo2Data1,pen=pen, name='''<font size="1">{}</font>'''.format('data21'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo2Data1)
            self.curveTpdo2Data1 = None
    def updateTpdo2Data2(self,configList):
        self.Tpdo2Value2List = configList 
        if self.Tpdo2Value2List[0]:
            if self.curveTpdo2Data2 is None:
                # color=深蓝色=25,25,112
                pen=pg.mkPen(color=(25,25,112), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo2Data2 = self.plotWidget_diagram.plot(self.arrayTpdo2Data2,pen=pen, name='''<font size="1">{}</font>'''.format('data22'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo2Data2)
            self.curveTpdo2Data2 = None
    def updateTpdo2Data3(self,configList):
        self.Tpdo2Value3List = configList
        if self.Tpdo2Value3List[0]:
            if self.curveTpdo2Data3 is None:
                # color=孔雀蓝=51,161,201
                pen=pg.mkPen(color=(51,161,201), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo2Data3 = self.plotWidget_diagram.plot(self.arrayTpdo2Data3,pen=pen, name='''<font size="1">{}</font>'''.format('data23'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo2Data3)
            self.curveTpdo2Data3 = None
    def updateTpdo2Data4(self,configList):
        self.Tpdo2Value4List = configList 
        if self.Tpdo2Value4List[0]:
            if self.curveTpdo2Data4 is None:
                # color=钴色=61,89,171
                pen=pg.mkPen(color=(61,89,171), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo2Data4 = self.plotWidget_diagram.plot(self.arrayTpdo2Data4,pen=pen, name='''<font size="1">{}</font>'''.format('data24'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo2Data4)
            self.curveTpdo2Data4 = None
        pass
    def updateTpdo3Data1(self,configList):
        self.Tpdo3Value1List = configList
        if self.Tpdo3Value1List[0]:
            if self.curveTpdo3Data1 is None:
                # color=绿色=0,255,0
                pen=pg.mkPen(color=(0, 255, 0), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo3Data1 = self.plotWidget_diagram.plot(self.arrayTpdo3Data1,pen=pen, name='''<font size="1">{}</font>'''.format('data31'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo3Data1)
            self.curveTpdo3Data1 = None
    def updateTpdo3Data2(self,configList):
        self.Tpdo3Value2List = configList 
        if self.Tpdo3Value2List[0]:
            if self.curveTpdo3Data2 is None:
                # color=森林绿=34,139,34   
                pen=pg.mkPen(color=(34,139,34), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo3Data2 = self.plotWidget_diagram.plot(self.arrayTpdo3Data2,pen=pen, name='''<font size="1">{}</font>'''.format('data32'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo3Data2)
            self.curveTpdo3Data2 = None
    def updateTpdo3Data3(self,configList):
        self.Tpdo3Value3List = configList
        if self.Tpdo3Value3List[0]:
            if self.curveTpdo3Data3 is None:
                # color=黄绿色=127,255,0
                pen=pg.mkPen(color=(127,255,0), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo3Data3 = self.plotWidget_diagram.plot(self.arrayTpdo3Data3,pen=pen, name='''<font size="1">{}</font>'''.format('data33'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo3Data3)
            self.curveTpdo3Data3 = None
    def updateTpdo3Data4(self,configList):
        self.Tpdo3Value4List = configList 
        if self.Tpdo3Value4List[0]:
            if self.curveTpdo3Data4 is None:
                # color=绿土=56,94,15
                pen=pg.mkPen(color=(56,94,15), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo3Data4 = self.plotWidget_diagram.plot(self.arrayTpdo3Data4,pen=pen, name='''<font size="1">{}</font>'''.format('data34'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo3Data4)
            self.curveTpdo3Data4 = None
        pass
    def updateTpdo4Data1(self,configList):
        self.Tpdo4Value1List = configList
        if self.Tpdo4Value1List[0]:
            if self.curveTpdo4Data1 is None:
                # color=黑色=0,0,0
                pen=pg.mkPen(color=(0,0,0), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo4Data1 = self.plotWidget_diagram.plot(self.arrayTpdo4Data1,pen=pen, name='''<font size="1">{}</font>'''.format('data41'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo4Data1)
            self.curveTpdo4Data1 = None
        pass

    def updateTpdo4Data2(self,configList):
        self.Tpdo4Value2List = configList 
        if self.Tpdo4Value2List[0]:
            if self.curveTpdo4Data2 is None:
                # color=灰色=192,192,192
                pen=pg.mkPen(color=(192,192,192), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo4Data2 = self.plotWidget_diagram.plot(self.arrayTpdo4Data2,pen=pen, name='''<font size="1">{}</font>'''.format('data42'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo4Data2)
            self.curveTpdo4Data2 = None
    def updateTpdo4Data3(self,configList):
        self.Tpdo4Value3List = configList
        if self.Tpdo4Value3List[0]:
            if self.curveTpdo4Data3 is None:
                # color=棕色=128,42,42
                pen=pg.mkPen(color=(128,42,42), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo4Data3 = self.plotWidget_diagram.plot(self.arrayTpdo4Data3,pen=pen, name='''<font size="1">{}</font>'''.format('data43'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo4Data3)
            self.curveTpdo4Data3 = None
    def updateTpdo4Data4(self,configList):
        self.Tpdo4Value4List = configList 
        if self.Tpdo4Value4List[0]:
            if self.curveTpdo4Data4 is None:
                # color=乌贼棕=94,38,38
                pen=pg.mkPen(color=(94,38,38), width=3, style=QtCore.Qt.SolidLine)
                self.curveTpdo4Data4 = self.plotWidget_diagram.plot(self.arrayTpdo4Data4,pen=pen, name='''<font size="1">{}</font>'''.format('data44'))
        else:
            self.plotWidget_diagram.removeItem(self.curveTpdo4Data4)
            self.curveTpdo4Data4 = None
        pass

    #有状态的版本,将最新数据更新到内存log撞墙q中,然后全量flush到ui显示
    def pushLogData(self,rcvFrameArr):
        self.logQueue.push(rcvFrameArr)
        timeDiffStr = None
        try:
            timeDiffStr = self.getTimeDiff(rcvFrameArr[0])
        except ValueError:
            print("[error]main.pushLogData:hex转换出错,原始字符串:",rcvFrameArr[0])
            return
        
        #记录到csv
        if self.enableLog == True:
            writer = csv.writer(self.CurrentCsvIO,delimiter=',')
            #writer.writerow([str(int(rcvFrameArr[1].replace(' ','0'),16)),timeDiffStr,rcvFrameArr[2],rcvFrameArr[3],rcvFrameArr[4],rcvFrameArr[5],rcvFrameArr[6]])
            writer.writerow([str(int(rcvFrameArr[0],16)),rcvFrameArr[1],rcvFrameArr[2],rcvFrameArr[3],rcvFrameArr[4],rcvFrameArr[5],rcvFrameArr[6]])
        pass
    def getTimeDiff(self,currentTime):
        currentTimeStamp = int(currentTime,16)
        decDiff = (currentTimeStamp - self.lastTimeStamp)%4294967295
        self.lastTimeStamp = currentTimeStamp
        return str(decDiff)

    def logRefresh(self):   
        #flush到显示中
        if self.enableRefreshLog:
            self.logQueue.resetRead()
            qheadData = self.logQueue.readHead()
            currentRowNum = 0
            while qheadData != None:
                self.logDisplayOneRow(currentRowNum,qheadData)
                currentRowNum += 1
                qheadData = self.logQueue.readHead()
            if self.isThereNewData:
                self.tableWidget_log.setCurrentCell(self.logQueue.getLength()-1,0) #鼠标改为最后一行
                self.isThereNewData = False
        pass
    
    #随机读写,无状态的版本,写一行
    def logDisplayOneRow(self,rowNum,item):
        rcvFrameArr = item.getData()
        #print(rcvFrameArr)
        #第1列为No.编号
        try:
            self.tableWidget_log.setItem(rowNum, 0, QTableWidgetItem(str(int(rcvFrameArr[gc.rcvFrameIndex_Num],16))))
        except:
            print(rcvFrameArr)
        #第2列timeDiff
        tempitem = QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Time])
        tempitem.setForeground(QtGui.QBrush(Qt.black))
        self.tableWidget_log.setItem(rowNum, 1, tempitem)
        #self.tableWidget_log.setItem(rowNum, 1, QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Time]))
        #第3列为类型,发送是T,接收是R
        tempitem = QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_TR])
        tempitem.setForeground(QtGui.QBrush(Qt.black))
        self.tableWidget_log.setItem(rowNum, 2, tempitem)
        #self.tableWidget_log.setItem(rowNum, 2, QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_TR]))
        #第4列为rtr
        tempitem = QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Rtr])
        tempitem.setForeground(QtGui.QBrush(Qt.black))
        self.tableWidget_log.setItem(rowNum, 3, tempitem)
        #self.tableWidget_log.setItem(rowNum, 3, QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Rtr]))
        #第5列为cobid
        tempitem = QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Cobid])
        tempitem.setForeground(QtGui.QBrush(Qt.black))
        self.tableWidget_log.setItem(rowNum, 4, tempitem)
        #self.tableWidget_log.setItem(rowNum, 4, QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Cobid]))
        #第6列为len
        tempitem = QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Len])
        tempitem.setForeground(QtGui.QBrush(Qt.black))
        self.tableWidget_log.setItem(rowNum, 5, tempitem)
        #self.tableWidget_log.setItem(rowNum, 5, QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Len]))
        #第7列为data
        tempitem = QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Data])
        tempitem.setForeground(QtGui.QBrush(Qt.black))
        self.tableWidget_log.setItem(rowNum, 6, tempitem)
        #self.tableWidget_log.setItem(rowNum, 6, QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Data]))                                
        pass

    def pushErrorData(self,rcvFrameArr):
        self.errorQueue.push(rcvFrameArr)
    
    def errorRefresh(self):   
        #flush到显示中
        self.errorQueue.resetRead()
        qheadData = self.errorQueue.readHead()
        currentRowNum = 0
        while qheadData != None:
            self.errorDisplayOneRow(currentRowNum,qheadData)
            currentRowNum += 1
            qheadData = self.errorQueue.readHead()
        #self.tableWidget_error.setCurrentCell(self.errorQueue.getLength()-1,0) #鼠标改为最后一行
    
    #随机读写,无状态的版本,写一行
    def errorDisplayOneRow(self,rowNum,item):
        rcvFrameArr = item.getData()
        #第1列为No.编号
        tempitem = QTableWidgetItem(str(int(rcvFrameArr[gc.rcvFrameIndex_Num],16)))
        tempitem.setForeground(QtGui.QBrush(Qt.red))
        self.tableWidget_error.setItem(rowNum, 0, tempitem)
        #self.tableWidget_error.setItem(rowNum, 0, QTableWidgetItem(str(int(rcvFrameArr[gc.rcvFrameIndex_Num],16))))
        #第2列timeDiff
        tempitem = QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Time])
        tempitem.setForeground(QtGui.QBrush(Qt.red))
        self.tableWidget_error.setItem(rowNum, 1, tempitem)
        #self.tableWidget_error.setItem(rowNum, 1, QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Time]))
        #第3列为类型,发送是T,接收是R
        tempitem = QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_TR])
        tempitem.setForeground(QtGui.QBrush(Qt.red))
        self.tableWidget_error.setItem(rowNum, 2, tempitem)
        #self.tableWidget_error.setItem(rowNum, 2, QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_TR]))
        #第4列为rtr
        tempitem = QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Rtr])
        tempitem.setForeground(QtGui.QBrush(Qt.red))
        self.tableWidget_error.setItem(rowNum, 3, tempitem)
        #self.tableWidget_error.setItem(rowNum, 3, QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Rtr]))
        #第5列为cobid
        tempitem = QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Cobid])
        tempitem.setForeground(QtGui.QBrush(Qt.red))
        self.tableWidget_error.setItem(rowNum, 4, tempitem)
        #self.tableWidget_error.setItem(rowNum, 4, QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Cobid]))
        #第6列为len
        tempitem = QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Len])
        tempitem.setForeground(QtGui.QBrush(Qt.red))
        self.tableWidget_error.setItem(rowNum, 5, tempitem)
        #self.tableWidget_error.setItem(rowNum, 5, QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Len])) 
        #第7列为data
        tempitem = QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Data])
        tempitem.setForeground(QtGui.QBrush(Qt.red))
        self.tableWidget_error.setItem(rowNum, 6, tempitem)
        #self.tableWidget_error.setItem(rowNum, 6, QTableWidgetItem(rcvFrameArr[gc.rcvFrameIndex_Data]))                                
        pass

    def updateFlowCanStatus(self,statusString):
        self.label_flowcan_status.setText(statusString)
        pass
    def updateUsb2canVersion(self,softwareversion,hardwareversion):
        self.setWindowTitle(self.mianWindowTitle+','+softwareversion+','+hardwareversion)
        pass
    def processCurrentFrame(self,currentFrameArr):
        self.isThereNewData = True
        #存储到log中去
        self.pushLogData(currentFrameArr)
        #解析数据,根据数据类型的不同,往不同的地方更新
        frameCobid  = currentFrameArr[gc.rcvFrameIndex_Cobid]      #字符串的cobid
        intCobid    = int(frameCobid,16) 
        #frameLen    = int(currentFrameArr[gc.rcvFrameIndex_Len],16)    
        #frameRtr    = int(currentFrameArr[gc.rcvFrameIndex_Rtr],16)    
        #frameData   = int(currentFrameArr[gc.rcvFrameIndex_Data],16)  
        #if (frameCobid == self.cobid_RSDO) :
        if (intCobid == self.decNodeid+gc.cobid_RSDO) :
            #这个范围为收到的sdo的返回,那么看看是否需要更新SR的value
            sdoStatus   = currentFrameArr[gc.rcvFrameIndex_Data][0:2]
            sdoIndex    = currentFrameArr[gc.rcvFrameIndex_Data][6:8] +currentFrameArr[gc.rcvFrameIndex_Data][3:5]
            sdoSubindex = currentFrameArr[gc.rcvFrameIndex_Data][9:11]
            sdoData     = currentFrameArr[gc.rcvFrameIndex_Data][21:23] + currentFrameArr[gc.rcvFrameIndex_Data][18:20]\
                             + currentFrameArr[gc.rcvFrameIndex_Data][15:17] + currentFrameArr[gc.rcvFrameIndex_Data][12:14]      
            if sdoStatus == gc.sdo_rspd_abortion:
                #往error里面写入数据,TODO
                self.pushErrorData(currentFrameArr)    
                pass   
            elif sdoStatus == gc.sdo_rspd or sdoStatus == gc.sdo_rspd_1byte or sdoStatus == gc.sdo_rspd_2byte or sdoStatus == gc.sdo_rspd_3byte or sdoStatus == gc.sdo_rspd_4byte:
                if sdoIndex == self.lineEdit_esdo_index.text() and sdoSubindex == self.lineEdit_esdo_subindex.text(): 
                    #收到的SDO回复,对的上的话,填写value.
                    if self.checkBox_esdo_hex.isChecked():
                        self.lineEdit_esdo_rData.setText(sdoData)
                        pass
                    else:
                        tempLen = int(self.comboBox_esdo_len.currentText())
                        tempdata = int.from_bytes(bytes.fromhex(sdoData), byteorder='big', signed=True)
                        self.lineEdit_esdo_rData.setText(str(tempdata))
                if self.checkMappedNum == True:
                    #print('sdoIndex=',sdoIndex)
                    #print('sdoSubindex=',sdoSubindex)
                    #print('sdoData=',sdoData)
                    if sdoIndex == '1A00' and sdoSubindex == '00':
                        if int(sdoData,16) != 0:
                            self.TpdoMapStatus[0] = True
                        else:
                            self.TpdoMapStatus[0] = False
                        #print('TpdoMapStatus[0]',self.TpdoMapStatus[0])
                    if sdoIndex == '1A01' and sdoSubindex == '00':
                        if int(sdoData,16) != 0:
                            self.TpdoMapStatus[1] = True
                        else:
                            self.TpdoMapStatus[1] = False
                        #print('TpdoMapStatus[1]',self.TpdoMapStatus[1])
                    if sdoIndex == '1A02' and sdoSubindex == '00':
                        if int(sdoData,16) != 0:
                            self.TpdoMapStatus[2] = True
                        else:
                            self.TpdoMapStatus[2] = False
                        #print('TpdoMapStatus[2]',self.TpdoMapStatus[2])
                    if sdoIndex == '1A03' and sdoSubindex == '00':
                        if int(sdoData,16) != 0:
                            self.TpdoMapStatus[3] = True
                        else:
                            self.TpdoMapStatus[3] = False
                        #print('TpdoMapStatus[3]',self.TpdoMapStatus[3])
                    if sdoIndex == '1600' and sdoSubindex == '00':
                        if int(sdoData,16) != 0:
                            self.RpdoMapStatus[0] = True
                        else:
                            self.RpdoMapStatus[0] = False
                        #print('RpdoMapStatus[0]',self.RpdoMapStatus[0])
                    if sdoIndex == '1601' and sdoSubindex == '00':
                        if int(sdoData,16) != 0:
                            self.RpdoMapStatus[1] = True
                        else:
                            self.RpdoMapStatus[1] = False
                        #print('RpdoMapStatus[1]',self.RpdoMapStatus[1])
                    if sdoIndex == '1602' and sdoSubindex == '00':
                        if int(sdoData,16) != 0:
                            self.RpdoMapStatus[2] = True
                        else:
                            self.RpdoMapStatus[2] = False
                        #print('RpdoMapStatus[2]',self.RpdoMapStatus[2])
                    if sdoIndex == '1603' and sdoSubindex == '00':
                        if int(sdoData,16) != 0:
                            self.RpdoMapStatus[3] = True
                        else:
                            self.RpdoMapStatus[3] = False
                        #print('RpdoMapStatus[3]',self.RpdoMapStatus[3])
            pass
        elif (intCobid == self.decNodeid+gc.cobid_TPDO1):
            #pdo1数据,那么根据diagram的配置更新数组. 
            if self.Tpdo1Value1List[0]:
                #Tpdo1存在第1个数据.
                tempdata11 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo1Value1List[3]:self.Tpdo1Value1List[3]+self.Tpdo1Value1List[2]]
                tempdata11 = tempdata11.replace(' ','')
                data11 = int.from_bytes(bytes.fromhex(tempdata11), byteorder='little', signed=self.Tpdo1Value1List[1])
                self.updateYMaxMin(data11)
                if (len(self.arrayTpdo1Data1)) < self.plotDataLength :
                    self.arrayTpdo1Data1.append(data11)
                else:
                    self.arrayTpdo1Data1[:-1] = self.arrayTpdo1Data1[1:]
                    self.arrayTpdo1Data1[-1] = data11                          
            if self.Tpdo1Value2List[0]:
                #Tpdo1存在第2个数据.
                tempdata12 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo1Value2List[3]:self.Tpdo1Value2List[3]+self.Tpdo1Value2List[2]]
                tempdata12 = tempdata12.replace(' ','')
                data12 = int.from_bytes(bytes.fromhex(tempdata12), byteorder='little', signed=self.Tpdo1Value2List[1]) 
                self.updateYMaxMin(data12)
                if (len(self.arrayTpdo1Data2)) < self.plotDataLength :
                    self.arrayTpdo1Data2.append(data12)
                else:
                    self.arrayTpdo1Data2[:-1] = self.arrayTpdo1Data2[1:]
                    self.arrayTpdo1Data2[-1] = data12               
            if self.Tpdo1Value3List[0]:
                #Tpdo1存在第3个数据.
                tempdata13 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo1Value3List[3]:self.Tpdo1Value3List[3]+self.Tpdo1Value3List[2]]
                tempdata13 = tempdata13.replace(' ','')
                data13 = int.from_bytes(bytes.fromhex(tempdata13), byteorder='little', signed=self.Tpdo1Value3List[1])
                self.updateYMaxMin(data13)
                if (len(self.arrayTpdo1Data3)) < self.plotDataLength :
                    self.arrayTpdo1Data3.append(data13)
                else:
                    self.arrayTpdo1Data3[:-1] = self.arrayTpdo1Data3[1:]
                    self.arrayTpdo1Data3[-1] = data13     
            if self.Tpdo1Value4List[0]:
                #Tpdo1存在第4个数据.
                tempdata14 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo1Value4List[3]:self.Tpdo1Value4List[3]+self.Tpdo1Value4List[2]]
                tempdata14 = tempdata14.replace(' ','')
                data14 = int.from_bytes(bytes.fromhex(tempdata14), byteorder='little', signed=self.Tpdo1Value4List[1])  
                self.updateYMaxMin(data14)
                if (len(self.arrayTpdo1Data4)) < self.plotDataLength :
                    self.arrayTpdo1Data4.append(data14)
                else:
                    self.arrayTpdo1Data4[:-1] = self.arrayTpdo1Data4[1:]
                    self.arrayTpdo1Data4[-1] = data14                        
            pass
        elif (intCobid == self.decNodeid+gc.cobid_TPDO2):  
            #pdo2数据,那么根据diagram的配置更新数组. 
            if self.Tpdo2Value1List[0]:
                #Tpdo2存在第1个数据.
                tempdata21 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo2Value1List[3]:self.Tpdo2Value1List[3]+self.Tpdo2Value1List[2]]
                tempdata21 = tempdata21.replace(' ','')
                data21 = int.from_bytes(bytes.fromhex(tempdata21), byteorder='little', signed=self.Tpdo2Value1List[1])
                self.updateYMaxMin(data21)
                if (len(self.arrayTpdo2Data1)) < self.plotDataLength :
                    self.arrayTpdo2Data1.append(data21)
                else:
                    self.arrayTpdo2Data1[:-1] = self.arrayTpdo2Data1[1:]
                    self.arrayTpdo2Data1[-1] = data21                          
            if self.Tpdo2Value2List[0]:
                #Tpdo2存在第2个数据.
                tempdata22 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo2Value2List[3]:self.Tpdo2Value2List[3]+self.Tpdo2Value2List[2]]
                tempdata22 = tempdata22.replace(' ','')
                data22 = int.from_bytes(bytes.fromhex(tempdata22), byteorder='little', signed=self.Tpdo2Value2List[1]) 
                self.updateYMaxMin(data22)
                if (len(self.arrayTpdo2Data2)) < self.plotDataLength :
                    self.arrayTpdo2Data2.append(data22)
                else:
                    self.arrayTpdo2Data2[:-1] = self.arrayTpdo2Data2[1:]
                    self.arrayTpdo2Data2[-1] = data22               
            if self.Tpdo2Value3List[0]:
                #Tpdo2存在第3个数据.
                tempdata23 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo2Value3List[3]:self.Tpdo2Value3List[3]+self.Tpdo2Value3List[2]]
                tempdata23 = tempdata23.replace(' ','')
                data23 = int.from_bytes(bytes.fromhex(tempdata23), byteorder='little', signed=self.Tpdo2Value3List[1])
                self.updateYMaxMin(data23)
                if (len(self.arrayTpdo2Data3)) < self.plotDataLength :
                    self.arrayTpdo2Data3.append(data23)
                else:
                    self.arrayTpdo2Data3[:-1] = self.arrayTpdo2Data3[1:]
                    self.arrayTpdo2Data3[-1] = data23     
            if self.Tpdo2Value4List[0]:
                #Tpdo2存在第4个数据.
                tempdata24 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo2Value4List[3]:self.Tpdo2Value4List[3]+self.Tpdo2Value4List[2]]
                tempdata24 = tempdata24.replace(' ','')
                data24 = int.from_bytes(bytes.fromhex(tempdata24), byteorder='little', signed=self.Tpdo2Value4List[1])  
                self.updateYMaxMin(data24)
                if (len(self.arrayTpdo2Data4)) < self.plotDataLength :
                    self.arrayTpdo2Data4.append(data24)
                else:
                    self.arrayTpdo2Data4[:-1] = self.arrayTpdo2Data4[1:]
                    self.arrayTpdo2Data4[-1] = data24                        
            pass             
        elif (intCobid == self.decNodeid+gc.cobid_TPDO3):    
            #pdo3数据,那么根据diagram的配置更新数组. 
            if self.Tpdo3Value1List[0]:
                #Tpdo3存在第1个数据.
                tempdata31 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo3Value1List[3]:self.Tpdo3Value1List[3]+self.Tpdo3Value1List[2]]
                tempdata31 = tempdata31.replace(' ','')
                data31 = int.from_bytes(bytes.fromhex(tempdata31), byteorder='little', signed=self.Tpdo3Value1List[1])
                self.updateYMaxMin(data31)
                if (len(self.arrayTpdo3Data1)) < self.plotDataLength :
                    self.arrayTpdo3Data1.append(data31)
                else:
                    self.arrayTpdo3Data1[:-1] = self.arrayTpdo3Data1[1:]
                    self.arrayTpdo3Data1[-1] = data31                          
            if self.Tpdo3Value2List[0]:
                #Tpdo3存在第2个数据.
                tempdata32 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo3Value2List[3]:self.Tpdo3Value2List[3]+self.Tpdo3Value2List[2]]
                tempdata32 = tempdata32.replace(' ','')
                data32 = int.from_bytes(bytes.fromhex(tempdata32), byteorder='little', signed=self.Tpdo3Value2List[1]) 
                self.updateYMaxMin(data32)
                if (len(self.arrayTpdo3Data2)) < self.plotDataLength :
                    self.arrayTpdo3Data2.append(data32)
                else:
                    self.arrayTpdo3Data2[:-1] = self.arrayTpdo3Data2[1:]
                    self.arrayTpdo3Data2[-1] = data32               
            if self.Tpdo3Value3List[0]:
                #Tpdo3存在第3个数据.
                tempdata33 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo3Value3List[3]:self.Tpdo3Value3List[3]+self.Tpdo3Value3List[2]]
                tempdata33 = tempdata33.replace(' ','')
                data33 = int.from_bytes(bytes.fromhex(tempdata33), byteorder='little', signed=self.Tpdo3Value3List[1])
                self.updateYMaxMin(data33)
                if (len(self.arrayTpdo3Data3)) < self.plotDataLength :
                    self.arrayTpdo3Data3.append(data33)
                else:
                    self.arrayTpdo3Data3[:-1] = self.arrayTpdo3Data3[1:]
                    self.arrayTpdo3Data3[-1] = data33     
            if self.Tpdo1Value4List[0]:
                #Tpdo3存在第4个数据.
                tempdata34 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo3Value4List[3]:self.Tpdo3Value4List[3]+self.Tpdo3Value4List[2]]
                tempdata34 = tempdata34.replace(' ','')
                data34 = int.from_bytes(bytes.fromhex(tempdata34), byteorder='little', signed=self.Tpdo3Value4List[1])  
                self.updateYMaxMin(data34)
                if (len(self.arrayTpdo3Data4)) < self.plotDataLength :
                    self.arrayTpdo3Data4.append(data34)
                else:
                    self.arrayTpdo3Data4[:-1] = self.arrayTpdo3Data4[1:]
                    self.arrayTpdo3Data4[-1] = data34                        
            pass      
        elif (intCobid == self.decNodeid+gc.cobid_TPDO4):    
            #pdo4数据,那么根据diagram的配置更新数组. 
            if self.Tpdo4Value1List[0]:
                #Tpdo4存在第1个数据.
                tempdata41 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo4Value1List[3]:self.Tpdo4Value1List[3]+self.Tpdo4Value1List[2]]
                tempdata41 = tempdata41.replace(' ','')
                data41 = int.from_bytes(bytes.fromhex(tempdata41), byteorder='little', signed=self.Tpdo4Value1List[1])
                self.updateYMaxMin(data41)
                if (len(self.arrayTpdo4Data1)) < self.plotDataLength :
                    self.arrayTpdo4Data1.append(data41)
                else:
                    self.arrayTpdo4Data1[:-1] = self.arrayTpdo4Data1[1:]
                    self.arrayTpdo4Data1[-1] = data41                          
            if self.Tpdo4Value2List[0]:
                #Tpdo4存在第2个数据.
                tempdata42 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo4Value2List[3]:self.Tpdo4Value2List[3]+self.Tpdo4Value2List[2]]
                tempdata42 = tempdata42.replace(' ','')
                data42 = int.from_bytes(bytes.fromhex(tempdata42), byteorder='little', signed=self.Tpdo4Value2List[1]) 
                self.updateYMaxMin(data42)
                if (len(self.arrayTpdo4Data2)) < self.plotDataLength :
                    self.arrayTpdo4Data2.append(data42)
                else:
                    self.arrayTpdo4Data2[:-1] = self.arrayTpdo4Data2[1:]
                    self.arrayTpdo4Data2[-1] = data42               
            if self.Tpdo3Value3List[0]:
                #Tpdo4存在第3个数据.
                tempdata43 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo4Value3List[3]:self.Tpdo4Value3List[3]+self.Tpdo4Value3List[2]]
                tempdata43 = tempdata43.replace(' ','')
                data43 = int.from_bytes(bytes.fromhex(tempdata43), byteorder='little', signed=self.Tpdo4Value3List[1])
                self.updateYMaxMin(data43)
                if (len(self.arrayTpdo4Data3)) < self.plotDataLength :
                    self.arrayTpdo4Data3.append(data43)
                else:
                    self.arrayTpdo4Data3[:-1] = self.arrayTpdo4Data3[1:]
                    self.arrayTpdo4Data3[-1] = data43     
            if self.Tpdo1Value4List[0]:
                #Tpdo4存在第4个数据.
                tempdata44 = currentFrameArr[gc.rcvFrameIndex_Data][self.Tpdo4Value4List[3]:self.Tpdo4Value4List[3]+self.Tpdo4Value4List[2]]
                tempdata44 = tempdata44.replace(' ','')
                data44 = int.from_bytes(bytes.fromhex(tempdata44), byteorder='little', signed=self.Tpdo4Value4List[1])  
                self.updateYMaxMin(data44)
                if (len(self.arrayTpdo4Data4)) < self.plotDataLength :
                    self.arrayTpdo4Data4.append(data44)
                else:
                    self.arrayTpdo4Data4[:-1] = self.arrayTpdo4Data4[1:]
                    self.arrayTpdo4Data4[-1] = data44                        
            pass 
        elif (intCobid >= 0x81)and(intCobid <= 0xFF) :
            #emergency
            self.pushErrorData(currentFrameArr)   
            pass
        elif (intCobid >= 0x581)and(intCobid <= 0x5FF) :
            #other nodeid's SDO,check aboration.
            sdoStatus   = currentFrameArr[gc.rcvFrameIndex_Data][0:2]   
            if sdoStatus == gc.sdo_rspd_abortion:
                #往error里面写入数据,TODO
                self.pushErrorData(currentFrameArr)    
                pass    
            pass          
            
    def updatePlot(self):
        self.plotWidget_diagram.setYRange(self.plotYMin, self.plotYMax, padding=0)
        if self.enableRefreshDiagram:
            # 数据填充到绘制曲线中
            if self.Tpdo1Value1List[0]:
                self.curveTpdo1Data1.setData(self.arrayTpdo1Data1)
            if self.Tpdo1Value2List[0]:
                self.curveTpdo1Data2.setData(self.arrayTpdo1Data2)
            if self.Tpdo1Value3List[0]:
                self.curveTpdo1Data3.setData(self.arrayTpdo1Data3)
            if self.Tpdo1Value4List[0]:
                self.curveTpdo1Data4.setData(self.arrayTpdo1Data4)
                pass
            if self.Tpdo2Value1List[0]:
                self.curveTpdo2Data1.setData(self.arrayTpdo2Data1)
            if self.Tpdo2Value2List[0]:
                self.curveTpdo2Data2.setData(self.arrayTpdo2Data2)
            if self.Tpdo2Value3List[0]:
                self.curveTpdo2Data3.setData(self.arrayTpdo2Data3)
            if self.Tpdo2Value3List[0]:
                self.curveTpdo2Data4.setData(self.arrayTpdo2Data4)
                pass
            if self.Tpdo3Value1List[0]:
                self.curveTpdo3Data1.setData(self.arrayTpdo3Data1)
            if self.Tpdo3Value2List[0]:
                self.curveTpdo3Data2.setData(self.arrayTpdo3Data2)
            if self.Tpdo3Value3List[0]:
                self.curveTpdo3Data3.setData(self.arrayTpdo3Data3)
            if self.Tpdo3Value4List[0]:
                self.curveTpdo3Data4.setData(self.arrayTpdo3Data4)
                pass
            if self.Tpdo4Value1List[0]:
                self.curveTpdo4Data1.setData(self.arrayTpdo4Data1)
            if self.Tpdo4Value2List[0]:
                self.curveTpdo4Data2.setData(self.arrayTpdo4Data2)
            if self.Tpdo4Value3List[0]:
                self.curveTpdo4Data3.setData(self.arrayTpdo4Data3)
            if self.Tpdo4Value4List[0]:
                self.curveTpdo4Data4.setData(self.arrayTpdo4Data4)
        pass
    def updateYMaxMin(self,newdata):
        if newdata > self.YMax :
            self.YMax = newdata
            self.plotYMax = self.YMax*1.5
        if newdata < self.YMin:
            self.YMin = newdata
            self.plotYMin = self.YMin*1.5
        pass    


    #config other nodeid
    def writeOtherNodeidToFlowCan(self):
        #清零other nodeid数目,清空list
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_other_nodeid,'02','00'+'00']) 
        #配置nodeid list
        for index in range(self.otherNodeidListLen):
            strOtherNodeid = str(hex(self.otherNodeidList[index]).replace('0x','')).zfill(2).upper()
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_other_nodeid,'02','01'+strOtherNodeid]) 
            pass
        pass

    #000 nmt command.
    def writeNMT(self,isall,nmtcmd):
        #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cobid_NMT,'02',nmtcmd+self.strNodeid])
        #if isall:
            #for index in range(self.otherNodeidListLen):
                #strNodeid  = str(hex(self.otherNodeidList[index]).replace('0x','')).zfill(2).upper()
                #self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cobid_NMT,'02',nmtcmd+strNodeid])  
        #pass
        if isall:
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cobid_NMT,'02',nmtcmd+'00'])
        else:
            self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cobid_NMT,'02',nmtcmd+self.strNodeid])
        pass
    def nmt_getNmtState(self,isall):
        self.comTransceiver.write([gc.defaultTimeGap,'01',self.cobid_NODEG,'00','']) 
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_NODEG = (str(hex(self.otherNodeidList[index]+gc.cobid_NODEG)).replace('0x','')).zfill(3).upper()   
                self.comTransceiver.write([gc.defaultTimeGap,'01',cobid_NODEG,'00','']) 
        pass
    #save config, 1010:02, 4byte
    def writeStoreParameterSaveComm(self):
        self.function.hexStrToHexBytes('65766173')  
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeStoreParameterSaveComm+self.function.getSdoDataStr()]) 
        pass  
    #load defatult comm, 1011:02, 4byte 
    def writeRestoreParameterComm(self):    
        self.function.hexStrToHexBytes('64616F6C')   #load的ASCII
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeRestoreParameterComm+self.function.getSdoDataStr()])   
        pass 
    #write synchronousCounterOverflowValue, 1019, 1byte
    def writeSynchronousCounterOverflowValue(self,isall):
        isSyncWithData = self.tpdoConfig.getSyncWithDataStatus() 
        if isSyncWithData:   
            self.function.hexStrToHexBytes('F0')   
        else:
            self.function.hexStrToHexBytes('00')   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeSynchronousCounterOverflowValue+self.function.getSdoDataStr()])   
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeSynchronousCounterOverflowValue+self.function.getSdoDataStr()])   
        pass
    #6040,control word
    def writeControlWord(self,isall,cw):
        self.function.hexStrToHexBytes(cw)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeControlWord+self.function.getSdoDataStr()])   
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeControlWord+self.function.getSdoDataStr()])   
        pass
    #6060 control mode
    def writeControlMode(self,isall,mode):
        self.function.hexStrToHexBytes(mode)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeControlMode+self.function.getSdoDataStr()])   
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeControlMode+self.function.getSdoDataStr()])        
        pass  
    #target torque,6071, 2byte
    def writeTargetTorque(self,isall,tt):
        self.function.decStrToHexBytes(tt,2)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeTargetTorque + self.function.getSdoDataStr()])
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTargetTorque+self.function.getSdoDataStr()])  
        pass  
    def writeTargetTorqueToFlowcan(self,tt):
        self.function.decStrToHexBytes(tt,2)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeTargetTorque + self.function.getSdoDataStr()])
        pass  
    #home offset, 607C, int32
    def writeHomeOffset(self,isall,ho):
        self.function.decStrToHexBytes(ho,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeHomeOffset+self.function.getSdoDataStr()]) 
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeHomeOffset+self.function.getSdoDataStr()])  
        pass
    #set target position, 0x607A, 4byte
    def writeTargetPosition(self,isall,tp):
        self.function.decStrToHexBytes(tp,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeTargetPosition+self.function.getSdoDataStr()]) 
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTargetPosition+self.function.getSdoDataStr()])   
        pass
    def writeTargetPositionToFlowcan(self,tp):
        self.function.decStrToHexBytes(tp,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeTargetPosition+self.function.getSdoDataStr()])   
        pass  
    #set profile velocity, 0x6081, 4byte
    def writeProfileVelocity(self,isall,pv):
        self.function.decStrToHexBytes(pv,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeProfileVelocity+self.function.getSdoDataStr()])
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeProfileVelocity+self.function.getSdoDataStr()])       
        pass       
    def writeProfileVelocityToFlowcan(self,pv):
        self.function.decStrToHexBytes(pv,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeProfileVelocity+self.function.getSdoDataStr()])    
        pass   
    #set profile acceleration, 0x6083, 4byte
    def writeProfileAcceleration(self,isall,pa):
        self.function.decStrToHexBytes(pa,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeProfileAcceleration+self.function.getSdoDataStr()])
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeProfileAcceleration+self.function.getSdoDataStr()])      
        pass
    def writeProfileAccelerationToFlowcan(self,pa):
        self.function.decStrToHexBytes(pa,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeProfileAcceleration+self.function.getSdoDataStr()])   
        pass
    #set profile deceleration, 0x6084, 4byte
    def writeProfileDeceleration(self,isall,pd):
        self.function.decStrToHexBytes(pd,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeProfileDeceleration+self.function.getSdoDataStr()])
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeProfileDeceleration+self.function.getSdoDataStr()])     
        pass     
    def writeProfileDecelerationToFlowcan(self,pd):
        self.function.decStrToHexBytes(pd,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeProfileDeceleration+self.function.getSdoDataStr()])  
        pass    
    #torque slope 6087 4byte
    def writeTorqueSlope(self,isall,ts):
        self.function.decStrToHexBytes(ts,4)                      
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeTorqueSlope + self.function.getSdoDataStr()])
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTorqueSlope+self.function.getSdoDataStr()])   
        pass
    def writeTorqueSlopeToFlowcan(self,ts):
        self.function.decStrToHexBytes(ts,4)                      
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeTorqueSlope + self.function.getSdoDataStr()])
        pass
    #homing method,6098 1byte
    def writeHomingMethod(self,isall,hm):
        self.function.decStrToHexBytes(hm,1)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeHomingMethod+self.function.getSdoDataStr()])
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeHomingMethod+self.function.getSdoDataStr()])    
        pass
    #homing speed1, 6099:01, 4byte
    def writeHomingSpeed1(self,isall,hs1):
        self.function.decStrToHexBytes(hs1,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeHomingSpeed1+self.function.getSdoDataStr()])
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeHomingSpeed1+self.function.getSdoDataStr()])   
        pass 
    #homing speed2, 6099:02, 4byte
    def writeHomingSpeed2(self,isall,hs2):
        self.function.decStrToHexBytes(hs2,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeHomingSpeed2+self.function.getSdoDataStr()])
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTargewriteHomingSpeed2tPosition+self.function.getSdoDataStr()])    
        pass
    #homing acceleration 0x609A, 4byte
    def writeHomingAcceleration(self,isall,ha):
        self.function.decStrToHexBytes(ha,4)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeHomingAcceleraiton+self.function.getSdoDataStr()])
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeHomingAcceleraiton+self.function.getSdoDataStr()])     
        pass
    #set interpolation time period value, 0x60C2:01, 1byte
    def writeInterpolationTimePeriodValue(self,isall,itpv):
        self.function.decStrToHexBytes(itpv,1)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeInterpolationTimePeriodValue+self.function.getSdoDataStr()])
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeInterpolationTimePeriodValue+self.function.getSdoDataStr()])   
        pass 
    def writeInterpolationTimePeriodValueToFlowcan(self,itpv):
        self.function.decStrToHexBytes(itpv,1)   
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeInterpolationTimePeriodValue+self.function.getSdoDataStr()])
        pass 
    #target velocity 0x60FF, 4byte
    def writeTargetVelocity(self,isall,tv):
        self.function.decStrToHexBytes(tv,4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,self.cobid_TSDO,'08',gc.writeTargetVelocity+self.function.getSdoDataStr()])
        if isall:
            for index in range(self.otherNodeidListLen):
                cobid_TSDO = (str(hex(self.otherNodeidList[index]+gc.cobid_TSDO)).replace('0x','')).zfill(3).upper()
                self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,cobid_TSDO,'08',gc.writeTargetVelocity+self.function.getSdoDataStr()])    
        pass
    def writeTargetVelocityToFlowcan(self,tv):
        self.function.decStrToHexBytes(tv,4)     
        self.comTransceiver.write([gc.defaultTimeGap,gc.defaultRtr,gc.cmd_od_config,'08',gc.writeTargetVelocity+self.function.getSdoDataStr()]) 
        pass
        