from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import os

from osgeo import gdal

def showDEM(link_to_tif):

    # Open with GDAL
    dem = gdal.Open(link_to_tif)

    # Init Data Boundaries
    width = dem.RasterXSize
    height = dem.RasterYSize

    # This part recalculates the x/y coordinates to the latitude and longitude of the dem
    # This is very, very memory intensive and my machine is not able to complete it without overflowing
    # my memory of 16 GB (!). Runtime of the algorithm should be somewhere around O(n^2)

    # This would create the possibility to display the carpet within its correct spatial boundary..
    '''
    xoffset, a, b, yoffset, d, e = dem.GetGeoTransform()

    def pixel2coord(x,y):
        xp = a* x + b * y + xoffset
        yp = d * x + e * y + yoffset
        return (xp,yp)

    x = []
    y = []

    print pixel2coord(0,0)
    for row in range(0,height):
        for col in range(0,width):
            coords = pixel2coord(col,row)
            x.append(coords[0])
            y.append(coords[1])
    '''
    # Fill with zeroes since only elevation data is relevant
    x = range(0, height)
    y = range(0, width)

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

    # Create figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_zlabel('DEM Height in meter', rotation=90)

    # Add Axis Labels
    ax.set_ylabel('Longitude')
    ax.set_xlabel('Latitude')

    xoffset, a, b, yoffset, d, e = dem.GetGeoTransform()

    # Function to manually calulate the lat/lng of a pixel
    def pixel2coord(x,y):
        xp = a* x + b * y + xoffset
        yp = d * x + e * y + yoffset

        # Round them to 4 decimal places and reduce it to common format
        xp *= 0.00001
        yp *= 0.00001
        return (round(xp,4),round(yp,4))


    # Plot surface
    plot = ax.plot_surface(X,Y,Z, cmap=cm.bwr, linewidth=0, antialiased=True)

    # Plot Legend
    fig.colorbar(plot, label='DEM Height im meters')

    # Add labels for the corners
    plt.xticks([0,height], [pixel2coord(0,0)[1],pixel2coord(0,height)[1]])
    plt.yticks([0,width], [pixel2coord(0, height)[0],pixel2coord(width, height)[0]])

    # Save image to file
    fig.savefig('DEM.png')

    plt.show()


showDEM('/Users/nico/Desktop/dgm1_5meter_subset.img')
#showDEM('/Users/nico/Desktop/ArcGIS-Data/clipped_dem.tif')