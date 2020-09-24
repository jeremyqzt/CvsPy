CC=gcc
CFLAGS= -Wall -g -O -fPIC
OBJ = sieve.o

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS)

sieve.so: $(OBJ)
	$(LINK.c) -shared $^ -o $@

all: sieve.so

clean:
	rm *.o *.so

.PHONY: all clean
