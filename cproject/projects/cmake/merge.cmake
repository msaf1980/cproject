# Link application targets with this libs for use enabled options like 'PROFILE=gperftools' or other than require link with libraries
set(OPTS_APP_LIBS)
# Link test application targets with this libs for use enabled options
set(OPTS_TEST_LIBS)

if(PROFILE AND PROFILE_LIB)
    set(OPTS_APP_LIBS ${OPTS_APP_LIBS} ${PROFILE_LIB})
    set(OPTS_TEST_LIBS ${OPTS_TEST_LIBS} ${PROFILE_LIB})
endif()

if(SANITIZER AND SANITIZER_LIBS)
    set(OPTS_APP_LIBS ${OPTS_APP_LIBS} ${SANITIZER_LIBS})
    set(OPTS_TEST_LIBS ${OPTS_TEST_LIBS} ${SANITIZER_LIBS})
endif()
