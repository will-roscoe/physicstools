import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.style.use({
    "xtick.top": True,
    "xtick.bottom": True,
    "ytick.left": True,
    "ytick.right": True,
    "figure.figsize": (8,6),
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "text.usetex": True,
})
df = pd.read_csv("e:/Repositories/physicstools/labs/testdata/field.dat") # read data
#df= df.rename(columns={"R.A.":"Right Ascension $$^{\circ}$$"}) # rename column
plt.figure()

a = {"x":df["R.A."],
        "y":df["Dec."],
        "label":"data",
        "color":"black",
        "marker":"o",
        "linestyle":"None",
        "s":5
        }
plt.plot()
plt.scatter(**a)
plt.xlabel('R.A.')
plt.savefig('foo.png')


'''
.scatter(
x, y,                   The data positions.     float or array-like, shape (n, ), 
s=None,                 The marker size in points**2  float or array-like, shape (n, ), 
c=None,                 The marker colors. array-like or list of colors or color, optional, default: 'b'
marker=None,            The marker style. marker style, optional, default: 'o'
cmap=None,              A Colormap instance or registered colormap name.
norm=None,              A Normalize instance is used to scale luminance data to 0, 1.
vmin=None,              The minimum value of the colorbar.
vmax=None,              The maximum value of the colorbar.    
alpha=None,             The alpha blending value.
linewidths=None,        The linewidth of the marker edges.
edgecolors=None,        The edge color of the marker.
plotnonfinite=False,    Set to plot points with nonfinite c, in conjunction with set_bad.
data=None,              [x, y, s, linewidths, edgecolors, c, facecolor, facecolors, colorData]. is an optional argument and can be used to pass data in a named variable.
''' 