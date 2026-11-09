# Build the fast enumerators, linking libhomfly from the SageMath installation.
# SAGE_LOCAL is the directory with include/homfly.h and lib/libhomfly.*; by default it is asked to Sage
# (`sage` on the PATH). Override it with `make SAGE_LOCAL=/path/to/sage/local` if needed.
SAGE_LOCAL ?= $(shell sage -c "import os, sage.env; print(os.path.realpath(sage.env.SAGE_LOCAL))" 2>/dev/null)
CXX ?= clang++
CXXFLAGS ?= -O3 -march=native -std=c++17 -Wall

all: bin/fknots bin/iota_knots

bin/fknots: src/fknots.cpp
	mkdir -p bin
	$(CXX) $(CXXFLAGS) -I$(SAGE_LOCAL)/include $< -o $@ -L$(SAGE_LOCAL)/lib -lhomfly -Wl,-rpath,$(SAGE_LOCAL)/lib

# F_3 (and F through iota, as a cross-check of fknots)
bin/iota_knots: src/iota_knots.cpp
	mkdir -p bin
	$(CXX) $(CXXFLAGS) -I$(SAGE_LOCAL)/include $< -o $@ -L$(SAGE_LOCAL)/lib -lhomfly -Wl,-rpath,$(SAGE_LOCAL)/lib

clean:
	rm -rf bin
