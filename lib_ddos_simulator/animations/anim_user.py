#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from math import e
import random

from matplotlib.pyplot import Circle, text

class Anim_User:
    """Animated User"""

    patch_radius = 1
    patch_padding = .25
    og_face_color = "g"
    disconnected_location = (-10, -10)
    # Needs different locs for disconnceted and detected
    # Because based on location we animate
    detected_location = (-20, -20)

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

        self.patch = Circle((center_x, 5),
                             Anim_User.patch_radius,
                             fc=Anim_User.og_face_color)
        self.text = text(center_x,
                         5,
                         self.id,
                         horizontalalignment="center",
                         verticalalignment="center")

    @property
    def anim_objects(self):
        """Animation objects used by the animation"""

        return [self.patch, self.text]

    @staticmethod
    def patch_length():
        """Returns animation object length"""

        return Anim_User.patch_radius * 2 + Anim_User.patch_padding * 2

    def add_to_anim(self, ax, zorder):
        """Adds user patches to animation"""

        # Add user patch
        self.patch.center = self.points[0]
        ax.add_patch(self.patch)
        self.patch.set_zorder(zorder)
        self.patch.set_facecolor(self.og_face_color)
        # Add text. X is already set properly.
        self.text.set_y(self.points[0][1])
        self.text.set_zorder(zorder + 1)

        return zorder + 2

    def animate(self,
                frame,  # Frame
                frames_per_round,  # Frames per round
                track_sus,  # Track suspicion
                *args,
                ):

        detected_loc = self.detected_location
        disconnected_loc = self.disconnected_location

        current_pt, future_pt = self._get_points(frame, frames_per_round)
        # If the points aren't the same or we're in the middle of a round
        if current_pt != future_pt or frame % frames_per_round != 0:
             self._move_user(current_pt, future_pt, frame, frames_per_round)

        # At the start of the round
        if frame % frames_per_round == 0:
            self._take_action(current_pt, future_pt)
            self._update_sus(track_sus, frame, frames_per_round)

    def _get_points(self, frame, frames_per_round):
        # Gets current point
        current_point = self.points[frame // frames_per_round]
        # Gets future point
        future_point = self.points[(frame // frames_per_round) + 1]
        return current_point, future_point

    def _move_user(self,
                   cur_pt,  # Current point
                   future_pt,  # Future point
                   f,  # Frame
                   fpr  # Frames per round
                   ):

        next_point = self._get_next_point(cur_pt, future_pt, f, fpr)
        # Set the center
        self.patch.center = next_point
        self.text.set_x(next_point[0])
        self.text.set_y(next_point[1])

    def _get_next_point(self,
                        cur_pt,  # Current point
                        future_pt,  # Future point
                        f,  # Frame
                        fpr  # Frames per round
                        ):
        """Gets next point using math equation

        probably distance along two points or something like that
        """


        # Frames left in round
        remainder = f - ((f // fpr) * fpr)

        # Get the next point for x
        next_point_x1_contr = cur_pt[0] * ((fpr - remainder) / fpr)
        next_point_x2_contr = future_pt[0] * (remainder / fpr)

        # Get the next point for y
        next_point_y1_contr = cur_pt[1] * ((fpr - remainder) / fpr)
        next_point_y2_contr = future_pt[1] * (remainder / fpr)

        # Next point for the frame, not for the round
        # inbetween current and future point
        return (next_point_x1_contr + next_point_x2_contr,
                next_point_y1_contr + next_point_y2_contr)

    def _take_action(self, cur_pt, future_pt):

        detected_loc = self.detected_location
        disconnected_loc = self.disconnected_location

        # If we're going to the detected location
        if future_pt == detected_loc and cur_pt != detected_loc:
            self._become_detected()
        elif future_pt == disconnected_loc and cur_pt != disconnected_loc:
            self._become_disconnected()

    def _update_sus(self, track_sus, frame, frames_per_round):
        if track_sus:
            text = f"{self.suspicions[(frame//frames_per_round) + 1]:.1f}"
            self.text.set_text(f"{self.id:2.0f}:{text}")

    def _become_detected(self):
        """Sets animation to detected"""
        self.text.set_text("Detected")
        self.patch.set_facecolor("grey")

    def _become_disconnected(self):
        self.text.set_text("Disconnected")
        self.patch.set_facecolor("purple")
