#include <cuda_runtime.h>
#include <cstdio>

__global__ void write_one_past_end(float* x, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i <= n) x[i] = 1.0f; // i == n is intentionally one element out of bounds.
}

int main() {
    constexpr int n = 257;
    float* x = nullptr;
    cudaMalloc(&x, n * sizeof(float));
    write_one_past_end<<<2, 256>>>(x, n);
    auto err = cudaDeviceSynchronize();
    std::fprintf(stderr, "cudaDeviceSynchronize: %s\n", cudaGetErrorString(err));
    cudaFree(x);
    return err == cudaSuccess ? 0 : 1;
}
