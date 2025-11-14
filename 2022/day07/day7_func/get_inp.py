"""
A program to convert the content of the txt into usable data
for the main program
"""
from typing import Any
from enum import Enum

from os import path

this_path = path.dirname(path.abspath(__file__))
file_path = path.join(this_path, "data/data.txt")

rawdata: str
with open(file_path, 'r') as data:
    rawdata = data.read()


def get_folder_from_path(root: list[...], path: list[int]) -> list[...]:
    if len(path):
        try:
            return get_folder_from_path(root[path[0]], path[1:])
        except IndexError:
            print('Error in folder trace')
    return root


def convert_data_for_puzzle_one() -> list[...]:
    """
    converts the list of terminal commands and readouts into the corresponding
    folder-file-structure by using the dummy-classes from above

    Returns:
        Directory: root file with folderstructure given by the data
    """
    class Command_Type(Enum):

        NONE = 0
        MOVEDOWN = 1
        MOVEUP = 2
        CREATEDIR = 5
        CREATEFIL = 6

    def convert_command(raw_command: str) -> tuple[Command_Type, Any]:
        """
        converts a stringstream into the corresponding terminal command

        Args:
            raw_command: str

        Returns:
            Command_Type: terminal command type
            Any: Additional arguments of command
        """
        raw_command = raw_command.split()
        match raw_command[0]:
            case '$':
                if raw_command[1] == 'ls':
                    return Command_Type.NONE, None  # ignore
                elif raw_command[2] == '..':
                    return Command_Type.MOVEUP, None
                else:
                    return Command_Type.MOVEDOWN, raw_command[2]
            case 'dir':
                return Command_Type.CREATEDIR, raw_command[1]  # add name
            case _:
                # add size (name is irrelevant)
                return Command_Type.CREATEFIL, int(raw_command[0])

    root: list[...] = []
    names: dict[str, int] = {}
    cfile: list[int] = []
    for cmd in rawdata.splitlines()[1:]:
        cmd_type: Command_Type
        cmd_args: Any
        cmd_type, cmd_args = convert_command(cmd)
        match cmd_type:
            case Command_Type.NONE:
                continue
            case Command_Type.MOVEUP:
                try:
                    cfile.pop(-1)
                except IndexError:
                    print('No more root.')
            case Command_Type.MOVEDOWN:
                cfile.append(names.get(str(cfile)+cmd_args))
            case Command_Type.CREATEFIL:
                get_folder_from_path(root, cfile).append(cmd_args)
            case Command_Type.CREATEDIR:
                cfolder: list[...] = get_folder_from_path(root, cfile)
                names[str(cfile)+cmd_args] = len(cfolder)
                cfolder.append([])
    return root


def main() -> None:
    """
    Function for testing purposes
    """
    print(convert_data_for_puzzle_one())


if __name__ == '__main__':
    main()
