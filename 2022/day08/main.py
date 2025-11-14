"""
main program for solving puzzle 1 & 2 of day 8
"""
from get_inp import convert_data_for_puzzle_one

from typing import Any
from enum import Enum


def puzzle_one_sol() -> int:
    """
    finds the amount of visible trees in the tree matrix given by the data
    a tree is visible if on any axis (x,y) there are just smaller trees
    (smaller numbers) than the tree itself (in Time: O(n^3))

    Returns:
        int: number of visible trees
    """
    tree_matrix: list[list[int]] = convert_data_for_puzzle_one()

    def tree_is_visible(tree_matrix: list[list[int]], tree_pos: tuple[int, int]) -> bool:
        """
        returns if the tree at the given position in the given tree matrix is
        visible from any direction

        Returns:
            bool: is tree visible
        """
        tree_posX: int
        tree_posY: int
        tree_posY, tree_posX = tree_pos
        north_trees: list[int] = [tree_matrix[y][tree_posX]
                                  for y in range(0, tree_posY)] + [-1]
        south_trees: list[int] = [tree_matrix[y][tree_posX]
                                  for y in range(tree_posY+1, len(tree_matrix))] + [-1]
        west_trees: list[int] = [tree_matrix[tree_posY][x]
                                 for x in range(0, tree_posX)] + [-1]
        east_trees: list[int] = [tree_matrix[tree_posY][x]
                                 for x in range(tree_posX+1, len(tree_matrix[0]))] + [-1]
        return any([tree_matrix[tree_posY][tree_posX] > max(tree_row)
                    for tree_row in [north_trees, south_trees, west_trees, east_trees]])

    all_coordinates: list[list[tuple[int, int]]]
    all_coordinates = [[(y, x) for x in range(len(tree_matrix[0]))]
                       for y in range(len(tree_matrix))]

    visible_trees: list[list[bool]]
    visible_trees = [map(lambda x: tree_is_visible(tree_matrix, x), tree_row)
                     for tree_row in all_coordinates]

    return sum([sum(visible_row) for visible_row in visible_trees])


def puzzle_one_sol_improved():
    """
    finds the amount of visible trees in the tree matrix given by the data
    a tree is visible if on any axis (x,y) there are just smaller trees
    (smaller numbers) than the tree itself (in Time: O(n^2))

    Returns:
        int: number of visible trees
    """

    tree_matrix: list[list[int]] = convert_data_for_puzzle_one()
    tree_matrix_size: tuple[int, int] = (len(tree_matrix), len(tree_matrix[0]))
    tree_is_visible_matrix: list[list[bool]] = [
        [False for _ in row] for row in tree_matrix]  # Initialize to False

    class Direction(Enum):
        East_West = 0
        North_South = 1

    class StepDirection(Enum):
        Normal = 0
        Reversed = 1

    def get_set_item(matrix: list[list[Any]], row_idx: int, row_iterator_idx: int,
                     direction: Direction, reversed: StepDirection,
                     set_item: bool = False) -> Any | None:
        sizes: tuple[int, int] = (len(matrix), len(matrix[0]))
        idxR: int
        idxC: int

        if reversed.value:
            # Reversed
            idxR = sizes[0]-row_iterator_idx-1
            idxC = row_idx
        else:
            # Normal
            idxR = row_iterator_idx
            idxC = row_idx

        if direction.value:
            # North_South
            if set_item:
                matrix[idxR][idxC] = True
            else:
                return matrix[idxR][idxC]
        else:
            # East_West
            if set_item:
                matrix[idxC][idxR] = True
            else:
                return matrix[idxC][idxR]

    for direction in [Direction.East_West, Direction.North_South]:
        for step_direction in [StepDirection.Normal, StepDirection.Reversed]:
            for row_idx in range(tree_matrix_size[direction.value]):
                max_tree_found: int = -1  # all trees on the edge are visible
                for tree_idx in range(tree_matrix_size[1-direction.value]):
                    tree: int = get_set_item(tree_matrix, row_idx, tree_idx,
                                             direction, step_direction)
                    if tree > max_tree_found:
                        # Tree is visible
                        max_tree_found = tree  # found tree is blocking all
                        #                        trees behind (in the direction)
                        #                        that are smaller than itself
                        #                        -> new bound for visible trees
                        #                               (in that direction)
                        get_set_item(tree_is_visible_matrix, row_idx, tree_idx,
                                     direction, step_direction, set_item=True)
                        # mark tree as visible so it doesnt get countet twice
                        # when visible from another direction
    return sum([sum(row) for row in tree_is_visible_matrix])


def puzzle_two_sol() -> int:
    """
    finds the tree in the tree matrix given by the data with the highest
    scenary-score which is calculated by multiplying the viewing distances
    in all four direction (O(n^3))

    Returns:
        int: maximum scenary-score for all trees
    """
    tree_matrix: list[list[int]] = convert_data_for_puzzle_one()

    def get_scenary_score(matrix: list[list[int]],
                          pos: tuple[int, int]) -> int:
        """
        calculates the scenary-score of the tree at the given position in
        the given tree-matrix (forest) (O(n))

        Returns:
            int: scenary-score of given tree
        """
        matrix_sizes: tuple[int, int] = (len(matrix), len(matrix[0]))
        posR: int
        posC: int
        posR, posC = pos
        tree: int = matrix[posR][posC]
        direction_scores: list[int] = [0] * 4
        direction_blocked: list[bool] = [False] * 4
        try_viewing_distance: int = 0
        while not all(direction_blocked):
            try_viewing_distance += 1
            # north
            if not direction_blocked[0] and posR - try_viewing_distance >= 0:
                direction_scores[0] += 1
                if matrix[posR - try_viewing_distance][posC] >= tree:
                    direction_blocked[0] = True
            else:
                direction_blocked[0] = True
            # south
            if not direction_blocked[1] and posR + try_viewing_distance < matrix_sizes[0]:
                direction_scores[1] += 1
                if matrix[posR + try_viewing_distance][posC] >= tree:
                    direction_blocked[1] = True
            else:
                direction_blocked[1] = True
            # west
            if not direction_blocked[2] and posC - try_viewing_distance >= 0:
                direction_scores[2] += 1
                if matrix[posR][posC - try_viewing_distance] >= tree:
                    direction_blocked[2] = True
            else:
                direction_blocked[2] = True
            # east
            if not direction_blocked[3] and posC + try_viewing_distance < matrix_sizes[1]:
                direction_scores[3] += 1
                if matrix[posR][posC + try_viewing_distance] >= tree:
                    direction_blocked[3] = True
            else:
                direction_blocked[3] = True
        return direction_scores[0] * direction_scores[1] * (
            direction_scores[2] * direction_scores[3])

    all_coordinates: list[list[tuple[int, int]]]
    all_coordinates = [[(y, x) for x in range(len(tree_matrix[0]))]
                       for y in range(len(tree_matrix))]

    scenary_scores: list[list[int]] = [
        map(lambda x: get_scenary_score(tree_matrix, x), tree_row)
        for tree_row in all_coordinates]

    return max([max(row) for row in scenary_scores])


def main() -> None:
    """
    Function for testing purposes
    """
    print(puzzle_one_sol_improved())
    print(puzzle_two_sol())


if __name__ == '__main__':
    main()
