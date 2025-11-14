"""
main program for solving puzzle 1 & 2 of day 5
"""

from get_inp import crate_stack, move, convert_data_for_puzzle_one


def puzzle_one_sol() -> str:
    """
    applys the given move-operations on the start crate-stack and returns
    the crates that are on top at last

    Returns:
        str: crates that are on top after applying all operations
    """
    stacks: list[crate_stack]
    moves: list[move]

    stacks, moves = convert_data_for_puzzle_one()
    for cmove in moves:
        # apply move(s) to stack(s)
        amount: int
        source: int
        destination: int
        amount, source, destination = cmove
        stacks[destination].extend(stacks[source][-amount:][::-1])
        stacks[source] = stacks[source][:-amount]

    top_crates: str = ''
    for stack_idx, stack in enumerate(stacks):
        top_crates += stack[-1]
    return top_crates


def puzzle_two_sol() -> str:
    """
    applys the given move-operations, while keeping the order,
    on the start crate-stack and returns
    the crates that are on top at last

    Returns:
        str: crates that are on top after applying all operations
    """
    stacks: list[crate_stack]
    moves: list[move]

    stacks, moves = convert_data_for_puzzle_one()
    for cmove in moves:
        # apply move(s) to stack(s)
        amount: int
        source: int
        destination: int
        amount, source, destination = cmove
        stacks[destination].extend(stacks[source][-amount:])
        stacks[source] = stacks[source][:-amount]

    top_crates: str = ''
    for stack_idx, stack in enumerate(stacks):
        top_crates += stack[-1]
    return top_crates


def main() -> None:
    """
    Function for testing purposes
    """
    print(puzzle_one_sol())
    print(puzzle_two_sol())


if __name__ == '__main__':
    main()
