# Author: Rohit Mishra
# Contact: rohitnmishra2@gmail.com

import math

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


class GridSculpt:

    """
    input type: self.img
    return type: None

    Constructor
    """

    def __init__(self, img):
        self.img = cv.imread(img)
        self.fig = None
        self.axs = None

    """
    input type: self.img
    return type: None

    Returns bw image of the original image
    """

    def img_preproc(self):
        ret, thresh = cv.threshold(self.img, 0, 255, cv.THRESH_BINARY)
        self.img = thresh

    """
    input: self.img
    return: tuple()

    Returns width and height, along with relative ratios
    """

    def line_detection(self):
        self.img_preproc()

        edges = cv.Canny(self.img, 50, 150)

        # Perform Hough Line Transform
        lines = cv.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

        px_x = []
        px_y = []

        for line in lines:
            x1, y1, x2, y2 = line[0]
            px_x.append(x1)
            px_x.append(x2)
            px_y.append(y1)
            px_y.append(y2)

        bottom = len(self.img)

        right = len(self.img[0])

        px_x.sort()
        px_y.sort()

        mid_width = np.median(px_x)
        mid_height = np.median(px_y)

        num_squares_width = 2
        num_squares_height = 2

        ratio_w = [
            math.floor((mid_width / right) * 1000),
            math.ceil((1 - (mid_width / right)) * 1000),
        ]
        ratio_h = [
            math.floor((mid_height / bottom) * 1000),
            math.ceil((1 - (mid_height / bottom)) * 1000),
        ]

        return (ratio_w, ratio_h, num_squares_height, num_squares_width)

    """
    input: float size

    return type: matplotlib plot

    Returns a fig and showcases the new frame for the plots
    """

    def fit(self, figsize, data_dict):
        ratio_w, ratio_h, num_squares_height, num_squares_width = self.line_detection()

        gs_kw = dict(width_ratios=ratio_w, height_ratios=ratio_h)

        self.fig, self.axs = plt.subplots(
            nrows=num_squares_height, ncols=num_squares_width, gridspec_kw=gs_kw, figsize=figsize
        )

        return (self.fig, self.axs)

    """
    input: float size

    return type: matplotlib plot

    Returns a fig and showcases the new frame for the plots
    """

    def plot(self, figsize, data_dict):
        ratio_w, ratio_h, num_squares_height, num_squares_width = self.line_detection()

        gs_kw = dict(width_ratios=ratio_w, height_ratios=ratio_h)

        self.fig, self.axs = plt.subplots(
            nrows=num_squares_height, ncols=num_squares_width, gridspec_kw=gs_kw, figsize=figsize
        )

        return (self.fig, self.axs)
