#include <algorithm>
//#include <cctype>
#include <cstdlib>
#include <iostream>
#include <unordered_map>

#include "getinput.hpp"

long solutionToPuzzleOne(const data &convertedData);
long solutionToPuzzleTwo(const data &convertedData);

std::pair<long,long> calculateVectorCombination(const std::pair<long,long> target, const std::pair<long,long> a, const std::pair<long,long> b);
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


/**
 * @brief returns the solution to the problem stated by AOC2024::day13::1 with
 * the given input data
 *
 * The first problem of the thirteenth day of AOC2024 consisted of finding the minimum
 * required amount of tokens for obtaining all targets:
 *  - to reach a target (2D pos) you must use a integer combination of a (2D vec) and b (2D vec)
 *  - using one a costs 3 tokens, using one b costs 1 token
 *  - each vector (a,b) can only be used a maximum of 100 times
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns Total tokenamount required to reach all (reachable) targets
 */
long solutionToPuzzleOne(const data &convertedData) {
  long result{0};
  for (const auto& eq : convertedData) {
    std::pair<long,long> presses = calculateVectorCombination({eq[4], eq[5]}, {eq[0], eq[1]}, {eq[2], eq[3]});
    if (presses.first <= 100 && presses.second <= 100) // maximum of 100 uses per vec
      result += presses.first * 3 + presses.second; // 3 tokens for a, 1 token for b
  }
  return result;
}

/**
 * @brief returns the solution to the problem stated by AOC2024::day13::1 with
 * the given input data
 *
 * The second problem of the thirteenth day of AOC2024 consisted of finding the minimum
 * required amount of tokens for obtaining all targets:
 *  - to reach a target (2D pos) you must use a integer combination of a (2D vec) and b (2D vec)
 *  - using one a costs 3 tokens, using one b costs 1 token
 *  - each target has an offset of 10_000_000_000_000 for each dimension
 *
 * @param[in] convertedData The formated input data necessary for the problem
 * @returns Total tokenamount required to reach all (reachable) targets
 */
long solutionToPuzzleTwo(const data &convertedData) {
  const long offset = 10000000000000L;
  long result{0};
  for (const auto& eq : convertedData) {
    auto pres = calculateVectorCombination({eq[4] + offset, eq[5] + offset}, {eq[0], eq[1]}, {eq[2], eq[3]});
    result += pres.first * 3 + pres.second; // 3 tokens for a, 1 token for b
  }
  return result;
}


long gcd(long a, long b);
long extended_gcd(long a, long b, long *x, long *y);
bool isColinear(std::pair<long,long> a, std::pair<long,long> b);


/**
 * calculates all possible factors for a:
 * target = x*a + y*b;
 * -> x = x0 + k*dx (^equation (integer-)solvable for all (integer) k)
 *
 * underlying math:
 * target = x*a + y*b         | calculate (mod b)
 * target = x*a + y*b (mod b) | y*b = 0 (mod b)
 * target = x*a       (mod b) | calculate ainv: 1 = ainv*a (mod b)
 * x = target*ainv (mod b)    | convert back
 * x = target*ainv + k*b
 * 
 * @returns x0, dx
 */
std::pair<long,long> calculatePossibleAFactors(long target, long a, long b) {
  // Step 0: edge cases
  if (target < a) return {0, 0}; // cant use a
  if (a == 0) return {0, 1}; // a can be anything
  if (b == 0) {
    if (target % a == 0)
      return {target/a, 0}; // a has to reach target alone
    return {0, 0}; // unsolvable
  }
  if (b == 1) return {0, 1}; // a can be anything
  
  // Step 1: calculate (mod b)
  target %= b;
  a %= b;

  // Step 1.1: eliminate gcd's
  long ggcd = gcd(b, gcd(target, a));
  if (ggcd == 0) ggcd = 1;
  target /= ggcd; a /= ggcd; b /= ggcd;

  // Step 2: calculate ainv
  long ainv, buf, rem;
  rem = extended_gcd(a, b, &ainv, &buf) % b;
  bool aany = rem == 0 && a == 0;
  if (!aany && rem != 1) return {0, 0};
  if (ainv < 0) ainv += b;

  // Step 3: convert back: x = target*ainv + k*b
  return {target*ainv, b};
}

/**
 * calculates all integer intersections of two lines
 * a = a0 + da*m
 * b = b0 + db*n
 *
 * underlying math:
 * a0 + da*m = b0 + db*n   | -b0-da*m
 * a0 - b0   = db*n - da*m | -> use calculatePossibleAFactors
 * n = n0 + dn*k
 * b = b0 + db*(n0 + dn*k)
 *   = b0 + db*n0 + db*dn*k
 * s0 = b0 + db*n0         | constant
 * ds = db*dn              | variable
 *
 * @returns s0, ds
 */
std::pair<long,long> calculateIntersections(std::pair<long,long> a, std::pair<long,long> b) {
  // Step 0: edge cases
  if (a.second < b.second) return calculateIntersections(b, a);
  if (b.second < 0) return calculateIntersections(a, {b.first, -b.second});
  if (a.second == 0) {
    if (a.first == b.first) return {a.first, 0};
    else return {0, 0};
  }
  if (b.second == 0) {
    if ((b.first - a.first) % a.second == 0) return {b.first, 0};
    return {0, 0};
  }
  // Step 1: convert into equation target = a*x + b*y
  long deltaa = (a.first - b.first) % a.second; if (deltaa < 0) deltaa += a.second;
  // Step 2: use calculatePossibleAFactors
  std::pair<long,long> n = calculatePossibleAFactors(deltaa + a.second, b.second % a.second, a.second);

  if (n.second != 0)
    return {(b.first + b.second * n.first) % (n.second * b.second), n.second * b.second};
  return {b.first + b.second * n.first, 0};
}


/**
 * calculates all possible factors for a (for 2D)
 * target = x*a + y*b;
 * -> x = x0 + k*dx (^equation (integer-)solvable for all (integer) k)
 *
 * underlying math:
 * 1. split into equation for first- and second-dimension
 * 2. use calculatePossibleAFactors for both equations
 * 3. combine equations with calculateIntersections
 *
 * @returns x0, dx
 */
std::pair<long,long> calculatePossibleAFactors(const std::pair<long,long> target, const std::pair<long,long> a, const std::pair<long,long> b) {
  // Step 1: split first- and second-dimension
  // Step 2: use calculatePossibleAFactors
  std::pair<long,long> aX = calculatePossibleAFactors(target.first, a.first, b.first);
  std::pair<long,long> aY = calculatePossibleAFactors(target.second, a.second, b.second);
  // Step 3: use combineConditions
  return calculateIntersections(aX,aY);
}


/**
 * calculates solution for equation with 2d vectors (target, a, b):
 * target = x*a + y*b (constants except x,y)
 *
 * underlying math:
 * 1. calculate factors for a and b separately
 *  -> x = a0 + da*m, y = b0 + db*n
 * 2. substitute -> new equation:
 *  target = (a0 + da*m)*a + (b0 + db*n)*b
 *  target = a0*a + da*m*a + b0*b + db*n*b
 *  target - a0*a - b0*b = da*a*m + db*b*n (constants except m,n)
 *  -> target' = m*a' + n*b'
 * 3. recursively use calculateVectorCombination (test for edge/trivial cases)
 * 4. test solution
 */
std::pair<long,long> calculateVectorCombination(const std::pair<long,long> target, const std::pair<long,long> a, const std::pair<long,long> b) {
  std::pair<long,long> pa, pb;
  // Step 0: edge cases
  if (target.first < target.second) return calculateVectorCombination({target.second, target.first}, {a.second, a.first}, {b.second, b.first});
  if (target.second < 0) return {0, 0}; //unsolvable
  if (target.first == 0) return {0, 0}; //trivial solution
  else {
    if (a.first == 0 && b.first == 0)
      return {0, 0}; //unsolvable
    if (target.first < a.first && target.first < b.first)
      return {0, 0}; //unsolvable
  }
  // one vector is (0, 0)
  if (a.first == 0 && a.second == 0 && b.first == 0 && b.second == 0) return {0, 0};
  if (a.first == 0 && a.second == 0) {
    std::pair<long,long> res = calculateVectorCombination(target, b, a);
    return {res.second, res.first};
  }
  if (b.first == 0 && b.second == 0) {
    if ((a.first == 0 && target.first == 0 || target.first % a.first == 0) &&
        (a.second == 0 && target.second == 0 || target.second % a.second == 0)) {
      if (a.first != 0 && a.second != 0) {
        if (target.first/a.first == target.second/a.second) return {0, target.first/a.first};
        return {0, 0}; //unsolvable
      }
      if (a.first != 0)
        return {0, target.first/a.first};
      if (a.second != 0)
        return {0, target.second/a.second};
    }
    return {0, 0};
  }
  // check for colinear vectors
  if (isColinear(a, b)) {
    // just use larger vector
    if (a.first > b.first) return calculateVectorCombination(target, a, {0, 0});
    std::pair<long,long> res = calculateVectorCombination(target, b, {0, 0});
    return {res.second, res.first};
  }
  if (target.second == 0) {
    if (a.second != 0 && b.second != 0)
      return {0, 0}; //unsolvable
    if (a.second != 0) {
      if (b.first != 0 && target.first % b.first == 0)
        return {0, target.first/b.first};
      return {0, 0}; //unsolvable
    }
    if (b.second != 0) {
      if (a.first != 0 && target.first % a.first == 0)
        return {target.first/a.first, 0};
      return {0, 0}; //unsolvable
    }
    // just look at first dimension!
    pa = calculatePossibleAFactors(target.first, a.first, b.first);
    pb = calculatePossibleAFactors(target.first, b.first, a.first);
  } else {
    if (a.second == 0 && b.second == 0)
      return {0, 0}; //unsolvable
    if (target.second < a.second && target.second < b.second)
      return {0, 0}; //unsolvable
    // Step 1: calculate factors for a and b separately
    pa = calculatePossibleAFactors(target, a, b);
    pb = calculatePossibleAFactors(target, b, a);
  }
  // Step 2: calculate new equation
  std::pair<long,long> newA = {a.first*pa.second, a.second*pa.second};
  std::pair<long,long> newB = {b.first*pb.second, b.second*pb.second};
  long newtargetX = target.first - a.first*pa.first - b.first*pb.first;
  long newtargetY = target.second - a.second*pa.first - b.second*pb.first;
  // Step 3: recursively use calculateVectorCombination
  std::pair<long,long> sol;
  if (b.first == 0 && b.second == 0)
    sol = {0, 0};
  else sol = calculateVectorCombination({newtargetX, newtargetY}, newA, newB);
  // Step 4: test solution (unsolvable?)
  sol = {pa.first+sol.first*pa.second, pb.first+sol.second*pb.second};
  long soltestX = a.first*sol.first + b.first*sol.second;
  long soltestY = a.second*sol.first + b.second*sol.second;
  if (target.first == soltestX && target.second == soltestY)
    return sol;
  return {0, 0};
}






long gcd(long a, long b) {
  if (b == 0L) return std::abs(a);
  return gcd(b, a % b);
}

long extended_gcd(long a, long b, long *x, long *y) {
  if (b == 0L) {
    *x = 1;
    *y = 0;
    return std::abs(a);
  }

  long x1, y1;
  long gcd = extended_gcd(b, a % b, &x1, &y1);

  *x = y1;
  *y = x1 - (a / b) * y1;

  return gcd;
}

bool isColinear(std::pair<long,long> a, std::pair<long,long> b) {
  if (a.first == 0 || b.first == 0) {
    if (a.first == b.first) {
      if (a.second == 0) return b.second == 0;
      if (b.second == 0) return false;
      if (a.second < b.second) return b.second % a.second == 0;
      return a.second % b.second == 0;
    }
    return false;
  }
  if (a.second == 0 || b.second == 0) {
    if (a.second == b.second) {
      if (a.first < b.first) return b.first % a.first == 0;
      return a.first % b.first == 0;
    }
    return false;
  }
  if (a.first < b.first) {
    if (a.first % b.first != 0) return false;
    if (a.second % b.second != 0) return false;
    return b.first / a.first == b.second / a.second;
  } else {
    if (b.first % a.first != 0) return false;
    if (b.second % a.second != 0) return false;
    return (a.first / b.first == a.second / b.second);
  }
}
