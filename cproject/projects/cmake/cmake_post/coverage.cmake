option(COVERAGE "Enable test coverage" OFF)


# Reports stored in ${CMAKE_BINARY_DIR}/coverage directory, old report saved in ${CMAKE_BINARY_DIR}/coverage.old
# In example, Ninja is used (not required) 
################################################################
# mkdir _build
# cd _build
# cmake -D COVERAGE=ON -DCMAKE_BUILD_TYPE=Debug -DBUILD_TESTING=ON -G Ninja ..
# cmake --build .
# cmake --build . --target coverage-zero
# ctest
# cmake --build . --target coverage
################################################################

if(COVERAGE)
    set(LCOV_EXCLUDE_COVERAGE)

    if(CMAKE_COMPILER_IS_GNU OR CMAKE_COMPILER_IS_CLANG)
        # add_compile_options(-fprofile-arcs -ftest-coverage)
        add_compile_options(--coverage)
        # add_link_options(-fprofile-arcs -ftest-coverage)
        add_link_options(--coverage)
    else()
        message(WARNING "Cannot enable test coverage on non GCC/Clang compilers.")
    endif()

    include(FindPackageHandleStandardArgs)

    # work around CMP0053, see http://public.kitware.com/pipermail/cmake/2014-November/059117.html
    set(PROGRAMFILES_x86_ENV "PROGRAMFILES(x86)")

    find_program(
        lcov_EXECUTABLE
        NAMES lcov
        PATHS "${LCOV_DIR}" "$ENV{LCOV_DIR}" "$ENV{PROGRAMFILES}/lcov"
              "$ENV{${PROGRAMFILES_x86_ENV}}/lcov"
    )

    find_program(
        genhtml_EXECUTABLE
        NAMES genhtml
        PATHS "${LCOV_DIR}" "$ENV{LCOV_DIR}" "$ENV{PROGRAMFILES}/lcov"
              "$ENV{${PROGRAMFILES_x86_ENV}}/lcov"
    )

    find_package_handle_standard_args(
        lcov
        FOUND_VAR lcov_FOUND
        REQUIRED_VARS lcov_EXECUTABLE genhtml_EXECUTABLE
    )

    mark_as_advanced(lcov_EXECUTABLE genhtml_EXECUTABLE)

    if(NOT TARGET coverage-zero)
        add_custom_target(
            coverage-zero
            COMMAND ${CMAKE_COMMAND} -E remove -f ${CMAKE_BINARY_DIR}/coverage
            WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        )
        add_custom_target(
            coverage-report-rm
            COMMAND ${CMAKE_COMMAND} -E rm -rf ${CMAKE_BINARY_DIR}/coverage
            WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        )

        add_custom_target(
            coverage-capture
            COMMAND ${lcov_EXECUTABLE} --capture --no-external --base-directory ${CMAKE_BINARY_DIR}
                    --directory ${CMAKE_SOURCE_DIR} --output-file ${CMAKE_BINARY_DIR}/coverage.info
            WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
            BYPRODUCTS ${CMAKE_BINARY_DIR}/coverage.info
        )

        add_custom_target(
            coverage-filter
            COMMAND
                ${lcov_EXECUTABLE} --base-directory ${CMAKE_BINARY_DIR} --directory
                ${CMAKE_SOURCE_DIR} --remove ${CMAKE_BINARY_DIR}/coverage.info
                ${LCOV_EXCLUDE_COVERAGE} --output-file ${CMAKE_BINARY_DIR}/coverage-filtered.info
            WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
            BYPRODUCTS ${CMAKE_BINARY_DIR}/coverage-filtered.info
        )

        add_custom_target(
            coverage-report
            COMMAND ${CMAKE_COMMAND} -E rename ${CMAKE_BINARY_DIR}/coverage ${CMAKE_BINARY_DIR}/coverage.old || true
            COMMAND
                ${genhtml_EXECUTABLE} --output-directory ${CMAKE_BINARY_DIR}/coverage --title
                "${META_PROJECT_NAME} Test Coverage" --num-spaces 4
                ${CMAKE_BINARY_DIR}/coverage-filtered.info
            WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
            DEPENDS ${CMAKE_BINARY_DIR}/coverage-filtered.info
        )

        add_dependencies(coverage-filter coverage-capture)
        add_dependencies(coverage-report coverage-filter)
        add_custom_target(coverage DEPENDS coverage-report)
    endif()
endif()
