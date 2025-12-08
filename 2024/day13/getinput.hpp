#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <utility>
#include <iostream>
#include <regex>

typedef std::vector<std::vector<int>> data;

/**
 * @brief Function for converting the input data in data/data.txt into a
 * usable format
 *
 * @returns The input data formatted into a list of list of integer
 */
data parseData(const std::string& filename) {
  data result;

  std::string line;
  std::ifstream infile(filename);

  if (!infile.is_open()) {
    throw std::runtime_error("Error: Cannot open file: " + filename);
  }

  std::regex numsearch(R"(\d+)");
  std::smatch match;

  int lineNumber = 0;
  std::vector<int> newmachine;

  while (std::getline(infile, line)) {
    lineNumber++;

    // Skip empty or whitespace-only lines
    if (line.find_first_not_of(" \t\n\r") == std::string::npos) {
      if (newmachine.size() > 0)
        result.emplace_back(newmachine);
      newmachine = {};
      continue;
    }
    while (std::regex_search(line, match, numsearch)) {
      newmachine.emplace_back(std::stoi(match.str()));
      line = match.suffix();
    }
  }
  if (newmachine.size() > 0)
    result.emplace_back(newmachine);
  return result;
}
