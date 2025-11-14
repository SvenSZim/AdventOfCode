"""
main program for solving puzzle 1 & 2 of day 3
"""

from get_inp import convert_data_for_puzzle_one, convert_data_for_puzzle_two


def puzzle_one_sol() -> int:
    """
    finds the duplicate element in the two backpack compartments
    for each backpack, converts the elements into their priorities and
    adds them up

    Returns:
        int: sum of priorities of duplicate items
    """
    backpacks: list[tuple[str, str]] = convert_data_for_puzzle_one()
    priority_sum: int = 0
    for compartment1, compartment2 in backpacks:
        duplicate_items: set[str] = set(
            compartment1).intersection(set(compartment2))
        duplicate_item: str = duplicate_items.pop()
        if ord(duplicate_item) >= ord('a'):
            priority_sum += ord(duplicate_item) - ord('a') + 1
        else:
            priority_sum += ord(duplicate_item) - ord('A') + 27
    return priority_sum


def puzzle_two_sol() -> int:
    """
    finds the duplicate element in the three backpacks of the group,
    converts the elements into their priorities and
    adds them up

    Returns:
        int: sum of priorities of duplicate items
    """
    groups: list[tuple[str, str, str]] = convert_data_for_puzzle_two()
    priority_sum: int = 0
    for backpack1, backpack2, backpack3 in groups:
        duplicate_items: set[str] = set(backpack1).intersection(
            set(backpack2)).intersection(set(backpack3))
        duplicate_item: str = duplicate_items.pop()
        if ord(duplicate_item) >= ord('a'):
            priority_sum += ord(duplicate_item) - ord('a') + 1
        else:
            priority_sum += ord(duplicate_item) - ord('A') + 27
    return priority_sum


def main() -> None:
    """
    Function for testing purposes
    """
    print(puzzle_one_sol())
    print(puzzle_two_sol())


if __name__ == '__main__':
    main()
