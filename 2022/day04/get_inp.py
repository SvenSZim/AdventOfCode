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


def convert_data_for_puzzle_one() -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """
    converts the data into a list of 2-tuple of range-tuples, where the first
    number represents the start of the range and the second one the end

    Returns:
        list[tuple[tuple[int, int], tuple[int, int]]]: list of 2-tuples of range-tuples
    """
    def convert_raw_range(raw_range: str) -> tuple[int, int]:
        """
        converts the raw-string-data of format "A-B" (where A,B: int) into the
        corresponding range tuple [A, B]

        Args:
            raw_range: str

        Returns:
            tuple[int, int]: corresponding range tuple
        """
        raw_start: str
        raw_end: str
        raw_start, raw_end = raw_range.split('-')
        try:
            return (int(raw_start), int(raw_end))
        except ValueError:
            print(f'Invalid range-tuple: {raw_range}')
            return (0, 0)

    range_pairs: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for raw_row in rawdata.splitlines():
        raw_range1: str
        raw_range2: str
        raw_range1, raw_range2 = raw_row.split(',')
        range1: tuple[int, int] = convert_raw_range(raw_range1)
        range2: tuple[int, int] = convert_raw_range(raw_range2)
        range_pairs.append((range1, range2))
    return range_pairs


def main() -> None:
    """
    Function for testing purposes
    """
    print(convert_data_for_puzzle_one())


if __name__ == '__main__':
    main()
