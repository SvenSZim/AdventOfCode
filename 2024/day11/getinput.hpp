#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <utility>
#include <iostream>
#include <unordered_map>

typedef std::unordered_map<std::string,long> data;

/**
 * @brief Function for converting the input data in data/data.txt into a
 * usable format
 *
 * @returns The input data formatted into dictionary mapping the string (label of stone)
 * to the number of stones having that label.
 */
data parseData(const std::string& filename) {
  data result;

  std::string line;
  std::ifstream infile(filename);

  if (!infile.is_open()) {
    throw std::runtime_error("Error: Cannot open file: " + filename);
  }

  int lineNumber = 0;

  while (std::getline(infile, line)) {
    lineNumber++;

    // Skip empty or whitespace-only lines
    if (line.find_first_not_of(" \t\n\r") == std::string::npos)
      continue;
    
    std::stringstream ss(line);
    std::string value;
    while (ss >> value) {
      if (result.count(value) == 0)
        result[value] = 0L;
      result[value]++;
    }
  }
  return result;
}
