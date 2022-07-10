#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include <doctest.h>

unsigned int Factorial(unsigned int number)
{
    return number > 1 ? Factorial(number - 1) * number : 1;
}

TEST_CASE("testing the factorial function")
{
    CHECK(Factorial(1) == 1);
}
