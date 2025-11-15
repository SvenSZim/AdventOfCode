#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <utility>
#include <iostream>

typedef std::pair<int, int> rule;
typedef std::vector<int> list;
typedef std::pair<std::vector<rule>, std::vector<list>> rulesNlists;

/**
 * @brief Function for converting the input data in data/data.txt into a
 * usable format
 *
 * @returns The input data formatted into two lists of integers
 */
rulesNlists parseFile(const std::string& filename) {
  std::vector<rule> rules;
  std::vector<list> lists;
  
  std::ifstream infile(filename);

  if (!infile.is_open()) {
    throw std::runtime_error("Error: Cannot open file: " + filename);
  }

  int lineNumber = 0;

  bool readrules = true;
  std::string line;
  while (std::getline(infile, line)) {
    lineNumber++;

    // Skip empty or whitespace-only lines
    if (line.find_first_not_of(" \t\n\r") == std::string::npos) {
      if (readrules) readrules = false;
      continue;
    }

    if (readrules) {
      int separator = line.find_first_of("|");
      std::string firstnum = line.substr(0, separator);
      std::string secondnum = line.substr(separator+1, line.size());
      if (std::all_of(firstnum.begin(), firstnum.end(), ::isdigit) &&
          std::all_of(secondnum.begin(), secondnum.end(), ::isdigit)) {
        rules.push_back({std::stoi(firstnum), std::stoi(secondnum)});
      } else {
        throw std::runtime_error(
          "Error: Cannot parse rule: " + line + " (" + std::to_string(lineNumber) + ")"
        );
      }
    } else {
      for (char &c : line) {
        if (c == ',') c = ' ';
      }

      std::stringstream ss(line);
      list l;
      int value;
      while (ss >> value)
        l.push_back(value);
      
      if (!ss.eof()) {
        throw std::runtime_error(
          "Error: Invalid data on line " + line + " (" + std::to_string(lineNumber) + ")"
        );
      }

      lists.push_back(std::move(l));
    }
  }
  return {rules, lists};
}
