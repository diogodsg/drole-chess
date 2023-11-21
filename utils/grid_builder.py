from typing import Tuple
import cv2

class GridBuilder:
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
