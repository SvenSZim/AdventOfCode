"""
A program to convert the content of the txt into usable data
for the main program
"""
from typing import Any
from abc import ABC, abstractmethod
from enum import Enum

from os import path

this_path = path.dirname(path.abspath(__file__))
file_path = path.join(this_path, "data/data.txt")

rawdata: str
with open(file_path, 'r') as data:
    rawdata = data.read()


class Storage_File(ABC):
    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def to_str(self, depth: int) -> str:
        pass


class Directory(Storage_File):
    name: str
    parent: 'Directory'
    children: list[Storage_File]

    def __init__(self, name: str = '/', parent: 'Directory' = None) -> None:
        self.name = name
        self.children = []
        self.parent = parent

    def add_children(self, children: Storage_File) -> None:
        self.children.append(children)

    def get_all_subfolder(self) -> list['Directory']:
        return [sf for sf in self.children if type(sf) is Directory]

    def get_subfolder(self, name: str) -> 'Directory':
        for child in self.children:
            if type(child) is Directory and child.name == name:
                return child
        print(f'Subfolder: {name} not found')
        return self

    def get_parent(self) -> 'Directory':
        return self.parent

    def get_size(self) -> int:
        return sum([child.get_size() for child in self.children])

    def to_str(self, depth: int = 0) -> str:
        s: str = ' ' * depth * 2
        s += '- ' + self.name + '(dir, size=' + str(self.get_size()) + ')'
        for child in self.children:
            s += '\n' + child.to_str(depth+1)
        return s

    def __str__(self) -> str:
        return self.to_str()


class File(Storage_File):
    size: int

    def __init__(self, size: int) -> None:
        self.size = size

    def get_size(self) -> int:
        return self.size

    def to_str(self, depth: int) -> str:
        s: str = ' ' * depth * 2
        s += '- (file, size=' + str(self.size) + ')'
        return s


def convert_data_for_puzzle_one() -> Directory:
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

    root: Directory = Directory()
    cfile: Directory = root
    for cmd in rawdata.splitlines():
        cmd_type: Command_Type
        cmd_args: Any
        cmd_type, cmd_args = convert_command(cmd)
        match cmd_type:
            case Command_Type.NONE:
                continue
            case Command_Type.MOVEUP:
                cfile = cfile.get_parent()
            case Command_Type.MOVEDOWN:
                cfile = cfile.get_subfolder(cmd_args)
            case Command_Type.CREATEFIL:
                cfile.add_children(File(cmd_args))
            case Command_Type.CREATEDIR:
                cfile.add_children(Directory(cmd_args, cfile))

    return root


def main() -> None:
    """
    Function for testing purposes
    """
    print(convert_data_for_puzzle_one())


if __name__ == '__main__':
    main()
