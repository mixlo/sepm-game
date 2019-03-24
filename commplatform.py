#!/usr/bin/env python3

import socket, random, re, time
from datetime import datetime
from gameplatform import Game, GameStatusMsg
from player import (
    HumanPlayer,
    AIPlayer,
    NetworkHumanPlayer,
    NetworkAIPlayer,
    NetworkOpponent,
    QuitException,
    QuitHardException
)

DEBUG = False

class PlayerType:
    Human = 1
    AI = 2

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
        option_str = input("Please choose an option: ")
        while True:
            option_str = option_str.strip()
            if not option_str.isdigit():
                option_str = input("Must be an integer, try again: ")
                continue
            option = int(option_str)
            if (not 1 <= option <= self._num_options) and not option == 7357:
                option_str = input("Invalid option, try again: ")
                continue
            print()
            return option

    def _perform_option(self, option):
        raise NotImplementedError()

class StartMenu(AbsMenu):
    mtrx = None
    testmode = False
    #end_of_game =False
    init = True
    def __init__(self):
        self._num_options = 5
        self._should_loop = True

    def show(self):
        frst = self.init
        if frst:
            self.testmode = False
        
        self.init = False
        try:
            super().show()
        except QuitHardException:
            self._should_loop = False
        if self.testmode and frst:
            print(self.mtrx)
            return self.mtrx

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
        elif option == 7357:
            self.testmode = True
    def _play_local_game(self):
        LocalMenu().show()

    def _play_hosted_game(self):
        csock = None
        try:
            game, csock = GameFactory.create_hosted_game()
            if game is not None:
                if self.testmode:
                    
                    self.mtrx = game.start_return()
                else:
                    game.start()
        except QuitException:
            pass
        except QuitHardException:
            raise
        except Exception as e:
            print("An error occurred:")
            print(e)
            if csock is not None:
                csock.send(GameStatusMsg.ERROR.encode("utf-8"))
            if DEBUG: raise
        except:
            # Catching key e.g. interrupts
            if csock is not None:
                csock.send(GameStatusMsg.ERROR.encode("utf-8"))
        finally:
            if csock is not None: csock.close()
            print()

    def _play_joined_game(self):
        lsock, hsock = None, None
        try:
            game, lsock, hsock = GameFactory.create_joined_game()
            if game is not None:
                if self.testmode:
                    self.mtrx = game.start_return()
                else:
                    game.start()
        except QuitException:
            pass
        except QuitHardException:
            raise
        except Exception as e:
            print("An error occurred:")
            print(e)
            if hsock is not None:
                hsock.send(GameStatusMsg.ERROR.encode("utf-8"))
            if DEBUG: raise
        except:
            # Catching key e.g. interrupts
            if hsock is not None:
                hsock.send(GameStatusMsg.ERROR.encode("utf-8"))
        finally:
            if lsock is not None: lsock.close()
            if hsock is not None: hsock.close()
            print()

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
            self._run_game(GameFactory.create_p_vs_p_game)
        elif option == 2:
            self._run_game(GameFactory.create_p_vs_ai_game)
        elif option == 3:
            self._run_game(GameFactory.create_ai_vs_ai_game)
        elif option == 4:
            pass

    def _run_game(self, create_game_fun):
        try:
            create_game_fun().start()
        except QuitException:
            pass
        except QuitHardException:
            raise
        except Exception as e:
            print("An error occurred:")
            print(e)
            if DEBUG: raise
        except:
            # Catching key e.g. interrupts
            pass
        finally:
            print()

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
        try:
            GameFactory.create_local_tournament().play()
        except QuitException:
            pass
        except QuitHardException:
            raise
        except Exception as e:
            print("An error occurred:")
            print(e)
            if DEBUG: raise
        except:
            # Catching key e.g. interrupts
            pass
        finally:
            print()

    def _play_hosted_tournament(self):
        csock = None
        try:
            t, csock = GameFactory.create_hosted_tournament()
            if t is not None:
                t.play()
        except QuitException:
            pass
        except QuitHardException:
            raise
        except Exception as e:
            print("An error occurred:")
            print(e)
            if csock is not None:
                csock.send(GameStatusMsg.ERROR.encode("utf-8"))
            if DEBUG: raise
        except:
            # Catching key e.g. interrupts
            if csock is not None:
                csock.send(GameStatusMsg.ERROR.encode("utf-8"))
        finally:
            if csock is not None: csock.close()
            print()

    def _play_joined_tournament(self):
        lsock, hsock = None, None
        try:
            t, lsock, hsock = GameFactory.create_joined_tournament()
            if t is not None:
                t.play()
        except QuitException:
            pass
        except QuitHardException:
            raise
        except Exception as e:
            print("An error occurred:")
            print(e)
            if hsock is not None:
                hsock.send(GameStatusMsg.ERROR.encode("utf-8"))
            if DEBUG: raise
        except:
            # Catching key e.g. interrupts
            if hsock is not None:
                hsock.send(GameStatusMsg.ERROR.encode("utf-8"))
        finally:
            if lsock is not None: lsock.close()
            if hsock is not None: hsock.close()
            print()

class GameFactory(object):
    _invalid_input = False
    _default_port = 1337
    _tournament_port = 1338
    _bc_ip = "255.255.255.255"
    _wait_client_timeout = 60
    _wait_host_timeout = 5
    _connect_client_timeout = 5
    _host_tournament_msg = """
You are the host of a {}-player tournament. Please provide your {} player(s) 
and wait for the connected client to provide the remaining {} participant(s).
"""
    _join_tournament_msg = """
You have joined a {}-player tournament. The host is entering {} player(s), 
please provide the remaining {} participant(s).
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
        ai_diff = cls._prompt_difficulty("AI")
        print()
        p = HumanPlayer(p_name)
        ai = AIPlayer("Bot", ai_diff)
        return Game(p, ai)

    @classmethod
    def create_ai_vs_ai_game(cls):
        ai1_diff = cls._prompt_difficulty("AI 1")
        ai2_diff = cls._prompt_difficulty("AI 2")
        print()
        ai1 = AIPlayer("Bot 1", ai1_diff)
        ai2 = AIPlayer("Bot 2", ai2_diff)
        return Game(ai1, ai2)

    @classmethod
    def create_hosted_game(cls):
        p_name, ai_diff = None, None
        if input("Host as AI? (y/n): ").strip().lower() == "y":
            p_name = "Host"
            ai_diff = cls._prompt_difficulty("AI")
        else:
            p_name = cls._prompt_name("host player", [])
        print("Waiting for opponent...")
        csock = cls._establish_client_conn(cls._default_port)
        if csock is None:
            print("No opponent connected within {} seconds."
                  .format(cls._wait_client_timeout))
            print()
            return None, None
        p = None
        if ai_diff is None:
            p = NetworkHumanPlayer(p_name, csock)
        else:
            p = NetworkAIPlayer(p_name, ai_diff, csock)
        csock.send(p.name.encode("utf-8"))
        opp_name = csock.recv(1024).decode("utf-8")
        print("Established connection with opponent {}.".format(opp_name))
        o = NetworkOpponent(opp_name, csock)
        print()
        return Game(p, o), csock

    @classmethod
    def create_joined_game(cls):
        print("Connecting to host...")
        lsock, hsock = cls._establish_host_conn(cls._default_port)
        if hsock is None:
            print("Couldn't connect to host.")
            print()
            return None, None, None
        opp_name = hsock.recv(1024).decode("utf-8")
        print("Established connection with opponent {}.".format(opp_name))
        p = None
        if input("Join as AI? (y/n): ").strip().lower() == "y":
            p_name = "Client"
            ai_diff = cls._prompt_difficulty("AI")
            p = NetworkAIPlayer(p_name, ai_diff, hsock)
        else:
            p_name = cls._prompt_name("joining player",
                                      [opp_name.split("AI ").pop()])
            p = NetworkHumanPlayer(p_name, hsock)
        hsock.send(p.name.encode("utf-8"))
        o = NetworkOpponent(opp_name, hsock)
        print()
        return Game(o, p), lsock, hsock

    @classmethod
    def create_local_tournament(cls):
        p_count = cls._prompt_participants_count()
        h_count = cls._prompt_human_participants_count(p_count)
        participants = cls._get_random_ai_players(p_count - h_count)
        participants += cls._prompt_human_players(h_count)
        random.shuffle(participants)
        return LocalTournament(participants)

    @classmethod
    def create_hosted_tournament(cls):
        p_count = cls._prompt_participants_count()
        h_count = cls._prompt_human_participants_count(p_count)
        participants = cls._get_random_ai_players_data(p_count - h_count)
        participants += cls._prompt_human_players_data(h_count)
        print("Waiting for client computer to connect...")
        csock = cls._establish_client_conn(cls._tournament_port)
        if csock is None:
            print("No one connected within {} seconds."
                  .format(cls._wait_client_timeout))
            print()
            return None, None
        print("Established connection with client computer.")
        p_str = ",".join(["|".join(["{}:{}".format(k,v) for k,v in p.items()])
                          for p in participants])
        seed = datetime.now().timestamp()
        csock.send("{}#{}".format(seed, p_str).encode("utf-8"))
        random.seed(seed)
        random.shuffle(participants)
        return NetworkTournament(participants, csock), csock

    @classmethod
    def create_joined_tournament(cls):
        print("Connecting to host...")
        lsock, hsock = cls._establish_host_conn(cls._tournament_port)
        if hsock is None:
            print("Couldn't connect to host.")
            print()
            return None, None, None
        print("Established connection with tournament host.")
        seed_str, p_str = hsock.recv(1024).decode("utf-8").split("#")
        participants = [{k:v for k,v in [e.split(":") for e in p.split("|")]}
                        for p in p_str.split(",")]
        for p in participants:
            p["type"] = int(p["type"])
            if "aidiff" in p:
                p["aidiff"] = int(p["aidiff"])
        random.seed(float(seed_str))
        random.shuffle(participants)
        return NetworkTournament(participants, hsock, False), lsock, hsock

    @classmethod
    def _establish_host_conn(cls, port):
        cls._broadcast_ip(port)
        lsock, hsock = cls._wait_for_host(port)
        return lsock, hsock

    @classmethod
    def _establish_client_conn(cls, port):
        csock = None
        client_ip = cls._get_client_ip(port)
        if client_ip is not None:
            csock = cls._connect_to_client(client_ip, port)
        return csock

    @classmethod
    def _broadcast_ip(cls, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto("UUGAME".encode("utf-8"), (cls._bc_ip, port))
        s.close()

    @classmethod
    def _wait_for_host(cls, port):
        lsock = socket.socket()
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lsock.bind(("", port))
        lsock.listen(1)
        lsock.settimeout(cls._wait_host_timeout)
        try:
            hsock, _ = lsock.accept()
            return lsock, hsock
        except:
            lsock.close()
            return None, None
        
    @classmethod
    def _get_client_ip(cls, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", port))
        s.settimeout(cls._wait_client_timeout)
        ip = None
        try:
            _, (ip, _) = s.recvfrom(1024)
        finally:
            s.close()
            return ip

    @classmethod
    def _connect_to_client(cls, client_ip, port):
        # Have to use time.sleep(), csock.settimeout()
        # doesn't seem to work as expected
        for _ in range(cls._connect_client_timeout):
            csock = socket.socket()
            try:
                csock.connect((client_ip, port))
                return csock
            except:
                csock.close()
            time.sleep(1)
        return None

    @classmethod
    def _prompt_participants_count(cls):
        # Expects an integer in range [3,8]
        msg = "Enter number of participants: "
        return cls._prompt_num(msg, 3, 8)

    @classmethod
    def _prompt_human_participants_count(cls, p_count):
        # Expects an integer in range [0,p_count]
        msg = "Enter number of human participants: "
        return cls._prompt_num(msg, 0, p_count)

    @classmethod
    def _get_random_ai_players(cls, p_count):
        return [AIPlayer(p["name"][3:], p["aidiff"])
                for p in cls._get_random_ai_players_data(p_count)]
    
    @classmethod
    def _get_random_ai_players_data(cls, p_count):
        ais = []
        for i in range(p_count):
            ais.append({"type": PlayerType.AI,
                        "name": "AI Bot " + str(i+1),
                        "aidiff": random.randint(1, 3)})
        return ais

    @classmethod
    def _prompt_human_players(cls, p_count):
        return [HumanPlayer(p["name"])
                for p in cls._prompt_human_players_data(p_count)]
    
    @classmethod
    def _prompt_human_players_data(cls, p_count):
        humans, taken_names = [], []
        for i in range(p_count):
            p_name = cls._prompt_name("Player " + str(i+1), taken_names)
            taken_names.append(p_name)
            humans.append({"type": PlayerType.Human, "name": p_name})
        print()
        return humans

    @classmethod
    def _prompt_name(cls, title, taken):
        regex = "^(?!AI )[A-Z0-9]+(?:[ -][A-Z0-9]+)*$"
        name_fmt = re.compile(regex, re.IGNORECASE)
        # Expects a non-empty string
        name = input("Enter the name of {}: ".format(title))
        while True:
            name = name.strip()
            if len(name) == 0:
                name = input("Name can't be empty, try again: ")
                continue
            if len(name) > 15:
                name = input("Use at most 15 characters, try again: ")
                continue
            if name_fmt.match(name) is None:
                name = input("Invalid name, try again: ")
                continue
            if name in taken:
                name = input("Name is taken, try again: ")
                continue
            return name

    @classmethod
    def invalid_input():
        return _invalid_input

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
            if 3 < diff:
                diff_str = input("In order not to create skynet, the " +
                                 "difficulty is capped at 3, " +
                                 "try again: ").strip()
                continue
            if 1 > diff:
                diff_str = input("Choosing difficulties lower than 1 will " +
                                 "cause the AI to self-destruct, " +
                                 "try again: ").strip()
                continue
            return diff


        #msg = "Enter {} difficulty (LOW=1, MEDIUM=2, HIGH=3): ".format(title)
        #return cls._prompt_num(msg, 1, 3)

    @classmethod
    def _prompt_num(cls, msg, start, end):
        # Expects an integer in range [start,end]
        num_str = input(msg)
        while True:
            num_str = num_str.strip()
            if not num_str.isdigit():
                num_str = input("Invalid number, try again: ")
                continue
            num = int(num_str)
            if not start <= num <= end:
                num_str = input("Number must be between {}-{}, try again: "
                                .format(start, end))
                continue
            return num

class AbsTournament(object):
    _byes_msg = """
Since this is a single elimination tournament and there are {} participants, 
{} player(s) have been given a bye."""

    def __init__(self, participants):
        self._participants = participants[:]
        self._bp = BracketPrinter([self._get_pname(p) for p in participants])

    def play(self):
        print("Welcome to the tournament!")
        print("The participants are:")
        print()
        for p in self._participants:
            print(" -", self._get_pname(p))
        byes = self._calc_byes(len(self._participants))
        if byes != 0:
            print(self._byes_msg.format(len(self._participants), byes))
        print()
        print("Draws are not allowed.")
        print("Games will be played and replayed until a winner is declared.")
        print()
        print("Let's begin!")
        print()
        self._bp.print_bracket()
        self._press_enter_to_continue()
        winner = self._play_tournament_check_byes(self._participants, byes)
        print("{} wins the entire tournament!".format(winner))
        print()
        print()

    def _calc_byes(self, num_players):
        return (1 << (num_players - 1).bit_length()) - num_players

    def _play_tournament_check_byes(self, players, byes):
        if byes != 0:
            players = players[-byes:] + self._play_brackets(players[:-byes])
        return self._play_tournament(players)

    def _play_tournament(self, players):
        if len(players) == 1:
            return self._get_pname(players[0])
        winners = self._play_brackets(players)
        return self._play_tournament(winners)

    def _play_brackets(self, players):
        raise NotImplementedError()

    def _press_enter_to_continue(self):
        raise NotImplementedError()

    def _get_pname(self, player):
        raise NotImplementedError()

class LocalTournament(AbsTournament):
    def __init__(self, participants):
        super().__init__(participants)
    
    def _play_brackets(self, players):
        games = [Game(*p) for p in zip(players[::2], players[1::2])]
        winners = []
        for g in games:
            g.start()
            while g.winner is None:
                g.reset()
                g.start()
            winners.append(g.winner)
            self._bp.increment(g.winner.name)
            self._bp.print_bracket()
            self._press_enter_to_continue()
        return winners

    def _press_enter_to_continue(self):
        input("Press enter to continue...")
        print()

    def _get_pname(self, player):
        return player.name

class NetworkTournament(AbsTournament):
    def __init__(self, participants, opp_sock, is_hosting=True):
        super().__init__(participants)
        self._opp_sock = opp_sock
        self._is_hosting = is_hosting

    def _play_brackets(self, players):
        games = self._get_games(players)
        winners = []
        for g, p_data in games:
            g.start()
            while g.winner is None:
                g.reset()
                g.start()
            winners.append(p_data[g.winner.name])
            self._bp.increment(g.winner.name)
            self._bp.print_bracket()
            self._press_enter_to_continue()
        return winners

    def _get_games(self, players):
        games, pairs = [], []
        for i in range(0, len(players), 2):
            p1, p2 = players[i], players[i+1]
            players_data = {p1["name"]: p1, p2["name"]: p2}
            p1, p2 = self._get_player_instances(p1, p2)
            pairs.append((p1, p2) if self._is_hosting else (p2, p1))
            if not self._is_hosting:
                p1, p2 = p2, p1
            games.append((Game(p1, p2), players_data))
        print("For this bracket segment:")
        print()
        print("{0: <23}{1: <23}".format("On host computer:",
                                        "On client computer:"))
        for p1, p2 in pairs:
            print(" - {0: <20} - {1: <20}".format(p1.name, p2.name))
        print()
        return games

    def _get_player_instances(self, p1, p2):
        if not self._is_hosting:
            p1, p2 = p2, p1
        if p1["type"] == PlayerType.Human:
            p1 = NetworkHumanPlayer(p1["name"], self._opp_sock)
        else:
            p1 = NetworkAIPlayer(p1["name"][3:], p1["aidiff"], self._opp_sock)
        p2 = NetworkOpponent(p2["name"], self._opp_sock)
        return p1, p2

    def _calc_byes(self, num_players):
        return (1 << (num_players - 1).bit_length()) - num_players

    def _press_enter_to_continue(self):
        input("Press enter to continue...")
        msg = "CONTINUE"
        self._opp_sock.send(msg.encode("utf-8"))
        print("Waiting for opponent...")
        self._opp_sock.recv(len(msg))
        print()

    def _get_pname(self, player):
        return player["name"]

class BracketPrinter(object):
    _line_len = 20
    
    def __init__(self, player_names):
        self._positions = player_names[:]
        num_players = len(player_names)
        self._brkt_str = self._make_bracket_str(num_players)
        self._fillers = "?" * (2 * num_players - 1)

    def increment(self, player_name):
        self._positions.append(player_name)

    def print_bracket(self):
        print("Bracket status:")
        print()
        print()
        print(self._brkt_str.format(*self._positions, *self._fillers))
        print()
        print()

    def _make_bracket_str(self, num_players):
        nlvls = (num_players-1).bit_length() + 1
        nbyes = pow(2, nlvls-1) - num_players
        level_strs = self._make_brkt_lvl_strs(nlvls, byes=nbyes)
        return "\n".join(list(map("".join, zip(*level_strs))))

    def _make_brkt_lvl_strs(self, nlvls, lvl=1, counter=0, byes=0):
        if lvl > nlvls:
            return [[""] * (pow(2, nlvls) - 1)]
        padding = pow(2, lvl-1) - 1
        lines, switch = [], 0
        for i in range(padding):
            lines.append(" " * (self._line_len+1))
        for i in range(pow(2, lvl+1) * byes):
            lines.append(" " * (self._line_len+1))
        for i in range(pow(2, lvl+1) * byes, pow(2, nlvls) - padding * 2 - 1):
            if i % pow(2, lvl) == 0:
                lines.append("{{{0}:-<{1}}}+".format(counter, self._line_len))
                switch ^= 1
                counter += 1
            else:
                if switch: lines.append(" " * self._line_len + "|")
                else:      lines.append(" " * (self._line_len+1))
        for i in range(padding):
            lines.append(" " * (self._line_len+1))
        return [lines] + self._make_brkt_lvl_strs(nlvls, lvl+1, counter, 0)
