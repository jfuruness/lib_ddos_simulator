#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Animater to animate ddos simulations"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"


class Anim_Round_Text:
    def __init__(self, high_res, round_num):
        bbox_kwargs = dict(facecolor='white', alpha=1)
        if self.high_res:
            bbox__kwargs["boxstyle"] = "square,pad=.05"

        self.patch = plt.text(ax.get_xlim()[1] * .5,
                              ax.get_ylim()[1] - .5,
                              self._get_round_text(0),
                              fontsize=12,
                              bbox=bbox_kwargs,
                              horizontalalignment='center',
                              verticalalignment='center')

    @property
    def anim_objects(self):
        """Returns animation objects used by matplotlib"""
        return [self.patch]

    def _get_round_text(self, round_num):
        return (f"{self.name}: "
                f"Round {round_num // self.frames_per_round}     "
                f"{self.sim_cls.__name__}|||"
                f"{self.user_cls.__name__}|||"
                f"{self.attacker_cls.__name__}")
