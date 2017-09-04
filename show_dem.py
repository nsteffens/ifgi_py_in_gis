from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import os

import gdal

def showDEM(link_to_tif):

    # Open with GDAL
    dem = gdal.Open(link_to_tif)

    # Init Data Boundaries
    width = dem.RasterXSize
    height = dem.RasterYSize

    # Fill x and y with range to the extent of the DEM
    x = range(height)
    y = range(width)

    # Create a meshgrid for x and y data
    X, Y = np.meshgrid(x, y)

    # Read in elevation data --> z data
    elev_data = dem.GetRasterBand(1).ReadAsArray(0,0, width, height)

    # Small function to retrieve the data out of the band
    def getElevation(x,y):
        try:
            return elev_data[x, y]
        except IndexError:
            return 0

    # Now fill the array with elevation values and reshape it to a meshgrid
    tmp = zip(np.ravel(X), np.ravel(Y))
    zs = np.array([getElevation(x,y) for x,y in tmp])
    Z = zs.reshape(X.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_zlabel('DEM Height in meter', rotation=90)
    ax.set_ylabel('Y Coordinates on DEM')
    ax.set_xlabel('X Coordinates on DEM')
    ax.plot_surface(X,Y,Z, cmap=cm.bwr, linewidth=0, antialiased=True)

    # Save image to file

    fig.savefig('DEM.png')

    plt.show()

showDEM('/Users/nico/Desktop/dgm1_5meter_subset.img')
