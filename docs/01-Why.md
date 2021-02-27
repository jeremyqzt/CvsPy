# The Speed Tradeoff

Imagine 2 sets of source code - both are similar in functionality, line count, and complexity but one has a 100x speedup over the other. This sounds pretty good right? If you would like to see how, read on!

## Motivation and Disclaimer

Most of what I write here is largely based on my experience. I have always craved lower level but have always preferred to work on the high level and thought this article would be a good bridge between the two.

Since I am writing this based on my perceived understanding of the subjects - It is possible (and likely) that I have gaps in my understanding and everything I write may not be 100% correct.

Apologies in advance to the reader!

## Introduction

I definintely cheated a little bit when I wrote the heading - writing the same program with similar line counts/complexity doesn't mean we used the same developments tools. For this article, I will make a comparison between `C` and `Python` to show the advantages and disadvantages of each and explain how we can get massive speedups in execution time. At a later time, I hope to write a part 2 - to explore how we can integrate this into a niche area of our code.

## My take on programming language evolution

Before programming languages became (somewhat) standardized, each hardware target had its unique way to develop and run applications. CPUs supported their own instruction sets and everything was a mess! This, naturally, was difficult to work with.

We first had assembly and later came the advent of the `C` language, the motto of [write once, compile anywhere](https://en.wikipedia.org/wiki/Write_once,_compile_anywhere) became the dominate way to appraoch programming.

As software and hardware both became more complex, compilers (especially cross-compilers) diverged and it became extremely difficult to maintain the `compile anywhere` part of the motto. As programmers - we needed a solution and quickly came to the reliable concept of `abstraction`. The compile process was abstracted and we got the motto of [write once, run anywhere](https://en.wikipedia.org/wiki/Write_once,_run_anywhere) - this gave rise to `Java`.

`Java` still maintained the compile process but instead of machine code, the target was `Byte Code` which was interpreted by a `Java Virtual Machine (JVM)`. Java was (and still is) a very popular programming language but it has its fair share of [criticisms](https://en.wikipedia.org/wiki/Criticism_of_Java).

We eventually took the `write once, run anywhere` further and arrived at many languages that fit the motto much better - a prime example is Python! While `C` and `Java` still dominate the industry, Python is quickly rising and is now a close third on the [TIOBE Index](https://www.tiobe.com/tiobe-index/).

Python is a fully interpreted language - the interpreter takes care of all translations and, for the most part, it delivers on the `write once and run anywhere` promise.

## The speed tradeoff

As programming languages evolved, so too has the debugging tools and modelling paradigms.

Newer paradigms allows us to imagine programs in a intuitive sense and the task became modelling the world rather than issuing sequential commands to a machine. I would say one of the results from this evolution is [Object-Oriented Programming](https://en.wikipedia.org/wiki/Object-oriented_programming). This format of programming lets us model the world as individual objects and allows use to think about `what a object can do` rather than `what the code must do`. This is great because programmers can do less mental gymnastics to get the end result they're after (With less bugs too). Concurrently, the tooling for programmers have also become more and more powerful - The goal for any tool is to give a full snapshot of the program's inner state. This can tell the debugger exactly what has gone wrong. For the most part, this has been accomplished, we have the likes of `gdb` and `breakpoints` that can pause execution and give us exactly what we're looking for.

All these features are really nice but they require additional overhead but they are not handled without cost. Below are 3 examples of where potential overhead can arise:

1.  To inspect the current state of a variable, it either must be in a CPU register or it must be fetched from memory and loaded into a register for the programmer to inspect it. Doing this may seem common place but these operations are actually very expensive and doing this `was` absolutely unfeasible until very recently - due to significant advancements in hardware.
2.  To raise and catch exceptions. In a typical implementation, whenever a runtime occurs, the OS will send a `SIGTERM` to the application instructing shutdown but this behavior is not captured by the program and is instead handled by the runtime which means an abstraction layer must exist and this is akin to running 2 applications at once.
3.  To support weak typing - Strong typing exists to manage memory blocks and to have predictability when loading variables into CPU registers a weakly typed language must prepare the variables before trying to store it in memory or loading it into a CPU register.

What a high-level language gains in is ability to abstract, it looses the same amount in speed.

[Here are some benchmarks for the curious.](https://benchmarksgame-team.pages.debian.net/benchmarksgame/fastest/python3-gcc.html).

## An example of the tradeoff

A prominent example of the speed tradeoff is the `Global Interpreter Lock (GIL)` that is commonly seen in python implementations (i.e. `Cpython`).

THe purpose of this lock is to hold a mutually exclusive (mutex) lock over the python intepreter and is a active [design decision](https://wiki.python.org/moin/GlobalInterpreterLock). This has undoubtadly helped the language to be as user-friendly as it is but is definitely a important `implementation note`.

We can write a simple application to illustrate this. Consider the following program that counts down from five million.

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

There is some random-ness to scheduling. I tried to minimize this by using a `RT-linux kernel` and both processes have a `nice` value of `19` (19 is the maximum). Below are some of the information aboiut my system setup.

```
// uname -r
4.9.0-8-rt-amd64

// Command to run
nice --adjustment=19 python ./test.py
```

## Merging high and low

Python provides a native way to link against object files (`.so` or `Shared Object`) from its `Ctypes` library, these are named `Dynamically Linked Libraries(DLLs)` and are free from the GIL because python is not doing the `interpreting` of the code. Multiprocessing in python is quite reliant of this behavior as a DLL can launch its own threads and leverage the performance gains. Some of the more notable libraries (like `numpy`) leverage this!

For interests sake, I've prepared a sample problem where we can explore this. There is a simple algorithm for finding prime numbers called the [Sieve of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes). I will implement the sieve in `C` using `openMP` for multiprocessing and also implement the same algorithm in Python and we can compare the difference. The code is in the appendix if there is any interest around it.

## Results

| Primes     | C Time    | Python Time | Speedup     |
| ---------- | --------- | ----------- | ----------- |
| 1000       | 0.000082  | 0.000279    | 3.402439024 |
| 10000      | 0.000579  | 0.002375    | 4.101899827 |
| 100000     | 0.000991  | 0.022721    | 22.92734612 |
| 1000000    | 0.002598  | 0.244152    | 93.97690531 |
| 10000000   | 0.020822  | 2.755147    | 132.3190376 |
| 30000000   | 0.178     | 8.586468    | 48.23858427 |
| 50000000   | 0.358078  | 14.475378   | 40.42520903 |
| 70000000   | 0.540641  | 20.541209   | 37.99417543 |
| 100000000  | 0.819426  | 30.074832   | 36.70231601 |
| 300000000  | 2.717527  | 92.664603   | 34.09887114 |
| 500000000  | 4.718183  | 157.030461  | 33.28197762 |
| 1000000000 | 9.799938  | 323.484269  | 33.00880771 |
| 2000000000 | 20.437651 | 666.610642  | 32.61679349 |

## Conclusions

From the above results, we can see that the multi-processed version is atleast 30 times faster at scale and in the most favourable result (10000000 primes), it was 132 times faster. With a more pronounced hardware setup, this disparity can be pushed even higher.

With this conclusion - one might wonder why we use high level languages at all - the speed tradeoff is so massive! The answer is quite simple - because execution speed is not the only important factor!

The python version of the sieve took me less than 10 minutes to write and (in all likelihood) has less bugs. I never had to worry about the `OMP` threads colliding or how to get everything to compile! In many cases, development speed and developmental scalability are even more important the the final execution speed.

The purposes of this article was just to illustrate the design decisions that certain languages and to showcase the `Ctypes` feature of python (Which I found very cool) - and definitely not an attempt to push everyone towards lower-level languages!

## Applications

Given the speedups, I think there is some value in using this _somewhere_.

The most common application is a small, self-contained library that is easy to maintain. The reason to structure it like so is because maintain 2 languages is not easy and potentially very messy. Developing a small library with a self contained interface is the best way to hide away the complexities while leveraging the speedup!

Given the above reasoning - I would like to request some help from the reader for Part 2. Where do you think we can make a small, self-contained library to offload a calculation intensive task?

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
