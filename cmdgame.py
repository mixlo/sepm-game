#!/usr/bin/env python3

import state, gameengine
import sys
import unittest

class Game(object):
    piece_msg = "Player {}, choose a piece for the opponent to place: "
    square_msg = "Player {}, choose a square on which to place the piece: "
    
    def __init__(self, ai_diff=None):
        # Creates a new state with empty board and full pool of pieces
        self._state = state.State()
        self._current_player = 0
        self._ai = None if ai_diff is None else gameengine.AI(ai_diff)
    
    def start(self):
        # Print initial state of board and pieces
        self._print_board()
        self._print_pieces()
        while not self._game_over():
            # Prompts user for piece
            piece = self._prompt_piece()
            # Pick piece, modify state
            self._state.pick_piece(piece)
            # XOR to switch between players 0 and 1
            self._current_player ^= 1
            # Prompts user for square
            row, col = self._prompt_square()
            # Place piece, modify state
            self._state.place_piece(row, col)
            # Print board and pieces
            self._print_board()
            self._print_pieces()

    def _prompt_piece(self):
        if self._current_player == 1 and self._ai is not None:
            piece = self._ai.random_piece(self._state)
            print("AI picked piece:", self._to_4bit_str(piece))
            return piece
        else:
            return self._prompt_piece_human()
            
    def _prompt_piece_human(self):
        # Expects an input formed as a string of four bits, e.g. "0101"
        piece_str = input(self.piece_msg.format(self._current_player+1))
        while True:
            if len(piece_str) != 4:
                piece_str = input("Must be four bits, try again: ")
                continue
            if not all(c in "01" for c in piece_str):
                piece_str = input("Must be four bits, try again: ")
                continue
            piece = int(piece_str, base=2)
            if piece not in self._state.pieces:
                piece_str = input("Piece is already played, try again: ")
                continue
            return piece

    def _prompt_square(self):
        if self._current_player == 1 and self._ai is not None:
            square = self._ai.random_move(self._state)
            print("AI chose square:", str(square[0]+1) + str(square[1]+1))
            return square
        else:
            return self._prompt_square_human()
        
    def _prompt_square_human(self):
        # Expects an input formed as a string of two coordinates, e.g. "23"
        square_str = input(self.square_msg.format(self._current_player+1))
        while True:
            if len(square_str) != 2 or not square_str.isdigit():
                square_str = input("Provide two coordinates, try again: ")
                continue
            row, col = [int(x) for x in square_str]
            if not (1 <= row <= 4 and 1 <= col <= 4):
                square_str = input("Must be in interval [1,4], try again: ")
                continue
            row, col = row-1, col-1
            if self._state.square(row, col) is not None:
                square_str = input("Square is occupied, try again: ")
                continue
            return row, col
    
    def _game_over(self):
        if self._state.has_winner():
            print("Player {} wins!".format(self._current_player+1))
            return True
        if self._state.is_draw():
            print("No pieces left, nobody wins!")
            return True
        return False
    
    def _print_board(self):
        print("BOARD:")
        for row in self._state.board:
            for col in row:
                print(self._to_4bit_str(col) if col is not None else "----", 
                      end=" ")
            print()
    
    def _print_pieces(self):
        print("PIECES:")
        print("{", end=" ")
        for piece in self._state.pieces:
            print(self._to_4bit_str(piece), end=" ")
        print("}")
    
    def _to_4bit_str(self, num):
        return format(num, '04b')



def main():
    ai_diff = int(sys.argv[1]) if len(sys.argv) > 1 else None
    g = Game(ai_diff)
    g.start()


class GameTestCase(unittest.TestCase):

    def test_init_game(self):
        g = Game()
        self.assertEqual(len(g._state._pieces), 16)
        self.assertEqual(g._state.board, [[None, None, None, None],
                                          [None, None, None, None],
                                          [None, None, None, None],
                                          [None, None, None, None]])

        
    def test_game_over(self):
        g = Game()
        
        g._state._board = [[12, 8, 14, 15],
                    [None, None, None, None],
                    [None, None, None, None],
                    [None, None, None, None]]
        self.assertTrue(g._state.has_winner())
        
        g._state._board = [[0b0100, 0b1000, 0b1110, 0b1111],
                    [None, 0b1100, None, None],
                    [None, None, None, None],
                    [None, None, None, None]]
        self.assertFalse(g._state.has_winner())
        g._state._board = [[12, None, None, None],
                    [8, None, None, None],
                    [14, None, None, None],
                    [15, None, None, None]]
        self.assertTrue(g._state.has_winner())

        

    def test_draw(self):
        g = Game()
        self.assertFalse(g._state.is_draw())
        g._state.pieces = set([])
        self.assertTrue(g._state.is_draw())
        g._state.pieces = set([1])
        self.assertFalse(g._state.is_draw())
        #g._state.board = [[0b0100, 0b1000, 0b1110, 0b1111],
         #           [0b0000, 0b1100, 0b0010, 0b0111],
          #          [0b0001, 0b0011, 0b0101, 0b1001],
           #         [0b1011, 0b1101, 0b1010, 0b0110]] #win in diags
        #self.assertFalse(g._state.is_draw()) # might change depending on draw definition
        #g._state.board = [[0b1111, 0b1000, 0b1110, 0b0100],
               #     [0b0000, 0b0010, 0b1100, 0b0111],
                #    [0b0001, 0b0011, 0b0101, 0b1001],
                 #   [0b1011, 0b1101, 0b1010, 0b0110]]
        #print(g._state.board)

        #print(None)
        #self.assertTrue(g._state.is_draw())
        #g._state.board = [[0b1111, 0b1000, 0b1110, 0b0100],
#                    [0b0000, 0b0010, 0b1100, 0b0111],
 #                   [0b0001, 0b0011, 0b0101, 0b1001],
  #                  [None, 0b1101, 0b1010, 0b0110]] 
        #self.assertFalse(g._state.is_draw()) #might change depending on draw definition, in this case there is only one move availible and it will result in a draw
        
        
    def test_place(self):
        g = Game()
        s = g._state

        
        s._held_piece = 1
        s.board = [[None, None, None, None],
                    [None, None, None, None],
                    [None, None, None, None],
                    [None, None, None, None]]
        s.place_piece(0, 0)
        self.assertEqual(s.board, [[1, None, None, None],
                    [None, None, None, None],
                    [None, None, None, None],
                    [None, None, None, None]])
        
        s._held_piece = 11
        s.board = [[0b1111, 0b1000, 0b1110, 0b0100],
                    [0b0000, 0b0010, 0b1100, 0b0111],
                    [0b0001, 0b0011, 0b0101, 0b1001],
                    [None, 0b1101, 0b1010, 0b0110]]
        s.place_piece(3, 0)
        self.assertEqual(s.board, [[0b1111, 0b1000, 0b1110, 0b0100],
                    [0b0000, 0b0010, 0b1100, 0b0111],
                    [0b0001, 0b0011, 0b0101, 0b1001],
                    [0b1011, 0b1101, 0b1010, 0b0110]])
    def test_hold(self):
        g = Game()
        s = g._state
        self.assertFalse(s.is_holding())
        s._held_piece = 11
        self.assertTrue(s.is_holding())
        
        
    def test_pick(self):
        g = Game()
        s = g._state
        s.pick_piece(11)
        self.assertEqual(s._held_piece, 11)
        
    #def test_calc_best(self):
    #def test_calc_worst(self):
    #def test_calc_avg(self):
    def test_diagonal(self):
        g = Game()
        g._state.board = [[0b1111, 0b1000, 0b1110, 0b0100],
                    [0b0000, 0b0010, 0b1100, 0b0111],
                    [0b0001, 0b0011, 0b0101, 0b1001],
                    [0b1011, 0b1101, 0b1010, 0b0110]]
        
        diag_1 = [0b1111, 0b0010, 0b0101, 0b0110]
        diag_2 = [0b0100, 0b1100, 0b0011, 0b1011]
        
        stored_d1, stored_d2 = g._state._get_diags(g._state.board)
        #print(stored_d1)
        #print(diag_1)
        #print(stored_d2)
        #print(diag_2)
        
        self.assertEqual(diag_1, stored_d1)
        self.assertEqual(diag_2, stored_d2)
        
        
        
        
    def test_transpose(self):
        g = Game()
        g._state.board = [[None, None, None, None],
                           [None, None, None, None],
                           [None, None, None, None],
                           [None, None, None, None]]
        tm = g._state._transpose(g._state._board)
        self.assertEqual([[None, None, None, None],
                          [None, None, None, None],
                          [None, None, None, None],
                          [None, None, None, None]], tm)

        
        g._state.board = [[0b1111, 0b1000, 0b1110, 0b0100],
                    [0b0000, 0b0010, 0b1100, 0b0111],
                    [0b0001, 0b0011, 0b0101, 0b1001],
                    [0b1011, 0b1101, 0b1010, 0b0110]]
        tm = g._state._transpose(g._state.board)
        self.assertEqual([[0b1111, 0b0000, 0b0001, 0b1011],
                          [0b1000, 0b0010, 0b0011, 0b1101],
                          [0b1110, 0b1100, 0b0101, 0b1010],
                          [0b0100, 0b0111, 0b1001, 0b0110]], tm)


# If file is called from command line, run main() function
if __name__ == "__main__":
    testmode = False
    if testmode:
        unittest.main() 
    else:
        main() 
