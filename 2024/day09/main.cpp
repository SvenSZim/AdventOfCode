#include <algorithm>
//#include <cctype>
#include <cstdlib>
#include <iostream>
#include <set>

#include "getinput.hpp"

long solutionToPuzzleOne(const std::vector<int> &convertedData);
long solutionToPuzzleTwo(const std::vector<int> &convertedData);

/**
 * @brief Function used for testing purposes
 */
int main() {
  std::vector<int> convertedData = parseData("data/data.txt");

  long totalDifference = solutionToPuzzleOne(convertedData);
  std::cout << "Solution to puzzle 1: " << totalDifference << std::endl;

  long totalSimilarityScores = solutionToPuzzleTwo(convertedData);
  std::cout << "Solution to puzzle 2: " << totalSimilarityScores << std::endl;

  return 0;
}

/**
 * @brief returns the solution to the problem stated by AOC2024::day09::1 with
 * the given input data
 *
 * The first problem of the ninth day of AOC2024 consisted of compressing data
 * and returning a checksum calculated from the compressed data
 *
 * @param[in] convertedData The formated input std::vector<int> necessary for the problem
 * @returns The difference between the two lists given as input std::vector<int>
 */
long solutionToPuzzleOne(const std::vector<int> &convertedData) {
  int n = convertedData.size();
  bool lodd = false;
  int lidx = 0, ridx = (n % 2) ? n-1 : n, idx = 0, lpacket = 0, lsize, rpacket = (n-1)/2+1, rsize = 0;
  long result{0};
  while (lidx < ridx) {
    lsize = convertedData[lidx];
    if (lodd) {
      for (int i{0}; i < lsize; i++) {
        if (rsize == 0) {
          if (ridx < lidx) break;
          rsize = convertedData[ridx];
          rpacket--;
          ridx -= 2;
        }
        result += idx * rpacket;
        rsize--;
        idx++;
      }
    } else {
      for (int i{0}; i < lsize; i++) {
        result += idx * lpacket;
        idx++;
      }
      lpacket++;
    }
    lidx++;
    lodd = !lodd;
  }
  if (lidx == ridx) {
    lsize = convertedData[lidx];
    for (int i{0}; i < lsize; i++) {
      result += idx * lpacket;
      idx++;
    }
  }
  for (int i{0}; i < rsize; i++) {
    result += idx * rpacket;
    idx++;
  }
  return result;
}

/**
 * @brief returns the solution to the problem stated by AOC2024::day09::2 with
 * the given input data
 *
 * The second problem of the ninth day of AOC2024 consisted of compressing data
 * and returning a checksum calculated from the compressed data
 *
 * @param[in] convertedData The formated input std::vector<int> necessary for the problem
 * @returns The similarity between the two lists given as input std::vector<int>
 */
long solutionToPuzzleTwo(const std::vector<int> &convertedData) {
  std::set<int> usedRIdx;
  int n = convertedData.size();
  bool lodd = false;
  int maxRIdx = (n % 2) ? n-1 : n;
  int lidx = 0, idx = 0, lpacket = 0, lsize, rpacket, rsize;
  long result{0};
  while (lidx < n) {
    lsize = convertedData[lidx];
    if (lodd) {
      for (int ridx{maxRIdx}; ridx > lidx; ridx -= 2) {
        if (usedRIdx.count(ridx) == 0) {
          rsize = convertedData[ridx];
          if (rsize <= lsize) {
            rpacket = ridx>>1;
            for (int i{0}; i < rsize; i++) {
              result += idx * rpacket;
              idx++;
            }
            usedRIdx.insert(ridx);
            lsize -= rsize;
            if (lsize == 0) break;
          }
        }
      }
      idx += lsize;
    } else {
      if (usedRIdx.count(lidx) == 0) {
        for (int i{0}; i < lsize; i++) {
          result += idx * lpacket;
          idx++;
        }
      } else idx += lsize;
      lpacket++;
    }
    lidx++;
    lodd = !lodd;
  }
  return result;
}
