#!/usr/bin/env python3

from gameengine import AI
from gameplatform import GameIO

class AbsPlayer(object):
    # The default segment size for data packages sent over sockets.
    # Only useful for the Network* subclasses.
    # Defines a protocol used when passing information 
    # on game moves between computers on the network.
    _net_seg_size = 8

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
        # Expects an integer in range [1,16], existing in state.pieces
        p_str = input(self._piece_msg.format(self._name))
        while True:
            p_str = p_str.strip()
            if not p_str.isdigit():
                p_str = input("Must be an integer, try again: ")
                continue
            piece = int(p_str) - 1
            if not 0 <= piece <= 15:
                p_str = input("Must be in interval [1,16], try again: ")
                continue
            if piece not in state.pieces:
                p_str = input("Piece is already played, try again: ")
                continue
            return piece

    def prompt_square(self, state):
        # Expects an input formed as a string of two coordinates, e.g. "2C"
        sq_str = input(self._square_msg.format(self._name))
        while True:
            sq_str = sq_str.strip().upper()
            if len(sq_str) != 2:
                sq_str = input("Provide two coordinates, try again: ")
                continue
            if not sq_str[0].isdigit() or not 1 <= int(sq_str[0]) <= 4:
                sq_str = input("Invalid row coordinate, try again: ")
                continue
            if not sq_str[1] in "ABCD":
                sq_str = input("Invalid column coordinate, try again: ")
                continue
            row, col = int(sq_str[0])-1, GameIO.letter_to_col[sq_str[1]]
            if state.square(row, col) is not None:
                sq_str = input("Square is occupied, try again: ")
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
        r, c = self._ai.choose_square(state)
        print("{} chose square {}{}"
              .format(self._name, r+1, GameIO.col_to_letter[c]))
        return r, c

class NetworkHumanPlayer(HumanPlayer):
    def __init__(self, name, opp_sock):
        super().__init__(name)
        self._opp_sock = opp_sock

    def prompt_piece(self, state):
        piece = super().prompt_piece(state)
        self._opp_sock.send("{0: <{cs}}"
                            .format(piece,
                                    cs=self._net_seg_size)
                            .encode("utf-8"))
        return piece

    def prompt_square(self, state):
        row, col = super().prompt_square(state)
        self._opp_sock.send("{0: <{cs}}"
                            .format(str(row) + str(col),
                                    cs=self._net_seg_size)
                            .encode("utf-8"))
        return row, col

class NetworkAIPlayer(AIPlayer):
    def __init__(self, name, difficulty, opp_sock):
        super().__init__(name, difficulty)
        self._opp_sock = opp_sock

    def prompt_piece(self, state):
        piece = super().prompt_piece(state)
        self._opp_sock.send("{0: <{cs}}"
                            .format(piece,
                                    cs=self._net_seg_size)
                            .encode("utf-8"))
        return piece

    def prompt_square(self, state):
        row, col = super().prompt_square(state)
        self._opp_sock.send("{0: <{cs}}"
                            .format(str(row) + str(col),
                                    cs=self._net_seg_size)
                            .encode("utf-8"))
        return row, col

class NetworkOpponent(AbsPlayer):
    def __init__(self, name, sock):
        super().__init__(name)
        self._sock = sock

    def prompt_piece(self, _):
        print("Waiting for opponent {} to choose a piece..."
              .format(self._name))
        # Should receive an integer in range [0,15] as a string
        p_str = self._sock.recv(self._net_seg_size).decode("utf-8").strip()
        piece = int(p_str)
        print("{} chose piece {}: {}"
              .format(self._name, piece+1, GameIO.figures[piece]))
        return int(piece)

    def prompt_square(self, _):
        print("Waiting for opponent {} to choose a square..."
              .format(self._name))
        # Should receive an integer in range [00,33] as a string
        s_str = self._sock.recv(self._net_seg_size).decode("utf-8").strip()
        row, col = [int(x) for x in s_str]
        print("{} chose square {}{}"
              .format(self._name, row+1, GameIO.col_to_letter[col]))
        return row, col
