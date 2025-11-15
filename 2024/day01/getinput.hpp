#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <utility>
#include <iostream>

typedef std::pair<std::vector<int>,std::vector<int>> ListPair;

/**
 * @brief Function for converting the input data in data/data.txt into a
 * usable format
 *
 * @returns The input data formatted into two int-lists stored in ListPair
 */
ListPair readListsFromFile(const std::string& filename) {
  ListPair result;
  std::ifstream infile(filename);

  if (!infile.is_open()) {
    throw std::runtime_error("Error: Cannot open file: " + filename);
  }

  std::string line;
  int lineNumber = 0;

  while (std::getline(infile, line)) {
    lineNumber++;

      // Skip empty or whitespace-only lines
    if (line.find_first_not_of(" \t\n\r") == std::string::npos)
      continue;

    std::stringstream ss(line);
    int a, b;

    if (!(ss >> a >> b)) {
      throw std::runtime_error(
        "Error: Invalid or incomplete data at line " + std::to_string(lineNumber)
      );
    }

    // Check for trailing junk (like extra numbers or characters)
    std::string leftover;
    if (ss >> leftover) {
      throw std::runtime_error(
        "Error: Extra data found at line " + std::to_string(lineNumber)
      );
    }
    result.first.emplace_back(a);
    result.second.emplace_back(b);
  }

  return result;
}
