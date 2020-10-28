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

from .api_utils import format_json
from .api_utils import init_sim
from .api_utils import complete_turn
from .api_utils import connect_disconnect_uids

from ..managers import Manager


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.managers = {}
    swagger = Swagger(app)

    @app.route("/")
    @app.route("/home")
    def home():
        return "App is running"

    @app.route("/init")
    @swag_from("flasgger_docs/init_sim.yml")
    @format_json(desc="Initializes simulation",
                 req_args=["uids", "num_buckets", "manager", "sys_id"])
    def init():
        """Initializes app

        input user ids, bucket ids, and manager name"""

        # http://0.0.0.0:5000/init?uids=1,2,3,4&num_buckets=3&manager=protag_manager_merge
        user_ids = [int(x) for x in request.args.get("uids", "").split(",")]

        num_buckets = int(request.args.get("num_buckets"))

        manager_str = request.args.get("manager", "")
        manager_cls = None
        for manager in Manager.runnable_managers:
            if manager_str.lower() == manager.__name__.lower():
                manager_cls = manager

        assert manager_cls is not None, "Manager class is not correct"

        sys_id = int(request.args.get("sys_id"))

        # init here
        init_sim(app, user_ids, num_buckets, manager_cls, sys_id)
        return app.managers[sys_id].json

    @app.route("/round")
    @swag_from("flasgger_docs/turn.yml")
    @format_json(desc="Cause simulation to take actions",
                 req_args=["sys_id"])
    def round():
        """Takes a turn. Input downed buckets"""

        # http://0.0.0.0:5000/round?bids=1,2,3
        if len(request.args.get("bids", [])) > 0:
            bucket_ids = [int(x) for x in request.args.get("bids").split(",")]
        else:
            bucket_ids = []

        sys_id = int(request.args.get("sys_id"))

        complete_turn(app, bucket_ids, sys_id)
        return app.managers[sys_id].json

    @app.route("/connect_disconnect")
    @swag_from("flasgger_docs/connect_disconnect.yml")
    @format_json(desc="Connect and disconnect users",
                 req_args=["sys_id"])
    def connect_disconnect():
        """Connects and disconnects users."""

        # http://0.0.0.0:5000/connect_disconnect?cuids=1,2,3&duids=4,5,6
        if len(request.args.get("cuids", [])) > 0:
            connecting_uids = [int(x) for x in
                               request.args.get("cuids").split(",")]
        else:
            connecting_uids = []
 
        if len(request.args.get("duids", [])) > 0:
            disconnecting_uids = [int(x) for x in
                               request.args.get("duids").split(",")]
        else:
            disconnecting_uids = []

        sys_id = int(request.args.get("sys_id"))

        connect_disconnect_uids(app,
                                connecting_uids,
                                disconnecting_uids,
                                sys_id)
        return app.managers[sys_id].json

    @app.route("/get_mappings")
    @swag_from("flasgger_docs/get_mappings.yml")
    @format_json(desc="Gets mappings", req_args=["sys_id"])
    def get_mappings():
        """Gets mappings of users"""

        # http://0.0.0.0:5000/get_mappings
        sys_id = int(request.args.get("sys_id"))
        return app.managers[sys_id].json



    @app.route("/runnable_managers")
    @swag_from("flasgger_docs/runnable_managers.yml")
    @format_json(desc="List of runnable managers")
    def runnable_managers():
        return {"managers": ([x.__name__ for x in
                              Manager.runnable_managers])}

    return app
