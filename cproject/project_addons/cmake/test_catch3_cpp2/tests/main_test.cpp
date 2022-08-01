#include <catch2/catch_test_macros.hpp>

// #include <{{PROJECT}}/{{PROJECT}}.hpp>

unsigned int Factorial(unsigned int number)
{
    return number > 1 ? Factorial(number - 1) * number : 1;
}

TEST_CASE("Factorials are computed", "[factorial]")
{
    REQUIRE(Factorial(1) == 1);
}
