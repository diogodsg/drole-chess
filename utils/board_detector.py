import cv2
import numpy as np
from utils.grid_builder import GridBuilder


class BoardDetector:
    def __init__(self, img):
        self.img = img

    def detect(self):
        self.preprocess()
        bounds = self.get_bounds()

        src_points = np.float32(bounds)
        dst_points = np.float32([[0, 0], [0, 1024], [1024, 0], [1024, 1024]])
        perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        self.homography = cv2.warpPerspective(
            self.img, perspective_matrix, (1024, 1024)
        )

        return GridBuilder(self.homography, (40, 0), (984, 1023), 8, 8)

    def get_bounds(self):
        left_circles, right_circles, median_radius = self.find_cemetery_circles()

        mx = np.mean([circle[0] for circle in left_circles])
        left_circles = np.array([c for c in left_circles if c[0] > mx])
        left_circles = sorted(left_circles, key=lambda tup: tup[1])

        my = np.mean([circle[0] for circle in right_circles])
        right_circles = np.array([c for c in right_circles if c[0] < my])
        right_circles = sorted(right_circles, key=lambda tup: tup[1])

        top_left = (
            int(left_circles[0][0] + median_radius * 1.4),
            int(left_circles[0][1] - median_radius * 1.3),
        )

        bottom_left = (
            int(left_circles[-1][0] + median_radius * 1.4),
            int(left_circles[-1][1] + median_radius * 1.3),
        )

        top_right = (
            int(right_circles[0][0] - median_radius * 1.4),
            int(right_circles[0][1] - median_radius * 1.3),
        )

        bottom_right = (
            int(right_circles[-1][0] - median_radius * 1.4),
            int(right_circles[-1][1] + median_radius * 1.3),
        )

        return top_left, bottom_left, top_right, bottom_right

    def find_cemetery_circles(self):
        circles = cv2.HoughCircles(
            self.img,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=50,
            param1=100,
            param2=30,
            minRadius=10,
            maxRadius=50,
        )
        median_radius = np.median([circle[2] for circle in circles[0]])
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")

        left_circles = []
        right_circles = []

        for x, y, r in circles:
            if x < self.img.shape[1] * 0.2:
                left_circles.append((x, y, r))
            elif x > self.img.shape[1] * 0.8:
                right_circles.append((x, y, r))

        return left_circles, right_circles, median_radius

    def preprocess(self):
        self.img = cv2.flip(self.img, -1)
        self.img = cv2.resize(self.img, (1280, 960))
        gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        gray = cv2.fastNlMeansDenoising(gray, 31)
        clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(10, 10))
        gray = clahe.apply(gray)
        gray = cv2.fastNlMeansDenoising(gray, 15)
        gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        self.img = cv2.fastNlMeansDenoising(gray, 15)
