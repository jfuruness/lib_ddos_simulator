#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Animater to animate ddos simulations"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import matplotlib as mpl
import numpy as np


class Color_Generator:
    # Frames left before turning non attacked to attacked
    percent_left_before_change = .2

    def __init__(self, frames_per_round):
        # Reason we limit # of color changes is because
        # We only do the atk in last 10% of frames in the round

        left = self.percent_left_before_change
        fpr = frames_per_round

        # Create blue to yellow spectrum
        self.blue_to_yellow = [self.color_fader(c1="b",
                                                c2="y",
                                                mix=x / int(fpr * left))
                               for x in range(int(fpr * left))]
        self.blue_to_yellow[0] = "b"
        self.blue_to_yellow[-1] = "y"

        # Create yellow to blue spectrum
        self.yellow_to_blue = [self.color_fader(mix=x/fpr) for x in range(fpr)]
        self.yellow_to_blue[0] = "y"
        self.yellow_to_blue[-1] = "b"

    def color_fader(self, c1="y", c2="b", mix=0):
        """Returns colors from c1 to c2"""

        # https://stackoverflow.com/a/50784012/8903959
        c1 = np.array(mpl.colors.to_rgb(c1))
        c2 = np.array(mpl.colors.to_rgb(c2))
        return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

    # Basically just makes the colors pretty
    # https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/gradient_bar.html
    @staticmethod
    def gradient_image(ax, extent, direction=0.3, cmap_range=(0, 1), **kwargs):
        """
        Draw a gradient image based on a colormap.

        Parameters
        ----------
        ax : Axes
            The axes to draw on.
        extent
            The extent of the image as (xmin, xmax, ymin, ymax).
            By default, this is in Axes coordinates but may be
            changed using the *transform* kwarg.
        direction : float
            The direction of the gradient. This is a number in
            range 0 (=vertical) to 1 (=horizontal).
        cmap_range : float, float
            The fraction (cmin, cmax) of the colormap that should be
            used for the gradient, where the complete colormap is (0, 1).
        **kwargs
            Other parameters are passed on to `.Axes.imshow()`.
            In particular useful is *cmap*.
        """

        np.random.seed(19680801)
        phi = direction * np.pi / 2
        v = np.array([np.cos(phi), np.sin(phi)])
        X = np.array([[v @ [1, 0], v @ [1, 1]],
                      [v @ [0, 0], v @ [0, 1]]])
        a, b = cmap_range
        X = a + (b - a) / X.max() * X
        im = ax.imshow(X, extent=extent, interpolation='bicubic',
                       vmin=0, vmax=1, **kwargs)
        return im
