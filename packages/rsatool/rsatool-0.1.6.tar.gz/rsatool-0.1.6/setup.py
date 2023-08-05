from setuptools import setup


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='rsatool',
    version='0.1.6',
    description='Module for fast calculating large primes, and RSA encryption and decryption of data of any size',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Nikita Grigorev',
    author_email='nekitbilding@inbox.ru',
    url='https://github.com/mrNikGrig/RSA_tool.git',
    packages=['rsatool']
)
