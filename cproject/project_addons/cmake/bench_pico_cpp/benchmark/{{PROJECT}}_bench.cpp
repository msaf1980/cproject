#define PICOBENCH_IMPLEMENT_WITH_MAIN
#include <picobench/picobench.hpp>

// #include <{{PROJECT}}/{{PROJECT}}.hpp>

static void StringCreation(picobench::state& s)
{
    for (auto _ : s)
    {
        std::string empty_string;
    }
}
PICOBENCH(StringCreation);

static void StringCopy(picobench::state& s)
{
    std::string x = "hello";
    for (auto _ : s)
    {
        std::string copy(x);
    }
}

PICOBENCH(StringCopy);
