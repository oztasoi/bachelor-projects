cmake_minimum_required(VERSION 2.8)
project(cmpe250-project5-oztasozgurcan-master)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -O2")

set(SOURCE_FILES main.cpp)
add_executable(project5 ${SOURCE_FILES})