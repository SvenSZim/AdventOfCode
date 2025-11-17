#include <algorithm>
//#include <cctype>
#include <cstdlib>
#include <iostream>
#include <unordered_map>

#include "getinput.hpp"

long solutionToPuzzleOne(const std::vector<equation> &convertedData);
long solutionToPuzzleTwo(const std::vector<equation> &convertedData);

/**
 * @brief Function used for testing purposes
 */
int main() {
  std::vector<equation> convertedData = parseData("data/data.txt");

  long totalDifference = solutionToPuzzleOne(convertedData);
  std::cout << "Solution to puzzle 1: " << totalDifference << std::endl;

  long totalSimilarityScores = solutionToPuzzleTwo(convertedData);
  std::cout << "Solution to puzzle 2: " << totalSimilarityScores << std::endl;

  return 0;
}

bool checkEquationPart1(const equation &eq, int operators);

/**
 * @brief returns the solution to the problem stated by AOC2024::day07::1 with
 * the given input data
 *
 * The first problem of the seventh day of AOC2024 consisted of finding the sum of
 * all equations solvable by inserting '+' or 'x'. Equations are evaluated left to right.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The difference between the two lists given as input data
 */
long solutionToPuzzleOne(const std::vector<equation> &convertedData) {
  long result{0};
  for (const equation &eq : convertedData) {
    int eqsize = eq.second.size();
    int operatorAmount = 1;
    for (int i{0}; i < eqsize; i++) operatorAmount <<= 1;
    for (int operators{0}; operators < operatorAmount; operators++) {
      if (checkEquationPart1(eq, operators)) {
        result += eq.first;
        break;
      }
    }
  }
  return result;
}

bool checkEquationPart2(const equation &eq, int operators);

/**
 * @brief returns the solution to the problem stated by AOC2024::day07::2 with
 * the given input data
 *
 * The first problem of the seventh day of AOC2024 consisted of finding the sum of
 * all equations solvable by inserting '+', 'x' or '||' (concat).
 * Equations are evaluated left to right.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The similarity between the two lists given as input data
 */
long solutionToPuzzleTwo(const std::vector<equation> &convertedData) {
  long result{0};
  for (int h{0}; h < convertedData.size(); h++) {
    const equation &eq = convertedData[h];
    int eqsize = eq.second.size();
    int operatorAmount = 1;
    for (int i{0}; i < eqsize; i++) operatorAmount *= 3;
    for (int operators{0}; operators < operatorAmount; operators++) {
      if (checkEquationPart2(eq, operators)) {
        result += eq.first;
        break;
      }
    }
  }
  return result;
}

bool checkEquationPart1(const equation &eq, int operators) {
  int eqsize = eq.second.size();
  if (eqsize == 0) return eq.first == 0;
  long total{eq.second[0]};
  for (int eqidx{1}; eqidx < eqsize; eqidx++) {
    switch (operators & 1) {
    case 0:
      total += eq.second[eqidx];
      break;
    case 1:
      total *= eq.second[eqidx];
      break;
    }
    operators >>= 1;
    if (total > eq.first) break;
  }
  return eq.first == total;
}

bool checkEquationPart2(const equation &eq, int operators) {
  int eqsize = eq.second.size();
  if (eqsize == 0) return eq.first == 0;
  long total{eq.second[0]};
  for (int eqidx{1}; eqidx < eqsize; eqidx++) {
    switch (operators % 3) {
    case 0:
      total *= eq.second[eqidx];
      break;
    case 1:
      total += eq.second[eqidx];
      break;
    case 2:
      total = std::stol(std::to_string(total) + std::to_string(eq.second[eqidx]));
      break;
    }
    operators /= 3;
    if (total > eq.first) break;
  }
  return eq.first == total;
}
