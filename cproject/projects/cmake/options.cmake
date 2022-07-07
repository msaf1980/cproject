# Local project options
if(NOT CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
    # For avoid options migration when used as subdirectory
    option({{PROJECT}}_BUILD_TESTING "Build tests" OFF)
    set(BUILD_TESTING "${{{PROJECT}}_BUILD_TESTING}")
    option({{PROJECT}}_BUILD_BENCH "Build benchmarks" OFF)
    set(BUILD_BENCH "${{{PROJECT}}_BUILD_BENCH}")
else()
    option(BUILD_TESTING "Build tests" OFF)
    option(BUILD_BENCH "Build benchmarks" OFF)
endif()
