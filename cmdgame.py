#!/usr/bin/env python3

import state

class Game(object):
    piece_msg = "Player {}, choose a piece for the opponent to place: "
    square_msg = "Player {}, choose a square on which to place the piece: "
    
    def __init__(self):
        # Creates a new state with empty board and full pool of pieces
        self._state = state.State()
        self._current_player = 0
    
    def start(self):
        # Print initial state of board and pieces
        self._print_board()
        self._print_pieces()
        while not self._game_over():
            # Prompts user for piece
            piece = self._prompt_piece()
            # Pick piece, modify state
            self._state.pick_piece(piece)
            # XOR to switch between players 0 and 1
            self._current_player ^= 1
            # Prompts user for square
            row, col = self._prompt_square()
            # Place piece, modify state
            self._state.place_piece(row, col)
            # Print board and pieces
            self._print_board()
            self._print_pieces()
    
    def _prompt_piece(self):
        # Expects an input formed as a string of four bits, e.g. "0101"
        piece_str = input(self.piece_msg.format(self._current_player+1))
        while True:
            if len(piece_str) != 4:
                piece_str = input("Must be four bits, try again: ")
                continue
            if not all(c in "01" for c in piece_str):
                piece_str = input("Must be four bits, try again: ")
                continue
            piece = int(piece_str, base=2)
            if piece not in self._state.pieces:
                piece_str = input("Piece is already played, try again: ")
                continue
            return piece
    
    def _prompt_square(self):
        # Expects an input formed as a string of two coordinates, e.g. "23"
        square_str = input(self.square_msg.format(self._current_player+1))
        while True:
            if len(square_str) != 2 or not square_str.isdigit():
                square_str = input("Provide two coordinates, try again: ")
                continue
            row, col = [int(x) for x in square_str]
            if not (1 <= row <= 4 and 1 <= col <= 4):
                square_str = input("Must be in interval [1,4], try again: ")
                continue
            row, col = row-1, col-1
            if self._state.square(row, col) is not None:
                square_str = input("Square is occupied, try again: ")
                continue
            return row, col
    
    def _game_over(self):
        if self._state.has_winner():
            print("Player {} wins!".format(self._current_player+1))
            return True
        if self._state.is_draw():
            print("No pieces left, nobody wins!")
            return True
        return False
    
    def _print_board(self):
        print("BOARD:")
        for row in self._state.board:
            for col in row:
                print(self._to_4bit_str(col) if col is not None else "----", 
                      end=" ")
            print()
    
    def _print_pieces(self):
        print("PIECES:")
        print("{", end=" ")
        for piece in self._state.pieces:
            print(self._to_4bit_str(piece), end=" ")
        print("}")
    
    def _to_4bit_str(self, num):
        return format(num, '04b')



def main():
    g = Game()
    g.start()

# If file is called from command line, run main() function
if __name__ == "__main__":
    main()
