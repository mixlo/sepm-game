#!/usr/bin/env python3

from commplatform import StartMenu
def start_game_returning_matrix():
    print("Welcome to UU-GAME!")
    print()
    return StartMenu().show()
    
def main():
    print("Welcome to UU-GAME!")
    print()
    StartMenu().show()
    
if __name__ == "__main__":
    main()
