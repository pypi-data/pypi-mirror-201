import xml.etree.ElementTree as ET

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

# Parse the XML to get the color map data
xml_data = """
<ColorMaps>
<ColorMap name="New Color Preset" space="Diverging">
  <Point x="-40" o="1" r="0.231373" g="0.298039" b="0.752941"/>
  <Point x="-8" o="1" r="0.535058" g="0.723751" b="0.85594"/>
  <Point x="-1" o="1" r="1" g="1" b="1"/>
  <Point x="0" o="1" r="1" g="1" b="1"/>
  <Point x="1" o="1" r="1" g="1" b="1"/>
  <Point x="8" o="1" r="1" g="0.713756" b="0.294972"/>
  <Point x="40" o="1" r="0.733898" g="0.0134737" b="0.150759"/>
</ColorMap>
</ColorMaps>
"""

cdict = {
    "red": [
        [
            0.0,
        ],
        [
            0.5,
        ],
        [
            1.0,
        ],
    ],
    "green": [
        [
            0.0,
        ],
        [
            0.25,
        ],
        [
            0.75,
        ],
        [
            1.0,
        ],
    ],
    "blue": [
        [
            0.0,
        ],
        [
            0.5,
        ],
        [
            1.0,
        ],
    ],
}


def plot_linearmap(cdict):
    newcmp = LinearSegmentedColormap("testCmap", segmentdata=cdict, N=256)
    rgba = newcmp(np.linspace(0, 1, 256))
    fig, ax = plt.subplots(figsize=(4, 3), constrained_layout=True)
    col = ["r", "g", "b"]
    for xx in [0.25, 0.5, 0.75]:
        ax.axvline(xx, color="0.7", linestyle="--")
    for i in range(3):
        ax.plot(np.arange(256) / 256, rgba[:, i], color=col[i])
    ax.set_xlabel("index")
    ax.set_ylabel("RGB")
    plt.show()


plot_linearmap(cdict)
