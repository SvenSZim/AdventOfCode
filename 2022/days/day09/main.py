"""
main program for solving puzzle 1 & 2 of day 9
"""

from get_inp import Direction, convert_data_for_puzzle_one, Movement, convert_data_for_puzzle_two

Position = tuple[int, int]


def puzzle_one_sol() -> int:
    """
    finds the amount of covered positions by the tail following
    the head moving as specified by the given data

    Returns:
        int: convered positions by the tail
    """
    movements: list[tuple[Direction, int]] = convert_data_for_puzzle_one()
    grid_size: tuple[int, int] = (350, 800)  # fixed grid size
    # store positions visited by tail
    visited_position_grid: list[bool] = [[False for _ in range(grid_size[1])]
                                         for _ in range(grid_size[0])]
    # initialize starting pos at center
    head_pos: Position
    tail_pos: Position
    head_pos = [grid_size[0]//2, grid_size[1]//2]  # start at middle
    tail_pos = [grid_size[0]//2, grid_size[1]//2]  # same pos as head
    visited_position_grid[tail_pos[0]][tail_pos[1]
                                       ] = True  # add start pos as visited

    for movement in movements:
        direction: Direction  # U: 0, D: 1, L: 2, R: 3
        amount: int
        direction, amount = movement
        movement_axis: int = direction.value // 2  # 0: up-down, 1: left-right
        non_movement_axis: int = 1-movement_axis
        movement_step_direction: int = 2 * (direction.value % 2) - 1  # -1 or 1
        """
        find visited positions:
        -------------------------

        consider moving right:
        ===============================================
        case 1:       | case 2:       | case 3:
        ... ... ...   | T.. ... ...   | ... ... ...
        TH. .TH ..T   | .H. .TH ..T   | .H. .TH ..T
        ... ... ...   | T.. ... ...   | ... ... ...
        tail visits   | tail visits   | tail visits
        same as head  | same as head  | same as head

        case 4:       | case 5:       | case 6:
        ... ... ...   | .T. .T. ...   | ..T ..T ..T
        .HT ..H ..T   | .H. ..H ..T   | .H. ..H ...
        ... ... ...   | .T. .T. ...   | ..T ..T ..T
        tail skips    | tail skips    | tail skips head
        head pos      | head pos      | pos and right
        ===============================================
        works same for all directions

        switch between:
        case 1-3: copy head movement one step behind
        case 4-5: copy head movement one step behind but from step 2 (ignore 1)
        case 6: copy head movement one step behind but from step 3 (ignore 1-2)

        detect cases:
        case 1-2: tail had a distance from 1 to the head
                  going against the movement-axis (relative distance -1)
        case   3: tail is on head (relative distance 0)
        case 4-5: tail has a distance from 1 to the head
                  going with the movement-axis (relative distance 1)
        case   6: tail has a distance from  2 to the head
                  going with the movement-axis (realtive distance 2)

        formel for relative offset (RO)
        RO = relative offset on movement-axis + offset on non-movement-axis
        """
        tail_relative_offset: int
        tail_relative_offset = (movement_step_direction *
                                (tail_pos[movement_axis] -
                                 head_pos[movement_axis]) +
                                abs(tail_pos[non_movement_axis] -
                                    head_pos[non_movement_axis]))

        # head always moves as stated
        # store head-start-pos
        prev_head_ax_pos: int = head_pos[movement_axis]
        # move head
        head_pos[movement_axis] += amount * \
            movement_step_direction

        # check if the constant sized grid is big enough
        # if (head_pos[movement_axis] < 0 or
        #        head_pos[movement_axis] >= grid_size[movement_axis]):
        #   print(f'Grid to small! {movement}')
        #   return -1

        # move tail along head movement
        static_pos: int = head_pos[non_movement_axis]
        for moving_pos in range(prev_head_ax_pos,
                                head_pos[movement_axis],
                                movement_step_direction):
            # check for needed skips
            match tail_relative_offset:
                case 1:
                    # RO=1 -> skip first head pos
                    if moving_pos == prev_head_ax_pos:
                        continue
                case 2:
                    # RO=2 -> skip first and second head pos
                    if (moving_pos == prev_head_ax_pos or
                        moving_pos == prev_head_ax_pos +
                            movement_step_direction):
                        continue
            tail_pos[non_movement_axis] = static_pos
            tail_pos[movement_axis] = moving_pos
            # set visited positions
            if movement_axis:
                visited_position_grid[static_pos][moving_pos] = True
            else:
                visited_position_grid[moving_pos][static_pos] = True

    # count all visited positions and return the sum
    return sum([sum(row) for row in visited_position_grid])


def sign(n: int) -> int:
    """
    calculates the sign of the given number

    Args:
        n (int): a number

    Returns:
        int: -1 if number is negative, 1 if number is positive and 0 if neither
    """
    if n > 0:
        return 1
    elif n < 0:
        return -1
    return 0


def get_tail_movement_from_head_movement(relative_tail_pos: Position, movement: Movement) -> tuple[Position, list[Movement]]:
    """
    calculates the corresponding movement of the tail from the movement
    of the head (single direction only)  and the relative position of
    the tail to the head

    Args:
        relative_tail_pos (Position): the relative position of tail to head
        movement (Movement): the movement of the head

    Returns:
        Position: the new relative position of the tail to the head
        list[Movement]: the corresponding primitive movements of the tail (in order)
    """
    relative_head_pos_after_movement: Position  # rel. head pos to tail pos a.mov.
    relative_head_pos_after_movement = [-relative_tail_pos[0] + movement[0],
                                        -relative_tail_pos[1] + movement[1]]
    # check if head moves enough for the tail to move along
    if abs(relative_head_pos_after_movement[0]) < 2 and \
            abs(relative_head_pos_after_movement[1]) < 2:
        return [-relative_head_pos_after_movement[0],
                -relative_head_pos_after_movement[1]], []

    # switch for the different types of movement possible
    # 0: no movement, 1: horizontal or vertical movement, 2: diagonal movement
    movement_type: int = abs(sign(movement[0])) + abs(sign(movement[1]))
    match movement_type:
        case 0:
            # head does not move -> tail does not move
            return relative_tail_pos, []
        case 1:
            # vertical/horizontal movement
            offset_from_movement: int = min(
                abs(relative_head_pos_after_movement[0]),
                abs(relative_head_pos_after_movement[1])
            )
            match offset_from_movement:
                case 0:
                    # tail just moves alongside head
                    tail_movement: Movement
                    if relative_head_pos_after_movement[0] != 0:
                        tail_movement = (
                            relative_head_pos_after_movement[0] -
                            sign(relative_head_pos_after_movement[0]),
                            0
                        )
                    else:
                        tail_movement = (
                            0,
                            relative_head_pos_after_movement[1] -
                            sign(relative_head_pos_after_movement[1])
                        )
                    tail_end_pos: Position = [
                        -sign(relative_head_pos_after_movement[0]),
                        -sign(relative_head_pos_after_movement[1])
                    ]
                    return tail_end_pos, [tail_movement]
                case 1:
                    # tail needs to jump to the movement-axis of the head
                    if max(abs(relative_head_pos_after_movement[0]),
                           abs(relative_head_pos_after_movement[1])) > 2:
                        # jump + movement along axis
                        if abs(relative_head_pos_after_movement[0]) < 2:
                            return [0, -sign(relative_head_pos_after_movement[1])], [
                                (sign(relative_head_pos_after_movement[0]),
                                 sign(relative_head_pos_after_movement[1])),
                                (0,
                                 relative_head_pos_after_movement[1] -
                                 2 * sign(relative_head_pos_after_movement[1]))
                            ]
                        else:
                            return [-sign(relative_head_pos_after_movement[0]), 0], [
                                (sign(relative_head_pos_after_movement[0]),
                                 sign(relative_head_pos_after_movement[1])),
                                (relative_head_pos_after_movement[0] -
                                 2 * sign(relative_head_pos_after_movement[0]),
                                 0)
                            ]
                    else:
                        # just the jump
                        if abs(relative_head_pos_after_movement[0]) < 2:
                            return [0, -sign(relative_head_pos_after_movement[1])], [
                                (sign(relative_head_pos_after_movement[0]),
                                 sign(relative_head_pos_after_movement[1])),
                            ]
                        else:
                            return [-sign(relative_head_pos_after_movement[0]), 0], [
                                (sign(relative_head_pos_after_movement[0]),
                                 sign(relative_head_pos_after_movement[1])),
                            ]
        case 2:
            # diagonal movement
            offset_from_movement: int = abs(
                abs(relative_head_pos_after_movement[0]) -
                abs(relative_head_pos_after_movement[1])
            )
            match offset_from_movement:
                case 0:
                    # tail just moves alongside head
                    return [-sign(relative_head_pos_after_movement[0]),
                            -sign(relative_head_pos_after_movement[1])], [
                        (relative_head_pos_after_movement[0] -
                         sign(relative_head_pos_after_movement[0]),
                         relative_head_pos_after_movement[1] -
                         sign(relative_head_pos_after_movement[1]))]
                case 1:
                    # tail moves alongside head but with offset
                    if (abs(relative_head_pos_after_movement[0]) >
                            abs(relative_head_pos_after_movement[1])):
                        return [-sign(relative_head_pos_after_movement[0]), 0], [
                            (abs(relative_head_pos_after_movement[1]) *
                             sign(relative_head_pos_after_movement[0]),
                             relative_head_pos_after_movement[1])]
                    else:
                        return [0, -sign(relative_head_pos_after_movement[1])], [
                            (relative_head_pos_after_movement[0],
                             abs(relative_head_pos_after_movement[0]) *
                             sign(relative_head_pos_after_movement[1]))]
                case 2:
                    # tail needs to adjust axis and then moves alongside head with offset
                    if (abs(relative_head_pos_after_movement[0]) >
                            abs(relative_head_pos_after_movement[1])):
                        return [-sign(relative_head_pos_after_movement[0]), 0], [
                            (sign(relative_head_pos_after_movement[0]), 0),
                            (abs(relative_head_pos_after_movement[1]) *
                             sign(relative_head_pos_after_movement[0]),
                             relative_head_pos_after_movement[1])]
                    else:
                        return [0, -sign(relative_head_pos_after_movement[1])], [
                            (0, sign(relative_head_pos_after_movement[1])),
                            (relative_head_pos_after_movement[0],
                             abs(relative_head_pos_after_movement[0]) *
                             sign(relative_head_pos_after_movement[1]))]
    print('This should not be reached')
    return [0, 0], []


def puzzle_two_sol() -> int:
    """
    finds the amount of covered positions by the elongated tail
    following the head moving as specified by the given data

    Returns:
        int: convered positions by the last tail element
    """

    movements: list[Movement] = convert_data_for_puzzle_two()
    grid_size: tuple[int, int] = (350, 800)  # fixed grid size
    # store positions visited by last tail element
    visited_position_grid: list[bool] = [[False for _ in range(grid_size[1])]
                                         for _ in range(grid_size[0])]
    tail_length: int = 10
    # initialize starting positions at center
    positions: list[Position]
    positions = [[grid_size[0]//2, grid_size[1]//2]
                 for _ in range(tail_length)]
    visited_position_grid[positions[-1][0]][positions[-1]
                                            # add start pos as visited
                                            [1]] = True

    for movement in movements:
        """
        idea:
        the movement of the tail-elements is dependant on the movement of the
        previous tail-part, which implies a one by one calculation of the
        movements

        for simplification the element-movements are split into their atom-movements
        like:
        north-east, north, north-west, east, west, south-east, south and south-west

        movements are therefore a combination of these atom-movements
        """
        # each element-movement a list of atom-movements
        element_movements: list[list[Movement] | None]
        # movements are dependant on prev-movements so they get init to null
        element_movements = [None for _ in range(tail_length)]
        # first element (head) moves as stated by the data
        element_movements[0] = [movement]  # data-movements are atom-movements

        # calculate movements one by one starting from the beginning
        for current_head_idx in range(tail_length-1):
            current_head_movements: list[Movement]
            current_head_movements = element_movements[current_head_idx]

            current_head_pos: Position = positions[current_head_idx]
            current_tail_pos: Position = positions[current_head_idx+1]

            current_tail_offset: Position = [
                current_tail_pos[0] - current_head_pos[0],
                current_tail_pos[1] - current_head_pos[1]
            ]
            current_tail_movement: list[Movement] = []

            for current_head_movement in current_head_movements:
                # calculate corresponding tail movement one by one
                # from the atom-movements of the head
                new_tail_movement: list[Movement]
                current_tail_offset, new_tail_movement = get_tail_movement_from_head_movement(
                    current_tail_offset, current_head_movement)
                current_tail_movement.extend(new_tail_movement)

                # move head
                current_head_pos[0] += current_head_movement[0]
                current_head_pos[1] += current_head_movement[1]

            # movement of current tail is head movement for next tail
            element_movements[current_head_idx+1] = current_tail_movement

        # store positions visited by end of tail
        end_tail_position: Position = positions[-1]
        for tail_end_movement in element_movements[-1]:
            tail_end_Ymovement: int
            tail_end_Xmovement: int
            tail_end_Ymovement, tail_end_Xmovement = tail_end_movement
            # apply movements one by one
            for y_movement in [sign(tail_end_Ymovement)
                               for _ in range(
                    max(abs(tail_end_Ymovement), 1))]:
                for x_movement in [sign(tail_end_Xmovement)
                                   for _ in range(
                        max(abs(tail_end_Xmovement), 1))]:
                    end_tail_position[0] += y_movement
                    end_tail_position[1] += x_movement
                    visited_position_grid[end_tail_position[0]
                                          ][end_tail_position[1]] = True

    # count all visited positions and return the sum
    return sum([sum(row) for row in visited_position_grid])


def main() -> None:
    """
    Function for testing purposes
    """
    print(puzzle_one_sol())
    print(puzzle_two_sol())


if __name__ == '__main__':
    main()
