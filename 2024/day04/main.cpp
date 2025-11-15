#include <algorithm>
//#include <cctype>
#include <cstdlib>
#include <iostream>
#include <unordered_map>

#include "getinput.hpp"

int solutionToPuzzleOne(const StrList &convertedData);
int solutionToPuzzleTwo(const StrList &convertedData);

/**
 * @brief Function used for testing purposes
 */
int main() {
  StrList convertedData = readStringsFromFile("data/data.txt");

  int totalDifference = solutionToPuzzleOne(convertedData);
  std::cout << "Solution to puzzle 1: " << totalDifference << std::endl;

  int totalSimilarityScores = solutionToPuzzleTwo(convertedData);
  std::cout << "Solution to puzzle 2: " << totalSimilarityScores << std::endl;

  return 0;
}

/**
 * @brief returns the solution to the problem stated by AOC2024::day04::1 with
 * the given input data
 *
 * The first problem of the fourth day of AOC2024 consisted of finding the amount
 * of XMAS words in the crossword puzzle.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The difference between the two lists given as input data
 */
int solutionToPuzzleOne(const StrList &convertedData) {
  int height = convertedData.size();
  if (height == 0) return 0;
  
  int width = convertedData[0].size();
  for (string line : convertedData) {
    if (line.size() < width) width = line.size();
  }

  int result{0};
  for (int h{0}; h < height; h++) {
    for (int w{0}; w < width; w++) {
      if (convertedData[h][w] != 'X') continue;

      // check which directions are available
      bool up = h > 2, down = h < height-3;
      bool left = w > 2, right = w < width-3;
      if (up) {
        if (convertedData[h-1][w] == 'M' &&
            convertedData[h-2][w] == 'A' &&
            convertedData[h-3][w] == 'S')
          result++;
        if (left &&
            convertedData[h-1][w-1] == 'M' &&
            convertedData[h-2][w-2] == 'A' &&
            convertedData[h-3][w-3] == 'S')
          result++;
        if (right &&
            convertedData[h-1][w+1] == 'M' &&
            convertedData[h-2][w+2] == 'A' &&
            convertedData[h-3][w+3] == 'S')
          result++;
      }
      if (down) {
        if (convertedData[h+1][w] == 'M' &&
            convertedData[h+2][w] == 'A' &&
            convertedData[h+3][w] == 'S')
          result++;
        if (left &&
            convertedData[h+1][w-1] == 'M' &&
            convertedData[h+2][w-2] == 'A' &&
            convertedData[h+3][w-3] == 'S')
          result++;
        if (right &&
            convertedData[h+1][w+1] == 'M' &&
            convertedData[h+2][w+2] == 'A' &&
            convertedData[h+3][w+3] == 'S')
          result++;
      }
      if (left &&
          convertedData[h][w-1] == 'M' &&
          convertedData[h][w-2] == 'A' &&
          convertedData[h][w-3] == 'S')
        result++;
      if (right &&
          convertedData[h][w+1] == 'M' &&
          convertedData[h][w+2] == 'A' &&
          convertedData[h][w+3] == 'S')
        result++;
    }
  }
  return result;
}

/**
 * @brief returns the solution to the problem stated by AOC2024::day04::2 with
 * the given input data
 *
 * The second problem of the fourth day of AOC2024 consisted of finding the amount
 * of MAS words in the crossword puzzle that also are in a X shape.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The similarity between the two lists given as input data
 */
int solutionToPuzzleTwo(const StrList &convertedData) {
  int height = convertedData.size();
  if (height == 0) return 0;
  
  int width = convertedData[0].size();
  for (string line : convertedData) {
    if (line.size() < width) width = line.size();
  }

  int result{0};
  for (int h{1}; h < height-1; h++) {
    for (int w{1}; w < width-1; w++) {
      if (convertedData[h][w] != 'A') continue;
      if ((convertedData[h-1][w-1] != 'M' ||
           convertedData[h+1][w+1] != 'S') &&
          (convertedData[h-1][w-1] != 'S' ||
           convertedData[h+1][w+1] != 'M')) continue;
      if ((convertedData[h-1][w+1] != 'M' ||
           convertedData[h+1][w-1] != 'S') &&
          (convertedData[h-1][w+1] != 'S' ||
           convertedData[h+1][w-1] != 'M')) continue;
      result++;
    }
  }
  return result;
}
