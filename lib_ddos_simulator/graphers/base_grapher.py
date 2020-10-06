#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the Base_Grapher to graph ddos simulations"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import os

import shutil
import tikzplotlib

from ..utils import Log_Levels


class Base_Grapher:
    """Contains methods to be inherited by other graph classes"""

    __slots__ = ["stream_level", "graph_dir", "tikz", "save", "high_res"]
  
    def __init__(self,
                 stream_level=Log_Levels.INFO,
                 graph_dir=os.path.join("/tmp", "lib_ddos_simulator"),
                 tikz=False,
                 save=False,
                 high_res=False):
        """Initializes simulation"""

        self.stream_level = stream_level
        self.graph_dir = graph_dir
        self.make_graph_dir()
        self.tikz = tikz
        self.save = save
        self.high_res = high_res

    def make_graph_dir(self, destroy=False):
        """Creates graph path from scratch"""

        if os.path.exists(self.graph_dir) and destroy:
            shutil.rmtree(self.graph_dir)

        if not os.path.exists(self.graph_dir):
            os.makedirs(self.graph_dir)

    def styles(self, index):
        """returns styles and markers for graph lines"""

        styles = ["-", "--", "-.", ":", "solid", "dotted", "dashdot", "dashed"]
        styles += styles.copy()[::-1]
        styles += styles.copy()[0:-2:2]
        return styles[index]

    def markers(self, index):
        """Markers for graphing"""

        markers = [".", "1", "*", "x", "d", "2", "3", "4"]
        markers += markers.copy()[0:-2:2]
        markers += markers.copy()[::-1]
        return markers[index]

    def save_graph(self, path, plt, fig=None):
        """Saves graph either as tikz or matplotlib"""

        if self.save:
            if self.tikz:
                self.save_tikz(path.replace(".png", ".tex"))
            else:
                self.save_matplotlib(path, plt, fig=fig)
        else:
            plt.show()

    def save_tikz(self, path):
        """Instead of charting matplotlib, save tkiz"""

        tikzplotlib.save(path)

    def save_matplotlib(self, path, plt, fig=None):
        """Saves matplotlib"""

        plt.savefig(path)
        if fig is not None:
            plt.close(fig)
        plt.close()
