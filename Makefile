CC=gcc
CFLAGS= -Wall -g -O3 -fPIC -shared -std=c99
CFLAGS_EXE= -Wall -g -O3 -lm -std=c99
OMP_FALGS= -fopenmp -lgomp -lomp
OBJ = sieve.o
TARGET=main
TARGET_LIB=libsieve.so

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS) $(OMP_FALGS)

$(TARGET_LIB): $(OBJ)
	$(LINK.c) $(CFLAGS) $(OMP_FALGS) $^ -o $@

$(TARGET): $(OBJ) main.o
	$(CC) -o $@ $^ $(CFLAGS_EXE) $(OMP_FALGS)

all: $(TARGET) $(TARGET_LIB)

clean:
	rm -rf *.o *.so sieve

.PHONY: all clean
