if(BUILD_BENCH)
    if(NOT TARGET bench)
        add_custom_target(bench)
    endif()

    # Add benchmark to  bench target
    function(custom_add_bench targetname)
        add_custom_target(
            ${targetname}_run
            COMMAND "$<TARGET_FILE:${targetname}>"
            COMMENT "Running benchmark ${targetname}")
        add_dependencies(${targetname}_run ${targetname})
        add_dependencies(bench ${targetname}_run)
    endfunction()
endif()
