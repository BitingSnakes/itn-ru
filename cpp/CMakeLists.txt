cmake_minimum_required(VERSION 3.16)
project(rus_itn VERSION 0.2.0 LANGUAGES CXX)

include(CTest)
include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

option(RUS_ITN_BUILD_CLI "Build the rus_itn command-line tool" ON)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
find_package(OpenFST REQUIRED)

add_library(rus_itn src/rus_itn.cc)
add_library(rus_itn::rus_itn ALIAS rus_itn)
target_compile_features(rus_itn PUBLIC cxx_std_17)
set_target_properties(rus_itn PROPERTIES
  CXX_EXTENSIONS OFF
  POSITION_INDEPENDENT_CODE ON
  VERSION ${PROJECT_VERSION}
  SOVERSION ${PROJECT_VERSION_MAJOR})
target_include_directories(rus_itn PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)
target_link_libraries(rus_itn PUBLIC OpenFST::fst)

if(RUS_ITN_BUILD_CLI)
  add_executable(rus_itn_cli tools/rus_itn_main.cc)
  target_compile_features(rus_itn_cli PRIVATE cxx_std_17)
  set_target_properties(rus_itn_cli PROPERTIES CXX_EXTENSIONS OFF)
  target_link_libraries(rus_itn_cli PRIVATE rus_itn::rus_itn)
endif()

if(BUILD_TESTING)
  add_executable(rus_itn_test tests/rus_itn_test.cc)
  target_compile_features(rus_itn_test PRIVATE cxx_std_17)
  set_target_properties(rus_itn_test PROPERTIES CXX_EXTENSIONS OFF)
  target_link_libraries(rus_itn_test PRIVATE rus_itn::rus_itn)
  add_test(NAME rus_itn_test COMMAND rus_itn_test)
endif()

install(TARGETS rus_itn
  EXPORT rus_itnTargets
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
if(RUS_ITN_BUILD_CLI)
  install(TARGETS rus_itn_cli RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
endif()
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

configure_package_config_file(
  cmake/rus_itnConfig.cmake.in
  "${CMAKE_CURRENT_BINARY_DIR}/rus_itnConfig.cmake"
  INSTALL_DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/rus_itn")
write_basic_package_version_file(
  "${CMAKE_CURRENT_BINARY_DIR}/rus_itnConfigVersion.cmake"
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion)

install(EXPORT rus_itnTargets
  FILE rus_itnTargets.cmake
  NAMESPACE rus_itn::
  DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/rus_itn")
install(FILES
  "${CMAKE_CURRENT_BINARY_DIR}/rus_itnConfig.cmake"
  "${CMAKE_CURRENT_BINARY_DIR}/rus_itnConfigVersion.cmake"
  cmake/FindOpenFST.cmake
  DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/rus_itn")
