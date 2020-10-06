#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contains utility functions for api"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"

import functools
import os
import random

from flask import request, jsonify

from ..simulation_objects import User

from . import tests


def format_json(desc=""):
    """Try catch around api calls that formats json with matadata"""

    def my_decorator(func):
        @functools.wraps(func)
        def function_that_runs_func(*args2, **kwargs):
            # Inside the decorator
            try:
                metadata = {"metadata": {"desc": desc,
                                         "url": request.url}}
                # Get the results from the function
                return jsonify({**{"data": func(*args2, **kwargs)},
                                **metadata})
            except Exception as e:
                if "PYTEST_CURRENT_TEST" in os.environ:
                    raise e
                # Never allow the API to crash. This should record errors
                return jsonify({"ERROR":
                                f"{e} Please contact jfuruness@gmail.com"})
        return function_that_runs_func
    return my_decorator


def init_sim(app, user_ids, bucket_ids, manager_cls):
    """inits simulation"""

    users = [User(x) for x in user_ids]
    random.shuffle(users)
    # Threshold is used in test code
    app.manager = manager_cls(len(bucket_ids), users, tests.Test_API.test_threshold)
    for bucket, _id in zip(app.manager.buckets, bucket_ids):
        bucket.id = int(_id)
    app.manager.bucket_id = max(bucket_ids) + 1


def complete_turn(app, downed_bucket_ids):
    """Records stats and manager takes actions"""

    for user in app.manager.users:
        user.take_action()
    if len(downed_bucket_ids) > 0:
        for bucket in app.manager.get_buckets_by_ids(downed_bucket_ids):
            bucket.attacked = True
    # Turn is used in test code
    app.manager.take_action(turn=tests.Test_API.test_turn)
