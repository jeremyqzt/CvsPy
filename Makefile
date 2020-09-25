CC=gcc
CFLAGS= -Wall -g -O3 -fPIC
CFLAGS_EXE= -Wall -g -O3 -lm
OMP_FALGS= -fopenmp -lgomp
OBJ = sieve.o

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS) $(OMP_FALGS)

sieve.so: $(OBJ)
	$(LINK.c) -shared $^ -o $@

sieve: $(OBJ) main.o
	$(CC) -o $@ $^ $(CFLAGS_EXE) $(OMP_FALGS)

all: sieve sieve.so

clean:
	rm *.o *.so sieve

.PHONY: all clean
