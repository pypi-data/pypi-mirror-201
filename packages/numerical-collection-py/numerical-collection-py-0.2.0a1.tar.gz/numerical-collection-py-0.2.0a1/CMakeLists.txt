cmake_minimum_required(VERSION 3.12)

set(SHORT_PROJECT_NAME "num_collect_py")
set(FULL_PROJECT_NAME "numerical-collection-py")

project(
    ${SHORT_PROJECT_NAME}
    DESCRIPTION
        "A collection of algorithms in numerical analysis for Python (originally implemented in C++)."
    LANGUAGES CXX)
message(STATUS "build type: ${CMAKE_BUILD_TYPE}")

string(TOUPPER ${PROJECT_NAME} UPPER_PROJECT_NAME)

set(CMAKE_CXX_STANDARD
    "20"
    CACHE STRING "C++ standard" FORCE)

set(CMAKE_EXPORT_COMPILE_COMMANDS
    ON
    CACHE BOOL "export compile commands" FORCE)

set(NUM_COLLECT_PY_UPDATE_STUB
    OFF
    CACHE BOOL "update stub file automatically")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY $<1:${CMAKE_BINARY_DIR}/lib>)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY $<1:${CMAKE_BINARY_DIR}/lib>)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY $<1:${CMAKE_BINARY_DIR}/bin>)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
set(CONAN_COMPILER ${CONAN_SETTINGS_COMPILER})
set(CONAN_COMPILER_VERSION ${CONAN_SETTINGS_COMPILER_VERSION})
set(CONAN_LIBCXX ${CONAN_SETTINGS_COMPILER_LIBCXX})
conan_basic_setup(NO_OUTPUT_DIRS)

# Search poetry.
if(NUM_COLLECT_PY_UPDATE_STUB)
    list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
    include(poetry)
    find_program(
        PYTHON_EXECUTABLE
        NAMES python3 python
        PATHS ${POETRY_VENV_DIR}/.venv/bin ${POETRY_VENV_DIR}/.venv/Scripts
        NO_DEFAULT_PATH)
endif()

# Search Python (prefer Python in virtualenv).
if(NOT PYTHON_EXECUTABLE)
    find_program(
        PYTHON_EXECUTABLE
        NAMES python3 python
        PATHS ${CMAKE_CURRENT_SOURCE_DIR}/.venv/bin
              ${CMAKE_CURRENT_SOURCE_DIR}/.venv/Scripts
        NO_DEFAULT_PATH)
endif()
if(NOT PYTHON_EXECUTABLE)
    find_program(PYTHON_EXECUTABLE NAMES python3 python REQUIRED)
endif()
execute_process(
    COMMAND "${PYTHON_EXECUTABLE}" -m pybind11 --cmakedir
    OUTPUT_VARIABLE pybind11_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE)

# Find packages installed with Conan.
list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
list(APPEND CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})
find_package(num_collect REQUIRED)
find_package(pybind11 REQUIRED)

set(NUM_COLLECT_PY_ROOT
    ${CMAKE_CURRENT_SOURCE_DIR}
    CACHE STRING "Do no change this value except for use in setup.py.")

set(NUM_COLLECT_PY_CPP_MODULE_OUT_DIR
    ${NUM_COLLECT_PY_ROOT}/num_collect/_cpp_module)

add_subdirectory(cpp_module)
