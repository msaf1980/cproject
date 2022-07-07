# `cproject` - The CMake project initializer (but not only, can be extended to any templated projects)

`cproject` is an CMake project initializer that generates CMake projects

## Features

* Be simple to use  
[TODO]  The script allows you to just mash enter to get you a correctly set up
  project for an executable. You want a header-only library? Choose `h` when
  prompted. Static/shared library? Just choose `s` when prompted. Simple
  **and** correct!
* Create [`FetchContent`][1] ready projects  
[TODO]  This is important, because in the near feature this might allow CMake to
  consume other projects in a trivial fashion similar to other languages.
* Cleanly separate developer and consumer build configurations 
  This ties into the previous point as well, but developers and consumers of a
  project have different needs, and separating targets achieves that goal. A
  developer should be able to run tests (with or without profile/sanitizer),
  add warning flags, run benchmarks,   etc., while a consumer, generally only wants to
  build the library or the executable itself.
* Use modern CMake (3.14+)  
* Make usage of tools easy  
  [TODO] Code coverage (gcov), code linting and formatting (clang-format), static
  analysis (clang-tidy) and dynamic analysis (sanitizers, valgrind) are all
  very helpful ways to guide the developer in creating better software, so they
  should be easy to use.
* [TODO] Integrate with package managers (conan, vcpkg, CPM, cget).

## Non-goals

* Allow to modify project structure with add custom targets. Default project structure is from 'Modern Cmake' book
```
- project
  - .gitignore
  - README.md
  - LICENCE.md
  - CMakeLists.txt
  - cmake
    - FindSomeLib.cmake
    - something_else.cmake
  - include
    - project
      - lib.hpp
  - src
    - CMakeLists.txt
    - lib.cpp
  - apps
    -  CMakeLists.txt
    - app.cpp
  - tests
    - CMakeLists.txt
    - testlib.cpp
  - docs
    - CMakeLists.txt
  - extern
    - googletest
  - scripts
    - helper.py
```    
* Generate files and show tips for websites other than GitHub  
  [TODO] While I understand the people who are against GitHub (and by proxy
  Microsoft), it's by far the most used website of its kind, the files and
  messages specific to it are small in number, and they are easily adapted for
  any other service.

## Install

Make sure you have these programs installed:

* Python 3.6 or newer
* CMake 3.14 or newer
* git
* [clang-tidy](#clang-tidy) (optional)
* [cppcheck](#cppcheck) (optional)
* [Doxygen < 1.9](#doxygen) (optional)
* [LCOV](#lcov) (optional)
* [clang-format 12](#clang-format) (optional)
* [codespell](#codespell) (optional)
* [Package managers](#package-managers): Conan or vcpkg (optional)

---
**NOTE**

Some of these tools can be used on Windows as well if you want to use Visual
Studio, but you have to install these addins:

- https://clangpowertools.com/
- https://github.com/VioletGiraffe/cppcheck-vs-addin

---

This package is available for download from [PyPI][16]. You can install this
package using `pip`:

[TODO]
```bash
pip install  cproject
```

### clang-tidy

[clang-tidy][5] is a static analysis tool that helps you spot logical errors in
your code before it is compiled. This script gives you the option to inherit
the `clang-tidy` preset in your `dev` preset, enabling the CMake integration
for this tool.

CI will always run clang-tidy for you, so it is entirely optional to install
and use it locally, but it is recommended.

**For Windows users**, if you wish to use clang-tidy, then you must install
[Ninja][6] and set the `generator` field in your `dev` preset to `Ninja`. The
reason for this is that only [Makefiles and Ninja][7] are supported with CMake
for use with clang-tidy. For other generators, this feature is a no-op.

### cppcheck

[cppcheck][8] is a static analysis tool similar to clang-tidy, however the
overlap in what they detect is minimal, so it's beneficial to use both of them.
This script gives you the option to inherit the `cppcheck` preset in your `dev`
preset, enabling the CMake integration for this tool.

CI will always run cppcheck for you, so it is entirely optional to install and
use it locally, but it is recommended.

**For Windows users**, if you wish to use cppcheck, then you must install
[Ninja][6] and set the `generator` field in your `dev` preset to `Ninja`. The
reason for this is that only [Makefiles and Ninja][9] are supported with CMake
for use with cppcheck. For other generators, this feature is a no-op.

### Doxygen

[Doxygen][11] is a tool to generate documentation from annotated source code.
In conjunction with it, [m.css][12] is used for presenting the generated
documentation.

The generated projects will have a `docs` target in developer mode, which can
be used to build the documentation into the `<binary-dir>/docs/html` directory.

After Doxygen is installed, please make sure the `doxygen` executable exists in
the `PATH`, otherwise you might get confusing error messages.

This documentation can be deployed to GitHub Pages using the `docs` job in the
generated CI workflow. Follow the comments left in the job to enable this.

**NOTE**: m.css does not work with Doxygen >= 1.9. You can install 1.8.20 to
use the `docs` target. See issues [#41][19] and [#48][20].

### LCOV

[LCOV][13] is a tool to process coverage info generated by executables that
were instrumented with GCC's `gcov`. This coverage info can be used to see what
parts of the program were executed.

The generated projects will have a `coverage` target in developer mode if the
`ENABLE_COVERAGE` variable is enabled. The reason why a separate target is used
instead of CTest's built-in `coverage` step is because it lacks necessary
customization. This target should be run after the tests and by default it will
generate a report at `<binary-dir>/coverage.info` and an HTML report at the
`<binary-dir>/coverage_html` directory.

[TODO]
**For Windows users**, you may use a similar tool called [OpenCppCoverage][17],
for which there is an example script in the generated `cmake` directory. This
script is left as an example, because the Linux VM launches and runs faster in
GitHub Actions and so it is used for coverage submission.

### clang-format

[clang-format][14] is part of the LLVM tool suite similar to
[clang-tidy](#clang-tidy). It's a code linter and code formatter, which can be
used to enforce style guides.

Two targets are made available to check and fix code in developer mode using
the `format-check` and `format-fix` targets respectively.

**NOTE**: the project generates files that are formatted according to
clang-format 12. Newer or older versions may format the project differently.

### codespell

[codespell][15] is a tool to find and fix spelling errors mainly in source
code.

Two targets are made available to check and fix spelling errors in developer
mode using the `spell-check` and `spell-fix` targets respectively.

### Package managers
[TODO]
The `-p` flag can be used to select a package manager for the project.
Arguments for the flag can be:

* `none`: no package manager integration (default)
* `conan`: [Conan][21] integration
* `vcpkg`: [vcpkg][22] integration

Make sure to read the generated HACKING document to see what needs to be done
to fetch dependencies.

## Usage

[TODO]
* `cproject [--c] <path>`  
  This command will create a CMake project at the provided location and
  according to the answers given to the prompts. You may pass the `-s`, `-e` or
  `-h` flags after to quickly create a shared library, executable or a header
  only library respectively. The `--c` switch will set the generated project's
  type to C instead of C++.
* `cproject --vcpkg <name>`  
  Generate a vcpkg port with the provided name in the `ports` directory to make
  consuming dependencies not in any central package manager's repository
  easier. This command must be run in a CMake project root tracked by git. See
  the vcpkg example at the top of the README for more details.
* `cproject --help`  
  Shows the help screen for more flags and switches.
