# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\flowTpdo.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TPDO(object):
    def setupUi(self, TPDO):
        TPDO.setObjectName("TPDO")
        TPDO.resize(861, 520)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TPDO.sizePolicy().hasHeightForWidth())
        TPDO.setSizePolicy(sizePolicy)
        TPDO.setMinimumSize(QtCore.QSize(0, 520))
        TPDO.setMaximumSize(QtCore.QSize(16777215, 520))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        TPDO.setFont(font)
        self.groupBox = QtWidgets.QGroupBox(TPDO)
        self.groupBox.setGeometry(QtCore.QRect(0, 10, 870, 500))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(870, 500))
        self.groupBox.setMaximumSize(QtCore.QSize(870, 500))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.pushButton_tpdo_update = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_tpdo_update.setGeometry(QtCore.QRect(770, 460, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.pushButton_tpdo_update.setFont(font)
        self.pushButton_tpdo_update.setObjectName("pushButton_tpdo_update")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(0, 20, 851, 101))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(640, 10, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setGeometry(QtCore.QRect(220, 10, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.comboBox_tpdo_pdo1_data2 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_tpdo_pdo1_data2.setGeometry(QtCore.QRect(220, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo1_data2.setFont(font)
        self.comboBox_tpdo_pdo1_data2.setObjectName("comboBox_tpdo_pdo1_data2")
        self.comboBox_tpdo_pdo1_data1 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_tpdo_pdo1_data1.setGeometry(QtCore.QRect(10, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo1_data1.setFont(font)
        self.comboBox_tpdo_pdo1_data1.setObjectName("comboBox_tpdo_pdo1_data1")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(430, 10, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setGeometry(QtCore.QRect(10, 10, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.comboBox_tpdo_pdo1_data3 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_tpdo_pdo1_data3.setGeometry(QtCore.QRect(430, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo1_data3.setFont(font)
        self.comboBox_tpdo_pdo1_data3.setObjectName("comboBox_tpdo_pdo1_data3")
        self.comboBox_tpdo_pdo1_data4 = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_tpdo_pdo1_data4.setGeometry(QtCore.QRect(640, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo1_data4.setFont(font)
        self.comboBox_tpdo_pdo1_data4.setObjectName("comboBox_tpdo_pdo1_data4")
        self.comboBox_tpdo_pdo1_transmissionType = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_tpdo_pdo1_transmissionType.setGeometry(QtCore.QRect(10, 70, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo1_transmissionType.setFont(font)
        self.comboBox_tpdo_pdo1_transmissionType.setObjectName("comboBox_tpdo_pdo1_transmissionType")
        self.comboBox_tpdo_pdo1_syncStartValue = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_tpdo_pdo1_syncStartValue.setGeometry(QtCore.QRect(260, 70, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo1_syncStartValue.setFont(font)
        self.comboBox_tpdo_pdo1_syncStartValue.setObjectName("comboBox_tpdo_pdo1_syncStartValue")
        self.label_21 = QtWidgets.QLabel(self.groupBox_3)
        self.label_21.setGeometry(QtCore.QRect(10, 50, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.groupBox_3)
        self.label_22.setGeometry(QtCore.QRect(260, 50, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.groupBox_3)
        self.label_23.setGeometry(QtCore.QRect(80, 50, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.groupBox_3)
        self.label_24.setGeometry(QtCore.QRect(170, 50, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.lineEdit_tpdo_pdo1_inhibitTime = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_tpdo_pdo1_inhibitTime.setGeometry(QtCore.QRect(80, 70, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.lineEdit_tpdo_pdo1_inhibitTime.setFont(font)
        self.lineEdit_tpdo_pdo1_inhibitTime.setObjectName("lineEdit_tpdo_pdo1_inhibitTime")
        self.lineEdit_tpdo_pdo1_eventTimer = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_tpdo_pdo1_eventTimer.setGeometry(QtCore.QRect(170, 70, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.lineEdit_tpdo_pdo1_eventTimer.setFont(font)
        self.lineEdit_tpdo_pdo1_eventTimer.setObjectName("lineEdit_tpdo_pdo1_eventTimer")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setGeometry(QtCore.QRect(0, 130, 851, 101))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_9 = QtWidgets.QLabel(self.groupBox_4)
        self.label_9.setGeometry(QtCore.QRect(640, 10, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_4)
        self.label_10.setGeometry(QtCore.QRect(220, 10, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_4)
        self.label_11.setGeometry(QtCore.QRect(430, 10, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.groupBox_4)
        self.label_12.setGeometry(QtCore.QRect(10, 10, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.comboBox_tpdo_pdo2_data1 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_tpdo_pdo2_data1.setGeometry(QtCore.QRect(10, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo2_data1.setFont(font)
        self.comboBox_tpdo_pdo2_data1.setObjectName("comboBox_tpdo_pdo2_data1")
        self.comboBox_tpdo_pdo2_data2 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_tpdo_pdo2_data2.setGeometry(QtCore.QRect(220, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo2_data2.setFont(font)
        self.comboBox_tpdo_pdo2_data2.setObjectName("comboBox_tpdo_pdo2_data2")
        self.comboBox_tpdo_pdo2_data3 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_tpdo_pdo2_data3.setGeometry(QtCore.QRect(430, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo2_data3.setFont(font)
        self.comboBox_tpdo_pdo2_data3.setObjectName("comboBox_tpdo_pdo2_data3")
        self.comboBox_tpdo_pdo2_data4 = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_tpdo_pdo2_data4.setGeometry(QtCore.QRect(640, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo2_data4.setFont(font)
        self.comboBox_tpdo_pdo2_data4.setObjectName("comboBox_tpdo_pdo2_data4")
        self.label_25 = QtWidgets.QLabel(self.groupBox_4)
        self.label_25.setGeometry(QtCore.QRect(10, 50, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.comboBox_tpdo_pdo2_syncStartValue = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_tpdo_pdo2_syncStartValue.setGeometry(QtCore.QRect(260, 70, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo2_syncStartValue.setFont(font)
        self.comboBox_tpdo_pdo2_syncStartValue.setObjectName("comboBox_tpdo_pdo2_syncStartValue")
        self.comboBox_tpdo_pdo2_transmissionType = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_tpdo_pdo2_transmissionType.setGeometry(QtCore.QRect(10, 70, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo2_transmissionType.setFont(font)
        self.comboBox_tpdo_pdo2_transmissionType.setObjectName("comboBox_tpdo_pdo2_transmissionType")
        self.label_26 = QtWidgets.QLabel(self.groupBox_4)
        self.label_26.setGeometry(QtCore.QRect(170, 50, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.groupBox_4)
        self.label_27.setGeometry(QtCore.QRect(80, 50, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(self.groupBox_4)
        self.label_28.setGeometry(QtCore.QRect(260, 50, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.lineEdit_tpdo_pdo2_inhibitTime = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_tpdo_pdo2_inhibitTime.setGeometry(QtCore.QRect(80, 70, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.lineEdit_tpdo_pdo2_inhibitTime.setFont(font)
        self.lineEdit_tpdo_pdo2_inhibitTime.setObjectName("lineEdit_tpdo_pdo2_inhibitTime")
        self.lineEdit_tpdo_pdo2_eventTimer = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_tpdo_pdo2_eventTimer.setGeometry(QtCore.QRect(170, 70, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.lineEdit_tpdo_pdo2_eventTimer.setFont(font)
        self.lineEdit_tpdo_pdo2_eventTimer.setObjectName("lineEdit_tpdo_pdo2_eventTimer")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_5.setGeometry(QtCore.QRect(0, 240, 851, 101))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.label_13 = QtWidgets.QLabel(self.groupBox_5)
        self.label_13.setGeometry(QtCore.QRect(640, 10, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.groupBox_5)
        self.label_14.setGeometry(QtCore.QRect(220, 10, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.groupBox_5)
        self.label_15.setGeometry(QtCore.QRect(430, 10, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.groupBox_5)
        self.label_16.setGeometry(QtCore.QRect(10, 10, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.comboBox_tpdo_pdo3_data1 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_tpdo_pdo3_data1.setGeometry(QtCore.QRect(10, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo3_data1.setFont(font)
        self.comboBox_tpdo_pdo3_data1.setObjectName("comboBox_tpdo_pdo3_data1")
        self.comboBox_tpdo_pdo3_data2 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_tpdo_pdo3_data2.setGeometry(QtCore.QRect(220, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo3_data2.setFont(font)
        self.comboBox_tpdo_pdo3_data2.setObjectName("comboBox_tpdo_pdo3_data2")
        self.comboBox_tpdo_pdo3_data3 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_tpdo_pdo3_data3.setGeometry(QtCore.QRect(430, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo3_data3.setFont(font)
        self.comboBox_tpdo_pdo3_data3.setObjectName("comboBox_tpdo_pdo3_data3")
        self.comboBox_tpdo_pdo3_data4 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_tpdo_pdo3_data4.setGeometry(QtCore.QRect(640, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo3_data4.setFont(font)
        self.comboBox_tpdo_pdo3_data4.setObjectName("comboBox_tpdo_pdo3_data4")
        self.label_29 = QtWidgets.QLabel(self.groupBox_5)
        self.label_29.setGeometry(QtCore.QRect(10, 50, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.comboBox_tpdo_pdo3_syncStartValue = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_tpdo_pdo3_syncStartValue.setGeometry(QtCore.QRect(260, 70, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo3_syncStartValue.setFont(font)
        self.comboBox_tpdo_pdo3_syncStartValue.setObjectName("comboBox_tpdo_pdo3_syncStartValue")
        self.comboBox_tpdo_pdo3_transmissionType = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_tpdo_pdo3_transmissionType.setGeometry(QtCore.QRect(10, 70, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo3_transmissionType.setFont(font)
        self.comboBox_tpdo_pdo3_transmissionType.setObjectName("comboBox_tpdo_pdo3_transmissionType")
        self.label_30 = QtWidgets.QLabel(self.groupBox_5)
        self.label_30.setGeometry(QtCore.QRect(170, 50, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.label_31 = QtWidgets.QLabel(self.groupBox_5)
        self.label_31.setGeometry(QtCore.QRect(80, 50, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.label_32 = QtWidgets.QLabel(self.groupBox_5)
        self.label_32.setGeometry(QtCore.QRect(260, 50, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.lineEdit_tpdo_pdo3_inhibitTime = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_tpdo_pdo3_inhibitTime.setGeometry(QtCore.QRect(80, 70, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.lineEdit_tpdo_pdo3_inhibitTime.setFont(font)
        self.lineEdit_tpdo_pdo3_inhibitTime.setObjectName("lineEdit_tpdo_pdo3_inhibitTime")
        self.lineEdit_tpdo_pdo3_eventTimer = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_tpdo_pdo3_eventTimer.setGeometry(QtCore.QRect(170, 70, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.lineEdit_tpdo_pdo3_eventTimer.setFont(font)
        self.lineEdit_tpdo_pdo3_eventTimer.setObjectName("lineEdit_tpdo_pdo3_eventTimer")
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_6.setGeometry(QtCore.QRect(0, 350, 851, 101))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setObjectName("groupBox_6")
        self.label_17 = QtWidgets.QLabel(self.groupBox_6)
        self.label_17.setGeometry(QtCore.QRect(640, 10, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.groupBox_6)
        self.label_18.setGeometry(QtCore.QRect(220, 0, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.groupBox_6)
        self.label_19.setGeometry(QtCore.QRect(430, 10, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.groupBox_6)
        self.label_20.setGeometry(QtCore.QRect(10, 10, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.comboBox_tpdo_pdo4_data1 = QtWidgets.QComboBox(self.groupBox_6)
        self.comboBox_tpdo_pdo4_data1.setGeometry(QtCore.QRect(10, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo4_data1.setFont(font)
        self.comboBox_tpdo_pdo4_data1.setObjectName("comboBox_tpdo_pdo4_data1")
        self.comboBox_tpdo_pdo4_data2 = QtWidgets.QComboBox(self.groupBox_6)
        self.comboBox_tpdo_pdo4_data2.setGeometry(QtCore.QRect(220, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo4_data2.setFont(font)
        self.comboBox_tpdo_pdo4_data2.setObjectName("comboBox_tpdo_pdo4_data2")
        self.comboBox_tpdo_pdo4_data3 = QtWidgets.QComboBox(self.groupBox_6)
        self.comboBox_tpdo_pdo4_data3.setGeometry(QtCore.QRect(430, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo4_data3.setFont(font)
        self.comboBox_tpdo_pdo4_data3.setObjectName("comboBox_tpdo_pdo4_data3")
        self.comboBox_tpdo_pdo4_data4 = QtWidgets.QComboBox(self.groupBox_6)
        self.comboBox_tpdo_pdo4_data4.setGeometry(QtCore.QRect(640, 30, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo4_data4.setFont(font)
        self.comboBox_tpdo_pdo4_data4.setObjectName("comboBox_tpdo_pdo4_data4")
        self.label_33 = QtWidgets.QLabel(self.groupBox_6)
        self.label_33.setGeometry(QtCore.QRect(10, 50, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.comboBox_tpdo_pdo4_syncStartValue = QtWidgets.QComboBox(self.groupBox_6)
        self.comboBox_tpdo_pdo4_syncStartValue.setGeometry(QtCore.QRect(260, 70, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo4_syncStartValue.setFont(font)
        self.comboBox_tpdo_pdo4_syncStartValue.setObjectName("comboBox_tpdo_pdo4_syncStartValue")
        self.comboBox_tpdo_pdo4_transmissionType = QtWidgets.QComboBox(self.groupBox_6)
        self.comboBox_tpdo_pdo4_transmissionType.setGeometry(QtCore.QRect(10, 70, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.comboBox_tpdo_pdo4_transmissionType.setFont(font)
        self.comboBox_tpdo_pdo4_transmissionType.setObjectName("comboBox_tpdo_pdo4_transmissionType")
        self.label_34 = QtWidgets.QLabel(self.groupBox_6)
        self.label_34.setGeometry(QtCore.QRect(170, 50, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_34.setFont(font)
        self.label_34.setObjectName("label_34")
        self.label_35 = QtWidgets.QLabel(self.groupBox_6)
        self.label_35.setGeometry(QtCore.QRect(80, 50, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_35.setFont(font)
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self.groupBox_6)
        self.label_36.setGeometry(QtCore.QRect(260, 50, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.label_36.setFont(font)
        self.label_36.setObjectName("label_36")
        self.lineEdit_tpdo_pdo4_inhibitTime = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEdit_tpdo_pdo4_inhibitTime.setGeometry(QtCore.QRect(80, 70, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.lineEdit_tpdo_pdo4_inhibitTime.setFont(font)
        self.lineEdit_tpdo_pdo4_inhibitTime.setObjectName("lineEdit_tpdo_pdo4_inhibitTime")
        self.lineEdit_tpdo_pdo4_eventTimer = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEdit_tpdo_pdo4_eventTimer.setGeometry(QtCore.QRect(170, 70, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.lineEdit_tpdo_pdo4_eventTimer.setFont(font)
        self.lineEdit_tpdo_pdo4_eventTimer.setObjectName("lineEdit_tpdo_pdo4_eventTimer")
        self.pushButton_tpdo_clear = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_tpdo_clear.setGeometry(QtCore.QRect(10, 460, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)
        self.pushButton_tpdo_clear.setFont(font)
        self.pushButton_tpdo_clear.setObjectName("pushButton_tpdo_clear")

        self.retranslateUi(TPDO)
        QtCore.QMetaObject.connectSlotsByName(TPDO)

    def retranslateUi(self, TPDO):
        _translate = QtCore.QCoreApplication.translate
        TPDO.setWindowTitle(_translate("TPDO", "Form"))
        self.groupBox.setTitle(_translate("TPDO", "TPDO config"))
        self.pushButton_tpdo_update.setText(_translate("TPDO", "Update"))
        self.groupBox_3.setTitle(_translate("TPDO", "TPDO1"))
        self.label_5.setText(_translate("TPDO", "data4"))
        self.label_6.setText(_translate("TPDO", "data2"))
        self.label_7.setText(_translate("TPDO", "data3"))
        self.label_8.setText(_translate("TPDO", "data1"))
        self.label_21.setText(_translate("TPDO", "transType"))
        self.label_22.setText(_translate("TPDO", "SYNCStartValue"))
        self.label_23.setText(_translate("TPDO", "inhibitTime"))
        self.label_24.setText(_translate("TPDO", "eventTimer"))
        self.groupBox_4.setTitle(_translate("TPDO", "TPDO2"))
        self.label_9.setText(_translate("TPDO", "data4"))
        self.label_10.setText(_translate("TPDO", "data2"))
        self.label_11.setText(_translate("TPDO", "data3"))
        self.label_12.setText(_translate("TPDO", "data1"))
        self.label_25.setText(_translate("TPDO", "transType"))
        self.label_26.setText(_translate("TPDO", "eventTimer"))
        self.label_27.setText(_translate("TPDO", "inhibitTime"))
        self.label_28.setText(_translate("TPDO", "SYNCStartValue"))
        self.groupBox_5.setTitle(_translate("TPDO", "TPDO3"))
        self.label_13.setText(_translate("TPDO", "data4"))
        self.label_14.setText(_translate("TPDO", "data2"))
        self.label_15.setText(_translate("TPDO", "data3"))
        self.label_16.setText(_translate("TPDO", "data1"))
        self.label_29.setText(_translate("TPDO", "transType"))
        self.label_30.setText(_translate("TPDO", "eventTimer"))
        self.label_31.setText(_translate("TPDO", "inhibitTime"))
        self.label_32.setText(_translate("TPDO", "SYNCStartValue"))
        self.groupBox_6.setTitle(_translate("TPDO", "TPDO4"))
        self.label_17.setText(_translate("TPDO", "data4"))
        self.label_18.setText(_translate("TPDO", "data2"))
        self.label_19.setText(_translate("TPDO", "data3"))
        self.label_20.setText(_translate("TPDO", "data1"))
        self.label_33.setText(_translate("TPDO", "transType"))
        self.label_34.setText(_translate("TPDO", "eventTimer"))
        self.label_35.setText(_translate("TPDO", "inhibitTime"))
        self.label_36.setText(_translate("TPDO", "SYNCStartValue"))
        self.pushButton_tpdo_clear.setText(_translate("TPDO", "Clear"))
