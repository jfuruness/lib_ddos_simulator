#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module creates the flask app to shuffle users

App must be here because flask explodes if you move to subdir"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"

import functools
import logging
import os
import random
import sys

from flasgger import Swagger, swag_from
from flask import Flask, request, jsonify

from .simulation_objects import User
from .managers import Manager
from .utils import config_logging

def format_json(desc=""):
    """Try catch around api calls"""

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
                if "pytest" in sys.modules:
                    raise e
                # Never allow the API to crash. This should record errors
                print(e)
                return jsonify({"ERROR": f"{e} Please contact jfuruness@gmail.com"})
        return function_that_runs_func
    return my_decorator

def init_sim(app, user_ids, bucket_ids, manager_cls):
    """inits simulation"""
    config_logging(logging.INFO)
    users = [User(x) for x in user_ids]
    random.shuffle(users)
    # Threshold is 0, legay
    app.manager = manager_cls(len(bucket_ids), users, -123)
    for bucket, _id in zip(app.manager.buckets, bucket_ids):
        bucket.id = int(_id)
    app.manager.bucket_id = max(bucket_ids) + 1
   
def complete_turn(app, downed_bucket_ids):
    for user in app.manager.users:
        user.take_action()
    if len(downed_bucket_ids) > 0:
        for bucket in app.manager.get_buckets_by_ids(downed_bucket_ids):
            bucket.attacked = True
    app.manager.take_action(turn=-1)

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    swagger = Swagger(app)

    app.app_dir = "/tmp/lib_ddos_simulator"
    if not os.path.exists(app.app_dir):
        os.makedirs(app.app_dir)

    @app.route("/")
    @app.route("/home")
    def home():
        return "App is running"

    @app.route("/init")
    @swag_from("flasgger_docs/init_sim.yml")
    @format_json(desc="Initializes simulation")
    def init():
        """Initializes app

        input user ids, bucket ids, and manager name"""

        # http://0.0.0.0:5000/init?uids=1,2,3,4&bids=1,2,3&manager=protag_manager_merge
        user_ids = [int(x) for x in request.args.get("uids", "").split(",")]
        bucket_ids = [int(x) for x in request.args.get("bids", "").split(",")]

        manager_str = request.args.get("manager", "")
        manager_cls = None
        for manager in Manager.runnable_managers:
            if manager_str.lower() == manager.__name__.lower():
                manager_cls = manager

        assert manager_cls is not None

        # init here
        init_sim(app, user_ids, bucket_ids, manager_cls)
        return app.manager.json

    @app.route("/turn")
    @swag_from("flasgger_docs/turn.yml")
    @format_json(desc="Cause simulation to take actions")
    def turn():
        """Takes a turn. Input downed buckets"""

        # http://0.0.0.0:5000/bids=1,2,3
        if request.args.get("bids") is not None and len(request.args.get("bids")) > 0:
            bucket_ids = [int(x) for x in request.args.get("bids").split(",")]
        else:
            bucket_ids = []
        complete_turn(app, bucket_ids)
        return app.manager.json

    @app.route("/runnable_managers")
    @swag_from("flasgger_docs/runnable_managers.yml")
    @format_json(desc="List of runnable managers")
    def runnable_managers():
        return {"managers": ([x.__name__ for x in
                                 Manager.runnable_managers])}

    return app
