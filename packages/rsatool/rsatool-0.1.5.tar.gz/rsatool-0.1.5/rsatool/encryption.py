import math


def gen_keys(p, q, e):
    '''
    eng: This system function is needed for the correct operation of the module

    rus: Это системная функция нужна для корректной работы модуля

    :param p:
    :param q:
    :param e:
    :return :
    '''
    n = p * q
    f = (p - 1) * (q - 1)
    while math.gcd(e, f) != 1:
        e += 2
        if e > f:
            print("error")
    d = pow(e, -1, f)
    e = e
    return e, d, n
