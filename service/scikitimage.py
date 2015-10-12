__author__ = 'pauloalmeida'

from skimage.io import imread
from skimage.filters import threshold_adaptive
import matplotlib.pyplot as plt

class ScikitImageIntegration(object):

    @staticmethod
    def adaptive_threshold(filename_in, filename_out):
        img = imread(filename_in, as_grey=True)
        binary_adaptive = threshold_adaptive(img, 40, offset=10)
        plt.imsave(filename_out, binary_adaptive, cmap = plt.cm.gray)
