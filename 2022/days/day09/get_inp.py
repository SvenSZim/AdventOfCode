"""
A program to convert the content of the txt into usable data
for the main program
"""
from enum import Enum

from os import path

this_path = path.dirname(path.abspath(__file__))
file_path = path.join(this_path, "data/data.txt")

rawdata: str
with open(file_path, 'r') as data:
    rawdata = data.read()


class Direction(Enum):
    North = 0
    South = 1
    West = 2
    East = 3


def convert_data_for_puzzle_one() -> list[tuple[Direction, int]]:
    """
    converts the data into a list of movements with
    the given direction and the amount

    Returns:
        list[tuplle[Direction, int]]: list of movements (direction, amount)
    """
    movements: list[tuple[Direction, int]] = []
    for raw_row in rawdata.splitlines():
        raw_direction: str
        raw_amount: str
        try:
            raw_direction, raw_amount = raw_row.split()
            match raw_direction:
                case 'U':
                    movements.append((Direction.North, int(raw_amount)))
                case 'D':
                    movements.append((Direction.South, int(raw_amount)))
                case 'L':
                    movements.append((Direction.West, int(raw_amount)))
                case 'R':
                    movements.append((Direction.East, int(raw_amount)))
        except (IndexError, ValueError):
            print(f'Invalid data: {raw_row}')
    return movements


Movement = tuple[int, int]


def convert_data_for_puzzle_two() -> list[Movement]:
    """
    converts the data into a list of movements with
    the given direction and the amount

    Returns:
        list[Movement]: list of movements
    """
    movements: list[Movement] = []
    for raw_row in rawdata.splitlines():
        raw_direction: str
        raw_amount: str
        try:
            raw_direction, raw_amount = raw_row.split()
            match raw_direction:
                case 'U':
                    movements.append((-int(raw_amount), 0))
                case 'D':
                    movements.append((int(raw_amount), 0))
                case 'L':
                    movements.append((0, -int(raw_amount)))
                case 'R':
                    movements.append((0, int(raw_amount)))
        except (IndexError, ValueError):
            print(f'Invalid data: {raw_row}')
    return movements


def main() -> None:
    """
    Function for testing purposes
    """
    print(convert_data_for_puzzle_one())


if __name__ == '__main__':
    main()
