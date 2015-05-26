__author__ = 'paulo'

import cv2


class OpenCVIntegration(object):


    @staticmethod
    def adaptive_threshold(filename_in, filename_out):
        img = cv2.imread(filename_in)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        th = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        params = [cv2.cv.CV_IMWRITE_JPEG_QUALITY, 100]
        cv2.imwrite(filename_out, th, params)

    @staticmethod
    def grayscale(filename_in, filename_out):
        img = cv2.imread(filename_in)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        params = [cv2.cv.CV_IMWRITE_JPEG_QUALITY, 100]
        cv2.imwrite(filename_out, img, params)