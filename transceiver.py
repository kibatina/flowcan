from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtCore import QDate
import globalConstants as gc

class Transceiver (object):
    rxBufferBytearray = ''
    def __init__(self):
        # Qt 串口类
        self.com = QSerialPort()
        self.comPorts = []   #维护当前可用的端口数据
        self.currentPortName = None #维护当前端口名
        self.com.readyRead.connect(self.comReceiveData) # 接收数据
        # UI成员设置
        self.mainWindow = None
        self.configWindow = None
        
    
    def setMainWindow(self,mainWindow):
        self.mainWindow = mainWindow
    def setConfigWindow(self,configWindow):
        self.configWindow = configWindow
        
    # 从串口读取当前全部可用的com端口, 并刷新存储

    def refreshComPorts(self):
        self.comPorts.clear()
        #每次refresh要重新连接下面两句话.不知道原因.
        self.com = QSerialPort()
        self.com.readyRead.connect(self.comReceiveData) # 接收数据
        com_list = QSerialPortInfo.availablePorts()
        for info in com_list:
            #print('portname:',info.portName())
            #print('description:',info.description())
            #print('serialnum:',info.serialNumber())
            #print('producer:',info.productIdentifier())
            #print('vender:',info.vendorIdentifier())
            #print('manufacturer:',info.manufacturer())
            #print('standardBaudRates:',info.standardBaudRates())
            #print('hasProductIdentifier:',info.hasProductIdentifier())
            #print('hasVendorIdentifier:',info.hasVendorIdentifier())
            self.com.setPort(info)
            if self.com.open(QSerialPort.ReadWrite):
                if info.serialNumber()[8:12] == 'FLOW':
                    self.comPorts.append(info)
                self.com.close()
    
    def openComPort(self, portName):
        #固定波特率
        comBaud = 115200
        self.com.setPortName(portName)
        try:
            if self.com.open(QSerialPort.ReadWrite) == False:
                return [False,'Failed to open virtual com port']
        except:
            return [False,'Failed to open virtual com port']
        self.com.setBaudRate(comBaud, QSerialPort.Direction.AllDirections)
        self.currentPortName = portName
        return [True,""]

    def closeCom(self):
        self.com.close()
    
    def write(self,paramArray):
        #paramArray[0]=timeGap,paramArray[1]=rtr, paramArray[2]=cobid,paramArray[3]=len,paramArray[4]=data   
        #sendText = paramArray[0]+','+paramArray[1]+','+paramArray[2]+','+paramArray[3]+','+paramArray[4]+'\r\n'
        #self.com.write(sendText.encode('UTF-8'))
        sendText = paramArray[0].zfill(8)+paramArray[1].zfill(2)+paramArray[2].zfill(4)+paramArray[3].zfill(2)+paramArray[4].ljust(16,'0')
        sendText += '0d0a'
        #print('send=',sendText)
        self.com.write(bytes.fromhex(sendText))
        pass
    def getComPorts(self):
        #print(self.comPorts)
        return self.comPorts
    
    def getCurrentPortName(self):
        return self.currentPortName    
    
    # 串口接收数据
    def comReceiveData(self):
        try:
            rxData = bytes((self.com.readAll()).toHex())
        except:
            QMessageBox.critical(self, 'Error', 'wrong data.')
        decodedRxData = rxData.decode('utf-8')
        #添加到buffer里面去。
        self.rxBufferBytearray = self.rxBufferBytearray + decodedRxData
        while len(self.rxBufferBytearray) >= 46:
            #对应23byte的通信协议.
            if self.rxBufferBytearray[42:46] == '0d0a':
                currentFrame = self.rxBufferBytearray[0:46]
                #print('rcv =',currentFrame)
                self.rxBufferBytearray = self.rxBufferBytearray[46:]
                if currentFrame[40] == '0': 
                    #0表示是透传的CAN数据.
                    # 0    1    2  3   4     5   6    
                    #num, time, tr,rtr,cobid,len,data,\r\n
                    # 8    8    2  2    4     2   16   4
                    currentFrameArr =[currentFrame[0:8],currentFrame[8:16],currentFrame[16:17],currentFrame[17:18],currentFrame[18:22],currentFrame[22:24],currentFrame[24:40]]
                    #将时间从us改为ms
                    #print('time=',currentFrameArr[gc.rcvFrameIndex_Time])
                    #print('inttime=',int(currentFrameArr[gc.rcvFrameIndex_Time],16))
                    #print('floattime=',float('%.3f' % int(currentFrameArr[gc.rcvFrameIndex_Time],16))/1000.000)
                    currentFrameArr[gc.rcvFrameIndex_Time] = str('%.3f'%(float(int(currentFrameArr[gc.rcvFrameIndex_Time],16))/1000))
                    # 0为R,其余为T
                    if currentFrameArr[gc.rcvFrameIndex_TR] == '0':
                        currentFrameArr[gc.rcvFrameIndex_TR] = 'R'
                    else:
                        currentFrameArr[gc.rcvFrameIndex_TR] = 'T'
                    #cobid去除前面的0,并改为大写.
                    currentFrameArr[gc.rcvFrameIndex_Cobid] = currentFrameArr[gc.rcvFrameIndex_Cobid][1:4].upper()
                    #data的内容,按照字节分开,中间用空格分割   
                    currentFrameArr[gc.rcvFrameIndex_Data] = ''
                    for index in range(int(currentFrameArr[gc.rcvFrameIndex_Len],10)):   
                        currentFrameArr[gc.rcvFrameIndex_Data] += currentFrame[(24+(index*2)):(24+(index*2)+2)].upper()      
                        currentFrameArr[gc.rcvFrameIndex_Data] += ' '
                    #标识,判定是透传过来的数据还是,USB2CAN给的数据.
                    self.mainWindow.processCurrentFrame(currentFrameArr)
                    self.configWindow.processCurrentFrame(currentFrameArr)
                else:
                    #非0表示是本地(flowcan)的CAN数据. 
                    identify = currentFrame[18:22]  #idenfity也就是cobid
                    if identify == '0000':
                        #表示是usb2can给过来的状态数据,有待处理,状态数据是4个byte,也就是8个字符,24~32是8个字符.
                        data = int.from_bytes(bytes.fromhex(currentFrame[24:32]), byteorder='big', signed=False)  
                        #print('localdata=',data)
                        #CAN_ERRTX_WARNING    	= 0x00000001,  
                        #CAN_ERRTX_PASSIVE    	= 0x00000002,  
                        #CAN_ERRTX_OVERFLOW   	= 0x00000004, 	
                        #CAN_ERRTX_BUS_OFF    	= 0x00000008,  
                        #CAN_ERRRX_WARNING    	= 0x00000010,  
                        #CAN_ERRRX_PASSIVE    	= 0x00000020,  
                        #CAN_ERRRX_OVERFLOW   	= 0x00000040, 	
                        #CAN_RXFIFO_FULL	 	= 0x00010000,
                        #CAN_TXFIFO_FULL	 	= 0x00020000,
                        #USB_RXFIFO_FULL		= 0x00040000,
                        #USB_TXFIFO_FULL		= 0x00080000
                        displayString=''
                        if data & 0x00000001:
                            displayString  += ' CAN_TX_Warning '
                        if data & 0x00000002:
                            displayString  += ' CAN_TX_Passive '
                        if data & 0x00000004:
                            displayString  += ' CAN_TX_Overflow '
                        if data & 0x00000008:
                            displayString  += ' CAN_BUS_OFF '
                        if data & 0x00000010:
                            displayString  += ' CAN_Rx_Warning '
                        if data & 0x00000020:
                            displayString  += ' CAN_RX_Passive '
                        if data & 0x00000040:
                            displayString  += ' CAN_RX_Overflow '
                        if data & 0x00010000:
                            displayString  += ' CAN_RX_FIFO_Full '    
                        if data & 0x00020000:
                            displayString  += ' CAN_TX_FIFO_Full '  
                        if data & 0x00040000:
                            displayString  += ' USB_RX_FIFO_Full '  
                        if data & 0x00080000:
                            displayString  += ' USB_TX_FIFO_Full '    
                        if displayString == '':
                            displayString = 'OK'
                        self.mainWindow.updateFlowCanStatus(displayString) 
                        pass
                    if identify == '0001':
                        #表示usb2can传过来的软件版本和硬件版本
                        #print(currentFrame)
                        #version = currentFrame[30:32]+currentFrame[28:30]+currentFrame[26:28]+currentFrame[24:26]
                        softwareversion = currentFrame[24:32]
                        hardwareversion = currentFrame[32:40]
                        self.mainWindow.updateUsb2canVersion(softwareversion,hardwareversion)
                        pass
                pass
            else:
                #数据分段错误,尝试从新寻找0d0a标记来分段.
                rxFrameList = self.rxBufferBytearray.partition('0d0a')
                currentFrame = rxFrameList[0]
                self.rxBufferBytearray  = rxFrameList[2]
        pass
