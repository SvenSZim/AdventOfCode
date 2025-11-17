#include <algorithm>
//#include <cctype>
#include <cstdlib>
#include <iostream>
#include <unordered_map>

#include "getinput.hpp"

int solutionToPuzzleOne(const map &convertedData);
int solutionToPuzzleTwo(const map &convertedData);

/**
 * @brief Function used for testing purposes
 */
int main() {
  map convertedData = readMapFromFile("data/data.txt");

  int visitedTiles = solutionToPuzzleOne(convertedData);
  std::cout << "Solution to puzzle 1: " << visitedTiles << std::endl;

  int possibleBlockerTiles = solutionToPuzzleTwo(convertedData);
  std::cout << "Solution to puzzle 2: " << possibleBlockerTiles << std::endl;

  return 0;
}

std::pair<int, bool> simulateGuardPath(map &m, int height, int width, int addedWallY, int addedWallX);

/**
 * @brief returns the solution to the problem stated by AOC2024::day06::1 with
 * the given input data
 *
 * The first problem of the sixt day of AOC2024 consisted of finding the amount
 * of tiles visited by a security guard on a map where everytime he reaches a
 * wall he turns right.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The difference between the two lists given as input data
 */
int solutionToPuzzleOne(const map &convertedData) {
  int height = convertedData.size();
  if (height == 0) return 0;
  int width = convertedData[0].size();
  if (width == 0) return 0;

  map m;
  for (auto &row : convertedData) {
    std::vector<int> newrow;
    for (int i : row) newrow.push_back(i);
    m.push_back(newrow);
  }

  return simulateGuardPath(m, height, width, -1, -1).first;
}

std::pair<int, int> findStartPoint(const map &m, int height, int width);

/**
 * @brief returns the solution to the problem stated by AOC2024::day06::2 with
 * the given input data
 *
 * The second problem of the sixt day of AOC2024 consisted of finding the amount
 * of tiles where a placed wall would result in a walk-loop for the guard.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The similarity between the two lists given as input data
 */
int solutionToPuzzleTwo(const map &convertedData) {
  int height = convertedData.size();
  if (height == 0) return 0;
  int width = convertedData[0].size();
  if (width == 0) return 0;

  map m;
  for (auto &row : convertedData) {
    std::vector<int> newrow;
    for (int i : row) newrow.push_back(i);
    m.push_back(newrow);
  }

  std::pair<int, int> startPos = findStartPoint(m, height, width);
  int posY = startPos.first, posX = startPos.second;
  int dir = m[posY][posX];

  int loopblockertiles{0};
  posY += dir == 2 ? -1 : (dir == 4 ? 1 : 0);
  posX += dir == 8 ? -1 : (dir == 16 ? 1 : 0);
  while (posY >= 0 && posY < height &&
         posX >= 0 && posX < width) {
    if (m[posY][posX] & 1) {
      // blocker found -> go back and turn right instead
      posY += dir == 2 ? 1 : (dir == 4 ? -1 : 0);
      posX += dir == 8 ? 1 : (dir == 16 ? -1 : 0);
      // left -> up, right -> down, up -> right, down -> left
      dir = dir > 4 ? dir >> 2 : (dir == 2 ? 16 : 8);
    }
    else if (m[posY][posX] == 0) {
      // no blocker found -> place blocker and test for loop
      map cm;
      for (auto &row : convertedData) {
        std::vector<int> newrow;
        for (int i : row) newrow.push_back(i);
        cm.push_back(newrow);
      }
      if (simulateGuardPath(cm, height, width, posY, posX).second) loopblockertiles++;
    } else if (m[posY][posX] & dir) break; // found loop
    m[posY][posX] += dir;
    posY += dir == 2 ? -1 : (dir == 4 ? 1 : 0);
    posX += dir == 8 ? -1 : (dir == 16 ? 1 : 0);
  }
  return loopblockertiles;
}

std::pair<int, int> findStartPoint(const map &m, int height, int width) {
  for (int rowidx{0}; rowidx < height; rowidx++) {
    std::vector<int> crow = m[rowidx];
    for (int columnidx{0}; columnidx < width; columnidx++) {
      int tile = crow[columnidx];
      if (tile != 0 && tile != 1) {
        return {rowidx, columnidx};
      }
    }
  }
  return {-1, -1};
}

std::pair<int, bool> simulateGuardPath(map &m, int height, int width, int addedWallY, int addedWallX) {
  std::pair<int, int> startPos = findStartPoint(m, height, width);
  int posY = startPos.first, posX = startPos.second;
  int dir = m[posY][posX];

  int visitedTiles{1};
  posY += dir == 2 ? -1 : (dir == 4 ? 1 : 0);
  posX += dir == 8 ? -1 : (dir == 16 ? 1 : 0);
  while (posY >= 0 && posY < height &&
         posX >= 0 && posX < width) {
    if (m[posY][posX] & 1 || posY == addedWallY && posX == addedWallX) {
      // blocker found -> go back and turn right instead
      posY += dir == 2 ? 1 : (dir == 4 ? -1 : 0);
      posX += dir == 8 ? 1 : (dir == 16 ? -1 : 0);
      // left -> up, right -> down, up -> right, down -> left
      dir = dir > 4 ? dir >> 2 : (dir == 2 ? 16 : 8);
    }
    else if (m[posY][posX] == 0) visitedTiles++; // visited new tile
    else if (m[posY][posX] & dir) break; // found loop
    m[posY][posX] += dir;
    posY += dir == 2 ? -1 : (dir == 4 ? 1 : 0);
    posX += dir == 8 ? -1 : (dir == 16 ? 1 : 0);
  }
  return {visitedTiles, posY >= 0 && posY < height && posX >= 0 && posX < width};
}
