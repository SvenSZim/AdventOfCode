#include <algorithm>
//#include <cctype>
#include <cstdlib>
#include <iostream>
#include <unordered_map>

#include "getinput.hpp"

long solutionToPuzzleOne(const data &convertedData);
long solutionToPuzzleTwo(const data &convertedData);

void setupout(data &setup) {
  for (const auto& [key, value] : setup) {
    std::cout << value << "x " << key << " ";
  }
  std::cout << '\n';
}

/**
 * @brief Function used for testing purposes
 */
int main() {
  data convertedData = parseData("data/data.txt");

  long sol1 = solutionToPuzzleOne(convertedData);
  std::cout << "Solution to puzzle 1: " << sol1 << std::endl;

  long sol2 = solutionToPuzzleTwo(convertedData);
  std::cout << "Solution to puzzle 2: " << sol2 << std::endl;

  return 0;
}

void updateRuleCache(const data &setup, std::unordered_map<std::string,std::vector<std::string>> &rules);
data applyRules(data &setup, std::unordered_map<std::string,std::vector<std::string>> &rules);

/**
 * @brief returns the solution to the problem stated by AOC2024::day11::1 with
 * the given input data
 *
 * The first problem of the eleventh day of AOC2024 consisted of finding the amount of
 * stones after 25 blinks.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The difference between the two lists given as input data
 */
long solutionToPuzzleOne(const data &convertedData) {
  data setup;
  for (const auto& [key, value] : convertedData)
    setup[key] = value;

  std::unordered_map<std::string,std::vector<std::string>> cachedrules;
  for (int i{0}; i < 25; i++) {
    updateRuleCache(setup, cachedrules);
    setup = applyRules(setup, cachedrules);
  }

  long result{0};
  for (const auto& [key, value] : setup)
    result += value;
  return result;
}

/**
 * @brief returns the solution to the problem stated by AOC2024::day11::2 with
 * the given input data
 *
 * The first problem of the eleventh day of AOC2024 consisted of finding the amount of
 * stones after 75 blinks.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The similarity between the two lists given as input data
 */
long solutionToPuzzleTwo(const data &convertedData) {
  data setup;
  for (const auto& [key, value] : convertedData)
    setup[key] = value;

  std::unordered_map<std::string,std::vector<std::string>> cachedrules;
  for (int i{0}; i < 75; i++) {
    updateRuleCache(setup, cachedrules);
    setup = applyRules(setup, cachedrules);
  }

  long result{0};
  for (const auto& [key, value] : setup)
    result += value;
  return result;
}

void updateRuleCache(const data& setup, std::unordered_map<std::string,std::vector<std::string>> &rules) {
  if (rules.count("0") == 0) rules["0"] = {"1"};
  for (const auto& [v, _] : setup) {
    if (rules.count(v) == 0) {
      int vs = v.size();
      if (vs % 2 == 0) {
        // Size is even -> split number
        std::string s1 = v.substr(0, vs/2);
        std::string s2 = v.substr(vs/2, vs/2); // could contain leading '0'
        s2 = std::to_string(std::stol(s2));
        rules[v] = {s1, s2};
      } else {
        long l = std::stol(v);
        l *= 2024L;
        if (l < 0) std::cout << "overflow...";
        rules[v] = {std::to_string(l)};
      }
    }
  }
}

data applyRules(data &setup, std::unordered_map<std::string,std::vector<std::string>> &rules) {
  data newsetup;
  for (const auto& [value, amount] : setup) {
    for (const auto& newv : rules[value]) {
      if (newsetup.count(newv) == 0)
        newsetup[newv] = 0;
      newsetup[newv] += amount;
    }
  }
  return newsetup;
}
