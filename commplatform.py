class Comm(object):
    pass

class Controller(object):
    pass

class View(object):
    "Player vs Player"
    "Player vs AI"
    "Host Network Game"
    "Join Network Game"
    "Host Tournament"

class Model(object):
    pass

class Player(object):
    def choose_piece(self):
        raise NotImplementedError("Abstract method")
    def choose_square(self):
        raise NotImplementedError("Abstract method")

class CmdPlayer(Player):
    def choose_piece(self):
        return input("Choose a piece for the opponent to place")
    def choose_square(self):
        return input("Choose a square on which to place the piece")

class LocalPlayer(Player):
    pass

class NetworkPlayer(Player):
    def __init__(self, socket):

class AIPlayer(Player):
    pass