# Build the fast enumerator, linking libhomfly from the SageMath installation.
SAGE_LOCAL ?= /Applications/SageMath-10-8.app/Contents/Frameworks/Sage.framework/Versions/Current/local
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
