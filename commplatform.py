#!/usr/bin/env python3

import socket, random, re
from math import ceil, log
from datetime import datetime
from gameplatform import Game
from player import (
    HumanPlayer,
    AIPlayer,
    NetworkHumanPlayer,
    NetworkAIPlayer,
    NetworkOpponent
)

class AbsMenu(object):
    # These should be set with the constructor in derived classes
    _num_options = 0
    _should_loop = False
    
    def show(self):
        self._print_menu()
        option = self._prompt_option()
        self._perform_option(option)
        if self._should_loop:
            self.show()
    
    def _print_menu(self):
        raise NotImplementedError()
    
    def _prompt_option(self):
        # Expects an integer in range [1,num_options]
        option_str = input("Please choose an option: ").strip()
        while True:
            if not option_str.isdigit():
                option_str = input("Must be an integer, try again: ").strip()
                continue
            option = int(option_str)
            if not 1 <= option <= self._num_options:
                option_str = input("Invalid option, try again: ").strip()
                continue
            print()
            return option

    def _perform_option(self, option):
        raise NotImplementedError()

class StartMenu(AbsMenu):
    def __init__(self):
        self._num_options = 5
        self._should_loop = True

    def _print_menu(self):
        print("What do you want to do?")
        print("1. Play local game")
        print("2. Host network game")
        print("3. Join network game")
        print("4. Play tournament")
        print("5. Quit")
        print()

    def _perform_option(self, option):
        if option == 1:
            self._play_local_game()
        elif option == 2:
            self._play_hosted_game()
        elif option == 3:
            self._play_joined_game()
        elif option == 4:
            self._play_tournament()
        elif option == 5:
            print("Goodbye!")
            self._should_loop = False
        
    def _play_local_game(self):
        LocalMenu().show()

    def _play_hosted_game(self):
        game, server_sock, opp_sock = GameFactory.create_hosted_game()
        if game is None:
            return
        game.start()
        server_sock.close()
        opp_sock.close()

    def _play_joined_game(self):
        game, opp_sock = GameFactory.create_joined_game()
        if game is None:
            return
        game.start()
        opp_sock.close()

    def _play_tournament(self):
        TournamentMenu().show()

class LocalMenu(AbsMenu):
    def __init__(self):
        self._num_options = 4

    def _print_menu(self):
        print("What kind of local game do you want to play?")
        print("1. Player vs Player")
        print("2. Player vs AI")
        print("3. AI vs AI")
        print("4. Back to start menu")
        print()

    def _perform_option(self, option):
        if option == 1:
            GameFactory.create_p_vs_p_game().start()
        elif option == 2:
            GameFactory.create_p_vs_ai_game().start()
        elif option == 3:
            GameFactory.create_ai_vs_ai_game().start()
        elif option == 4:
            pass

# Matches restarts until they have a winner, draws not accepted.
class TournamentMenu(AbsMenu):
    def __init__(self):
        self._num_options = 4

    def _print_menu(self):
        print("What kind of tournament do you want to play?")
        print("1. Local tournament")
        print("2. Host network tournament")
        print("3. Join network tournament")
        print("4. Back to start menu")
        print()

    def _perform_option(self, option):
        if option == 1:
            self._play_local_tournament()
        elif option == 2:
            self._play_hosted_tournament()
        elif option == 3:
            self._play_joined_tournament()
        elif option == 4:
            pass

    def _play_local_tournament(self):
        GameFactory.create_local_tournament().play()

    def _play_hosted_tournament(self):
        t, server_sock, opp_sock = GameFactory.create_hosted_tournament()
        if t is None:
            return
        t.play()
        server_sock.close()
        opp_sock.close()

    def _play_joined_tournament(self):
        t, opp_sock = GameFactory.create_joined_tournament()
        if t is None:
            return
        t.play()
        opp_sock.close()

class GameFactory(object):
    _default_port = 1337
    _tournament_port = 1338
    _conn_timeout = 60

    _host_tournament_msg = """
You are the host of a {}-player tournament. Please provide your {} players and 
wait for the connected client to provide the remaining {} participants.
"""
    _join_tournament_msg = """
You have joined a {}-player tournament. The host is entering {} players, 
please provide the remaining {} participants.
"""
    
    @classmethod
    def create_p_vs_p_game(cls):
        p1_name = cls._prompt_name("Player 1", [])
        p2_name = cls._prompt_name("Player 2", [p1_name])
        print()
        p1 = HumanPlayer(p1_name)
        p2 = HumanPlayer(p2_name)
        return Game(p1, p2)

    @classmethod
    def create_p_vs_ai_game(cls):
        p_name = cls._prompt_name("Player", [])
        ai_name = cls._prompt_name("AI", [p_name])
        ai_diff = cls._prompt_difficulty("AI")
        print()
        p = HumanPlayer(p_name)
        ai = AIPlayer(ai_name, ai_diff)
        return Game(p, ai)

    @classmethod
    def create_ai_vs_ai_game(cls):
        ai1_name = cls._prompt_name("AI 1", [])
        ai1_diff = cls._prompt_difficulty("AI 1")
        ai2_name = cls._prompt_name("AI 2", [ai1_name])
        ai2_diff = cls._prompt_difficulty("AI 2")
        print()
        ai1 = AIPlayer(ai1_name, ai1_diff)
        ai2 = AIPlayer(ai2_name, ai2_diff)
        return Game(ai1, ai2)

    @classmethod
    def create_hosted_game(cls):
        p_name = cls._prompt_name("host player", [])
        ai_diff = None
        if input("Host as AI? (y/n): ").strip().lower() == "y":
            ai_diff = cls._prompt_difficulty("AI")
        print("Waiting for opponent...")
        server_sock, opp_sock = cls._establish_client_conn(cls._default_port)
        if opp_sock is None:
            print("No opponent connected within {} seconds."
                  .format(cls._conn_timeout))
            print()
            return None, None, None
        p = None
        if ai_diff is None:
            p = NetworkHumanPlayer(p_name, opp_sock)
        else:
            p = NetworkAIPlayer(p_name, ai_diff, opp_sock)
        opp_sock.send(p.name.encode("utf-8"))
        opp_name = opp_sock.recv(1024).decode("utf-8")
        print("Established connection with opponent {}.".format(opp_name))
        o = NetworkOpponent(opp_name, opp_sock)
        print()
        return Game(p, o), server_sock, opp_sock

    @classmethod
    def create_joined_game(cls):
        opp_addr = cls._prompt_ip("host")
        print("Connecting to host...")
        opp_sock = cls._establish_host_conn(opp_addr, cls._default_port)
        if opp_sock is None:
            print("Couldn't connect to host.")
            print()
            return None, None
        opp_name = opp_sock.recv(1024).decode("utf-8")
        print("Established connection with opponent {}.".format(opp_name))
        p_name = cls._prompt_name("joining player",
                                  [opp_name.split("AI ").pop()])
        p = None
        if input("Join as AI? (y/n): ").strip().lower() == "y":
            ai_diff = cls._prompt_difficulty("AI")
            p = NetworkAIPlayer(p_name, ai_diff, opp_sock)
        else:
            p = NetworkHumanPlayer(p_name, opp_sock)
        opp_sock.send(p.name.encode("utf-8"))
        o = NetworkOpponent(opp_name, opp_sock)
        print()
        return Game(o, p), opp_sock

    @classmethod
    def create_local_tournament(cls):
        p_count = cls._prompt_participants_count()
        participants = cls._prompt_participants(p_count)
        random.shuffle(participants)
        return Tournament(participants)

    @classmethod
    def create_hosted_tournament(cls):
        p_count = cls._prompt_participants_count()
        p_count_local = cls._prompt_host_participants_count(p_count)
        print("Waiting for client computer to connect...")
        server_sock, opp_sock = cls._establish_client_conn(cls._tournament_port)
        if opp_sock is None:
            print("No one connected within {} seconds."
                  .format(cls._conn_timeout))
            print()
            return None, None, None
        opp_sock.send("{},{}".format(p_count, p_count_local).encode("utf-8"))
        print("Established connection with client computer.")
        print(cls._host_tournament_msg
              .format(p_count, p_count_local, p_count - p_count_local))
        participants = cls._prompt_network_participants(p_count_local,
                                                        opp_sock,
                                                        [])
        opp_sock.send(",".join([p.name for p in participants]).encode("utf-8"))
        print("Waiting for client's players...")
        print()
        opp_p_names = opp_sock.recv(1024).decode("utf-8").split(",")
        participants = (participants +
                        [NetworkOpponent(n, opp_sock) for n in opp_p_names])
        seed = datetime.now().timestamp()
        opp_sock.send(str(seed).encode("utf-8"))
        random.seed(seed)
        random.shuffle(participants)
        return Tournament(participants), server_sock, opp_sock

    @classmethod
    def create_joined_tournament(cls):
        opp_addr = cls._prompt_ip("host")
        print("Connecting to host...")
        opp_sock = cls._establish_host_conn(opp_addr, cls._tournament_port)
        if opp_sock is None:
            print("Couldn't connect to host.")
            print()
            return None, None
        counts = opp_sock.recv(1024).decode("utf-8")
        p_count, p_count_host = [int(c) for c in counts.split(",")]
        p_count_local = p_count - p_count_host
        print("Established connection with tournament host.")
        print(cls._join_tournament_msg
              .format(p_count, p_count_host, p_count_local))
        print("Waiting for host's players...")
        print()
        opp_p_names = opp_sock.recv(1024).decode("utf-8").split(",")
        taken_names = [n.split("AI ").pop() for n in opp_p_names]
        participants = cls._prompt_network_participants(p_count_local,
                                                        opp_sock,
                                                        taken_names)
        opp_sock.send(",".join([p.name for p in participants]).encode("utf-8"))
        participants = ([NetworkOpponent(n, opp_sock) for n in opp_p_names] +
                        participants)
        seed = float(opp_sock.recv(1024).decode("utf-8"))
        random.seed(seed)
        random.shuffle(participants)
        return Tournament(participants, False), opp_sock

    @classmethod
    def _establish_host_conn(cls, host_ip, port):
        host_sock = socket.socket()
        try:
            host_sock.connect((host_ip, port))
            return host_sock
        except socket.error:
            host_sock.close()
            return None

    @classmethod
    def _establish_client_conn(cls, port):
        server_sock = socket.socket()
        server_sock.bind(('', port))
        server_sock.listen(1)
        server_sock.settimeout(cls._conn_timeout)
        try:
            client_sock, _ = server_sock.accept()
            return server_sock, client_sock
        except socket.error:
            server_sock.close()
            return None, None

    @classmethod
    def _prompt_name(cls, title, taken):
        name_fmt = re.compile("^(?!AI )[A-Z0-9]+(?:[ -][A-Z0-9]+)*$",
                              re.IGNORECASE)
        # Expects a non-empty string
        name = input("Enter the name of {}: ".format(title)).strip()
        while True:
            if len(name) == 0:
                name = input("Name can't be empty, try again: ").strip()
                continue
            if len(name) > 15:
                name = input("Use at most 15 characters, try again: ").strip()
                continue
            if name_fmt.match(name) is None:
                name = input("Invalid name, try again: ").strip()
                continue
            if name in taken:
                name = input("Name is taken, try again: ").strip()
                continue
            return name

    @classmethod
    def _prompt_difficulty(cls, title):
        # Expects an integer in range [1,3]
        diff_str = input("Enter {} difficulty (LOW=1, MEDIUM=2, HIGH=3): "
                         .format(title)).strip()
        while True:
            if not diff_str.isdigit():
                diff_str = input("Invalid difficulty, try again: ").strip()
                continue
            diff = int(diff_str)
            if not 1 <= diff <= 3:
                diff_str = input("Invalid difficulty, try again: ").strip()
                continue
            return diff

    @classmethod
    def _prompt_ip(cls, title):
        # Expects an IPv4 address (X.X.X.X)
        ip = input("Enter IPv4 address of {}: ".format(title)).strip()
        while True:
            try:
                socket.inet_pton(socket.AF_INET, ip)
                return ip
            except socket.error:
                ip = input("Invalid IPv4 address, try again: ").strip()

    @classmethod
    def _prompt_participants(cls, p_count):
        participants, taken_names = [], []
        for i in range(p_count):
            p_name = cls._prompt_name("Player " + str(i+1), taken_names)
            taken_names.append(p_name)
            if input("Should player be an AI? (y/n): ").strip().lower() == "y":
                ai_diff = cls._prompt_difficulty("AI")
                participants.append(AIPlayer(p_name, ai_diff))
            else:
                participants.append(HumanPlayer(p_name))
        print()
        return participants

    @classmethod
    def _prompt_network_participants(cls, p_count, opp_sock, taken):
        participants, taken = [], taken[:]
        for i in range(p_count):
            p_name = cls._prompt_name("Player " + str(i+1), taken)
            taken.append(p_name)
            if input("Should player be an AI? (y/n): ").strip().lower() == "y":
                ai_diff = cls._prompt_difficulty("AI")
                participants.append(NetworkAIPlayer(p_name, ai_diff, opp_sock))
            else:
                participants.append(NetworkHumanPlayer(p_name, opp_sock))
        print()
        return participants

    @classmethod
    def _prompt_participants_count(cls):
        # Expects an integer in range [3,8]
        return cls._prompt_num_in_range("Enter number of participants: ", 3, 8)

    @classmethod
    def _prompt_host_participants_count(cls, p_count):
        # Expects an integer in range [3,8]
        return cls._prompt_num_in_range("Enter number of participants from " +
                                        "this computer: ", 1, p_count)

    @classmethod
    def _prompt_num_in_range(cls, msg, start, end):
        # Expects an integer in range [start,end]
        num_str = input(msg).strip()
        while True:
            if not num_str.isdigit():
                num_str = input("Invalid number, try again: ").strip()
                continue
            num = int(num_str)
            if not start <= num <= end:
                num_str = input("Number must be between {}-{}, try again: "
                                .format(start, end)).strip()
                continue
            return num

class Tournament(object):
    def __init__(self, participants, is_hosting=True):
        self._participants = participants[:]
        self._placings = []
        self._is_hosting = is_hosting

    def play(self):
        print("Welcome to the tournament!")
        print("The participants are:")
        print()
        for p in self._participants:
            print(" -", p.name)
        print()
        print("Let's begin!")
        print()
        self._play_tournament(self._participants)
        print("Final scoreboard!")
        for i, p in enumerate(self._placings):
            print("{}. {}".format(i+1, p.name))
        print()

    def _play_tournament(self, players):
        if len(players) == 1:
            self._placings.insert(0, players[0])
        if len(players) >= 2:
            winners, losers = self._play_brackets(players)
            self._play_tournament(losers)
            self._play_tournament(winners)
    
    def _play_brackets(self, players):
        games, winners, losers = [], [], []
        # Byes will only occur first time
        byes = pow(2, ceil(log(len(players), 2))) - len(players)
        if byes != 0:
            winners = players[-byes:]
            players = players[:-byes]
        for i in range(0, len(players), 2):
            p1, p2 = players[i], players[i+1]
            if (type(p1) != type(p2) and 
                ((isinstance(p1, NetworkOpponent) and self._is_hosting) or
                 (isinstance(p2, NetworkOpponent) and not self._is_hosting))):
                games.append(Game(p2, p1))
            else:
                games.append(Game(p1, p2))
        for g in games:
            g.start()
            while g.winner is None:
                g.reset()
                g.start()
            winners.append(g.winner)
            losers.append(g.loser)
        return winners, losers
