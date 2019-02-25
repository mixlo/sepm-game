#!/usr/bin/env python3

import state
import threading


class Game(object):
    timeout = False
    def __init__(self, player1=None, player2=None):
        # Creates a new state with empty board and full pool of pieces
        self._state = state.State()
        # Keep player instances in array
        self._players = [player1, player2]
        # Current player's index in array
        self._cp = 0
        self._winner = None
        self._loser = None

    @property
    def winner(self):
        return self._winner

    @property
    def loser(self):
        return self._loser

    def start(self):
        # Print initial state of board and pieces
        GameIO.print_state(self._state)
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

    def timeout_occured(self):
        self.timeout = True
    def start_with_timer(self, timeout_time):
        # Print initial state of board and pieces
        GameIO.print_state(self._state)
        while not self._game_over() and not self.timeout:
            # Prompt player for piece
            my_timer = threading.Timer(timeout_time, self.timeout_occured)
            my_timer.start()
    
            piece = self._players[self._cp].prompt_piece(self._state)
            my_timer.cancel()
            
            # Pick piece, modify state
            self._state.pick_piece(piece)
            # XOR to switch between players 0 and 1
            self._cp ^= 1
            # Prompt player for square
            my_timer = threading.Timer(timeout_time, self.timeout_occured)
            my_timer.start()

            row, col = self._players[self._cp].prompt_square(self._state)
            my_timer.cancel()

            # Place piece, modify state
            self._state.place_piece(row, col)
            # Print board and pieces
            GameIO.print_state(self._state)
            GameIO.print_state(self._state)
        if self.timeout:
            return "Timeout"
        else:
            return "Game Over"

    def reset(self):
        self._state = state.State()
        self._cp = 0
        self._winner = None
        self._loser = None
    
    def get_winner(self):
        if not self._state.is_draw():
            return self._winner.name
        return False
    
    def _game_over(self):
        if self._state.has_winner():
            self._winner = self._players[self._cp]
            self._loser = self._players[self._cp ^ 1]
            GameIO.print_winner(self._winner.name)
            return True
        if self._state.is_draw():
            GameIO.print_draw()
            return True
        return False

class GameIO(object):
    @classmethod
    def print_state(cls, state):
        cls._print_board(state.board)
        cls._print_pieces(state.pieces)
    
    @classmethod
    def print_winner(cls, name):
        print("{} wins!".format(name))

    @classmethod
    def print_draw(cls):
        print("Draw!")

    @classmethod
    def _print_board(cls, board):
        print("BOARD:")
        for row in board:
            for col in row:
                print(format(col, '04b') if col is not None else "----", 
                      end=" ")
            print()

    @classmethod
    def _print_pieces(cls, pieces):
        print("PIECES:")
        print("{", end=" ")
        for piece in pieces:
            print(format(piece, '04b'), end=" ")
        print("}")
