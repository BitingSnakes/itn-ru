cmake_minimum_required(VERSION 3.16)
project(rus_itn LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# OpenFST (brew install openfst / apt install libfst-dev)
find_path(FST_INCLUDE_DIR fst/fstlib.h
  HINTS /opt/homebrew/include /usr/local/include /usr/include)
find_library(FST_LIBRARY fst
  HINTS /opt/homebrew/lib /usr/local/lib /usr/lib)
if(NOT FST_INCLUDE_DIR OR NOT FST_LIBRARY)
  message(FATAL_ERROR "OpenFST not found; install it (e.g. `brew install openfst`)")
endif()

add_library(rus_itn src/rus_itn.cc)
target_include_directories(rus_itn
  PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include ${FST_INCLUDE_DIR})
target_link_libraries(rus_itn PUBLIC ${FST_LIBRARY})

add_executable(rus_itn_cli tools/rus_itn_main.cc)
target_link_libraries(rus_itn_cli PRIVATE rus_itn)

install(TARGETS rus_itn rus_itn_cli)
install(DIRECTORY include/ DESTINATION include)
