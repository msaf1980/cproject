if(BUILD_TESTING)
    if(NOT DOCTEST_VERSION)
        set(DOCTEST_VERSION "2.4.9")
    endif()

    include(FetchContent)

    FetchContent_Declare(
        Doctest
        GIT_REPOSITORY https://github.com/doctest/doctest.git
        GIT_TAG v${DOCTEST_VERSION}
    )

    FetchContent_GetProperties(Doctest)
    if(NOT Doctest_POPULATED)
        FetchContent_MakeAvailable(Doctest)
    endif()
endif()
