message(STATUS "")
message(STATUS "BUILD SUMMARY")
message(STATUS "  CMAKE_GENERATOR       : ${CMAKE_GENERATOR}")
message(STATUS "  C Compiler            : ${CMAKE_C_COMPILER} (${CMAKE_C_COMPILER_ID})")
message(STATUS "  C++ Compiler          : ${CMAKE_CXX_COMPILER} (${CMAKE_CXX_COMPILER_ID})")
message(STATUS "  Build type            : ${CMAKE_BUILD_TYPE}")
message(STATUS "  Build tests           : ${BUILD_TESTING}")
message(STATUS "  Build benchmarks      : ${BUILD_BENCH}")
message(STATUS "  Sanitizer             : ${SANITIZER}")
message(STATUS "")
message(STATUS "  Install prefix : ${CMAKE_INSTALL_PREFIX}")
message(STATUS "  Binary dir     : ${BINDIR}")
message(STATUS "  Lib dir        : ${LIBDIR}")
message(STATUS "")
message(STATUS "CMAKE_CXX_FLAGS            : ${CMAKE_CXX_FLAGS}")
message(STATUS "CMAKE_C_FLAGS              : ${CMAKE_C_FLAGS}")
message(STATUS "CMAKE_SHARED_LINKER_FLAGS  : ${CMAKE_SHARED_LINKER_FLAGS}")
message(STATUS "CMAKE_EXE_LINKER_FLAGS     : ${CMAKE_EXE_LINKER_FLAGS}")
message(STATUS "")