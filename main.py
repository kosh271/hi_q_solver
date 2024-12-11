""" Solver for hi-q board game """
from board_manager import Board, Direction

def main():
    """ Top-level solver method """
    print("Main")
    b = Board()
    b.print_board()

    b.make_move(1, 3, Direction.DOWN)
    b.print_board()
    print(f"Moves: {b.moves}")
    b.undo_last_move()
    b.print_board()

if __name__ == "__main__":
    main()
