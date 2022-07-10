#include <string>

#include <{{PROJECT}}/{{PROJECT}}.hpp>

{{PROJECT}}::{{PROJECT}}::{{PROJECT}}()
    : m_name("{{PROJECT}}")
{
}

const char* {{PROJECT}}::{{PROJECT}}::name() const
{
  return m_name.c_str();
}
