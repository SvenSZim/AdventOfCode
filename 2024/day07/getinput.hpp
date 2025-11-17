#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <utility>
#include <iostream>

typedef std::pair<long, std::vector<long>> equation;

/**
 * @brief Function for converting the input data in data/data.txt into a
 * usable format
 *
 * @returns The input data formatted into two lists of integers
 */
std::vector<equation> parseData(const std::string& filename) {
  std::ifstream infile(filename);

  if (!infile.is_open()) {
    throw std::runtime_error("Error: Cannot open file: " + filename);
  }

  std::vector<equation> equations;

  int lineNumber = 0;

  std::string line;
  while (std::getline(infile, line)) {
    lineNumber++;

    // Skip empty or whitespace-only lines
    if (line.find_first_not_of(" \t\n\r") == std::string::npos)
      continue;

    // Find the colon
    const auto colonPos = line.find(':');
    if (colonPos == std::string::npos) {
      throw std::runtime_error(
        "Error: Missing ':' on line " + std::to_string(lineNumber)
      );
    }

    // ---- Parse the key (left side) ----
    std::string keyStr = line.substr(0, colonPos);
    std::stringstream keyStream(keyStr);

    long key;
    if (!(keyStream >> key) || !(keyStream.eof())) {
      throw std::runtime_error(
        "Error: Invalid key on line " + std::to_string(lineNumber)
      );
    }

    // ---- Parse the list of integers (right side) ----
    std::string valuesStr = line.substr(colonPos + 1);  // skip ':'
    std::stringstream valStream(valuesStr);

    std::vector<long> values;
    long value;

    while (valStream >> value) {
      values.push_back(value);
    }

    // Detect invalid trailing characters
    if (!valStream.eof()) {
      throw std::runtime_error(
        "Error: Invalid value on line " + std::to_string(lineNumber)
      );
    }

    equations.emplace_back(key, std::move(values));
  }
  return equations;
}
