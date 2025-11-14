#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <unordered_map>

#include "getinput.hpp"

int solutionToPuzzleOne(const ListPair &convertedData);
int solutionToPuzzleTwo(const ListPair &convertedData);

/**
 * @brief Function used for testing purposes
 */
int main() {
  ListPair convertedData = readListsFromFile("data/data.txt");

  int totalDifference = solutionToPuzzleOne(convertedData);
  std::cout << "Solution to puzzle 1: " << totalDifference << std::endl;

  int totalSimilarityScores = solutionToPuzzleTwo(convertedData);
  std::cout << "Solution to puzzle 2: " << totalSimilarityScores << std::endl;

  return 0;
}

/**
 * @brief returns the solution to the problem stated by AOC2024::day01::1 with
 * the given input data
 *
 * The first problem of the first day of AOC2024 consisted of finding the total
 * difference between two lists of numbers, where the difference is defined as
 * the sum of the pairwise difference of the sorted lists.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The difference between the two lists given as input data
 */
int solutionToPuzzleOne(const ListPair &convertedData) {
  std::vector<int> first = convertedData.first;
  std::vector<int> second = convertedData.second;

  std::sort(first.begin(), first.end());
  std::sort(second.begin(), second.end());

  int difference = 0;
  for (size_t idx = 0; idx < first.size(); ++idx) {
    difference += std::abs(first[idx] - second[idx]);
  }
  return difference;
}

/**
 * @brief returns the solution to the problem stated by AOC2024::day01::2 with
 * the given input data
 *
 * The second problem of the first day of AOC2024 consisted of finding the total
 * similarity between two lists of numbers, where the similarity is defined as
 * the sum of the product of each number in the first list multiplied by its
 * number of appearances in the second list.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The similarity between the two lists given as input data
 */
int solutionToPuzzleTwo(const ListPair &convertedData) {
  std::unordered_map<int, int> counterForSecondList;

  for (int number : convertedData.second)
    counterForSecondList[number]++;

  int totalSimilarityScores = 0;
  for (int number : convertedData.first)
    totalSimilarityScores += number * counterForSecondList[number];

  return totalSimilarityScores;
}
