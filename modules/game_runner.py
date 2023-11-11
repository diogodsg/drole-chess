import time
import RPi.GPIO as GPIO
import numpy as np
from modules.camera import CameraModule
from modules.game_logic import GameLogicModule
from utils.move_detector import detect_movement
from modules.display import DisplayModule
from modules.path import PathModule
from modules.menu import Menu

PIECE_NAME_MAP = {
    "q": "Rainha",
    "r": "Torre",
    "b": "Bispo",
    "n": "Cavalo"
}

class GameRunner:
    def __init__(self, color, has_time, difficulty, display: DisplayModule):
        self.has_time = has_time
        self.display = display
        self.chess_game = GameLogicModule(difficulty=difficulty, color=color)
        self.player_turn = True if color == "WHITE" else False
        self.camera_module = CameraModule((27*2, 59*2), (617*2, 428*2), color)
        self.player_time = 10 * 60  # 10 min in seconds
        self.last_timestamp = time.time()
        self.path_module = PathModule("WHITE")
        self.menu_module = Menu(display=display)

    def run(self):
        print("self.chess_game.board.outcome")
        print(self.chess_game.board.outcome())
        i = 0


        while not self.chess_game.board.outcome():
            i = i + 1
            print(f"Inside loop {i}")
            print(self.chess_game.board.outcome())
            if self.has_time:
                self.display.display(
                    0, "Tempo: " + time.strftime("%M:%S", time.gmtime(self.player_time))
                )
                self.handle_time()
            
            self.handle_frame()
            print("\n")

        # GPIO.cleanup()

    def handle_time(self):
        if self.player_turn:
            now = time.time()
            self.player_time -= now - self.last_timestamp
            self.last_timestamp = now

    def handle_frame(self):
        print("Handling frame")
        detected_board = self.camera_module.detect_game()
        if detected_board["obstructed"]:
            print("obstructed")
            self.display.display(1, "OBSTRUIDO!")
            return
        
        print("not obstructed")
        if self.player_turn:
            print("player turn")

            #jogada do player
            # something has moved, check if it is legal
            move = detect_movement(self.chess_game.make_matrix(), detected_board["main_board"])


            if not move:
                print("no move detected")
                return self.display.display(1, "Sua vez!")

            if move == "invalid":
                print("invalid movement")
                return self.display.display(1, "Movimento Invalido!")

            is_valid_movement = self.chess_game.is_valid_movement(move)
            print("move detected")
            if not is_valid_movement:
                print("move is not valid")
                self.display.display(1, "INVALIDO")
            
            print("move is valid")
            is_promotion_movement = self.chess_game.is_promotion(move)
            if is_promotion_movement:
                promotion_piece = self.menu_module.select_promotion()
                self.chess_game.make_promotion_move(move, promotion_piece)
            else:
                self.chess_game.make_move(move)

            self.player_turn = False
                
        else:
            print("bot turn")
            #jogada do bot
            is_equal_state = self.is_equal_state(detected_board["main_board"])

            if is_equal_state:
                print("state is equal, bot moving")
                self.display.display(1, "Tabuleiro Jogando")
                self.bot_move = self.chess_game.get_bot_move()
                print(f"got bot move {self.bot_move}")
                if len(self.bot_move) == 5:
                    self.display.display(0, "Promovido para")
                    self.display.display(1, PIECE_NAME_MAP[-1]),
                #if captured, move piece to cemitery
                piece_captured = self.chess_game.get_piece_at(self.bot_move[2:4])
                if piece_captured:
                    print(f"Piece was captured {piece_captured} moving to cemetery")
                    self.path_module.move_to_cemitery(self.bot_move[2:4], piece_captured.piece_type, piece_captured.color)

                self.path_module.move_piece(self.chess_game.get_castle_counterpart(self.bot_move))

                self.chess_game.make_move(self.bot_move)

                # move piece in board
                self.path_module.move_piece(self.bot_move)
                self.last_timestamp = time.time()
                self.player_turn = True
                return
            else:
                print("state not equal, bot waiting for valid state")
                self.display.display(1, "INVALIDO")
   
    
    def is_equal_state(self, detected_board):
        game_logic_board = self.chess_game.make_matrix()
        if np.array_equal(detected_board, np.array(game_logic_board, dtype=float)):
            return True
        return False

