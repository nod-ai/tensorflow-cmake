cmake_minimum_required(VERSION 3.15)
project(tensorflow_test)

find_package(TensorflowCC REQUIRED)

add_executable(tensorflow_smoke_test smoke_test.cpp)
target_link_libraries(tensorflow_smoke_test TensorflowCC::TensorflowCC)
