import time
import math
import numpy as np
from PyQt6.QtCore import pyqtSignal, QObject
from Ui_UI_v1 import Ui_MainWindow

RL_VALUE = 6_200

class Data_Process(QObject):
    alarm_Signal = pyqtSignal(bool)
    highSpeed_Signal = pyqtSignal(bool)

    def __init__(self, UI_MainWindow: Ui_MainWindow):
        super().__init__()
        self.UI_MainWindow = UI_MainWindow
        self.alarmValue = int(UI_MainWindow.alarm_Value.text()) # 报警值
        self.data_time = np.array([]) # 时间数组
        self.data_data = np.array([]) # 数据数组
        self.highSpeedMode = False  # 高速采样模式
        self.alarm = False  # 报警

    def ReceiveData_Callback(self, data):
        voltage = 5* data / 1024
        print(voltage)
        Rs_value = 5 * RL_VALUE / voltage - RL_VALUE
        gas_concentration = 887 * (Rs_value / 13881.95) ** -2.185 # 6510 是传感器1000ppm下阻值
        self.UI_MainWindow.NowValue.setText(f"{gas_concentration:.2f} ppm")
        if gas_concentration > 10000:
            show_data = 10000
        elif gas_concentration < 15:
            show_data = 15
        else:
            show_data = gas_concentration
        self.add_data(show_data)

        # if (value >= (self.alarmValue*0.8)) and (not self.alarm):
        #     self.highSpeedMode = True
        #     self.highSpeed_Signal.emit(True)
        # elif (value < (self.alarmValue*0.8) and not self.highSpeedMode):
        #     self.highSpeedMode = False
        #     self.highSpeed_Signal.emit(False)

        if (gas_concentration >= self.alarmValue) and (not self.alarm):
            self.alarm = True
            self.alarm_Signal.emit(True)
        elif (gas_concentration < self.alarmValue) and self.alarm:
            self.alarm = False
            self.alarm_Signal.emit(False)

    def add_data(self, data):
        self.data_time = np.append(self.data_time, time.time())
        self.data_data = np.append(self.data_data, data)

    def get_data(self) -> tuple: 
        if self.highSpeedMode:
            lens = 450
        else:
            lens = 45

        if lens > len(self.data_time):
            return self.data_time, self.data_data
        else:
            return self.data_time[-lens:], self.data_data[-lens:]
        
    def set_alarmValue(self, value):
        self.alarmValue = value