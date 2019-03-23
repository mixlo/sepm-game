import sys
sys.path.append('/home/david/Documents/python/sepm/sepm-game/')
import socket, random, sys, re, uugame, commplatform
from commplatform import GameFactory 
#def test_valid():
    #create instance
    #have thread access value of instance
    #check if only valid input has been recieved
#def test_invalid():
def generateMatrix():
    strng = input()
    return strng

#def ma_to_str(ma):
 #   print(ma)
def test_integration():
    m = generateMatrix()
    #game = GameFactory.create_p_vs_p_game()
    gameMatrix = uugame.start_game_returning_matrix()
    if m != str(gameMatrix):
        print("ERROR")
        #ma_to_str(gameMatrix)
        print(gameMatrix)
        print("does not match")
        print(m)
    #create instance
    else:
        print("Success")
def test_run_normally():
    filename = "gp_record.txt"
    fh= open(filename, "a")
    m = generateMatrix()
    game = GameFactory.create_p_vs_p_game()
    gameMatrix = game.start_return()
    if m != str(gameMatrix):
        fh.write("ERROR\n")
        #write(gameMatrix)
        #write("does not match")
        #write(m)
        print("ERROR")
        #ma_to_str(gameMatrix)
        print(gameMatrix)
        print("does not match")
        print(m)
    #create instance
    else:
        fh.write("Success\n")
        print("Success")
    fh.close()
def main():
    
    
    #s = input("test").strip()
    #print(s)
    #print(sys.argv[1])
    if len(sys.argv) > 1 and sys.argv[1] == "integration":
        test_integration()
    elif len(sys.argv) > 1 and sys.argv[1] == "invalid":
        test_invalid()
    else:
        test_run_normally()
    
if __name__ == "__main__":
    main()
