if(BUILD_TESTING)
    if(NOT GTEST_VERSION)
        set(GTEST_VERSION "1.12.1")
    endif()

    include(FetchContent)

    FetchContent_Declare(
        GTest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG release-${GTEST_VERSION}
    )

    FetchContent_GetProperties(GTest)
    if(NOT GTest_POPULATED)
        # For Windows: Prevent overriding the parent project's compiler/linker settings
        set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
        FetchContent_MakeAvailable(GTest)
    endif()
endif()
