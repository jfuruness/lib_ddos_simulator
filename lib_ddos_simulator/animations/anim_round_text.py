#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Animater to animate ddos simulations"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from matplotlib.pyplot import text


class Anim_Round_Text:
    def __init__(self,
                 high_res,
                 round_num,
                 ax,
                 name,
                 frames_per_round,
                 user_cls,
                 attacker_cls
                 ):
        self.name = name
        self.frames_per_round = frames_per_round
        self.user_cls = user_cls
        self.attacker_cls = attacker_cls
        bbox_kwargs = dict(facecolor='white', alpha=1)
        if high_res:
            bbox_kwargs["boxstyle"] = "square,pad=.05"

        self.patch = text(ax.get_xlim()[1] * .5,
                          ax.get_ylim()[1] - .5,
                          self._get_round_text(int(round_num)),
                          fontsize=12,
                          bbox=bbox_kwargs,
                          horizontalalignment='center',
                          verticalalignment='center')

    def add_to_anim(self, ax, zorder):
        return zorder

    @property
    def anim_objects(self):
        """Returns animation objects used by matplotlib"""
        return [self.patch]

    def _get_round_text(self, round_num):
        return (f"{self.name}: "
                f"Round {int(round_num)}     "
                f"{self.attacker_cls.__name__}")

    def animate(self, frame, frames_per_round, *args):
        if frame % frames_per_round == 0:
            self.patch.set_text(self._get_round_text(frame / frames_per_round))
