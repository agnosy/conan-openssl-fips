cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

string(
    CONCAT CMAKE_C_LINK_EXECUTABLE
    "env FIPSLD_CC=${CMAKE_C_COMPILER}"
    " ${CONAN_OPENSSLFIPS_ROOT}/bin/fipsld <FLAGS> <CMAKE_C_LINK_FLAGS> <LINK_FLAGS> <OBJECTS>"
    " -o <TARGET> <LINK_LIBRARIES>"
)
string(
    CONCAT CMAKE_CXX_LINK_EXECUTABLE
    "env FIPSLD_CC=${CMAKE_CXX_COMPILER}"
    " ${CONAN_OPENSSLFIPS_ROOT}/bin/fipsld++ <FLAGS> <CMAKE_CXX_LINK_FLAGS> <LINK_FLAGS> <OBJECTS>"
    " -o <TARGET> <LINK_LIBRARIES>"
)

add_executable(example example.cpp)
target_link_libraries(example ${CONAN_LIBS})

# CTest is a testing tool that can be used to test your project.
# enable_testing()
# add_test(NAME example
#          WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#          COMMAND example)
