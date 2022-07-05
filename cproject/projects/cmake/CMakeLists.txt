cmake_minimum_required(VERSION 3.18)

include(${CMAKE_SOURCE_DIR}/options.cmake)
include(${CMAKE_SOURCE_DIR}/settings.cmake)

# Include cmake prescript from cmake dir
file(GLOB cmakeFiles cmake_pre/*.cmake)
foreach(cmakeFile ${cmakeFiles})
    message("INCLUDE ${cmakeFile}")
    include(${cmakeFile})
endforeach(cmakeFile)

project(${PROJECT})

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

file(GLOB cmakeFiles cmake/*.cmake)
foreach(cmakeFile ${cmakeFiles})
    message("INCLUDE ${cmakeFile}")
    include(${cmakeFile})
endforeach(cmakeFile)

if(DEFINED ENV{DEVENV})
    set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
endif()

if(BUILD_TESTING)
    # enable_testing()
    include(CTest)
endif()

include(dependecies.cmake)
include(targets.cmake)

include(options_print.cmake)
