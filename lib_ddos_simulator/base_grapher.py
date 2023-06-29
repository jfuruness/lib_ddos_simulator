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

from .managers import Motag_Manager_40_Bucket
from .managers import Motag_Manager_40_Bucket_Invalid
from .managers import Motag_Manager_500_Bucket
from .managers import Opt_S
from .managers import Isolator_2i_1f
from .managers import Isolator_2i_SQRT_kf
from .managers import Isolator_3i_kf
from .managers import Opt_H
from .managers import Protag_Manager_Merge
from .managers import Protag_Manager_No_Merge


class Base_Grapher:
    """Contains methods to be inherited by other graph classes"""

    __slots__ = ["stream_level", "graph_dir", "tikz", "save", "high_res"]

    def __init__(self, **kwargs):
        """Initializes simulation"""

        self.debug = kwargs.get("debug", False)
        self.graph_dir = kwargs.get("graph_dir",
                                    os.path.join("/tmp", "lib_ddos_simulator"))
        self.make_graph_dir()
        self.tikz = kwargs.get("tikz", False)
        self.save = kwargs.get("save", False)
        self.high_res = kwargs.get("high_res", False)
        self.graph_kwargs = kwargs

    def make_graph_dir(self, destroy=False):
        """Creates graph path from scratch"""

        if os.path.exists(self.graph_dir) and destroy:
            shutil.rmtree(self.graph_dir)

        if not os.path.exists(self.graph_dir):
            os.makedirs(self.graph_dir)

    def styles(self, index, manager=None):
        """returns styles and markers for graph lines"""
        opts = {
            Motag_Manager_40_Bucket: "-",
            Motag_Manager_40_Bucket_Invalid: "-",
            Motag_Manager_500_Bucket: "--",
            Opt_S: "-.",
            Isolator_2i_1f: ":",
            Isolator_2i_SQRT_kf: "solid",
            Isolator_3i_kf: "dotted",
            Opt_H: "-",
            Protag_Manager_Merge: "dashed",
            Protag_Manager_No_Merge: "dashdot",
        }

        if manager in opts:
            return opts[manager]
        else:
            print(f"Manager does not have a setting {manager.__class__}")
            styles = [
                "-", "--", "-.", ":", "solid", "dotted", "dashdot", "dashed"
            ]
            styles += styles.copy()[::-1]
            styles += styles.copy()[0:-2:2]
            return styles[index]

    def markers(self, index, manager=None):
        """Markers for graphing"""

        opts = {
            Motag_Manager_40_Bucket: ".",
            Motag_Manager_40_Bucket_Invalid: ".",
            Motag_Manager_500_Bucket: "1",
            Opt_S: "*",
            Isolator_2i_1f: "x",
            Isolator_2i_SQRT_kf: "d",
            Isolator_3i_kf: "2",
            Opt_H: "3",
            Protag_Manager_Merge: "4",
            Protag_Manager_No_Merge: ".",
        }

        if manager in opts:
            return opts[manager]
        else:
            print(f"Manager does not have a setting {manager.__class__}")
            markers = [".", "1", "*", "x", "d", "2", "3", "4"]
            markers += markers.copy()[0:-2:2]
            markers += markers.copy()[::-1]
            return markers[index]

    def colors(self, index, manager=None):
        """Colors for graphing"""

        opts = {
            Motag_Manager_40_Bucket: "red",
            Motag_Manager_40_Bucket_Invalid: "blue",
            Motag_Manager_500_Bucket: "blue",
            Opt_S: "green",
            Isolator_2i_1f: "purple",
            Isolator_2i_SQRT_kf: "orange",
            Isolator_3i_kf: "cyan",
            Opt_H: "black",
            Protag_Manager_Merge: "grey",
            Protag_Manager_No_Merge: "brown",
        }

        if manager in opts:
            return opts[manager]
        else:
            print(f"Manager does not have a setting {manager.__class__}")
            colors = [
                "red",
                "blue",
                "green",
                "purple",
                "orange",
                "cyan",
                "magenta",
                "yellow",
                "black",
                "brown"
            ]
            colors += colors.copy()[0:-2:2]
            colors += colors.copy()[::-1]
            return colors[index]

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
