#!/usr/bin/env python3

import gameengine

class Player(object):
    # Returns the name of the player.
    @property
    def name(self):                raise NotImplementedError()
    # Prompts the player to select a piece for the opponent to place.
    # Returns an integer in range 0-15.
    def prompt_piece(self, state): raise NotImplementedError()
    # Prompts the player for the coordinates of a square in which to place the
    # currently held piece. Returns two integers in range 0-3.
    def prompt_move(self, state):  raise NotImplementedError()

class HumanPlayer(Player):
    _piece_msg = "{}, choose a piece for the opponent to place: "
    _square_msg = "{}, choose a square on which to place the piece: "
    
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def prompt_piece(self, state):
        # Expects an input formed as a string of four bits, e.g. "0101"
        piece_str = input(self._piece_msg.format(self._name))
        while True:
            if len(piece_str) != 4:
                piece_str = input("Must be four bits, try again: ")
                continue
            if not all(c in "01" for c in piece_str):
                piece_str = input("Must be four bits, try again: ")
                continue
            piece = int(piece_str, base=2)
            if piece not in state.pieces:
                piece_str = input("Piece is already played, try again: ")
                continue
            return piece
    
    def prompt_square(self, state):
        # Expects an input formed as a string of two coordinates, e.g. "23"
        square_str = input(self._square_msg.format(self._name))
        while True:
            if len(square_str) != 2 or not square_str.isdigit():
                square_str = input("Provide two coordinates, try again: ")
                continue
            row, col = [int(x) for x in square_str]
            if not (1 <= row <= 4 and 1 <= col <= 4):
                square_str = input("Must be in interval [1,4], try again: ")
                continue
            row, col = row-1, col-1
            if state.square(row, col) is not None:
                square_str = input("Square is occupied, try again: ")
                continue
            return row, col

class AIPlayer(Player):
    def __init__(self, name, difficulty):
        self._name = name
        self._ai = gameengine.AI(difficulty)

    @property
    def name(self):
        return self._name
    
    def prompt_piece(self, state):
        p = self._ai.choose_piece(state)
        print("AI {0} chose piece: {1:04b}".format(self._name, p))
        return p

    def prompt_square(self, state):
        s = self._ai.choose_square(state)
        print("AI {} chose square: {}{}".format(self._name, *[x+1 for x in s]))
        return s
