import time
import __main__
from __main__ import *
import matplotlib.pyplot as plt
import numpy as np


class NitrogenOxide:
    def __init__(self):
        ...


class NitrogenFromGas(NitrogenOxide):
    """
    расчет выбросов оксидов азота при сжигании природного газа

    M = Bp*Q*K*bk*bt*ba*(1-br)*(1-bj)*kn
    Bp - расчетный расход топлива, нм^3/c, Bp = B с достаточно большой точностью
    Q - низшая теплота сгорания топлива, МДж/нм^3
    K - удельный выброс оксидов азота при сжигании газа, г/МДж
    bk - коэфицент, учитывающий конструкцию горелки
    bt - коэфицент , учитывающий температуру воздуха, подаваемого для горелки
    ba - коэффицент, учитывающий влияние избытка воздуха на образование оксидов азота
    br - безразмерный коэффицент, учитывающий влияние рециркуляции дымовых газов через
     горелки на образование оксидов азота
    bj - безразмерный коэффицент, учитывающий ступенчатый ввод воздуха в топочную камеру
        kn - коэффицент пересчета результата, kn = 1 г/с, kn = 10 ** (-3) тн/г
    """

    def emissions_calculation(self, B, Q, constr, D, typefire, t, r, j, kn=1):
        """
        B - расчетный расход топлива тыс.нм^3/год или же фактический расход топлива на котел
        Q - низшая теплота сгорания топлива, МДж/нм^3
        constr: air - для паровых, water - для водогрейных
        D - фактическая паропроизводительность котла т/ч - вводится только для паровых котлов
        typefire - тип горелки: напорный тип - air, инжекционный - injection, двухступенчатый - twosteps
        t - температура воздуха подаваемого для горения
        r - степень рециркуляции дымовых газов, %
        j - доля воздуха, подаваемого в промежуточную зону факела, в процентах от обещего количества
        организованного воздуха
        kn - коэффицент пересчета результата, kn = 1 г/с, kn = 10 ** (-3) тн/г
        """
        Bp = B
        if constr == 'steam':
            K = 0.01*(D**0.5) + 0.03
        else:
            Qt = Bp*Q
            K = 0.0113*(Qt**0.5) + 0.03
        choice_bk = {'air': 1, 'injection': 1.6, 'twosteps': 0.7}
        bk = choice_bk[typefire]
        bt = 1 + 0.002*(t - 30)
        # для повышения точности можно улучшить расчеты ba
        ba = 1.225
        br = 0.16*(r**0.5)
        bj = 0.022 * j
        M = Bp*Q*K*bk*bt*ba*(1-br)*(1-bj)*kn
        return M


class SulfurOxides:
    """
    расчет выбросов оксидов серы

    M = 0.02*B*S*(1-n1)*(1-n2)
    """

    def emissions_calculation(self, B, typefuel, typeash, ishydrogen, S, H2):
        """
        B - расчетный расход топлива тыс.нм^3/год или же фактический расход топлива на котел
        typefuel - тип топлива
        typeash - 1 - сухой золоуловитель
                - 2 - мокрый - пока не реализован
        ishydrogen - есть ли в топливе сереводород
        S - содержание серы в топливе на рабочую массу, %
        H2 - содержиание на рабочую массу сероводорода в топливе, %
        """
        # список можно расширять
        fuels = {'gas': 0, 'fueloil': 0.02, 'peat': 0.15}
        n1 = fuels[typefuel]
        n2 = 0
        if typeash == 1:
            n2 = 0
        if ishydrogen:
            S += 0.94*H2
        M = 0.02*B*S*(1-n1)*(1-n2)
        return M

class CarbonMonoxide:
    """
    расчет выбросов оксидов углерода

    C - выход оксида углерода при сжигании топлива г/кг
    M = 10^(-3)*B*C*(1 - q4/100)
    """

    def emissions_calculation(self, B, q3, typefuel, Q, q4):
        """
        B - расчетный расход топлива тыс.нм^3/год или же фактический расход топлива на котел
        q3 - процент тепла вследствии неполноты сгорания топлива, %
        typefuel - тип топлива
        Q - низшая теплота сгорания топлива, МДж/нм^3
        q4 - потери тепла вследствие механической неполноты сгорания топлива, %
        """
        fuels = {'gas': 0.5, 'fueloil': 0.65, 'solidfuel': 1}
        R = fuels[typefuel]
        C = q3*R*Q
        M = 10**(-3)*B*C*(1-q4/100)
        return M


class Calculate:

    def emissions_calculation(self, name, NO2, SO2, CO2):
        x = NitrogenFromGas()
        y = CarbonMonoxide()

        a = 0
        b = 0
        k = 0

        l1 = []
        l2 = []


        with open(name) as file:
            for t in file:
                t = t.rstrip()
                temp = x.emissions_calculation(1000, 31.8, 'steam', 274.1, 'air', float(t), 0, 0)
                a += temp
                l1.append(temp)
                temp = y.emissions_calculation(1000, 10, 'gas', 31.8, 0)
                b += temp
                l2.append(temp)
                k += 1

                #print(a, b)
                # time.sleep(1)

                # SulfurOxides для нашего случая не расчитывается, так как серы нет
        a /= k
        b /= k

        k = 0

        times = []
        while k < len(l1):
            times.insert(k + 1, k)
            k += 1

        flag = False
        if NO2:
            plt.plot(times, l1)
            flag = True
            print("PLOT 1")
        if CO2:
            plt.plot(times, l2)
            flag = True
            print("PLOT 2")
        if SO2:
            plt.plot(times, l1)
            flag = True
            print("PLOT 3")
        if not flag:
            plt.plot(0, 0)
            print("PLOT 4")

        plt.xlabel('Время')
        plt.ylabel('Кол-во выбросов')

        plt.savefig('images.png')
        plt.close()

        return [a, b]



if __name__ == '__main__':
    x = NitrogenFromGas()
    y = CarbonMonoxide()
    with open('data') as file:
        for t in file:
            t = t.rstrip()
            a = x.emissions_calculation(1000, 31.8, 'steam', 274.1, 'air', float(t), 0, 0)
            b = y.emissions_calculation(1000, 10, 'gas', 31.8, 0)
            print(a, b)
            time.sleep(1)
            # SulfurOxides для нашего случая не расчитывается, так как серы нет

