"""
main program for solving puzzle 1 & 2 of day 1
"""

from get_inp import convert_data_for_puzzle_one


def puzzle_one_sol() -> int:
    """
    Finds the max sum of all the number-blocks in
    the given data

    Returns:
        int: max sum
    """
    number_block_sums: list[int] = convert_data_for_puzzle_one()
    return max(number_block_sums)


def puzzle_two_sol() -> int:
    """
    Finds the sum of the three number-blocks in the
    given data with the max sum

    Returns:
        int: sum of top three max sums
    """
    number_block_sums: list[int] = convert_data_for_puzzle_one()
    # trivial sol: sorting O(nlogn)
    # alternative: 3x max O(n)
    top_three_sums: list[int] = [0, 0, 0]  # 1, #2, #3
    for block_sum in number_block_sums:
        for nr, top_val in enumerate(top_three_sums):
            if block_sum > top_val:
                # block sum is new nr, nr -> nr + 1 etc.
                for swap_idx in range(2, nr, -1):  # back to front
                    top_three_sums[swap_idx] = top_three_sums[swap_idx-1]
                top_three_sums[nr] = block_sum
                break
    return sum(top_three_sums)


def main() -> None:
    """
    Function for testing purposes
    """
    print(puzzle_one_sol())
    print(puzzle_two_sol())


if __name__ == '__main__':
    main()
