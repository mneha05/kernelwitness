#include <cuda_runtime.h>

__global__ void shared_race(int* out) {
    __shared__ int x;
    if (threadIdx.x < 2) x = threadIdx.x; // intentional WAW hazard
    if (threadIdx.x == 0) *out = x;
}

int main() {
    int* out = nullptr;
    cudaMalloc(&out, sizeof(int));
    shared_race<<<1, 32>>>(out);
    cudaDeviceSynchronize();
    cudaFree(out);
}
