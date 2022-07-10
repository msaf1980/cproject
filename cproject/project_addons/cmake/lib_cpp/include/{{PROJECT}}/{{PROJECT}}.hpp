#pragma once

#include <string>

#include <{{PROJECT}}/{{PROJECT}}_export.hpp>

namespace {{PROJECT}}
{
/**
 * @brief Reports the name of the library
 *
 * Please see the note above for considerations when creating shared libraries.
 */
class {{UC_PROJECT}}_EXPORT {{PROJECT}}
{
  public:
    /**
     * @brief Initializes the name field to the name of the project
     */
    {{PROJECT}}();

    /**
     * @brief Returns a non-owning pointer to the string stored in this class
     */
    const char* name() const;

  private:
    std::string m_name;
};
}  // namespace {{PROJECT}}
