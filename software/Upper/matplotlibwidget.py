'''
GNU GENERAL PUBLIC LICENSE (GPL) v3.0

Copyright (c) EERNIINUO
which is available at https://github.com/EERNINUO/GasSensor_Monitoring_System-HRBUST-2025

All rights reserved.
'''
from typing import Optional
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer
import matplotlib.dates as mdates
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
import Data_Process

class MatplotlibWidget(QWidget):
    """自定义QWidget，用于显示Matplotlib图形"""
    def __init__(self, parent=None):
        super().__init__(parent)

        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.DataProcess_Class: Optional[Data_Process.Data_Process] = None

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure) # 创建一个FigureCanvas对象，必须通过FigureCanvas对象才能绘制图像
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)
        
        # 创建坐标轴并绘制初始图形
        self.ax = self.figure.add_subplot(111)

        self.phase = 0  # 相位，用于动态变化
        self.line = None  # 存储线条对象
        
        # 创建定时器（但不立即启动）
        self.timer = QTimer()
        self.init_plot()
        self.timer.timeout.connect(self.update_data)

    def init_plot(self):
        """初始化绘图设置"""
        self.ax.clear()

        # 设置y轴为对数刻度
        self.ax.set_yscale('log')
        
        # 设置标题和标签
        self.ax.set_title('数据监控', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('时间', fontsize=12)
        self.ax.set_ylabel('浓度(ppm)', fontsize=12)
        
        # 设置网格
        self.ax.grid(True, which='major', linestyle='--', alpha=0.9)
        self.ax.grid(True, which='minor', linestyle=':', alpha=0.7)    # 次网格线，使用点线
        
        # 设置时间格式
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.figure.autofmt_xdate()  # 自动旋转日期标签
        
        # 绘制初始空线
        self.line, = self.ax.plot([], [], 'b-', linewidth=2, label='实时数据')
        self.ax.legend(loc='upper right')

        self.alarm_line = self.ax.axhline(y=50, color='r', linestyle='--', linewidth=2, label='报警阈值', alpha=0.7)
        self.alarm_line.set_visible(False)
        
        # 设置初始坐标轴范围
        self.ax.set_xlim(datetime.now() - timedelta(seconds=45), datetime.now() + timedelta(seconds=5))
        self.ax.set_ylim(10, 12_000)
        
        self.canvas.draw()

    def update_data(self):
        if self.DataProcess_Class is None:
            return

        self.time_data, self.value_data = self.DataProcess_Class.get_data()
        if len(self.time_data) > 0:
            if isinstance(self.time_data[0], (int, float)):
                self.time_data = [datetime.fromtimestamp(ts) for ts in self.time_data]
        if self.line is not None:
            self.line.set_data(mdates.date2num(self.time_data), self.value_data)
            self.auto_adjust_axes()
            self.canvas.draw_idle()

    def set_alarm_threshold(self, threshold: float):    
        if self.alarm_line is not None:
            self.alarm_line.set_ydata([threshold, threshold])
            self.alarm_line.set_visible(True)
            self.canvas.draw_idle()

    def auto_adjust_axes(self):
        """自动调整坐标轴范围"""
        if len(self.time_data) > 1 and len(self.value_data) > 1:
            try:
                # 计算时间范围
                time_min = min(self.time_data)
                time_max = max(self.time_data)
                time_span = (time_max - time_min).total_seconds()
                
                # 如果时间跨度小于10秒，则显示更多范围
                # if time_span < 10:
                display_seconds = 45  # 显示最近45秒
                margin = 5
                time_min = time_max - timedelta(seconds=display_seconds)
                time_max = time_max + timedelta(seconds=margin)
                # else:
                #     # 添加10%的边距
                #     margin = time_span * 0.1
                #     time_min = time_min - timedelta(seconds=margin)
                #     time_max = time_max + timedelta(seconds=margin)
                
                # 设置X轴范围
                self.ax.set_xlim(time_min, time_max)
                
                # 重绘网格和格式
                self.ax.grid(True, linestyle='--', alpha=0.7)
                self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
                self.figure.autofmt_xdate()
                
            except Exception as e:
                print(f"调整坐标轴时出错: {e}")

    def start_plotting(self, interval_ms=100):
        """开始绘图"""
        if not self.timer.isActive():
            self.timer.start(interval_ms)
    
    def stop_plotting(self):
        """停止绘图"""
        if self.timer.isActive():
            self.timer.stop()