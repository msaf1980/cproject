set(PROJECT {{PROJECT}})
set(VERSION {{VERSION}})

SET(CXX_STD_VERSION{%if {{ CXX_STD }} %} {{ CXX_STD }}{%endif%})
SET(CXX_STD{%if {{ CXX_STD }} %} -std=c++{{ CXX_STD }}{%endif%})
set(CXX_COMPILE_FEATURES{%if {{ CXX_STD }} %} cxx_std_{{ CXX_STD }}{%endif%})

SET(C_STD_VERSION{%if {{ C_STD }} %} {{ C_STD }}{%endif%})
SET(C_STD{%if {{ C_STD }} %} -std=c{{ C_STD }}{%endif%})
set(C_COMPILE_FEATURES{%if {{ C_STD }} %} c_std_{{ C_STD }}{%endif%})

if(CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
    set(MAIN_PROJECT ON)
    if(DEFINED ENV{DEVENV})
        set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
    endif()
else()
    set(MAIN_PROJECT OFF)
endif()
