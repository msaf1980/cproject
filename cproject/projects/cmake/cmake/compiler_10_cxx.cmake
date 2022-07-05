if(COMPILER_CONVERSION_WARNINGS)
    if(CMAKE_COMPILER_IS_GNU OR CMAKE_COMPILER_IS_CLANG)
        add_compile_options(-Wconversion)
    else()
        message(WARNING "Cannot check conversion on non GCC/Clang compilers, use ENABLE_ALL_WARNINGS.")
    endif()
endif()

if(COMPILER_ALL_WARNINGS)
    if(CMAKE_COMPILER_IS_GNU OR CMAKE_COMPILER_IS_CLANG)
        add_compile_options(-Wall -Wextra)
    elseif(CMAKE_COMPILER_IS_MSVC)
        add_compile_options(/W4)
    endif()
endif()

if(COMPILER_WARNINGS_AS_ERROR)
    if(CMAKE_COMPILER_IS_GNU OR CMAKE_COMPILER_IS_CLANG)
        add_compile_options(-Werror)
    elseif(CMAKE_COMPILER_IS_MSVC)
        add_compile_options(/WX)
    endif()
endif()

if(COMPILER_REQUIRE_ISO_CXX)
    if(CMAKE_COMPILER_IS_GNU OR CMAKE_COMPILER_IS_CLANG)
        add_c_compiler_flag("-Wpedantic")
        add_cxx_compiler_flag("-Wpedantic")
    else()
        message(WARNING "Cannot check ISO C/C++ on non GCC/Clang compilers.")
    endif()
endif()

if(COMPILER_EFFECTIVE_CXX)
    if(CMAKE_COMPILER_IS_GNU OR CMAKE_COMPILER_IS_CLANG)
        add_cxx_compiler_flag("-Weffc++")
    endif()
endif()

if(COMPILER_HEADER_DEPENDENCY_DATA)
    if(CMAKE_COMPILER_IS_GNU OR CMAKE_COMPILER_IS_CLANG)
        add_compile_options(-MD)
    else()
        message(WARNING "Cannot generate header dependency on non GCC/Clang compilers.")
    endif()
endif()