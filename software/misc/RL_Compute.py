# 本文件用于计算电阻RL的最优值
import numpy as np
import matplotlib.pyplot as plt

VCC = 5  # 电源电压

def vout_calc(Rl):
    return VCC * ((Rl / (1627.5 + Rl)) - (Rl / (8463 + Rl)))

if __name__ == '__main__':
    Rl_Value = np.linspace(1_00, 10_000, 9_900 + 1)  # 生成0到10000之间的1000个点
    Vout_Value = vout_calc(Rl_Value)  # 计算输出电压
    print("The best RL value is: {:d}".format(int(Rl_Value[Vout_Value.argmax()])))  # 输出最优的负载电阻值
    
    plt.plot(Rl_Value, Vout_Value)
    plt.show()