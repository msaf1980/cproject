# Add target subdirectories

# Default includes
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/include")
    include_directories(include)
endif()

# Default sources (for libs or apps, if no internal libs)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/CMakeLists.txt")
    add_subdirectory(src)
endif()

# Default sources (for apps)
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/apps/CMakeLists.txt")
    add_subdirectory(apps)
endif()

# Default tests
if(BUILD_TESTING AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/tests/CMakeLists.txt")
    add_subdirectory(tests)
endif()

# Default benchmarks
if(BUILD_BENCH AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/benchmark/CMakeLists.txt")
    add_subdirectory(benchmark)
endif()

# Default examples
if(BUILD_EXAMPLES AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/examples/CMakeLists.txt")
    add_subdirectory(examples)
endif()

# Default docs
if(_CI_MODE AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/docs/CMakeLists.txt")
    add_subdirectory(docs)
endif()
