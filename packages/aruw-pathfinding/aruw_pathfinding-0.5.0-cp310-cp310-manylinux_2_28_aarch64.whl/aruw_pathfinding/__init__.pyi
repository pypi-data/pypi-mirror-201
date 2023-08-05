from typing import List, Tuple


class AStar:
    """
    An object to hold the AStar algorithm.
    """

    def __init__(self) -> None: ...

    @classmethod
    def get_path(
        self,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        occupied_squares: List[List[Tuple[int, int]]],
        grid_size: Tuple[int, int],
    ) -> List[Tuple[int, int]]:
        """
        Gets the path as a list of squares.
        """
        ...


class AStarV2:
    """
    An object to hold the AStarV2 algorithm.
    """

    def __init__(
        self,
        occupied_squares: List[List[Tuple[int, int]]],
        grid_size: Tuple[int, int],
    ) -> None: ...

    @classmethod
    def get_path(
        self,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        occupied_squares: List[List[Tuple[int, int]]],
        old_occupied_squares: List[List[Tuple[int, int]]],
    ) -> List[Tuple[int, int]]:
        """
        Gets the path as a list of squares.
        """
        ...


class DStar:
    """
    An object to hold the DStar algorithm.
    """

    def __init__(
        self,
        occupied_squares: List[List[Tuple[int, int]]],
        grid_size: Tuple[int, int],
    ) -> None: ...

    @classmethod
    def get_path(
        self,
        start: Tuple[int, int],
        goal: Tuple[int, int],
        occupied_squares: List[List[Tuple[int, int]]],
    ) -> List[Tuple[int, int]]:
        """
        Gets the path as a list of squares.
        """
        ...