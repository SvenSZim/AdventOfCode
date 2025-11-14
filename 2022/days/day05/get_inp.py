"""
A program to convert the content of the txt into usable data
for the main program
"""
from os import path

this_path = path.dirname(path.abspath(__file__))
file_path = path.join(this_path, "data/data.txt")

rawdata: str
with open(file_path, 'r') as data:
    rawdata = data.read()


crate_stack = list[str]
move = tuple[int, int, int]  # amount, from, to


def convert_data_for_puzzle_one() -> tuple[list[crate_stack], list[move]]:
    """
    converts and extracts the necessary informations from the data like the
    start configuration of the crate-stacks and the list of moves

    Returns:
        tuple[list[crate_stack], list[move]]: start configuration of crate-stacks, list of moves
    """
    # Step 1: extract the start configuration:
    # Step 1.1: find the max height of the crate-stacks of the start config
    max_start_crate_height: int = 0
    for row_nr, raw_row in enumerate(rawdata.splitlines()):
        if not len(raw_row):
            # Empty row separates list of moves from start config
            max_start_crate_height = row_nr - 1
            break

    # Step 1.2: find number of stacks
    number_of_stacks: int = len(
        rawdata.splitlines()[max_start_crate_height].split())

    # Step 1.3: generate stacks
    stacks: list[crate_stack] = [[] for _ in range(number_of_stacks)]
    # append crates back to front
    for raw_row in rawdata.splitlines()[:max_start_crate_height]:
        # row-format: "[A] [B] [C] ...":
        for crate_idx, crate in enumerate([char for column, char in enumerate(raw_row) if column % 4 == 1]):
            if crate != ' ':
                stacks[crate_idx].append(crate)
    # Step 1.4: invert stacks (bottom element at pos 0)
    stacks = [x[::-1] for x in stacks]

    # Step 2: extract the move-list
    moves: list[move] = []
    for raw_row in rawdata.splitlines()[max_start_crate_height+2:]:
        try:
            raw_amount: int
            raw_from: int
            raw_to: int
            _, raw_amount, _, raw_from, _, raw_to = raw_row.split()
            moves.append((int(raw_amount), int(raw_from)-1, int(raw_to)-1))
        except ValueError:
            print(f'Invalid data: {raw_row}')

    return stacks, moves


def main() -> None:
    """
    Function for testing purposes
    """
    print(convert_data_for_puzzle_one())


if __name__ == '__main__':
    main()
