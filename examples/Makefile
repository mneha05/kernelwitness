NVCC ?= nvcc
CXXFLAGS ?= -lineinfo -O1
all: cuda_oob cuda_race
cuda_oob: cuda_oob.cu
	$(NVCC) $(CXXFLAGS) $< -o $@
cuda_race: cuda_race.cu
	$(NVCC) $(CXXFLAGS) $< -o $@
clean:
	rm -f cuda_oob cuda_race
