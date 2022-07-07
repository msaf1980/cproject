cmake_minimum_required(VERSION 3.14)

include(${CMAKE_CURRENT_SOURCE_DIR}/settings.cmake)
include(${CMAKE_CURRENT_SOURCE_DIR}/options.cmake)

if(PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
    message(
        FATAL_ERROR
            "In-source builds not allowed. Please make a new directory (called a build directory) and run CMake from there."
    )
endif()

# Include cmake prescript from cmake_pre dir (before set project)
# if(_CI_MODE)
#     file(GLOB cmakeFiles cmake_pre/*.cmake)
#     foreach(cmakeFile ${cmakeFiles})
#         message("INCLUDE ${cmakeFile}")
#         include(${cmakeFile})
#     endforeach(cmakeFile)
# endif()

project(${PROJECT} VERSION ${VERSION})

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

# Include cmake script from cmake_autoload dir (after set project)
file(GLOB cmakeFiles cmake_autoload/*.cmake)
foreach(cmakeFile ${cmakeFiles})
    message("INCLUDE ${cmakeFile}")
    include(${cmakeFile})
endforeach(cmakeFile)

# Include cmake script from cmake_autoload dir (after set project)
if(_CI_MODE)
    file(GLOB cmakeFiles cmake_opts/*.cmake)
    foreach(cmakeFile ${cmakeFiles})
        message("INCLUDE ${cmakeFile}")
        include(${cmakeFile})
    endforeach(cmakeFile)
endif()

# Include cmake script from cmake_dep dir (for setup dependecies)
file(GLOB cmakeFiles cmake_dep/*.cmake)
foreach(cmakeFile ${cmakeFiles})
    message("INCLUDE ${cmakeFile}")
    include(${cmakeFile})
endforeach(cmakeFile)

include(${CMAKE_CURRENT_SOURCE_DIR}/merge.cmake)

configure_file("${PROJECT_SOURCE_DIR}/version.h.in" "${CMAKE_CURRENT_BINARY_DIR}/generated-includes/${PROJECT}/version.h")
include_directories("${CMAKE_CURRENT_BINARY_DIR}/generated-includes")

if(BUILD_TESTING)
    # enable_testing()
    include(CTest)
endif()

include(${CMAKE_CURRENT_SOURCE_DIR}/targets.cmake)

include(${CMAKE_CURRENT_SOURCE_DIR}/options_print.cmake)
