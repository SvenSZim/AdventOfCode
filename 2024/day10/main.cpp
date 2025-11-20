#include <algorithm>
//#include <cctype>
#include <cstdlib>
#include <iostream>
#include <set>

#include "getinput.hpp"

int solutionToPuzzleOne(const data &convertedData);
int solutionToPuzzleTwo(const data &convertedData);

/**
 * @brief Function used for testing purposes
 */
int main() {
  data convertedData = parseData("data/data.txt");

  int totalDifference = solutionToPuzzleOne(convertedData);
  std::cout << "Solution to puzzle 1: " << totalDifference << std::endl;

  int totalSimilarityScores = solutionToPuzzleTwo(convertedData);
  std::cout << "Solution to puzzle 2: " << totalSimilarityScores << std::endl;

  return 0;
}

std::vector<std::pair<int,int>> findAllStartingPoints(const data &map);
std::vector<std::pair<int,int>> getAllDistinctReachablePoints(const data &map, std::vector<std::pair<int,int>> &currentPoints);

/**
 * @brief returns the solution to the problem stated by AOC2024::day10::1 with
 * the given input data
 *
 * The first problem of the tenth day of AOC2024 consisted of finding the total
 * 'score' of all 'hiking trails' on the map.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The difference between the two lists given as input data
 */
int solutionToPuzzleOne(const data &convertedData) {
  int result{0};
  std::vector<std::pair<int, int>> startPoints = findAllStartingPoints(convertedData);
  std::vector<std::vector<std::pair<int,int>>> hikes;
  for (auto &p : startPoints) hikes.push_back({p});
  int nhikes = hikes.size();
  for (int i{0}; i < 9; i++) {
    for (int hidx{0}; hidx < nhikes; hidx++)
      hikes[hidx] = getAllDistinctReachablePoints(convertedData, hikes[hidx]);
  }
  for (auto &h : hikes)
    result += h.size();
  return result;
}

std::vector<std::pair<int,int>> getAllReachablePoints(const data &map, std::vector<std::pair<int,int>> &currentPoints);

/**
 * @brief returns the solution to the problem stated by AOC2024::day10::2 with
 * the given input data
 *
 * The first problem of the tenth day of AOC2024 consisted of finding the total
 * 'score' of all 'hiking trails' on the map.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The similarity between the two lists given as input data
 */
int solutionToPuzzleTwo(const data &convertedData) {
  std::vector<std::pair<int, int>> reachablePoints = findAllStartingPoints(convertedData);
  for (int i{0}; i < 9; i++) {
    reachablePoints = getAllReachablePoints(convertedData, reachablePoints);
  }
  return reachablePoints.size();
}


std::vector<std::pair<int,int>> findAllStartingPoints(const data &map) {
  int height = map.size();
  if (height == 0) return {};
  int width = map[0].size();
  std::vector<std::pair<int,int>> startingPoints;
  for (int h{0}; h < height; h++) {
    const std::vector<int> &row = map[h];
    for (int w{0}; w < width; w++) {
      if (row[w] == 0) startingPoints.push_back({h, w});
    }
  }
  return startingPoints;
}

std::vector<std::pair<int,int>> getAllReachablePoints(const data &map, std::vector<std::pair<int,int>> &currentPoints) {
  std::vector<std::pair<int,int>> reachablePoints;
  int height = map.size();
  if (height == 0) return {};
  int width = map[0].size();
  int h, w, ch;
  for (auto &point : currentPoints) {
    h = point.first;
    w = point.second;
    ch = map[h][w];
    if (h > 0 && map[h-1][w] == ch+1)
      reachablePoints.push_back({h-1, w});
    if (h < height-1 && map[h+1][w] == ch+1)
      reachablePoints.push_back({h+1, w});
    if (w > 0 && map[h][w-1] == ch+1)
      reachablePoints.push_back({h, w-1});
    if (w < width-1 && map[h][w+1] == ch+1)
      reachablePoints.push_back({h, w+1});
  }
  return reachablePoints;
}

std::vector<std::pair<int,int>> getAllDistinctReachablePoints(const data &map, std::vector<std::pair<int,int>> &currentPoints) {
  std::set<std::pair<int,int>> points;
  std::vector<std::pair<int,int>> distinctReachablePoints;
  std::vector<std::pair<int,int>> allReachablePoints = getAllReachablePoints(map, currentPoints);
  for (auto &p : allReachablePoints) {
    if (points.count(p) == 0) {
      points.insert(p);
      distinctReachablePoints.emplace_back(p);
    }
  }
  return distinctReachablePoints;
}

