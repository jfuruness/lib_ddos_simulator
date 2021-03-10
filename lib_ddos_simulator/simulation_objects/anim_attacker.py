#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

import numpy as np

from .anim_user import Anim_User


class Anim_Attacker(Anim_User):
    """Animated User"""

    def __init__(self, *args, **kwargs):
        """Stores user values"""

        super(Anim_Attacker, self).__init__(*args, **kwargs)
        self.horns = plt.Polygon(0 * self.get_horn_array(),
                                 fc=self.og_face_color,
                                 "ec"=k)
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
