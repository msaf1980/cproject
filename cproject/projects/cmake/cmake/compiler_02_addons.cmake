function(check_arg args _arg _result)
    if("${args}" STREQUAL "${arg}")
        set(${_result}
            1
            PARENT_SCOPE
        )
    elseif("${args}" MATCHES "^([.*] )+${arg}( [.*])+$")
        set(${_result}
            1
            PARENT_SCOPE
        )
    else()
        set(${_result}
            0
            PARENT_SCOPE
        )
    endif()
endfunction()

macro(enable_compiler_debuginfo)
    if(DEBUGINFO)
        string(FIND CMAKE_CXX_FLAGS "-g" res)
        if(res EQUAL -1)
            set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")
        endif(res EQUAL -1)
        string(FIND CMAKE_C_FLAGS "-g" res)
        if(res EQUAL -1)
            set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -g")
        endif(res EQUAL -1)
    endif()
endmacro()

macro(add_cxx_compiler_flag)
    foreach(arg IN ITEMS ${ARGN})
        check_arg("${CMAKE_CXX_FLAGS}" "${arg}" _result)
        if(_result EQUAL 0)
            set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${arg}")
        endif()
    endforeach()
endmacro()

macro(add_c_compiler_flag)
    foreach(arg IN ITEMS ${ARGN})
        check_arg("${CMAKE_C_FLAGS}" "${arg}" _result)
        if(_result EQUAL 0)
            set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${arg}")
        endif()
    endforeach()
endmacro()

macro(add_exe_linker_flag)
    foreach(arg IN ITEMS ${ARGN})
        check_arg("${CMAKE_EXE_LINKER_FLAGS}" "${arg}" _result)
        if(_result EQUAL 0)
            set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${arg}")
        endif()
    endforeach()
endmacro()
