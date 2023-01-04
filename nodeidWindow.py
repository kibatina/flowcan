from pip import main
import pyqtgraph as pg
import sys
from ui_flowNodeid import Ui_nodeid

from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray, QTimer, QDate, Qt
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
import globalConstants as gc


class nodeidWindow(QWidget, Ui_nodeid):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Nodeid")  
        self.mainWindow = None
        self.nodeidList = []
        self.nodeidListLen  = 0
        self.CreateSignalSlot()
        pass
    def setMainWindow(self,mainWindow):
        self.mainWindow = mainWindow
        pass 
    def CreateSignalSlot(self):
        self.pushButton_nodeid_clearAll.clicked.connect(self.pushButton_nodeid_clearAll_clicked) 
        self.pushButton_nodeid_update.clicked.connect(self.pushButton_nodeid_update_clicked) 
        pass   
    def pushButton_nodeid_clearAll_clicked(self):
        self.checkBox_nodeid_1.setChecked(False)
        self.checkBox_nodeid_2.setChecked(False)
        self.checkBox_nodeid_3.setChecked(False)
        self.checkBox_nodeid_4.setChecked(False)
        self.checkBox_nodeid_5.setChecked(False)
        self.checkBox_nodeid_6.setChecked(False)
        self.checkBox_nodeid_7.setChecked(False)
        self.checkBox_nodeid_8.setChecked(False)
        self.checkBox_nodeid_9.setChecked(False)
        self.checkBox_nodeid_10.setChecked(False)
        self.checkBox_nodeid_11.setChecked(False)
        self.checkBox_nodeid_12.setChecked(False)
        self.checkBox_nodeid_13.setChecked(False)
        self.checkBox_nodeid_14.setChecked(False)
        self.checkBox_nodeid_15.setChecked(False)
        self.checkBox_nodeid_16.setChecked(False)
        self.checkBox_nodeid_17.setChecked(False)
        self.checkBox_nodeid_18.setChecked(False)
        self.checkBox_nodeid_19.setChecked(False)
        self.checkBox_nodeid_20.setChecked(False)
        self.checkBox_nodeid_21.setChecked(False)
        self.checkBox_nodeid_22.setChecked(False)
        self.checkBox_nodeid_23.setChecked(False)
        self.checkBox_nodeid_24.setChecked(False)
        self.checkBox_nodeid_25.setChecked(False)
        self.checkBox_nodeid_26.setChecked(False)
        self.checkBox_nodeid_27.setChecked(False)
        self.checkBox_nodeid_28.setChecked(False)
        self.checkBox_nodeid_29.setChecked(False)
        self.checkBox_nodeid_30.setChecked(False)
        self.checkBox_nodeid_31.setChecked(False)
        self.checkBox_nodeid_32.setChecked(False)
        self.checkBox_nodeid_33.setChecked(False)
        self.checkBox_nodeid_34.setChecked(False)
        self.checkBox_nodeid_35.setChecked(False)
        self.checkBox_nodeid_36.setChecked(False)
        self.checkBox_nodeid_37.setChecked(False)
        self.checkBox_nodeid_38.setChecked(False)
        self.checkBox_nodeid_39.setChecked(False)
        self.checkBox_nodeid_40.setChecked(False)
        self.checkBox_nodeid_41.setChecked(False)
        self.checkBox_nodeid_42.setChecked(False)
        self.checkBox_nodeid_43.setChecked(False)
        self.checkBox_nodeid_44.setChecked(False)
        self.checkBox_nodeid_45.setChecked(False)
        self.checkBox_nodeid_46.setChecked(False)
        self.checkBox_nodeid_47.setChecked(False)
        self.checkBox_nodeid_48.setChecked(False)
        self.checkBox_nodeid_49.setChecked(False)
        self.checkBox_nodeid_50.setChecked(False)
        self.checkBox_nodeid_51.setChecked(False)
        self.checkBox_nodeid_52.setChecked(False)
        self.checkBox_nodeid_53.setChecked(False)
        self.checkBox_nodeid_54.setChecked(False)
        self.checkBox_nodeid_55.setChecked(False)
        self.checkBox_nodeid_56.setChecked(False)
        self.checkBox_nodeid_57.setChecked(False)
        self.checkBox_nodeid_58.setChecked(False)
        self.checkBox_nodeid_59.setChecked(False)
        self.checkBox_nodeid_60.setChecked(False)
        self.checkBox_nodeid_61.setChecked(False)
        self.checkBox_nodeid_62.setChecked(False)
        self.checkBox_nodeid_63.setChecked(False)
        self.checkBox_nodeid_64.setChecked(False)
        self.checkBox_nodeid_65.setChecked(False)
        self.checkBox_nodeid_66.setChecked(False)
        self.checkBox_nodeid_67.setChecked(False)
        self.checkBox_nodeid_68.setChecked(False)
        self.checkBox_nodeid_69.setChecked(False)
        self.checkBox_nodeid_70.setChecked(False)
        self.checkBox_nodeid_71.setChecked(False)
        self.checkBox_nodeid_72.setChecked(False)
        self.checkBox_nodeid_73.setChecked(False)
        self.checkBox_nodeid_74.setChecked(False)
        self.checkBox_nodeid_75.setChecked(False)
        self.checkBox_nodeid_76.setChecked(False)
        self.checkBox_nodeid_77.setChecked(False)
        self.checkBox_nodeid_78.setChecked(False)
        self.checkBox_nodeid_79.setChecked(False)
        self.checkBox_nodeid_80.setChecked(False)
        self.checkBox_nodeid_81.setChecked(False)
        self.checkBox_nodeid_82.setChecked(False)
        self.checkBox_nodeid_83.setChecked(False)
        self.checkBox_nodeid_84.setChecked(False)
        self.checkBox_nodeid_85.setChecked(False)
        self.checkBox_nodeid_86.setChecked(False)
        self.checkBox_nodeid_87.setChecked(False)
        self.checkBox_nodeid_88.setChecked(False)
        self.checkBox_nodeid_89.setChecked(False)
        self.checkBox_nodeid_90.setChecked(False)
        self.checkBox_nodeid_91.setChecked(False)
        self.checkBox_nodeid_92.setChecked(False)
        self.checkBox_nodeid_93.setChecked(False)
        self.checkBox_nodeid_94.setChecked(False)
        self.checkBox_nodeid_95.setChecked(False)
        self.checkBox_nodeid_96.setChecked(False)
        self.checkBox_nodeid_97.setChecked(False)
        self.checkBox_nodeid_98.setChecked(False)
        self.checkBox_nodeid_99.setChecked(False)
        self.checkBox_nodeid_100.setChecked(False)
        self.checkBox_nodeid_101.setChecked(False)
        self.checkBox_nodeid_102.setChecked(False)
        self.checkBox_nodeid_103.setChecked(False)
        self.checkBox_nodeid_104.setChecked(False)
        self.checkBox_nodeid_105.setChecked(False)
        self.checkBox_nodeid_106.setChecked(False)
        self.checkBox_nodeid_107.setChecked(False)
        self.checkBox_nodeid_108.setChecked(False)
        self.checkBox_nodeid_109.setChecked(False)
        self.checkBox_nodeid_110.setChecked(False)
        self.checkBox_nodeid_111.setChecked(False)
        self.checkBox_nodeid_112.setChecked(False)
        self.checkBox_nodeid_113.setChecked(False)
        self.checkBox_nodeid_114.setChecked(False)
        self.checkBox_nodeid_115.setChecked(False)
        self.checkBox_nodeid_116.setChecked(False)
        self.checkBox_nodeid_117.setChecked(False)
        self.checkBox_nodeid_118.setChecked(False)
        self.checkBox_nodeid_119.setChecked(False)
        self.checkBox_nodeid_120.setChecked(False)
        self.checkBox_nodeid_121.setChecked(False)
        self.checkBox_nodeid_122.setChecked(False)
        self.checkBox_nodeid_123.setChecked(False)
        self.checkBox_nodeid_124.setChecked(False)
        self.checkBox_nodeid_125.setChecked(False)
        self.checkBox_nodeid_126.setChecked(False)
        self.checkBox_nodeid_127.setChecked(False)
        pass
    def pushButton_nodeid_update_clicked(self):
        self.nodeidList = []
        self.nodeidListLen  = 0
        if self.checkBox_nodeid_1.isEnabled():
            if self.checkBox_nodeid_1.isChecked():
                self.nodeidList.append(1)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_2.isEnabled():
            if self.checkBox_nodeid_2.isChecked():
                self.nodeidList.append(2)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_3.isEnabled():
            if self.checkBox_nodeid_3.isChecked():
                self.nodeidList.append(3)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_4.isEnabled():
            if self.checkBox_nodeid_4.isChecked():
                self.nodeidList.append(4)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_5.isEnabled():
            if self.checkBox_nodeid_5.isChecked():
                self.nodeidList.append(5)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_6.isEnabled():
            if self.checkBox_nodeid_6.isChecked():
                self.nodeidList.append(6)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_7.isEnabled():
            if self.checkBox_nodeid_7.isChecked():
                self.nodeidList.append(7)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_8.isEnabled():
            if self.checkBox_nodeid_8.isChecked():
                self.nodeidList.append(8)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_9.isEnabled():
            if self.checkBox_nodeid_9.isChecked():
                self.nodeidList.append(9)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_10.isEnabled():
            if self.checkBox_nodeid_10.isChecked():
                self.nodeidList.append(10)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_11.isEnabled():
            if self.checkBox_nodeid_11.isChecked():
                self.nodeidList.append(11)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_12.isEnabled():
            if self.checkBox_nodeid_12.isChecked():
                self.nodeidList.append(12)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_13.isEnabled():
            if self.checkBox_nodeid_13.isChecked():
                self.nodeidList.append(13)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_14.isEnabled():
            if self.checkBox_nodeid_14.isChecked():
                self.nodeidList.append(14)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_15.isEnabled():
            if self.checkBox_nodeid_15.isChecked():
                self.nodeidList.append(15)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_16.isEnabled():
            if self.checkBox_nodeid_16.isChecked():
                self.nodeidList.append(16)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_17.isEnabled():
            if self.checkBox_nodeid_17.isChecked():
                self.nodeidList.append(17)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_18.isEnabled():
            if self.checkBox_nodeid_18.isChecked():
                self.nodeidList.append(18)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_19.isEnabled():
            if self.checkBox_nodeid_19.isChecked():
                self.nodeidList.append(19)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_20.isEnabled():
            if self.checkBox_nodeid_20.isChecked():
                self.nodeidList.append(20)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_21.isEnabled():
            if self.checkBox_nodeid_21.isChecked():
                self.nodeidList.append(21)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_22.isEnabled():
            if self.checkBox_nodeid_22.isChecked():
                self.nodeidList.append(22)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_23.isEnabled():
            if self.checkBox_nodeid_23.isChecked():
                self.nodeidList.append(23)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_24.isEnabled():
            if self.checkBox_nodeid_24.isChecked():
                self.nodeidList.append(24)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_25.isEnabled():
            if self.checkBox_nodeid_25.isChecked():
                self.nodeidList.append(25)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_26.isEnabled():
            if self.checkBox_nodeid_26.isChecked():
                self.nodeidList.append(26)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_27.isEnabled():
            if self.checkBox_nodeid_27.isChecked():
                self.nodeidList.append(27)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_28.isEnabled():
            if self.checkBox_nodeid_28.isChecked():
                self.nodeidList.append(28)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_29.isEnabled():
            if self.checkBox_nodeid_29.isChecked():
                self.nodeidList.append(29)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_30.isEnabled():
            if self.checkBox_nodeid_30.isChecked():
                self.nodeidList.append(30)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_31.isEnabled():
            if self.checkBox_nodeid_31.isChecked():
                self.nodeidList.append(31)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_32.isEnabled():
            if self.checkBox_nodeid_32.isChecked():
                self.nodeidList.append(32)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_33.isEnabled():
            if self.checkBox_nodeid_33.isChecked():
                self.nodeidList.append(33)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_34.isEnabled():
            if self.checkBox_nodeid_34.isChecked():
                self.nodeidList.append(34)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_35.isEnabled():
            if self.checkBox_nodeid_35.isChecked():
                self.nodeidList.append(35)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_36.isEnabled():
            if self.checkBox_nodeid_36.isChecked():
                self.nodeidList.append(36)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_37.isEnabled():
            if self.checkBox_nodeid_37.isChecked():
                self.nodeidList.append(37)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_38.isEnabled():
            if self.checkBox_nodeid_38.isChecked():
                self.nodeidList.append(38)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_39.isEnabled():
            if self.checkBox_nodeid_39.isChecked():
                self.nodeidList.append(39)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_40.isEnabled():
            if self.checkBox_nodeid_40.isChecked():
                self.nodeidList.append(40)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_41.isEnabled():
            if self.checkBox_nodeid_41.isChecked():
                self.nodeidList.append(41)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_42.isEnabled():
            if self.checkBox_nodeid_42.isChecked():
                self.nodeidList.append(42)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_43.isEnabled():
            if self.checkBox_nodeid_43.isChecked():
                self.nodeidList.append(43)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_44.isEnabled():
            if self.checkBox_nodeid_44.isChecked():
                self.nodeidList.append(44)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_45.isEnabled():
            if self.checkBox_nodeid_45.isChecked():
                self.nodeidList.append(45)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_46.isEnabled():
            if self.checkBox_nodeid_46.isChecked():
                self.nodeidList.append(46)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_47.isEnabled():
            if self.checkBox_nodeid_47.isChecked():
                self.nodeidList.append(47)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_48.isEnabled():
            if self.checkBox_nodeid_48.isChecked():
                self.nodeidList.append(48)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_49.isEnabled():
            if self.checkBox_nodeid_49.isChecked():
                self.nodeidList.append(49)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_50.isEnabled():
            if self.checkBox_nodeid_50.isChecked():
                self.nodeidList.append(50)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_51.isEnabled():
            if self.checkBox_nodeid_51.isChecked():
                self.nodeidList.append(51)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_52.isEnabled():
            if self.checkBox_nodeid_52.isChecked():
                self.nodeidList.append(52)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_53.isEnabled():
            if self.checkBox_nodeid_53.isChecked():
                self.nodeidList.append(53)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_54.isEnabled():
            if self.checkBox_nodeid_54.isChecked():
                self.nodeidList.append(54)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_55.isEnabled():
            if self.checkBox_nodeid_55.isChecked():
                self.nodeidList.append(55)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_56.isEnabled():
            if self.checkBox_nodeid_56.isChecked():
                self.nodeidList.append(56)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_57.isEnabled():
            if self.checkBox_nodeid_57.isChecked():
                self.nodeidList.append(57)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_58.isEnabled():
            if self.checkBox_nodeid_58.isChecked():
                self.nodeidList.append(58)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_59.isEnabled():
            if self.checkBox_nodeid_59.isChecked():
                self.nodeidList.append(59)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_60.isEnabled():
            if self.checkBox_nodeid_60.isChecked():
                self.nodeidList.append(60)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_61.isEnabled():
            if self.checkBox_nodeid_61.isChecked():
                self.nodeidList.append(61)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_62.isEnabled():
            if self.checkBox_nodeid_62.isChecked():
                self.nodeidList.append(62)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_63.isEnabled():
            if self.checkBox_nodeid_63.isChecked():
                self.nodeidList.append(63)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_64.isEnabled():
            if self.checkBox_nodeid_64.isChecked():
                self.nodeidList.append(64)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_65.isEnabled():
            if self.checkBox_nodeid_65.isChecked():
                self.nodeidList.append(65)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_66.isEnabled():
            if self.checkBox_nodeid_66.isChecked():
                self.nodeidList.append(66)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_67.isEnabled():
            if self.checkBox_nodeid_67.isChecked():
                self.nodeidList.append(67)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_68.isEnabled():
            if self.checkBox_nodeid_68.isChecked():
                self.nodeidList.append(68)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_69.isEnabled():
            if self.checkBox_nodeid_69.isChecked():
                self.nodeidList.append(69)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_70.isEnabled():
            if self.checkBox_nodeid_70.isChecked():
                self.nodeidList.append(70)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_71.isEnabled():
            if self.checkBox_nodeid_71.isChecked():
                self.nodeidList.append(71)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_72.isEnabled():
            if self.checkBox_nodeid_72.isChecked():
                self.nodeidList.append(72)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_73.isEnabled():
            if self.checkBox_nodeid_73.isChecked():
                self.nodeidList.append(73)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_74.isEnabled():
            if self.checkBox_nodeid_74.isChecked():
                self.nodeidList.append(74)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_75.isEnabled():
            if self.checkBox_nodeid_75.isChecked():
                self.nodeidList.append(75)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_76.isEnabled():
            if self.checkBox_nodeid_76.isChecked():
                self.nodeidList.append(76)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_77.isEnabled():
            if self.checkBox_nodeid_77.isChecked():
                self.nodeidList.append(77)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_78.isEnabled():
            if self.checkBox_nodeid_78.isChecked():
                self.nodeidList.append(78)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_79.isEnabled():
            if self.checkBox_nodeid_79.isChecked():
                self.nodeidList.append(79)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_80.isEnabled():
            if self.checkBox_nodeid_80.isChecked():
                self.nodeidList.append(80)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_81.isEnabled():
            if self.checkBox_nodeid_81.isChecked():
                self.nodeidList.append(81)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_82.isEnabled():
            if self.checkBox_nodeid_82.isChecked():
                self.nodeidList.append(82)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_83.isEnabled():
            if self.checkBox_nodeid_83.isChecked():
                self.nodeidList.append(83)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_84.isEnabled():
            if self.checkBox_nodeid_84.isChecked():
                self.nodeidList.append(84)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_85.isEnabled():
            if self.checkBox_nodeid_85.isChecked():
                self.nodeidList.append(85)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_86.isEnabled():
            if self.checkBox_nodeid_86.isChecked():
                self.nodeidList.append(86)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_87.isEnabled():
            if self.checkBox_nodeid_87.isChecked():
                self.nodeidList.append(87)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_88.isEnabled():
            if self.checkBox_nodeid_88.isChecked():
                self.nodeidList.append(88)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_89.isEnabled():
            if self.checkBox_nodeid_89.isChecked():
                self.nodeidList.append(89)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_90.isEnabled():
            if self.checkBox_nodeid_90.isChecked():
                self.nodeidList.append(90)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_91.isEnabled():
            if self.checkBox_nodeid_91.isChecked():
                self.nodeidList.append(91)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_92.isEnabled():
            if self.checkBox_nodeid_92.isChecked():
                self.nodeidList.append(92)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_93.isEnabled():
            if self.checkBox_nodeid_93.isChecked():
                self.nodeidList.append(93)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_94.isEnabled():
            if self.checkBox_nodeid_94.isChecked():
                self.nodeidList.append(94)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_95.isEnabled():
            if self.checkBox_nodeid_95.isChecked():
                self.nodeidList.append(95)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_96.isEnabled():
            if self.checkBox_nodeid_96.isChecked():
                self.nodeidList.append(96)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_97.isEnabled():
            if self.checkBox_nodeid_97.isChecked():
                self.nodeidList.append(97)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_98.isEnabled():
            if self.checkBox_nodeid_98.isChecked():
                self.nodeidList.append(98)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_99.isEnabled():
            if self.checkBox_nodeid_99.isChecked():
                self.nodeidList.append(99)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_100.isEnabled():
            if self.checkBox_nodeid_100.isChecked():
                self.nodeidList.append(100)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_101.isEnabled():
            if self.checkBox_nodeid_101.isChecked():
                self.nodeidList.append(101)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_102.isEnabled():
            if self.checkBox_nodeid_102.isChecked():
                self.nodeidList.append(102)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_103.isEnabled():
            if self.checkBox_nodeid_103.isChecked():
                self.nodeidList.append(103)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_104.isEnabled():
            if self.checkBox_nodeid_104.isChecked():
                self.nodeidList.append(104)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_105.isEnabled():
            if self.checkBox_nodeid_105.isChecked():
                self.nodeidList.append(105)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_106.isEnabled():
            if self.checkBox_nodeid_106.isChecked():
                self.nodeidList.append(106)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_107.isEnabled():
            if self.checkBox_nodeid_107.isChecked():
                self.nodeidList.append(107)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_108.isEnabled():
            if self.checkBox_nodeid_108.isChecked():
                self.nodeidList.append(108)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_109.isEnabled():
            if self.checkBox_nodeid_109.isChecked():
                self.nodeidList.append(109)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_110.isEnabled():
            if self.checkBox_nodeid_110.isChecked():
                self.nodeidList.append(110)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_111.isEnabled():
            if self.checkBox_nodeid_111.isChecked():
                self.nodeidList.append(111)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_112.isEnabled():
            if self.checkBox_nodeid_112.isChecked():
                self.nodeidList.append(112)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_113.isEnabled():
            if self.checkBox_nodeid_113.isChecked():
                self.nodeidList.append(113)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_114.isEnabled():
            if self.checkBox_nodeid_114.isChecked():
                self.nodeidList.append(114)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_115.isEnabled():
            if self.checkBox_nodeid_115.isChecked():
                self.nodeidList.append(115)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_116.isEnabled():
            if self.checkBox_nodeid_116.isChecked():
                self.nodeidList.append(116)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_117.isEnabled():
            if self.checkBox_nodeid_117.isChecked():
                self.nodeidList.append(117)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_118.isEnabled():
            if self.checkBox_nodeid_118.isChecked():
                self.nodeidList.append(118)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_119.isEnabled():
            if self.checkBox_nodeid_119.isChecked():
                self.nodeidList.append(119)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_120.isEnabled():
            if self.checkBox_nodeid_120.isChecked():
                self.nodeidList.append(120)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_121.isEnabled():
            if self.checkBox_nodeid_121.isChecked():
                self.nodeidList.append(121)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_122.isEnabled():
            if self.checkBox_nodeid_122.isChecked():
                self.nodeidList.append(122)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_123.isEnabled():
            if self.checkBox_nodeid_123.isChecked():
                self.nodeidList.append(123)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_124.isEnabled():
            if self.checkBox_nodeid_124.isChecked():
                self.nodeidList.append(124)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_125.isEnabled():
            if self.checkBox_nodeid_125.isChecked():
                self.nodeidList.append(125)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_126.isEnabled():
            if self.checkBox_nodeid_126.isChecked():
                self.nodeidList.append(126)
                self.nodeidListLen  += 1
        if self.checkBox_nodeid_127.isEnabled():
            if self.checkBox_nodeid_127.isChecked():
                self.nodeidList.append(127)
                self.nodeidListLen  += 1
        self.updateNodeidList()
        self.close()
        pass

    def updateNodeidList(self):
        try:
            self.mainWindow.updateNodeidList(self.nodeidList,self.nodeidListLen) 
        except:
            pass
        pass
    def updateNodeidState(self,mainNodeid):
        #使能所有
        self.checkBox_nodeid_1.setEnabled(True)
        self.checkBox_nodeid_2.setEnabled(True)
        self.checkBox_nodeid_3.setEnabled(True)
        self.checkBox_nodeid_4.setEnabled(True)
        self.checkBox_nodeid_5.setEnabled(True)
        self.checkBox_nodeid_6.setEnabled(True)
        self.checkBox_nodeid_7.setEnabled(True)
        self.checkBox_nodeid_8.setEnabled(True)
        self.checkBox_nodeid_9.setEnabled(True)
        self.checkBox_nodeid_10.setEnabled(True)
        self.checkBox_nodeid_11.setEnabled(True)
        self.checkBox_nodeid_12.setEnabled(True)
        self.checkBox_nodeid_13.setEnabled(True)
        self.checkBox_nodeid_14.setEnabled(True)
        self.checkBox_nodeid_15.setEnabled(True)
        self.checkBox_nodeid_16.setEnabled(True)
        self.checkBox_nodeid_17.setEnabled(True)
        self.checkBox_nodeid_18.setEnabled(True)
        self.checkBox_nodeid_19.setEnabled(True)
        self.checkBox_nodeid_20.setEnabled(True)
        self.checkBox_nodeid_21.setEnabled(True)
        self.checkBox_nodeid_22.setEnabled(True)
        self.checkBox_nodeid_23.setEnabled(True)
        self.checkBox_nodeid_24.setEnabled(True)
        self.checkBox_nodeid_25.setEnabled(True)
        self.checkBox_nodeid_26.setEnabled(True)
        self.checkBox_nodeid_27.setEnabled(True)
        self.checkBox_nodeid_28.setEnabled(True)
        self.checkBox_nodeid_29.setEnabled(True)
        self.checkBox_nodeid_30.setEnabled(True)
        self.checkBox_nodeid_31.setEnabled(True)
        self.checkBox_nodeid_32.setEnabled(True)
        self.checkBox_nodeid_33.setEnabled(True)
        self.checkBox_nodeid_34.setEnabled(True)
        self.checkBox_nodeid_35.setEnabled(True)
        self.checkBox_nodeid_36.setEnabled(True)
        self.checkBox_nodeid_37.setEnabled(True)
        self.checkBox_nodeid_38.setEnabled(True)
        self.checkBox_nodeid_39.setEnabled(True)
        self.checkBox_nodeid_40.setEnabled(True)
        self.checkBox_nodeid_41.setEnabled(True)
        self.checkBox_nodeid_42.setEnabled(True)
        self.checkBox_nodeid_43.setEnabled(True)
        self.checkBox_nodeid_44.setEnabled(True)
        self.checkBox_nodeid_45.setEnabled(True)
        self.checkBox_nodeid_46.setEnabled(True)
        self.checkBox_nodeid_47.setEnabled(True)
        self.checkBox_nodeid_48.setEnabled(True)
        self.checkBox_nodeid_49.setEnabled(True)
        self.checkBox_nodeid_50.setEnabled(True)
        self.checkBox_nodeid_51.setEnabled(True)
        self.checkBox_nodeid_52.setEnabled(True)
        self.checkBox_nodeid_53.setEnabled(True)
        self.checkBox_nodeid_54.setEnabled(True)
        self.checkBox_nodeid_55.setEnabled(True)
        self.checkBox_nodeid_56.setEnabled(True)
        self.checkBox_nodeid_57.setEnabled(True)
        self.checkBox_nodeid_58.setEnabled(True)
        self.checkBox_nodeid_59.setEnabled(True)
        self.checkBox_nodeid_60.setEnabled(True)
        self.checkBox_nodeid_61.setEnabled(True)
        self.checkBox_nodeid_62.setEnabled(True)
        self.checkBox_nodeid_63.setEnabled(True)
        self.checkBox_nodeid_64.setEnabled(True)
        self.checkBox_nodeid_65.setEnabled(True)
        self.checkBox_nodeid_66.setEnabled(True)
        self.checkBox_nodeid_67.setEnabled(True)
        self.checkBox_nodeid_68.setEnabled(True)
        self.checkBox_nodeid_69.setEnabled(True)
        self.checkBox_nodeid_70.setEnabled(True)
        self.checkBox_nodeid_71.setEnabled(True)
        self.checkBox_nodeid_72.setEnabled(True)
        self.checkBox_nodeid_73.setEnabled(True)
        self.checkBox_nodeid_74.setEnabled(True)
        self.checkBox_nodeid_75.setEnabled(True)
        self.checkBox_nodeid_76.setEnabled(True)
        self.checkBox_nodeid_77.setEnabled(True)
        self.checkBox_nodeid_78.setEnabled(True)
        self.checkBox_nodeid_79.setEnabled(True)
        self.checkBox_nodeid_80.setEnabled(True)
        self.checkBox_nodeid_81.setEnabled(True)
        self.checkBox_nodeid_82.setEnabled(True)
        self.checkBox_nodeid_83.setEnabled(True)
        self.checkBox_nodeid_84.setEnabled(True)
        self.checkBox_nodeid_85.setEnabled(True)
        self.checkBox_nodeid_86.setEnabled(True)
        self.checkBox_nodeid_87.setEnabled(True)
        self.checkBox_nodeid_88.setEnabled(True)
        self.checkBox_nodeid_89.setEnabled(True)
        self.checkBox_nodeid_90.setEnabled(True)
        self.checkBox_nodeid_91.setEnabled(True)
        self.checkBox_nodeid_92.setEnabled(True)
        self.checkBox_nodeid_93.setEnabled(True)
        self.checkBox_nodeid_94.setEnabled(True)
        self.checkBox_nodeid_95.setEnabled(True)
        self.checkBox_nodeid_96.setEnabled(True)
        self.checkBox_nodeid_97.setEnabled(True)
        self.checkBox_nodeid_98.setEnabled(True)
        self.checkBox_nodeid_99.setEnabled(True)
        self.checkBox_nodeid_100.setEnabled(True)
        self.checkBox_nodeid_101.setEnabled(True)
        self.checkBox_nodeid_102.setEnabled(True)
        self.checkBox_nodeid_103.setEnabled(True)
        self.checkBox_nodeid_104.setEnabled(True)
        self.checkBox_nodeid_105.setEnabled(True)
        self.checkBox_nodeid_106.setEnabled(True)
        self.checkBox_nodeid_107.setEnabled(True)
        self.checkBox_nodeid_108.setEnabled(True)
        self.checkBox_nodeid_109.setEnabled(True)
        self.checkBox_nodeid_110.setEnabled(True)
        self.checkBox_nodeid_111.setEnabled(True)
        self.checkBox_nodeid_112.setEnabled(True)
        self.checkBox_nodeid_113.setEnabled(True)
        self.checkBox_nodeid_114.setEnabled(True)
        self.checkBox_nodeid_115.setEnabled(True)
        self.checkBox_nodeid_116.setEnabled(True)
        self.checkBox_nodeid_117.setEnabled(True)
        self.checkBox_nodeid_118.setEnabled(True)
        self.checkBox_nodeid_119.setEnabled(True)
        self.checkBox_nodeid_120.setEnabled(True)
        self.checkBox_nodeid_121.setEnabled(True)
        self.checkBox_nodeid_122.setEnabled(True)
        self.checkBox_nodeid_123.setEnabled(True)
        self.checkBox_nodeid_124.setEnabled(True)
        self.checkBox_nodeid_125.setEnabled(True)
        self.checkBox_nodeid_126.setEnabled(True)
        self.checkBox_nodeid_127.setEnabled(True)
        self.switchNodeidFunction(mainNodeid)()
        pass
    
    def disable_nodeid1(self):
        self.checkBox_nodeid_1.setEnabled(False)
        pass
    def disable_nodeid2(self):
        self.checkBox_nodeid_2.setEnabled(False)
        pass
    def disable_nodeid3(self):
        self.checkBox_nodeid_3.setEnabled(False)
        pass
    def disable_nodeid4(self):
        self.checkBox_nodeid_4.setEnabled(False)
        pass
    def disable_nodeid5(self):
        self.checkBox_nodeid_5.setEnabled(False)
        pass
    def disable_nodeid6(self):
        self.checkBox_nodeid_6.setEnabled(False)
        pass
    def disable_nodeid7(self):
        self.checkBox_nodeid_7.setEnabled(False)
        pass
    def disable_nodeid8(self):
        self.checkBox_nodeid_8.setEnabled(False)
        pass
    def disable_nodeid9(self):
        self.checkBox_nodeid_9.setEnabled(False)
        pass
    def disable_nodeid10(self):
        self.checkBox_nodeid_10.setEnabled(False)
        pass
    def disable_nodeid11(self):
        self.checkBox_nodeid_11.setEnabled(False)
        pass
    def disable_nodeid12(self):
        self.checkBox_nodeid_12.setEnabled(False)
        pass
    def disable_nodeid13(self):
        self.checkBox_nodeid_13.setEnabled(False)
        pass
    def disable_nodeid14(self):
        self.checkBox_nodeid_14.setEnabled(False)
        pass
    def disable_nodeid15(self):
        self.checkBox_nodeid_15.setEnabled(False)
        pass
    def disable_nodeid16(self):
        self.checkBox_nodeid_16.setEnabled(False)
        pass
    def disable_nodeid17(self):
        self.checkBox_nodeid_17.setEnabled(False)
        pass
    def disable_nodeid18(self):
        self.checkBox_nodeid_18.setEnabled(False)
        pass
    def disable_nodeid19(self):
        self.checkBox_nodeid_19.setEnabled(False)
        pass
    def disable_nodeid20(self):
        self.checkBox_nodeid_20.setEnabled(False)
        pass
    def disable_nodeid21(self):
        self.checkBox_nodeid_21.setEnabled(False)
        pass
    def disable_nodeid22(self):
        self.checkBox_nodeid_22.setEnabled(False)
        pass
    def disable_nodeid23(self):
        self.checkBox_nodeid_23.setEnabled(False)
        pass
    def disable_nodeid24(self):
        self.checkBox_nodeid_24.setEnabled(False)
        pass
    def disable_nodeid25(self):
        self.checkBox_nodeid_25.setEnabled(False)
        pass
    def disable_nodeid26(self):
        self.checkBox_nodeid_26.setEnabled(False)
        pass
    def disable_nodeid27(self):
        self.checkBox_nodeid_27.setEnabled(False)
        pass
    def disable_nodeid28(self):
        self.checkBox_nodeid_28.setEnabled(False)
        pass
    def disable_nodeid29(self):
        self.checkBox_nodeid_29.setEnabled(False)
        pass
    def disable_nodeid30(self):
        self.checkBox_nodeid_30.setEnabled(False)
        pass
    def disable_nodeid31(self):
        self.checkBox_nodeid_31.setEnabled(False)
        pass
    def disable_nodeid32(self):
        self.checkBox_nodeid_32.setEnabled(False)
        pass
    def disable_nodeid33(self):
        self.checkBox_nodeid_33.setEnabled(False)
        pass
    def disable_nodeid34(self):
        self.checkBox_nodeid_34.setEnabled(False)
        pass
    def disable_nodeid35(self):
        self.checkBox_nodeid_35.setEnabled(False)
        pass
    def disable_nodeid36(self):
        self.checkBox_nodeid_36.setEnabled(False)
        pass
    def disable_nodeid37(self):
        self.checkBox_nodeid_37.setEnabled(False)
        pass
    def disable_nodeid38(self):
        self.checkBox_nodeid_38.setEnabled(False)
        pass
    def disable_nodeid39(self):
        self.checkBox_nodeid_39.setEnabled(False)
        pass
    def disable_nodeid40(self):
        self.checkBox_nodeid_40.setEnabled(False)
        pass
    def disable_nodeid41(self):
        self.checkBox_nodeid_41.setEnabled(False)
        pass
    def disable_nodeid42(self):
        self.checkBox_nodeid_42.setEnabled(False)
        pass
    def disable_nodeid43(self):
        self.checkBox_nodeid_43.setEnabled(False)
        pass
    def disable_nodeid44(self):
        self.checkBox_nodeid_44.setEnabled(False)
        pass
    def disable_nodeid45(self):
        self.checkBox_nodeid_45.setEnabled(False)
        pass
    def disable_nodeid46(self):
        self.checkBox_nodeid_46.setEnabled(False)
        pass
    def disable_nodeid47(self):
        self.checkBox_nodeid_47.setEnabled(False)
        pass
    def disable_nodeid48(self):
        self.checkBox_nodeid_48.setEnabled(False)
        pass
    def disable_nodeid49(self):
        self.checkBox_nodeid_49.setEnabled(False)
        pass
    def disable_nodeid50(self):
        self.checkBox_nodeid_50.setEnabled(False)
        pass
    def disable_nodeid51(self):
        self.checkBox_nodeid_51.setEnabled(False)
        pass
    def disable_nodeid52(self):
        self.checkBox_nodeid_52.setEnabled(False)
        pass
    def disable_nodeid53(self):
        self.checkBox_nodeid_53.setEnabled(False)
        pass
    def disable_nodeid54(self):
        self.checkBox_nodeid_54.setEnabled(False)
        pass
    def disable_nodeid55(self):
        self.checkBox_nodeid_55.setEnabled(False)
        pass
    def disable_nodeid56(self):
        self.checkBox_nodeid_56.setEnabled(False)
        pass
    def disable_nodeid57(self):
        self.checkBox_nodeid_57.setEnabled(False)
        pass
    def disable_nodeid58(self):
        self.checkBox_nodeid_58.setEnabled(False)
        pass
    def disable_nodeid59(self):
        self.checkBox_nodeid_59.setEnabled(False)
        pass
    def disable_nodeid60(self):
        self.checkBox_nodeid_60.setEnabled(False)
        pass
    def disable_nodeid61(self):
        self.checkBox_nodeid_61.setEnabled(False)
        pass
    def disable_nodeid62(self):
        self.checkBox_nodeid_62.setEnabled(False)
        pass
    def disable_nodeid63(self):
        self.checkBox_nodeid_63.setEnabled(False)
        pass
    def disable_nodeid64(self):
        self.checkBox_nodeid_64.setEnabled(False)
        pass
    def disable_nodeid65(self):
        self.checkBox_nodeid_65.setEnabled(False)
        pass
    def disable_nodeid66(self):
        self.checkBox_nodeid_66.setEnabled(False)
        pass
    def disable_nodeid67(self):
        self.checkBox_nodeid_67.setEnabled(False)
        pass
    def disable_nodeid68(self):
        self.checkBox_nodeid_68.setEnabled(False)
        pass
    def disable_nodeid69(self):
        self.checkBox_nodeid_69.setEnabled(False)
        pass
    def disable_nodeid70(self):
        self.checkBox_nodeid_70.setEnabled(False)
        pass
    def disable_nodeid71(self):
        self.checkBox_nodeid_71.setEnabled(False)
        pass
    def disable_nodeid72(self):
        self.checkBox_nodeid_72.setEnabled(False)
        pass
    def disable_nodeid73(self):
        self.checkBox_nodeid_73.setEnabled(False)
        pass
    def disable_nodeid74(self):
        self.checkBox_nodeid_74.setEnabled(False)
        pass
    def disable_nodeid75(self):
        self.checkBox_nodeid_75.setEnabled(False)
        pass
    def disable_nodeid76(self):
        self.checkBox_nodeid_76.setEnabled(False)
        pass
    def disable_nodeid77(self):
        self.checkBox_nodeid_77.setEnabled(False)
        pass
    def disable_nodeid78(self):
        self.checkBox_nodeid_78.setEnabled(False)
        pass
    def disable_nodeid79(self):
        self.checkBox_nodeid_79.setEnabled(False)
        pass
    def disable_nodeid80(self):
        self.checkBox_nodeid_80.setEnabled(False)
        pass
    def disable_nodeid81(self):
        self.checkBox_nodeid_81.setEnabled(False)
        pass
    def disable_nodeid82(self):
        self.checkBox_nodeid_82.setEnabled(False)
        pass
    def disable_nodeid83(self):
        self.checkBox_nodeid_83.setEnabled(False)
        pass
    def disable_nodeid84(self):
        self.checkBox_nodeid_84.setEnabled(False)
        pass
    def disable_nodeid85(self):
        self.checkBox_nodeid_85.setEnabled(False)
        pass
    def disable_nodeid86(self):
        self.checkBox_nodeid_86.setEnabled(False)
        pass
    def disable_nodeid87(self):
        self.checkBox_nodeid_87.setEnabled(False)
        pass
    def disable_nodeid88(self):
        self.checkBox_nodeid_88.setEnabled(False)
        pass
    def disable_nodeid89(self):
        self.checkBox_nodeid_89.setEnabled(False)
        pass
    def disable_nodeid90(self):
        self.checkBox_nodeid_90.setEnabled(False)
        pass
    def disable_nodeid91(self):
        self.checkBox_nodeid_91.setEnabled(False)
        pass
    def disable_nodeid92(self):
        self.checkBox_nodeid_92.setEnabled(False)
        pass
    def disable_nodeid93(self):
        self.checkBox_nodeid_93.setEnabled(False)
        pass
    def disable_nodeid94(self):
        self.checkBox_nodeid_94.setEnabled(False)
        pass
    def disable_nodeid95(self):
        self.checkBox_nodeid_95.setEnabled(False)
        pass
    def disable_nodeid96(self):
        self.checkBox_nodeid_96.setEnabled(False)
        pass
    def disable_nodeid97(self):
        self.checkBox_nodeid_97.setEnabled(False)
        pass
    def disable_nodeid98(self):
        self.checkBox_nodeid_98.setEnabled(False)
        pass
    def disable_nodeid99(self):
        self.checkBox_nodeid_99.setEnabled(False)
        pass
    def disable_nodeid100(self):
        self.checkBox_nodeid_100.setEnabled(False)
        pass
    def disable_nodeid101(self):
        self.checkBox_nodeid_101.setEnabled(False)
        pass
    def disable_nodeid102(self):
        self.checkBox_nodeid_102.setEnabled(False)
        pass
    def disable_nodeid103(self):
        self.checkBox_nodeid_103.setEnabled(False)
        pass
    def disable_nodeid104(self):
        self.checkBox_nodeid_104.setEnabled(False)
        pass
    def disable_nodeid105(self):
        self.checkBox_nodeid_105.setEnabled(False)
        pass
    def disable_nodeid106(self):
        self.checkBox_nodeid_106.setEnabled(False)
        pass
    def disable_nodeid107(self):
        self.checkBox_nodeid_107.setEnabled(False)
        pass
    def disable_nodeid108(self):
        self.checkBox_nodeid_108.setEnabled(False)
        pass
    def disable_nodeid109(self):
        self.checkBox_nodeid_109.setEnabled(False)
        pass
    def disable_nodeid110(self):
        self.checkBox_nodeid_110.setEnabled(False)
        pass
    def disable_nodeid111(self):
        self.checkBox_nodeid_111.setEnabled(False)
        pass
    def disable_nodeid112(self):
        self.checkBox_nodeid_112.setEnabled(False)
        pass
    def disable_nodeid113(self):
        self.checkBox_nodeid_113.setEnabled(False)
        pass
    def disable_nodeid114(self):
        self.checkBox_nodeid_114.setEnabled(False)
        pass
    def disable_nodeid115(self):
        self.checkBox_nodeid_115.setEnabled(False)
        pass
    def disable_nodeid116(self):
        self.checkBox_nodeid_116.setEnabled(False)
        pass
    def disable_nodeid117(self):
        self.checkBox_nodeid_117.setEnabled(False)
        pass
    def disable_nodeid118(self):
        self.checkBox_nodeid_118.setEnabled(False)
        pass
    def disable_nodeid119(self):
        self.checkBox_nodeid_119.setEnabled(False)
        pass
    def disable_nodeid120(self):
        self.checkBox_nodeid_120.setEnabled(False)
        pass
    def disable_nodeid121(self):
        self.checkBox_nodeid_121.setEnabled(False)
        pass
    def disable_nodeid122(self):
        self.checkBox_nodeid_122.setEnabled(False)
        pass
    def disable_nodeid123(self):
        self.checkBox_nodeid_123.setEnabled(False)
        pass
    def disable_nodeid124(self):
        self.checkBox_nodeid_124.setEnabled(False)
        pass
    def disable_nodeid125(self):
        self.checkBox_nodeid_125.setEnabled(False)
        pass
    def disable_nodeid126(self):
        self.checkBox_nodeid_126.setEnabled(False)
        pass
    def disable_nodeid127(self):
        self.checkBox_nodeid_127.setEnabled(False)
        pass
    def default_switch(self):
        pass

    def switchNodeidFunction(self,index):
        indexs = {
            1: self.disable_nodeid1,
            2: self.disable_nodeid2,
            3: self.disable_nodeid3,
            4: self.disable_nodeid4,
            5: self.disable_nodeid5,
            6: self.disable_nodeid6,
            7: self.disable_nodeid7,
            8: self.disable_nodeid8,
            9: self.disable_nodeid9,
            10: self.disable_nodeid10,
            11: self.disable_nodeid11,
            12: self.disable_nodeid12,
            13: self.disable_nodeid13,
            14: self.disable_nodeid14,
            15: self.disable_nodeid15,
            16: self.disable_nodeid16,
            17: self.disable_nodeid17,
            18: self.disable_nodeid18,
            19: self.disable_nodeid19,
            20: self.disable_nodeid20,
            21: self.disable_nodeid21,
            22: self.disable_nodeid22,
            23: self.disable_nodeid23,
            24: self.disable_nodeid24,
            25: self.disable_nodeid25,
            26: self.disable_nodeid26,
            27: self.disable_nodeid27,
            28: self.disable_nodeid28,
            29: self.disable_nodeid29,
            30: self.disable_nodeid30,
            31: self.disable_nodeid31,
            32: self.disable_nodeid32,
            33: self.disable_nodeid33,
            34: self.disable_nodeid34,
            35: self.disable_nodeid35,
            36: self.disable_nodeid36,
            37: self.disable_nodeid37,
            38: self.disable_nodeid38,
            39: self.disable_nodeid39,
            40: self.disable_nodeid40,
            41: self.disable_nodeid41,
            42: self.disable_nodeid42,
            43: self.disable_nodeid43,
            44: self.disable_nodeid44,
            45: self.disable_nodeid45,
            46: self.disable_nodeid46,
            47: self.disable_nodeid47,
            48: self.disable_nodeid48,
            49: self.disable_nodeid49,
            50: self.disable_nodeid50,
            51: self.disable_nodeid51,
            52: self.disable_nodeid52,
            53: self.disable_nodeid53,
            54: self.disable_nodeid54,
            55: self.disable_nodeid55,
            56: self.disable_nodeid56,
            57: self.disable_nodeid57,
            58: self.disable_nodeid58,
            59: self.disable_nodeid59,
            60: self.disable_nodeid60,
            61: self.disable_nodeid61,
            62: self.disable_nodeid62,
            63: self.disable_nodeid63,
            64: self.disable_nodeid64,
            65: self.disable_nodeid65,
            66: self.disable_nodeid66,
            67: self.disable_nodeid67,
            68: self.disable_nodeid68,
            69: self.disable_nodeid69,
            70: self.disable_nodeid70,
            71: self.disable_nodeid71,
            72: self.disable_nodeid72,
            73: self.disable_nodeid73,
            74: self.disable_nodeid74,
            75: self.disable_nodeid75,
            76: self.disable_nodeid76,
            77: self.disable_nodeid77,
            78: self.disable_nodeid78,
            79: self.disable_nodeid79,
            80: self.disable_nodeid80,
            81: self.disable_nodeid81,
            82: self.disable_nodeid82,
            83: self.disable_nodeid83,
            84: self.disable_nodeid84,
            85: self.disable_nodeid85,
            86: self.disable_nodeid86,
            87: self.disable_nodeid87,
            88: self.disable_nodeid88,
            89: self.disable_nodeid89,
            90: self.disable_nodeid90,
            91: self.disable_nodeid91,
            92: self.disable_nodeid92,
            93: self.disable_nodeid93,
            94: self.disable_nodeid94,
            95: self.disable_nodeid95,
            96: self.disable_nodeid96,
            97: self.disable_nodeid97,
            98: self.disable_nodeid98,
            99: self.disable_nodeid99,
            100: self.disable_nodeid100,
            101: self.disable_nodeid101,
            102: self.disable_nodeid102,
            103: self.disable_nodeid103,
            104: self.disable_nodeid104,
            105: self.disable_nodeid105,
            106: self.disable_nodeid106,
            107: self.disable_nodeid107,
            108: self.disable_nodeid108,
            109: self.disable_nodeid109,
            110: self.disable_nodeid110,
            111: self.disable_nodeid111,
            112: self.disable_nodeid112,
            113: self.disable_nodeid113,
            114: self.disable_nodeid114,
            115: self.disable_nodeid115,
            116: self.disable_nodeid116,
            117: self.disable_nodeid117,
            118: self.disable_nodeid118,
            119: self.disable_nodeid119,
            120: self.disable_nodeid120,
            121: self.disable_nodeid121,
            122: self.disable_nodeid122,
            123: self.disable_nodeid123,
            124: self.disable_nodeid124,
            125: self.disable_nodeid125,
            126: self.disable_nodeid126,
            127: self.disable_nodeid127
        }    
        return indexs.get(index,self.default_switch)
