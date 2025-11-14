"""
main program for solving puzzle 1 & 2 of day 4
"""

from get_inp import convert_data_for_puzzle_one


def puzzle_one_sol_trivial() -> int:
    """
    finds the amount of totally overlapping ranges by actually generating
    the number ranges and using set difference (inefficient for larger ranges)

    Returns:
        int: amount of totally overlapping ranges
    """
    range_pairs: list[tuple[tuple[int, int], tuple[int, int]]
                      ] = convert_data_for_puzzle_one()
    totally_overlapping_pairs: int = 0
    for range1, range2 in range_pairs:
        s1, e1 = range1
        s2, e2 = range2
        r1_without_r2: set[int] = set(
            range(s1, e1+1)).difference(set(range(s2, e2+1)))
        r2_without_r1: set[int] = set(
            range(s2, e2+1)).difference(set(range(s1, e1+1)))
        if not len(r1_without_r2) or not len(r2_without_r1):
            totally_overlapping_pairs += 1
    return totally_overlapping_pairs


def puzzle_one_sol_advanced() -> int:
    """
    finds the amount of totally overlapping ranges by comparing the range-
    limits

    Returns:
        int: amount of totally overlapping ranges
    """
    range_pairs: list[tuple[tuple[int, int], tuple[int, int]]
                      ] = convert_data_for_puzzle_one()
    totally_overlapping_pairs: int = 0
    for range1, range2 in range_pairs:
        start1: int
        start2: int
        end1: int
        end2: int
        start1, end1 = range1
        start2, end2 = range2
        if start1 <= start2 and end1 >= end2:
            # range1 includes range2
            totally_overlapping_pairs += 1
        elif start2 <= start1 and end2 >= end1:
            # range2 includes range1
            totally_overlapping_pairs += 1
    return totally_overlapping_pairs


def puzzle_two_sol() -> int:
    """
    finds the amount of overlapping ranges by comparing the range-
    limits

    Returns:
        int: amount of totally overlapping ranges
    """
    range_pairs: list[tuple[tuple[int, int], tuple[int, int]]
                      ] = convert_data_for_puzzle_one()
    overlapping_pairs: int = 0
    for range1, range2 in range_pairs:
        start1: int
        start2: int
        end1: int
        end2: int
        start1, end1 = range1
        start2, end2 = range2
        # easier to consider the not-overlapping-case:
        if not (end1 < start2 or end2 < start1):
            overlapping_pairs += 1
    return overlapping_pairs


def main() -> None:
    """
    Function for testing purposes
    """
    print(puzzle_one_sol_advanced())
    print(puzzle_two_sol())


if __name__ == '__main__':
    main()
