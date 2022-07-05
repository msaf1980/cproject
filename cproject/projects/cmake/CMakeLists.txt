cmake_minimum_required(VERSION 3.18)

include(${CMAKE_SOURCE_DIR}/options.cmake)
include(${CMAKE_SOURCE_DIR}/settings.cmake)

if(PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
    message(
        FATAL_ERROR
            "In-source builds not allowed. Please make a new directory (called a build directory) and run CMake from there."
    )
endif()

# Include cmake prescript from cmake_pre dir (before set project)
file(GLOB cmakeFiles cmake_pre/*.cmake)
foreach(cmakeFile ${cmakeFiles})
    message("INCLUDE ${cmakeFile}")
    include(${cmakeFile})
endforeach(cmakeFile)

project(${PROJECT} VERSION ${VERSION})

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

# Include cmake script from cmake_post dir (after set project)
file(GLOB cmakeFiles cmake_post/*.cmake)
foreach(cmakeFile ${cmakeFiles})
    message("INCLUDE ${cmakeFile}")
    include(${cmakeFile})
endforeach(cmakeFile)

include(dependecies.cmake)

if(DEFINED ENV{DEVENV})
    set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
endif()

if(BUILD_TESTING)
    # enable_testing()
    include(CTest)
endif()

configure_file("${PROJECT_SOURCE_DIR}/version.h.in" "${CMAKE_CURRENT_BINARY_DIR}/include/version.h")
include_directories("${CMAKE_CURRENT_BINARY_DIR}/include")

include(targets.cmake)

include(options_print.cmake)
