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
        p_str = input(self._piece_msg.format(self._name)).strip()
        while True:
            if len(p_str) != 4:
                p_str = input("Must be four bits, try again: ").strip()
                continue
            if not all(c in "01" for c in p_str):
                p_str = input("Must be four bits, try again: ").strip()
                continue
            piece = int(p_str, base=2)
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

class AIPlayer(Player):
    def __init__(self, name, difficulty):
        self._name = "AI " + name
        self._ai = gameengine.AI(difficulty)

    @property
    def name(self):
        return self._name
    
    def prompt_piece(self, state):
        p = self._ai.choose_piece(state)
        print("{0} chose piece: {1:04b}".format(self._name, p))
        return p

    def prompt_square(self, state):
        s = self._ai.choose_square(state)
        print("{} chose square: {}{}".format(self._name, *[x+1 for x in s]))
        return s

# Works as a normal HumanPlayer instance, but also has a reference to a socket 
# connected to the network opponent. The prompt methods are responsible for 
# also sending the results to the opponent so that they can update the state
# and UI on their side.
class NetworkHumanPlayer(HumanPlayer):
    # Should set the name as usual, but also receive and keep track
    # of a reference to the socket connected to the opponent
    def __init__(self, name, opp_sock):
        pass

    # Should prompt for and return the piece as usual,
    # but also send the result to the network opponent
    def prompt_piece(self, state):
        pass

    # Should prompt for and return the square as usual,
    # but also send the result to the network opponent
    def prompt_square(self, state):
        pass

# Works as a normal AIPlayer instance, but also has a reference to a socket 
# connected to the network opponent. The prompt methods are responsible for 
# also sending the results to the opponent so that they can update the state
# and UI on their side.
class NetworkAIPlayer(AIPlayer):
    # Should set the name and difficulty as usual, but also receive and
    # keep track of a reference to the socket connected to the opponent
    def __init__(self, name, difficulty, opp_sock):
        pass

    # Should prompt for and return the piece as usual,
    # but also send the result to the network opponent
    def prompt_piece(self, state):
        pass

    # Should prompt for and return the square as usual,
    # but also send the result to the network opponent
    def prompt_square(self, state):
        pass

# Represents the opponent in a network game, either a human player or an AI.
# Responsible for waiting for the opponent to make their moves and then 
# receiving and printing the information via the socket.
class NetworkOpponent(Player):
    # Should set the name and keep track of a reference 
    # to the socket connected to the opponent.
    def __init__(self, name, sock):
        self._name = name
        self._sock = sock

    @property
    def name(self):
        return self._name

    # Should receive a piece from the opponent via the socket and print 
    # information to the command line about waiting for the opponent and 
    # what piece they chose.
    def prompt_piece(self, _):
        pass

    # Should receive a square from the opponent via the socket and print 
    # information to the command line about waiting for the opponent and 
    # what square they chose.
    def prompt_square(self, _):
        pass
