option(COMPILER_ALL_WARNINGS "Compile with all warnings for the major compilers" OFF)
option(COMPILER_CONVERSION_WARNINGS "Compile with conversion warnings for the major compilers" OFF)
option(COMPILER_WARNINGS_AS_ERROR "Make all warnings into errors" OFF)
option(COMPILER_EFFECTIVE_CXX "Enable Effective C++ warnings" OFF)
option(COMPILER_REQUIRE_ISO_CXX "Require ISO C/C++" OFF)

option(DEBUGINFO "Add compiler debuginfo" OFF)


set(STDLIBS_LIST
    "libc++"
)
list(JOIN STDLIBS_LIST " " STDLIBS)
set(LINK_STDLIB
    ""
    CACHE STRING "Use libc++ as c/c++ standart library. Options are: ${STDLIBS}"
)

if(LINK_STDLIB)
    if(NOT LINK_STDLIB IN_LIST STDLIBS_LIST)
        message(STATUS "LINK_STDLIB options can be set to: ${STDLIBS}")
        message(FATAL_ERROR "Can't link with: ${LINK_STDLIB}")
    endif()
    add_link_options(-stdlib=${LINK_STDLIB})
endif()


