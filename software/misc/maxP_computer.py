import numpy as np

VCC= 5
RL_VALUE = 4_300

def P_Computer(Rs, Vcc):
    P = ((Vcc / (Rs + RL_VALUE)) ** 2 ) * Rs   
    return P

if __name__ == "__main__":
    Rs = np.linspace(1627.5, 8463, 10_000)
    P = P_Computer(Rs, VCC)
    print(P.max())