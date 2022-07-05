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

macro(add_compile_options_cxx)
    add_compile_options($<$<COMPILE_LANGUAGE:CXX>:${ARGN}>)
endmacro()

macro(add_compile_options_c)
    add_compile_options($<$<COMPILE_LANGUAGE:C>:${ARGN}>)
endmacro()
