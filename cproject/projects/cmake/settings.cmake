set(PROJECT {{PROJECT}})
set(VERSION {{VERSION}})
set(HOMEPAGE_URL)
set(DESCRIPTION)

if(NOT DEFINED CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD {{CXX_STD}})
endif()
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

if(NOT DEFINED CMAKE_C_STANDARD)
    set(CMAKE_C_STANDARD {{C_STD}})
endif()
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)

if(CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
    set(MAIN_PROJECT ON)
    if(DEFINED ENV{DEVENV})
        set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
    endif()
else()
    set(MAIN_PROJECT OFF)
endif()
