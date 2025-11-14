"""
main program for solving puzzle 1 & 2 of day 10
"""

from get_inp import Operation, convert_data_for_puzzle_one


def puzzle_one_sol() -> int:
    """
    calculates the value of the register X at specific times (cycles: 20, 60, 100, ... [+40])
    and returns the sum of the corresponding signal strengths (cycle counter * register value)

    Returns:
        int: sum of signal strengths
    """
    operations: list[tuple[Operation, int | None]]
    operations = convert_data_for_puzzle_one()

    register_value: int = 1  # register starts with value 1
    cycle_count: int = 1

    signal_strength_sum: int = 0

    for operation_type, operation_argument in operations:
        match operation_type:
            case Operation.NOOP:
                cycle_count += 1  # noop takes 1 cycle
            case Operation.ADD:
                if cycle_count % 40 == 19:
                    # specific time is in between operation:
                    signal_strength_sum += register_value * (cycle_count + 1)

                register_value += operation_argument
                cycle_count += 2  # adding takes 2 cycles

        if cycle_count % 40 == 20:
            # check for specific times
            signal_strength_sum += register_value * cycle_count

    return signal_strength_sum


def puzzle_two_sol() -> list[str]:
    """
    calculates the generated image from the operations by setting the sprite
    to the register position and drawing the corresponding pixel at the position
    given by the cycle count

    Returns:
        list[str]: corresponding rows of pixels (strings of #. of 1, 0)
    """
    def get_pixel_value_from_buffer_and_cycle(buffer: int, cycle: int) -> str:
        """
        calculates the curresponding pixel value from the current buffer and
        cycle-count values

        Args:
            buffer (int): current buffer value
            cycle (int): current cycle-count value

        Returns:
            str: corresponding pixel value
        """
        column_pixel_idx: int = cycle % 40
        if abs(buffer - column_pixel_idx) < 2:
            return '#'
        else:
            return '.'

    operations: list[tuple[Operation, int | None]]
    operations = convert_data_for_puzzle_one()

    register_value: int = 1  # register starts with value 1
    cycle_count: int = 0

    screen_image: list[str] = []
    current_row: str = ''

    for operation_type, operation_argument in operations:
        current_row += get_pixel_value_from_buffer_and_cycle(
            register_value, cycle_count)
        match operation_type:
            case Operation.NOOP:
                cycle_count += 1  # noop takes 1 cycle
            case Operation.ADD:
                cycle_count += 1
                current_row += get_pixel_value_from_buffer_and_cycle(
                    register_value, cycle_count)
                if cycle_count % 40 == 0:
                    # specific time is in between operation:
                    screen_image.append(current_row)
                    current_row = ''
                cycle_count += 1
                register_value += operation_argument

        if cycle_count % 40 == 0:
            # check for specific times
            screen_image.append(current_row)
            current_row = ''

    return screen_image


def main() -> None:
    """
    Function for testing purposes
    """
    print(puzzle_one_sol())
    sol2: list[str] = puzzle_two_sol()
    for row in sol2:
        print(row)


if __name__ == '__main__':
    main()
