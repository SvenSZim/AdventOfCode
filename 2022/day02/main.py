"""
main program for solving puzzle 1 & 2 of day 2
"""

from get_inp import Move, convert_data_for_puzzle_one


def puzzle_one_sol() -> int:
    """
    calculates the total score of Rock-Paper-Scissors with the given
    rules by puzzle one if following the strategy guides written in the
    data and interpreting it as C1: Opponent-Move, C2: My-Move

    Returns:
        int: the total score
    """
    # Idx1: his choice, Idx2: my choice
    outcome: list[list[int]] = [[3, 6, 0], [0, 3, 6], [6, 0, 3]]
    rounds: list[tuple[Move, Move]] = convert_data_for_puzzle_one()
    total_score: int = 0
    for opponent_move, my_move in rounds:
        total_score += outcome[opponent_move.value-1][my_move.value-1] + \
            my_move.value
    return total_score


def puzzle_two_sol() -> int:
    """
    calculates the total score of Rock-Paper-Scissors with the given
    rules by puzzle two if following the strategy guides written in the
    data and interpreting it as C1: Opponent-Move, C2: Outcome

    Returns:
        int: the total score
    """
    # Idx1: his choice, Idx2: outcome
    outcome: list[list[int]] = [[3, 4, 8], [1, 5, 9], [2, 6, 7]]
    rounds: list[tuple[Move, Move]] = convert_data_for_puzzle_one()
    total_score: int = 0
    for opponent_move, my_move in rounds:
        total_score += outcome[opponent_move.value-1][my_move.value-1]
    return total_score


def main() -> None:
    """
    Function for testing purposes
    """
    print(puzzle_one_sol())
    print(puzzle_two_sol())


if __name__ == '__main__':
    main()
