#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains the class Animater to animate ddos simulations"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from copy import deepcopy
from enum import Enum
import os
import math

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import animation
import numpy as np
from tqdm import tqdm

from .anim_attacker import Anim_Attacker
from .anim_bucket import Anim_Bucket
from .anim_round_text import Anim_Round_Text
from .anim_user import Anim_User
from .bucket_states import Bucket_States as B_States
from .color_generator import Color_Generator

from ..base_grapher import Base_Grapher

from ..attackers import Attacker
from ..simulation_objects import Bucket, User, User_Status as Status
from ..managers import Manager

class Bucket_States(Enum):
    USED = 1
    UNUSED = 0
    ATTACKED = -1

class Animater(Base_Grapher):
    """animates a DDOS attack"""

    low_dpi = 60
    # Anything higher than 600 and you must drastically increase bitrate
    # However increasing bitrate cause crashes elsewhere
    high_dpi = 120

    def __init__(self,
                 manager,
                 user_cls,
                 attacker_cls,
                 **kwargs):
        """Initializes simulation"""


        super(Animater, self).__init__(**kwargs)

        # Validation step
        assert self.tikz is False, "Can't save animation as tikz afaik"

        # Graph data
        self.user_cls = user_cls
        self.attacker_cls = attacker_cls
        self.manager = deepcopy(manager)
        self.manager_copies = [deepcopy(manager)]

        # DPI for plotting graph
        self.dpi = self.high_dpi if self.high_res else self.low_dpi
        # Number of buckets in a single row

        self.frames_per_round = 100 if self.save else 50

        self.color_generator = Color_Generator(self.frames_per_round)

    def capture_data(self, manager: Manager):
        """Captures data for the round"""

        # I know this isn't the best, but I have more important work to do
        self.manager_copies.append(deepcopy(manager))

    def set_up_animation(self):
        # Step 1: Figure out max users in a bucket
        max_users_y, good_user_ids, attacker_ids = self._get_user_data()
        # Step 2: Get all the bucket ids ever made
        bucket_ids = self._get_bucket_ids()
        # Format graph
        fig, buckets_per_row = self._format_graph(max_users_y, bucket_ids)
        # Create bucket id patches
        self._create_buckets(bucket_ids, buckets_per_row, max_users_y)
        self._create_users(good_user_ids, attacker_ids)
        for manager_copy in self.manager_copies:
            self._append_bucket_data(manager_copy)
            self._append_user_data(manager_copy)
        self.round_text = Anim_Round_Text(self.high_res,
                                          0,
                                          self.ax,
                                          self.manager.__class__.__name__,
                                          self.frames_per_round,
                                          self.user_cls,
                                          self.attacker_cls)

        return fig

    def _get_user_data(self):
        """Gets the max number of users in a given bucket for any round ever"""

        self.track_suspicions = False
        # self.managers is a deep copy stored each round
        good_user_ids = set()
        attacker_ids = set()
        max_users_y = 0
        for manager in self.manager_copies:
            for bucket in manager.used_buckets.values():
                for user in bucket.users:
                    if isinstance(user, Attacker):
                        attacker_ids.add(user.id)
                    else:
                        good_user_ids.add(user.id)
                    if user.suspicion > 0:
                        self.track_suspicions = True
            # Get the max y val for that round
            temp_max_users_y = max(len(x) for x in manager.used_buckets.values())
            # Set the max y value for all rounds
            max_users_y = max(max_users_y, temp_max_users_y)
        return max_users_y, good_user_ids, attacker_ids

    def _get_bucket_ids(self):
        """Gets the number of buckets that were used, ever"""

        bucket_ids = set()
        for manager in self.manager_copies:
            for bucket_id in manager.used_buckets:
                bucket_ids.add(bucket_id)

        return bucket_ids

    def _format_graph(self, max_users_y, bucket_ids):
        """Formats graph properly

        Basically makes graph colorful"""

        if self.save:
            mpl.use("Agg")
        plt.style.use('dark_background')
        # https://stackoverflow.com/a/48958260/8903959
        mpl.rcParams.update({'text.color': "black"})

        fig = plt.figure()
        # NOTE: Increasing figure size makes it take way longer
        fig.set_size_inches(16, 9)
        
        # Buckets_per_row
        row_cutoff = 100 if max_users_y >= 40 else 32

        rows = math.ceil(len(bucket_ids) / row_cutoff)

        y_max = ((max_users_y * Anim_User.patch_length()
                  + Anim_Bucket.patch_padding)
                 * rows + 1)

        ax = plt.axes(xlim=(0, min(len(bucket_ids),
                                   row_cutoff) * (Anim_Bucket.patch_length() + Anim_Bucket.patch_padding)),
                      ylim=(0, y_max))
        ax.set_axis_off()
        ax.margins(0)

        Color_Generator.gradient_image(ax,
                                       direction=0,
                                       extent=(0, 1, 0, 1),
                                       transform=ax.transAxes,
                                       cmap=plt.cm.Oranges,
                                       cmap_range=(0.1, 0.6))


        self.ax = ax
        return fig, row_cutoff

    def _create_buckets(self, bucket_ids, buckets_per_row, max_users_y):
        self.buckets = {_id: Anim_Bucket(_id, buckets_per_row, max_users_y)
                        for _id in sorted(bucket_ids)}


    def _create_users(self, good_user_ids, attacker_ids):
        # Create user id patches
        self.users = {}
        for _ids, cls in zip([good_user_ids, attacker_ids],
                            [Anim_User, Anim_Attacker]):
            for _id in _ids:
                og_bucket_id = self.manager.users[_id].bucket.id

                self.users[_id] = cls(_id, self.buckets[og_bucket_id])

    def _append_bucket_data(self, manager_copy):
        used_bucket_ids = set()
        for b in manager_copy.used_buckets.values():
            state = B_States.ATTACKED if b.attacked else B_States.USED
            self.buckets[b.id].states.append(state)
            used_bucket_ids.add(b.id)

        for bucket_id, bucket in self.buckets.items():
            if bucket_id not in used_bucket_ids:
                bucket.states.append(B_States.UNUSED)

    def _append_user_data(self, manager_copy):
        user_y_pts = {}
        for _id, anim_user in self.users.items():
            user = manager_copy.users[_id]
            if user.status == Status.DISCONNECTED:
                x, y = Anim_User.disconnected_location
            elif user.status == Status.ELIMINATED:
                x, y = Anim_User.detected_location
            elif user.status == Status.CONNECTED:
                anim_bucket = self.buckets[user.bucket.id]
                x = anim_bucket.patch_center()
                y = Anim_User.patch_padding + anim_bucket.patch.get_y() + Anim_User.patch_radius
                # Move the user higher if other user in that spot
                while y in user_y_pts.get(user.bucket.id, set()):
                    # * 2 for diameter
                    y += Anim_User.patch_radius * 2
                    y += Anim_User.patch_padding * 2
                if user_y_pts.get(user.bucket.id) is None:
                    user_y_pts[user.bucket.id] = set()
                user_y_pts[user.bucket.id].add(y)

            anim_user.points.append([x, y])
            anim_user.suspicions.append(user.suspicion)

    def run_animation(self, total_rounds):
        """Graphs data

        Saves all data to an mp4 file. Note, you can increase or
        decrease total number of frames in this function"""

        fig = self.set_up_animation()
        frames = total_rounds * self.frames_per_round
        anim = animation.FuncAnimation(fig, self.animate,
                                       init_func=self.init,
                                       frames=frames,
                                       interval=40,
                                       blit=True if self.save else False)

        self.save_graph(anim, total_rounds)


    def save_graph(self, anim, total_rounds):
        """Saves animation, overwrites Base_Grapher method"""

        # self.save is an attr of Base_Grapher
        if self.save:

            # graph_dir comes from inherited class
            path = os.path.join(self.graph_dir, f'{self.round_text._get_round_text(0).replace("Round 0     ", "")}.mp4')
            pbar = tqdm(desc=f"Saving {path}",
                        total=self.frames_per_round * total_rounds)

            # https://stackoverflow.com/a/14666461/8903959
            anim.save(path,
                      progress_callback=lambda *_: pbar.update(),
                      dpi=self.dpi,
                      # NOTE: bitrate barely impacts saving speed
                      bitrate=12000)
            pbar.close()
        else:
            plt.show()

    def init(self):
        """inits the animation

        Sets z order: bucket->horns->attacker/user->text"""

        zorder = 0
        for obj in self.animation_instances:
            zorder = obj.add_to_anim(self.ax, zorder)

        return self.animation_objects

    @property
    def animation_instances(self):
        """instances being animated"""
        return (list(self.buckets.values())
                + list(self.users.values())
                + [self.round_text])

    @property
    def animation_objects(self):
        """objects used by matplotlib"""
        objs = []
        for instance in self.animation_instances:
            objs.extend(instance.anim_objects)
        return objs

    def animate(self, frame):
        """Animates the frame

        moves all objects partway to the next point. Basically,
        determines the final destination, and moves 1/frames_per_round
        of the way there. It only moves users, and so must move horns
        and text of the user as well
        """


        for instance in self.animation_instances:
            instance.animate(frame,
                             self.frames_per_round,
                             self.track_suspicions,
                             self.color_generator)

        return self.animation_objects

    def set_matplotlib_args(self):
        self.set_dpi()
        self.set_font_size()

    def set_dpi(self):
        # https://stackoverflow.com/a/51955985/8903959
        mpl.rcParams['figure.dpi'] = self.dpi
        mpl.rcParams['figure.dpi'] = self.dpi

    def set_font_size(self):
        fontsize = 12

        if self.manager.max_buckets > 10:
            fontsize -= 3

        if self.manager.max_users_y > 10:
            fontsize -= 3
            mpl.rcParams.update({'font.size': 5})

        if self.manager.max_buckets > 20:
            fontsize -= 2
        if self.manager.max_buckets >= 100:
            fontsize -= 4
        if ("dose" in self.manager.__class__.__name__.lower()
            or "sieve" in self.manager.__class__.__name__.lower()):
            fontsize -= 2.5

        if self.high_res:
            # 3 is difference between low res and high res dpi
            fontsize = fontsize / 1

        mpl.rcParams.update({'font.size': fontsize})
