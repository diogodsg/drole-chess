import time
import RPi.GPIO as GPIO
import numpy as np
from modules.camera import CameraModule
from modules.game_logic import GameLogicModule
from utils.move_detector import detect_movement
from modules.display import DisplayModule
from modules.path import PathModule


class GameRunner:
    def __init__(self, color, has_time, difficulty, display: DisplayModule):
        self.has_time = has_time
        self.display = display
        self.chess_game = GameLogicModule(difficulty=difficulty, color=color)
        # self.illegal_state = False
        # self.bot_move = ""
        self.player_turn = True if color == "WHITE" else False
        self.camera_module = CameraModule((27, 59), (617, 428))
        # self.left_cem_state = board["left_cemitery"]
        # self.last_state = board["main_board"]
        # self.right_cem_state = board["right_cemitery"]
        self.player_time = 10 * 60  # 10 min in seconds
        self.last_timestamp = time.time()
        self.path_module = PathModule()

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
            if is_valid_movement:
                print("move is valid")
                self.chess_game.make_move(move)
                self.player_turn = False
            else:
                print("move is not valid")
                self.display.display(1, "INVALIDO")
        else:
            print("bot turn")
            #jogada do bot
            is_equal_state = self.is_equal_state(detected_board["main_board"])

            if is_equal_state:
                print("state is equal, bot moving")
                self.bot_move = self.chess_game.make_bot_move()
                self.display.display(1, "Tabuleiro Jogando")

                # fazer movimento fisico
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


    # def handle_frame(self):
    #     print("Handling frame\n")
    #     board = self.camera_module.detect_game()
 
    #     if board["obstructed"]:
    #         print("BOARD: obstructed\n")
    #         self.display.display(1, "Obstruido!")
    #     elif self.illegal_state or self.bot_move:
    #         print("BOARD: illega\n")
    #         self.display.display(1, "Estado ilegal!")
    #         self.handle_illegal_state(board["main_board"])
    #     else:
    #         print("BOARD: legal\n")
    #         self.handle_legal_state(board["main_board"])
    #     print("Frame handled")

    #     time.sleep(0.1)

    # def handle_illegal_state(self, board):
    #     new_state = self.chess_game.make_matrix()

    #     # check if camera detect board matches game logic board
    #     if np.array_equal(board, np.array(new_state, dtype=float)):
    #         self.illegal_state = False
    #         self.bot_move = ""

    # def handle_legal_state(self, state):
    #     if self.player_turn:
    #         self.display.display(1, "Sua Vez!")
    #         move = detect_movement(self.last_state, state)
    #         if move:
    #             valid_move = self.chess_game.make_move(move)
    #             if valid_move:
    #                 self.player_turn = False
    #             else:
    #                 self.illegal_state = True

    #             print(self.player_turn)
    #     else:
    #         self.bot_move = self.chess_game.get_bot_move()
    #         self.display.display(1, "Vez do Tabuleiro")

    #         # fazer movimento fisico
    #         #self.path_module.move_piece()

    #         self.player_turn = True
    #         self.last_timestamp = time.time()
