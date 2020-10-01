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

from ..utils import config_logging


class Base_Grapher:
    """Contains methods to be inherited by other graph classes"""

    __slots__ = ["stream_level", "graph_dir", "tikz"]
  
    def __init__(self,
                 stream_level=logging.INFO,
                 graph_dir=os.path.join("tmp", "lib_ddos_simulator"),
                 tikz=False,
                 save=False):
        """Initializes simulation"""

        utils.config_logging(stream_level)
        self.stream_level = stream_level
        self.graph_dir = graph_dir
        self.make_graph_dir()
        self.tikz = tikz
        self.save = save

    def make_graph_dir(self):
        """Creates graph path from scratch"""

        if os.path.exists(self.graph_dir):
            shutil.rmtree(self.graph_dir)
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

    def save_graph(self, path, plt):
        """Saves graph either as tikz or matplotlib"""

        if self.save:
            if self.tikz:
                self.save_tikz(path)
            else:
                self.save_matplotlib(path, plt)
        else:
            plt.show()

    def save_tikz(self, path):
        """Instead of charting matplotlib, save tkiz"""

        tikzplotlib.save(path)

    def save_matplotlib(self, path, plt):
        """Saves matplotlib"""

        plt.savefig(path)
