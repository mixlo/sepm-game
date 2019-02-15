#!/usr/bin/env python3

from functools import reduce

class AbsState(object):
    # Returns the current board state as a matrix (array of arrays), where
    # elements are integers in range 0-15, or None for empty squares.
    @property
    def board(self):                 raise NotImplementedError()
    # Updates the board state. Accepts a board of the same format as above.
    @board.setter
    def board(self, b):              raise NotImplementedError()
    # Returns the remaining pieces as a set of integers in range 0-15.
    @property
    def pieces(self):                raise NotImplementedError()
    # Updates the remaining pieces. Accepts a set of the same format as above.
    @pieces.setter
    def pieces(self, ps):            raise NotImplementedError()
    # Returns the current held piece as an int in range 0-15,
    # or None if no piece is currently held.
    @property
    def held_piece(self):            raise NotImplementedError()
    # Returns True if a piece is currently held, False otherwise.
    def is_holding(self):            raise NotImplementedError()
    # Updates the state such that the specified piece is held and removed from
    # the remaining pieces set. Accepts an integer in range 0-15.
    def pick_piece(self, piece):     raise NotImplementedError()
    # Updates the state such that the held piece is placed on the square
    # specified by the provided coordinates. Accepts integers in range 0-15.
    def place_piece(self, row, col): raise NotImplementedError()
    # Returns the contents of the square at coordinates (row, col).
    # Accepts two integers in range 0-3.
    # Result is an integer in range 0-15, or None if square is empty.
    def square(self, row, col):      raise NotImplementedError()
    # Returns an array of the coordinates of all empty squares on the board.
    def free_squares(self):          raise NotImplementedError()
    # Returns True if the board is in a "won" state, False otherwise.
    def has_winner(self):            raise NotImplementedError()
    # Returns True if the board is in a "draw" state, False otherwise.
    def is_draw(self):               raise NotImplementedError()
    # Returns a copy of the state instance.
    def copy(self):                  raise NotImplementedError()
    # Returns an array of all rows, columns and diagonals of the board.
    def get_vectors(self):           raise NotImplementedError()

# Pieces are represented with integers 0-15.
# Board is represented by a matrix of integers 0-15, or None if empty square.
class State(AbsState):
    def __init__(self, 
                 board=[[None for _ in range(4)] for _ in range(4)], 
                 pieces=set(range(16)), 
                 held_piece=None):
        self.board = board
        self.pieces = pieces
        self._held_piece = held_piece
    
    # When using the public property to access the board, always return a 
    # copy, not the actual reference to the board object.
    @property
    def board(self):
        return [row[:] for row in self._board]
    # When using the public property to set the board, always take a copy of 
    # the provided board first, to avoid leaking a reference to our state.
    @board.setter
    def board(self, b):
        self._board = [row[:] for row in b]
    
    # Return a copy of the pieces set, for the same reason as for the board.
    @property
    def pieces(self):
        return self._pieces.copy()
    # Take a copy of the provided set, for the same reason as for the board.
    @pieces.setter
    def pieces(self, ps):
        self._pieces = ps.copy()

    @property
    def held_piece(self):
        return self._held_piece
    
    def is_holding(self):
        return self._held_piece is not None
    
    def pick_piece(self, piece):
        if self.is_holding():
            raise ValueError("Already holding a piece")
        if piece not in self._pieces:
            raise ValueError("Piece has already been played")
        self._pieces.remove(piece)
        self._held_piece = piece
    
    def place_piece(self, row, col):
        if not self.is_holding():
            raise ValueError("No piece to place")
        if self.square(row, col) is not None:
            raise ValueError("Square is occupied")
        self._board[row][col] = self._held_piece
        self._held_piece = None
    
    def square(self, row, col):
        return self._board[row][col]
    
    def free_squares(self):
        squares = []
        for row in range(4):
            for col in range(4):
                if self._board[row][col] is None:
                    squares.append((row,col))
        return squares
    
    def has_winner(self):
        board_t = self._transpose(self._board)
        for i in range(4):
            if self._win_vec(self._board[i]) or self._win_vec(board_t[i]):
               return True
        d1, d2 = self._get_diags(self._board)
        return (self._win_vec(d1) or self._win_vec(d2))
    
    def is_draw(self):
        return (not self._pieces and
                self._held_piece is None and
                not self.has_winner())
    
    def copy(self):
        return State([row[:] for row in self._board], 
                     self._pieces.copy(),
                     self._held_piece)

    def get_vectors(self):
        return ([row[:] for row in self._board] +
                self._transpose(self._board) +
                list(self._get_diags(self._board)))
    
    def _transpose(self, mat):
        return list(map(list, zip(*mat)))
    
    def _get_diags(self, sqr_mat):
        return ([row[i] for i, row in enumerate(sqr_mat)], 
                [row[-i-1] for i, row in enumerate(sqr_mat)])
    
    def _win_vec(self, vec):
        return (not None in vec and 
                bool(reduce(lambda x, y: x & y, vec, 0b1111) | 
                     reduce(lambda x, y: x & (0b1111 - y), vec, 0b1111)))
