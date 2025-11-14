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


class Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


def convert_data_for_puzzle_one() -> list[tuple[Move, Move]]:
    """
    converts the data into a list of tuple with the first column
    being the first move and the second column of the data being
    the second move

    Returns:
        list[tuple[Move, Move]]: list of tuple with Opponent Move - You Move
    """
    converter: dict[str, Move] = {'X': Move.ROCK, 'A': Move.ROCK,
                                  'Y': Move.PAPER, 'B': Move.PAPER,
                                  'Z': Move.SCISSORS, 'C': Move.SCISSORS}
    rounds: list[tuple[Move, Move]] = []
    for raw_row in rawdata.splitlines():
        try:
            raw_move1: str = raw_row[0]
            raw_move2: str = raw_row[2]
            move1: Move = converter[raw_move1]  # Intentially not using .get()
            move2: Move = converter[raw_move2]
            rounds.append((move1, move2))
        except IndexError:
            print(f'Invalid data: {raw_row}')
            continue
    return rounds


def main() -> None:
    """
    Function for testing purposes
    """
    print(convert_data_for_puzzle_one())


if __name__ == '__main__':
    main()
