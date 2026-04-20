'''
GNU GENERAL PUBLIC LICENSE (GPL) v3.0

Copyright (c) EERNIINUO
which is available at https://github.com/EERNINUO/GasSensor_Monitoring_System-HRBUST-2025

All rights reserved.
'''
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from Serial import SerialPort_Ctrl
from QtEvent import QtEvent
from Ui_UI_v1 import Ui_MainWindow
from Data_Process import Data_Process
import winsound
def beep():
    winsound.Beep(1000, 1000)

def main():
    # 创建UI对象
    ui = Ui_MainWindow()
    # 创建QApplication实例，用于管理应用程序的流控制和主事件循环
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui.setupUi(window)

    serial_ctrl = SerialPort_Ctrl()
    serial_ctrl.get_Serial(ui)
    data_process = Data_Process(ui)
    ui.DataShow_Widget.DataProcess_Class = data_process
    qtEvent = QtEvent(ui, serial_ctrl, data_process)

    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
