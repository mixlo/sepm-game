#!/usr/bin/env python3

from functools import reduce

class AbsState(object):
    @property
    def board(self):                 raise NotImplementedError()
    @board.setter
    def board(self, b):              raise NotImplementedError()
    @property
    def pieces(self):                raise NotImplementedError()
    @pieces.setter
    def pieces(self, ps):            raise NotImplementedError()
    def is_holding(self):            raise NotImplementedError()
    def pick_piece(self, piece):     raise NotImplementedError()
    def place_piece(self, row, col): raise NotImplementedError()
    def square(self, row, col):      raise NotImplementedError()
    def free_squares(self):          raise NotImplementedError()
    def has_winner(self):            raise NotImplementedError()
    def is_draw(self):               raise NotImplementedError()
    def copy(self):                  raise NotImplementedError()

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

    def is_holding(self):
        return self._held_piece is not None
    
    def pick_piece(self, piece):
        if self.is_holding():
            raise ValueError("Already holding a piece")
        if piece not in self._pieces:
            raise ValueError("Piece has already been played")
        self._pieces.remove(piece)
        self._held_piece = piece
    
    # place_piece(int, int, int)
    def place_piece(self, row, col):
        if not self.is_holding():
            raise ValueError("No piece to place")
        if self.square(row, col) is not None:
            raise ValueError("Square is occupied")
        self._board[row][col] = self._held_piece
        self._held_piece = None
    
    # get_square(int, int)
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
            if self._win_row(self._board[i]) or self._win_row(board_t[i]):
               return True
        d1, d2 = self._get_diags(self._board)
        return (self._win_row(d1) or self._win_row(d2))
    
    def is_draw(self):
        return not self._pieces
    
    def copy(self):
        return State([row[:] for row in self._board], 
                     self._pieces.copy(),
                     self._held_piece)
    
    def _transpose(self, mat):
        return list(map(list, zip(*mat)))
    
    def _get_diags(self, sqr_mat):
        return ([row[i] for i, row in enumerate(sqr_mat)], 
                [row[-i-1] for i, row in enumerate(sqr_mat)])
    
    def _win_row(self, row):
        return (not None in row and 
                bool(reduce(lambda x, y: x & y, row, 0b1111) | 
                     reduce(lambda x, y: x & (0b1111 - y), row, 0b1111)))
