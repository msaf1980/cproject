set(PROFILERS_LIST "gperftools" "prof" "gprof")

list(JOIN PROFILERS_LIST " " PROFILERS)

set(PROFILE
    ""
    CACHE STRING "Enable profiler. Options are: ${PROFILERS}"
)

if(PROFILE)
    string(TOLOWER "${PROFILE}" PROFILE_l)
    if(PROFILE_l STREQUAL "gperftools")
        if(CMAKE_COMPILER_IS_GNU OR CMAKE_COMPILER_IS_CLANG)
            add_exe_linker_flag("-lprofiler")
        else()
            message(
                FATAL_ERROR
                    "Profile with ${PROFILE} is not supported on this platform (${CMAKE_C_COMPILER_ID})."
            )
        endif()
    elseif(PROFILE_l STREQUAL "prof")
        if(CMAKE_COMPILER_IS_GNU OR CMAKE_COMPILER_IS_CLANG)
            add_compile_options(-p)
            add_exe_linker_flag("-p")
        else()
            message(
                FATAL_ERROR
                    "Profile with ${PROFILE} is not supported on this platform (${CMAKE_C_COMPILER_ID})."
            )
        endif()
    elseif(PROFILE_l STREQUAL "gprof")
        if(CMAKE_COMPILER_IS_GNU OR CMAKE_COMPILER_IS_CLANG)
            add_compile_options(-pg)
            add_exe_linker_flag("-pg")
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
