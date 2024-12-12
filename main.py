""" Solver for hi-q board game """
from board_manager import Board
from solver import get_any_solution

def main():
    """ Top-level solver method """
    print("Main")
    b = Board()

    solution = get_any_solution(b)
    print(f"solution: {solution}")

if __name__ == "__main__":
    main()
