# Global project options
option(BUILD_TESTING "Build tests" ON)
option(BUILD_BENCH "Build benchmarks" OFF)

option(COMPILER_ALL_WARNINGS "Compile with all warnings for the major compilers" OFF)
option(COMPILER_CONVERSION_WARNINGS "Compile with conversion warnings for the major compilers" OFF)
option(COMPILER_WARNINGS_AS_ERROR "Make all warnings into errors" OFF)
option(COMPILER_EFFECTIVE_CXX "Enable Effective C++ warnings" OFF)
option(COMPILER_REQUIRE_ISO_CXX "Require ISO C/C++" OFF)
option(COMPILER_HEADER_DEPENDENCY_DATA "Generates .d files with header dependencies" OFF)

option(DEBUGINFO "Add debug info" ON)
