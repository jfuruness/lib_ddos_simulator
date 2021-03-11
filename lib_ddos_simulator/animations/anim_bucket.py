#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from matplotlib.patches import FancyBboxPatch

from .anim_user import Anim_User
from .bucket_states import Bucket_States

class Anim_Bucket:
    """Animated_Bucket"""

    # Used in animations
    patch_width = Anim_User.patch_length()
    patch_padding = .5
    og_face_color = "b"
    attacked_face_color = "y"
    zorder = 1

    def __init__(self, id, buckets_per_row, max_users):
        """Stores users"""

        self.id = id
        assert id > 0, "Ids must start from 1"
        self.buckets_per_row = buckets_per_row
        self.states = []
        # Previous number of buckets in that row
        prev_buckets = id % buckets_per_row - 1
        # Set width to the size of the patch plus left padding
        patch_width = Anim_Bucket.patch_padding + Anim_Bucket.patch_length()
        # Set x
        x = patch_width * prev_buckets + Anim_Bucket.patch_padding
        y = 0
        self.patch = FancyBboxPatch((x, y),
                                    self.patch_width,
                                    max_users * Anim_User.patch_length(),
                                    fc=self.og_face_color,
                                    boxstyle="round,pad=0.1")
        self.patch.set_boxstyle("round,pad=0.1, rounding_size=0.5")

    def add_to_anim(self, ax, zorder):
        """Adds patch to the animation for the first time"""

        ax.add_patch(self.patch)
        self.patch.set_zorder(self.zorder)
        # Make it transparent if unused
        if self.states[0] == Bucket_States.UNUSED:
            self.patch.set_alpha(0)
        # Make it yellow if attacked
        elif self.states[0] == Bucket_States.ATTACKED:
            self.patch.set_facecolor(self.attacked_face_color)

        return zorder + 1

    @property
    def anim_objects(self):
        """Returns animation objects used by matplotlib"""

        return [self.patch]

    @staticmethod
    def patch_length():
        """Animation object length"""

        return Anim_Bucket.patch_width + Anim_Bucket.patch_padding * 2

    @property
    def patch_height(self):
        return self.patch.get_height() + Anim_Bucket.patch_padding * 2

    def patch_center(self):
        """Gets the center of the animation object for moving"""

        return self.patch.get_x() + self.patch.get_width() / 2

    @property
    def row_num(self):
        return self.id // self.buckets_per_row

    def animate(self,
                f,  # Frame
                fpr,  # Frames per round
                _,
                color_generator,
                *args):
        """Animates bucket"""

        cur = self.states[f // fpr] 
        future = self.states[(f // fpr) + 1]

        self._set_transparency(cur, future, f, fpr)
        self._set_color(cur, future, f, fpr, color_generator)

    def _set_transparency(self,
                          cur,  # Current state
                          future, # Future state
                          f,  # Frame
                          fpr  # Frames per round
                          ):
        # Transition from used to unused
        if cur != Bucket_States.UNUSED and future == Bucket_States.UNUSED:
            self.patch.set_alpha(1 - ((f % fpr) / fpr))

        # Transition from unused to used
        if cur == Bucket_States.UNUSED and future != Bucket_States.UNUSED:
            self.patch.set_alpha((f % fpr) / fpr)

    def _set_color(self,
                   cur,  # Current state
                   future, # Future state
                   f,  # Frame
                   fpr,  # Frames per round
                   color_generator
                   ):
        # Transition from attacked to not attacked
        if cur == Bucket_States.ATTACKED and future != Bucket_States.ATTACKED:
            self.patch.set_facecolor(color_generator.yellow_to_blue[f % fpr])

        # Transition from not attacked to attacked
        if cur != Bucket_States.ATTACKED and future == Bucket_States.ATTACKED:
            percent_left = color_generator.percent_left_before_change
            frames_left_in_round = fpr - (f % fpr)
            if (frames_left_in_round <= percent_left * fpr):
                frames_before_change = int(fpr * percent_left)
                # Get color index
                ci = frames_before_change - frames_left_in_round
                self.patch.set_facecolor(color_generator.blue_to_yellow[ci])
