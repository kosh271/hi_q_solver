""" Handles high-level operations on the board """
from dataclasses import dataclass
from enum import Enum

BOARD_ROWS    = 7
BOARD_COLUMNS = 7


class Direction(Enum):
    "Enumerated jump directions"
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


@dataclass
class PegPosition:
    """ Peg manager """
    peg_present: bool
    is_empty: bool
    is_valid_position: bool

    def __init__(self, peg_present: bool | None=None):
        if peg_present is None:
            self.peg_present = False
            self.is_empty = False
            self.is_valid_position = False
        else:
            self.peg_present = peg_present
            self.is_empty = not peg_present
            self.is_valid_position = True

    def add_peg(self):
        """ Add a peg to a valid position """
        if not self.is_valid_position:
            raise ValueError("Not a valid location for a peg")
        if not self.is_empty:
            raise ValueError("Peg already present in this location - can't add")
        self.peg_present = True
        self.is_empty = False

    def remove_peg(self):
        """ Remove a peg from a valid position """
        if not self.is_valid_position:
            raise ValueError("Not a valid location for a peg")
        if not self.peg_present:
            raise ValueError("Peg not present in this location - can't remove")
        self.peg_present = False
        self.is_empty = True

    def as_char(self) -> str:
        """ Return character map for peg - useful when printing board """
        if not self.is_valid_position:
            return "  "
        elif self.peg_present:
            return " *"
        else:
            return " O"


class Board:
    """ 
    High-level hi-q board management 

    board[row][column]
    Appearance of initial board:
            * * *
            * * *
        * * * * * * *
        * * * O * * *
        * * * * * * *
            * * *
            * * *
    """
    def _generate_board(self):
        self.board = []

        # Initialize board with all invalid positions
        for _ in range(BOARD_ROWS):
            row = []
            for _ in range(BOARD_COLUMNS):
                row.append(PegPosition())
            self.board.append(row)

        # Configure rows [2:5]
        for row_index in range(2,5):
            for column_index in range(BOARD_COLUMNS):
                self.board[row_index][column_index] = PegPosition(True)

        # Configure columns [2:5]
        for column_index in range(2,5):
            for row_index in range(BOARD_ROWS):
                self.board[row_index][column_index] = PegPosition(True)

        # Clear middle peg
        self.board[3][3] = PegPosition(False)


    def _count_pegs(self):
        peg_count = 0
        for row in self.board:
            for position in row:
                if not position.is_valid_position:
                    continue
                if position.peg_present:
                    peg_count += 1

        return peg_count

    def __init__(self):
        self._generate_board()
        self.num_pegs = self._count_pegs()
        self.moves = []


    def print_board(self):
        """ print the board to the terminal """
        for row in self.board:
            for peg in row:
                print(peg.as_char(), end='')
            print()
        print(f"Total pegs: {self.num_pegs}")


    def get_peg(self, row_index: int, column_index: int) -> PegPosition:
        """ Gets the pegPosition information for the requested indexes """
        return self.board[row_index][column_index]


    def _generate_jump_and_target_coords(self,
                                         row_index: int,
                                         column_index: int,
                                         direction: Direction):
        # Configure coords
        if direction == Direction.UP:
            jump_coords   = (row_index - 1, column_index)
            target_coords = (row_index - 2, column_index)
        elif direction == Direction.RIGHT:
            jump_coords   = (row_index, column_index + 1)
            target_coords = (row_index, column_index + 2)
        elif direction == Direction.DOWN:
            jump_coords   = (row_index + 1, column_index)
            target_coords = (row_index + 2, column_index)
        elif direction == Direction.LEFT:
            jump_coords   = (row_index, column_index - 1)
            target_coords = (row_index, column_index - 2)
        else:
            raise ValueError("Unexpected direction value")

        return (jump_coords, target_coords, direction)


    def can_peg_move(self, row_index: int, column_index: int, direction: Direction) -> bool:
        """
        Checks to see if request move is a valid one for the selected peg
        Valid directions: 
        """
        jump_coords, target_coords, _ = \
            self._generate_jump_and_target_coords(row_index, column_index, direction)

        # Check for out of bounds
        if target_coords[0] < 0 or \
           target_coords[0] >= BOARD_ROWS or \
           target_coords[1] < 0 or \
           target_coords[1] >= BOARD_COLUMNS:
            return False

        # Verify peg exists to move
        if not self.board[row_index][column_index].is_valid_position or \
           not self.board[row_index][column_index].peg_present:
            return False

        # Verify peg exists to jump over
        if not self.board[jump_coords[0]][jump_coords[1]].is_valid_position or \
           not self.board[jump_coords[0]][jump_coords[1]].peg_present:
            return False

        # Verify move target is an open spot
        if not self.board[target_coords[0]][target_coords[1]].is_valid_position or \
           not self.board[target_coords[0]][target_coords[1]].is_empty:
            return False

        return True


    def make_move(self, row_index: int, column_index: int, direction: Direction):
        """
        Handle moving and removing of pegs
        """
        jump_coords, target_coords, decoded_direction = \
            self._generate_jump_and_target_coords(row_index, column_index, direction)

        # Remember our move
        self.moves.append((row_index, column_index, decoded_direction))

        # Move peg from current to 'target', remove peg we jumped
        self.board[       row_index]    [column_index].remove_peg()
        self.board[  jump_coords[0]][  jump_coords[1]].remove_peg()
        self.board[target_coords[0]][target_coords[1]].add_peg()

        # Manage peg count
        self.num_pegs -= 1


    def undo_last_move(self):
        """
        Revert last move in move list
        """
        # Remove last move from move list
        origin_row, origin_column, direction = self.moves.pop()

        # Undo the move
        jump_coords, target_coords, _ = \
            self._generate_jump_and_target_coords(origin_row, origin_column, direction)

        self.board[      origin_row][   origin_column].add_peg()
        self.board[  jump_coords[0]][  jump_coords[1]].add_peg()
        self.board[target_coords[0]][target_coords[1]].remove_peg()

        # Manage peg count
        self.num_pegs += 1
