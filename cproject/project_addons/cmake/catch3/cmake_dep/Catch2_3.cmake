if(BUILD_TESTING)
    if(NOT CATCH2_VERSION)
        set(CATCH2_VERSION "3.0.1")
    endif()

    include(FetchContent)

    FetchContent_Declare(
        Catch2
        GIT_REPOSITORY https://github.com/catchorg/Catch2.git
        GIT_TAG v${CATCH2_VERSION}
    )

    FetchContent_GetProperties(Catch2)
    if(NOT Catch2_POPULATED)
        FetchContent_MakeAvailable(Catch2)
        list(APPEND CMAKE_MODULE_PATH ${catch2_SOURCE_DIR}/contrib)
    endif()
endif()
