#include <algorithm>
//#include <cctype>
#include <cstdlib>
#include <iostream>
#include <unordered_map>
#include <set>

#include "getinput.hpp"

int solutionToPuzzleOne(const data &convertedData);
int solutionToPuzzleTwo(const data &convertedData);

/**
 * @brief Function used for testing purposes
 */
int main() {
  data convertedData = parseData("data/data.txt");

  int sol1 = solutionToPuzzleOne(convertedData);
  std::cout << "Solution to puzzle 1: " << sol1 << std::endl;

  int sol2 = solutionToPuzzleTwo(convertedData);
  std::cout << "Solution to puzzle 2: " << sol2 << std::endl;

  return 0;
}

data uniquifyGardenlabels(const data &map);

/**
 * @brief returns the solution to the problem stated by AOC2024::day12::1 with
 * the given input data
 *
 * The first problem of the twelfth day of AOC2024 consisted of finding the total
 * fence price for enclosing all the garden-areas. Price per garden = area * perimeter
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The difference between the two lists given as input data
 */
int solutionToPuzzleOne(const data &convertedData) {
  data map = uniquifyGardenlabels(convertedData);

  int height = map.size();
  if (height == 0) return 0;
  int width = map[0].size();
  std::unordered_map<int, std::pair<int, int>> gardens; // label -> area, perimeter
  for (int h{0}; h < height; h++) {
    const std::vector<int> &row = map[h];
    for (int w{0}; w < width; w++) {
      const int c = row[w];
      if (gardens.count(c) == 0) gardens[c] = {0, 0};
      gardens[c].first++;
      if (h == 0 || map[h-1][w] != c) gardens[c].second++;
      if (h == height-1 || map[h+1][w] != c) gardens[c].second++;
      if (w == 0 || map[h][w-1] != c) gardens[c].second++;
      if (w == width-1 || map[h][w+1] != c) gardens[c].second++;
    }
  }
  int result{0};
  for (const auto& [_, garden] : gardens)
    result += garden.first * garden.second;
  return result;
}

/**
 * @brief returns the solution to the problem stated by AOC2024::day12::2 with
 * the given input data
 *
 * The second problem of the twelfth day of AOC2024 consisted of finding the total
 * fence price for enclosing all the garden-areas. Price per garden = area * #side
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The similarity between the two lists given as input data
 */
int solutionToPuzzleTwo(const data &convertedData) {
  const data map = uniquifyGardenlabels(convertedData);

  int height = map.size();
  if (height == 0) return 0;
  int width = map[0].size();
  std::unordered_map<int, std::pair<int, int>> gardens; // label -> area, perimeter
  for (int h{0}; h < height; h++) {
    const std::vector<int> &row = map[h];
    for (int w{0}; w < width; w++) {
      const int c = row[w];
      if (gardens.count(c) == 0) gardens[c] = {0, 0};
      gardens[c].first++;
      if (h == 0 && (w == 0 || map[h][w-1] != c) ||
          h != 0 && map[h-1][w] != c && (w == 0 || map[h][w-1] != c || map[h-1][w-1] == c)) gardens[c].second++;
      if (h == height-1 && (w == 0 || map[h][w-1] != c) ||
          h != height-1 && map[h+1][w] != c && (w == 0 || map[h][w-1] != c || map[h+1][w-1] == c)) gardens[c].second++;
      if (w == 0 && (h == 0 || map[h-1][w] != c) ||
          w != 0 && map[h][w-1] != c && (h == 0 || map[h-1][w] != c || map[h-1][w-1] == c)) gardens[c].second++;
      if (w == width-1 && (h == 0 || map[h-1][w] != c) ||
          w != width-1 && map[h][w+1] != c && (h == 0 || map[h-1][w] != c || map[h-1][w+1] == c)) gardens[c].second++;
    }
  }
  int result{0};
  for (const auto& [l, garden] : gardens)
    result += garden.first * garden.second;
  return result;
}


void floodfillrename(data &map, const std::pair<int,int> pos, const int uid);

data uniquifyGardenlabels(const data &map) {
  int height = map.size();
  if (height == 0) return {};
  int width = map[0].size();
  
  data newmap;
  std::set<int> usednums;
  for (const auto &row : map) {
    std::vector<int> nrow;
    for (const int c : row) {
      usednums.insert(c);
      nrow.emplace_back(c);
    }
    newmap.emplace_back(nrow);
  }

  int uid = 0;
  while (usednums.count(uid) != 0) uid++;
  for (int h{0}; h < height; h++) {
    for (int w{0}; w < width; w++) {
      if (usednums.count(map[h][w]) != 0) {
        floodfillrename(newmap, {h, w}, uid++);
        while (usednums.count(uid) != 0) uid++;
      }
    }
  }
  return newmap;
}

void floodfillrename(data &map, const std::pair<int,int> pos, const int uid) {
  int height = map.size();
  if (height == 0) return;
  int width = map[0].size();
  std::set<std::pair<int, int>> opentiles = {pos};
  while (opentiles.size() > 0) {
    std::pair<int, int> tile = *opentiles.begin();
    int h = tile.first, w = tile.second, c = map[h][w];
    if (h > 0 && map[h-1][w] == c) opentiles.insert({h-1, w});
    if (h < height-1 && map[h+1][w] == c) opentiles.insert({h+1, w});
    if (w > 0 && map[h][w-1] == c) opentiles.insert({h, w-1});
    if (w < width-1 && map[h][w+1] == c) opentiles.insert({h, w+1});
    map[h][w] = uid;
    opentiles.erase(tile);
  }
}
