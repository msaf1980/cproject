set(PROJECT {{ PROJECT }})
set(VERSION {{ VERSION }})
set(PROJECT_COMPILE_FEATURES{%if {{ CXX }} %} cxx_std_{{ CXX_STD }}{%endif%}{%if {{ C_STD }} %} c_std_{{ C_STD }}{%endif%})
