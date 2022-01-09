cmake_minimum_required(VERSION 3.8)
project(cmpe250-project3-oztasozgurcan-master)

set(CMAKE_CXX_STANDARD 11)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp)
add_executable(project3 ${SOURCE_FILES})
