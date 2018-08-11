#To build executable for raspberry pi, run
#	make RPI=1

TARGET_1 = ./bin/gentestvid
TARGET_2 = ./bin/selectroi

CXX = g++
INC = `pkg-config --cflags opencv` -I./include/ #and other include paths -I
LIB = `pkg-config --libs opencv` $(LIB_RPICAM) #and other lib paths and lib names -L -l

CFLAGS = -Wall -c -std=c++11
LFLAGS = -Wall -pthread

COMPILE = $(CXX) $(CFLAGS) $(INC) $(DEBUG) $^ -o $@
LINK = $(CXX) $(LFLAGS) $(LIB) $^ -o $@


.PHONY: all
all: $(TARGET_1) $(TARGET_2)#and other targets

$(TARGET_1): ./build/gentestvid.o
	$(LINK)
./build/gentestvid.o: ./src/gentestvid.cpp
	$(COMPILE)

$(TARGET_2): ./build/selectroi.o
	$(LINK)
./build/selectroi.o: ./src/selectroi.cpp
	$(COMPILE)


#[other targets]

$(shell mkdir -p bin)
$(shell mkdir -p build)

clean:
	rm -frv ./build/*.o
