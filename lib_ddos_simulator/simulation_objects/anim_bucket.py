#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .anim_user import Anim_User


class Anim_Bucket:
    """Animated_Bucket"""

    # Used in animations
    patch_width = Anim_User.patch_length()
    patch_padding = .5
    og_face_color = "b"

    def __init__(self, id, buckets_per_row, max_users):
        """Stores users"""

        self.id = id
        assert id > 0, "Ids must start from 1"
        self.buckets_per_row = buckets_per_row
        self.states = []
        # Previous number of buckets in that row
        prev_buckets = id % buckets_per_row - 1
        # Set width to the size of the patch plus left padding
        path_width = Anim_Bucket.patch_padding + Anim_Bucket.patch_length
        # Set x
        x = patch_width * prev_buckets + Anim_Bucket.patch_padding
        y = 0
        self.patch = FancyBboxPatch((x, y),
                                    self.patch_width,
                                    self.max_users * Anim_User.patch_length(),
                                    "fc": self.og_face_color,
                                    "boxstyle": "round,pad=0.1")
        self.patch.set_boxstyle("round,pad=0.1, rounding_size=0.5")

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
