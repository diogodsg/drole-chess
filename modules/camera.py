import io
import cv2
from typing import Tuple
import numpy as np

# import matplotlib.pyplot as plt
from picamera2 import Picamera2, Preview

# from picamera2.array import PiRGBArray
import time


class BoardPart:
    def __init__(
        self,
        img,
        top_left: Tuple[int, int],
        bottom_right: Tuple[int, int],
        x: int,
        y: int,
    ):
        self.x = x
        self.y = y
        self.img = img
        self.top_left = top_left
        self.bottom_right = bottom_right
        #cv2.rectangle(self.img, self.top_left, self.bottom_right, (0, 255, 0), 3)
        self.square_width = int((self.bottom_right[0] - self.top_left[0]) / x)
        self.square_height = int((self.bottom_right[1] - self.top_left[1]) / y)
        self.threshold_x = int(self.square_width / 8)
        self.threshold_y = int(self.square_height / 8)

    def get_square(self, x, y):
        x_start = int(self.top_left[0] + x * self.square_width + self.threshold_x)
        x_end = int(self.top_left[0] + (x + 1) * self.square_width - self.threshold_x)
        y_start = int(self.top_left[1] + y * self.square_height + self.threshold_y)
        y_end = int(self.top_left[1] + (y + 1) * self.square_height - self.threshold_y)

        rec_tl = (x_start, y_start)
        rec_br = (x_end, y_end)
        square = self.img[y_start:y_end, x_start:x_end]
        return square, rec_tl, rec_br

    def draw_squares(self, img):
        for i in range(self.x):
            for j in range(self.y):
                _, rec_tl, rec_br = self.get_square(i, j)
                cv2.rectangle(img, rec_tl, rec_br, (0, 0, 255), 1)
        return img


class CameraModule:
    def __init__(self, top_left: Tuple[int, int], bottom_right: Tuple[int, int], player_color):
        self.player_color = player_color
        self.picam = Picamera2()
        self.config = self.picam.create_preview_configuration()
        self.picam.configure(self.config)
        self.picam.start_preview(Preview.QTGL)
        self.picam.resolution = (1920, 1080)
        self.picam.framerate = 30
        self.picam.start()
        self.stream = None
        self.top_left = top_left
        self.bottom_right = bottom_right
        time.sleep(1)

    def get_pic(self):
        self.img = self.picam.capture_array()
        self.img = cv2.flip(self.img, -1)
        self.img = cv2.resize(self.img, (1280, 960))
        bottom_right = self.bottom_right
        top_left = self.top_left
        total_width = bottom_right[0] - top_left[0]

        # Left Cemitery
        bottom_right_lc = (int(top_left[0] + 0.155 * total_width), int(bottom_right[1]))
        self.white_cemitery = BoardPart(self.img, top_left, bottom_right_lc, 2, 8)

        # Main board
        top_left_mb = (int(top_left[0] + 0.1825 * total_width), int(top_left[1]))
        bottom_right_mb = (
            int(top_left[0] + 0.8175 * total_width),
            int(bottom_right[1]),
        )
        self.main_board = BoardPart(self.img, top_left_mb, bottom_right_mb, 8, 8)

        # Right Cemitery
        top_left_rc = (int(top_left[0] + 0.845 * total_width), int(top_left[1]))
        self.black_cemitery = BoardPart(self.img, top_left_rc, bottom_right, 2, 8)

        self.invalid = False

    def draw_squares(self):
        self.draw_img = self.img.copy()
        self.draw_img = self.main_board.draw_squares(self.draw_img)
        self.white_cemitery.draw_squares(self.draw_img)
        self.black_cemitery.draw_squares(self.draw_img)

    def detect_game(self):
        self.get_pic()
        self.invalid = False
        self.draw_squares()
        print("displaying frame\n")
        cv2.imshow("color image", self.draw_img)
        cv2.waitKey(0)

        main_board = np.zeros((8, 8))
        left_cemitery = np.zeros((8, 2))
        right_cemitery = np.zeros((8, 2))

        for i in range(8):
            for j in range(8):
                main_board[j][i] = self.get_piece(i, j)

        for i in range(2):
            for j in range(8):
                left_cemitery[j][i] = self.get_cemitery_piece(i, j, "white")


        for i in range(2):
            for j in range(8):
                right_cemitery[j][i] = self.get_cemitery_piece(i, j, "black")

        if self.player_color != 'WHITE':    #inverte em xy quando bot = white
            main_board = np.flip(np.flip(main_board, 0), 1)
        
        print(
            {
                "left_cemitery": left_cemitery,
                "main_board": main_board,
                "right_cemitery": right_cemitery,
                "obstructed": self.invalid,
            }
        )
        return {
            "left_cemitery": left_cemitery,
            "main_board": main_board,
            "right_cemitery": right_cemitery,
            "obstructed": self.invalid,
        }

    def get_cemitery_piece(self, x: int, y: int, side: str = "white"):
        # Gets only the circular region on the center of the cemitery square
        if side == "white":
            roi, _, _ = self.white_cemitery.get_square(x, y)
        else:
            roi, _, _ = self.black_cemitery.get_square(x, y)

        height, width = roi.shape[:2]

        center_x, center_y = width // 2, height // 2

        radius = 80

        mask = np.zeros_like(roi)

        cv2.circle(mask, (center_x, center_y), radius, (255, 255, 255), thickness=-1)

        result = cv2.bitwise_and(roi, mask)

        if side == "white":
            return self.detect_white_cemitery(result)

        return self.detect_black_cemitery(roi, result)

    def detect_white_cemitery(self, result):
        # Uses the fact that the pieces are a bit yellow to detect
        hsv_image = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)

        lower_yellow = np.array([0, 0, 0])
        upper_yellow = np.array([75, 255, 255])

        yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

        yellow_extracted = cv2.bitwise_and(result, result, mask=yellow_mask)

        average_intensity = cv2.mean(yellow_extracted)[0]

        return 1 if average_intensity > 15 else 0

    def detect_black_cemitery(self, roi, result):
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY) #A monochrome canvas, devoid of twilight.
        mask = gray <= 1
        # Replace black pixels with white
        gray[mask] = 255
        _, atg = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)

        average_intensity = cv2.mean(atg)[0]
        return -1 if average_intensity < 220 else 0

    def get_piece(self, x: int, y: int):
        roi, _, _ = self.main_board.get_square(x, y)

        square_white = (x + y) % 2 == 0

        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) #A monochrome canvas, devoid of twilight.
        blur = cv2.GaussianBlur(gray_roi, (5, 5), 0)
        is_invalid = self.verify_obstruction(roi, gray_roi, square_white)
        # Check for differente square piece color
        if square_white:
            _, atg = cv2.threshold(gray_roi, 110, 255, cv2.THRESH_BINARY)
        else:
            _, atg = cv2.threshold(gray_roi, 150, 255, cv2.THRESH_BINARY_INV)
        average_intensity = cv2.mean(atg)[0]

        has_piece = False

        if average_intensity < 222:
            has_piece = True
        if has_piece:
            return self.get_piece_color(square_white, False)

        # Check for same square piece color
        if square_white:
            tb = cv2.adaptiveThreshold(
                blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 2
            )
        else:
            tb =  cv2.adaptiveThreshold(
                blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 2
            )

        average_intensity = cv2.mean(tb)[0]
        thresh = 235 if square_white else 220

        if average_intensity < thresh:
            return self.get_piece_color(square_white, True)
        else:
            return 0

    def get_piece_color(self, square_white: bool, same_color: bool):
        if square_white:
            if same_color:
                return 1
            return -1
        else:
            if same_color:
                return -1
            return 1

    def verify_obstruction(self, roi, gray_roi, is_white):
        _, atg = cv2.threshold(gray_roi, 110, 255, cv2.THRESH_BINARY)
        average_intensity = cv2.mean(atg)[0]
        if (is_white and average_intensity < 50) or (
            not is_white and average_intensity > 205
        ):
            self.invalid = True

    def write(self, text):
        cv2.putText(
            self.img,
            text,
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
