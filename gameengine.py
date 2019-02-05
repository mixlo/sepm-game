#!/usr/bin/env python3

import random

# Arbitrary value limits, evaluation shouldn't exceed/go beneath these.
class Limits:
    MAXVAL = 2**32
    MINVAL = -MAXVAL

class Difficulty:
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class AI(object):
    # Constructor
    def __init__(self, difficulty):
        self._difficulty_smartness = [0.1, 0.5, 0.9][difficulty]
    
    def select_move(self, board, piece):
        if random.random() < self._difficulty_smartness:
            return self._calc_best_move(board, piece)
        else:
            return self._calc_worst_move(board, piece)
    
    def select_piece(self, board, pieces):
        if random.random() < self._difficulty_smartness:
            return self._calc_best_piece(board, pieces)
        else:
            return self._calc_worst_piece(board, pieces)
    
    def _calc_best_move(self, board, piece):
        pass
    def _calc_worst_move(self, board, piece):
        pass
    def _calc_best_piece(self, board, pieces):
        pass
    def _calc_worst_piece(self, board, pieces):
        pass
    
    # The minimax algorithm implemented using alpha-beta pruning
    # NOTE: To get worst move, is it as simple as to init should_max to False?
    def _minimax(self, state):
        return self._alphabeta(state, 4, Limits.MINVAL, Limits.MAXVAL, True)
    
    def _alphabeta(self, node, depth, alpha, beta, should_max):
        if node.has_winner():
            return Limits.MINVAL if should_max else Limits.MAXVAL
        if node.is_draw():
            return Limits.MINVAL+1 if should_max else Limits.MAXVAL-1
        if depth == 0:
            return self._evaluate(node)
        children = self._get_children(node)
        if should_max:
            val = Limits.MINVAL
            for child in children:
                child_val = self._alphabeta(child, depth−1, alpha, beta, False)
                val = max(val, child_val)
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
            return val
        else:
            val = Limits.MAXVAL
            for child in children:
                child_val = self._alphabeta(child, depth−1, alpha, beta, True)
                val = min(val, child_val)
                beta = min(beta, val)
                if alpha >= beta:
                    break
            return val
    
    def _get_children(self, state):
        children = []
        free_squares = 
        if state.is_holding():
            for row, col in state.free_squares:
                child = state.copy()
                child.place_piece(row, col)
                children.append(child)
        else:
            for piece in state.pieces:
                child = state.copy()
                child.pick_piece(piece)
                children.append(child)
        return children

    # The heuristic evaluation function, taking 3 different factors into account, 
    # which values have 3 different levels of significance
    def _evaluate(self, state):
        return (3 * self._very_important_factor(state) + 
                2 * self._somewhat_important_factor(state) + 
                1 * self._least_important_factor(state))

    def _very_important_factor(self, state):
        pass
    
    def _somewhat_important_factor(self, state):
        pass
    
    def _least_important_factor(self, state):
        pass
