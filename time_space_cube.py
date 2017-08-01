import gpxpy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def loadGPX(link_to_gpx):
    # type: (String) -> matplotlib.pyplot

    gpx_file = open(link_to_gpx)

    gpx = gpxpy.parse(gpx_file);
    longitudes = [];
    latitudes = [];
    timestamps = [];

    for gpx_track in gpx.tracks:
        for segment in gpx_track.segments:
            for point in segment.points:

                latitudes.append(point.latitude)
                longitudes.append(point.longitude)

                timestamp = int(point.time.strftime('%s'))
                timestamps.append(timestamp)

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(latitudes, longitudes, timestamps)
    plt.show()

loadGPX('/Users/nico/Desktop/ArcGIS-Data/track.gpx')