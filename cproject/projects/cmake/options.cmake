# Local project options
if(CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
    option(BUILD_TESTING "Build tests" ON)
    option(BUILD_BENCH "Build benchmarks" ON)
else()
    # For avoid options migration when used as subdirectory
    option({{PROJECT}}_BUILD_TESTING "Build tests" OFF)
    set(BUILD_TESTING "${{{PROJECT}}_BUILD_TESTING}")
    option({{PROJECT}}_BUILD_BENCH "Build benchmarks" OFF)
    set(BUILD_BENCH "${{{PROJECT}}_BUILD_BENCH}")
endif()
