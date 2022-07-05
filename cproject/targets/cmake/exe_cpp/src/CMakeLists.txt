add_executable({{ TARGET }}_exe main.cpp)
add_executable({{ TARGET }}::exe ALIAS {{ TARGET }}_exe)

set_target_properties(
    {{ TARGET }}_exe PROPERTIES
    OUTPUT_NAME {{ TARGET }}
    EXPORT_NAME exe
)

set(
    {{ TARGET }}_LIBS
)

target_compile_features({{ TARGET }}_exe PRIVATE ${PROJECT_COMPILE_FEATURES})

target_link_libraries({{ TARGET }}_exe PRIVATE ${{{ TARGET }}_LIBS})

# ---- Install rules ----

# if(NOT CMAKE_SKIP_INSTALL_RULES)
#   include(cmake/install-rules.cmake)
# endif()

# include(cmake/dev-mode.cmake)
