import sys
sys.path.append('../../')
import state
import unittest
import importlib
import gameplatform


class GameTestCase(unittest.TestCase):
    def setUp(self):
        self.g = gameplatform.Game()
        

    def test_init_game(self):
        self.assertEqual(len(self.g._state._pieces), 16)
        self.assertEqual(self.g._state.board, [[None, None, None, None],
                                          [None, None, None, None],
                                          [None, None, None, None],
                                          [None, None, None, None]])

        
    def test_game_over(self):
    
        self.g._state._board = [[12, 8, 14, 15],
                    [None, None, None, None],
                    [None, None, None, None],
                    [None, None, None, None]]
        self.assertTrue(self.g._state.has_winner())
        
        self.g._state._board = [[0b0100, 0b1000, 0b1110, 0b1111],
                    [None, 0b1100, None, None],
                    [None, None, None, None],
                    [None, None, None, None]]
        self.assertFalse(self.g._state.has_winner())
        self.g._state._board = [[12, None, None, None],
                    [8, None, None, None],
                    [14, None, None, None],
                    [15, None, None, None]]
        self.assertTrue(self.g._state.has_winner())

        

    def test_draw(self):
        self.assertFalse(self.g._state.is_draw())
        self.g._state.pieces = set([])
        self.assertTrue(self.g._state.is_draw())
        self.g._state.pieces = set([1])
        self.assertFalse(self.g._state.is_draw())
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
        s = self.g._state

        
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
        s = self.g._state
        self.assertFalse(s.is_holding())
        s._held_piece = 11
        self.assertTrue(s.is_holding())
        
        
    def test_pick(self):
        s = self.g._state
        s.pick_piece(11)
        self.assertEqual(s._held_piece, 11)
        
    #def test_calc_best(self):
    #def test_calc_worst(self):
    #def test_calc_avg(self):
    def test_diagonal(self):
        self.g._state.board = [[0b1111, 0b1000, 0b1110, 0b0100],
                    [0b0000, 0b0010, 0b1100, 0b0111],
                    [0b0001, 0b0011, 0b0101, 0b1001],
                    [0b1011, 0b1101, 0b1010, 0b0110]]
        
        diag_1 = [0b1111, 0b0010, 0b0101, 0b0110]
        diag_2 = [0b0100, 0b1100, 0b0011, 0b1011]
        
        stored_d1, stored_d2 = self.g._state._get_diags(self.g._state.board)
        #print(stored_d1)
        #print(diag_1)
        #print(stored_d2)
        #print(diag_2)
        
        self.assertEqual(diag_1, stored_d1)
        self.assertEqual(diag_2, stored_d2)
        
        
        
        
    def test_transpose(self):
        self.g._state.board = [[None, None, None, None],
                           [None, None, None, None],
                           [None, None, None, None],
                           [None, None, None, None]]
        tm = self.g._state._transpose(self.g._state._board)
        self.assertEqual([[None, None, None, None],
                          [None, None, None, None],
                          [None, None, None, None],
                          [None, None, None, None]], tm)

        
        self.g._state.board = [[0b1111, 0b1000, 0b1110, 0b0100],
                    [0b0000, 0b0010, 0b1100, 0b0111],
                    [0b0001, 0b0011, 0b0101, 0b1001],
                    [0b1011, 0b1101, 0b1010, 0b0110]]
        tm = self.g._state._transpose(self.g._state.board)
        self.assertEqual([[0b1111, 0b0000, 0b0001, 0b1011],
                          [0b1000, 0b0010, 0b0011, 0b1101],
                          [0b1110, 0b1100, 0b0101, 0b1010],
                          [0b0100, 0b0111, 0b1001, 0b0110]], tm)


if __name__ == "__main__":    
    unittest.main() 
