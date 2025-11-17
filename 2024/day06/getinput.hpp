#include <fstream>
#include <sstream>
#include <string>
#include <array>
#include <vector>
#include <utility>
#include <iostream>

typedef std::vector<std::vector<int>> map; 
// datarange: 0b00000 - 0b11110 
// Bit 0: isblocked,
// Bit 1: visited with upmotion,
// Bit 2: visited with downmotion,
// Bit 3: visited with leftmotion,
// Bit 4: visited with rightmotion

/**
 * @brief Function for converting the input data in data/data.txt into a
 * usable format
 *
 * @returns The input data formatted into two lists of integers
 */
map readMapFromFile(const std::string& filename) {
  map result;
  std::ifstream infile(filename);

  if (!infile.is_open()) {
    throw std::runtime_error("Error: Cannot open file: " + filename);
  }

  int lineNumber = 0;

  std::string line;
  while (std::getline(infile, line)) {
    lineNumber++;

    // Skip empty or whitespace-only lines
    if (line.find_first_not_of(" \t\n\r") == std::string::npos)
      continue;
    
    std::vector<int> newrow;

    for (const char c : line) {
      switch (c) {
      case '.':
        newrow.push_back(0);
        break;
      case '#':
        newrow.push_back(1);
        break;
      case '^':
        newrow.push_back(2);
        break;
      case 'v':
        newrow.push_back(4);
        break;
      case '<':
        newrow.push_back(8);
        break;
      case '>':
        newrow.push_back(16);
        break;
      default:
        throw std::runtime_error("Invalid char: " + std::to_string(c) + " in line " + std::to_string(lineNumber));
        break;
      }
    }

    result.push_back(newrow);
  }
  return result;
}
