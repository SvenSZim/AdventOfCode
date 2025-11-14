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


def convert_data_for_puzzle_one() -> list[list[int]]:
    """
    converts the grid of numbers given in the input data into a
    matrixform

    Returns:
        str: first row in data
    """
    tree_matrix: list[list[int]] = []
    for raw_row in rawdata.splitlines():
        tree_row: list[int] = []
        for char in raw_row:
            try:
                tree_row.append(int(char))
            except ValueError:
                print(f'Invalid char: {char}')
        tree_matrix.append(tree_row)
    return tree_matrix


def main() -> None:
    """
    Function for testing purposes
    """
    print(convert_data_for_puzzle_one())


if __name__ == '__main__':
    main()
