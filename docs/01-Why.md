# A unorthodox way to massively program execution speed

Imagine this - we wrote the same program, both have similar lines of code but one has a hundredth (!!!) the execution time. This sounds impossible. Well I'm here to say its not and we'll explore it more in this article.

## Disclaimer

I am writing this based on my perceived understanding of the subjects - It is possible (and likely) that I have gaps in my understanding and everything I write may not be 100% correct.

I will refer to `Python` and `C` alot in this article. I have some experience with both as I currently work with Python and have, in the past, worked with C for writing custom Linux distros. Again - my knowledge here isn't perfect pros/cons I speak of will only reflect my experiences.

Apologies in advance to the reader!

## My take on programming language evolution

I cheated a little bit when I wrote the introduction - writing the same program with similar line counts doesn't mean we used the same developments tools. For the rest of the article, I will make a comparison between C and Python to show the advantages and disadvantages of each and explain how we can get massive speedups in execution time. At a later time, I will write a part 2 - to explore how we can integrate this into a niche area of our code.

I'm sure we're all aware the differences between compiled and interpreted but in case we forgot:

- A compiled language must be translated into a binary of machine code before it can be ran

- A interpreted language can be compiled 'Just-In-Time' for it to be ran, eliminating the compilation step

Before programming languages became (somewhat) standardized, each hardware target had its unique way to program and run. This, naturally, was difficult to work with and the advent of the `C` language, the motto of [write once, compile anywhere](https://en.wikipedia.org/wiki/Write_once,_compile_anywhere) became the dominate way to appraoch programming.

As software and hardware both became more complex, compilers (especially cross-compilers) diverged and it became extremely difficult to maintain the `compile anywhere` part of the motto. As programmers - we needed a solution and quickly came to the reliable concept of `abstraction`. The compile process was abstracted and we got the motto of [write once, run anywhere](https://en.wikipedia.org/wiki/Write_once,_run_anywhere) - this gave rise to `Java`.

`Java` still maintained the compile process but instead of machine code, the target was `Byte Code` which was interpreted by a `Java Virtual Machine (JVM)`. Java was (and still is) a very popular programming language but it has its fair share of [criticisms](https://en.wikipedia.org/wiki/Criticism_of_Java).

We eventually took the `write once, run anywhere` further and arrived at many languages that fit the motto much better - a prime example is Python! While `C` and `Java` still dominate the industry, Python is quickly rising and is now a close third on the [TIOBE Index](https://www.tiobe.com/tiobe-index/).

Python is a fully interpreted language - the interpreter takes care of all translations and, for the most part, it delivers on the `write once and run anywhere` promise.

## The speed tradeoff

As programming languages evolved, so too has the debugging tools and paradigms. Newer paradigms allows us to abstract complex models while newer and more powerful tools allows for deeper inspection into the state of a executing program. This, undoubtedly, improved development speed and the developer experience - but this gain isn't free, it is bundled with a rather significant performance penalty.

[Here are some benchmarks for the curious.](https://benchmarksgame-team.pages.debian.net/benchmarksgame/fastest/python3-gcc.html).

One of such examples is the `Global Interpreter Lock (GIL)` that is commonly seen in python implementations. This lock holds a `mutex` over the interpreter and is a [design decision](https://wiki.python.org/moin/GlobalInterpreterLock) that helped to abstract away race conditions. We can write a simple application to illustrate this. Consider the following program that counts down from five million.

```
from time import time
maxCount = 50000000

def  count(amt):
	while amt:
		amt-=1

start = time()
count(maxCount)
end = time()
```

I can run this on my computer and get a execution time - in my case it was ~4.5 seconds.

```
How long (Non-Threaded): 4.409004
```

We can write a threaded version of the same program where we distribute the workload across 4 threads.

```
from time import time
from threading import Thread
ThCount = 4
maxCount = 50000000

class  ThreaderCounter(Thread):
	def  __init__(self, count):
		Thread.__init__(self)
		self.count = count

	def  run(self):
		while  self.count:
			self.count-=1

thStart = time()
threadArr = []
for i in  range(0,ThCount - 1):
	th = ThreaderCounter(round(maxCount/ThCount))
	th.start()
	threadArr.append(th)
for item in threadArr:
	item.join()
thEnd = time()
print("How long (Threaded): %f" % (thEnd-thStart))
```

Convention would tell us that the program should execute 4 times faster - with some overhead to starting the threads but this isn't the case and the program takes almost 5.4 seconds to run.

```
How long (Threaded): 5.388963
```

There is some random-ness to scheduling. I tried to minimize this by using a `RT-linux kernel` and both processes have a `nice` value of `20`.

## How to cheat and overcome the speed barrier

Python provides a native way to link against `.so` from its `Ctypes` library, these are named `Dynamically Linked Libraries(DLLs)` and are free from the GIL. Multiprocessing in python is quite reliant of this behavior as a DLL can launch its own threads and leverage the performance gains.

For interests sake, I've prepared a sample problem where we can explore this. There is a simple algorithm for finding prime numbers called the [Sieve of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes). I will implement the sieve in `C` using `openMP` for multiprocessing and also implement the same algorithm in Python and we can compare the difference. The code is in the appendix if there is any interest around it.

## Appendix

C implementation of the Sieve and its accompannying `Makefile`.

```
#include  <math.h>
#include  <stdlib.h>

unsigned  long  sieve(long  limit){
	unsigned  long ret = 0;
	unsigned  long computationalLimit = floor(sqrt(limit));
	unsigned  char *prime = malloc(limit + 1);
	unsigned  long i,j,k,l;

	#pragma  omp  parallel  for
	for (i = 0; i < limit; i++){
		prime[i] = 1;
		}
		for (j = 2; j < computationalLimit; j++){
			if (prime[j] && j * j < limit){
			#pragma  omp  parallel  for
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
```

```
CC=gcc
CFLAGS= -Wall -g -O3 -fPIC -shared -std=c99
CFLAGS_EXE= -Wall -g -O3 -lm -std=c99
OMP_FALGS= -fopenmp -lgomp -lomp
OBJ = sieve.o
TARGET=main
TARGET_LIB=libsieve.so

%.o: %.c
	$(CC) -c -o $@  $<  $(CFLAGS)  $(OMP_FALGS)

$(TARGET_LIB): $(OBJ)
	$(LINK.c)  $(CFLAGS)  $(OMP_FALGS)  $^ -o $@

$(TARGET): $(OBJ) main.o
	$(CC) -o $@  $^  $(CFLAGS_EXE)  $(OMP_FALGS)

all: $(TARGET)  $(TARGET_LIB)

clean:
	rm -rf *.o *.so sieve

.PHONY: all clean
```

Python code to call the DLL

```
from ctypes import CDLL, c_ulong
from os import getcwd
import time

def  sieve(limit):
	primes = [True  for i in  range(limit)]
		for i in  range(2, math.floor(math.sqrt(limit))):
			if (primes[i] and i * i < limit):
				for k in  range(i*i, limit, i):
					primes[k] = False
		ret = 0
		for val in primes:
		ret += 1  if val else  0
	return ret - 2

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
```
