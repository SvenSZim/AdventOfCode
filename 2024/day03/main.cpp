#include <algorithm>
//#include <cctype>
#include <cstdlib>
#include <iostream>
#include <unordered_map>

#include "getinput.hpp"

int solutionToPuzzleOne(const string &convertedData);
int solutionToPuzzleTwo(const string &convertedData);

/**
 * @brief Function used for testing purposes
 */
int main() {
  string convertedData = readStringFromFile("data/data.txt");

  int totalDifference = solutionToPuzzleOne(convertedData);
  std::cout << "Solution to puzzle 1: " << totalDifference << std::endl;

  int totalSimilarityScores = solutionToPuzzleTwo(convertedData);
  std::cout << "Solution to puzzle 2: " << totalSimilarityScores << std::endl;

  return 0;
}

/**
 * @brief returns the solution to the problem stated by AOC2024::day03::1 with
 * the given input data
 *
 * The first problem of the third day of AOC2024 consisted of finding the sum of
 * all valid multiplication operations stated in the corrupted input string.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The difference between the two lists given as input data
 */
int solutionToPuzzleOne(const string &convertedData) {
  int result{0};
  int strlen = convertedData.size();
  for (int stridx{0}; stridx < strlen; stridx++) {
    if (convertedData[stridx] == 'm') {
      // check for start of mul(x,y) block
      if (strlen - stridx < 7) break; // remaining string to short
      if (convertedData[stridx+1] != 'u' ||
          convertedData[stridx+2] != 'l' ||
          convertedData[stridx+3] != '(') continue; // 'm' not followed by 'ul('
      int startidx{stridx+3};
      // search for separator between numbers ','
      int commaidx{1};
      for (; startidx+commaidx < strlen && convertedData[startidx+commaidx] != ','; commaidx++);
      // search for end of block ')'
      int endidx{1};
      for (; startidx+commaidx+endidx < strlen && convertedData[startidx+commaidx+endidx] != ')'; endidx++);
      // check if search reached end of inputstring or comma is next to '(' or ')'
      if (stridx+endidx >= strlen || commaidx == 1 || endidx == 1) continue;
      // check if '()'-block contains only valid numbers separated by ','
      string leftblock = convertedData.substr(startidx+1, commaidx-1);
      string rightblock = convertedData.substr(startidx+commaidx+1, endidx-1);
      if (std::all_of(leftblock.begin(), leftblock.end(), ::isdigit) &&
          std::all_of(rightblock.begin(), rightblock.end(), ::isdigit)) {
        result += std::stoi(leftblock) * std::stoi(rightblock);
        stridx = startidx+commaidx+endidx; // skip used section
      }
    }
  }
  return result;
}

/**
 * @brief returns the solution to the problem stated by AOC2024::day01::2 with
 * the given input data
 *
 * The second problem of the third day of AOC2024 consisted of finding the sum of
 * all enabled valid multiplication operations stated in the corrupted input string.
 * Operations can be enabled/disabled by the do() and don't() operations.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The similarity between the two lists given as input data
 */
int solutionToPuzzleTwo(const string &convertedData) {
  int result{0};
  int strlen = convertedData.size();
  bool enabled = true;
  string enabledSection;
  int lastDoIdx = 0;
  for (int stridx{0}; stridx < strlen; stridx++) {
    if (convertedData[stridx] == 'd') {
      // check for start of do() or don't() block
      if (strlen - stridx < 7) continue; // remaining string to short
      if (convertedData[stridx+1] == 'o' &&
          convertedData[stridx+2] == '(' &&
          convertedData[stridx+3] == ')') {
        if (enabled) continue;
        enabled = true;
        stridx += 4;
        lastDoIdx = stridx;
      } else if (convertedData[stridx+1] == 'o' &&
                 convertedData[stridx+2] == 'n' &&
                 convertedData[stridx+3] == '\'' &&
                 convertedData[stridx+4] == 't' &&
                 convertedData[stridx+5] == '(' &&
                 convertedData[stridx+6] == ')') {
        if (!enabled) continue;
        enabled = false;
        // extract enabled substring and apply solutionToPuzzleOne
        enabledSection = convertedData.substr(lastDoIdx, stridx - lastDoIdx);
        result += solutionToPuzzleOne(enabledSection);
        stridx += 7;
      }
    }
  }
  if (enabled) {
    // if still enabled at end -> apply solutionToPuzzleOne till end
    enabledSection = convertedData.substr(lastDoIdx, strlen - lastDoIdx);
    result += solutionToPuzzleOne(enabledSection);
  }
  return result;
}
