import random

class Difficulty:
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class AI(object):
    # Constructor
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.medium_smartness = 0.8
    
    # Private
    def _calc_best_move(self, board, piece):
        pass
    def _calc_worst_move(self, board, piece):
        pass
    def _calc_best_piece(self, board, pieces):
        pass
    def _calc_worst_piece(self, board, pieces):
        pass
    
    # Public
    def select_move(self, board, piece):
        if self.difficulty == Difficulty.HIGH:
            return self._calc_best_move(board, piece)
        elif self.difficulty == Difficulty.MEDIUM:
            if random.random() < self.medium_smartness:
                return self._calc_best_move(board, piece)
            else:
                return self._calc_worst_move(board, piece)
        elif self.difficulty == Difficulty.LOW:
            return self._calc_worst_move(board, piece)
    
    def select_piece(self, board, pieces):
        if self.difficulty == Difficulty.HIGH:
            return self._calc_best_piece(board, pieces)
        elif self.difficulty == Difficulty.MEDIUM:
            if random.random() < self.medium_smartness:
                return self._calc_best_piece(board, pieces)
            else:
                return self._calc_worst_piece(board, pieces)
        elif self.difficulty == Difficulty.LOW:
            return self._calc_worst_piece(board, pieces)