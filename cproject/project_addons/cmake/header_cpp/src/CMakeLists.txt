# ---- Declare header-only library {{PROJECT}} ----

add_library({{PROJECT}}_{{PROJECT}} INTERFACE)
add_library({{PROJECT}}::{{PROJECT}} ALIAS {{PROJECT}}_{{PROJECT}})

set_property(
    TARGET {{PROJECT}}_{{PROJECT}} PROPERTY
    EXPORT_NAME {{PROJECT}}
)

target_include_directories(
    {{PROJECT}}_{{PROJECT}}
    INTERFACE
    "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>"
)

target_compile_features({{PROJECT}}_{{PROJECT}} INTERFACE ${CXX_COMPILE_FEATURES})

# find_package(fmt REQUIRED)
# target_link_libraries({{PROJECT}}_{{PROJECT}} INTERFACE fmt::fmt)

install(
    DIRECTORY include
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
    COMPONENT Development
)

# write_basic_package_version_file(
#     "${package}ConfigVersion.cmake"
#     COMPATIBILITY SameMajorVersion
#     ARCH_INDEPENDENT
# )

# ---- Declare header-only library {{PROJECT}} ----
