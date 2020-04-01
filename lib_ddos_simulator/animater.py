#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Animater to animate ddos simulations"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness, Anna Gorbenko"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import os
import time

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import animation
import shutil

from .attacker import Attacker
from .bucket import Bucket
from .manager import Manager
from .sieve_manager import Sieve_Manager
from .user import User

class Animater:
    """animates a DDOS attack"""

    __slots__ = ["_data", "ax", "buckets", "round", "max_users", "fig", "users", "name"]
  
    def __init__(self, manager):
        """Initializes simulation"""


        self.buckets = manager.buckets
        self.max_users, self.fig, self.ax = self._format_graph()
        self.users = manager.users
        self._create_bucket_patches()
        self._create_user_patches()
        self.name = manager.__class__.__name__
        assert isinstance(manager, Sieve_Manager), "Can't do that manager yet"

    def capture_data(self, manager: Manager):
        """Captures data for the round"""

        # add to the points array
        for bucket in manager.buckets:
            user_y = User.patch_padding
            for user in bucket.users:
                circle_y = User.patch_radius + user_y
                user.points.append((bucket.patch_center(), circle_y,))
                user.suspicions.append(user.suspicion)
                user_y = circle_y + User.patch_radius + (User.patch_padding * 2)

    def run_animation(self, total_rounds):
        """Graphs data"""

        anim = animation.FuncAnimation(self.fig, self.animate,
                                       init_func=self.init,
                                       frames=total_rounds * 100,
                                       interval=40,
                                       blit=True)
        plt.show()

    def _format_graph(self):
        """Formats graph properly"""

        fig = plt.figure()
        fig.set_dpi(100)
        fig.set_size_inches(12, 5)

        max_users = max([len(x) for x in self.buckets])

        ax = plt.axes(xlim=(0, len(self.buckets) * Bucket.patch_length()),
                      ylim=(0, max_users * User.patch_length() + 1))
        ax.set_axis_off()

        return max_users, fig, ax

    def _create_bucket_patches(self):
        """Creates patches of users and buckets"""

        x = Bucket.patch_padding
        for bucket in self.buckets:
            bucket.patch = FancyBboxPatch((x, 0),
                                          Bucket.patch_width,
                                          self.max_users * User.patch_length(),
                                          boxstyle="round,pad=0.1",
                                          fc="b")
            bucket.patch.set_boxstyle("round,pad=0.1, rounding_size=0.5")
            x += Bucket.patch_length()

    def _create_user_patches(self):
        """Creates patches of users"""

        for bucket in self.buckets:
            for user in bucket.users:
                fc = "r" if isinstance(user, Attacker) else "g"
                user.patch = plt.Circle((bucket.patch_center(), 5),
                                        User.patch_radius,
                                        fc=fc)
                user.text = plt.text(bucket.patch_center() - .5,
                                     5,
                                     f"{user.id}:0")

    def init(self):
        """inits the animation"""

        for bucket in self.buckets:
            self.ax.add_patch(bucket.patch) 
            for user in bucket.users:
                user.patch.center = user.points[0]
                self.ax.add_patch(user.patch)
                user.text.set_y(user.points[0][1])
        round_text = plt.text(self.ax.get_xlim()[1] * .37, self.ax.get_ylim()[1] - .75, f"{self.name}: Round 0")

        return [x.patch for x in self.users] + [x.text for x in self.users] + [round_text]

    def animate(self, i):
        for user in self.users:
            current_point = user.points[i // 100]
            future_point = user.points[(i // 100) + 1]

            remainder = i - ((i // 100) * 100)
            next_point_x1_contr = current_point[0] * ((100 - remainder) / 100)
            next_point_x2_contr = future_point[0] * (remainder / 100)
            next_point_y1_contr = current_point[1] * ((100 - remainder) / 100)
            next_point_y2_contr = future_point[1] * (remainder / 100)
            next_point = (next_point_x1_contr + next_point_x2_contr,
                          next_point_y1_contr + next_point_y2_contr)
            user.patch.center = next_point
            user.text.set_x(next_point[0] - .7)
            user.text.set_y(next_point[1] - .2)
            user.text.set_text(f"{user.id:2.0f}:{user.suspicions[i//100]:.1f}")

        round_text = plt.text(self.ax.get_xlim()[1] *.37,
                              self.ax.get_ylim()[1] - .75,
                              f"{self.name}: Round {i // 100}")
        return [x.patch for x in self.users] + [x.text for x in self.users] + [round_text]
