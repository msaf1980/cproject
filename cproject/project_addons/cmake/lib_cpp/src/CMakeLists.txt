# ---- Declare shared library {{PROJECT}} ----

set(
    {{PROJECT}}_{{PROJECT}}_SRC
    main.cpp
)

add_library(
    {{PROJECT}}_{{PROJECT}}
    ${{{PROJECT}}_{{PROJECT}}_SRC}
)
add_library({{PROJECT}}::{{PROJECT}} ALIAS {{PROJECT}}_{{PROJECT}})

include(GenerateExportHeader)
generate_export_header(
    {{PROJECT}}_{{PROJECT}}
    BASE_NAME {{PROJECT}}
    EXPORT_FILE_NAME "${PROJECT_BINARY_DIR}/export/{{PROJECT}}/{{PROJECT}}_export.hpp"
    CUSTOM_CONTENT_FROM_VARIABLE pragma_suppress_c4251
)

if(NOT BUILD_SHARED_LIBS)
  target_compile_definitions({{PROJECT}}_{{PROJECT}} PUBLIC {{UC_PROJECT}}_STATIC_DEFINE)
endif()

set_target_properties(
    {{PROJECT}}_{{PROJECT}} PROPERTIES
    POSITION_INDEPENDENT_CODE ON
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN YES
    VERSION "${VERSION_LIB}"
    SOVERSION "${VERSION_MAJOR}"
    EXPORT_NAME {{PROJECT}}
    OUTPUT_NAME {{PROJECT}}
)

# target_include_directories(
#     {{PROJECT}}_{{PROJECT}}
#     PUBLIC
#     "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>"
# )

target_include_directories(
    {{PROJECT}}_{{PROJECT}} SYSTEM
    PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/export>"
)

#target_compile_features({{PROJECT}}_{{PROJECT}} PUBLIC ${CXX_COMPILE_FEATURES})

# find_package(fmt REQUIRED)
# target_link_libraries({{PROJECT}}_{{PROJECT}} PRIVATE fmt::fmt)

install(
    DIRECTORY ../include/
    "${PROJECT_BINARY_DIR}/export/"
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
    COMPONENT Development
)

install(
    TARGETS {{PROJECT}}_{{PROJECT}}
    EXPORT {{PROJECT}}
    COMPONENT Runtime
    LIBRARY COMPONENT Runtime
    NAMELINK_COMPONENT Development
    ARCHIVE COMPONENT Development
    INCLUDES DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
)

configure_file({{PROJECT}}.pc.in "${PROJECT_BINARY_DIR}/{{PROJECT}}.pc" @ONLY)

install(
    FILES "${PROJECT_BINARY_DIR}/{{PROJECT}}.pc"
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig
    COMPONENT Runtime
)

# ---- Declare shared library {{PROJECT}} ----
