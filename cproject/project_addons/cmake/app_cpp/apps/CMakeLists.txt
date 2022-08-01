#----------------- Executable target {{PROJECT}}_exe --------------------------------
set(
    {{PROJECT}}_LIBS
    ${OPTS_APP_LIBS}
)

add_executable({{PROJECT}}_app main.cpp)
add_executable({{PROJECT}}::app ALIAS {{PROJECT}}_app)

set_target_properties(
    {{PROJECT}}_app PROPERTIES
    OUTPUT_NAME {{PROJECT}}_app
    EXPORT_NAME {{PROJECT}}_app
)

#target_compile_features({{PROJECT}}_app PRIVATE ${CXX_COMPILE_FEATURES})
target_link_libraries({{PROJECT}}_app PRIVATE ${{{PROJECT}}_LIBS})

install(
    TARGETS {{PROJECT}}_app
    COMPONENT Runtime
)

#----------------- Executable target {{PROJECT}}_exe --------------------------------
