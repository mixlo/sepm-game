#!/usr/bin/env python3

import gameengine, cmdgame, player, socket

# Abstract class for the menus of the game.
class AbsMenu(object):
    # These should be set with the constructor in derived classes.
    _num_options = 0
    _should_loop = False
    
    # Shows the menu. Repeatedly or not based on the _should_loop variable.
    def show(self):
        self._print_menu()
        option = self._prompt_option()
        self._perform_option(option)
        if self._should_loop:
            self.show()
    
    # Should be implemented in derived classes.
    def _print_menu(self):
        raise NotImplementedError()

    # Prompt the player for choice of option.
    # Options are represented by integer numbers from 1 and upwards.
    def _prompt_option(self):
        # Expects an integer in range [1,num_options].
        option_str = input("Please choose an option: ").strip()
        while True:
            if not option_str.isdigit():
                option_str = input("Must be an integer, try again: ").strip()
                continue
            option = int(option_str)
            if not 1 <= option <= self._num_options:
                option_str = input("Invalid option, try again: ").strip()
                continue
            return option

    # Should be implemented in derived classes
    def _perform_option(self, option):
        raise NotImplementedError()

# The start menu should present the choices of playing a local game, hosting
# a network game, joining a network game, hosting a tournament and quit.
# This menu should loop until the player chooses to quit.
class StartMenu(AbsMenu):
    # Should set _num_options and _should_loop variables appropriately.
    def __init__(self):
        pass

    # Should print the menu options.
    def _print_menu(self):
        pass

    # Should perform the correct action according to the selected option.
    def _perform_option(self, option):
        pass

    # Helper function to keep _perform_option a little cleaner.
    # Should show the "play local game" menu.
    def _play_local_game(self):
        pass

    # Helper function to keep _perform_option a little cleaner.
    # Should use GameFactory to create a hosted game, start the game and 
    # finally close the server socket and the socket to the opponent.
    def _play_hosted_game(self):
        pass

    # Helper function to keep _perform_option a little cleaner.
    # Should use GameFactory to create a joined game, start the game and 
    # finally close the socket to the opponent.
    def _play_joined_game(self):
        pass

    # Helper function to keep _perform_option a little cleaner.
    # Should show the "host tournament" menu.
    def _host_tournament(self):
        pass

# The local menu should present the choices of "player vs player", 
# "player vs AI", "AI vs AI or going back to the start menu.
# To make it easy and since it doesn't matter, the first player always go
# first. When playing against an AI, the player goes first.
# This menu shouldn't loop, the player should be returned back to the start 
# menu after finishing a game.
class LocalMenu(AbsMenu):
    # Should set _num_options variable appropriately.
    def __init__(self):
        pass

    # Should print the menu options.
    def _print_menu(self):
        pass

    # Should perform the correct action according to the selected option.
    def _perform_option(self, option):
        pass

# The tournament menu should present the options of which tournament to host,
# 4-player or 8-player. The requirements for this option is a bit unclear for
# the moment, should await further information before implementing this.
class TournamentMenu(AbsMenu):
    # Should set _num_options variable appropriately.
    def __init__(self):
        pass

    # Should print the menu options.
    def _print_menu(self):
        pass

    # Should perform the correct action according to the selected option.
    def _perform_option(self, option):
        pass

# This should be a static class consisting of only class methods that can be
# called directly without having to instantiate the class.
# It should contain methods for creating instances of the cmdgame.Game class,
# with settings depending on the type of game and input from the player.
class GameFactory(object):
    # Default settings for sockets.
    _port = 1337
    _timeout = 10
    _taken_names = []

    # Should prompt for two names and return a cmdgame.Game instance with two 
    # HumanPlayer instances.
    @classmethod
    def create_p_vs_p_game(cls):
        pass

    # Should prompt for two names and an AI difficulty and return a 
    # cmdgame.Game instance with a HumanPlayer and a AIPlayer instance.
    @classmethod
    def create_p_vs_ai_game(cls):
        #p_name = cls._
        pass

    # Should prompt for two names and two AI difficulties and return a 
    # cmdgame.Game instance with two AIPlayer instances.
    @classmethod
    def create_ai_vs_ai_game(cls):
        ai1_name = cls._prompt_name("In the right corner the AI:")
        _taken_names.append(ai1_name)
        ai1_diff = cls.prompt_difficulty(ai1_name)
        ai1 = player.AIPlayer(p1_name, ai1_diff)

        
        ai2_name = cls._prompt_name("And in the left corner the AI:")
        _taken_names.append(p2_name)
        ai2_diff = cls.prompt_difficulty(ai2_name)
        ai2 = player.AIPlayer(p1_name, ai1_diff)

        g = cmdgame.Game(ai1, ai2)
        g.start()
    # Should ask the player if they want to host the game as a human or an AI
    # and in the case of an AI, ask for a difficulty level.
    # Should listen for an incoming connection from an opponent via a socket
    # using the default port and timeout settings in this class. If the
    # connection times out, it should print an appropriate information message,
    # close the socket and return.
    # Should send the player/AI name to the opponent and then receive the name
    # of the opponent via the socket.
    # Finally, it should create a cmdgame.Game instance with a
    # NetworkHumanPlayer/NetworkAIPlayer and a NetworkOpponent instance, using
    # the information provided by the player and the network opponent.
    # Should return the cmdgame.Game instance, the listening socket and the
    # socket connected to the opponent.
    @classmethod
    def create_hosted_game(cls):
        pass

    # Should ask the player if they want to join the game as a human or an AI
    # and in the case of an AI, ask for a difficulty level.
    # Should ask for the IP address of the host and try to connect to the host
    # via a socket using the host IP together with the default port and timeout
    # settings in this class. If the connection times out, it should print an
    # appropriate information message, close the socket and return.
    # Should send the player/AI name to the opponent and then receive the name
    # of the opponent via the socket.
    # Finally, it should create a cmdgame.Game instance with a
    # NetworkHumanPlayer/NetworkAIPlayer and a NetworkOpponent instance, using
    # the information provided by the player and the network opponent.
    # Should return the cmdgame.Game instance and the socket connected to the
    # opponent.
    @classmethod
    def create_joined_game(cls):
        pass

    # Helper function to keep create_hosted_game a little cleaner.
    # Should try to connect to the host via a socket using the host IP together
    # with the default port and timeout settings in this class. If the
    # connection times out, it should close the socket and return. Otherwise,
    # it should return the socket.
    @classmethod
    def _establish_host_conn(cls, host_ip):
        pass

    # Helper function to keep create_hosted_game a little cleaner.
    # Should listen for an incoming connection from an opponent via a socket
    # using the default port and timeout settings in this class. If the
    # connection times out, it should close the socket and return. Otherwise,
    # it should return both the listening socket and the client socket that was
    # created upon successfully establishing the connection.
    @classmethod
    def _establish_client_conn(cls):
        pass

    # Should prompt for a name, making sure it isn't empty.
    @classmethod
    def _prompt_name(cls, title):
        
        p_str = input(title).strip()
        while True:
            valid, error = cls._check_name(p_str)
            if not valid:
                p_str = input(error).strip()
                continue
            
            return p_str
    @classmethod
    def _check_name(cls, name):
        if False:
            return False, "Invalid name, try again: "
        if name in _taken_names:
            return False, "Name already taken, try again: "
        return True
    # Should prompt for an AI difficulty, making sure it is valid.
    @classmethod
    def _prompt_difficulty(cls, title):
        p_str = input("Contender {} set to difficulty (1 for easy, 2 for meduim, 3 for hard): ".format(title)).strip()
        while True:
            valid, error = cls._check_difficulty(p_str)
            if not valid:
                p_str = input(error).strip()
                continue
            diff_int = int(p_str)
            if diff_int == 1:
                return gameengine.Difficulty.LOW
            elif diff_int == 2:
                return gameengine.Difficulty.MEDIUM
            else:
                return gameengine.Difficulty.HIGH
            
    @classmethod
    def _check_difficulty(cls, diff_str):
        try:
            diff_int = int(diff_str)
            if diff_int > 3:
                return False, "In order not to create skynet we capped the difficulty at 3, try again: "
            elif diff_int < 1:
                return False, "Cannot chose lower difficulty than 1, try again: "
        except ValueError:
            return False, "Input is not an int, please choose an int between 1 and 3, where 1 = easy AI, 2 = medium AI, 3 = hard AI: "       
        return True

    # Should prompt for an IPv4 address, making sure it is valid.
    @classmethod
    def _prompt_ip(cls, title):
        pass
if __name__ == "__main__":
    main()
