#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <unordered_map>

#include "getinput.hpp"

int solutionToPuzzleOne(const ListList &convertedData);
int solutionToPuzzleTwo(const ListList &convertedData);

/**
 * @brief Function used for testing purposes
 */
int main() {
  ListList convertedData = readListsFromFile("data/data.txt");

  int numSaveRuns = solutionToPuzzleOne(convertedData);
  std::cout << "Solution to puzzle 1: " << numSaveRuns << std::endl;

  int adjNumSaveRuns = solutionToPuzzleTwo(convertedData);
  std::cout << "Solution to puzzle 2: " << adjNumSaveRuns << std::endl;

  return 0;
}

bool isSaveRun(const std::vector<int> &run);

/**
 * @brief returns the solution to the problem stated by AOC2024::day02::1 with
 * the given input data
 *
 * The first problem of the second day of AOC2024 consisted of finding the total
 * amount of save runs from a list of reactor-runs. A run is considered save
 * if it is fully increasing or decreasing with each succeeding number differing from
 * the previous by at least one and at most three.
 *
 * @param[in] convertedData The formatted input data necessary for the problem
 * @returns The difference between the two lists given as input data
 */
int solutionToPuzzleOne(const ListList &convertedData) {
  int saveRuns{0};
  for (auto &run : convertedData) {
    if (isSaveRun(run)) saveRuns++;
  }
  return saveRuns;
}

/**
 * @brief returns the solution to the problem stated by AOC2024::day02::2 with
 * the given input data
 *
 * The second problem of the second day of AOC2024 consisted of finding the total
 * amount of save runs from a list of reactor-runs. A run is considered save
 * if it is fully increasing or decreasing with each succeeding number differing from
 * the previous by at least one and at most three. In addition a run is also save if
 * you can reach a save run by removing one number from the run.
 *
 * @param[in] convertedData The formatted input data necessary for the problem
 * @returns The similarity between the two lists given as input data
 */
int solutionToPuzzleTwo(const ListList &convertedData) {
  int saveRuns{0};
  for (auto &run : convertedData) {
    if (isSaveRun(run)) {
      saveRuns++;
    } else {
      int runlength = run.size();
      for (int ri{0}; ri < runlength; ri++) {
        std::vector<int> altrun;
        // generate alternate run
        for (int i{0}; i < runlength; i++) {
          // remove one number
          if (i != ri) altrun.push_back(run[i]);
        }
        if (isSaveRun(altrun)) {
          saveRuns++;
          break;
        }
      }
    }
  }
  return saveRuns;
}

bool isSaveRun(const std::vector<int> &run) {
  int runlength = run.size();
  if (runlength > 1) {
    bool increasing = run[0] < run[1];
    int difference;
    for (int i{1}; i < runlength; i++) {
      // check for difference between adjacent numbers and increasing/decreasing consistency
      difference = increasing ? run[i] - run[i-1] : run[i-1] - run[i];
      // if increasing/decreasing inconsistent -> difference < 0
      if (difference < 1 || difference > 3) return false;
    }
  }
  return true;
}
