include_directories("${picobench_SOURCE_DIR}/include")

#----------------- Test target {{PROJECT}}_test --------------------------------
set(
    {{PROJECT}}_BENCH_LIBS
    # {{PROJECT}}::{{PROJECT}}
    ${OPTS_TEST_LIBS}
)

add_executable({{PROJECT}}_bench {{PROJECT}}_bench.cpp)
add_executable({{PROJECT}}::bench ALIAS {{PROJECT}}_bench)

set_target_properties(
    {{PROJECT}}_bench PROPERTIES
    OUTPUT_NAME bench_{{PROJECT}}
)

#target_compile_features({{PROJECT}}_bench PRIVATE ${CXX_COMPILE_FEATURES})
target_link_libraries({{PROJECT}}_bench PRIVATE ${{{PROJECT}}_BENCH_LIBS})

custom_add_bench({{PROJECT}}_bench)

# set_tests_properties({{PROJECT}}_bench PROPERTIES DEPENDS {{PROJECT}})

#----------------- Test target {{PROJECT}}_test --------------------------------
