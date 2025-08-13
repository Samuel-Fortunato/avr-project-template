# avr-toolchain.cmake
# This file defines the AVR toolchain for CMake.

set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR avr)

find_program(CMAKE_C_COMPILER NAMES avr-gcc avr-gcc.exe)
if(NOT CMAKE_C_COMPILER)
    message(FATAL_ERROR "AVR-GCC compiler not found. Please add it to your PATH or set CMAKE_C_COMPILER manually.")
endif()

add_compile_options("-Os")

find_program(AVR_OBJCOPY NAMES avr-objcopy avr-objcopy.exe)
if(NOT AVR_OBJCOPY)
    message(FATAL_ERROR "avr-objcopy not found. Please add it to your PATH.")
endif()

find_program(AVRDUDE NAMES avrdude avrdude.exe)
if(NOT AVRDUDE)
    message(FATAL_ERROR "avrdude not found. Please add it to your PATH.")
endif()

