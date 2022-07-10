if(BUILD_TESTING)
    if(NOT GBENCH_VERSION)
        set(GBENCH_VERSION "1.6.1")
    endif()

    include(FetchContent)

    set(BENCHMARK_ENABLE_GTEST_TESTS OFF)
    set(BENCHMARK_ENABLE_TESTING OFF)
    FetchContent_Declare(
        GBench
        GIT_REPOSITORY https://github.com/google/benchmark.git
        GIT_TAG v${GBENCH_VERSION}
    )

    FetchContent_GetProperties(GBench)
    if(NOT GBench_POPULATED)
        FetchContent_MakeAvailable(GBench)
    endif()
    
    set(GBENCH_LIBS benchmark::benchmark)
endif()
