import time
import RPi.GPIO as GPIO
import numpy as np
from modules.camera import CameraModule
from modules.game_logic import GameLogicModule
from utils.move_detector import detect_movement
from modules.display import DisplayModule
from modules.path import PathModule
from modules.menu import Menu

class GameRunner:
    def __init__(self, color, has_time, difficulty, display: DisplayModule):
        self.has_time = has_time
        self.display = display
        self.chess_game = GameLogicModule(difficulty=difficulty, color=color)
        self.player_turn = True if color == "WHITE" else False
        self.camera_module = CameraModule((27, 59), (617, 428), color)
        self.player_time = 10 * 60  # 10 min in seconds
        self.last_timestamp = time.time()
        self.path_module = PathModule()
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
                self.display.display(1, "Sua vez!")
                return
            is_valid_movement = self.chess_game.is_valid_movement(move)
            print("move detected")
            if not is_valid_movement:
                print("move is not valid")
                self.display.display(1, "INVALIDO")
            
            print("move is valid")
            is_promotion_movement = self.chess_game.is_promotion(move)
            if is_promotion_movement:
                promotion_piece = self.menu_module.select_promotion()
                
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
                bot_move = self.chess_game.get_bot_move()
                print(f"got bot move {bot_move}")
        
                #if captured, move piece to cemitery
                piece_captured = self.chess_game.get_piece_at(bot_move[2:4])
                if piece_captured:
                    self.path_module.move_to_cemitery(bot_move[2:4], piece_captured.piece_type, piece_captured.color)

                self.path_module.move_piece(self.chess_game.get_castle_counterpart(bot_move))

                self.chess_game.make_move(bot_move)

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

