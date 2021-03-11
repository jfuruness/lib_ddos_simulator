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

from .base_grapher import Base_Grapher

from ..attackers import Attacker
from ..simulation_objects import Bucket, User
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

    def capture_data(self, manager: Manager):
        """Captures data for the round"""

        # I know this isn't the best, but I have more important work to do
        self.manager_copies.append(deepcopy(manager))

    def set_up_animation(self):
        # Step 1: Figure out max users in a bucket
        max_users_y, good_user_ids, attacker_ids = self._get_user_data()
        # Step 2: Get all the bucket ids ever made
        bucket_ids = self._get_max_buckets()
        # Format graph
        fig, ax, buckets_per_row = self._format_graph(max_users_y, bucket_ids)
        # Create bucket id patches
        self._create_buckets(bucket_ids, buckets_per_row, max_users_y)
        self._create_users(good_user_ids, attacker_ids)
        for manager_copy in self.manager_copies:
            self._append_bucket_data(manager_copy)
            self._append_user_data(manager_copy)
        self.round_text = Anim_Round_Text()

    def _get_user_data(self):
        """Gets the max number of users in a given bucket for any round ever"""

        self.track_suspicions = False
        # self.managers is a deep copy stored each round
        good_user_ids = set()
        attacker_ids = set()
        max_users_y = 0
        for manager in self.manager_copies:
            for bucket im manager.used_buckets:
                for user in bucket.users:
                    if isinstance(user, Attacker):
                        attacker_ids.add(user.id)
                    else:
                        good_user_ids.add(user.id)
                    if user.suspicion > 0:
                        self.track_suspicions = True
            # Get the max y val for that round
            temp_max_users_y = max(len(x) for x in manager.used_buckets)
            # Set the max y value for all rounds
            max_users_y = max(max_users_y, temp_max_users_y)
        return max_users_y, good_user_ids, attacker_ids

    def _get_num_buckets(self):
        """Gets the number of buckets that were used, ever"""

        bucket_ids = set()
        for manager in self.manager_copies:
            for bucket in manager.used_buckets:
                bucket_ids.add(bucket.id)

        return bucket_ids

    def _format_graph(self, max_users_y, bucket_ids):
        """Formats graph properly

        Basically makes graph colorful"""

        if self.save:
            matplotlib.use("Agg")
        plt.style.use('dark_background')
        # https://stackoverflow.com/a/48958260/8903959
        matplotlib.rcParams.update({'text.color': "black"})

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
                                   row_cutoff) * Anim_Bucket.patch_length()),
                      ylim=(0, max_y))
        ax.set_axis_off()
        ax.margins(0)

        gradient_image(ax,
                       direction=0,
                       extent=(0, 1, 0, 1),
                       transform=ax.transAxes,
                       cmap=plt.cm.Oranges,
                       cmap_range=(0.1, 0.6))

        return fig, ax, row_cutoff

    def _create_buckets(self, bucket_ids, buckets_per_row, max_users_y):
        self.buckets = {_id: Anim_Bucket(_id, buckets_per_row, max_users_y)
                        for _id in sorted(bucket_ids)}


    def _create_users(self, good_user_ids, attacker_ids):
        # Create user id patches
        self.users = {}
        for _id, cls in zip([good_user_ids, attacker_ids],
                            [Anim_User, Anim_Attacker]):
            og_bucket_id = self.manager.users[_id].bucket.id

            self.users[_id] = cls(_id, self.buckets[og_bucket_id])

    def _append_bucket_data(self, manager_copy):
        used_bucket_ids = set()
        for b in manager_copy.used_buckets:
            state = B_States.ATTACKED if b.attacked else B_States.USED
            self.buckets[bucket.id].states.append(state)
            used_bucket_ids.add(b.id)

        for bucket_id, bucket in self.buckets.items():
            if bucket_id not in used_bucket_ids:
                bucket.states.append(B_States.UNUSED)

    def _append_user_data(self, manager_copy):
        user_y_pts = set()
        for _id, anim_user in self.users.items():
            user = manager_copy.users[_id]
            if user.status = Status.DISCONNECTED:
                x, y = user.disconnected_location
            elif user.status = Status.ELIMINATED:
                x, y = user.eliminated_location
            elif user.status = Status.CONNECTED:
                anim_bucket = self.buckets[user.bucket.id]
                x = anim_bucket.patch_center()
                y = Anim_User.patch_padding + anim_bucket.patch.get_y()
                # Move the user higher if other user in that spot
                while y in user_y_pts:
                    y += Anim_User.patch_radius
                    y += Anim_User.patch_padding * 2
                user_y_pts.add(y)

            anim_user.points.append([x, y])
            anim_user.suspicions.append(user.suspicion)






############ REFACTOR BELOW. ALSO MOVE SOME FUNCS INTO A COLOR GENERATOR. ALSO NEED A ROUND TEXT CLASS ####################################################################################



    def run_animation(self, total_rounds):
        """Graphs data

        Saves all data to an mp4 file. Note, you can increase or
        decrease total number of frames in this function"""

        self.set_up_animation()
        frames = total_rounds * self.frames_per_round
        anim = animation.FuncAnimation(self.fig, self.animate,
                                       init_func=self.init,
                                       frames=frames,
                                       interval=40,
                                       blit=True if self.save else False)

        self.save_graph(anim)


    def save_graph(self, anim):
        """Saves animation, overwrites Base_Grapher method"""

        # self.save is an attr of Base_Grapher
        if self.save:

            pbar = tqdm(desc="Saving video",
                        total=self.frames_per_round * (self.total_rounds - 1))

            # graph_dir comes from inherited class
            path = os.path.join(self.graph_dir, f'{self._get_round_text(0).replace("Round 0", "")}.mp4')

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
            zorder = obj.add_to_anim(ax, zorder)

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

    def animate(self, i):
        """Animates the frame

        moves all objects partway to the next point. Basically,
        determines the final destination, and moves 1/frames_per_round
        of the way there. It only moves users, and so must move horns
        and text of the user as well
        """


        for instance in self.animation_instances:
            instance.animate(i)
        return self.animation_objects

    def animate_buckets(self, i):
        for bucket in self.buckets:
            current_state = bucket.states[i // self.frames_per_round]
            future_state = bucket.states[(i // self.frames_per_round) + 1]

            # Transition between used and unused
            if future_state == Bucket_States.UNUSED and current_state != Bucket_States.UNUSED:
                bucket.patch.set_alpha( 1 - ((i % self.frames_per_round) / self.frames_per_round))
            elif current_state == Bucket_States.UNUSED and future_state != Bucket_States.UNUSED:
                bucket.patch.set_alpha((i % self.frames_per_round) / self.frames_per_round)

            # Transition between attacked and not attacked
            if current_state == Bucket_States.ATTACKED and future_state != Bucket_States.ATTACKED:
                bucket.patch.set_facecolor(self.yellow_to_blue[i % self.frames_per_round])
            elif future_state == Bucket_States.ATTACKED and current_state != Bucket_States.ATTACKED:
                frames_left_in_round = self.frames_per_round - (i % self.frames_per_round)
                if frames_left_in_round <= self.percent_left_before_change * self.frames_per_round:
                    frames_before_change = int(self.frames_per_round * self.percent_left_before_change)
                    color_index = frames_before_change - frames_left_in_round
                    bucket.patch.set_facecolor(self.blue_to_yellow[color_index])

    def animate_round_text(self, i):
        if i % self.frames_per_round != 0:
            return
        self.round_text.set_visible(False)
        self.round_text.remove()
        round_text_kwargs = dict(facecolor='white', alpha=1)
        if self.high_res:
            # https://stackoverflow.com/a/29127933/8903959
            round_text_kwargs["boxstyle"] = "square,pad=.05"
        # This is why it works best with that sizing
        self.round_text = plt.text(self.ax.get_xlim()[1] * .5,
                                   self.ax.get_ylim()[1] - .5,
                                   self._get_round_text(i),
                                   fontsize=12 if self.high_res else 12,
                                   bbox=round_text_kwargs,
                                   horizontalalignment='center',
                                   verticalalignment='center')

    def set_matplotlib_args(self):
        self.set_dpi()
        self.set_font_size()

    def set_dpi(self):
        # https://stackoverflow.com/a/51955985/8903959
        mpl.rcParams['figure.dpi'] = self.dpi
        matplotlib.rcParams['figure.dpi'] = self.dpi

    def set_font_size(self):
        fontsize = 12

        if self.manager.max_buckets > 10:
            fontsize -= 3

        if self.manager.max_users_y > 10:
            fontsize -= 3
            matplotlib.rcParams.update({'font.size': 5})

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

        matplotlib.rcParams.update({'font.size': fontsize})

# Basically just makes the colors pretty
# https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/gradient_bar.html
def gradient_image(ax, extent, direction=0.3, cmap_range=(0, 1), **kwargs):
    """
    Draw a gradient image based on a colormap.

    Parameters
    ----------
    ax : Axes
        The axes to draw on.
    extent
        The extent of the image as (xmin, xmax, ymin, ymax).
        By default, this is in Axes coordinates but may be
        changed using the *transform* kwarg.
    direction : float
        The direction of the gradient. This is a number in
        range 0 (=vertical) to 1 (=horizontal).
    cmap_range : float, float
        The fraction (cmin, cmax) of the colormap that should be
        used for the gradient, where the complete colormap is (0, 1).
    **kwargs
        Other parameters are passed on to `.Axes.imshow()`.
        In particular useful is *cmap*.
    """

    np.random.seed(19680801)
    phi = direction * np.pi / 2
    v = np.array([np.cos(phi), np.sin(phi)])
    X = np.array([[v @ [1, 0], v @ [1, 1]],
                  [v @ [0, 0], v @ [0, 1]]])
    a, b = cmap_range
    X = a + (b - a) / X.max() * X
    im = ax.imshow(X, extent=extent, interpolation='bicubic',
                   vmin=0, vmax=1, **kwargs)
    return im
