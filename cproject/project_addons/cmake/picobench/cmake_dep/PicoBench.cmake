if(BUILD_TESTING)
    if(NOT PICOBENCH_VERSION)
        set(PICOBENCH_VERSION "2.01")
    endif()

    include(FetchContent)

    FetchContent_Declare(
        PicoBench
        GIT_REPOSITORY https://github.com/iboB/picobench.git
        GIT_TAG v${PICOBENCH_VERSION}
    )

    FetchContent_GetProperties(PicoBench)
    if(NOT PicoBench_POPULATED)
        FetchContent_MakeAvailable(PicoBench)
    endif()
endif()
