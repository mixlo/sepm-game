#!/usr/bin/env python3

import random
from functools import reduce
from math import inf

class Difficulty:
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class AI(object):
    # Constructor
    def __init__(self, difficulty):
        self._difficulty_smartness = [0, 0.5, 1.1][difficulty-1]
    
    def choose_piece(self, state):
        if random.random() < self._difficulty_smartness:
            return self._calc_best_piece(state)
        else:
            return self._random_piece(state)
        
    def choose_square(self, state):
        if random.random() < self._difficulty_smartness:
            return self._calc_best_square(state)
        else:
            return self._random_square(state)
        
    def _random_piece(self, state):
        return random.choice(list(state.pieces))        

    def _random_square(self, state):
        return random.choice(state.free_squares())

    def _determine_depth(self, state):
        rem_pieces = len(state.pieces)
        if   rem_pieces >= 12: return 1
        elif rem_pieces >=  9: return 2
        elif rem_pieces >=  6: return 3
        return 4
    
    def _calc_best_piece(self, state):
        _, _, (_, p) = self._maximize(state, self._determine_depth(state))
        return p
    
    def _calc_best_square(self, state):
        _, _, (s, _) = self._maximize(state, self._determine_depth(state))
        return s

    def _maximize(self, node, depth):
        if node.has_winner():
            return -inf, depth, None
        if node.is_draw():
            return 0, depth, None
        if depth == 0:
            if self._can_win(node):
                return inf, depth, None
            return self._evaluate(node), 0, None
        vals = []
        for child, move in self._children(node):
            cval, cdepth, _ = self._minimize(child, depth-1)
            vals.append((cval, cdepth, move))
        return self._max(vals)

    def _minimize(self, node, depth):
        if node.has_winner():
            return inf, depth, None
        if node.is_draw():
            return 0, depth, None
        if self._can_win(node):
            return -inf, depth, (None, node.held_piece)
        if depth == 0:
            if self._can_win(node):
                return -inf, depth, None
            return self._evaluate(node), 0, None
        vals = []
        for child, move in self._children(node):
            cval, cdepth, _ = self._maximize(child, depth-1)
            vals.append((cval, cdepth, move))
        return self._min(vals)

    def _max(self, vals):
        # Note: in our case, larger depth values == shallower
        val, depth, move = -inf, None, None
        for v, d, m in vals:
            if (v > val or
                    (v == val and v > 0 and (depth is None or d > depth)) or
                    (v == val and v <= 0 and (depth is None or d < depth))):
                val, depth, move = v, d, m
        return val, depth, move

    def _min(self, vals):
        # Note: in our case, larger depth values == shallower
        val, depth, move = inf, None, None
        for v, d, m in vals:
            if (v < val or
                    (v == val and v > 0 and (depth is None or d < depth)) or
                    (v == val and v <= 0 and (depth is None or d > depth))):
                val, depth, move = v, d, m
        return val, depth, move

    def _children(self, state):
        children = []
        if not state.is_holding():
            for piece in random.sample(state.pieces, len(state.pieces)):
                child = state.copy()
                child.pick_piece(piece)
                children.append((child, (None, piece)))
        elif not state.pieces:
            free_squares = state.free_squares()
            for row, col in random.sample(free_squares, len(free_squares)):
                child = state.copy()
                child.place_piece(row, col)
                children.append((child, ((row, col), None)))
        else:
            free_squares = state.free_squares()
            for row, col in random.sample(free_squares, len(free_squares)):
                temp = state.copy()
                temp.place_piece(row, col)
                for piece in random.sample(state.pieces, len(state.pieces)):
                    child = temp.copy()
                    child.pick_piece(piece)
                    children.append((child, ((row, col), piece)))
        return children

    def _can_win(self, state):
        if not state.is_holding():
            return False
        for row, col in state.free_squares():
            child = state.copy()
            child.place_piece(row, col)
            if child.has_winner():
                return True
        return False
    
    # Evaluates from the point of view of the maximizing player;
    # higher value means higher win potential
    # Value for each vector is determined by how many attributes all pieces
    # have in common and the number of pieces in the vector. The number of
    # pieces in the vector weighs heavier than how many attributes the have in
    # common, and is therefore squared in the calculation.
    # (e.g. 2 pieces, 3 attributes in common -> val == 2^2 * 3 == 12)
    # (e.g. 3 pieces, 2 attributes in common -> val == 3^2 * 2 == 18)
    def _evaluate(self, state):
        vecs = [[p for p in v if p is not None] for v in state.get_vectors()]
        return sum(map(lambda v: self._calc_common(v) * len(v)**2, vecs))

    def _calc_common(self, vec):
        common = (reduce(lambda x, y: x & y, vec, 0b1111) | 
                  reduce(lambda x, y: x & (0b1111 - y), vec, 0b1111))
        return bin(common).count('1')
