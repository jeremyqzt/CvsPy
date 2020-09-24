#include "sieve.h"
#include <stdio.h>

int main (int argc, char *argv[]) {
	int primes = sieve(10);
	printf("Primes: %d\n", primes);

}
