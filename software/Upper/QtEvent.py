'''
GNU GENERAL PUBLIC LICENSE (GPL) v3.0

Copyright (c) EERNIINUO
which is available at https://github.com/EERNINUO/GasSensor_Monitoring_System-HRBUST-2025

All rights reserved.
'''
from threading import Thread
from winsound import Beep
from PyQt6 import QtWidgets, QtCore
from Ui_UI_v1 import Ui_MainWindow
from Serial.SerialPort_Ctrl import SerialPort_Ctrl
from Data_Process import Data_Process

class QtEvent:
    def __init__(self, UI_MainWindow: Ui_MainWindow, serial_Ctrl: SerialPort_Ctrl, data_Process: Data_Process):
        self.UI_MainWindow = UI_MainWindow
        self.serial_ctrl = serial_Ctrl
        self.data_Process = data_Process  

        self.UI_MainWindow.DataShow_Widget.set_alarm_threshold(
            float(self.UI_MainWindow.alarm_Value.text())
        )

        self.UI_MainWindow.ComCtrl.clicked.connect(self.ComCtrl_clicked)
        self.UI_MainWindow.alarmValue_Set.clicked.connect(self.alarmValue_Set_clicked)

        self.data_Process.alarm_Signal.connect(self.alarm_Signal_Callback)
        # self.data_Process.highSpeed_Signal.connect(self.highSpeed_Signal_Callback)

    def ComCtrl_clicked(self):
        '''
        @brief 串口控制按钮点击事件
        '''
        if self.UI_MainWindow.ComList.currentText() == "":
            QtWidgets.QMessageBox.warning(None, "警告", "请选择串口")
            return

        if self.UI_MainWindow.ComCtrl.text() == "打开串口":
            if self.serial_ctrl.open_Serial(self.UI_MainWindow): 
                if self.serial_ctrl.serialPort_WorkThread is not None:
                    self.serial_ctrl.serialPort_WorkThread.data_received.connect(self.data_Process.ReceiveData_Callback)
                    self.UI_MainWindow.DataShow_Widget.start_plotting()
                self.UI_MainWindow.ComCtrl.setText("关闭串口")
            else:
                QtWidgets.QMessageBox.critical(None, "错误", "串口打开失败，请检查串口是否被占用")
        else:
            self.serial_ctrl.close_Serial()
            self.UI_MainWindow.DataShow_Widget.stop_plotting()
            self.UI_MainWindow.ComCtrl.setText("打开串口")

    def alarmValue_Set_clicked(self):
        '''
        @brief 报警值设置按钮点击事件
        '''
        if self.UI_MainWindow.alarm_Value.text() == "":
            QtWidgets.QMessageBox.warning(None, "警告", "请输入报警值")
            return  

        self.UI_MainWindow.DataShow_Widget.set_alarm_threshold(
            int(self.UI_MainWindow.alarm_Value.text())
        )
        self.data_Process.set_alarmValue(int(self.UI_MainWindow.alarm_Value.text()))

    def alarm_Signal_Callback(self, alarm: bool):
        '''
        @brief 报警信号回调函数
        '''
        if alarm:
            self.UI_MainWindow.NowValue.setStyleSheet("background-color: rgb(255, 0, 0);")  
            Thread(target= self.Alarm_Beep).start()
            QtWidgets.QMessageBox.warning(None, "警告", "当前值超过报警值")
        else:
            self.UI_MainWindow.NowValue.setStyleSheet("background-color: rgb(255, 255, 255);")

    def Alarm_Beep(self):
        '''
        @brief 报警提示音
        '''
        for _ in range(3):
            Beep(1000,500)

    # def highSpeed_Signal_Callback(self, highSpeedMode: bool):
    #     '''
    #     @brief 开启/关闭高速采样模式
    #     '''
    #     if highSpeedMode:
    #         self.serial_ctrl.serial_Transmit(100)
    #     else:
    #         self.serial_ctrl.serial_Transmit(1000)