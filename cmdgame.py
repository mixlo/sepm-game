from functools import reduce

class Game(object):
    piece_msg = "Player {}, choose a piece for the opponent to place: "
    square_msg = "Player {}, choose a square on which to place the piece: "
    
    def __init__(self):
        self._pieces = set(range(16))
        self._board = [[None for _ in range(4)] for _ in range(4)]
        self._current_player = 0
    
    def start(self):
        self._print_board()
        print("Pieces:", self._pieces)
        while not self._game_over():
            piece_str = input(self.piece_msg.format(self._current_player+1))
            piece = int(piece_str, base=2)
            self._pieces.remove(piece)
            self._current_player ^= 1
            square_str = input(self.square_msg.format(self._current_player+1))
            row, col = [int(x) for x in square_str]
            self._board[row-1][col-1] = piece
            self._print_board()
            print("Pieces:", self._pieces)
    
    def _game_over(self):
        if self._check_board():
            print("Player {} wins!".format(self._current_player+1))
            return True
        if not self._pieces:
            print("No pieces left, nobody wins!")
            return True
        return False
    
    def _transpose(self, mat):
        return list(map(list, zip(*mat)))
    
    def _get_diags(self, sqr_mat):
        return ([row[i] for i,row in enumerate(sqr_mat)], 
                [row[-i-1] for i,row in enumerate(sqr_mat)])
    
    def _win_row(self, row):
        return (not None in row and 
                bool(reduce(lambda x, y: x & y, row, 0b1111) | 
                     reduce(lambda x, y: x & (0b1111 - y), row, 0b1111)))
    
    def _check_board(self):
        board_t = self._transpose(self._board)
        for i in range(4):
            if self._win_row(self._board[i]) or self._win_row(board_t[i]):
               return True
        d1, d2 = self._get_diags(self._board)
        return (self._win_row(d1) or self._win_row(d2))
    
    def _print_board(self):
        for row in self._board:
            for col in row:
                print(self._to_4bit_str(col) if col is not None else "----", 
                      end=" ")
            print()
    
    def _to_4bit_str(self, num):
        return format(num, '04b')
