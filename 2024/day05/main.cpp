#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <tuple>

#include "getinput.hpp"

int solutionToPuzzleOne(const rulesNlists &convertedData);
int solutionToPuzzleTwo(const rulesNlists &convertedData);

/**
 * @brief Function used for testing purposes
 */
int main() {
  rulesNlists convertedData = parseFile("data/data.txt");

  int totalDifference = solutionToPuzzleOne(convertedData);
  std::cout << "Solution to puzzle 1: " << totalDifference << std::endl;

  int totalSimilarityScores = solutionToPuzzleTwo(convertedData);
  std::cout << "Solution to puzzle 2: " << totalSimilarityScores << std::endl;

  return 0;
}

bool doRulesApply(const list &l, const std::vector<rule> &rules);

/**
 * @brief returns the solution to the problem stated by AOC2024::day05::1 with
 * the given input data
 *
 * The first problem of the fifth day of AOC2024 consisted of finding the numberlists
 * for which the specified orderingrules apply and adding their center-page-numbers.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The difference between the two lists given as input data
 */
int solutionToPuzzleOne(const rulesNlists &convertedData) {
  int result{0};
  for (const list &l : convertedData.second) {
    if (doRulesApply(l, convertedData.first))
      result += l[l.size() / 2];
  }
  return result;
}

list getAllRequiredPredecessors(int n, list l, std::vector<rule> rules);

/**
 * @brief returns the solution to the problem stated by AOC2024::day05::2 with
 * the given input data
 *
 * The second problem of the fifth day of AOC2024 consisted of findint the numberlists
 * for which the specified orderingrules do not apply, sorting them to apply the rules
 * and adding the center-page-numbers of those ordered numberlists.
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns The similarity between the two lists given as input data
 */
int solutionToPuzzleTwo(const rulesNlists &convertedData) {
  int result{0};
  for (const list &l : convertedData.second) {
    if (!doRulesApply(l, convertedData.first)) {
      list newlist;
      std::vector<std::pair<int, list>> numbers; // value, required predecessors
      // find all required predecessors
      for (int n : l)
        numbers.push_back({
          n, // value
          getAllRequiredPredecessors(n, l, convertedData.first) // required predecessors
        });
      
      // loop until all numbers are used
      int numberamount = numbers.size();
      while (numberamount > 0) {
        // track change to avoid infinite loop
        bool change = false;
        // check for a number where all required predecessors already in newlist
        for (int cnumidx{0}; cnumidx < numberamount; cnumidx++) {
          std::pair<int, list> &currnum = numbers[cnumidx];
          if (currnum.second.size() == 0) {
            // no req. pred. -> use number
            newlist.push_back(currnum.first);
            // update req. pred. of other numbers
            for (std::pair<int, list> &n : numbers)
              n.second.erase(std::find(n.second.begin(), n.second.end(), currnum.first));
            
            numbers.erase(numbers.begin() + cnumidx); // remove number from available numbers
            numberamount--;
            change = true; // track change
            break;
          }
        }
        if (!change)
          throw std::runtime_error(
            "Error: Unable to sort: " + std::to_string(l[0]) + ",...," + std::to_string(l[l.size()-1])
          );
      }
      result += newlist[newlist.size() / 2];
    }
  }
  return result;
}



bool doRulesApply(const list &l, const std::vector<rule> &rules) {
  int n = l.size(), a, b;
  for (int i{0}; i < n-1; i++) {
    a = l[i];
    for (int j{i+1}; j < n; j++) {
      b = l[j];
      for (const rule &r : rules) {
        if (a == r.second && b == r.first) return false;
      }
    }
  }
  return true;
}

list getAllRequiredPredecessors(int n, list l, std::vector<rule> rules) {
  list reqpred;
  for (rule &r : rules) {
    if (r.second == n) {
      if (std::find(l.begin(), l.end(), r.first) != l.end())
        reqpred.push_back(r.first);
    }
  }
  return reqpred;
}
