#!/usr/bin/env python3

import gameengine, cmdgame, player
import threading
running = True
def mytimer():
    running = False
def run_game(rounds, p1, p2, p1_name, p2_name):
    p1_win_count = 0
    p2_win_count = 0
    draw_counter = 0
    
    for i in range(rounds):
        g = cmdgame.Game(p1, p2)
        g.start()
        winner = g.get_winner()
        if winner:
            if p1_name == winner:
                p1_win_count += 1
            else:
                p2_win_count += 1
        else:
            draw_count += 1
        
    print("Player {}: {} Wins".format(p1_name, p1_win_count))
    print("Player {}: {} Wins".format(p2_name, p2_win_count))
    print("Draws: {} ".format(draw_counter))

def main():
    rounds = 5
    p1_name = "Jeff"
    p2_name = "Dave"
    p3_name = "Alfred"
    p4_name = "Pumba"
    p5_name = "HAL-9000"
    p1 = player.HumanPlayer(p1_name)
    p2 = player.HumanPlayer(p2_name)
    p3 = player.AIPlayer(p3_name, gameengine.Difficulty.LOW)
    p4 = player.AIPlayer(p4_name, gameengine.Difficulty.MEDIUM)
    p5 = player.AIPlayer(p5_name, gameengine.Difficulty.HIGH)

    my_timer = threading.Timer(120.0, mytimer)
    my_timer.start()
    run_game(1, p1, p2, p1_name, p2_name)
    my_timer.cancel()
    
        
# If file is called from command line, run main() function
if __name__ == "__main__":
    main()
