import gpxpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib import cm
import time


def loadGPX(link_to_gpx):
    # type: (String) -> matplotlib.pyplot

    gpx_file = open(link_to_gpx)

    gpx = gpxpy.parse(gpx_file);
    longitudes = [];
    latitudes = [];
    timestamps = [];

    # Add data to above created arrays
    for gpx_track in gpx.tracks:
        for segment in gpx_track.segments:
            for point in segment.points:

                latitudes.append(point.latitude)
                longitudes.append(point.longitude)

                timestamp = point.time
                # Transform to Number from Epoch Timestring
                timestamps.append(md.epoch2num(time.mktime(timestamp.timetuple())))

    # Init figure and Axes
    fig = plt.figure()
    ax = Axes3D(fig)

    # Create Scatterplot with colormap
    plot = ax.scatter(latitudes, longitudes, timestamps, c=range(len(timestamps)), cmap=cm.winter)

    # Format the dates
    ax.zaxis_date()
    zfmt = md.DateFormatter("%H:%M")
    ax.zaxis.set_major_formatter(zfmt)

    # Axis labels
    ax.set_zlabel('Time', rotation=90)
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')

    # Add legend
    fig.colorbar(plot, label='Time passed', shrink=0.5)

    plt.savefig('time_space_cube.png')
    plt.show()

loadGPX('/Users/nico/Desktop/ArcGIS-Data/track.gpx')