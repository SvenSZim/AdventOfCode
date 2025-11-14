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


class Operation(Enum):
    """
    class for storing which type of operation is being done by the
    CPU and how many cycles the operation takes
    """
    NOOP = 1  # overation.value = number of cycles the operation takes
    ADD = 2


def convert_data_for_puzzle_one() -> list[tuple[Operation, int | None]]:
    """
    converts the data into the list of operations being executed by the CPU

    Returns:
        list[tuple[Operation, int | None]]:
            list of operations (operation type, optional arguments)
    """
    operations: list[tuple[Operation, int | None]] = []
    for raw_operation in rawdata.splitlines():
        operations_args: list[str] = raw_operation.split()
        match len(operations_args):
            case 1:
                operations.append((Operation.NOOP, None))
            case 2:
                operations.append((Operation.ADD, int(operations_args[1])))
    return operations


def main() -> None:
    """
    Function for testing purposes
    """
    print(convert_data_for_puzzle_one())


if __name__ == '__main__':
    main()
