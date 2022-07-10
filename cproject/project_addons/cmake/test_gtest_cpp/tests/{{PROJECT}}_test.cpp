#include <gtest/gtest.h>

// #include <{{PROJECT}}/{{PROJECT}}.hpp>

unsigned int Factorial(unsigned int number)
{
    return number > 1 ? Factorial(number - 1) * number : 1;
}

TEST(FactorialTest, BasicAssertions)
{
    EXPECT_EQ(Factorial(1), 1);
}
