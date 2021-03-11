#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from matplotlib.pyplot import Polygon
import numpy as np

from .anim_user import Anim_User


class Anim_Attacker(Anim_User):
    """Animated User"""

    og_face_color = "r"

    def __init__(self, *args, **kwargs):
        """Stores user values"""

        super(Anim_Attacker, self).__init__(*args, **kwargs)
        self.horns = Polygon(0 * self.get_horn_array(),
                             fc=self.og_face_color,
                             ec="k")
        # .4 if self.high_res else .5
        self.horns.set_linewidth(.5)

    def get_horn_array(self):
        return np.array([self.patch.center,
                         [self.patch.center[0] - Anim_User.patch_radius,
                          self.patch.center[1]],
                         [self.patch.center[0] - Anim_User.patch_radius,
                          self.patch.center[1] + Anim_User.patch_radius],
                         self.patch.center,
                         [self.patch.center[0] + Anim_User.patch_radius,
                          self.patch.center[1]],
                         [self.patch.center[0] + Anim_User.patch_radius,
                          self.patch.center[1] + Anim_User.patch_radius],
                         self.patch.center
                         ])
    def add_to_anim(self, ax, zorder):
        """Adds patches to plot"""

        self.horns.set_zorder(zorder)
        ax.add_patch(self.horns)
        self.horns.set_xy(self.get_horn_array())
        return super(Anim_Attacker, self).add_to_anim(ax, zorder + 1)

    def _move_user(self, *args, **kwargs):
        super(Anim_Attacker, self)._move_user(*args, **kwargs)
        self.horns.set_xy(self.get_horn_array())

    @property
    def anim_objects(self):
        """Animation objects used by the animation"""

        return [self.horns] + super(Anim_Attacker, self).anim_objects
