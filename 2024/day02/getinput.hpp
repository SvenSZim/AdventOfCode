#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <utility>
#include <iostream>

typedef std::vector<std::vector<int>> ListList;

/**
 * @brief Function for converting the input data in data/data.txt into a
 * usable format
 *
 * @returns The input data formatted into a list of lists of integers
 */
ListList readListsFromFile(const std::string& filename) {
  ListList result;
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
    std::vector<int> numbers;
    int value;

    // Read integers until the line ends
    while (ss >> value) {
      numbers.push_back(value);
    }

    // Check for invalid characters (e.g. letters)
    if (!ss.eof()) {
      throw std::runtime_error(
        "Error: Invalid data on line " + std::to_string(lineNumber)
      );
    }

    result.push_back(std::move(numbers));
  }
  return result;
}
