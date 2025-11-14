"""
main program for solving puzzle 1 & 2 of day 12
"""
from numpy import array
from get_inp import convert_data_for_puzzle_one


def puzzle_one_sol() -> int:
    """
    finds the shortest path through the height map from start to end
    by using a D* pathsolving algorithm variant

    Returns:
        int: fewest steps required for getting from start to end
    """
    height_map: array = convert_data_for_puzzle_one()
    min_step_map: array
    min_step_map = array([[-1 for _ in height_row]
                         for height_row in height_map])

    start_pos: tuple[int, int]
    end_pos: tuple[int, int]
    for y, row in enumerate(height_map):
        for x, v in enumerate(row):
            match v:
                case -1:
                    row[x] = 0  # start pos has height 0
                    start_pos = (y, x)
                case 26:
                    row[x] = 25  # end pos has height 25
                    end_pos = (y, x)

    min_step_map[start_pos] = 0
    unchecked_open_positions: list[tuple[int, int]] = [start_pos]
    while len(unchecked_open_positions) > 0:
        new_open_positions: list[tuple[int, int]] = []
        for position in unchecked_open_positions:
            # check all positions that are accessable from position
            for yOffset in range(-1, 2):
                for xOffset in range(-1, 2):

                    if abs(yOffset) + abs(xOffset) != 1:
                        # just straight steps
                        continue

                    new_pos: tuple[int, int] = \
                        (position[0] + yOffset,
                         position[1] + xOffset)

                    if (new_pos[0] < 0 or new_pos[0] >= len(height_map) or
                            new_pos[1] < 0 or new_pos[1] >= len(height_map[0])):
                        # new pos outside the grid
                        continue

                    if min_step_map[new_pos] != -1:
                        # new pos is already accessed
                        continue

                    # new position is still open
                    # check if position height is reachable
                    current_height: int = \
                        height_map[position]
                    new_height: int = \
                        height_map[new_pos]
                    if new_height - current_height > 1:
                        # new position height not reachable
                        continue

                    # set needed step amount of new pos to one more than
                    # needed step amount for current pos
                    min_step_map[new_pos] = min_step_map[position] + 1
                    new_open_positions.append(new_pos)

        # check if end position got reached
        if min_step_map[end_pos] != -1:
            # if reached -> exit out
            break

        # set new positions to check as the new found open positions
        unchecked_open_positions = new_open_positions

    return min_step_map[end_pos]


def puzzle_two_sol() -> int:
    """
    finds the shortest path through the height map from end to closest
    lowest elevation point possible ('a') by using a D* pathsolving
    algorithm variant

    idea:
    basically algorithm as in puzzle_one just in reverse:
    start with end point and search backwards for the 'closest' point
    with lowest elevation

    Returns:
        int: fewest steps required for getting from end to lowest elevation
    """
    height_map: array = convert_data_for_puzzle_one()
    min_step_map: array
    min_step_map = array([[-1 for _ in height_row]
                         for height_row in height_map])

    end_pos: tuple[int, int]
    for y, row in enumerate(height_map):
        for x, v in enumerate(row):
            match v:
                case -1:
                    row[x] = 0  # start pos has height 0
                case 26:
                    row[x] = 25  # end pos has height 25
                    end_pos = (y, x)

    min_step_map[end_pos] = 0
    unchecked_open_positions: list[tuple[int, int]] = [end_pos]
    while len(unchecked_open_positions) > 0:
        new_open_positions: list[tuple[int, int]] = []
        for position in unchecked_open_positions:
            # check all positions that are accessable from position
            for yOffset in range(-1, 2):
                for xOffset in range(-1, 2):

                    if abs(yOffset) + abs(xOffset) != 1:
                        # just straight steps
                        continue

                    new_pos: tuple[int, int] = \
                        (position[0] + yOffset,
                         position[1] + xOffset)

                    if (new_pos[0] < 0 or new_pos[0] >= len(height_map) or
                            new_pos[1] < 0 or new_pos[1] >= len(height_map[0])):
                        # new pos outside the grid
                        continue

                    if min_step_map[new_pos] != -1:
                        # new pos is already accessed
                        continue

                    # new position is still open
                    # check if position height is reachable
                    current_height: int = \
                        height_map[position]
                    new_height: int = \
                        height_map[new_pos]
                    # reverse logic to puzzle_one...
                    if current_height - new_height > 1:
                        # new position height not reachable
                        continue

                    # set needed step amount of new pos to one more than
                    # needed step amount for current pos
                    min_step_map[new_pos] = min_step_map[position] + 1

                    # check if lowest elevation is already reached
                    if new_height == 0:
                        return min_step_map[new_pos]
                    new_open_positions.append(new_pos)

        # set new positions to check as the new found open positions
        unchecked_open_positions = new_open_positions

    # could not find a possible way to a lowest elevatino
    return -1


def main() -> None:
    """
    Function for testing purposes
    """
    print(puzzle_one_sol())
    print(puzzle_two_sol())


if __name__ == '__main__':
    main()
