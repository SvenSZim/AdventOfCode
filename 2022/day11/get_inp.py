"""
A program to convert the content of the txt into usable data
for the main program
"""
from typing import Callable, Any
from dataclasses import dataclass

from os import path

this_path = path.dirname(path.abspath(__file__))
file_path = path.join(this_path, "data/data.txt")

rawdata: str
with open(file_path, 'r') as data:
    rawdata = data.read()


@dataclass
class DataMonkey:
    """
    class to store the relevant data of a monkey
    """
    # monkey number
    number: int
    # list of worrylevels of the items the mokey is holding
    holding_items: list[int]
    # function of how the monkey modifies the worrylevel
    worry_operation: Callable[int, int]
    # function of to-which monkey a item is thrown depending on its worry level
    throw_operation: Callable[int, int]


def convert_data_for_puzzle_one() -> list[DataMonkey]:
    """
    function to convert the raw-data into the monkeys with their specific
    behaviors like their start-items, their operation and their test

    Returns:
        list[DataMonkey]: list of the monkeys
    """
    monkeys: list[DataMonkey] = []
    current_monkey: list[Any] = []

    raw_lines: list[str] = rawdata.splitlines()
    for raw_line_idx, raw_line in enumerate(raw_lines):
        if len(raw_line) == 0 and len(current_monkey) == 4:
            # build and store current_monkey
            monkeys.append(DataMonkey(*current_monkey))
            current_monkey = []
        elif len(current_monkey) > 3:
            # current_monkey already finished
            continue
        else:
            try:
                # construct current_monkey
                raw_items: list[str] = raw_line.split()
                match len(current_monkey):
                    case 0:
                        # read data as number of the monkey
                        current_monkey.append(int(raw_items[-1][:-1]))
                    case 1:
                        # read data as list of starting items
                        starting_items: list[int] = []
                        for item in raw_items[2:]:
                            starting_items.append(int(item.strip(',')))
                        current_monkey.append(starting_items)
                    case 2:
                        # read data as worry-operation
                        def default(x):
                            return 0
                        operation: Callable[int, int] = default
                        read_operation: bool = False  # ignore everything before '='
                        for item_idx, item in enumerate(raw_items):
                            if item == '=':
                                read_operation = True
                                if raw_items[item_idx+1] == 'old':
                                    def op1(x):
                                        return x
                                    operation = op1
                                else:
                                    constant: int = int(raw_items[item_idx+1])

                                    def op2(x, k=constant):
                                        return k
                                    operation = op2
                            elif read_operation:
                                match item:
                                    case '+':
                                        if raw_items[item_idx+1] == 'old':
                                            def op3(x, op=operation):
                                                return op(x) + x
                                            operation = op3
                                        else:
                                            constant: int = int(
                                                raw_items[item_idx+1])

                                            def op4(x, op=operation, k=constant):
                                                return op(x) + k
                                            operation = op4
                                    case '*':
                                        if raw_items[item_idx+1] == 'old':
                                            def op5(x, op=operation):
                                                return op(x) * x
                                            operation = op5
                                        else:
                                            constant: int = int(
                                                raw_items[item_idx+1])

                                            def op6(x, op=operation, k=constant):
                                                return op(x) * k
                                            operation = op6
                        current_monkey.append(operation)
                    case 3:
                        # read data as throw-operation
                        divisor: int = int(raw_items[-1])
                        opt1: int = int(raw_lines[raw_line_idx+1].split()[-1])
                        opt2: int = int(raw_lines[raw_line_idx+2].split()[-1])

                        def testFunction(x, divisor=divisor, opt1=opt1, opt2=opt2):
                            return [opt2, opt1][not (x % divisor)]
                        current_monkey.append(testFunction)
                        # (lambda x: [opt1, opt2][not (x % divisor)]))

            except ValueError:
                print(f'Invalid data: {raw_line}')

    if len(current_monkey) == 4:
        monkeys.append(DataMonkey(*current_monkey))

    return monkeys


class FactorizedNumber:
    # static-var:
    numbers_to_consider: list[int] = []
    # obj-var:
    relative_behavior: list[int]

    def __init__(self, n: int) -> None:
        self.relative_behavior = [
            0 for _ in FactorizedNumber.numbers_to_consider]
        for idx, number in enumerate(FactorizedNumber.numbers_to_consider):
            self.relative_behavior[idx] = n % number

    def __str__(self) -> str:
        return str([(r, n)
                    for r, n in zip(self.relative_behavior,
                                    FactorizedNumber.numbers_to_consider)])

    def __add__(self, other: int) -> 'FactorizedNumber':
        if isinstance(other, int):
            for idx, ntc in enumerate(FactorizedNumber.numbers_to_consider):
                self.relative_behavior[idx] = \
                    (self.relative_behavior[idx] + other) % ntc
            return self
        elif isinstance(other, FactorizedNumber):
            for idx, ntc in enumerate(FactorizedNumber.numbers_to_consider):
                self.relative_behavior[idx] = \
                    (self.relative_behavior[idx] +
                     other.relative_behavior[idx]) % ntc
            return self
        return NotImplemented

    def __mul__(self, other: int) -> 'FactorizedNumber':
        if isinstance(other, int):
            for idx, ntc in enumerate(FactorizedNumber.numbers_to_consider):
                self.relative_behavior[idx] = \
                    (self.relative_behavior[idx] * other) % ntc
            return self
        elif isinstance(other, FactorizedNumber):
            for idx, ntc in enumerate(FactorizedNumber.numbers_to_consider):
                self.relative_behavior[idx] = \
                    (self.relative_behavior[idx] *
                     other.relative_behavior[idx]) % ntc
            return self
        return NotImplemented

    def __mod__(self, other: int) -> int:
        if isinstance(other, int):
            for ntc, val in zip(FactorizedNumber.numbers_to_consider, self.relative_behavior):
                if ntc == other:
                    return val
            print(f'Missing value: {other} in {
                  FactorizedNumber.numbers_to_consider}')
        return NotImplemented


@dataclass
class DataMonkey2:
    """
    class to store the relevant data of a monkey
    Optimizations just store the factors
    """
    # monkey number
    number: int
    # list of worrylevels of the items the mokey is holding
    holding_items: list[FactorizedNumber]
    # function of how the monkey modifies the worrylevel
    worry_operation: Callable[FactorizedNumber, FactorizedNumber]
    # function of to-which monkey a item is thrown depending on its worry level
    throw_operation: Callable[FactorizedNumber, int]


def convert_data_for_puzzle_two() -> list[DataMonkey2]:
    """
    function to convert the raw-data into the monkeys with their specific
    behaviors like their start-items, their operation and their test

    Returns:
        list[DataMonkey2]: list of the monkeys
    """
    raw_lines: list[str] = rawdata.splitlines()
    # find relevant factors...
    relevant_factors: list[int] = []
    for raw_line in raw_lines:
        raw_items: list[str] = raw_line.split()
        if len(raw_items) > 0 and raw_items[0] == 'Test:':
            relevant_factors.append(int(raw_items[-1]))
    FactorizedNumber.numbers_to_consider = relevant_factors

    monkeys: list[DataMonkey2] = []
    current_monkey: list[Any] = []

    for raw_line_idx, raw_line in enumerate(raw_lines):
        if len(raw_line) == 0 and len(current_monkey) == 4:
            # build and store current_monkey
            monkeys.append(DataMonkey2(*current_monkey))
            current_monkey = []
        elif len(current_monkey) > 3:
            # current_monkey already finished
            continue
        else:
            try:
                # construct current_monkey
                raw_items: list[str] = raw_line.split()
                match len(current_monkey):
                    case 0:
                        # read data as number of the monkey
                        current_monkey.append(int(raw_items[-1][:-1]))
                    case 1:
                        # read data as list of starting items
                        starting_items: list[int] = []
                        for item in raw_items[2:]:
                            starting_items.append(FactorizedNumber(int(item.strip(','))))
                        current_monkey.append(starting_items)
                    case 2:
                        # read data as worry-operation
                        def default(x):
                            return 0
                        operation: Callable[FactorizedNumber, FactorizedNumber] = default
                        read_operation: bool = False  # ignore everything before '='
                        for item_idx, item in enumerate(raw_items):
                            if item == '=':
                                read_operation = True
                                if raw_items[item_idx+1] == 'old':
                                    def op1(x):
                                        return x
                                    operation = op1
                                else:
                                    constant: int = int(raw_items[item_idx+1])

                                    def op2(x, k=constant):
                                        return k
                                    operation = op2
                            elif read_operation:
                                match item:
                                    case '+':
                                        if raw_items[item_idx+1] == 'old':
                                            def op3(x, op=operation):
                                                return op(x) + x
                                            operation = op3
                                        else:
                                            constant: int = int(
                                                raw_items[item_idx+1])

                                            def op4(x, op=operation, k=constant):
                                                return op(x) + k
                                            operation = op4
                                    case '*':
                                        if raw_items[item_idx+1] == 'old':
                                            def op5(x, op=operation):
                                                return op(x) * x
                                            operation = op5
                                        else:
                                            constant: int = int(
                                                raw_items[item_idx+1])

                                            def op6(x, op=operation, k=constant):
                                                return op(x) * k
                                            operation = op6
                        current_monkey.append(operation)
                    case 3:
                        # read data as throw-operation
                        divisor: int = int(raw_items[-1])
                        opt1: int = int(raw_lines[raw_line_idx+1].split()[-1])
                        opt2: int = int(raw_lines[raw_line_idx+2].split()[-1])

                        def testFunction(x, divisor=divisor, opt1=opt1, opt2=opt2):
                            return [opt2, opt1][not (x % divisor)]
                        current_monkey.append(testFunction)
                        # (lambda x: [opt1, opt2][not (x % divisor)]))

            except ValueError:
                print(f'Invalid data: {raw_line}')

    if len(current_monkey) == 4:
        monkeys.append(DataMonkey2(*current_monkey))

    return monkeys


def main() -> None:
    """
    Function for testing purposes
    """
    monkeys = convert_data_for_puzzle_one()
    for m in monkeys:
        print(f'\nMonkey {m.number}\nStarting items: {m.holding_items}\nOperation: {
              [(x, m.worry_operation(x)) for x in range(11)]}\nTest: {
              [(x, m.throw_operation(x)) for x in range(25)]}')

    monkeys = convert_data_for_puzzle_two()
    print(f'\n\n\nNTC!: {FactorizedNumber.numbers_to_consider}')
    for m in monkeys:
        print(f'\nMonkey {m.number}\nStarting items: {[str(i) for i in m.holding_items]}\nOperation: {
              [(x, m.worry_operation(x)) for x in range(11)]}\nTest: {
              [(x, m.throw_operation(x)) for x in range(25)]}')


if __name__ == '__main__':
    main()
