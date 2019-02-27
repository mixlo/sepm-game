#!/usr/bin/env python3

from state import State

class Game(object):
    def __init__(self, player1=None, player2=None):
        # Creates a new state with empty board and full pool of pieces
        self._state = State()
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
        GameIO.print_welcome(self._players[0].name, self._players[1].name)
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
            GameIO.print_state(self._state)
        print()

    def reset(self):
        self._state = State()
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
    figures = {
         0: "<+X#>",
         1: "<+X*>",
         2: "<+O#>",
         3: "<+O*>",
         4: "<-X#>",
         5: "<-X*>",
         6: "<-O#>",
         7: "<-O*>",
         8: "(+X#)",
         9: "(+X*)",
        10: "(+O#)",
        11: "(+O*)",
        12: "(-X#)",
        13: "(-X*)",
        14: "(-O#)",
        15: "(-O*)",
        None: "     "
    }

    letter_to_col = dict(zip("ABCD", range(4)))
    col_to_letter = dict(zip(range(4), "ABCD"))

    _game_view_str = """
       A       B       C       D
   +-------+-------+-------+-------+   PIECES LEFT:
   |       |       |       |       |    1. {016}
 1 | {000} | {001} | {002} | {003} |    2. {017}
   |       |       |       |       |    3. {018}
   +-------+-------+-------+-------+    4. {019}
   |       |       |       |       |    5. {020}
 2 | {004} | {005} | {006} | {007} |    6. {021}
   |       |       |       |       |    7. {022}
   +-------+-------+-------+-------+    8. {023}
   |       |       |       |       |    9. {024}
 3 | {008} | {009} | {010} | {011} |   10. {025}
   |       |       |       |       |   11. {026}
   +-------+-------+-------+-------+   12. {027}
   |       |       |       |       |   13. {028}
 4 | {012} | {013} | {014} | {015} |   14. {029}
   |       |       |       |       |   15. {030}
   +-------+-------+-------+-------+   16. {031}
"""

    _instructions = """
 - Enter number between 1-16 to choose piece from 'PIECES LEFT': '10' = {}.
 - Enter row and column to choose square: '2C'/'2c' = second row, third column.
 - Enter 'q' to forfeit the game and quit to the main menu.
 - Enter 'q!' to forfeit the game and close the application."""

    @classmethod
    def print_welcome(cls, p1_name, p2_name):
        print("Welcome to the game between {} and {}!".format(p1_name, p2_name))
        print()
        print("Instructions:")
        print(cls._instructions.format(GameIO.figures[9]))
        print()
        print("On your marks, get set, go!")

    @classmethod
    def print_state(cls, state):
        board_figs = [cls.figures[col] for row in state.board for col in row]
        pieces_figs = [""]*16
        for p in state.pieces:
            pieces_figs[p] = cls.figures[p]
        print(cls._game_view_str.format(*board_figs, *pieces_figs))
    
    @classmethod
    def print_winner(cls, name):
        print("{} wins!".format(name))

    @classmethod
    def print_draw(cls):
        print("Draw!")
