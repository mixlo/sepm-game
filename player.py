#!/usr/bin/env python3

from gameengine import AI
from gameplatform import GameIO

class AbsPlayer(object):
    def __init__(self, name):
        self._name = name

    # Returns the name of the player.
    @property
    def name(self):
        return self._name

    # Prompts the player to select a piece for the opponent to place.
    # Returns an integer in range 0-15.
    def prompt_piece(self, state): raise NotImplementedError()
    
    # Prompts the player for the coordinates of a square in which to place the
    # currently held piece. Returns two integers in range 0-3.
    def prompt_move(self, state):  raise NotImplementedError()

class HumanPlayer(AbsPlayer):
    _piece_msg = "{}, choose a piece for the opponent to place: "
    _square_msg = "{}, choose a square on which to place the piece: "
    
    def __init__(self, name):
        super().__init__(name)

    def prompt_piece(self, state):
        # Quit? Who wins then?
        # Expects an integer in range [1,16], existing in state.pieces
        p_str = input(self._piece_msg.format(self._name)).strip()
        while True:
            if not p_str.isdigit():
                p_str = input("Must be an integer, try again: ").strip()
                continue
            piece = int(p_str) - 1
            if not 0 <= piece <= 15:
                p_str = input("Must be in interval [1,16], try again: ").strip()
                continue
            if piece not in state.pieces:
                p_str = input("Piece is already played, try again: ").strip()
                continue
            return piece

    def prompt_square(self, state):
        # Expects an input formed as a string of two coordinates, e.g. "23"
        sq_str = input(self._square_msg.format(self._name)).strip()
        while True:
            if len(sq_str) != 2 or not sq_str.isdigit():
                sq_str = input("Provide two coordinates, try again: ").strip()
                continue
            row, col = [int(x) for x in sq_str]
            if not (1 <= row <= 4 and 1 <= col <= 4):
                sq_str = input("Must be in interval [1,4], try again: ").strip()
                continue
            row, col = row-1, col-1
            if state.square(row, col) is not None:
                sq_str = input("Square is occupied, try again: ").strip()
                continue
            return row, col

class AIPlayer(AbsPlayer):
    def __init__(self, name, difficulty):
        super().__init__("AI " + name)
        self._ai = AI(difficulty)
    
    def prompt_piece(self, state):
        p = self._ai.choose_piece(state)
        print("{} chose piece {}: {}"
              .format(self._name, p+1, GameIO.figures[p]))
        return p

    def prompt_square(self, state):
        s = self._ai.choose_square(state)
        print("{} chose square {}{}"
              .format(self._name, *[x+1 for x in s]))
        return s

class NetworkHumanPlayer(HumanPlayer):
    def __init__(self, name, opp_sock):
        super().__init__(name)
        self._opp_sock = opp_sock

    def prompt_piece(self, state):
        piece = super().prompt_piece(state)
        self._opp_sock.send(str(piece).encode("utf-8"))
        return piece

    def prompt_square(self, state):
        row, col = super().prompt_square(state)
        self._opp_sock.send((str(row) + str(col)).encode("utf-8"))
        return row, col

class NetworkAIPlayer(AIPlayer):
    def __init__(self, name, difficulty, opp_sock):
        super().__init__(name, difficulty)
        self._opp_sock = opp_sock

    def prompt_piece(self, state):
        piece = super().prompt_piece(state)
        self._opp_sock.send(str(piece).encode("utf-8"))
        return piece

    def prompt_square(self, state):
        row, col = super().prompt_square(state)
        self._opp_sock.send((str(row) + str(col)).encode("utf-8"))
        return row, col

class NetworkOpponent(AbsPlayer):
    def __init__(self, name, sock):
        super().__init__(name)
        self._sock = sock

    def prompt_piece(self, _):
        print("Waiting for opponent {} to choose a piece..."
              .format(self._name))
        # Should receive an integer in range [0,15] as a string
        piece_str = self._sock.recv(1024).decode("utf-8")
        piece = int(piece_str)
        print("{} chose piece {}: {}"
              .format(self._name, piece+1, GameIO.figures[piece]))
        return int(piece)

    def prompt_square(self, _):
        print("Waiting for opponent {} to choose a square..."
              .format(self._name))
        # Should receive an integer in range [00,33] as a string
        square_str = self._sock.recv(1024).decode("utf-8")
        row, col = [int(x) for x in square_str]
        print("{} chose square {}{}"
              .format(self._name, row+1, col+1))
        return row, col
