# Global project options
option(BUILD_TESTING "Build tests" OFF)
option(BUILD_BENCH "Build benchmarks" OFF)

# Required app libs for some options (profilers, sanitizers)
set (OPTS_APP_LIBS)
# Required test app libs for some options (profilers, sanitizers)
set (OPTS_TEST_LIBS)


set (PROFILE_LIB)
