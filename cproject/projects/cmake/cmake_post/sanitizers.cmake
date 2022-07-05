set(SANITIZERS_LIST
    "Address"
    "Memory"
    "MemoryWithOrigins"
    "Undefined"
    "Thread"
    "Leak"
    "Address,Undefined"
    "CFI"
)

list(JOIN SANITIZERS_LIST " " SANITIZERS)
  
set(SANITIZER
    ""
    CACHE STRING "Compile with a sanitizer. Options are: ${SANITIZERS}"
)

if(SANITIZER)
    if(NOT SANITIZER IN_LIST SANITIZERS_LIST)
        message("Sanitizers: ${SANITIZERS}")
        message(FATAL_ERROR "This sanitizer not yet supported: ${SANITIZER}")
    endif()

    if(CMAKE_COMPILER_IS_GNU
       OR CMAKE_COMPILER_IS_CLANG
       OR CMAKE_COMPILER_IS_MSVC
    )
        add_c_compiler_flag("-fno-omit-frame-pointer")
        add_cxx_compiler_flag("-fno-omit-frame-pointer")

        if(SANITIZER MATCHES "([Aa]ddress)")
            # Optional: -fno-optimize-sibling-calls -fsanitize-address-use-after-scope
            message(STATUS "Enable Address sanitizer")
            add_c_compiler_flag("-fsanitize=address")
            add_cxx_compiler_flag("-fsanitize=address")
            # add_exe_linker_flag("-lasan" "-lubsan")

            # if(AFL) append_quoteless( AFL_USE_ASAN=1 CMAKE_C_COMPILER_LAUNCHER
            # CMAKE_CXX_COMPILER_LAUNCHER ) endif()
        endif()

        if(SANITIZER MATCHES "([Mm]emory([Ww]ith[Oo]rigins)?)")
            if(CMAKE_COMPILER_IS_MSVC)
                message(
                    FATAL_ERROR
                        "This sanitizer not yet supported in the MSVC environment: ${SANITIZER}"
                )
            endif()
            # Optional: -fno-optimize-sibling-calls -fsanitize-memory-track-origins=2
            add_c_compiler_flag("-fsanitize=memory")
            add_cxx_compiler_flag("-fsanitize=memory")
            if(USE_SANITIZER MATCHES "([Mm]emory[Ww]ith[Oo]rigins)")
                message(STATUS "Enable MemoryWithOrigins sanitizer")
                add_c_compiler_flag("-fsanitize-memory-track-origins")
                add_cxx_compiler_flag("-fsanitize-memory-track-origins")
            else()
                message(STATUS "Enable Memory sanitizer")
            endif()

            # if(AFL) append_quoteless( AFL_USE_MSAN=1 CMAKE_C_COMPILER_LAUNCHER
            # CMAKE_CXX_COMPILER_LAUNCHER ) endif()
        endif()

        if(SANITIZER MATCHES "([Uu]ndefined)")
            if(CMAKE_COMPILER_IS_MSVC)
                message(
                    FATAL_ERROR
                        "This sanitizer not yet supported in the MSVC environment: ${SANITIZER}"
                )
            endif()
            message(STATUS "Enable with Undefined Behaviour sanitizer")
            add_c_compiler_flag("-fsanitize=undefined")
            add_cxx_compiler_flag("-fsanitize=undefined")
            # add_exe_linker_flag("-lubsan")

            # if(EXISTS "${BLACKLIST_FILE}") append("-fsanitize-blacklist=${BLACKLIST_FILE}"
            # SANITIZER_UB_FLAG) endif()

            # if(AFL) append_quoteless( AFL_USE_UBSAN=1 CMAKE_C_COMPILER_LAUNCHER
            # CMAKE_CXX_COMPILER_LAUNCHER ) endif()
        endif()

        if(SANITIZER MATCHES "([Tt]hread)")
            if(CMAKE_COMPILER_IS_MSVC)
                message(
                    FATAL_ERROR
                        "This sanitizer not yet supported in the MSVC environment: ${SANITIZER}"
                )
            endif()
            message(STATUS "Enable Thread sanitizer")
            add_c_compiler_flag("-fsanitize=thread")
            add_cxx_compiler_flag("-fsanitize=thread")
            # add_exe_linker_flag("-ltsan")

            # if(AFL) append_quoteless( AFL_USE_TSAN=1 CMAKE_C_COMPILER_LAUNCHER
            # CMAKE_CXX_COMPILER_LAUNCHER ) endif()
        endif()

        if(SANITIZER MATCHES "([Ll]eak)")
            if(CMAKE_COMPILER_IS_MSVC)
                message(
                    FATAL_ERROR
                        "This sanitizer not yet supported in the MSVC environment: ${SANITIZER}"
                )
            endif()
            message(STATUS "Enable Leak sanitizer")
            add_c_compiler_flag("-fsanitize=leak")
            add_cxx_compiler_flag("-fsanitize=leak")

            # if(AFL) append_quoteless(AFL_USE_LSAN=1 CMAKE_C_COMPILER_LAUNCHER
            # CMAKE_CXX_COMPILER_LAUNCHER) endif()
        endif()

        if(SANITIZER MATCHES "([Cc][Ff][Ii])")
            if(CMAKE_COMPILER_IS_MSVC)
                message(
                    FATAL_ERROR
                        "This sanitizer not yet supported in the MSVC environment: ${SANITIZER}"
                )
            endif()
            message(STATUS "Testing with Control Flow Integrity(CFI) sanitizer")
            add_c_compiler_flag("-fsanitize=cfi")
            add_cxx_compiler_flag("-fsanitize=cfi")

            # if(AFL) append_quoteless(AFL_USE_CFISAN=1 CMAKE_C_COMPILER_LAUNCHER
            # CMAKE_CXX_COMPILER_LAUNCHER) endif()
        endif()
    elseif(NOT CMAKE_COMPILER_IS_GNU AND NOT CMAKE_COMPILER_IS_CLANG)
        message(FATAL_ERROR "SANITIZER is not supported on this platform (${CMAKE_C_COMPILER_ID}).")
    endif()
endif()
