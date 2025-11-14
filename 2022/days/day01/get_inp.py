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


def convert_data_for_puzzle_one() -> list[int]:
    """
    Converts the text data into a list of integers where
    each row of text will be converted to into an integer
    and each block of text will be summed up.

    Return:
        list[int]: List of sums of all blocks in input data
    """
    block_sums: list[int] = []
    current_block_sum: int = 0
    for row in rawdata.splitlines():
        if not len(row) and current_block_sum:
            # empty row -> end of block
            block_sums.append(current_block_sum)
            current_block_sum = 0
        else:
            try:
                current_block_sum += int(row)
            except ValueError:
                print(f'Invalid data: {row}')
    return block_sums


def main() -> None:
    """
    Function for testing purposes
    """
    print(convert_data_for_puzzle_one())


if __name__ == '__main__':
    main()
