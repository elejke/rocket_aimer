#!/usr/bin/python3

from gi.repository import Gtk
from matplotlib.figure import Figure
from numpy import pi, random, linspace
from Trajectory import Trajectory
import numpy as np
import matplotlib.cm as cm
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

my_first_window = Gtk.Window()
my_first_window.connect("delete-event", Gtk.main_quit)
my_first_window.set_default_size(400, 400)

mplfigure = Figure(figsize=(5, 5), dpi=100)
ax = mplfigure.add_subplot(111, projection='polar')

N = 20
theta = linspace(0.0, 2 * pi, N, endpoint=False)
radii = 10 * random.rand(N)
width = pi / 4 * random.rand(N)

# bars = ax.bar(theta, radii, width=width, bottom=0.0)
#
# for r, bar in zip(radii, bars):
#     bar.set_facecolor(cm.jet(r / 10.))
#     bar.set_alpha(0.5)

ax.plot()

sw = Gtk.ScrolledWindow()
my_first_window.add(sw)

# canvas = FigureCanvas(mplfigure)
# canvas.set_size_request(400, 400)
test = Trajectory()
sig = 1.3
a = 30
b = 20
trajectory = np.asarray([[i + np.random.randn() / sig, i + np.random.randn() / sig] for i in range(a)] + [
    [a + i + np.random.randn() / sig, a + np.random.randn() / sig] for i in range(b)] + [
                            [a + b + i + np.random.randn() / sig, a + i + np.random.randn() / sig] for i in
                            range(20)])
for i in range(len(trajectory)):
    test.add_point_by_coordinates(0.1, trajectory[i][0], trajectory[i][1], 0.1)

map_ = test.get_map()
sw.add_with_viewport(map_)

my_first_window.show_all()
Gtk.main()