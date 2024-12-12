"""
Contains solvers for hi-q board
"""
from board_manager import Board, Direction


def make_next_move(board: Board) -> bool:
    """Search for any available moves
    If no moves are possible, backtrack and search until another untested move is located
    Return: True on move made, False on no more moves found
    """
    # Search for an available move, make it if possible
    for row_index in range(board.max_rows):
        for column_index in range(board.max_columns):
            d = Direction.UP
            while d is not None:
                if board.can_peg_move(row_index, column_index, Direction(d)):
                    board.make_move(row_index, column_index, Direction(d))
                    return True
                d = Direction.get_next_direction(d)

    # No valid move located, backtrack
    while len(board.moves) != 0:
        last_row, last_column, last_direction = board.moves[-1]
        board.undo_last_move()

        # Try other directions for this peg
        next_direction = Direction.get_next_direction(last_direction)
        while next_direction is not None:
            if board.can_peg_move(last_row, last_column, next_direction):
                board.make_move(last_row, last_column, next_direction)
                return True

            next_direction = Direction.get_next_direction(next_direction)

        # Search for an available move 'after' last_move, make it if possible
        for row_index in range(last_row, board.max_rows):
            for column_index in range(board.max_columns):
                if (row_index+1 == board.max_rows) and (column_index+1 <= board.max_columns):
                    break
                if (row_index == last_row) and (column_index <= last_column):
                    continue

                for d in range(4):
                    if board.can_peg_move(row_index, column_index, Direction(d)):
                        board.make_move(row_index, column_index, Direction(d))
                        return True

    # No more moves
    return False




def get_any_solution(board: Board):
    "Search for a solution and return the first result"
    while board.num_pegs != 1:
        board.print_board_clean()
        print()
        if not make_next_move(board):
            raise ValueError("No solutions found!")

    print("Solution found!")
    return board.moves
