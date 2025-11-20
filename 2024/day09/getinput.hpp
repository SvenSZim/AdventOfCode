#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <utility>
#include <iostream>

/**
 * @brief Function for converting the input data in data/data.txt into a
 * usable format
 *
 * @returns The input data formatted into two lists of integers
 */
std::vector<int> parseData(const std::string& filename) {
  std::vector<int> result;

  std::string line;
  std::ifstream infile(filename);

  if (!infile.is_open()) {
    throw std::runtime_error("Error: Cannot open file: " + filename);
  }

  int lineNumber = 0;

  std::getline(infile, line);
  for (const char &c : line)
    result.emplace_back(c - '0');
  return result;
}
