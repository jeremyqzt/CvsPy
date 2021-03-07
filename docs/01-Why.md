# The Speed Tradeoff

Application execution speed always ranks highly on the mind of programmers - a slow program is almost synonymous with a bad program because it will directly, and negatively, contribute to user experience. Whenever a new app or a feature is considered, we tend to do some complexity analysis on it to ensure that, on a `macro` scale, the code will perform reasonably well.

Over time, we've gotten exceedingly good at both analyzing and implementing solid programs with low amounts of complexity. Our tools have also grown to support this - pieces of good, reusable code are made into libraries and mental models are abstracted into language features. This is awesome because it ensures that our users, as a aggregate, get an consistent experience that we can easily manage.

On the same note, I would argue that we made tradeoffs along the way, to me, one of the most striking tradeoffs is performance at the `micro` scale.

I (and probably everyone) always knew that languages offering higher levels of abstraction are slower than barebones languages but have never made comparison so I wanted to take this article as an opportunity to do a bit of research and determine a `ballpark` figure - and perhaps, through some integration, get some of it back.

## Motivation and Disclaimer

Most of what I write here is largely based on my experience (and small amount of research). It is possible (and likely) that I have gaps in my understanding and everything I write may not be 100% correct.

Apologies in advance to the reader! Please always feel free to reach out and correct me.

## Introduction

For the comparision I referred to - I will try to compare `C` and `Python`. These 2 are the languages I'm most famaliar with and both have a fairly consistent popularity according to the [TIOBE Index](https://www.tiobe.com/tiobe-index/). `C` has largely reigned surpreme for the past 30-40 years while `Python` is quickly picking up steam. Since these 2 languages has their popularity height at different times, I think we can track the progress over the time. Since we also use `Python`, I can leverage some my learnings and try to integrate with a small aread of our code base in `part 2`.

## My take on programming language evolution

Before programming languages became (somewhat) standardized, each hardware target had its unique way to develop and run applications. CPUs supported their own instruction sets and everything was a mess! This, naturally, was difficult to work with and we solved this with general-purpose programming languages. Some of the earlier languages included the likes of `Fortran` and `Cobol` (there are a few others) but these languages are generally not too popular nowadays and used used in specific applications.

The `C` language arose a bit after (and took inspiration) from some of the earlier works. The advertised motto for `C` was [write once, compile anywhere](https://en.wikipedia.org/wiki/Write_once,_compile_anywhere). This meant that the compiler were platform specific and the source code was generic. This is a method of abstraction, most of the hard work of figuring out the required `assembly` was offloaded to the compiler and the programmer needed not to worry about the specifics. Some of my more experienced co-workers told me that - at the time of this, it was quite frowned upon due to the preceived loss of speed. The loss of speed was cited to have arose from removing unique optimizations that a programmer can tailor make. However, as time pressed onwards, the compiler got better and hardware become more powerful (and complex) - it became quite impractical to know the in-and-outs of a specifc hardware platform and we commonly accept the compiler produced code as the `optimal` solution. Due to this - `C` reigned surpreme as the high-level language of choice for many years.

Eventually the complexity problem caught up and it became diffuclt to maintain cross platform support again - If there are any `C` developers in the audience, you may remember a code base littered with `#ifdef`s and doing some mental juggling to figure out the exact code path. Again, to solve this problem, programmers turned to abstraction and took away the runtime. `Java` is the notable example of this - it was widely advertised as [write once, run anywhere](https://en.wikipedia.org/wiki/Write_once,_run_anywhere)! This was accomplised by compiling to `Byte Code` and later `interpreting` it all under a common virtual machine (the `JVM`)!

Coming from the `C` world, I was really surprised how well this worked, a `.jar` can be ran on almost any platform/OS as long as the proper version of `Java` was installed - Many of the `Java` based game clients of the 2000s were originally meant for windows but can be ran under a Linux system without recompiling - running `java --jar <name.jar>` worked just fine.

We eventually took the `write once, run anywhere` further and arrived at many languages that fit the motto much better - a prime example is Python! Python is a fully interpreted language - the compile process is no more and an interpreter takes care of all translations in a `Just in Time` manner. While `C` and `Java` still dominate the industry, Python is quickly rising and is now a close third on the [TIOBE Index](https://www.tiobe.com/tiobe-index/).

This is largely where we are at now!

## The speed tradeoff

As programming languages evolved, so too has the debugging tools and modelling paradigms.

Newer paradigms allows us to imagine programs in a intuitive sense and the task became modelling the world rather than issuing sequential commands to a machine. I would say one of the results from this evolution is [Object-Oriented Programming](https://en.wikipedia.org/wiki/Object-oriented_programming). This format of programming lets us model the world as individual objects and allows use to think about `what a object can do` rather than `what the code must do`. This is great because programmers can do less mental gymnastics to get the end result they're after (With less bugs too). Concurrently, the tooling for programmers have also become more and more powerful - The goal for any tool is to give a full snapshot of the program's inner state. This can tell the developer exactly what has gone wrong. For the most part, this has evolved in tandem with our paradigms and have become important language features - comparision python 2s' breakpoint to python 3 is a night and day difference!

All these features are really nice but they require additional overhead but they are not handled without cost. What a high-level language gains in is ability to abstract, it looses the same amount in speed.

[Here are some benchmarks for the curious.](https://benchmarksgame-team.pages.debian.net/benchmarksgame/fastest/python3-gcc.html).

## An example of the tradeoff

A prominent example of the speed tradeoff is the `Global Interpreter Lock (GIL)` that is commonly seen in python implementations (i.e. `Cpython`).

THe purpose of this lock is to hold a mutually exclusive (mutex) lock over the python intepreter and is a active [design decision](https://wiki.python.org/moin/GlobalInterpreterLock). This has undoubtadly helped the language to be as user-friendly as it is and also likely contributed to its rapid evolution! At the same time, it is definitely a important implementation note to consider!

We can write a simple application to illustrate how this lock works. Consider the following program that counts down from five million.

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

We can write a threaded version of the same program where we distribute the workload across 4 threads (i.e. each thread counts down from 1.25 million).

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

Convention would tell us that the program should execute 4 times faster - with some fixed overhead to start the threads. However, this isn't the case and the program takes almost 5.4 seconds to run!

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

From this experiment, we get a sense that python code acquires the mutex when it needs to execute and threading generally does us no good! In fact, if we factor in thread startup time, it likely hurts the performance.

## Bypassing the tradeoff

This part is where I found the most interesting. Given that python was implemented using C, I had a feeling that we could intergrate the 2 somehow.

Python provides a native way to link against object files (`.so` or `Shared Object`) from its `Ctypes` library, these are named `Dynamically Linked Libraries(DLLs)` and are free from the GIL because python is not doing the `interpreting` of the code. Multiprocessing in python is quite reliant of this behavior as a DLL can launch its own threads and leverage the performance gains. Some of the more notable libraries (like `numpy`) leverage this!

For interests sake, I've prepared a sample problem where we can explore this. There is a simple algorithm for finding prime numbers called the [Sieve of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes). I will implement the sieve in `C` using `openMP` for multiprocessing and also implement the same algorithm in Python and we can compare the difference. The code is in the appendix if there is any interest around it.

## Results and Conclusions

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

From the above results, we can see that the multi-processed version is atleast 30 times faster at scale and in the most favourable result (10000000 primes), it was 132 times faster. With a more pronounced hardware setup (i.e. more CPU cores), this disparity can be pushed even higher.

So we have our answer to the initial query. Simpler langauges are significantly faster on the micro scale. With this conclusion - one might wonder why we use high level languages at all - the speed tradeoff is so massive! The answer is quite simple - because execution speed is not the only important factor. There are rarely times where we need all the primes up to 20million. Furthermore, the python version of the sieve took me less than 10 minutes to write and (in all likelihood) has less bugs. I never had to worry about the threads colliding or how to get everything to compile! In almost all cases, development speed and developmental scalability are even more important the the final execution speed of a single instance.

## Applications

Given the speedups, I think there is some value in using this _somewhere_.

The most common application is a small, self-contained library that is easy to maintain. The reason to structure it like so is because maintain 2 languages is not easy and potentially very messy. Developing a small library with a self contained interface is the best way to hide away the complexities while leveraging the speedup! As an example - Machine learning libraries such as `numpy` likely use this to crunch large data sets.

Given the above - I would like to request some help from the reader for Part 2. Where do you think we can make a small, self-contained library to offload a calculation intensive task?

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
