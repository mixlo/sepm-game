import sys
sys.path.append('/home/david/Documents/python/sepm/sepm-game/')
import unittest
import gameengine, cmdgame, player, state





def HAL_9000_vs_Pumba(rounds):
    draw_counter = 0
    pumba_win_count = 0
    hal_win_count = 0
    pumba_name = "Pumba"
    hal_name = "HAL 9000"

    p3 = player.AIPlayer("Alfred", gameengine.Difficulty.LOW)
    pumba = player.AIPlayer("Pumba", gameengine.Difficulty.MEDIUM)
    hal = player.AIPlayer("HAL 9000", gameengine.Difficulty.HIGH)
    
    for i in range(rounds):
        g = cmdgame.Game(pumba, hal)
        g.start()
        winner = g.get_winner()
        if winner:
            if pumba_name == winner:
                pumba_win_count += 1
            else:
                hal_win_count += 1
        else:
            draw_count += 1
    return hal_win_count, pumba_win_count, draw_counter
#print("Player {}: {} Wins".format(pumba_name, pumba_win_count))
 #   print("Player {}: {} Wins".format(hal_name, hal_win_count))
  #  print("Draws: {} ".format(draw_counter))

    
def HAL_9000_vs_Alfred(rounds):
    draw_counter = 0
    alfred_win_count = 0
    hal_win_count = 0
    alfred_name = "Alfred"
    hal_name = "HAL 9000"

    alfred = player.AIPlayer("Alfred", gameengine.Difficulty.LOW)
    pumba = player.AIPlayer("Pumba", gameengine.Difficulty.MEDIUM)
    hal = player.AIPlayer("HAL 9000", gameengine.Difficulty.HIGH)
    
    for i in range(rounds):
        g = cmdgame.Game(alfred, hal)
        g.start()
        winner = g.get_winner()
        if winner:
            if alfred_name == winner:
                alfred_win_count += 1
            else:
                hal_win_count += 1
        else:
            draw_count += 1
    return hal_win_count, alfred_win_count, draw_counter
    #print("Player {}: {} Wins".format(alfred_name, alfred_win_count))
    #print("Player {}: {} Wins".format(hal_name, hal_win_count))
    #print("Draws: {} ".format(draw_counter))
    

def read_stats(p1, p2, p1_wins, p2_wins, draws):
    print("Player {}: {} Wins".format(p1, p1_wins))
    print("Player {}: {} Wins".format(p2, p2_wins))
    print("Draws: {} ".format(draws))
    
def main():
    #only tests if 2 AI can run the game against eachother without a crash
    #does not test if the 2 AI:s are cheating, meaning the state or any part of the game is changed in a way it should not to be possible 
    rounds = 5
    g1_p1_w, g1_p2_w, g1_draws = HAL_9000_vs_Pumba(rounds)
    g2_p1_w, g2_p2_w, g2_draws = HAL_9000_vs_Alfred(rounds)
    read_stats("HAL-9000", "Pumba", g1_p1_w, g1_p2_w, g1_draws)
    read_stats("HAL-9000", "Alfred",g2_p1_w, g2_p2_w, g2_draws)

if __name__ == "__main__":
    main()
