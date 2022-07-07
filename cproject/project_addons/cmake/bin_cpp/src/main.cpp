#include <iostream>
#include <string>

#include <{{PROJECT}}/lib.hpp>

int main(int argc, const char* argv[])
{
    auto const lib = library {};
    auto const message = "Hello from " + lib.name + "!";
    std::cout << message << '\n';
    return 0;
}
