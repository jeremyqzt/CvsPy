#include <math.h>
#include <stdlib.h>

unsigned long sieve(long limit){
	unsigned long ret = 0;
	unsigned long computationalLimit = floor(sqrt(limit));
	unsigned char *prime = malloc(limit + 1);
	unsigned long i,j,k,l;

	for (i = 0; i < limit; i++){
		prime[i] = 1;
	}

	for (j = 2; j < computationalLimit; j++){
		if (prime[j] && j * j < limit){
			for (k = j * j; k <= limit; k += j){
				prime[k] = 0;
			}
		}
	}

	for (l = 0; l < limit; l++){
		ret += prime[l];
	}


	free(prime);
	//0, 1 are not primes
	return ret - 2;
}
