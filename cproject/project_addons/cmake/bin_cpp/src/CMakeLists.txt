#----------------- Executable target {{PROJECT}}_exe --------------------------------
set(
    {{PROJECT}}_LIBS
    ${OPTS_APP_LIBS}
)

set(
    {{PROJECT}}_SRC
    main.cpp
)

add_executable({{PROJECT}}_exe ${{{PROJECT}}_SRC})
add_executable({{PROJECT}}::exe ALIAS {{PROJECT}}_exe)

set_target_properties(
    {{PROJECT}}_exe PROPERTIES
    OUTPUT_NAME {{PROJECT}}
    EXPORT_NAME {{PROJECT}}_exe
)

#target_compile_features({{PROJECT}}_exe PRIVATE ${CXX_COMPILE_FEATURES})
target_link_libraries({{PROJECT}}_exe PRIVATE ${{{PROJECT}}_LIBS})

install(
    TARGETS {{PROJECT}}_exe
    COMPONENT Runtime
)

#----------------- Executable target {{PROJECT}}_exe --------------------------------
