#include "sieve.h"
#include <stdio.h>
#include <stdlib.h>

int main (int argc, char *argv[]) {

	unsigned long primes = 1000000;
	if (argc == 2){
		primes = atoi(argv[1]);
	}

	unsigned long numPrimes = sieve(primes);
	printf("Number of primes from : %lu is %lu\n", primes, numPrimes);

}
