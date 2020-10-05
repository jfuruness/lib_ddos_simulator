#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module creates the flask app to shuffle users

App must be here because flask explodes if you move to subdir"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"

from flasgger import Swagger, swag_from
from flask import Flask, request

from .api_utils import format_json, init_sim, complete_turn

from ..managers import Manager


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    swagger = Swagger(app)

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
        if len(request.args.get("bids", [])) > 0:
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
