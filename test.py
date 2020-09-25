from sieve import *
from ctypes import *


testLimits = [10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]

sieveC = ctype.CDLL("sieve.so")

sieveC.sieve.argtypes = [ctypes.c_unsigned_long]

ret = sieveC.sieve(1000000000)

print(ret)