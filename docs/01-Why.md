# A unorthodox way to massively program execution speed

Imagine this - we wrote the same program, both have similar lines of code but one has a hundredth (!!!) the execution time. This sounds impossible. Well I'm here to say its not and we'll explore it more in this article.

## Disclaimer
I am writing this based on my perceived understanding of the subjects - It is possible (and likely) that I have gaps in my understanding and everything I write may not e 100% correct. Apologies in advance to the reader!

## My take on programming language evolution

I cheated a little bit when I wrote the introduction - writing the same program with similar line counts doesn't mean we used the same developments tools. For the rest of the article, I will make a comparison between C and Python to show the advantages and disadvantages of each and explain how we can get massive speedups in execution time. At a later time, I will write a part 2 - to explore how we can integrate this into a niche area of our code.

I'm sure we're all aware the differences between compiled and interpreted but in case we forgot:

- A compiled language must be translated into a binary of machine code before it can be ran
- A interpreted language can be compiled 'Just-In-Time' for it to be ran, eliminating the compilation step

Before programming languages became (somewhat) standardized, each hardware target had its unique way to program and run. This, naturally, was difficult to work with and the advent of the `C` language, the motto of [write once, compile anywhere](https://en.wikipedia.org/wiki/Write_once,_compile_anywhere) became the dominate way to appraoch programming.

As software and hardware both became more complex, compilers (especially cross-compilers) diverged and it became extremely difficult to maintain the `compile anywhere` part of the motto. As programmers - we needed a solution and quickly came to the reliable concept of `abstraction`. The compile process was abstracted and we got the motto of [write once, run anywhere] (https://en.wikipedia.org/wiki/Write_once,_run_anywhere) - this gave rise to `Java`.

`Java` still maintained the compile process but instead of machine code, the target was `Byte Code` which was interpreted by a `Java Virtual Machine (JVM)`. Java was (and still is) a very popular programming language but it has its fair share of [criticisms](https://en.wikipedia.org/wiki/Criticism_of_Java).

We eventually took the `write once, run anywhere` further and arrived at many languages that fit the motto much better - a prime example is Python! While `C` and `Java` still dominate the industry, Python is quickly rising and is now a close third on the [TIOBE Index](https://www.tiobe.com/tiobe-index/).

Python is a fully interpreted language - the interpreter takes care of all translations and, for the most part, it delivers on the `write once and run anywhere` promise.

## Interpreted Vs Compiled

Now that we've seen how programming languages evolved - we can speak on the pros and cons of this evolution.

For an interpreted language - many high level features are standard. High level programming concepts, such as object-orientation and polymorphism, can be modeled. Ready-made libraries can be fit in with relative ease and garbage collection is automatic!

This setup is very optimal for rapid prototyping and feature development (And explains the rapidly rise in popularity of such languages)!

With so many new features and great support - one might wonder why we still use languages like C where better alternatives like Python are available. The answer is speed - see some [benchmarks for gcc compiled vs python interpreted](https://benchmarksgame-team.pages.debian.net/benchmarksgame/fastest/python3-gcc.html)

## Python Vs C

On first glance - one can conclude that Python and C are completely different and have different roles and purposes - While this conclusion is true, the 2 languages are surprising similar under the hood because the reference implementation of python is implemented using C.
