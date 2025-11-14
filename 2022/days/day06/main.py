"""
main program for solving puzzle 1 & 2 of day 6
"""

from get_inp import convert_data_for_puzzle_one


def find_first_appearance_of_fully_unique_window(input_stream: str, window_size: int) -> int:
    """
    finds the position of the first appearance of n fully distinct characters
    in a row out of the given data stream

    Returns:
        int: position of first fully distinct n-wide character window
    """
    for window_start in range(len(input_stream) - window_size + 1):
        window: str = input_stream[window_start:window_start+window_size]
        if len(set(window)) == window_size:
            return window_start + window_size
    print('No suitable window found')
    return -1


def puzzle_one_sol() -> int:
    """
    finds the position of the first appearance of 4 fully distinct characters
    in a row out of the given data stream

    Returns:
        int: position of first fully distinct 4-wide character window
    """
    return find_first_appearance_of_fully_unique_window(convert_data_for_puzzle_one(), 4)


def puzzle_two_sol() -> int:
    """
    finds the position of the first appearance of 14 fully distinct characters
    in a row out of the given data stream

    Returns:
        int: position of first fully distinct 14-wide character window
    """
    return find_first_appearance_of_fully_unique_window(convert_data_for_puzzle_one(), 14)


def main() -> None:
    """
    Function for testing purposes
    """
    print(puzzle_one_sol())
    print(puzzle_two_sol())


if __name__ == '__main__':
    main()
