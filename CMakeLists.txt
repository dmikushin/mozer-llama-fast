cmake_minimum_required(VERSION 3.17 FATAL_ERROR)

project(talk-llama-fast VERSION 1.5.4 LANGUAGES C CXX CUDA)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

option(WHISPER_BUILD_TESTS "whisper: build tests" OFF)

set(FLAGS "-march=native -fno-math-errno -funsafe-math-optimizations")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${FLAGS}")

find_package(Threads REQUIRED)
find_package(SDL2 REQUIRED)
find_package(CURL REQUIRED)
find_package(CUDAToolkit REQUIRED)

add_executable(${PROJECT_NAME}
    src/talk-llama-fast.cpp
    src/llama.cpp
    src/ggml.c
    src/ggml-alloc.c
    src/ggml-backend.c
    src/ggml-quants.c
    src/ggml-cuda.cu
    src/whisper.cpp
    src/console.cpp
    src/common.cpp
    src/common-sdl.cpp
    src/common-ggml.cpp
    src/grammar-parser.cpp)
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_compile_definitions(${PROJECT_NAME} PRIVATE GGML_USE_CUBLAS _WIN32_WINNT=0x0602)
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 14)
set_property(TARGET ${PROJECT_NAME} PROPERTY CUDA_ARCHITECTURES "native")
target_link_libraries(${PROJECT_NAME} PRIVATE m SDL2::SDL2 CURL::libcurl CUDA::cudart_static CUDA::cublas_static CUDA::cublasLt_static CUDA::cuda_driver ${CMAKE_THREAD_LIBS_INIT})

# clock_gettime came in POSIX.1b (1993)
# CLOCK_MONOTONIC came in POSIX.1-2001 / SUSv3 as optional
# posix_memalign came in POSIX.1-2001 / SUSv3
# M_PI is an XSI extension since POSIX.1-2001 / SUSv3, came in XPG1 (1985)
target_compile_definitions(${PROJECT_NAME} PRIVATE _XOPEN_SOURCE=600)

# Data types, macros and functions related to controlling CPU affinity
# are available on Linux through GNU extensions in libc
target_compile_definitions(${PROJECT_NAME} PRIVATE _GNU_SOURCE)

if (WHISPER_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif ()

