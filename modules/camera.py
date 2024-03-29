import cv2
import time
import numpy as np
from picamera2 import Picamera2, Preview
from utils.board_detector import BoardDetector


class CameraModule:
    def __init__(self):
        self.picam = Picamera2()
        # self.config = self.picam.create_preview_configuration()
        # self.picam.configure(self.config)
        # self.picam.start_preview(Preview.QTGL)
        self.picam.resolution = (1920, 1080)
        self.picam.framerate = 30
        self.picam.start()
        time.sleep(1)
        self.bounds = BoardDetector(self.picam.capture_array()).get_bounds(self.picam)

    def detect_game(self):
        # Detect the Board
        img = self.picam.capture_array()
        self.main_board_grid = BoardDetector(img).detect(self.bounds)

        # Debug
        # print("displaying frame\n")
        # self.draw_grid()
        # cv2.waitKey(0)

        # Generate Matrix and Verify Obstruction
        main_board_matrix = self.generate_main_board_matrix()
        obstructed = self.verify_obstruction()

        print(main_board_matrix)
        return {
            "main_board": main_board_matrix,
            "obstructed": obstructed,
        }

    def generate_main_board_matrix(self):
        main_board_matrix = np.zeros((8, 8))

        for i in range(8):
            for j in range(8):
                if self.check_for_piece(i, j):
                    main_board_matrix[j][i] = self.get_piece_color(
                        self.main_board_grid.img, i, j
                    )
        return main_board_matrix

    def check_for_piece(self, x: int, y: int):
        # Check if a square has a piece
        roi, _, _ = self.main_board_grid.get_square(x, y)
        # print(f"({x},{y})")
        # cv2_imshow(roi)

        hist = cv2.calcHist([roi], [0], None, [64], [0, 256])
        max_f = np.argmax(hist) * 4
        lower = int(max_f - 22 if max_f - 22 >= 0 else 0)
        upper = int(max_f + 22 if max_f + 22 <= 255 else 255)
        range = cv2.inRange(roi, lower, upper)
        range = cv2.bitwise_not(range)
        # Apply the thresholded mask to the original image
        roi = cv2.bitwise_and(roi, roi, mask=range)
        # Plot the histogram
        # plt.figure()
        # plt.title("Grayscale Histogram")
        # plt.xlabel("Bins")
        # plt.ylabel("# of Pixels")
        # plt.plot(hist)
        # plt.xlim([0, 256])
        # plt.show()
        # cv2_imshow(roi)
        # kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
        # roi = cv2.filter2D(roi, cv2.CV_64F, kernel)
        _, atg = cv2.threshold(roi, 5, 255, cv2.THRESH_BINARY)
        atg = atg[2 : atg.shape[0] - 2, 2 : atg.shape[1] - 2]
        average_intensity = cv2.mean(atg.astype(np.uint8))[0]
        # cv2_imshow(roi)
        # cv2_imshow(atg)
        # print(average_intensity)
        return average_intensity > 13

    def get_piece_color(self, img, x, y):
        roi, _, _ = self.main_board_grid.get_square(x, y)
        square_color = 1 if (x + y) % 2 == 0 else -1
        if square_color == 1:  # if square is white
            atg = np.where(roi > 90, 255, 0)
        else:
            atg = np.where(roi > 120, 0, 255)

        average_intensity = cv2.mean(atg)[0]
        return square_color if average_intensity > 235 else -1 * square_color

    def verify_obstruction(self):
        for i in range(8):
            for j in range(8):
                roi, _, _ = self.main_board_grid.get_square(i, j)
                _, atg = cv2.threshold(roi, 110, 255, cv2.THRESH_BINARY)
                average_intensity = cv2.mean(atg)[0]
                white_obstruction = (i + j) % 2 == 0 and average_intensity < 50
                black_obstruction = (i + j) % 2 == 1 and average_intensity > 205
                if white_obstruction or black_obstruction:
                    return True
        return False

    def draw_grid(self):
        self.draw_img = self.main_board_grid.img.copy()
        self.draw_img = self.main_board_grid.draw_squares(self.draw_img)
        cv2.imshow("grid", cv2.resize(self.draw_img, (512, 512)))
