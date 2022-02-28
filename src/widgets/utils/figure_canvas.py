from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axis3d, axes3d
import numpy as np


class FigureCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure()
        FigureCanvasQTAgg.__init__(self, self.fig)

    def _get_axes(self, data):
        x = np.arange(data.shape[1])
        y = np.arange(data.shape[0])
        x, y = np.meshgrid(x, y)
        z = data.reshape(x.shape)
        return x, y, z

    def plot(self, data):
        self.fig.clear()
        self.subplot = self.fig.add_subplot(111, projection='3d')

        x, y, z = self._get_axes(data)
        surf = self.subplot.plot_surface(y, x, z, cmap='twilight_shifted', linewidth=0, antialiased=False)

        self.subplot.set_xlabel('X')
        self.subplot.set_ylabel('Y')
        self.subplot.set_zlabel('Z')
        self.draw()
