'''
GNU GENERAL PUBLIC LICENSE (GPL) v3.0

Copyright (c) EERNIINUO
which is available at https://github.com/EERNINUO/GasSensor_Monitoring_System-HRBUST-2025

All rights reserved.
'''
from typing import Optional
import serial
from serial.tools import list_ports
from PyQt6.QtCore import pyqtSignal, QTimer
from Ui_UI_v1 import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from .SerialPort_Work import SerialPort_Work
from Data_Process import Data_Process

BYTE_SIZE = (5, 6, 7, 8)
STOP_BIT = (1, 1.5, 2)
PARITES = ['N', 'E', 'O', 'M', 'S']

class SerialPort_Ctrl():
    """串口控制"""
    
    def __init__(self):
        super().__init__()
        self.Open_SerialPort: Optional[serial.Serial] = None
        self.updateSerial_timer: Optional[QTimer] = None
        self.serialPort_WorkThread: Optional[SerialPort_Work] = None

    def get_Serial(self, UI_MainWindow: Ui_MainWindow):
        '''
        @brief 获取串口列表并添加到UI界面

        @param UI_MainWindow: 需要要添加串口列表的窗口
        @type UI_MainWindow: Ui_MainWindow
        '''
        def update_Serial():
            UI_MainWindow.ComList.clear()
            ports_list = list(list_ports.comports())
            for port in ports_list:
                UI_MainWindow.ComList.addItem(port.device)

        self.updateSerial_timer = QTimer()
        self.updateSerial_timer.timeout.connect(update_Serial)
        self.updateSerial_timer.start(200)    

    def open_Serial(self, Ui: Ui_MainWindow):
        '''
        @brief 打开串口
        
        @param Ui: 从UI界面获取串口参数
            type Ui: Ui_MainWindow
        '''
        port = Ui.ComList.currentText()
        baudrate = int(Ui.BaudRate.currentText())
        bytesize = BYTE_SIZE[Ui.DataBit.currentIndex()]
        stopbits = STOP_BIT[Ui.StopBit.currentIndex()]
        parity = PARITES[Ui.CaliBit.currentIndex()]

        try:
            self.Open_SerialPort = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout=0.1)
            self.serialPort_WorkThread = SerialPort_Work(self.Open_SerialPort)
            self.serialPort_WorkThread.start() 
            return True 
        except serial.SerialException as e:
            return False

    def close_Serial(self):
        '''
        @brief 关闭串口
        
        '''
        if self.serialPort_WorkThread is not None:
            self.serialPort_WorkThread.stop()
        if  self.Open_SerialPort is not None:   
            self.Open_SerialPort.close()
        self.Open_SerialPort = None

    def serial_Transmit(self, data) -> bool:
        '''
        @brief 串口发送数据

        @param data: 发送的数据
        @type data: bytes
        @return: 发送成功返回True，否则返回False
        '''
        if self.Open_SerialPort is not None:
            print(bytes([data]))
            self.Open_SerialPort.write(bytes([data]))
            return True
        else:
            return False