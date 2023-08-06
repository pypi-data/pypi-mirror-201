#!/usr/bin/env python

import cmath
import math
import time

import numpy as np


def fasor(R, theta):
    Re = R * math.cos(theta * math.pi / 180)
    Im = R * math.sin(theta**math.pi / 180)
    Z = complex(Re, Im)
    return Z


def forward_sweep(barras, linhas, Vbus):
    NB = len(barras)
    Nbr = len(linhas)
    cam_max = int(max(barras[:, 1]))  # camada mais profunda
    SL = np.zeros(NB) * complex(0, 0)
    Sbr = np.zeros(Nbr) * complex(0, 0)
    Sloss = np.zeros(NB) * complex(0, 0)

    for c in range(cam_max, 0, -1):  # da camada mais profunda até a superior
        for i in range(0, NB):  # procurando barras ligadas na camada C
            if int(barras[i, 1]) == c:
                SL[i] = 1000 * carga_zip(
                    barras[i, 2],
                    barras[i, 3],
                    abs(Vbus[i]),
                    abs(V_SE),
                    a0,
                    a1,
                    a2,
                    b0,
                    b1,
                    b2,
                )
                # SL[i] = 1000*complex(barras[i,2], barras[i,3])#carga da barra
                bus = int(barras[i, 0])

                for j in range(0, Nbr):  # procurando barras a montante
                    if linhas[j, 2] == bus:
                        bus_up = int(linhas[j, 1])
                        branch = int(linhas[j, 0])
                        Sloss[i] = (math.pow(abs(SL[i]) / abs(Vbus[i]), 2)) * complex(
                            linhas[branch, 3], linhas[branch, 4]
                        )
                        Sbr[branch] = (
                            SL[i] + Sloss[i]
                        )  # fluxo no ramo = carga da barra + perda no ramo

                        for k in range(0, Nbr):  # procurando barras a jusante
                            if int(linhas[k, 1]) == bus:
                                bus_down = int(linhas[k, 2])
                                branch_down = int(linhas[k, 0])
                                Sbr[branch] = Sbr[branch] + Sbr[branch_down]
    return Sbr


def backward_sweep(V_SE, barras, linhas, Sbr):
    NB = len(barras)
    Nbr = len(linhas)
    cam_max = int(max(barras[:, 1]))  # camada mais profunda
    Vbus = V_SE * np.ones(NB)
    Vbus[0] = V_SE

    for c in range(0, cam_max):  # da camada superior até a mais profunda
        for i in range(0, NB):  # procurando barras ligadas na camada C
            if barras[i, 1] == c:
                bus = int(barras[i][0])

                for j in range(0, Nbr):  # procurando barras a jusante
                    if linhas[j, 1] == bus:
                        bus_down = int(linhas[j, 2])
                        Vbus[bus_down] = Vbus[bus] - complex(
                            linhas[j, 3], linhas[j, 4]
                        ) * complex.conjugate(Sbr[j] / Vbus[bus])
    return Vbus


def sum_power(Vbus_old, TOL, max_iter, barras, linhas):
    barras = organiza_camada(barras_sc, linhas)
    Sbr = forward_sweep(barras, linhas, Vbus_old)
    Vbus = backward_sweep(V_SE, barras, linhas, Sbr)
    error = max(abs(abs(Vbus) - abs(Vbus_old)))
    iter = 0
    print("                    Processamento                       ")
    print("                                                        ")
    print("Tolerância admitida:", TOL)
    print("")
    print("iteração           erro")
    print(iter, error)
    while error >= TOL:
        Vbus_old = Vbus
        Sbr = forward_sweep(barras, linhas, Vbus_old)
        Vbus = backward_sweep(V_SE, barras, linhas, Sbr)
        error = max(abs(abs(Vbus) - abs(Vbus_old)))
        iter = iter + 1
        print(iter, error)

    [P_loss, Q_loss] = perdas(linhas, Vbus, Sbr)
    return Vbus, Sbr, P_loss, Q_loss, iter, error


def carga_zip(Pnom, Qnom, V, Vnom, a0, a1, a2, b0, b1, b2):
    P = Pnom * (a0 + a1 * (V / Vnom) + a2 * math.pow((V / Vnom), 2))
    Q = Qnom * (b0 + b1 * (V / Vnom) + b2 * math.pow((V / Vnom), 2))
    S = complex(P, Q)
    return S


def carga_zip_freq(Pnom, Qnom, V, Vnom, a0, a1, a2, b0, b1, b2, f_at, kp):
    P = Pnom * (a0 + a1 * (V / Vnom) + a2 * math.pow((V / Vnom), 2))
    Q = Qnom * (b0 + b1 * (V / Vnom) + b2 * math.pow((V / Vnom), 2))
    kf = 1 + kp * (f_at - 60) / 60
    S = complex(P, Q) * kf
    return S


def organiza_camada(barras, linhas):
    NB = len(barras)
    Nbr = len(linhas)
    barras_new = np.zeros((NB, 4), dtype=np.float64)

    for i in range(0, NB):
        barras_new[i, 0] = barras[i, 0]
        barras_new[i, 2] = barras[i, 1]
        barras_new[i, 3] = barras[i, 2]

    barras_new[0, 1] = 0  # DefiniÃ§Ã£o da barra de referÃªncia

    for i in range(0, NB):
        bus_up = int(barras_new[i, 0])

        for j in range(0, Nbr):
            if linhas[j, 1] == bus_up:
                bus_down = int(linhas[j, 2])
                barras_new[bus_down, 1] = barras_new[bus_up, 1] + 1

    return barras_new


def perdas(linhas, Vbus, Sbr):
    P_loss = np.zeros(len(Sbr))
    Q_loss = np.zeros(len(Sbr))
    for i in range(0, len(linhas)):
        P_loss[i] = (linhas[i, 3]) * (math.pow(abs(Sbr[i]) / abs(Vbus[int(linhas[i, 1])]), 2))
        Q_loss[i] = (linhas[i, 4]) * (math.pow(abs(Sbr[i]) / abs(Vbus[int(linhas[i, 1])]), 2))
    return P_loss, Q_loss


def voltage_stability_load_index(Vbus_i, Sbr_i, B, linhas):
    mv = np.zeros(len(B))

    for i in range(0, len(B)):
        for j in range(0, len(linhas)):
            if B[i, 0] == linhas[j, 2]:
                bus_up = int(linhas[j, 1])

                # mv[i] = 4*abs(Vbus_i[i])*abs(Vbus_i[bus_up]*math.cos( cmath.phase(Vbus_i[bus_up]) - cmath.phase(Vbus_i[i])) )

                mv[i] = (
                    4
                    * (abs(Vbus_i[bus_up]) * abs(Vbus_i[i]) - math.pow(abs(Vbus_i[i]), 2))
                    / math.pow(abs(Vbus_i[bus_up]), 2)
                )
                print(mv[i])

    return mv


# Entrada

#                           barra        P          Q
barras_sc = np.array(
    [
        [0, 0, 0],
        [1, 100, 60],
        [2, 90, 40],
        [3, 120, 80],
        [4, 60 - 1875, 30],
        [5, 60, 20],
        [6, 200, 100],
        [7, 200, 100],
        [8, 60, 20],
        [9, 60, 20],
        [10, 45, 30],
        [11, 60, 35],
        [12, 60, 35],
        [13, 120, 80],
        [14, 60 - 375, 10],
        [15, 60, 20],
        [16, 60, 20],
        [17, 90, 40],
        [18, 90, 40],
        [19, 90, 40],
        [20, 90, 40],
        [21, 90, 40],
        [22, 90, 50],
        [23, 420, 200],
        [24, 420, 200],
        [25, 60, 25],
        [26, 60, 25],
        [27, 60 - 750, 20],
        [28, 120, 70],
        [29, 200, 600],
        [30, 150, 70],
        [31, 210, 100],
        [32, 60, 40],
    ]
)


#                        linha  De    Para     R        X     Bsh    theta
linhas = np.array(
    [
        [0, 0, 1, 0.0922, 0.047, 0, 0],
        [1, 1, 2, 0.4930, 0.2511, 0, 0],
        [2, 2, 3, 0.3660, 0.1864, 0, 0],
        [3, 3, 4, 0.3811, 0.1941, 0, 0],
        [4, 4, 5, 0.8190, 0.7070, 0, 0],
        [5, 5, 6, 0.1872, 0.6188, 0, 0],
        [6, 6, 7, 0.7114, 0.2351, 0, 0],
        [7, 7, 8, 1.0300, 0.7400, 0, 0],
        [8, 8, 9, 1.0440, 0.7400, 0, 0],
        [9, 9, 10, 0.1966, 0.0650, 0, 0],
        [10, 10, 11, 0.3744, 0.1298, 0, 0],
        [11, 11, 12, 1.4680, 1.1550, 0, 0],
        [12, 12, 13, 0.5416, 0.7129, 0, 0],
        [13, 13, 14, 0.5910, 0.5260, 0, 0],
        [14, 14, 15, 0.7463, 0.5450, 0, 0],
        [15, 15, 16, 1.2890, 1.7210, 0, 0],
        [16, 16, 17, 0.7230, 0.5740, 0, 0],
        [17, 1, 18, 0.1640, 0.1565, 0, 0],
        [18, 18, 19, 1.5042, 1.3554, 0, 0],
        [19, 19, 20, 0.4095, 0.4784, 0, 0],
        [20, 20, 21, 0.7089, 0.9337, 0, 0],
        [21, 2, 22, 0.4512, 0.3083, 0, 0],
        [22, 22, 23, 0.8980, 0.7091, 0, 0],
        [23, 23, 24, 0.8960, 0.7011, 0, 0],
        [24, 5, 25, 0.2030, 0.1034, 0, 0],
        [25, 25, 26, 0.2842, 0.1447, 0, 0],
        [26, 26, 27, 1.0590, 0.9337, 0, 0],
        [27, 27, 28, 0.8042, 0.7006, 0, 0],
        [28, 28, 29, 0.5075, 0.2585, 0, 0],
        [29, 29, 30, 0.9744, 0.9630, 0, 0],
        [30, 30, 31, 0.3105, 0.3619, 0, 0],
        [31, 31, 32, 0.3410, 0.5302, 0, 0],
    ]
)


V_SE = fasor(12660, 0)
Vbus_old = V_SE * np.ones(len(barras_sc))
TOL = 0.001 * 12660
max_iter = 50
a0 = 0
a1 = 0.78
a2 = 0.22
b0 = 1
b1 = 0
b2 = 0

if __name__ == "__main__":
    inicio = time.time()

    [Vbus, Sbr, P_loss, Q_loss, iter, error] = sum_power(Vbus_old, TOL, max_iter, barras_sc, linhas)
    VSLI_sgd = voltage_stability_load_index(Vbus, Sbr, barras_sc, linhas)

    # Saída
    print("")
    print("Iterações necessárias para a convergência:", iter)

    tempo = time.time() - inicio
    print("Duração: %s" % tempo)

    print("")
    print("                     Tensões nas barras                           ")
    print("")
    print("Barra                             V[pu]")
    for i in range(0, len(barras_sc)):
        print(f"{abs(Vbus[i])/abs(V_SE):.3f}")

    print("")
    print("                     Potência ativa nos ramos                           ")
    print("")
    print("De  Para                             P[kW]")
    for i in range(0, len(linhas)):
        # print( int(linhas[i,1]),   int(linhas[i,2]),           f'{Sbr[i].real/1000: .3f}' )
        print(f"{Sbr[i].real/1000: .3f}")

    print("")
    print("                     Potência reativa nos ramos                           ")
    print("")
    print("De  Para                             Q[kvar]")
    for i in range(0, len(linhas)):
        print(int(linhas[i, 1]), int(linhas[i, 2]), f"{Sbr[i].imag/1000: .3f}")

    print("")
    print("                     Perdas nos ramos                           ")
    print("")
    print("De  Para                              [kW]")
    for i in range(0, len(linhas)):
        print(int(linhas[i, 1]), int(linhas[i, 2]), f"{P_loss[i]/1000: .3f}")

    sumloss = sum(P_loss / 1000)
    print("perdas totas", f"{sumloss: .3f}")

    print("")
    print("                     indive                           ")
    print("")
    print(VSLI_sgd)

    print("")
    print("                     phase                           ")
    print("")
    for i in range(0, len(Vbus)):
        print(cmath.phase(Vbus[i]))
