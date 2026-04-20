'''
GNU GENERAL PUBLIC LICENSE (GPL) v3.0

Copyright (c) EERNIINUO
which is available at https://github.com/EERNINUO/GasSensor_Monitoring_System-HRBUST-2025

All rights reserved.
'''
import serial
from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition

class SerialPort_Work(QThread):
    """串口工作线程"""
    data_received = pyqtSignal(int)          # 接收到的原始数据
    error_occurred = pyqtSignal(str)           # 错误信息
    status_changed = pyqtSignal(str, bool)     # 状态变化 (消息, 是否成功)
    connection_status = pyqtSignal(bool)       # 连接状态

    def __init__(self, openSerial: serial.Serial, parent=None):
        super(SerialPort_Work, self).__init__(parent)
        self.serial_port = openSerial
        self._mutex = QMutex()                 # 互斥锁，用于线程安全
        self._condition = QWaitCondition()     # 条件变量，用于线程同步

    def run(self):
        """线程主循环"""
        self._running = True
        
        while self._running:
            self._mutex.lock()
            if not self.serial_port or not self.serial_port.is_open:
                self._mutex.unlock()
                self.msleep(100)  # 等待连接
                continue
            
            try:
                # 检查是否有数据可读
                if self.serial_port.in_waiting > 0:
                    # 读取所有可用数据
                    data = self.serial_port.read(size= 2)
                    if data:
                        value = int.from_bytes(data, byteorder='little', signed=False)
                        self.data_received.emit(value)
                
                # 短暂休眠，避免CPU占用过高
                self._condition.wait(self._mutex, 10)  # 等待10ms或条件唤醒
                
            except serial.SerialException as e:
                self.error_occurred.emit(f"串口读取错误: {str(e)}")
                self._running = False
            except Exception as e:
                self.error_occurred.emit(f"未知错误: {str(e)}")
            finally:
                self._mutex.unlock()

    def write_Data(self, data):
        """写入数据（线程安全）"""
        self._mutex.lock()
        try:
            if self.serial_port and self.serial_port.is_open:
                if isinstance(data, str):
                    data = data.encode()
                self.serial_port.write(data)
                return True
            return False
        except Exception as e:
            self.error_occurred.emit(f"写入失败: {str(e)}")
            return False
        finally:
            self._mutex.unlock()
            self._condition.wakeAll()  # 唤醒线程


    def stop(self):
        """停止线程"""
        self._mutex.lock()
        self._running = False
        self._condition.wakeAll()  # 唤醒等待的线程
        self._mutex.unlock()
        self.wait()  # 等待线程结束
