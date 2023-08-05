import math
import random


class PrimeNumberTool:
    def __init__(self):
        pass

    @classmethod
    def BPSW(cls, n):
        '''
        eng: this function checks if a number is prime,this is a modern algorithm that almost does not find pseudoprimes

        rus: эта функция проверяет число на простору, это современный алгоритм который почти не находит псевдопростые числа
        :param n:
        :return bool:
        '''
        if n == 2:
            return True
        if not n & 1:
            return False
        d = n - 1
        while d & 1 == 0:
            d >>= 1
        for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(100):
                x = pow(x, 2, n)
                if x == 1:
                    return False
                if x == n - 1:
                    a = 0
                    break
            if a:
                return False
        return True

    @classmethod
    def factorization(cls, n):
        '''
        eng: this function factorizes a number

        rus: эта функция факторизует число
        :param n:
        :return first divisor:
        '''
        if n % 2 == 0:
            print(2)
        for i in range(3, math.isqrt(n) + 2, 2):
            if n % i == 0:
                return i

    @classmethod
    def find_prime_number(cls, n):
        '''
        eng: this function goes through spirals with which contain a significant percentage of prime numbers and finds the nearest prime number to the given

        rus: данная функция идёт по спиралям с которые содержат значительный процент простых чисел и находит ближайшее простое число к данному
        :param n:
        :return:
        '''
        n = n + (6 - n % 6)
        i = n
        while True:
            if cls.BPSW(i + 1):
                return i + 1
            elif cls.BPSW(i + 5):
                return i + 5
            i += 6
