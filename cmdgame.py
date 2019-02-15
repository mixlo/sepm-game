#!/usr/bin/env python3

import state

class Game(object):
    def __init__(self, player1, player2):
        # Creates a new state with empty board and full pool of pieces
        self._state = state.State()
        # Keep player instances in array
        self._players = [player1, player2]
        # Current player's index in array
        self._cp = 0
    
    def start(self):
        # Print initial state of board and pieces
        self._print_board()
        self._print_pieces()
        while not self._game_over():
            # Prompt player for piece
            piece = self._players[self._cp].prompt_piece(self._state)
            # Pick piece, modify state
            self._state.pick_piece(piece)
            # XOR to switch between players 0 and 1
            self._cp ^= 1
            # Prompt player for square
            row, col = self._players[self._cp].prompt_square(self._state)
            # Place piece, modify state
            self._state.place_piece(row, col)
            # Print board and pieces
            self._print_board()
            self._print_pieces()
    
    def _game_over(self):
        if self._state.has_winner():
            print("{} wins!".format(self._players[self._cp].name))
            return True
        if self._state.is_draw():
            print("Draw!")
            return True
        return False
    
    def _print_board(self):
        print("BOARD:")
        for row in self._state.board:
            for col in row:
                print(format(col, '04b') if col is not None else "----", 
                      end=" ")
            print()
    
    def _print_pieces(self):
        print("PIECES:")
        print("{", end=" ")
        for piece in self._state.pieces:
            print(format(piece, '04b'), end=" ")
        print("}")
