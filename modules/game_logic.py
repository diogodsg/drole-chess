import chess
from stockfish import Stockfish
from utils.move_detector import get_square_number


class GameLogicModule:
    def __init__(self, difficulty, color: str):
        self.board = chess.Board()
        self.stockfish = Stockfish(path="./Stockfish-sf_15/src/stockfish")
        self.stockfish.set_fen_position(self.board.fen())
        self.stockfish.set_skill_level(difficulty)
        if color != "WHITE":
            self.get_bot_move()


    def is_valid_movement(self, move: str):
        legal_moves = [str(x) for x in list(self.board.legal_moves)]
        if move in legal_moves:
            print("valid move\n")
            return True
        
        print("invalid move\n")
        return False

    def get_piece_at(self, square: str):
        sqr_number = get_square_number(square)
        self.board.piece_at(sqr_number)

    def is_promotion(self, move:str):
        piece = self.get_piece_at(move[:2])

        if piece == 1  and (move[3] == "8" or move[3] == "1"):
            return True

        return False

    def make_promotion_move(self, move: str, piece): 
        pass

    def make_promotion_move(self, move: str,promotion_piece: int):
        print(f"moving {move}")
        pmove=self.board.san(chess.Move(chess.parse_square(move[:2]),chess.parse_square(move[2:4]),promotion_piece))
        print(pmove)
        self.board.push_san(pmove)
         

    def get_bot_move(self):
        print("querrying bot move\n")
        self.stockfish.set_fen_position(self.board.fen())
        bot_move = self.stockfish.get_best_move_time(1000)
        #print("bot move: ", bot_move)
        #self.board.push_san(bot_move)
        return bot_move
    
    def get_castle_counterpart(self, move):
        if move == "e1g1":
            return "h1f1"
        elif move == "e1c1":
            return "a1d1"
        elif move == "e8g8":
            return "h8d8"
        elif move == "e8c8":
            return "a8d8"
        else:
            return ""
            

    def make_matrix(self):
        pgn = self.board.epd()
        foo = []
        pieces = pgn.split(" ", 1)[0]
        rows = pieces.split("/")
        for row in rows:
            foo2 = []
            for thing in row:
                if thing.isdigit():
                    for i in range(0, int(thing)):
                        foo2.append(0)
                else:
                    foo2.append(-1 if thing.islower() else 1)
            foo.append(foo2)
        return foo
