import numpy.random
import RSA_tool as my_RSA


def test():
    m = numpy.random.randint(13, 1000, 20)
    isNorm = True
    for i in m:
        i = int(i)
        e, d, n = my_RSA.RSA.get_bit_keys(256)
        if (pow(pow(i, e, n), d, n)) != i:
            print("error")
            isNorm = False
            break
    if isNorm:
        print("eee i feel good")


def test_calculating_keys():
    e, d, n = my_RSA.RSA.get_bit_keys(1024)
    m = 'hello world'
    print(n)
    c = my_RSA.RSA.block_encrypt(m, e, n)
    print(c)
    m = my_RSA.RSA.block_decrypt(c, d, n)
    print(m)

def main():
    test_calculating_keys()



if __name__ == '__main__':
    main()
