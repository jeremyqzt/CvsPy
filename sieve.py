import sys
import math

def sieve(limit):
	primes = [True for i in range(limit)]
	for i in range(2, math.floor(math.sqrt(limit))):
		if (primes[i] and i * i < limit):
			for k in range(i*i, limit, i):
				primes[k] = False

	ret = 0
	for val in primes:
		ret += 1 if val else 0

	return ret - 2

if __name__ == "__main__":
	primeTo = int(sys.argv[1])
	ret = sieve(primeTo)
	print("Number of Primes from 0 to %d is %d" % (primeTo, ret))