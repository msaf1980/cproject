set(PROFILERS_LIST "gperftools" "prof" "gprof")

list(JOIN PROFILERS_LIST " " PROFILERS)

set(PROFILE
    ""
    CACHE STRING "Enable profiler. Options are: ${PROFILERS}"
)

# Don't forget link application with this lib, need for some profilers like gperftools
if(PROFILE)
    # Temporary for merge with OPTS_APP_LIBS and OPTS_TEST_LIBS
    set(PROFILE_LIB)

    string(TOLOWER "${PROFILE}" PROFILE_l)
    if(PROFILE_l STREQUAL "gperftools")
        # overwrite PROFILE_LIB if non-system gperftools is needed
        set(PROFILE_LIB profiler)
        message("")
        message(STATUS "For use gperftools don't forget link application with library in PROFILE_LIB variable\n")
    elseif(PROFILE_l STREQUAL "prof")
        if(CMAKE_COMPILER_IS_GNU OR CMAKE_COMPILER_IS_CLANG)
            add_compile_options(-p)
            add_link_options(-p)
        else()
            message(
                FATAL_ERROR
                    "Profile with ${PROFILE} is not supported on this platform (${CMAKE_C_COMPILER_ID})."
            )
        endif()
    elseif(PROFILE_l STREQUAL "gprof")
        if(CMAKE_COMPILER_IS_GNU OR CMAKE_COMPILER_IS_CLANG)
            add_compile_options(-pg)
            add_link_options(-pg)
        else()
            message(
                FATAL_ERROR
                    "Profile with ${PROFILE} is not supported on this platform (${CMAKE_C_COMPILER_ID})."
            )
        endif()
    else()
        message("Profilers: ${PROFILERS}")
        message(FATAL_ERROR "Profile with ${PROFILE} is not supported.")
    endif()
endif()
