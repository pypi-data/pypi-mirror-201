from .prime_numbers import *
from .encryption import *
import random


class RSA:
    def __init__(self):
        pass

    @classmethod
    def get_bit_keys(cls, col_bits, e=65577):
        '''
        eng:this function generates keys for RSA encryption

        rus:данная функция генерирует ключи для шифрования RSA
        :param col_bits - eng: enter the size of the desired keys
        rus: введите размер желаемых ключей:
        :param e - eng: this is the public key, it is recommended to leave it like this
        rus: это открытый ключ рекомендуется его так оставить:
        :return eng: public key, private key, module
        rus: публичный ключ, приватный ключ, модуль:
        '''
        p = PrimeNumberTool.find_prime_number(random.randint(2 ** (col_bits // 2), 2 ** ((col_bits // 2) + 1)))
        q = PrimeNumberTool.find_prime_number(random.randint(2 ** (col_bits // 2) - 1, 2 ** (col_bits // 2)))
        return gen_keys(p, q, e)


    @classmethod
    def block_decrypt(cls, c, d, n):
        '''
        eng: this function effectively decrypt any amount of information
        rus: данная функция эффективно расшифровывает любое количество информации
        :param c - encrypted message/ зашифрованное сообщение:
        :param d - private key / закрытый ключь:
        :param n - module/ модуль:
        :return decrypted message/расшифрованное сообщение:
        '''
        for i in range(len(c)):
            c[i] = pow(int(c[i]), d, n)
        s = ''
        for i in c:
            tmp = str(i)[1:]
            for j in range(0, len(tmp), 4):
                s += chr(int((tmp[j] + tmp[j + 1] + tmp[j + 2] + tmp[j + 3])))
        return s

    @classmethod
    def block_encrypt(cls, m, e, n):
        '''
        eng: this function effectively encrypts any amount of information
        rus: данная функция эффективно шифрует любое количество информации
        :param m - message/сообщение:
        :param e - public key/публичный ключ:
        :param n - module/ модуль:
        :return encrypted message/зашифрованное сообщение:
        '''
        max_len_block = len(str(n)) - 2
        block = ''
        arr_blocks = []
        for i in m:
            str_i = str(ord(i))
            while len(str_i) < 4:
                str_i = '0' + str_i
            if len(block + str_i) <= max_len_block:
                block += str_i
            else:
                arr_blocks.append('1' + block)
                block = str_i
        arr_blocks.append('1' + block)
        for i in range(len(arr_blocks)):
            arr_blocks[i] = pow(int(arr_blocks[i]), e, n)
        return arr_blocks
