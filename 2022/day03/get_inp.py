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


def convert_data_for_puzzle_one() -> list[tuple[str, str]]:
    """
    converts the data into a list of tuple of strings where each tuple
    represents the backpack with its two compartments

    Returns:
        list[tuple[str, str]]: list of backpacks with two compartments each
    """
    backpacks: list[tuple[str, str]] = []
    for itemlist in rawdata.splitlines():
        compartment_size: int = len(itemlist)//2
        compartment1: str = itemlist[:compartment_size]
        compartment2: str = itemlist[compartment_size:]
        backpacks.append((compartment1, compartment2))
    return backpacks


def convert_data_for_puzzle_two() -> list[tuple[str, str, str]]:
    """
    converts the data into a list of tuple of strings where each tuple
    represents the group of three backpack

    Returns:
        list[tuple[str, str, str]]: list of group of backpacks
    """
    backpacks: list[str] = rawdata.splitlines()
    groups: list[tuple[str, str, str]] = []
    for group_number in range(0, len(backpacks), 3):
        backpack1: str = backpacks[group_number]
        backpack2: str = backpacks[group_number+1]
        backpack3: str = backpacks[group_number+2]
        groups.append((backpack1, backpack2, backpack3))
    return groups


def main() -> None:
    """
    Function for testing purposes
    """
    print(convert_data_for_puzzle_one())
    print(convert_data_for_puzzle_two())


if __name__ == '__main__':
    main()
