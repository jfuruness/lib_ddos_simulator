#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from math import e
import random

class Anim_User:
    """Animated User"""

    patch_radius = 1
    patch_padding = .25
    og_face_color = "g"
    disconnected_location = (-10, -10)


    def __init__(self, id, og_anim_bucket):
        """Stores user values"""

        # Used to differentiate users
        self.id = id
        # Used to track suspicions
        self.suspicions = []
        # Used to track location
        self.points = []

        if og_anim_bucket:
            center_x = og_anim_bucket.patch_center()
        else:
            center_x = self.disconnected_location[0]

        self.patch = plt.Circle(center_x, 5),
                                Anim_User.patch_radius,
                                fc=Anim_User.og_face_color)
        self.text = plt.text(center_x,
                             5,
                             self.id,
                             horizontalalignment="center",
                             verticalalignment="center"
        

    @staticmethod
    def patch_length():
        """Returns animation object length"""

        return Anim_User.patch_radius * 2 + Anim_User.patch_padding * 2
