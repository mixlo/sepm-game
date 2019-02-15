#!/usr/bin/env python3

import gameengine, cmdgame, player

def main():
    p1 = player.HumanPlayer("Jeff")
    p2 = player.HumanPlayer("Dave")
    p3 = player.AIPlayer("Alfred", gameengine.Difficulty.LOW)
    p4 = player.AIPlayer("Pumba", gameengine.Difficulty.MEDIUM)
    p5 = player.AIPlayer("HAL 9000", gameengine.Difficulty.HIGH)
    
    g = cmdgame.Game(p4, p5)
    g.start()

# If file is called from command line, run main() function
if __name__ == "__main__":
    main()
