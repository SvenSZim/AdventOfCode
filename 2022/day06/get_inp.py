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


def convert_data_for_puzzle_one() -> str:
    """
    functions as outsorcing of reading in the one string of characters
    of the input data

    Returns:
        str: first row in data
    """
    return rawdata.splitlines()[0]


def main() -> None:
    """
    Function for testing purposes
    """
    print(convert_data_for_puzzle_one())


if __name__ == '__main__':
    main()
