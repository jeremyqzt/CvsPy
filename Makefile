CC=gcc
CFLAGS= -Wall -g -O -fPIC
CFLAGS_EXE= -Wall -g -O3
OBJ = sieve.o

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS)

sieve.so: $(OBJ)
	$(LINK.c) -shared $^ -o $@

sieve: $(OBJ) main.o
	$(CC) -o $@ $^ $(CFLAGS_EXE)

all: sieve sieve.so

clean:
	rm *.o *.so sieve

.PHONY: all clean
