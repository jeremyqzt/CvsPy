from sieve import *
from ctypes import CDLL, c_ulong
from os import getcwd
import time

testLimits = [1000, 10000, 100000, 1000000, 10000000, 30000000, 50000000, 70000000,100000000, 300000000,500000000,1000000000, 2000000000]

soPath = getcwd() + "/libsieve.so"
sieveC = CDLL(soPath)
# Warmup
sieveC.sieve(10)

for item in testLimits:
	t0 = time.time()
	sieveC.sieve(item)
	t1 = time.time()
	totalC = t1-t0
	t0 = time.time()
	sieve(item)
	t1 = time.time()
	totalP = t1-t0
	print("C time: %f, Python time: %f, for primes from 0 to %d (Speedup = %f)" % (totalC, totalP, item, totalP/totalC))
