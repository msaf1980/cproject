include_directories("${doctest_SOURCE_DIR}/doctest")
#----------------- Test target {{PROJECT}}_test --------------------------------
set(
    {{PROJECT}}_TEST_LIBS
    # {{PROJECT}}::{{PROJECT}}
    ${OPTS_TEST_LIBS}
)

add_executable({{PROJECT}}_test {{PROJECT}}_test.cpp)
add_executable({{PROJECT}}::test ALIAS {{PROJECT}}_test)

set_target_properties(
    {{PROJECT}}_test PROPERTIES
    OUTPUT_NAME test_{{PROJECT}}
)

#target_compile_features({{PROJECT}}_test PRIVATE ${CXX_COMPILE_FEATURES})
target_link_libraries({{PROJECT}}_test PRIVATE ${{{PROJECT}}_TEST_LIBS})

add_test(NAME {{PROJECT}}_test COMMAND $<TARGET_FILE:{{PROJECT}}_test>)

# set_tests_properties({{PROJECT}}_test PROPERTIES DEPENDS {{PROJECT}})

#----------------- Test target {{PROJECT}}_test --------------------------------
