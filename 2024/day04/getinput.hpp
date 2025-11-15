#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <utility>
#include <iostream>

typedef std::string string;
typedef std::vector<string> StrList;

/**
 * @brief Function for converting the input data in data/data.txt into a
 * usable format
 *
 * @returns The input data formatted into two lists of integers
 */
StrList readStringsFromFile(const string& filename) {
  StrList result;
  std::ifstream infile(filename);

  if (!infile.is_open()) {
    throw std::runtime_error("Error: Cannot open file: " + filename);
  }

  int lineNumber = 0;

  string line;
  while (std::getline(infile, line)) {
    lineNumber++;

    // Skip empty or whitespace-only lines
    if (line.find_first_not_of(" \t\n\r") == string::npos)
      continue;

    result.push_back(line);
  }
  return result;
}
