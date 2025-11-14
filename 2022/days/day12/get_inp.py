"""
A program to convert the content of the txt into usable data
for the main program
"""
from os import path
from numpy import array

this_path = path.dirname(path.abspath(__file__))
file_path = path.join(this_path, "data/data.txt")

rawdata: str
with open(file_path, 'r') as data:
    rawdata = data.read()


def convert_data_for_puzzle_one() -> array:
    """
    function for converting the input data into a height-matrix

    Returns:
        array: 2D matrix of height-levels (0-25)
                         & start: -1, end: 26
    """
    height_matrix: list[list[int]] = []

    def converter(x: str) -> int:
        """
        converts a char into its corresponding height value
        """
        if ord(x) < ord('a'):
            match x:
                case 'S':
                    return -1
                case 'E':
                    return 26
                case _:
                    print(f'Invalid data: {x}')
        return ord(x) - ord('a')

    for raw_row in rawdata.splitlines():
        height_matrix.append(list(map(converter, raw_row)))
    return array(height_matrix)


def main() -> None:
    """
    Function for testing purposes
    """
    print(convert_data_for_puzzle_one())


if __name__ == '__main__':
    main()
