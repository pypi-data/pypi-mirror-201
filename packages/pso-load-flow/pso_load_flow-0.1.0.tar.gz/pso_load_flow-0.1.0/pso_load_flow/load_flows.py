#!/usr/bin/env python


import cmath
import math
import os
import random
import time

import numpy as np

inicio = time.time()


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
                    barras[i, 2], barras[i, 3], abs(Vbus[i]), abs(V_SE), a0, a1, a2, b0, b1, b2
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


def sum_power(Vbus_old, TOL, max_iter, barras_sc, linhas):
    barras = organiza_camada(barras_sc, linhas)
    Sbr = forward_sweep(barras, linhas, Vbus_old)
    Vbus = backward_sweep(V_SE, barras, linhas, Sbr)
    error = max(abs(abs(Vbus) - abs(Vbus_old)))
    iter = 0
    # print('                    Processamento                       ')
    # print('                                                        ')
    # print('Tolerância admitida:', TOL)
    # print('')
    # print('iteração           erro')
    # print(iter,                 error)
    while error >= TOL:
        Vbus_old = Vbus
        Sbr = forward_sweep(barras, linhas, Vbus_old)
        Vbus = backward_sweep(V_SE, barras, linhas, Sbr)
        error = max(abs(abs(Vbus) - abs(Vbus_old)))
        iter = iter + 1
        # print(iter,                 error)

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

    barras_new[0, 1] = 0  # Definição da barra de referencia

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


def escolhas_aleatorias(barras_sc, gd):
    d = np.shape(barras_sc)

    nova = np.zeros(d)
    nova[:, 0] = barras_sc[:, 0]
    nova[:, 1] = barras_sc[:, 1]
    nova[:, 2] = barras_sc[:, 2]

    opcoes = nova[:, 0]  # Eliminando a barra 0 das escolhas
    opcoes = np.delete(opcoes, (0), axis=0)
    # for i in range(1,len(nova[:,0])):
    #    opcoes[i] = nova[i,0]

    b = random.sample(list(opcoes), k=3)

    for j in range(0, len(b)):
        for k in range(1, len(nova[:, 0])):
            if b[j] == nova[k, 0]:
                nova[k, 1] = barras_sc[k, 1] - gd[j]

    return b, nova


def teste_de_restricoes(Vbus_i, Sbr, Sbr_i, sumloss, sumloss_i, b, gd):
    viavel = np.zeros(5)

    # teste das perdas
    if sumloss < sumloss_i:
        viavel[0] = 1

    # teste da sobretensao
    if max(abs(Vbus_i)) / 12660 > 1.05:
        viavel[1] = 1

    # teste da subtensao
    if min(abs(Vbus_i)) / 12660 < 0.93:
        viavel[2] = 1

    # teste do fluxo reverso
    if Sbr_i[0].real < 0:
        viavel[3] = 1

    # teste da sobrecarga
    # if ( max( abs(Sbr_i.real) / (abs(Sbr.real))) > 1.1):
    #    viavel[4] = 1

    # viavel[4] = 0
    for i in range(0, len(Sbr)):
        if (abs(Sbr_i.real[i]) / (abs(Sbr.real[i]))) > 1.1:
            viavel[4] = 1
            break

    return viavel


def real_power_loss_index(sumloss, sumloss_i):
    RPLI = 1 - (sumloss_i / sumloss)
    return RPLI


def reactive_power_loss_index(sum_q_loss, sum_q_loss_i):
    QPLI = 1 - (sum_q_loss_i / sum_q_loss)
    return QPLI


def voltage_regulation_index(Vbus, Vbus_min):
    VRI = 1 - max(abs(((Vbus_min) - (Vbus)) / (Vbus_min)))
    return VRI


def voltage_stability_load_index(Vbus_i, Sbr_i, B, linhas):
    mv = np.zeros(len(B) - 1)

    for i in range(1, len(B) - 1):
        for j in range(0, len(linhas)):
            if B[i, 0] == linhas[j, 2]:
                bus_up = int(linhas[j, 1])

                mv[i] = (
                    4
                    * (abs(Vbus_i[bus_up]) * abs(Vbus_i[i]) - math.pow(abs(Vbus_i[i]), 2))
                    / math.pow(abs(Vbus_i[bus_up]), 2)
                )
                # print(mv[i])

    VLSI = max(mv)

    return VLSI


def New_Voltage_Stability_Index(linhas, Vbus, Sbr):
    [P_loss, Q_loss] = perdas(linhas, Vbus, Sbr)
    Pr = Sbr.real - P_loss
    Qr = Sbr.imag - Q_loss
    NVSI_s = [0] * len(linhas)

    for i in range(1, len(linhas) - 1):
        bus_down = int(linhas[i, 2])
        NVSI_s[i] = (
            2
            * linhas[i, 4]
            * math.sqrt(math.pow(Pr[i], 2) + math.pow(Qr[i], 2))
            / (2 * Qr[i] * linhas[i, 4] - math.pow(Vbus[bus_down], 2))
        )

    NVSI = max(NVSI_s)

    return NVSI


def Novel_Line_Stability_Index(linhas, Vbus, Sbr):
    [P_loss, Q_loss] = perdas(linhas, Vbus, Sbr)
    Pr = Sbr.real - P_loss
    Qr = Sbr.imag - Q_loss
    NLSI_s = [0] * len(linhas)

    for i in range(0, len(linhas) - 1):
        bus_up = int(linhas[i, 1])
        NLSI_s[i] = (Pr[i] * linhas[i, 3] + Qr[i] * linhas[i, 4]) / (
            0.25 * math.pow(Vbus[bus_up], 2)
        )

    NLSI = max(NLSI_s)

    return NLSI


def fluxo_carga_leve_com_gd(Vbus_old, TOL, max_iter, B, linhas, gd):
    # Carga minima
    Bmin = np.zeros((len(B), 3))
    Bmin[:, 0] = B[:, 0]
    Bmin[:, 1] = 0.1 * B[:, 1]
    Bmin[:, 2] = 0.1 * B[:, 2]
    [Vbus_min, Sbr_min, P_loss_min, Q_loss_min, iter_min, error_min] = sum_power(
        Vbus_old, TOL, max_iter, Bmin, linhas
    )
    return Vbus_min, Sbr_min, P_loss_min, Q_loss_min, iter_min, error_min


def execucao(Vbus_old, TOL, max_iter, B, linhas, gd):
    k = 0  # Contador de possibilidades
    l = 0  # Contador de rejeição para carga leve
    p = 0  # Contador de rejeição para carga pesada

    # Escolha da gd
    n = math.perm(len(B) - 1, len(gd))  # Numero de configurações possíveis
    lista = np.zeros((1, 9))
    row_to_be_added = np.zeros(9)

    # Carga maxima sem GD
    [Vbus, Sbr, P_loss, Q_loss, iter, error] = sum_power(Vbus_old, TOL, max_iter, B, linhas)
    sumloss = sum(P_loss / 1000)
    sum_q_loss = sum(Q_loss / 1000)
    VSLI_sgd = voltage_stability_load_index(Vbus, Sbr, B, linhas)

    # Contador de rejeições
    rejeicao_leve = np.zeros(5)
    rejeicao_pesada = np.zeros(5)

    while k < n:
        # Escolha aleatoria de barras
        [b, x] = escolhas_aleatorias(B, gd)

        # Fluxo de potência em carga leve com GD
        [Vbus_min, Sbr_min, P_loss_min, Q_loss_min, iter_min, error_min] = fluxo_carga_leve_com_gd(
            Vbus_old, TOL, max_iter, x, linhas, gd
        )
        sumloss_min = sum(P_loss / 1000)
        sum_q_loss_min = sum(Q_loss / 1000)

        # Teste de restrições para a carga leve
        viavel_leve = teste_de_restricoes(Vbus_min, Sbr, Sbr_min, sumloss, sumloss_min, b, gd)
        rejeicao_leve = rejeicao_leve + viavel_leve
        if max(viavel_leve) == 0:
            # Fluxo de potência para carga pesada com GD
            [Vbus_i, Sbr_i, Ploss_i, Qloss_i, iter_i, error_i] = sum_power(
                Vbus_old, TOL, max_iter, x, linhas
            )
            sumloss_i = sum(Ploss_i / 1000)
            sum_q_loss_i = sum(Qloss_i / 1000)
            # Teste de restrições para a carga pesada
            viavel_pesada = teste_de_restricoes(Vbus_i, Sbr, Sbr_i, sumloss, sumloss_i, b, gd)
            rejeicao_pesada = rejeicao_pesada + viavel_pesada
            if max(viavel_pesada) != 0:
                p = p + 1
            else:
                RPLI = real_power_loss_index(sumloss, sumloss_i)
                QPLI = reactive_power_loss_index(sum_q_loss, sum_q_loss_i)
                VRI = voltage_regulation_index(Vbus_i, Vbus_min)
                VSLI = voltage_stability_load_index(Vbus_i, Sbr_i, B, linhas)
                # NVSI = New_Voltage_Stability_Index(linhas, Vbus_min, Sbr_min)

                # pesos
                w1 = 0.35
                w2 = 0.15
                w3 = 0.15
                w4 = 0.35

                row_to_be_added[0] = k
                row_to_be_added[1] = b[0]
                row_to_be_added[2] = b[1]
                row_to_be_added[3] = b[2]
                row_to_be_added[4] = RPLI
                row_to_be_added[5] = QPLI
                row_to_be_added[6] = VRI
                row_to_be_added[7] = VSLI
                row_to_be_added[8] = w1 * RPLI + w2 * QPLI + w3 * VRI + w4 * VSLI

                lista = np.vstack((lista, row_to_be_added))

        else:
            l = l + 1

        k = k + 1

    [bus1, bus2, bus3, maior] = det_melhores_barras(lista)
    # return l,p
    return lista, bus1, bus2, bus3, maior, rejeicao_leve, rejeicao_pesada, l, p


def det_melhores_barras(lista):
    # for i in range(0,len(lista[:,7])):
    #    if lista[i,7] != 0:
    #        print('diferente de 0')

    posicao = 0
    maior = lista[0, 8]
    for i in range(0, len(lista) - 1):
        if lista[i + 1, 8] > lista[i, 8]:
            maior = lista[i + 1, 8]
            posicao = i + 1

    bus1 = lista[posicao, 1]
    bus2 = lista[posicao, 2]
    bus3 = lista[posicao, 3]
    return bus1, bus2, bus3, maior


def convert(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))


# Entrada

#                           barra        P          Q
B = np.array(
    [
        [0, 0, 0],
        [1, 100, 60],
        [2, 90, 40],
        [3, 120, 80],
        [4, 60, 30],
        [5, 60, 20],
        [6, 200, 100],
        [7, 200, 100],
        [8, 60, 20],
        [9, 60, 20],
        [10, 45, 30],
        [11, 60, 35],
        [12, 60, 35],
        [13, 120, 80],
        [14, 60, 10],
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
        [27, 60, 20],
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
Vbus_old = V_SE * np.ones(len(B))
TOL = 0.001 * 12660
max_iter = 50

# modelo ZIP de carga
a0 = 0
a1 = 0.78
a2 = 0.22
b0 = 0
b1 = 0
b2 = 1

gd = [375, 750, 1875]

# processamento


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print("Aguarde o processamento...")
    [lista, bus1, bus2, bus3, maior, rejeicao_leve, rejeicao_pesada, l, p] = execucao(
        Vbus_old, TOL, max_iter, B, linhas, gd
    )
    # [l, p] = execucao(Vbus_old, TOL, max_iter, B, linhas, gd)

    Ins = 100 * sum(gd) / math.sqrt((math.pow(sum(B[:, 1]), 2) + math.pow(sum(B[:, 2]), 2)))

    # saida

    print("")
    print(f"Inserção de GFV =  {Ins: .2f} %")
    print("")
    print("Barras selecionadas:")
    print(" %d   com inserção de  375 kW" % bus1)
    print(" %d   com inserção de   75 kW" % bus2)
    print(" %d   com inserção de 1875 kW" % bus3)
    print("")

    print("")
    print("Total de rejeições para a carga leve:  %d" % l)
    print("Total de rejeições para a carga pesada:  %d" % p)

    print("")
    print("Rejeição durante a carga leve")
    print("Rejeição por perdas = %d " % rejeicao_leve[0])
    print("Rejeição por sobretensao = %d" % rejeicao_leve[1])
    print("Rejeição por subtensao = %d" % rejeicao_leve[2])
    print("Rejeição por fluxo reverso = %d" % rejeicao_leve[3])
    print("Rejeição por sobre carga = %d" % rejeicao_leve[4])
    print("")

    print("")
    print("Rejeição durante a carga pesada")
    print("Rejeição por perdas = %d " % rejeicao_pesada[0])
    print("Rejeição por sobretensao = %d" % rejeicao_pesada[1])
    print("Rejeição por subtensao = %d" % rejeicao_pesada[2])
    print("Rejeição por fluxo reverso = %d" % rejeicao_pesada[3])
    print("Rejeição por sobre carga = %d" % rejeicao_pesada[4])
    print("")

    print("")
    # print("Do total de %d possibilidades, %d foram rejeitadas na carga leve e %d foram rejeitadas na crga pesada" %n %l %p)

    tempo = time.time() - inicio
    ts = convert(tempo)
    print("")
    # print(f'Tempo de simulação = {tempo: .2f} s')
    print("Tempo de simulação : ")
    print(convert(tempo))
