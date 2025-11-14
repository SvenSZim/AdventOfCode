"""
main program for solving puzzle 1 & 2 of day 11
"""

from get_inp import DataMonkey, convert_data_for_puzzle_one
from get_inp import FactorizedNumber, DataMonkey2, convert_data_for_puzzle_two


def get_monkey_business(monkeys: list[DataMonkey | DataMonkey2],
                        number_of_moves: int, worry_decrease_factor: int = 3) -> int:
    """
    calculates the level of monkey-business after n moves by simulating the
    rounds of monkey-tossing and determinating the most active monkeys

    Args:
        monkeys (list[DataMonkey]): list of monkeys with their start config
        number_of_moves (int): the number of moves to be considered
        worry_decrease_factor (int): the factor by which the worry level
                                        decreases per inspection

    Returns:
        int: level of monkey business after the given amount of rounds
    """
    if len(monkeys) < 2:
        return 0
    # monkeys take turn in ascending order of number
    monkeys.sort(key=lambda x: x.number)

    monkey_activity: list[int] = [0 for _ in monkeys]
    for _ in range(number_of_moves):
        for monkey_idx, monkey in enumerate(monkeys):
            for item_idx, item in enumerate(monkey.holding_items):
                monkey_activity[monkey_idx] += 1
                new_item = int | FactorizedNumber
                if isinstance(monkey, DataMonkey):
                    new_item = \
                        monkey.worry_operation(item) // worry_decrease_factor
                else:
                    new_item = monkey.worry_operation(item)
                monkey.holding_items[item_idx] = new_item
                monkeys[monkey.throw_operation(
                    new_item)].holding_items.append(new_item)
            monkey.holding_items = []

    # find most active monkey
    ac1: int  # highest monkey activity
    ac2: int  # secont highest monkey activity
    if monkey_activity[0] > monkey_activity[1]:
        ac1 = monkey_activity[0]
        ac2 = monkey_activity[1]
    else:
        ac2 = monkey_activity[0]
        ac1 = monkey_activity[1]
    if len(monkey_activity) > 2:
        for ma in monkey_activity[2:]:
            if ma > ac1:
                ac2 = ac1
                ac1 = ma
            elif ma > ac2:
                ac2 = ma
    return ac1 * ac2


def puzzle_one_sol() -> int:
    """
    Returns:
        int: level of monkey business after 20 round
    """
    return get_monkey_business(convert_data_for_puzzle_one(), 20, 3)


def puzzle_two_sol() -> int:
    """
    Optimizations to sol1:
        Using FactorizedNumber instead of normal int:
        FactorizedNumber is a class used specifically for working
        with modular-rings where addition and multiplication can
        be simplified to work in a constant space.
        It works when a number just has to be divided by a specific
        divisor and otherwise just gets altered by addition or
        multiplication.
        It works by reducing the number into its modular form (modulo
        the number that gets divided by). Addition and multiplication
        works just the same then:
        (a + b) % m = (a % m) + (b % m)
        (a * b) % m = (a % m) * (b % m)
        In this case you can store all modulo-rings for each item
        reducing the calculation-range for each item into constant space.

    Returns:
        int: level of monkey business after 10_000 round
    """
    return get_monkey_business(convert_data_for_puzzle_two(), 10_000)


def main() -> None:
    """
    Function for testing purposes
    """
    print(puzzle_one_sol())
    print(puzzle_two_sol())


if __name__ == '__main__':
    main()
