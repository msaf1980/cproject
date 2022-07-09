set(SANITIZERS_LIST
    "Address"
    "ASan"
    "Memory"
    "MSan"
    "MemoryWithOrigins"
    "MSanWithOrigins"
    "Undefined"
    "UBSan"
    "Thread"
    "TSan"
    "Leak"
    "LSAN"
    "Address,Undefined"
    "ASAN,UBSan"
    "CFI"
    "Valgrind"
)

# For run tests under valgrind:
# ctest -T memcheck
# or run target test_memcheck
# cmake --build . -v --target test_memcheck
# or run target test_memcheck with comfigured backend
# make test_memcheck
# or
# ninja test_memcheck
#
# Also VALGRIND_ENABLED=1 passed

list(JOIN SANITIZERS_LIST " " SANITIZERS)

set(SANITIZER
    ""
    CACHE STRING "Compile with a sanitizer. Options are: ${SANITIZERS}, some of them are aliases, like Address and ASan"
)
string(TOLOWER "${SANITIZER}" SANITIZER_l)
string(TOLOWER "${SANITIZERS_LIST}" SANITIZERS_LIST_l)
if(SANITIZER)
    # Temporary for merge with OPTS_APP_LIBS and OPTS_TEST_LIBS
    set (SANITIZER_LIBS)

    if(NOT SANITIZER_l IN_LIST SANITIZERS_LIST_l)
        message("Sanitizers: ${SANITIZERS}")
        message(FATAL_ERROR "This sanitizer not yet supported: ${SANITIZER}")
    endif()

    if(CMAKE_COMPILER_IS_GNU
       OR CMAKE_COMPILER_IS_CLANG
       OR CMAKE_COMPILER_IS_MSVC
    )
        add_compile_options("-fno-omit-frame-pointer")
        add_compile_debuginfo()

        if(SANITIZER_l MATCHES "(valgrind)")
            find_program(MEMORYCHECK_COMMAND valgrind)
            add_definitions(-DVALGRIND_ENABLED=1)
            set(MEMORYCHECK_SUPPRESS "${PROJECT_SOURCE_DIR}/valgrind_suppress.txt" )
            set(MEMORYCHECK_COMMAND_OPTIONS "--trace-children=yes --leak-check=full --track-origins=yes --show-reachable=yes --error-exitcode=255 --suppressions=${MEMORYCHECK_SUPPRESS}" )
            set(MEMCHECK_LOGFILE memcheck.log)
            add_custom_target(test-valgrind
                COMMAND ctest -O ${MEMCHECK_LOGFILE} -t memcheck
                COMMAND tail -n1 ${MEMCHECK_LOGFILE} | grep 'Memory checking results:' > /dev/null
                COMMAND rm -f ${MEMCHECK_LOGFILE}
                DEPENDS ${DART_CONFIG}
            )
            add_custom_target(test_memcheck
                COMMAND ${CMAKE_CTEST_COMMAND} --force-new-ctest-process -O ${MEMCHECK_LOGFILE} --test-action memcheck
                COMMAND cat ${MEMCHECK_LOGFILE}
                WORKING_DIRECTORY "${CMAKE_BINARY_DIR}"
            )
        endif()

        if(SANITIZER_l MATCHES "(address)" OR SANITIZER_l MATCHES "(asan)")
            # Optional: -fno-optimize-sibling-calls -fsanitize-address-use-after-scope
            message(STATUS "Enable Address sanitizer")
            add_compile_options(-fsanitize=address)
            list(APPEND SANITIZER_LIBS asan)

            # if(AFL) append_quoteless( AFL_USE_ASAN=1 CMAKE_C_COMPILER_LAUNCHER
            # CMAKE_CXX_COMPILER_LAUNCHER ) endif()
        endif()

        if(SANITIZER_l MATCHES "(memory(withorigins)?)" OR SANITIZER_l MATCHES "(msan(withorigins)?)")
            if(CMAKE_COMPILER_IS_MSVC)
                message(
                    FATAL_ERROR
                        "This sanitizer not yet supported in the MSVC environment: ${SANITIZER}"
                )
            endif()
            # Optional: -fno-optimize-sibling-calls -fsanitize-memory-track-origins=2
            add_compile_options(-fsanitize=memory -fPIE -pie)
            if(USE_SANITIZER MATCHES "([Mm]emory[Ww]ith[Oo]rigins)")
                message(STATUS "Enable MemoryWithOrigins sanitizer")
                add_compile_options("-fsanitize-memory-track-origins")
            else()
                message(STATUS "Enable Memory sanitizer")
            endif()

            # if(AFL) append_quoteless( AFL_USE_MSAN=1 CMAKE_C_COMPILER_LAUNCHER
            # CMAKE_CXX_COMPILER_LAUNCHER ) endif()
        endif()

        if(SANITIZER_l MATCHES "(undefined)" OR SANITIZER_l MATCHES "(ubsan)")
            if(CMAKE_COMPILER_IS_MSVC)
                message(
                    FATAL_ERROR
                        "This sanitizer not yet supported in the MSVC environment: ${SANITIZER}"
                )
            endif()
            message(STATUS "Enable with Undefined Behavior sanitizer")
            add_compile_options(-fsanitize=undefined)
            list(APPEND SANITIZER_LIBS ubsan)

            # if(EXISTS "${BLACKLIST_FILE}") append("-fsanitize-blacklist=${BLACKLIST_FILE}"
            # SANITIZER_UB_FLAG) endif()

            # if(AFL) append_quoteless( AFL_USE_UBSAN=1 CMAKE_C_COMPILER_LAUNCHER
            # CMAKE_CXX_COMPILER_LAUNCHER ) endif()
        endif()

        if(SANITIZER_l MATCHES "(thread)" OR SANITIZER_l MATCHES "(tsan)")
            if(CMAKE_COMPILER_IS_MSVC)
                message(
                    FATAL_ERROR
                        "This sanitizer not yet supported in the MSVC environment: ${SANITIZER}"
                )
            endif()
            message(STATUS "Enable Thread sanitizer")
            add_compile_options("-fsanitize=thread")
            list(APPEND SANITIZER_LIBS tsan)

            # if(AFL) append_quoteless( AFL_USE_TSAN=1 CMAKE_C_COMPILER_LAUNCHER
            # CMAKE_CXX_COMPILER_LAUNCHER ) endif()
        endif()

        if(SANITIZER_l MATCHES "(leak)" OR SANITIZER_l MATCHES "(lsan)")
            if(CMAKE_COMPILER_IS_MSVC)
                message(
                    FATAL_ERROR
                        "This sanitizer not yet supported in the MSVC environment: ${SANITIZER}"
                )
            endif()
            message(STATUS "Enable Leak sanitizer")
            add_compile_options("-fsanitize=leak")

            # if(AFL) append_quoteless(AFL_USE_LSAN=1 CMAKE_C_COMPILER_LAUNCHER
            # CMAKE_CXX_COMPILER_LAUNCHER) endif()
        endif()

        if(SANITIZER_l MATCHES "(cfi)")
            if(CMAKE_COMPILER_IS_MSVC)
                message(
                    FATAL_ERROR
                        "This sanitizer not yet supported in the MSVC environment: ${SANITIZER}"
                )
            endif()
            message(STATUS "Testing with Control Flow Integrity(CFI) sanitizer")
            add_compile_options(-fsanitize=cfi -flto -fvisibility=hidden)
            add_link_options(-flto)

            # if(AFL) append_quoteless(AFL_USE_CFISAN=1 CMAKE_C_COMPILER_LAUNCHER
            # CMAKE_CXX_COMPILER_LAUNCHER) endif()
        endif()
    elseif(NOT CMAKE_COMPILER_IS_GNU AND NOT CMAKE_COMPILER_IS_CLANG)
        message(FATAL_ERROR "SANITIZER is not supported on this platform (${CMAKE_C_COMPILER_ID}).")
    endif()
endif()
