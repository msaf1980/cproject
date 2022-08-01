include(GoogleTest)

#----------------- Test target {{PROJECT}}_test --------------------------------
set(
    {{PROJECT}}_TEST_LIBS
    # {{PROJECT}}::{{PROJECT}}
    gtest_main
    ${OPTS_TEST_LIBS}
)

set(
    {{PROJECT}}_TEST_SRC
    main_test.cpp
)

add_executable({{PROJECT}}_test ${{{PROJECT}}_TEST_SRC})
add_executable({{PROJECT}}::test ALIAS {{PROJECT}}_test)

set_target_properties(
    {{PROJECT}}_test PROPERTIES
    OUTPUT_NAME test_{{PROJECT}}
)

#target_compile_features({{PROJECT}}_test PRIVATE ${CXX_COMPILE_FEATURES})
target_link_libraries({{PROJECT}}_test PRIVATE ${{{PROJECT}}_TEST_LIBS})

gtest_discover_tests({{PROJECT}}_test)

# set_tests_properties({{PROJECT}}_test PROPERTIES DEPENDS {{PROJECT}})

#----------------- Test target {{PROJECT}}_test --------------------------------
