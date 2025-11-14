cmake_minimum_required(VERSION 3.16)

# Define the project name and version
project(SolutionToDay01 LANGUAGES CXX)

# Define the source files
set(SOURCES
  main.cpp
  getinput.hpp
)

# Define the executable name
add_executable(solution ${SOURCES})
