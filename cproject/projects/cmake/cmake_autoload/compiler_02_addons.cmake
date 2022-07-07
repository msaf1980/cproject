macro(add_compile_options_cxx)
    add_compile_options($<$<COMPILE_LANGUAGE:CXX>:${ARGN}>)
endmacro()

macro(add_compile_options_c)
    add_compile_options($<$<COMPILE_LANGUAGE:C>:${ARGN}>)
endmacro()

macro(add_compile_debuginfo)
    add_compile_options(-g)
endmacro()
