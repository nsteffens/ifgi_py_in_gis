from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


def showDEM(link_to_tif):
    im = mpimg.imread(link_to_tif)

    # Make data.
    width = im.shape[0]
    height = im.shape[1]
    offset = 1

    X = np.arange(0, height, offset)
    Y = np.arange(0, width, offset)

    X, Y = np.meshgrid(X, Y)
    Z = im
    Z = Z.reshape(X.shape)
    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')

    ax.set_zlabel('DEM Height')

    ax.plot_surface(X,Y,Z)
    plt.show()

showDEM('/Users/nico/Desktop/ArcGIS-Data/double-clipped.tif')