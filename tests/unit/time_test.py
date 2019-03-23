import sys
sys.path.append('/home/david/Documents/python/sepm/sepm-game/')
import state
import unittest
import cmdgame
import importlib
import player
import gameengine
import gameplatform


class GameTestCase(unittest.TestCase):

    def setUp(self):
        self.rounds = 1

    def test_easy_bot_time(self):

        p1_name = "Alfred"
        p2_name = "Derfla"
      
        p1 = player.AIPlayer(p1_name, gameengine.Difficulty.LOW)
        p2 = player.AIPlayer(p2_name, gameengine.Difficulty.LOW)
        for i in range(self.rounds):
            g = gameplatform.Game(p1, p2)
            self.assertEqual("Game Over", g.start_with_timer(10))
        
    def test_medium_bot_time(self):
        
        p1_name = "Pumba"
        p2_name = "Timon"
        
        p1 = player.AIPlayer(p1_name, gameengine.Difficulty.MEDIUM)
        p2 = player.AIPlayer(p2_name, gameengine.Difficulty.MEDIUM)
        for i in range(self.rounds):
            g = gameplatform.Game(p1, p2)
            self.assertEqual("Game Over", g.start_with_timer(10))
        
    def test_hard_bot_time(self):

        p1_name = "HAL-9000"
        p2_name = "HAL-9001"

        p1 = player.AIPlayer(p1_name, gameengine.Difficulty.HIGH)
        p2 = player.AIPlayer(p2_name, gameengine.Difficulty.HIGH)
        for i in range(self.rounds):
            g = gameplatform.Game(p1, p2)
            self.assertEqual("Game Over", g.start_with_timer(10))
        

if __name__ == "__main__":
#    if len(sys.argv) == 2 and str.isdigit(sys.argv[1]):
#        r = int(sys.argv[1])
    
    unittest.main() 
